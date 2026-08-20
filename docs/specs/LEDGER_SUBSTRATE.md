# SPEC: LEDGER_SUBSTRATE — the ledger as a state machine over the shared-log substrate

Status: presented for acceptance 2026-08-20 (grilling; the ledger-layering
settle — the sequencer/apply split is settled per session-scale-free +
MATERIALIZER acceptance; this write-up is for review). Reconciles
`LEDGER_CORE.md` §1's single-owner model with `MATERIALIZER.md`'s scale-free
apply — the **sequencer/apply split**. Research on file (GRILLING.md): the
ledger as a replicated state machine over a *reusable* shared-log primitive is
Delos/Tango/CORFU/Aurora-proven (Lane A); at-most-once-notify + cursor-recover
is End-to-End-theorem-backed (Lane B). Companion to `LEDGER_CORE.md` (the
machinery), `MATERIALIZER.md` (the apply path), `docs/architecture/LEDGER.md`
(the law), and the primitive family (`WAL.md`, `CONSENSUS.md`, `CACHE.md`,
`QUEUE.md`, `FANOUT.md`).

## 1. The shared-log primitive and its sibling instances

The ledger, the queue, the topics, and the cache are **sibling instances of one
shared-log primitive** (a `WAL.md` logical-log ordered by `CONSENSUS.md`), **not
layers stacked on each other** (the Delos/Tango pattern: one reusable log
abstraction, many state machines). The primitive's narrow interface is written
once; each instance layers its own semantics on top:

| The primitive (written once) | Per-instance semantics (layered on top) |
|---|---|
| `append(record) → index` | ledger: affordance check + claims lifecycle |
| `read_from(cursor, n) → records` | queue: lease / ack / visibility / DLQ |
| `advance_floor(index)` (reclaim) | topic-router: routing + filter + fan-out |
| replicate (replica count = durability, `WAL.md`/`CONSENSUS.md`) | cache: admission / eviction / coherence |

**Consensus lives in one reusable place** (`CONSENSUS.md`); a per-instance log
needs only a fault-tolerant `seal` + a lease/fence classification, never its own
consensus protocol (the Delos MetaStore split — getting this wrong rebuilds the
monolith). The ledger is therefore not privileged machinery: it is one
instance-consumer of the shared primitive, distinguished only by its claims
semantics.

## 2. The sequencer — the write path (single-owner, owns the order)

The ledger core is the session's **sequencer** (`LEDGER_CORE.md` §1/§2). The
exact flow:

```
input → affordance check (inform | yield | refuse, over effective state)
      → build WAL record → append (CONSENSUS API) → durable-ack → hand to apply
```

It is **single-owner** because the affordance check evaluates against **effective
state = applied arenas ⊕ pending queue, speculatively applied in input order**
(`LEDGER_CORE.md` §2): a serial, in-order operation that *produces* the total
order every monitor, replay, and effective-state check stands on. Sharding this
would lose the total order and the effective-state guarantee — so it is never
sharded. It is **not the bottleneck**: appending is an arena write +
consensus-batched commit (millions/sec class). The order it produces is the
log's index sequence.

**The applied/pending boundary is the watermark.** `applied arenas` = the
materializer's committed prefix (up to `watermark`, §3); `pending queue` =
records appended above the watermark, not yet materialized. The affordance check
is correct **regardless of how far the parallel apply has progressed**, because
it speculatively applies the pending queue on top of the committed prefix.

## 3. The apply path — the materializer (scale-free, order-preserving)

Applying the acked log into the claims-graph is `MATERIALIZER.md`. It refines the
`LEDGER_CORE.md` §2 step *"apply to arenas, assign sequence → build deltas →
emit"* from a single serial task into a scale-free path (serial `N=1` → within-
node DAG-parallel → multi-node partitioned), selected by derived parameters, no
mode.

- **Input**: the acked log records + each claim's **declared footprint** (its
  causal-DAG dependencies as read/write key-sets).
- **Output**: the committed claims-graph + the delta stream, both in **index
  order**.
- **Order-preserving**: the DAG edges run smaller-index → larger-index,
  independent claims commute, and the parallel/distributed result is
  bit-identical to serial (`MATERIALIZER.md` §7). **The sequencer owns the
  order; the apply preserves it** — so parallelizing apply does not violate the
  total order the former single-task model protected.

## 4. The read path — the cache

Reads of ledger state (claim status, testaments, `traverse` queries) ride the
`CACHE.md`, **off the apply path** (`LEDGER_CORE.md` §1: "read load rides
projections / the CACHE, never the mailbox"). Immutable testaments and content
are the **content-by-hash** cache face (key = hash, zero invalidation); mutable
claim-state is the **general-KV** face, kept coherent by invalidation over the
FANOUT into the cache's holder index (`CACHE.md` §4). A miss recomputes from the
committed claims-graph — the cache is a reconstructible projection, never a
source of truth.

## 5. The distribute path — the fanout (first cursor consumer, no outbox)

The materializer emits committed deltas in index order (`LEDGER_CORE.md` §5). The
**FANOUT** is the **first (and only) cursor consumer** of that delta stream — a
routing table, not a second outbox, so `LEDGER_CORE.md` §5's no-outbox law and
AC-3 hold literally. It routes each delta to the downstream consumers, each an
ordinary cursor consumer:

- **cross-region replicas** (async delta replication — no synchronous WAN);
- **cache-invalidation** (mutable claim-state → the cache holder index, §4);
- **external projections** (UI bridge, Archivalist mirror, frontier service —
  `LEDGER_CORE.md` §5).

Delivery is per-subscription (`FANOUT.md`): internal cursor-tracking consumers
take **at-most-once notify** with their cursor as the correctness backstop;
external non-recoverable consumers take **durable at-least-once** (a QUEUE
subscription with retries + DLQ).

## 6. The wake path — in-core deterministic, cross-node backstopped

Waking a parked agent when its blocking claims satisfy has two regimes:

- **In-core (the hot path)** — deterministic. The satisfaction-monitor
  subscriber index (`LEDGER_CORE.md` §3, its **own** instance, never shared with
  the cache — fork-2) dispatches the in-order delta stream to affected monitors,
  `O(affected)`; a monitor releases on its local fixpoint at the current prefix
  (§3 monotone-cut). Cursor-driven, reliable, no at-most-once *within* the core.
- **Cross-node (the rare path)** — a parked agent or projector on a different
  node than the ledger core is notified **at-most-once** (fast), with its cursor
  over the claim state as the **mandatory correctness backstop** (Lane B /
  End-to-End): a dropped wake *delays*, never hangs — the monitor re-derives
  satisfaction by polling the claim state / a reconcile floor.

The correctness-critical in-core dispatch is **never** the general fanout's
ephemeral class and is never coupled to cache-invalidation churn (fork-2:
separate subscriber-index instances, non-interference preserved).

## 7. Recovery

Durable truth = the session's **acked log** (`WAL.md`) + checkpoints. Recovery is
the materializer's **prefix-recoverable** replay (`MATERIALIZER.md` §8): replay
the acked-log suffix from the checkpoint watermark, deterministically → the exact
committed prefix. The claims-graph, the cache, and every projection are
reconstructible projections of the log — `LEDGER_CORE.md` §2's "state is a
function of the acked log, exactly" continues to hold **under parallel apply**,
because commit is in-order and replay is deterministic.

## 8. The interaction map

```
                 ┌───────────────── sequencer (single-owner, §2) ─────────────────┐
   input ─▶ affordance check(effective = applied⊕pending) ─▶ append ─▶ durable-ack │
                 └──────────────────────────────┬─────────────────────────────────┘
                                                ▼  (the acked, ordered log)
                        MATERIALIZER (§3, order-preserving, scale-free)
                                                │
                        committed claims-graph  +  delta stream (index order)
                             │                          │
             ┌───────────────┼──────────────┐           ├────────────▶ in-core monitors (wake, §6)
             ▼               ▼               ▼           ▼
          CACHE (reads §4)  projections   cache-inval   FANOUT (first cursor, §5)
                                                          └─▶ cross-region / external (§5)
   recovery: replay the acked log from the checkpoint watermark ⇒ exact prefix (§7)
```

## 9. Invariants

1. The **sequencer owns the order**; every consumer sees a prefix of the one
   deterministic delta stream (monotone-cut, no torn reads — `LEDGER_CORE.md` §3).
2. The **apply preserves the order** (order-preserving parallel/distributed —
   `MATERIALIZER.md`).
3. **No second cursor / no outbox** — the fanout is the first and only cursor on
   the delta stream (`LEDGER_CORE.md` §5).
4. The correctness-critical **in-core wake path is never coupled** to
   serving-plane churn (fork-2 separate instances).
5. **Consensus in one reusable place**; a per-log instance needs only `seal` +
   lease/fence.
6. **Everything is a reconstructible projection** of the acked log — the log is
   the source of truth; the claims-graph, cache, and projections are derived.

## 10. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| LS1 | **Sibling instances**: ledger/queue/topics/cache each instantiate the one shared-log primitive; no second log engine exists; each boot-classified | a bespoke per-subsystem log; the monolith rebuilt |
| LS2 | **Order end-to-end**: sequencer index order = materializer apply order = delta-stream order = every consumer's cursor order (SIM assertion) | a reordering anywhere in the chain |
| LS3 | **Sequencer single-owner**: the affordance-check + append is a single-owner serial path producing the total order; `effective = applied⊕pending` holds regardless of apply progress | a sharded sequencer losing the order / a stale affordance check |
| LS4 | **Apply scale-free + order-preserving**: `MATERIALIZER.md` M1/M4 (bit-identical at any core/node count) hold for the ledger's apply | apply that isn't order-preserving under parallelism |
| LS5 | **No outbox / single cursor**: the fanout is the first and only cursor on the delta stream (`LEDGER_CORE.md` AC-3) | a second delivery structure resurrected |
| LS6 | **Wake correctness**: an in-core monitor releases deterministically at its prefix fixpoint; a cross-node wake with the notify dropped still releases via the cursor backstop within the derived bound | a parked agent hung on a dropped notify |
| LS7 | **Recovery**: crash ⇒ replay the acked log ⇒ exact committed prefix; the claims-graph/cache/projections reconstruct | recovery to a non-prefix / lost projection |
| LS8 | **Reads off the apply path**: sustained read load rides the cache/projections, never the sequencer mailbox | read load throttling the write order |

## 11. References

Delos (OSDI 2020 / SOSP 2021), Tango (SOSP 2013), CORFU (NSDI 2012), Amazon
Aurora (SIGMOD 2017) — a replicated state machine over a reusable shared log,
with queues/namespaces as sibling instances. End-to-End Arguments (TOCS 1984) —
the wake-path notify/cursor split. Companions: `LEDGER_CORE.md`,
`MATERIALIZER.md`, `CACHE.md`, `QUEUE.md`, `FANOUT.md`, `WAL.md`, `CONSENSUS.md`,
`SESSIONS.md`.
