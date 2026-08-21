# SPEC: STORE — the settled-state store (pluggable engine, sharded, watchable)

Status: presented for acceptance 2026-08-21. Worked in-session (GRILLING.md) against
three research lanes — etcd's single-group ceiling; Meta's Delos / Borg / Twine and
Google Spanner control planes; and the FoundationDB / RocksDB / FASTER / Calvin durable-
store literature. Companion to `WAL.md` (the durable log floor), `CONSENSUS.md` (the
meta-tree Raft + the §1 shard-directory amendment this lands), `MATERIALIZER.md` (the
claims apply strategy), `LEDGER_SUBSTRATE.md` (the claims ledger's read/notify layer),
`OBJECT_TIER.md` (Tectonic — the checkpoint durable plane), and `SESSIONS.md` (the whale
shard boundary).

## 1. Role — a WAL is not a store

A write-ahead log makes a mutation stream durable; it is **not** settled, queryable,
on-disk state. A real store is a log **in front of a storage engine** — the log makes the
engine crash-safe, it does not replace it (etcd runs a Raft WAL *and* a bbolt B+tree;
`CONSENSUS §5` rejected bbolt but named no replacement, and `OBJECT_TIER §192` punted the
mutable side to "node-local per WAL.md" — a log spec). STORE is that missing engine: the
**foundational settled-state substrate** that both ledgers materialize into. DRAM-served,
NVMe-durable — the recent tier in memory, the cold tier on local NVMe, immutable
checkpoints sealed to Tectonic. One substrate, instantiated per workload; the apply, read,
and notify layers above it differ per ledger (§11).

## 2. Anatomy — one durable path

```
                 reads (ReadIndex) ─┐        ┌─ watch (per-shard resolved-ts, §7)
                                    ▼        │
   commit ──► [ consensus log = the ONE WAL (CONSENSUS + WAL, group-commit) ]
                                    │
                          async-apply driver (off the commit path)
                                    │
                          apply strategy (per ledger, §5)
                                    │
                          ┌─────────▼──────────┐   ages oldest out
                          │  DRAM window (§4)  │ ───────────────┐
                          │  authoritative,    │                ▼
                          │  concurrent        │      ┌── pluggable cold backend ──┐
                          └────────────────────┘      │  LSM | B-tree, on NVMe (§3) │
                                    ▲                  └──────────────┬─────────────┘
                          reads merge window over backend             │ seal_checkpoint
                                                                      ▼
                                                        Tectonic (immutable, §10)
```

**The consensus log is the only WAL.** The backend keeps no write-ahead log of its own and
fsyncs nothing on the apply path — on crash it recovers from its last checkpoint plus the
committed log tail (§10). One fsync per write (the log's group-commit), never two (TiKV
disables RocksDB's WAL for raft-applied data; Delos databases are learners above the shared
log; this is `LEDGER_SUBSTRATE`'s SMR-over-log shape).

## 3. The pluggable backend

The cold settled store for one shard-range — a small, sharp seam so an LSM and a B-tree are
*observationally identical* through it (the pluggability proof, AC-2). Every method is
`&self`: internally concurrent, no exclusive lock, reads never blocked by writes.

```rust
/// Holds ONLY aged-out state (mutations that have left the window, §4). Ordering, log
/// durability, recent-version reads, watch, and cross-region are the shared engine's.
trait StorageBackend: Send + Sync + Sized {
    fn ingest(&self, batch: AgedBatch) -> Result<()>;   // aged-out, LSN-ordered, immutable;
                                                        // idempotent+monotonic; NO self-WAL/fsync
    fn flush(&self) -> Result<()>;                      // promote to crash-durable; advance watermark
    fn durable_watermark(&self) -> Lsn;                 // log truncation gated on min() over consumers

    fn lag(&self) -> Lag;                               // backpressure → admission throttle (§9)

    fn snapshot(&self) -> Result<Self::Snapshot>;       // version-tagged, concurrent-with-ingest pin
    type Snapshot: ColdSnapshot;

    fn seal_checkpoint(&self, range: KeyRange) -> Result<Checkpoint>;  // immutable, content-addressed;
                                                                       // range-scoped: seal AND split
    fn recover(checkpoint: Checkpoint) -> Result<Self>;                // + driver replays the log tail
}

trait ColdSnapshot {
    fn version(&self) -> Lsn;
    fn point_read(&self, key: &Key) -> Result<Option<Value>>;   // Err(Corruption) → shared re-fetch
    fn range_scan(&self, r: KeyRange, after: Option<Cursor>) -> Result<impl OrderedIter>;  // resumable
}

enum Value { Inline(Bytes), Ref(ContentHash) }   // WIRE_FORMAT inline-vs-Tectonic law
```

**Single-version cold.** The backend keeps only the latest applied value per key; the window
owns recent multi-version reads. That is what lets one five-method seam sit over both an LSM
and a B-tree — neither implements MVCC, conflict, ordering, or log durability.

**Backend by declared workload property** (the CACHE/QUEUE/FANOUT opt-in-by-property
principle — a fact about the instance, never a mode): **LSM** (RocksDB-shape) for
write/append-dominated instances (ledger materialization); **B-tree** (Redwood-shape,
SSD-native — not bbolt's mmap) for read/watch-dominated instances (cluster state, registry,
IAM).

## 4. The window — the authoritative recent tier

Shared, in-DRAM, holds committed-but-not-yet-cold state `[durable_watermark .. commit head]`.
**Concurrent multi-writer** (FASTER epoch-latch-free) — it is where the MATERIALIZER's
parallel apply lands; the cluster's one-at-a-time apply is the easy case of the same thing.
It **ages its oldest state out to the backend as immutable batches** (`ingest`), so recent
data is buffered exactly once (window) and never twice (no backend memtable holding the same
mutations). It is **authoritative** — not the lossy CACHE primitive (which is the claims
ledger's separate read projection, §11).

## 5. The apply seam

One contract: **consume committed log entries → emit state changes into the window**, off
the commit path (async). Two strategies plug in, per ledger:

- **In-order (cluster ledger):** each committed entry is one state change, applied in the
  log's order. Trivial.
- **MATERIALIZER (claims ledger):** epoch the log, schedule by declared dependency edges,
  apply in parallel, partition by key for a whale (`MATERIALIZER.md`).

**The determinism rule (AC-3):** the resulting state is a pure function of the committed log
and nothing else — which is what lets a crash recover by replay and makes both strategies
prefix-recoverable. In-order gets it for free; the MATERIALIZER earns it (deterministic
tie-breaking, so parallel workers cannot diverge).

## 6. Reads

A linearizable read pays **ReadIndex** — a quorum-confirmed commit index at the shard's
leader (`CONSENSUS §3`; **not** lease or follower reads, which the doctrine rejects) — then
serves the **merge of `window[applied..V]` over the backend snapshot**. The window covers
the async apply lag, so apply need never be synchronous. Reads are **single-version** (latest
committed) over a **bounded window**; a read below the window floor is a typed `too_old`
(bounded staleness, FDB's model). Snapshots are version-tagged (clean merge) and
**integrity-checked** — a checksum failure is a typed `Corruption` that re-fetches from a
replica or checkpoint, never a silently bit-rotted value.

## 7. The watch

Per-shard **resolved-timestamp** streams (CockroachDB RangeFeed shape), fed by the **commit
stream** (backend-agnostic — an LSM and a B-tree instance watch identically) and **pushed**
by an in-core subscriber index (never polled — the no-polling law; the same dispatch as
`LEDGER_SUBSTRATE §6`'s wake, generalized). `REGISTRY §6`'s "external resumable watch" is an
instance of this.

```rust
fn watch(range: KeyRange, from: WatchStart) -> WatchStream;
enum WatchStart { Seed, FromVersion(Lsn) }
enum WatchEvent {
    Seed(SeedChunk),                                   // consistent initial state, CHUNKED (bounded memory)
    Change { key: Key, value: Option<Value>, version: Lsn },   // None = tombstone
    Resolved(Lsn),                                     // high-water: nothing ≤ this remains
    Resync { from: Lsn },                              // resume point below retention → re-seed
}
```

- **`Resolved` = the shard's commit watermark**, derived from the existing node-liveness
  fabric + commit index — **no new per-shard heartbeat** (preserving `CONSENSUS §1`'s
  idle-groups-cost-nothing law).
- **Seed → stream, no gap:** a `Seed` streams the current state chunked (via `after`, so a
  large seed never blows up memory — the etcd LIST-blowup class), ending at version V, then
  streams `Change` from V+1.
- **Multi-shard:** the client splits the range along shard boundaries and merges — per-key
  changes as they arrive, plus a merged `Resolved = min(Resolved)` over covering shards.
  **Within-shard order is total; per-key global order is guaranteed; cross-key cross-shard
  order is reconstructed from the resolved marks. Watches are not per-event linearizable.**
- **Resume / RESYNC:** reconnect from the last `Resolved` if within retention; below it,
  `Resync` → re-seed.
- **Slow-watcher isolation:** each stream has a bounded buffer; on overflow the watcher gets
  `Resync`, never back-pressuring the shard's emission to others.

## 8. Sharding — foundational, two-level

Horizontal scale past the single-group ceiling (one Raft group tops ~44K writes/s and
*degrades* with more nodes; many groups scale ~linearly — Borg cells, Spanner tablets, TiKV
regions, CRDB ranges). **Foundational** — both ledgers use this machinery, with different
parent + key (below).

- **Two levels.** A parent group owns a small, low-rate **shard directory**
  (`key-range → data-shard → host group + epoch`, one entry per shard); many **data shards**
  (each a Raft group + a STORE instance) hold **range-sharded** data (ordered, for scans and
  prefix watches — never hashed).
- **Routing:** the directory is cached and **range-scoped-watched** (a client watches only its
  own ranges' entries, so a split notifies only affected clients — not the whole fleet, the
  Endpoints-watch N² class). A stale-epoch route is refused → re-lookup. The directory is off
  the hot path; the parent group serves only directory *changes*.
- **Split** (a shard crosses its *derived* size/load bound — over `{bytes, write, read,
  watch}`): the parent commits a `split at key b` entry at index I; `seal_checkpoint([b,c))`
  at I hands the child its seed — **metadata-fast** (LSM: hard-link immutable SSTs; B-tree:
  COW root — no bulk copy; a split *with move* pays a background Tectonic-mediated fetch); the
  child spawns a new group, `recover`s, replays the tail past I; the **directory CAS**
  (epoch-bumped) cuts routing over. The watch survives: parent emits `Resolved(I)` for
  `[b,c)`, child takes over from I+1.
- **Merge** is the harder path — coordinate two leaders, one absorbs the other's range via
  ingest of its checkpoint, directory CAS, epoch-bump; it **briefly freezes** the merging
  range. Rare, driver-scheduled.
- **The placement driver** is a deterministic harness service (TiKV PD / Spanner placement
  driver / our autoscaler doctrine): it watches size + load + capacity and issues split /
  merge / move as **directory reconfiguration records** through Guardian admission
  (`CONSENSUS §1` already scopes placement to reconfiguration records). It is **HA + advisory**
  — the directory CAS + epoch fence are the authority; a wrong or dead driver yields
  suboptimal placement or stalled splits, **never corruption**.
- **Per-ledger instantiation** (the log/order model differs by consistency need):
  - **Cluster ledger** — parent = region meta group; key = **key-range**; **one log per data
    shard** (records are independent; cross-shard order via §7's resolved marks).
  - **Claims ledger** — parent = session group; key = **within-session claim-range** for a
    whale; **ONE ordered log per session** (claims causally depend; the MATERIALIZER applies
    in the log's order and partitions apply + state by key, `MATERIALIZER §5`). The whale's
    cut-lines are **owned by the shard directory — the one splitter** — which storage and
    apply both follow (already the MATERIALIZER's intent, "the shard boundary").
- **Costs bounded by prior law:** many groups is affordable because idle groups tick nothing
  (`CONSENSUS §1`), and per-shard DRAM (the window) is activity-sized — idle shards ≈ zero
  memory, total bounded by the working set, not shard count. The directory fits one meta group
  at scale (~1 MB); it recurses to a directory-of-directories only at extreme scale.

## 9. Backpressure

`lag()` (unflushed bytes + ingest-queue depth + compaction debt) crossing a derived bound
throttles the **lagging shard's admission** (FDB RateKeeper). Per-shard, and a *backstop* —
many-shards is the primary scaling (as the MATERIALIZER's parallelism is), never a global
throttle.

## 10. Recovery

Load the last checkpoint (local NVMe, or reseed from Tectonic by content hash) + replay the
committed log tail past `checkpoint.watermark` via `ingest`. **Prefix-recoverable**,
deterministic, no redo/undo of the backend's own (the log is the WAL). The log **cannot
truncate below `min(durable_watermark)`** across consumers (`CONSENSUS §5`'s checkpoint-
retention invariant).

## 11. The two ledgers over the substrate

**Foundational = the substrate** (backend + the one log + window + watch machinery + sharding
+ apply seam). **Per-ledger = apply + read + notify**, matched to consistency need:

| | **Claims ledger** (agent work) | **Cluster ledger** (cluster state) |
|---|---|---|
| Apply | MATERIALIZER (parallel, DAG) | in-order |
| Log/order | one ordered log per session | one log per data-shard |
| Reads | **CACHE** (lossy projection) | authoritative **window** (ReadIndex) |
| Notify | **FANOUT** / §6 wake | per-shard **resolved-ts watch** (§7) |
| Home | `LEDGER_SUBSTRATE.md` (unchanged) | this spec |

Registry and IAM also instantiate the substrate (read/watch-dominated → B-tree backend);
their change-feeds are the §7 watch.

## 12. Laptop degenerate

N=1: one region ≡ root ≡ one meta group; one data shard = the whole keyspace (the split
threshold is never reached); one backend; the window degenerates to a small in-DRAM buffer;
cross-region machinery is inert. Same code, derived params, **no mode**.

## 13. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| ST1 | **A WAL is never mistaken for a store**: every mutable-state read is served by a real engine (window + backend), not by "replay the log" (architecture test) | the corpus-wide WAL-is-storage conflation |
| ST2 | **Backend observational equivalence**: LSM and B-tree, fed the identical log, return byte-identical `point_read`/`range_scan`, including under concurrent ingest+read (differential conformance) | pluggability that is nominal, not real |
| ST3 | **State is a pure function of the committed log** (both apply strategies); crash at any ingest/flush/apply point ⇒ recover + tail-replay is identical, N=1 named | non-determinism; a backend that buffers-and-lies |
| ST4 | **No self-WAL**: neither backend fsyncs on the apply path; the only fsync is the shared log's (architecture test) | double-logging |
| ST5 | **No writer blocks a reader**: concurrent ingest + reads on a shard, reads measured never stalling; the window sustains N concurrent appliers | the `&mut self` serialization class |
| ST6 | **Bounded lag**: a write firehose exceeding flush+compaction trips `lag()` → admission throttle; memory + replay stay bounded | unbounded apply lag; OOM |
| ST7 | **Corruption caught, never served**: NVMe bit-flip ⇒ `Corruption` + re-fetch | silent bit-rot in a control decision |
| ST8 | **No single-group region ceiling**: a region's throughput scales with data-shard count (scale test); a stale-epoch route is always refused + re-looked-up | the etcd ceiling, re-created per region; routing to a shard that no longer owns the key |
| ST9 | **Split is crash-safe + watch-preserving**: kill at every split point ⇒ exactly the old range or the two new ranges is authoritative (never gap/overlap); an active watch across the split point gets every change exactly once | a torn split; a lost/dup watch event |
| ST10 | **Watch scales + resumes**: fan-out is per-shard; a `Seed` never blows memory (chunked); reconnect at any `Resolved` is gap/dup-free, below-retention ⇒ `Resync`; a slow watcher never stalls another | the single-watchableStore ceiling; the LIST-blowup; the resume-race |
| ST11 | **One splitter**: a whale's data-cuts and work-cuts are the same lines, both taken from the shard directory (architecture test) | data and apply disagreeing on where a whale divides |
| ST12 | **Every constant derived** (shard size/load thresholds, window size, group-commit width, false-alarm/lag bounds) from a physical anchor; `N=1` == fleet (no mode) | magic numbers; mode creep |

## 14. Test matrix (SIM)

| Test | Asserts |
|---|---|
| Differential backend | ST2 (LSM ↔ B-tree identical under concurrent load) |
| Crash-replay fuzz | ST3/ST4 (kill at every apply/flush; recover+replay identical; no self-fsync) |
| Concurrency probe | ST5 (reads never stall on ingest; N concurrent appliers) |
| Firehose | ST6 (lag → throttle; bounded memory/replay) |
| Bit-flip inject | ST7 (Corruption + re-fetch, never a wrong value) |
| Split/merge fuzz | ST8/ST9 (crash at every split/merge point; epoch-fence; watch continuity) |
| Watch suite | ST10 (per-shard fan-out; chunked seed; resume/RESYNC; slow-watcher isolation) |
| Whale split | ST11 (data-cut == work-cut, both from the directory) |
| Laptop parity | ST12 (`N=1` == fleet) |

## 15. References

etcd (the single-group ceiling: ~44K w/s degrading with nodes, 2 GiB/8 GiB quota → NOSPACE,
K8s 5k-node limit "assumes sharded etcd"); Delos (OSDI'20 / SOSP'21 — Meta's control plane:
RocksDB behind a shared log, the VirtualLog + pluggable Loglets, the LeaseEngine 0-RTT reads);
Borg (EuroSys'15 — ~10K-machine cells, Paxos-replicated Borgmaster); Spanner (OSDI'12 — Paxos
per tablet, directories/movedir); FoundationDB (SIGMOD'21 — the unbundled log/storage split,
async apply off the commit path, cheap recovery, pluggable `ssd`/`redwood` engines); RocksDB
(LSM: WAL + memtable + SST, pipelined group-commit); FASTER (SIGMOD'18 — epoch-latch-free,
the HybridLog hot/cold split); Calvin (SIGMOD'12) / Aria (VLDB'20 — deterministic apply);
TiKV multi-raft / CockroachDB RangeFeed + closed/resolved timestamps; NVMe fsync (PLP-DC
~135 µs vs consumer ms-class → group-commit as the throughput multiplier). Companions:
`WAL.md`, `CONSENSUS.md`, `MATERIALIZER.md`, `LEDGER_SUBSTRATE.md`, `OBJECT_TIER.md`,
`SESSIONS.md`, `REGISTRY.md`.
