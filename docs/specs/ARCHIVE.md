# SPEC: ARCHIVE — the archive plane (session memory: ingest, store, baselines, the Archivalist's machinery)

Status: presented for acceptance 2026-08-22 (v2 — rewritten for standalone
implementability after the rigor challenge: the store, index, replication,
serving, and query mechanics are now instantiated in-place, with the example
curve, the concrete detector resolution path, the enumerated failure walks, and
the formal laptop case). The settled decisions are unchanged from v1
(GRILLING.md): session-scoped curves, lineage-only inheritance + shipped
defaults, the no-duplication split, the plane as its own bounded component,
infrastructure-not-agent paths, the Archivalist's duty set. Research receipts on
file (per-entity baseline practice; Steiner/LC-CUSUM cold start; ANTIDOTE /
boiling-frog / Kloft–Laskov / Cretu poisoning defenses). Companions:
`MONITORING.md`, `COLLECTOR.md`, `HANDOFF.md`, `LEDGER.md` §8, `SESSIONS.md`,
`STORE.md`, `QUEUE.md`, `WAL.md`, `OBJECT_TIER.md`, `SERVING.md`/`MERGE.md` §0
(the node blob/serving plane), `TRANSFER.md`, `AGENTS.md`.

## 1. Role and the three laws

Every session accumulates memory that is **not** telemetry (lossy, expiring,
operational — the collector's), **not** work proof (complete, never sampled —
the ledger's), and **not** work content (the knowledge plane's): the Scribe's
judgment-bearing records, the **reference curves** that tell detection what
normal looks like for this workload, and the sealed history that survives the
session down its lineage. The archive plane is that memory's infrastructure — a
bounded per-session component with its own purpose, retention class, and owner.
The **Archivalist administers it and never carries it**.

- **Session-scoped, lineage-inherited**: nothing learned here crosses a user or
  session fence except *down the lineage tree* (single-owner by construction).
  A poisoner's blast radius is its own session's baselines — structural.
- **One collection path**: raw performance numbers live in the collector; this
  plane keeps **sufficient statistics and documents**, never a second copy of
  the points.
- **Infrastructure, not agent**: ingestion, fitting, serving, and the teardown
  gate are service work at service latencies; the Archivalist's judgments
  arrive as claims and configure the machinery.

## 1a. The whole machine, in plain terms

A hospital's medical-records department. Ward monitors (the collector) stream
vitals continuously — operational, nobody files every heartbeat. The **records
office** (this plane) keeps what must outlast the shift: the attending's
written assessments (the Scribe's records), the discharge summary whose receipt
gates the patient's release (the final flush and the teardown ack), and each
patient's **chart baselines** ("her resting heart rate runs low — normal *for
her*"), distilled from monitor history by records staff (the fitting service)
rather than by re-wiring the monitors. The **records officer** (the
Archivalist) never carries charts — clerks do; the officer rules on what enters
the record ("post-op week — exclude it"), orders re-summaries, signs the chart
transfer when care continues elsewhere (the lineage seed), and answers every
"what does the history show?" question. One patient's chart never calibrates
another's monitors; a new patient is judged against conservative textbook
ranges (shipped defaults) until her own chart fills in.

## 1b. Terms this document uses (reading guide)

- **Reference curve** — the fitted record of *normal* for one (agent-type,
  task-class) pair in this session: per-signal, per-difficulty-bucket robust
  location and scale. Detection's risk adjustment compares against it.
- **Sufficient statistics** — bounded accumulators (histograms, counts) from
  which curves fit; kilobytes, checkpointed, never raw points.
- **Sub-window / vote / frozen version / exclusion mark / lineage seed /
  shipped defaults / the ingest ack** — as settled in v1 (§7–§8 carry the
  mechanics): K disjoint stat slices fitted independently and median-voted;
  every refit gated against the frozen prior version; exclusions authored from
  lifecycle facts or Archivalist claims, never the model's own opinion.
- **The durable plane** — `OBJECT_TIER.md`'s content-addressed store (the
  corpus's Tectonic-shaped system): immutable objects named by BLAKE3 hash,
  replicated by copyset placement — **no consensus per object**.
- **The node blob/serving plane** — every node's local content store +
  pull-by-hash server (`MERGE.md` §0's picture; the EdenFS role): the one way
  any node reads any content-addressed bytes, cache included.
- **Copyset replication** — placing an object's R copies on a deliberate set of
  nodes spread across the failure-domain tree; durability without a log.

## 2. Data model (wire-exact)

All documents are **hecate-wire canonical bytes** (`WIRE_FORMAT.md` — one value,
one encoding); a document's identity is `BLAKE3(bytes)`; documents are
**immutable** (a correction is a new document referencing the old).

```rust
// ---- the documents ----
enum ArchiveDoc {                       // closed; UnknownDocKind = typed reject
    CurveVersion(CurveVersion),         // KB-class (≈2–20 KB, §7's example)
    TrajectorySummary(Summary),         // KB-class
    NarrationRecord(Narration),         // KB-class
    FinalFlush(FlushRecord),            // up to MB-class (the drained ring tail)
    LineageSeed(SeedManifest),          // KB-class: curve refs + provenance chain
    RetiredProof(..),                   // LEDGER §8's — same store, own kind
}

struct CurveVersion {
    pair: (AgentTypeId, TaskClassId),   // both closed registry enums
    version: u32,                       // dense per pair, from 0
    curves: Vec<(SignalId, SignalCurve)>,  // sorted by SignalId (canonical)
    fit: FitMeta,                       // window span, per-sub-window sample
                                        //   counts, votes cast/discarded,
                                        //   estimator id, exclusion-mark refs
    prev: Option<ContentHash>,          // the frozen predecessor — the CHAIN
    drift: DriftReport,                 // computed vs prev; always present ≥ v1
    provenance: CurveProvenance,        // Fitted | LineageSeed{ancestor: ContentHash}
}                                       //   | ShippedDefault{release: Version}
struct SignalCurve { buckets: Vec<BucketParams> }   // indexed by difficulty bucket
struct BucketParams { median: f64, mad: f64, n: u64 }  // robust location/scale/count

// ---- the index rows (what the index maps; §6 has the key layout) ----
struct IndexRow { key: IndexKey, doc: ContentHash, size: u32, kind: DocKind }

// ---- ingest / fitter / directives — v1's shapes, unchanged ----
struct ArchiveIngest { lane: QueueInstance, applier: IngestApplier }
struct Fitter { stats: DetHashMap<(PairId, SignalId), SubWindowRing>,
                ring_k: usize, marks: Vec<ExclusionMark>,
                cursor: QueryCursor, own_log: WalLogicalLog }
struct StatsWindow { span: TimeSpan, per_bucket: Vec<ExpHistogram> }
enum ArchivalistDirective { Exclude(ExclusionMark), TriggerRefit(PairId),
                            Prune{doc: ContentHash, reason: PruneReason},
                            ApproveSeedExport(SessionUid),
                            ApproveDriftPublication{pair: PairId, version: u32} }
```

## 2b. What each piece is built on (the substrate map — consensus named per piece)

| Piece | Built on | Replication / durability | Raft? |
|---|---|---|---|
| **Ingest lane** | one QUEUE instance (its own, session durable scope) over WAL logical logs | the session group's log replication — the environment-derived default (fleet: R-replica fsync-ack; laptop: single-node fsync) | **yes** — QUEUE partitions ride the session group's replicated logs (CONSENSUS §6 lease+fence, as every queue) |
| **Document bytes** | the durable plane (OBJECT_TIER, `archive` storage class, session scope) | **copyset replication** — R copies placed across the failure-domain tree, R = the same env derivation; integrity by content hash; background scrub re-replicates | **no** — immutable content-addressed objects need no consensus; the hash is the truth |
| **The index** | one session-scoped `STORE.md` instance (B-tree profile, in-order apply — STORE §16 row) | STORE's own: the shard's raft group (R = env derivation), all-replicas-apply, checkpoint→durable plane | **yes** — one raft group per index shard (one shard until the derived split bound, §6) |
| **Reads/caching** | the node blob/serving plane (pull-by-hash, verify, keep — MERGE §0) | cache, not truth: any node re-pulls by name | no |
| **Fitter state** | its own WAL logical log (client-owned checkpoint) | the session group's log replication | via the session group's logs |
| **Curve delivery to detection** | the index's STORE watch (resolved-ts) | — | via the index shard |
| **Seed import / large fetches** | TRANSFER (chunked, verified, resumable) | — | no |

So: **Raft appears exactly twice** (the ingest lane's backing logs; the index
shard) — both as instances of already-accepted machinery. Bytes are never
consensus-replicated; they are content-addressed copysets, which is the
Tectonic-shaped durable plane's whole design.

## 3. Architecture map and networking

```
POD                                    SESSION COLOCATION UNIT
 Scribe ── records/flush ─ vsock ─▶ host ─▶ INGEST LANE (QUEUE) ──durable ack──▶
                                             │        gates pod teardown (I6)
                                             ▼ applier: bytes THEN index (§4)
        DURABLE PLANE (OBJECT_TIER            ARCHIVE INDEX (STORE instance,
        archive class, session scope;         1 raft group; B-tree; watch)
        copyset R, scrubbed)  ◀── writes ──┘        ▲            ▲
              ▲                                     │ lookups     │ watch
              │ pull-by-hash (node serving plane)   │             │
 FITTER (collector query-class consumer;      DETECTION SUBSTRATE (curve
  stats → CurveVersions → bytes+index)         resolution at detector birth, §8)
 ARCHIVALIST (claims in; queries out — never a byte in transit)
LINEAGE: seed sealed at finalize → descendant imports at create (TRANSFER)
```

| Hop | Transport | Plane/class | Security |
|---|---|---|---|
| Scribe → ingest lane | its vsock flow → host → the lane | the lane's QUEUE delivery | the Scribe's per-workload flow key (records provably its own) |
| ingest ack → init | the control channel | Control class | the teardown gate signal |
| applier → durable plane | the durable-plane write path (bulk/TRANSFER for MB-class) | bulk | content-addressed; `archive` class admission |
| applier → index | the index shard's client op | directed-request-response | epoch-fenced like any STORE op |
| index raft / watch | class-0 / STORE's watch streams | as STORE §3b | as STORE |
| fitter → collector | hecate-quic query | query class, off ingest | session-scoped observability grant |
| any reader → doc bytes | node blob/serving pull-by-hash | bulk (Lane-A) | hash-verified on arrival |
| seed import at create | TRANSFER | bulk | provenance chain verified (§8) |
| Archivalist directives / queries | the claims plane / the query surfaces | standard | its own grants, per plane |

Zero new channels, zero new frame kinds — every hop is an instance of a
registered archetype.

## 4. Ingest — the exact pipeline and the ordering law

```
1. LAND      lane.enqueue(doc_bytes) → WAL append, group-commit fsync,
             session-group replication → THE ACK.  For a FinalFlush this ack is
             what pod teardown waits on (MONITORING §6): service-grade, µs–ms
             on PLP NVMe / ms-class consumer (WAL's measured anchors).
2. APPLY     the applier leases from the lane (at-least-once) and, PER DOC:
   2a. BYTES   put(hash, bytes) → durable plane, archive class, session scope
               (idempotent: content-addressed put of existing hash is a no-op)
   2b. INDEX   index.insert(IndexRow{key, hash, ...}) → raft-committed
   2c. ACK     lane.ack(offset) — only after 2b commits
   ORDERING LAW — BYTES BEFORE INDEX: an index row never references bytes that
   are not durable. Crash between 2a and 2b ⇒ an orphan object (unreferenced
   bytes) — swept later by the GC rule "index-referenced docs are the roots"
   (OBJECT_TIER §13 amendment); NEVER a dangling reference. Crash between 2b
   and 2c ⇒ redelivery ⇒ both steps idempotent ⇒ no-op.
3. VISIBLE   the index commit fires the watch; queries see the row.
```

**The durability chain, stated once**: `acked ⇒ on the replicated lane log`;
`indexed ⇒ raft-committed row + copyset-durable bytes`; `published curve ⇒
indexed`. At every point, recovery is replay (the lane redelivers; the index
recovers checkpoint + tail per STORE §11; bytes re-scrub by hash).

## 5. The store, concretely (bytes, placement, caching, Tectonic/EdenFS)

- **Writing**: the applier is an ordinary durable-plane client (the
  Tectonic-style writing daemon of OBJECT_TIER §4): it places R copies per the
  copyset map (R = the environment derivation — fleet: spread across
  AZs/nodes; laptop: R=1, the local store), acks at R_eff, and registers the
  object under the `archive` storage class (boot-validated, OT11). KB-class
  docs are single-chunk; a MB-class `FinalFlush` chunks by the standard CDC
  policy and rides TRANSFER.
- **Reading**: every consumer — detection resolving a curve, the Archivalist
  investigating, a descendant importing a seed — reads **by hash through its
  node's blob/serving plane** (MERGE §0): local hit, else pull-by-name from
  any holder, verify against the hash, keep. **That serving plane IS the
  cache** — no archive-specific cache exists (reads are by immutable name;
  the content-addressed cache needs no invalidation, ever).
- **Tiering**: hot = whatever the node serving planes currently hold (demand-
  driven); durable = the copyset R; cold = the durable plane's own EC cold
  tail for aged objects (OBJECT_TIER §5's seal-then-encode — inherited, not
  re-specified). Sealed `LineageSeed`s pin (GC roots) until their lineage
  retires.
- **The Tectonic/EdenFS integration, named**: OBJECT_TIER *is* the corpus's
  Tectonic-shaped system (its research lineage); the node blob/serving plane
  *is* the EdenFS role (lazy, pull-by-hash projection). The archive plane adds
  **one storage class and one GC-root rule** to the former and *nothing* to the
  latter — archive docs are ordinary named content the moment they're written.
- **Scrub/repair**: the durable plane's background scrub verifies and
  re-replicates archive objects like any content; a reader hitting a corrupt
  copy (hash mismatch) re-pulls from another holder — the standard path.

## 6. The index, concretely (keys, algorithm, sharding, replication)

One **session-scoped STORE instance**: B-tree backend (read/scan-dominated),
in-order apply, one shard, one raft group of R replicas (env-derived; laptop 1).

**The key layout** (fixed-width, hecate-wire canonical — ordered so every query
pattern is one contiguous range scan):

```
IndexKey = kind:u8 ‖ subject:16B ‖ discriminant:8B ‖ time:8B ‖ seq:4B

kind (closed u8)        subject                discriminant       time
CurveByPair             pair_id (padded)       version (desc)     fit span end
DocByAgent              agent_uid              kind:u8‖0          record HLC
DocByKindTime           0 (session-wide)       kind:u8‖0          record HLC
SeedByLineage           lineage_node_id        0                  seal HLC
ProofByScope            scope hash             domain:u8‖0        retire HLC   (LEDGER §8's rows)
```

Every document inserts under each key family it participates in (2–3 rows/doc;
rows are ~64 B — the write amplification is bounded and priced). **Algorithms**:
- `latest_curve(pair)` = a 1-row range scan at `CurveByPair‖pair` (version
  stored descending ⇒ the first row is the latest). O(log n) B-tree descent.
- `list(kind, time_range, cursor)` = a bounded, cursored range scan on
  `DocByKindTime` — the standard STORE `range_scan(after)`.
- `history(agent, range)` = range scan on `DocByAgent`.
- The **watch**: detection subscribes to the `CurveByPair‖pair` prefix (STORE's
  range-scoped resolved-ts watch) — a refit's insert fires exactly the
  affected subscribers.

**Sizing and sharding**: rows ≈ 64 B; a heavy session writing ~1 doc/sec for 90
days ≈ 7.8 M docs ≈ 23 M rows ≈ **1.5 GB of index** — inside one shard's
envelope. The split bound is STORE's derived one; if ever crossed, the index
range-splits by `kind‖subject` prefix through the standard directory machinery
(nothing archive-specific). Stated so the one-shard default is a derivation,
not an assumption.

## 7. The fitter and the example curve

Mechanics as settled (v1 §5, unchanged): collect inside the collector's
retention (exclusion-before-accumulation) → per-sub-window robust fits
(median + MAD read from histogram quantiles) → K-window median vote
(deviating windows discarded + counted; any window ≤ 1/K influence) → the
**drift gate** vs the frozen version (within bound ⇒ publish; beyond ⇒
withheld pending `ApproveDriftPublication`) → publish = ingest the
`CurveVersion` through §4's own pipeline (the fitter is just another lane
producer — one landing path for everything).

**The example curve** (concrete, the shape an implementer builds to):

```
CurveVersion {
  pair: (ENGINEER, REFACTOR), version: 3,
  curves: [
    (SIG_PROGRESSED_DURATION,      // claim_transition_duration{edge=progressed}
     SignalCurve { buckets: [      // difficulty buckets d0..d4 (the risk model's)
       BucketParams { median:  42_000.0, mad:  9_000.0, n: 210 },  // d0: ms
       BucketParams { median:  95_000.0, mad: 21_000.0, n: 340 },  // d1
       BucketParams { median: 214_000.0, mad: 55_000.0, n: 180 },  // d2
       BucketParams { median: 512_000.0, mad: 140_000.0, n: 65 },  // d3
       BucketParams { median: 1.31e6,    mad: 4.2e5,     n: 12 },  // d4
     ]}),
    (SIG_TOOL_SUCCESS_RATE, SignalCurve { buckets: [
       BucketParams { median: 0.97, mad: 0.02, n: 800 }, /* d1.. */ ]}),
    // … one entry per registered Tier-1/2 signal for the pair
  ],
  fit: FitMeta { span: [T0,T1], sub_windows: 6, votes_discarded: 0,
                 estimator: MEDIAN_MAD_V1, exclusions: [mark#7] },
  prev: Some(b3-9f2c…), drift: DriftReport { max_rel_shift: 0.06, per_signal: … },
  provenance: Fitted,
}                                  // ≈ 4 KB serialized for ~20 signals
```

**How HANDOFF consumes it** (the exact join): the detector's risk adjustment
for an observation `x` at difficulty `d` uses `μ_ref = median[d]`,
`σ_ref = 1.4826 × mad[d]` (the MAD-to-σ constant for the robust scale);
`k = Δ/2` with `Δ` derived from the handoff-vs-degradation cost anchors
(HANDOFF §4); bucket `n` gates confidence (a bucket below the derived minimum
falls back to the curve's provenance-declared wide bounds).

## 8. The detector resolution path (birth → fetch → watch → swap)

Answering "where is the CurveVersions detector?" precisely — the **consumer**
is HANDOFF's detection substrate, in this same colocation unit; the path:

```
D1 BIRTH    a detector for (agent_uid, phenomenon) derives its pair
            (agent-type from the registry, task-class from the claim) and asks
            the index: latest_curve(pair)               — one 1-row scan
D2 FETCH    found ⇒ read the doc by hash via the node serving plane; parse;
            hold BucketParams in detector RAM (KBs)
            not found ⇒ the ladder: LineageSeed (imported at session create,
            already indexed as version 0) ⇒ else ShippedDefault from the
            release bundle (a compiled-in table, no I/O)
D3 WATCH    subscribe the CurveByPair‖pair prefix (the index's range watch)
D4 SWAP     on a watch event (a refit published): fetch the new version, swap
            the in-RAM pointer atomically between statistic updates — the
            statistic S carries over (the curve moved, not the agent), and
            FitMeta's drift report is attached to the detector's own audit trail
```

The substrate's `RefCurveRef` (HANDOFF §3) is exactly `(pair, version,
ContentHash)` — the §15 amendment binds it to this index.

## 9. The query surface and the Archivalist

```rust
trait ArchiveQuery {                       // IAM: the archive read capability at
    fn latest_curve(&self, caller, pair) -> Result<CurveVersion>;      // this
    fn curve_history(&self, caller, pair, cursor) -> Result<Page>;     // plane's
    fn list(&self, caller, kind, range, cursor) -> Result<Page>;       // serving
    fn history(&self, caller, agent, range, cursor) -> Result<Page>;   // edge
    fn get_doc(&self, caller, hash) -> Result<ArchiveDoc>;
    fn seed_chain(&self, caller, lineage) -> Result<Vec<SeedManifest>>;
}
```

All reads: index range scan (§6's patterns) + serving-plane fetch — bounded,
cursored, session-scope-checked at the serving edge. The **Archivalist**
facilitates (agents/the user consult it; it composes from `ArchiveQuery` +,
under its own grants, the collector's surface) and directs (the
`ArchivalistDirective` claims) — never a hop; a wedged Archivalist queues
judgment only (auto lifecycle exclusions continue, within-bound refits
continue, ingest and teardown acks are untouched).

## 10. Failure cases, recovery, durability — enumerated and walked

| # | Failure | What is lost | The walk to recovery |
|---|---|---|---|
| F1 | Lane node crashes before the ack | the un-acked doc | the Scribe's send retries (at-least-once from its side); teardown keeps waiting — nothing tears down unlanded |
| F2 | Lane node crashes after ack, before apply | nothing (acked = on the replicated log) | lane recovery per QUEUE; the applier resumes leasing; idempotent 2a/2b |
| F3 | Applier crashes between bytes and index | an orphan object | redelivery re-runs 2a (no-op) + 2b; orphans from true aborts are GC-swept (index-referenced-roots rule) — dangling refs are unrepresentable (§4's ordering law) |
| F4 | Index shard leader crashes | in-flight inserts (raft's contract) | STORE §11: a materialized follower elects; the applier's un-acked lease redelivers; watch subscribers re-attach by cursor |
| F5 | Index quorum lost | index availability (reads/watch degrade) | detection keeps its in-RAM curves (D4's swap simply pauses); ingest keeps LANDING (the lane acks — teardown unaffected) with apply queued; STORE recovery restores; the backlog drains in order |
| F6 | A durable-plane copy corrupts | one copy | hash-mismatch on read ⇒ re-pull from another holder; scrub re-replicates; R copies + verification = the standard content story |
| F7 | The whole colocation node dies | the services' processes; nothing durable | SESSIONS re-places the unit: the lane recovers from its replicated logs; the index from checkpoint + tail; the fitter from its own-log checkpoint (cursor + stats exact); bytes were never node-local-only (copysets) |
| F8 | The fitter crashes mid-fit | the in-progress fit only | own-log checkpoint replay; the fit re-runs deterministically from stats (a pure function); sample-count dips from missed collection show in FitMeta — visible |
| F9 | The Archivalist is down | judgment latency | §9's degradation: nothing on any service path waits |
| F10 | Seed import fails at create | the lineage prior | the ladder falls to ShippedDefault (counted `ImportFallback`); retry via TRANSFER; detection never blocked |
| F11 | Poisoning (Bar-A agent skewing its signals) | nothing — the guards | vote-discard + drift-withhold + Archivalist prune (v1 §11's walked variant); worst case = this session's curves only |
| F12 | Laptop power loss (R=1) | nothing acked (WAL always-full fsync); un-acked in-flight only | on boot: lane log tail replays; index recovers checkpoint + local tail; objects re-verify by hash; the loss window is exactly WAL's acked-⇒-durable contract at N=1 (CONSENSUS §8's named crash-injection gate) |

**Durability, restated as the invariant**: every acked artifact is on a
replicated (or N=1-fsynced) log or in R content-addressed copies; every
recovery is replay or re-pull by name; **no archive component holds
unreplayable state** — the same invariant STORE and the collector already
carry, instantiated here.

## 11. Refusal & loss taxonomy (closed)

`ExcludedSpan | VoteDiscard | DriftWithheld | UnapprovedSeed | ImportFallback |
LaneWait | OrphanSwept | UnknownDocKind | IndexUnavailable(typed)` — one
counter each; CI walks every path into exactly one category.

## 12. Derived constants

| Constant | Formula | Anchors |
|---|---|---|
| Collect cadence | ≤ collector retention ÷ safety factor | series retention |
| K, sub-window span, drift bound, stats budget, refit cadence | as v1 §10 | contamination tolerance, HANDOFF's Δ anchors, pair census |
| Index row budget | rows/doc × doc rate × session horizon | measured doc rates |
| Index split bound | STORE's derived bound (bytes+load) | STORE §13 |
| Copyset R | the environment derivation (failure-domain tree) | QUEUE §4's same rule |
| Bucket-confidence minimum n | fit-variance target per bucket | measured signal variance |
| Ack-wait alarm | lane availability distribution | QUEUE availability |
| GC orphan-sweep cadence | orphan creation rate × space budget | measured abort rates |

## 13. The laptop case, formally

`N=1` is a derivation down every column of §2b, not a mode:

- **Lane**: the session group is 1-voter — the ack is the local WAL fsync
  (consumer-NVMe ms-class / macOS `F_FULLFSYNC` 17–24 ms — WAL's measured
  anchors; the teardown gate inherits exactly this latency, stated).
- **Bytes**: R derives to 1 — the local blob store *is* the copyset; scrub is
  local verify; "pull-by-hash" hits the local store always.
- **Index**: one shard, 1-voter raft (quorum = own durable append; the N=1
  crash-injection gate applies by name), B-tree on local NVMe, same watch.
- **Fitter/detection/Archivalist**: the one colocation unit on the one node.
- **Footprint derivation**: a laptop session at ~0.1 doc/sec for 30 days ≈
  260 K docs; median 4 KB ⇒ ≈ 1 GB bytes + ≈ 50 MB index — inside a laptop
  disk budget by two orders of magnitude; the formulas are the same ones that
  size the fleet.
- **Loss model**: F12's row — acked-⇒-durable at one fsync; nothing else
  differs. Same code, same tests, zero flags.

## 14. Worked example

v1 §11's life (lineage seed → exclusion → refit → the poisoning variant →
finalize/seed export) carries verbatim, now with the concrete joins: step 3's
publish is §4's pipeline (bytes b3-9f2c… then the `CurveByPair` row, watch
fires); step 4's discards and withhold are §7's vote and gate against the §7
example curve's frozen v1; the Scribe's 14:00 handoff mark is `mark#7` in the
example's FitMeta; the finalize seed is one `SeedManifest` referencing v4's
hash with the L3-ancestry chain, sealed and pinned.

## 15. Amendments landing with acceptance

As v1 §13, plus the v2 additions: `OBJECT_TIER.md` — the `archive` storage
class registration **and the index-referenced-roots GC rule + sealed-seed
pins**; `HANDOFF.md` §3 — `RefCurveRef = (pair, version, ContentHash)` bound to
this index; `STORE.md` §16 — the archive-index row (B-tree, in-order, the §6
key families and range watch named). MONITORING §6/§13 gate wording, SESSIONS
§2 colocation additions, AGENTS/CONTEXT entries, LEDGER §8 pointer, GAPS —
unchanged from v1's list.

## 16. Acceptance criteria

AR1–AR12 as v1 (the teardown-gate/service-ack law; one collection path;
structural session isolation; model-independent admission; the drift gate;
1/K influence; robust-only estimators; the inheritance ladder; directives as
claims; idempotent ingest; plane purity; laptop parity), plus:

| # | Criterion | The failure it catches |
|---|---|---|
| AR13 | **Bytes-before-index**: a dangling index reference is unrepresentable (crash-fuzz at every applier point); orphans are swept, counted, and bounded | a reference to nothing; unbounded orphan growth |
| AR14 | **Golden curves**: the §7 example (and a conformance set) round-trips serialization byte-identically; the HANDOFF join (μ/σ/k derivation from BucketParams) matches the oracle | wire drift; a mis-derived risk adjustment |
| AR15 | **The durability chain**: acked-⇒-replayable at every R including R=1 (crash injection per §10's F-rows, each row a named test); recovery is replay-or-repull only — no bespoke path | unreplayable state; a secret recovery mechanism |
| AR16 | **Query exactness**: every §9 read is one bounded index range scan + hash fetches (measured; no scan-the-world path exists); watches fire exactly the affected prefix subscribers | O(session) queries; watch storms |

## 17. Test matrix (SIM)

v1's ten rows, plus: applier crash-fuzz (AR13, every step boundary ×
redelivery), golden-curve conformance (AR14), the F1–F12 walk (AR15 — each
row seeded and killed at its point), query/watch exactness (AR16), and the
laptop column (every §13 derivation asserted at N=1).

## 18. References

As v1 §16 (the per-entity practice receipts; Steiner/LC-CUSUM; ANTIDOTE /
boiling-frog / Kloft–Laskov / Cretu; NIST AI 100-2), plus the substrate
lineage now load-bearing in-place: OBJECT_TIER's Tectonic shape (copysets,
seal-then-encode, scrub), MERGE §0's blob/serving picture (the EdenFS role),
STORE's B-tree/watch/recovery machinery, WAL's fsync anchors, QUEUE's
environment-derived durability.
