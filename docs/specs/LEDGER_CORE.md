# SPEC: the ledger core — machinery for the proof of work

Status: ACCEPTED 2026-08-16 (with sub-decisions (a) apply-on-ack, (b) no outbox,
(c) event-carried score snapshots; amended under maximal audit — four corners
closed: effective-state affordance checks, paced retirement, normalized replay
comparison, bounded monitor closures). The implementation companion to
`docs/architecture/LEDGER.md` (the law). Runs on hecate-rt under the memory
doctrine: single-owner tasks, arenas + generational handles, zero refcounting,
deterministic maps, apply-on-input purity.

## 1. The core task

One **ledger core** per session — a single-owner task in the session colocation
unit. All mutation flows through its mailbox; all hot state lives in its arenas.

**Ceiling, priced**: one session's mutations serialize through one task — the
ceiling (arena writes + delta emission, millions of ops/sec class) sits orders
of magnitude above session demand (agents generate hundreds/sec). Sharding the
core would destroy the total order that replay, monitors, and effective-state
checks stand on. The ceiling is measured in CI with its derivation at the
definition site; sustained read load rides projections (§5), never the mailbox.

**Slot layout enforces writer disjointness structurally:**

```rust
struct ClaimSlot {
    content: WireBytes,          // issuer-authored, hecate-wire canonical — immutable
    content_hash: Cell<Option<Hash>>, // derived on demand, memoized
    lifecycle: ClaimLifecycle,   // system-written: status, history, timestamps
}
```

`content` is written once at generation; `lifecycle` is the only mutable half; the
two write paths are separate module-private functions — crossing them is
unrepresentable, not reviewed-for. Same shape for testaments, validations,
artifacts (artifact `Data` lives in the chunk store; slots hold references).

**Relations** are an edge arena: `{from: Handle, to: Handle, rel: Relation}` with
per-node in/out edge lists and one secondary index
`BTreeMap<(HandleKind, Relation), EdgeList>` — deterministic iteration everywhere
a record or delta is produced.

## 2. The commit path (sub-decision a: apply-on-ack)

```
input → affordance check (inform | yield | refuse) → build WAL record →
emit append effect (consensus API) → … → durable-ack input →
apply to arenas, assign sequence → build deltas (deterministic order) → emit
```

- **State is a function of the acked log, exactly**: mutations apply only on
  durable-ack (pipelined — the pending queue keeps throughput; determinism keeps
  replay trivial: replaying acked records reproduces arenas identically,
  re-executing no validators, no handlers).
- **Effective-state checks (amendment, closes the pipelined-affordance race)**:
  the refuse/affordance set evaluates against **effective state = applied arenas
  ⊕ pending queue, speculatively applied in input order** — every input is
  checked against exactly the state it will apply onto, so a pipelined sequence
  can never pass a check its predecessor invalidates (the Sylk
  update-on-terminal class, structurally closed). Apply-on-ack is then
  unconditional. Determinism holds because input order is total (L13).
- The **refuse set** evaluates purely over core-local state: writer-crossing,
  self-targeting, malformed relations (closed enums — decode already rejected
  unknowns), non-agentic quality bars, and the **rank override check** — which
  needs performance modulation, provided as **event-carried snapshots**
  (sub-decision c): the score service pushes modulation snapshots as ordinary
  inputs; the check reads last-known-snapshot from local state. No synchronous
  query escapes the core; determinism and replay hold by construction.
- **Deadlines** are timer inputs (virtual in SIM) — expiry transitions are
  ordinary deterministic inputs, as `LEDGER.md` requires.

## 3. The graph engine

- **Satisfaction monitors are per-parked-scope materializations**, not a global
  incremental SCC: each parked turn's monitor holds its transitive blocking
  closure, SCC-condensed at construction, satisfied interiors collapsed to
  released tokens. A per-node subscriber index (`node → monitors`) makes delta
  dispatch O(affected monitors), never O(all). (Global incremental SCC rejected
  deliberately: its incrementality bugs are exactly the stranded-turn class L4
  exists to catch — per-scope + oracle fuzz is the more *verifiable* design.)
- **Closure memory is bounded (amendment)**: overlapping closures duplicate
  across monitors, so the aggregate carries a derived budget — parked-turn
  ceiling × live-graph anchors, derivation at the definition site — and a
  breach alarms loudly in the health plane rather than growing silently.
- **Monotone-cut release for free**: the core processes inputs in total order, so
  a monitor's view is always a prefix of the delta stream — no torn reads exist to
  defend against; release fires when the local fixpoint (`terminal ∧ children
  released`) holds at the current prefix.
- **Deadlock**: a deadline expiry inside an unsatisfied SCC selects the victim
  deterministically — lowest claim sequence — and fails it with a typed reason.
- **Traversal** (`traverse(node, filter, depth)`) is a bounded query message over
  the handle graph; crossing the retention boundary returns the typed archival
  continuation (§6).

## 4. Dispatch: agents, services, evaluators

- **Agents**: deltas ride the credit-based streams; the **inbox engine lives in
  the agent runtime** — expectation table (correlation → parked continuation) +
  standing identity subscriptions + the bounded dedup window
  (`(delta_key, seq)` LRU sized from queue-capacity derivation, plus content
  identity). One causally coherent entry point per dispatch.
- **Exactly-once is three layers doing different jobs** (stated so no layer is
  ever "simplified" away): cursor-exact stream resume (beyond-window
  retransmits impossible by construction) → windowed dedup LRU (in-window
  delivery races) → content identity (content-identical reposts). L6 tests the
  composition, not any single layer.
- **Services**: a boot-time handler registry, harness-side. Invocation in tracked
  scopes with bounded queues; overflow → durable `receipt_failed` + backpressure
  artifact; **handler panic → `testament_generation_failed` + error-trace
  artifact** (`catch_unwind` at the boundary — a panicking validator is evidence,
  never a crash). Synchronous handlers may compress lifecycle states into one
  commit; the wire-visible sequence is unchanged.
- **Validation evaluation**: receipt validations auto-pass in-core (pure).
  Programmatic validators run as service handlers, results committed as artifacts
  (replay replays the artifact, never the validator). Errored validators fall back
  per priority, then agentic. Agentic evaluation is a delta to the evaluator with
  testament + parent claim + pending validations preassembled — evaluation starts
  without traversal.
- **The accumulator** is agent-runtime-side: bounded, scope-keyed, flushes as one
  composite testament at scope close, suppressed on yield (no premature
  testimony).

## 5. Deltas and projections (sub-decision b: no outbox structure)

- Deltas are **derived from committed records at emission, deterministically
  ordered** — the replayed stream is byte-identical to the live stream.
- **There is no outbox table.** Projectors (UI bridge, Archivalist mirror,
  frontier service) are ordinary **cursor consumers of the delta stream**: durable
  watermarks, resumable, typed RESYNC below retention — the machinery the protocol
  already ships. At-least-once projection = cursor + replay; per-projector
  terminal-failure surfacing = a stuck-cursor alarm in the health plane. One
  structure deleted relative to Sylk (its outbox), zero guarantees lost — the log
  *is* the outbox.

## 6. The retirement engine

**Paced work, never idle work (amendment)**: a busy core never idles, so
retirement tracks **debt** (bytes past the retention watermark); when debt
crosses a derived threshold, retirement steps interleave with mutation
processing at a derived ratio (both from arena-budget anchors). Under
saturating load, retirement keeps pace by construction (L8). The sweep is a
**fast-forward custody transfer** (each step idempotent, self-checking):

1. Collect terminal-and-released objects beyond the retention watermark.
2. Write archive entries (content-addressed docs + retirement-time index entries
   for the Archivalist's archive) — idempotent by content hash.
3. Verify presence by hash.
4. Drop hot slots, prune edge lists and secondary indexes, collapse monitor
   references to released tokens.
5. Advance the retirement watermark (durable).

A crash between any steps resumes at the missing half. Hot memory is bounded by
live work; the archive is complete by content identity; traversals past the
watermark return archival continuations.

## 7. Test matrix (failure each catches)

| # | Test | Catches |
|---|---|---|
| L1 | Lifecycle conformance sweep: every transition × injected failure at every boundary ⇒ exactly the spec'd durable state | undocumented states; lost failure facts |
| L2 | Writer disjointness: compile-visibility probe + runtime attempt ⇒ unrepresentable/refused | the split eroding |
| L3 | Replay: arenas identical from acked log **with derived caches normalized** (lazy `content_hash` memoization state excluded from comparison — computed-when differs between live and replay; values must match, presence must not); zero validator/handler re-execution (instrumented) | hidden state; replay side effects; a CI gate that quietly lies |
| L4 | Monitor oracle fuzz: randomized graphs (cycles included) vs brute-force fixpoint oracle; delta-order fuzz ⇒ identical release decisions, no lost wakeup | satisfaction bugs — the class that strands turns |
| L5 | Deadlock: constructed SCCs ⇒ deadline then lowest-sequence victim, identical across seeds | nondeterministic victim selection |
| L6 | Dedup: retransmit/replay/content-identity fuzz ⇒ exactly-once effects at every seam | duplicate work; duplicate render |
| L7 | Rank refuse at commit (with RANK.md K1): override shapes refused purely from local snapshot state | authority checks leaving the core |
| L8 | Retirement under load: hot bounds hold; every retired object retrievable by hash; crash mid-sweep fast-forwards; archival continuations typed | unbounded growth; lossy cooling; half-retired limbo |
| L9 | Projector discipline: kill/lag/resume projectors ⇒ cursor recovery + RESYNC; architecture test: no outbox structure exists | a second delivery structure growing back |
| L10 | Service dispatch: panic ⇒ failure testament + trace artifact; overflow ⇒ receipt_failed + backpressure artifact; compression wire-identical | crashing validators; silent overload |
| L11 | Accumulator: bounded, flush-on-close, suppressed-on-yield | testimony floods; premature testimony |
| L12 | Modulation snapshots: rank verdicts identical under snapshot-delivery reordering within a window; replay identical | score coupling breaking purity |
| L13 | Effective-state checks: racing mutation fuzz through the pending window vs a serial oracle — zero divergence between checked-against state and applied-onto state; the update-on-terminal class unrepresentable | the pipelined-affordance race |
| L14 | Retirement pacing: saturating mutation load — debt stays under threshold, hot bounds hold, mutation latency degradation within derived budget | retirement starvation; the "idle work" lie |
| L15 | Monitor closure budget: adversarial shared-closure graphs — aggregate memory within derived budget, breach alarms loud | silent closure sprawl |

## 8. Acceptance criteria

1. L3 (replay), L4 (oracle-verified satisfaction), and L13 (effective-state
   checks) are permanent CI gates.
1b. The core's throughput ceiling is measured in CI against the derived session
   demand model; the margin is reported, never assumed.
2. The core is a single-owner task; no lock, no shared state, no synchronous
   out-call exists in it (architecture test).
3. No outbox structure exists; projectors are cursor consumers only (L9).
4. Hot memory bounded by live work (L8), archive complete by content identity.
5. Memory doctrine holds: arenas + generational handles, zero Arc/Rc, deterministic
   maps (inherits the runtime lint wall).
6. Every capacity, window, and cadence derives from stated anchors at its
   definition site.
