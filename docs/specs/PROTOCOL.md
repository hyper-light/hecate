# SPEC: the claims-plane protocol + hecate-wire

Status: presented for acceptance (grilling Branch 3). Ratified directions: dual-stack
UDP/TCP (static per message class); per-pod HKDF keys with AAD-clear headers; 64-bit
HLC; 24-byte fencing tuple; zerocopy `repr(C)` fixed layers; `hecate-wire` as the
owned payload codec (borsh canonicalization rules × postcard varint density, one
derive macro, decoder rejects non-canonical). References: hyperscale mercury-sync
survey + AD-52, on file in GRILLING.md.

Scope note: **hecate-wire is Rust-only.** The TS/Python skill SDKs speak MCP/JSON at
the tool plane; they never touch the claims plane. Cross-language codec parity is a
non-goal; format stability is guaranteed by committed test vectors instead.

## 1. Envelope

All integers little-endian. Fixed layers are zerocopy `repr(C)` structs — no padding
(statically rejected by `IntoBytes`), explicit-endian field types, compile-time size
asserts.

### 1.1 UDP datagram (stateless — full envelope every datagram)

```
AAD (authenticated, cleartext), 76 bytes:
  ver: u8          protocol major version
  kind: u8         envelope kind (request | response | gossip | probe | ack | ...)
  class: u8        delivery/admission class (§3)
  flags: u8        reserved, must-be-zero (decoder-enforced)
  hlc: u64         48-bit ms since Hecate epoch | 16-bit logical
  cluster_id: u64  random at cluster creation
  epoch: u32       membership epoch
  sender_id: u64   ephemeral per process start (restart ≠ rejoin)
  sender_term: u32
  src_pod: u64
  dst_pod: u64
  key_epoch: u32   rotates at handoff
  request_id: u64  response correlation (explicit — never (peer, handler))
  schema_hash: u64 truncated BLAKE3 of payload schema (one hash family)
  payload_len: u32
crypto:
  nonce: 12 bytes  = 64-bit per-(key, direction) counter | 32-bit channel id.
                   Counter-based, never random; reuse is refused, debug-fatal.
  ciphertext + 16-byte tag  (payload encoded by hecate-wire, then AES-256-GCM)
```

Fixed overhead: **104 bytes**. Datagram payload budget is **derived at the datagram
layer** — `min_mtu(1500) − IP/UDP headers − 104` = 1368 bytes on Ethernet — and the
builder rejects oversize before send (the hyperscale wrong-layer-budget fault, closed).

### 1.2 TCP frame (connection-scoped elision)

A connection opens with HELLO/HELLO-ACK carrying the full identity set (ver,
cluster_id, sender_id, sender_term, key_epoch, capability bits) — version negotiation
happens **at connect**, not at registration. Those fields pin into connection state;
per-frame AAD drops them:

```
len: u32          frame length cap: derived, one cap at every layer (framer =
                  validator = budget; never hyperscale's 1MB-framer-under-3MB-validator)
AAD, 48 bytes:    ver, kind, class, flags, hlc, epoch, src_pod, dst_pod,
                  request_id, schema_hash, payload_len
crypto:           nonce(12) + ciphertext + tag(16)
```

Fencing on TCP: the pinned (cluster, sender, term) is validated against the current
membership view **on every dispatch** (cached compare, ~ns); a term/epoch advance
kills the connection with a typed reason. UDP carries the full tuple per datagram.

### 1.3 Parser-resident enforcement (before any dispatch decision exists)

In order: length caps → AAD parse (flags must-be-zero, version) → fencing check →
AEAD verify (integrity of AAD + payload) → HLC window + replay check (per-sender
bounded seen-window keyed on (sender_id, nonce counter)) → admission (§3) → decode.
The hyperscale lesson is law: replay/integrity live in the parser, never behind a
type-registration lookup. Every rejection is a categorized counter (§5).

## 2. Keys

- Per-pod send keys: `HKDF(master_secret, pod_uid ‖ key_epoch ‖ direction)`, minted
  at summon as part of allocation, held by the pod and the host key table.
- A compromised pod can speak only as itself; it cannot read or forge peer traffic.
  Handoff rotates key_epoch — a lingering predecessor dies at both the key check and
  the fencing check.
- The host network stack (Guardian chokepoint) routes and polices on AAD cleartext;
  it holds the key table and *may* verify tags when policing, but never needs decrypt
  on the fast path.

## 3. Classes and admission

Delivery classes (delta taxonomy → wire): `0 Control` (health, membership, fencing —
critical), `1 Observation` (sheddable), `2 Phase`, `3 Directed` (never shed),
`4 ConsultRequest`, `5 ConsultResolved` (never shed — issuer is parked on it),
`6 StreamData` (credit-governed, §4).

Admission runs in the protocol callback before any task exists: per-class caps +
**named admission groups with reserved slots** (the health plane owns capacity the
data plane cannot touch); Control gets head-of-line scheduling into the next executor
iteration. All caps derived from shard count and queue bounds; every shed is a counted
drop; classes 0/3/5 are never shed — overload surfaces as backpressure to senders
(credit exhaustion or typed retryable errors), never as silent loss.

## 4. Delta streams (TCP)

- Subscribe: `{subject, from_seq}`. Records carry the ledger sequence as
  `stream_seq`; delivery is strictly ordered, no gaps.
- **Credit-based flow control**: the receiver grants explicit record/byte credits;
  the sender halts at zero credit. Deterministic, seed-replayable in SIM — never
  implicit TCP-buffer pressure (hyperscale's never-awaited `drain()` fault, closed
  by construction).
- **Flow-control clauses** (amended 2026-08-17 with `TRANSFER.md`'s acceptance,
  each with its receipt):
  1. Credit exists at **both stream and connection level** (RFC 9113 §5.2 +
     RFC 9000 §4.1: one bulk stream must not exhaust the connection buffer).
  2. Credits are **absolute offsets, QUIC-style** — idempotent under loss and
     reorder; never HTTP/2-style deltas.
  3. Windows are derived as `k × frame_cap` per delivery class and
     **BDP-autotuned** (OpenSSH's 64×-bulk / 4×-interactive pattern is the
     citable derivation shape); the **never-whole-object-in-credit** invariant
     is a permanent test — no grant admits an entire content object into buffer.
  4. Bulk transfer (class 6 carrying `TRANSFER.md` traffic) runs in its own
     delivery class with dumb prioritization — control frames never queue
     behind bulk, which is the frame cap's reason to exist (RFC 9113 §4.2).
- Resume: reconnect with cursor; the server replays forward. Cursor below the
  retention floor → typed `RESYNC_REQUIRED` with a snapshot handle; the client
  re-derives deterministically (watermark-recovery invariant). No best-effort repair
  path exists.
- Idle streams heartbeat inside the stream (liveness is per-stream, not inferred
  from the other stack's failure detector).

## 5. Liveness and observability

- Dedup eligibility is a structural property of each message kind (leader-heartbeat
  liveness lesson, encoded); probes/acks/votes are never content-deduped.
- Terminal-abort barriers checked before dispatch and after handler return; listener
  shutdown is ordered so a restart never inherits a dead process's accept queue.
- Categorized drop counters (rate_limited / too_large / decrypt_failed / malformed /
  replayed / shed / non_canonical), aggregated as a periodic structured log record.
  A drop with no signal is a bug.
- Keepalive is real on TCP; a dead peer is discovered by the owning transport.

## 6. hecate-wire (payload codec)

**Process rule: the format specification document (`docs/specs/WIRE_FORMAT.md`) is
written and merged before the implementation.** Satisfied 2026-08-17 —
`WIRE_FORMAT.md` (accepted) is now the normative format document; this section is
its summary and defers to it on every point, including the two length domains
(`FrameLen`/`ContentLen`), `ContentRef`/`ContentClass`, and the inline-vs-reference
derive law. Canonical-or-reject is the design axiom: for every rule there is a
decoder rejection clause.

- **Integers**: LEB128 varints, minimal-form only (overlong encodings rejected);
  signed via zigzag. **Booleans**: 0x00/0x01 only. **Option**: 0x00/0x01 only.
- **Floats**: permitted; exactly one canonical quiet-NaN bit pattern; −0 normalized
  to +0 on encode; decoder rejects any other NaN/−0 encoding.
- **Strings**: length-prefixed UTF-8; invalid UTF-8 rejected.
- **Maps/sets**: ordered entries are the only legal encoding — out-of-order or
  duplicate keys rejected. (There is no unordered container to mis-serialize; the
  runtime's std-HashMap ban composes with this.)
- **Structs**: fields in declaration order. **Enums**: varint variant index.
- **Evolution**: append-only. New struct fields append as defaulted/Option; new enum
  variants append. The `#[derive(Wire)]` macro checks every type against a
  **committed schema snapshot** — a removed, reordered, or retyped field/variant is a
  *compile error*, not a review hope. Payload compatibility is detected at the parser
  via `schema_hash` (truncated BLAKE3 over the canonical schema encoding).
- **One interpreter**: the derive emits canonical encode, rejecting decode, the
  schema reflection value, the schema hash, and the JSON Schema used by the tool
  plane where a type is shared. No serde, no schemars, no drift surface.
- **Test vectors**: committed corpus adapted from borsh's and postcard's edge cases
  plus our own (varint boundaries, NaN zoo, nested Option, max-depth); format
  stability = vectors never change within a major version.

## 7. Test matrix (failure each catches)

| # | Test | Catches |
|---|---|---|
| P1 | Property fuzz: encode→decode roundtrip identity over arbitrary values | codec correctness |
| P2 | Canonical-reject fuzz: mutated valid encodings (overlong varints, unordered/dup keys, alt NaN, trailing bytes, nonzero flags) → typed error, never acceptance | the content-identity break class |
| P3 | Garbage/truncation fuzz: decoder never panics, bounded time and allocation | untrusted-input DoS |
| P4 | Evolution: appended-field cross-version decode passes; reorder/remove/retype = compile failure (trybuild) against schema snapshot | silent wire breaks |
| P5 | Envelope statics: zerocopy size/alignment/no-padding compile-time asserts; flags must-be-zero runtime enforcement | layout drift, dirty reserved bits |
| P6 | Parser-order: stale epoch/term, replayed nonce, bad tag all rejected with counters **before** any dispatch, verified by instrumentation | enforcement behind dispatch (the never-executed-guard class) |
| P7 | Nonce discipline: per-(key,direction) counter monotonic; reuse refused, debug-fatal | AEAD nonce catastrophe |
| P8 | AAD tamper: any flipped header byte → receiver tag failure; host routing on AAD unaffected until then | header malleability |
| P9 | Admission reserve: data-plane flood in SIM; health-group probes still admitted; sheds counted | control-plane starvation |
| P10 | Stream kill/resume at arbitrary points (SIM): no gap, no duplicate at any cursor; behind-retention → RESYNC path exercised end to end | delta loss/dup; dead resync path |
| P11 | Credit stall: receiver stops granting; sender halts at zero credit; memory bounded; classes 3/5 never dropped | flow-control fiction |
| P12 | MTU: datagram builder rejects payload over derived budget (computed with AAD+tag included) | wrong-layer MTU budget |
| P13 | Fencing sweep: every RPC kind × stale (cluster/epoch/sender/term) combination rejected | zombie senders |

## 8. Acceptance criteria

1. `WIRE_FORMAT.md` merged before the codec implementation lands (process-checked).
2. Continuous fuzz (P1–P3) in CI: zero panics, zero non-canonical acceptances —
   permanent gates, like the WAL power-cut sweep.
3. Parser-resident enforcement order (§1.3) verified by P6 instrumentation on every
   merge; no dispatch path exists that precedes fencing+replay+integrity.
4. Classes 0/3/5 show zero drops across SIM overload sweeps; every sheddable drop is
   counted and aggregated; the drop taxonomy is exhaustive (unknown-drop = bug).
5. One frame cap per stack, derived, identical at framer/validator/budget; UDP
   payload budget computed at the datagram layer including all overhead.
6. Envelope overhead is exactly as specified (104 UDP / 48+len TCP AAD) and
   compile-time asserted; any change is a version bump, not a drift.
7. Schema snapshot committed; breaking type changes fail compilation (P4).
8. Two SIM runs, same (seed, trace): byte-identical frame sequences (inherits
   runtime T1).
9. Every derived constant carries its derivation at the definition site.
