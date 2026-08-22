# SPEC: MONITORING — the observability plane (Scribe, history channel, telemetry, score, interior warden/sensor, VMM truth)

Status: ACCEPTED 2026-08-22 (rewritten to the COLLECTOR bar; the §17 R1–R5 sweep
landed the same day; §18's riders remain the user's open exchanges). The
DESIGN was accepted 2026-08-19 (the accepted-design statement + arc lanes A/B/C +
reconcilers R1–R5, all on file in GRILLING.md); this rewrite adds the mechanics the
transcription compressed — the ring protocol at byte level, the init state machine,
fd custody, the score fold — and carries the R1–R5 corpus amendment sweep as §17,
with the reconcilers' still-open questions flagged as riders (§18), not silently
resolved. Amendments already landed elsewhere are marked. Companions: `PODS.md` (the
pod anatomy + host contract this extends), `HANDOFF.md` (the detection stack),
`HEALTH.md` (content-free + AbsenceIs), `COLLECTOR.md` (ACCEPTED — consumes this
plane; the hot-ring role amendment landed), `TRACING.md` (spans ride these rings),
`RANK.md`/`PLATFORM.md` (score semantics), `AGENTS_RUNTIME.md`, `IAM.md` §6
(residual compile-and-distribute).

## 1. The plane

A pod is **one libkrun microVM per primary agent, running two OCI containers**: the
primary's agent loop in one, its **Scribe** companion's loop in the other (Design A,
containers-per-loop — superseding "one microVM, one agent"; ADR-0006, §17). The
Scribe is a **coordinator atop deterministic substrate** (warden : Guardian ∷
substrate : Scribe) — never a decomposition into a pipeline. It scales 1:1 with
primaries at zero added VMs. The plane is governed by three comms laws (§5); the
cardinal rule is **observe-not-feed**: no path from the Scribe back to the primary,
and no model-controlled path from the primary to the Scribe.

## 1a. The whole machine, in plain terms

An aircraft. The **flight recorder** (the history ring) is bolted to the airframe by
the manufacturer (hecate-init mints it before either occupant boards): the pilot's
instruments write to it continuously and *cannot erase it* (the kernel's seals and
fd permissions, not policy), and it keeps the most recent window of flight —
overwriting the oldest tape, never pausing the aircraft to write. In the jump seat
rides an **investigator** (the Scribe) who can read the recorder and radio the
ground on their own channel, but has **no controls and no intercom to the pilot** —
nothing the investigator does can fly the plane, and nothing the pilot says can
rewrite the investigator's radio (observe-not-feed, in both directions). The
**ground stations** (warden verdicts, VMM counters, host-truth surfaces) track the
aircraft independently — radar doesn't ask the pilot where the plane is
(host-observed provenance; the lie-detector). When the aircraft is lost, the
investigator's last duty is to **pull the recorder's tape and file the report
before the wreckage is cleared** (the tail-drain and the flush-gated teardown).

The analogy carries the three least-obvious choices: the recorder is
**manufacturer-installed, not pilot-installed** (init mints the channel before
spawning either container — neither occupant can forge its custody); the
investigator's notes are **enrichment, never evidence** (verdicts, counters, and
ground tracking are the authority inputs; a compromised cockpit can scribble on its
own tape but cannot alter radar); and the tape **overwrites oldest-first** (a
wedged investigator costs the oldest history, never the newest — the crash's final
seconds are always present).

## 1b. Terms this document uses (reading guide)

- **Primary** — the agent whose work the pod exists for; one per pod.
- **Scribe** — the per-primary companion agent: narrator, history recorder and
  server, handoff judge. First-class, right-sized, resident-idle.
- **hecate-init** — PID 1 in the guest: mounts, mints the channel, spawns and
  supervises both containers, reaps, executes teardown. Mechanism, never authority.
- **History ring** — the supervisor-minted memfd flight-recorder ring + eventfd
  doorbell: the only inter-loop channel, one-way, enrichment-class.
- **Sub-buffer** — the ring's unit of overwrite and of torn-read safety.
- **Stream instance id** — regenerated each time the writer (re)starts; seqnums
  are monotone per instance, so a respawn is visible, never ambiguous.
- **Authority vs enrichment** — the two disjoint signal classes: host-side streams
  (verdicts, deltas, sensor, gateway, kernel liveness) may drive detection, score,
  billing, audit; the ring may only enrich narration and briefs.
- **Bar A / Bar B** — the two adversary tiers: a faulty/degrading primary vs a
  guest-kernel-compromised one.
- **Residual** — the warden-compiled per-pod kernel policy installed into the
  guest pre-spawn (seccomp/cgroup/BPF), pinned so it outlives its drainer.

## 2. Data model

```rust
// ---- the channel objects (minted by init BEFORE any spawn; §4 custody) ----
struct HistoryChannel {
    ring: MemfdRing,            // seals: SHRINK|GROW|SEAL (NOT FUTURE_WRITE — a
                                //   respawned writer must write again)
    cursor: MemfdCursor,        // Scribe-written read position; split custody
    doorbell: EventFd,          // primary writes (batched), Scribe multishot-polls
}
struct RingHeader {             // page 0 of the ring memfd
    magic: u32, layout_ver: u16,
    sub_count: u16,             // S ≥ 2 (derived, §12)
    sub_size: u32,              // B bytes (derived, §12)
    instance: InstanceId,       // REGENERATED on every writer start (§3 protocol)
}
struct SubBufHeader {           // heads each of the S sub-buffers
    seq: u64,                   // monotone per instance; assigned when the writer
                                //   CLAIMS the sub-buffer
    commit: u32,                // valid bytes; written LAST, release-ordered —
                                //   the reader's torn-read guard (§3)
}
struct RecordHeader { len: u16, kind: RecordKind, flags: u8, _seq_lo: u32 }  // 8 B
enum RecordKind {               // STRUCTURED ACTIVITY EVENTS ONLY — closed enum;
    TurnBoundary, ToolDispatch, //   never transcripts, never raw tool output
    ClaimPost, StopReason,      //   (H8-walked; content-free by type)
    Usage, InteriorSpan,        //   TRACING guest-interior spans ride here
    Gap,                        //   reader-emitted downstream on seq jumps
}
struct MemfdCursor { instance: InstanceId, last_seq: u64 }   // Scribe O_RDWR;
                                                             // primary O_RDONLY

// ---- the Scribe (right-sized hecate-rt, 1 shard) ----
struct Scribe {
    ingest: IngestThread,       // ONE thread, io_uring SINGLE_ISSUER, multishot
                                //   poll on the doorbell, batch drain — mechanical,
                                //   kernel-assertable, zero inference
    history: HistoryLog,        // the drained, ordered activity record it serves
    outbound: BlockingPool,     // capped to outbound-channel count: Archivalist
                                //   flush + external reach-out on its OWN vsock flow
    judge: EventDrivenLoop,     // inference ONLY on alerts/consults/narration-worthy
}                               //   events/derived cadence — NEVER per primary turn

// ---- the score service (one per session group; colocation unit) ----
struct ScoreService {
    state: DetHashMap<(AgentUid, Domain), Reputation>,
    applied: LogSeq,            // watermark over its ORDERED input stream
}
enum ScoreInput {               // the stream: logged, ordered, replayable
    OutcomeDelta(LedgerDelta),  //   claim outcomes from the delta stream
    ScribeSnapshot(SignalSnap), //   periodic content-free signal snapshots
}
// state = pure_fold(inputs[..applied]) — outcome-grounded; never turn-shape,
// never self-reported, never the history ring. Recovery = replay (§10).
```

## 3. The history-ring protocol (exact)

**Writer (the primary's runtime, below the model — instrumentation at turn
boundaries, tool dispatch, claim posts; zero token cost, not prompt-injectable,
capture continues mid-inference):**

```
W1 On start/restart: mint a fresh InstanceId into RingHeader; claim sub-buffer 0
   with the next seq. (A respawn is VISIBLE: the reader keys seqnums per instance.)
W2 Emit a record: bump-allocate len+8 bytes in the current sub-buffer (a mapped
   memfd — MEMORY WRITES ONLY; the hot path makes zero syscalls); write header
   then payload.
W3 Sub-buffer full (or the derived batch boundary): store `commit` with release
   ordering (the LAST write), claim the next sub-buffer (wrapping — the ring
   OVERWRITES the oldest sub-buffer; flight recorder, newest always present),
   ring the doorbell (one eventfd write per batch — the only syscall, amortized).
W4 The writer NEVER blocks and NEVER waits on the reader: a wedged Scribe costs
   the oldest unread sub-buffers, nothing else.
```

**Reader (the Scribe's ingest thread):**

```
R1 Doorbell fires (multishot poll) → for each sub-buffer beyond cursor.last_seq:
R2   COPY the sub-buffer out, THEN re-read {seq, commit} (acquire):
       changed during the copy ⇒ the writer lapped us mid-copy ⇒ discard the
       copy, count torn_read, continue (torn data is NEVER parsed)
R3   seq == last_seq + 1 ⇒ parse records [0, commit); append to history
     seq  > last_seq + 1 ⇒ overwritten window ⇒ append a Gap record downstream
       (assembled traces through this window mark incomplete — TRACING TR8)
     new InstanceId      ⇒ writer respawned ⇒ close the old stream, open new
R4   Advance cursor.last_seq (the cursor memfd — the reader's durable-enough
     position; a respawned Scribe resumes exactly here)
```

**Kernel-enforced direction** (not policy): ring = primary `O_RDWR` / Scribe
`O_RDONLY`; cursor = Scribe `O_RDWR` / primary `O_RDONLY` — cross-writes are
`EACCES` from the kernel. Seals `SHRINK|GROW|SEAL` on both memfds. The primary
**pre-faults the ring** at spawn: the memcg charge lands on the primary,
deterministically — *the observed pays for its own black box*.

## 4. The pod interior — architecture, custody, channels

```
GUEST (one microVM)                                HOST (per pod / per node)
┌──────────────────────────────────────────┐
│ hecate-init (PID 1)                      │       warden (host-side, per pod)
│   minted: ring, cursor, doorbell         │         pre-effect on every device
│   installed: warden residuals (pinned)   │         boundary; fail-closed
│ ┌──────────────┐   ┌───────────────────┐ │
│ │ PRIMARY ctr  │   │ SCRIBE ctr        │ │       VMM (libkrun fork): device
│ │ hecate-rt ×N │   │ hecate-rt ×1      │ │         counters + KVM stats-fd
│ │ runtime      │──▶│ ingest thread     │ │       host-truth: schedstat,
│ │ emitters     │ring│ (drain, R1–R4)   │ │         cgroup cpu.stat,
│ │ (below model)│   │ judge (bursty)    │─┼──────▶  smaps_rollup, steal-time
│ │              │   │ outbound pool     │ │vsock
│ │ tools = child│   └───────────────────┘ │flow    node collector rings
│ │ processes    │  sensor (guest kernel   │         (COLLECTOR §3a consumes
│ └──────────────┘  eBPF) + exporter proc ─┼──────▶  all of this plane)
└──────────────────────────────────────────┘sensor vsock
```

**Channel inventory + fd custody** (the corrected R1 count — four vsock flows,
all guest↔host; vsock never carries claims/tools, which ride virtio-net per the
landed PODS dual-stack fix):

| Object | primary | Scribe | init | host side |
|---|---|---|---|---|
| ring memfd | `O_RDWR` (pre-faulted; memcg-charged) | `O_RDONLY` | holder (survives both deaths) | — |
| cursor memfd | `O_RDONLY` | `O_RDWR` | holder | — |
| doorbell eventfd | write | read (multishot) | holder | — |
| control vsock | — | — | endpoint | harness (Control class) |
| Scribe flow vsock | — | pre-connected fd (SCM_RIGHTS at spawn; no guest-visible name) | minted | warden-gated; the Scribe's authority-input + outbound lane |
| sensor vsock | — (guest kernel) | — | liveness-verified at boot | warden (tighten-only) |
| virtio-net | claims + MCP + provider egress | — | — | gateway / Guardian chokepoint |

No other inter-loop object exists; `CID_LOCAL` is rejected (vsock is guest↔host
only); there is **no primary↔Scribe control channel at all**.

## 5. The three comms laws

- **(a) Observe-not-feed** — no Scribe→primary path of any kind; no
  model-controlled primary→Scribe path (no tool, no prompt surface reaches the
  ring; emission is runtime instrumentation below the model).
- **(b) Authority/enrichment split** — the Scribe's *authority* inputs are
  host-side streams on its own vsock flow (warden verdicts, ledger deltas, sensor
  telemetry, gateway usage) + kernel-pushed liveness (pidfd, `cgroup.events`).
  **Detection, scoring, billing, and audit read ONLY these.** The ring is
  enrichment: narration, history serving, handoff-brief continuity. (In series
  identity this is the landed `provenance` dimension — the split survives roll-up.)
- **(c) Context economy** — the primary spends context on work only; history
  events cost zero tokens and cannot be prompt-injected. Any "the agent feeds its
  Scribe after every turn" or "the Scribe reads the primary's transcript" language
  anywhere in the corpus is wrong and dies in §17's sweep.

## 6. hecate-init — the lifecycle, crash-stepped

The five-duty contract (PODS §3) is **re-stated, still exhaustive**, for the
two-container interior (§17 lands it in PODS):

```
I1 MOUNT      declared mount set; verify against the bundle manifest
I2 RESEED     on start and on every snapshot resume (VM-generation bump →
              entropy reinject, clock resync, sensor-channel liveness verified —
              a pod whose sensor won't come up fails summon, loudly)
I3 MINT+INSTALL   mint ring/cursor/doorbell (sealed) BEFORE any spawn;
              install the warden-compiled kernel residuals, PINNED via bpf_link/
              bpffs (enforcement survives its drainer — pin enforcement,
              supervise the drainer); spawn the sensor-exporter process
I4 SPAWN      Scribe FIRST (fds: ring RO, cursor RW, doorbell read, its
              pre-connected vsock flow), then the PRIMARY (ring RW, cursor RO,
              doorbell write; seccomp default-errno + socket(AF_VSOCK)⇒EPERM;
              cgroup memory.max/min + cpu.weight + pids.max from the pod budget;
              Σ memory.max + init overhead ≤ guest RAM — admission-enforced)
I5 SUPERVISE  reap; report lifecycle on the control channel; execute
              shutdown/abort orders
   crash edges:
   Scribe exits  → reap → re-create from the FROZEN bundle → restart with the
                   SAME channel fds (derived backoff; primary unaffected;
                   the respawned Scribe resumes from the cursor)
   primary exits → the Scribe observes race-free (pidfd close + cgroup.events
                   populated→0) → DRAINS THE RING TAIL → emits the death
                   report + final narration flush → init tears the VM down —
                   teardown is GATED on the Scribe's flush (never before)
   VM/init dies  → no interior actor remains: the colocation unit's checkpointed
                   detection substrate + the health plane drive replacement
                   (the R1 §7 correction — "the Scribe drives replacement" is
                   wrong when the VM itself dies); the successor's brief = the
                   last flushed window
```

**The pool-fill split (b′, accepted 2026-08-22)**: container *creation* (rootfs
mounts, cgroup skeletons) and the channel *mint* are identity-free and may run at
pool-fill (PODS §4); I2's reseed, I3's key derivation + residual install, and
I4's *starts* always run at assignment — the ordering law binds **start**, the
moment code runs, which is exactly what makes pre-creation legal.

Every step is idempotent; kill-fuzz at each boundary is T20–T24's job (§17).

## 7. Telemetry pipeline (role, post-COLLECTOR)

The per-node emission rings are the **source buffers** (bounded,
doorbell-drained); storage, retention, roll-up, and federation are the
collector's (`COLLECTOR.md`, accepted — the role amendment is landed in this
file's §5 note). What this spec owns is the emission plane: per-loop resource
envelopes read from the per-container cgroup files; **bounded-cardinality keys
only**; `HEALTH.md`'s content-free law + AbsenceIs carry through (a signal type
carrying a raw key/body/channel fails the H8 type-walk at CI). Execution spans
ride these same rings (`TRACING.md` §7) — no tracing-specific channel exists.

## 8. The score service

A **deterministic harness task in the colocation unit** (one per session group),
**single-writer**, summoned in the unit's gang admission (SESSIONS §2 — landed).
Per-`(agent, domain)` reputation as a **pure fold over its ordered input stream**
(ledger outcome deltas + Scribe signal snapshots — both *logged inputs*):

```rust
fn fold(state: &mut Reputation, input: &ScoreInput) { /* outcome-grounded only */ }
// applied advances with each input; recovery = checkpoint + replay of the logged
// stream — byte-identical (MO5). One authoritative copy: learner ≡ decision.
```

It is **not a CONSENSUS standing writer** — its sole ledger-directed output is
the modulation snapshot pushed as an ordinary logged core input through the front
door; it holds no lease, no epoch, no resource (the R4 roster finding resolves as:
an ordinary claims-plane *client*, boot-classified as such — the roster's
lease/CAS/writer-less trichotomy covers resource owners, which it is not; §17
lands the CONSENSUS note). `RANK.md` §4 semantics (prevalence/specificity/trust,
demote-only, observe-mode-first) are unchanged — this supplies the architecture
RANK deferred (§17 lands the pointer).

## 9. Warden & sensor — the two-workload interior

The PODS §6 host contract, extended (§17 lands the qualification):

- **Warden** — host-side, per-pod, pre-effect at every device-boundary crossing,
  compiled policy (SafetyPolicy + IAM residual + capability atoms + claim
  scopes), hold-and-escalate, fail-closed. Unchanged — and it now also gates the
  Scribe's flow (per-workload flow keys: a compromised primary cannot forge as
  its Scribe even at Bar A — landed 2026-08-22, WIRE_SECURITY §3).
- **Interior enforcement** = warden-compiled kernel residuals installed by init
  pre-spawn (I3), **pinned** — the Kata precedent: policy compiled outside,
  installed at spawn, enforced inside; `IAM.md` §6's compile-and-distribute
  extended one hop into the guest.
- **Interior observation** = the sensor with **per-container attribution**
  (`bpf_get_current_cgroup_id`) and the **denial-event export**: seccomp denials
  (via a deny-only `SECCOMP_RET_USER_NOTIF` listener where denials are
  rare-by-design — no `FLAG_CONTINUE`, no target deref, `ENOSYS`-fail-closed on
  supervisor death — or `RET_ERRNO + FILTER_FLAG_LOG`, or cgroup-BPF), cgroup
  events, tripwire firings — formerly silent, now counted. A **dedicated
  in-guest sensor-exporter process** (supervised by init, never PID 1 itself)
  drains the kernel rings to the sensor vsock; on drainer death the pinned
  programs keep enforcing and ring records persist until the ring fills — then
  reserve fails with counted drops, never blocking the workload.
- **Stock vs fork**: on stock libkrunfw (6.12.91): seccomp+unotify, the full
  cgroup-v2 event surface, cgroup-BPF UNIX interception. The **guest-kernel
  fork-flip list** (tracked, config-as-code): (1) `BPF_JIT` both arches;
  (2) `SECURITY`+`SECURITYFS` aarch64; (3) the `BPF_LSM` stack both;
  (4) `DEBUG_INFO_BTF` both; (5) `PSI` x86_64; (6) `AUDIT`+`AUDITSYSCALL`
  aarch64 (only if the audit route is chosen); (7) optional `KPROBES`,
  `IKCONFIG(_PROC)`. The flip harmonizes the arch asymmetry and unlocks BPF-LSM
  cross-container hooks + raw syscall-rate telemetry.
- **Sensor invariants unchanged**: fixed image-hashed programs, tighten-only,
  **silence is a signal** (channel death ⇒ the warden escalates everything).

## 10. VMM-observed truth (the lie-detector)

libkrun exports **zero** stats today; the fork adds **Firecracker-shaped
first-party device counters** (virtio-fs op counts by opcode; vsock per-port
flows + RST counts — a guest connect to a silent port is a VMM-authored RST,
every attempt countable; net counters incl. `tx_spoofed_mac`; queue events) plus
a **KVM `GET_STATS_FD`** collector (`halt_exits`, `halt_wait_ns`, exits,
io/mmio, hypercalls, insn_emulation), symmetric on WHP and self-counted on HVF.
Host-truth surfaces the guest cannot fake: `/proc/<pid>/schedstat`, the
VMM-cgroup `cpu.stat usage_usec`, `smaps_rollup`/`RssAnon`, the steal-time MSR.

Every metric is provenance-classed (`HostObserved`/`GuestReported` — the landed
series dimension); **cross-view divergence is itself a signal**. The seven-row
lie-detector: idle/spin (host-authoritative — claimed-idle + no halt exits +
full vCPU runtime = spinning); memory (split: host owns footprint+freshness,
guest owns semantics); hidden-process (cross-view); stream liveness (device
counters self-refute under-reporting); actor attribution (guest-authoritative
with host veto via boundary signature); starvation (host-manufactured, cleanest);
boundary probing (host-authoritative — the guest cannot suppress the host's
count of its own refused attempts).

## 11. Failure & recovery matrix

| What dies | What is lost | Counted where | What recovers, from where |
|---|---|---|---|
| The Scribe | nothing (the ring buffers) | respawn + backoff counters | init re-creates from the frozen bundle; same fds; resumes at the cursor; a long outage costs the OLDEST sub-buffers (gap records), never the newest |
| The primary | in-flight turn (parked on the ledger by construction) | lifecycle events | the Scribe tail-drains the ring (commit-stamped bytes only), emits the death report; teardown flush-gated; the successor's brief carries the drained tail |
| Both containers | as above, in either order | lifecycle events | init supervises both independently; the ring memfds live in init's fd table — they survive both |
| init / the VM | the interior, wholesale | control-channel death, host-observed | the colocation unit's checkpointed detection substrate + health plane drive replacement; brief = last flushed window (the R1 §7 correction) |
| The sensor / its exporter | interior *observation* granularity | silence-is-a-signal | enforcement is PINNED (survives); the warden flips to escalate-everything; exporter respawn drains the backlog until ring-full (counted) |
| The doorbell (stall) | drain latency | derived stall alarm | the reader also drains on its own derived cadence check — the doorbell is an accelerator, not the only trigger |
| The score service | nothing durable | task respawn | replay: checkpoint + the logged input stream ⇒ byte-identical state (MO5) |
| A cursor/ring memfd (corrupt at Bar B) | that pod's enrichment | classification | contained: the ring is never an authority input (MO2); every authority stream is host-side |

## 12. Derived constants

| Constant | Formula | Anchors |
|---|---|---|
| Ring size (S × B) | event-rate ceiling × max drain gap (incl. the Scribe restart-backoff ceiling); S ≥ 2 | measured emission rates, backoff ceiling |
| Sub-buffer size B | batch-efficiency knee of the drain path | measured drain cost |
| Doorbell batch bound | syscall amortization target ÷ record rate | measured syscall cost |
| Scribe cgroup floor | resident-idle footprint × derived headroom | measured Scribe RSS |
| Scribe judge cadence | narration budget ÷ event salience rate | narration budget |
| Respawn backoff | derived ladder from failure-rate anchors | observed crash rates |
| Score snapshot cadence | RANK modulation freshness bound | RANK's declared freshness |
| Sensor ring / exporter batch | denial-rate ceilings × drain gap | measured denial rates |

## 13. Worked example — one turn, then a death

1. **A turn**: the Engineer's runtime emits `TurnBoundary`, two `ToolDispatch`
   digests, a `ClaimPost`, `Usage`, `TurnBoundary` — six records, ~400 bytes,
   memory-writes into sub-buffer seq 42; `commit` stamps; the doorbell rings once.
   The Scribe's ingest thread drains R1–R4, appends to history. **No inference
   runs** — nothing was narration-worthy; the judge stays idle (thread census
   N+1, not 2N).
2. **Authority in parallel**: the same turn's warden verdicts, gateway usage, and
   ledger deltas arrive on the Scribe's vsock flow — these, not the ring, feed
   any judgment (MO2).
3. **The death**: the primary is OOM-killed mid-turn 43. Init reaps; the Scribe
   sees pidfd-close + `cgroup.events` populated→0 (race-free, kernel-pushed).
   It drains sub-buffer 43's committed bytes (the partial turn's real prefix —
   the commit stamp is why torn tails are never mis-read), emits the death
   report, flushes narration to the Archivalist on its outbound pool — and only
   then does init tear down (the flush gate). The successor's handoff brief
   carries the drained tail; the parked turn resumes from the ledger.
4. **The failure variant**: instead, the *Scribe* wedges during an emission
   flood. The primary never notices (W4 — it never blocks); sub-buffers 44–47
   overwrite 40–43. The respawned Scribe reads cursor `last_seq=39`, sees seq 44
   next ⇒ emits one `Gap` for 40–43, counted; the *newest* history — the part a
   handoff needs — is intact. Flight recorder, exactly.

## 14. Trust model

**Bar A** (faulty/degrading primary): every intra-guest mechanism holds — the
kernel-enforced ring direction, the seals, the residuals, per-workload flow keys
(the primary cannot forge as its Scribe). **Bar B** (guest-kernel compromised):
every intra-guest mechanism is forfeit **by assumption** — and the design holds
anyway, because nothing authority-grade lives in the guest: the warden, the VMM
counters, host-truth surfaces, the host-computed score, and the collector's
provenance dimension are all host-side; the ring at Bar B is contained **by
classification** (enrichment-only, MO2), and a Bar-B guest lies only as itself,
about itself, in streams already marked `GuestReported`.

## 15. Laptop degenerate

`N=1`: the same two containers in the one microVM, the same channel, the same
laws; the score service and detection substrate in the one colocation unit; the
emission rings drain to the one node collector. Zero modes.

## 16. Integration (every companion touchpoint)

- **PODS** — the anatomy this spec defines lands there (§17): pod definition,
  the re-stated init contract, the channel inventory, the two-workload §6
  qualification, the §7 crash correction, tests T20–T24.
- **HANDOFF** — consumes the authority streams and the detection substrate
  (a stage of the collector pipeline, per its accepted stage-not-consumer rule);
  the Scribe judges; briefs carry drained tails.
- **COLLECTOR** (accepted) — consumes this plane; the hot-ring role and
  provenance-dimension amendments are landed; the capture/detection colocation
  homes are landed.
- **TRACING** — guest-interior spans are `RecordKind::InteriorSpan` on the ring;
  host chokepoints emit to the node rings; the provenance split carries.
- **HEALTH** — content-free H8 walks every record kind; AbsenceIs covers sensor
  silence and stalled drains.
- **IAM** — §6 residual compile-and-distribute extends into the guest (I3); the
  Scribe is a principal with its own flow identity.
- **RANK / PLATFORM** — score semantics unchanged; §17 lands the architecture
  pointers and the stale "derived on demand"/"cannot outright block" fixes.
- **AGENTS_RUNTIME / AGENTS / CONTEXT** — the per-turn-feed language dies; pod =
  two minds; "sidecar"→"companion"; the glossary changes ride the same commit
  (the glossary-wins hazard, §17).
- **REGISTRY** — the Scribe's `AgentRole` declares the structural-1:1-companion
  scaling class (a primary's summon resolves its companion); two-bundle pods.
- **SESSIONS / SCHEDULER** — colocation-unit membership (landed); two-container
  admission: the requirement vector sums both containers + init; Σ memory.max
  bound admission-enforced.
- **CONSENSUS** — the score service is an ordinary claims-plane client, not a
  roster writer (§8's resolution; §17 note).
- **FAULTS / SIM** — the nemesis vocabulary gains pod-interior classes
  (container-exit orderings, ring-overrun, doorbell-stall); ring loss is typed
  in-protocol gap records, never a rebuild-from-quorum disposition (§18 rider
  set R3).

## 17. Amendments landing with acceptance (the R1–R5 sweep, one coordinated commit)

**PODS**: §1 pod definition (primary + Scribe, two containers, N+1 census,
one-way ring, no shared netns/volumes; ADR-0006 cited); §3 the init contract
re-stated exhaustive (§6's I1–I5 — mint-then-spawn-two, residual install,
scribe-first, supervise-both, tail-drain hold, flush-gated teardown) + the
four-flow channel inventory; §6 the two-workload qualification + denial export;
§7 the crash bullet (colocation substrate drives replacement); tests T20–T24
(Scribe respawn / tail-drain / channel-tamper / interior-residuals / census);
acceptance-criterion 2's five-duty count updated. **VFS**: two container rootfs
subtrees as RO lowerdirs; upper-on-tmpfs-per-container; work volumes mount the
PRIMARY container only (Scribe attachment-free by law); V12 intra-pod isolation
test. **SERVING**: container-upper writes never reach the machine (AC-1 note).
**RUNTIME**: per-process shard counts bundle-declared (primary N-from-cores,
Scribe clamped to 1); census N+1. **AGENTS_RUNTIME**: :4–7 (two hecate-rt
processes; history *emitter*, not "Scribe feed"; primary N shards), :21–23 (a
pod = two minds), :48–50 (TS/Py exec contradiction → SKILLS_API's law), :95–96
(no primary narration flush), :127 (acceptance criterion 5 — the corpus's only
literal per-turn-feed line → runtime-emits-below-model + teardown-gates-on-
flush), §6 handoff sequence (+ the four statement-§7 elements). **AGENTS**: the
six conflicts (anatomy, Guardian-can-deny, perf-handoff = adjudication,
detection-substrate-analyzes/Scribe-judges, score pushed-not-derived,
"sidecar"→"companion" ×3) — **in the same commit as CONTEXT** (glossary-wins).
**CONTEXT**: Pod + Scribe definitions corrected; new entries (History channel,
Runtime emitter, hecate-init, Detection substrate, Score service, Provenance
class). **PLATFORM**: §4 "cannot outright block" → the Guardian can deny
(fresh-probe-fail ⇒ task-hard ⇒ deny); §5 conduct analysis → substrate detects /
Scribe judges / Guardian adjudicates; §6 "derived on demand" → the pushed
single-writer architecture. **RANK**: §4 gains the MONITORING §8 pointer;
:56–59 stale trigger language; :70–71 + AC-4 → "writes no ledger objects; its
sole ledger-directed output is the modulation snapshot pushed as a logged core
input". **LEDGER_CORE**: the Scribe as a named per-primary delta consumer
(cursor, authority stream — never the ring); the accumulator suppressed across
handoff. **CONSENSUS**: the §8 client-classification note (the score service).
**MERGE**: the "─ring─►" arrow relabeled "host channel" (collides with the
history ring). **FOREST**: field aggregates advisory (the score service alone
computes reputation); :220–222 "Branch 14 owns detection" → MONITORING/HANDOFF.
**ADRs**: amend ADR-0001 (init seam + fork-owned kernel config + the stats
surface; "OS sandboxes only as degraded mode" scoped to the world-facing
boundary; the stale "virtio-fs workspace" ref); write **ADR-0006**
(two-container pod interior; Design B tombstoned as the live alternative).
**GAPS**: the §11a–e pending-amendments tracker closes; header counts. **The
per-subsystem span-clause sweep** (TRACING §12) lands jointly here.

## 18. Open riders (the reconcilers' unresolved questions — the user's, flagged)

- ~~R3's cross-cutting cluster~~ **LANDED 2026-08-22** (user-accepted as the
  maximal design): per-workload flow keys from the pod mint root, per-container
  custody, the workload-granular key-hint law (hints never coarsened), the
  pod-granular envelope kept (mis-attribution unrepresentable — no
  sender-written identity field exists), host-side attribution stamping, and
  the two-bar model recorded in FAULTS — one commit across PROTOCOL §2,
  WIRE_SECURITY §3/§6, FAULTS §1, IAM §1/§6, PODS §1.
- **R1-OQ1**: do pooled/snapshot generic VMs pre-create the two containers
  (faster ready; T7's genericity proof extends to container FS) or
  create-at-assignment (current text) — or hybrid (Scribe pre-created)?
- **R2-OQ-a**: the blocking rustls provider pool's home under Design A (host-side
  at the gateway vs in-guest over pre-connected fds) — ties to the landed
  dual-stack fix.
- **R2-OQ-b**: who owns the scaling-class enum (PODS table vs `AgentRole`).
- **R2-OQ-c**: fleet priors' home (cross-session artifacts: object-tier/registry
  vs a meta-group service).
- **R4-OQ-a/b/c**: homes for fitted-baseline artifacts, checkpointed
  detector-suite state (same species as the FOREST field checkpoint — one ruling
  covers both), and the teardown-gate archival rung for the Scribe's window
  flush (sealed vs placed vs referenced).
- **ADR-0004's two OQs**: the init binary identity (argv0 / separate /
  `--init-mode`); guest-image distribution (embedded vs side-shipped).

## 19. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| MO1 | **Observe-not-feed** structural: no Scribe→primary path; no model-reachable primary→Scribe surface (architecture test + the ring unreachable from any tool/prompt) | a feedback path; black-box injection |
| MO2 | **Authority/enrichment split**: detection/score/billing/audit read only host-side streams (typed, CI-checked); the ring is never an authority input | tampered enrichment driving a verdict |
| MO3 | **Context economy**: history events runtime-emitted below the model; zero token cost; capture continues mid-inference (instrumented) | per-turn feeds; transcript reads |
| MO4 | **Channel survives both deaths**: respawned writer = new instance id, resumed reader = cursor-exact; primary death ⇒ tail-drain of committed bytes; teardown flush-gated at every kill point | lost black box; teardown before flush |
| MO5 | **Score = pure fold**: replay of the logged input stream is byte-identical at any checkpoint; no roster entry; snapshots enter as logged inputs only | self-reported reputation; a second authority |
| MO6 | **Interior attribution + export**: every denial class × container ⇒ counted + attributed (cgroup-id); enforcement pinned — drainer death changes observation, never enforcement | silent denials; enforcement dying with its drainer |
| MO7 | **Host-observed truth + cross-view**: each lie-detector row decidable host-side; injected guest lies ⇒ divergence flagged | a Bar-B guest faking telemetry |
| MO8 | **Content-free**: the H8 type-walk over every record kind and signal type | work content leaking |
| MO9 | **Every constant derived** (§12 complete, definition sites); the fork-flip list explicit and tracked | magic numbers; undeclared kernel assumptions |
| MO10 | `N=1` ≡ fleet (no mode) | mode creep |
| MO11 | **Ring protocol exactness**: torn-read fuzz never parses torn data; gap honesty (every overwrite window ⇒ exactly one Gap); seals + cross-write `EACCES` enforced by the kernel (probe); writer never blocks (W4 under a dead reader, measured) | torn parses; silent overwrite; policy-only direction; a blocking emitter |
| MO12 | **Init crash-stepped**: kill-fuzz at every I1–I5 boundary and both crash edges ⇒ the stated recovery, mint-before-spawn invariant, flush-gated teardown | a half-minted channel; teardown racing the drain |
| MO13 | **Two-container admission**: Σ memory.max + init ≤ guest RAM enforced at admission; census N+1 measured; Scribe resident-idle ≈ 0 CPU (ratchet) | guest-global OOM; 2N thread creep; a resident-hot Scribe |

## 20. Test matrix (SIM + interior)

| Test | Asserts |
|---|---|
| Death fuzz | MO4/MO12 (every container/init kill point × order; tail-drain; cursor resume; flush gate) |
| Ring protocol fuzz | MO11 (lap-the-reader torn reads; overwrite windows; instance regeneration; dead-reader writer latency) |
| Comms-law probe | MO1/MO2 (path reachability; ring-as-authority unrepresentable) |
| Denial-attribution sweep | MO6 (every denial class × container; drainer-death ⇒ pinned enforcement holds + counted drops) |
| Cross-view lie fuzz | MO7 (all seven rows, injected lies) |
| Score replay | MO5 (fold determinism across checkpoints) |
| Content-free CI | MO8 |
| Admission/census | MO13 |
| Laptop parity | MO10 |

## 21. References

Firecracker (device metric families; the minimal-VMM precedent); KVM
`GET_STATS_FD` (api.rst 4.133); virtio-balloon freshness (the provenance
micro-pattern); Falco/Tetragon/Kata (pin-enforcement, supervise-drainer,
policy-compiled-outside); LTTng/perf sub-buffered ring designs (the
flight-recorder overwrite discipline); Ye 2002/2003; GhostBuster/Lycosid/
Antfarm/LibVMI (cross-view validation). Companions as enumerated in §16.
