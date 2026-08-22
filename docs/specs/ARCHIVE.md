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
- **Sub-window** — one of K disjoint time slices of accumulated statistics;
  fits are computed per sub-window and **voted**, so no single slice — however
  poisoned — moves the curve more than 1/K.
- **Frozen version** — the previously published curve document. Every refit is
  compared against it; drift beyond a derived bound is withheld for judgment.
  The boiling-frog stopper.
- **Exclusion mark** — a time-span excluded from fitting, authored from
  *lifecycle facts* (a handoff, an incident, a boot, a probe) or Archivalist
  provenance judgment — never from the fitted model's own opinion of the data.
- **Lineage seed** — the session's final curves, sealed at archive-finalize for
  descendants of the same lineage to inherit as their v0.
- **Shipped defaults** — conservative structural priors versioned with the
  harness release (logical clamps, wide bounds); learned from nobody.
- **The ingest ack** — the archive ingest service's durable receipt; the thing
  pod teardown actually waits for.
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

## 6b. Search — the archive is a searchable document plane (accepted 2026-08-22)

The key-family index answers *who/when/what-kind*; investigation also needs
*what was said* — the archive is a **document plane, searchable in itself**,
not merely a record vault awaiting promotion. Two search projections, both
**derived and rebuildable** (the content-addressed documents are the only
truth; index loss = re-index, never data loss):

- **Full-text**: one per-session FTS instance over the **declared text fields**
  of each doc kind (narration body, summary text, flush annotations — the kind
  registry declares which fields index; closed, like everything). Behind an
  `ArchiveSearch` trait — the same pluggable-seam discipline as STORE's
  backends — with **Tantivy as the exemplar-library engine** (Rust,
  Lucene-lineage, immutable segment files — which fit the plane naturally: on
  a derived cadence, sealed segments checkpoint to the durable plane as
  archive-class objects, bounding rebuild to checkpoint + tail-reindex).
  Recommendation flagged, not smuggled: the library-behind-a-seam posture is
  Sylk's authorized-search-tech precedent (Bleve there, Tantivy here); an
  owned engine remains a swap behind the same trait if the dependency ever
  fails the corpus's bar.
- **Semantic (opt-in per session profile)**: one per-session `VECTOR_INDEX.md`
  instance (the accepted HNSW spec, instantiated) over embeddings of the same
  declared fields. Embeddings are computed by a **paced, budget-bounded
  service** through the provider gateway (an ordinary metered egress —
  derived cadence, backlog-tolerant); a session that declines the profile
  simply has text search only.

**The indexing pipeline**: after §4's `INDEXED` step, the applier enqueues an
async index task (paced; **indexing never blocks ingest or the ack** — AR19);
the FTS add and the embedding job consume it. Crash/loss: rebuild by scanning
the key families and re-indexing — a derived-state recovery, F13/F14.

**Scope and content, stated plainly**: search is session-scope-ambient like
every read here (AR18 — a cross-session hit is unrepresentable, not filtered).
And a boundary people will trip on: **H8 does not apply to archive documents**
— H8 is the *telemetry* plane's content-free law; the archive is the session's
own content plane, IAM-fenced, where narrative *belongs*. The two planes'
different laws are exactly why they are different planes.

**The promotion flow, unchanged and now complemented**: the archive is
directly investigable pre-promotion (search here); the Archivalist still
*promotes* distilled material into the knowledge plane as a curation claim (a
knowledge-capability contribution referencing the archive doc's hash) — the
Sylk retirement-ingest pattern kept as a **flow between distinct planes**,
never a merged store.

```rust
// ArchiveQuery gains (session-scope ambient, cursored, budgeted):
fn search_text(&self, caller, query: TextQuery, kinds: &[DocKind],
               range: TimeRange, cursor: Option<Cursor>) -> Result<HitPage>;
fn search_semantic(&self, caller, text: &str, k: usize) -> Result<Vec<Hit>>;
// Hit = { doc: ContentHash, kind, score, snippet }  — snippets are session
// content served under the session's grant (not telemetry; see above).
```

## 7. The fitter and the example curve

**Collect** (cadence derived — comfortably inside the collector's retention
horizons, so points are always consumed before they expire):

```
1. batch = collector.read_series(session scope, pair selectors, since cursor)
2. for each observation: if covered by an ExclusionMark ⇒ skip (counted);
   else stats[pair, signal].current_window.per_bucket[difficulty].record(x)
3. rotate sub-windows on span boundaries (K disjoint slices, time-partitioned)
4. own_log.append(checkpoint{cursor', stats})        // crash ⇒ resume exactly
```

**Fit** (on derived cadence or an Archivalist `TriggerRefit`):

```
1. per sub-window w: fit_w = robust params per bucket — median + MAD read from
   the window's histogram quantiles (exact within the histogram's α — the
   ANTIDOTE lesson: robust estimators, never means/variance)
2. VOTE: param = median over {fit_1..fit_K}; a sub-window deviating from the
   vote by more than the derived bound is DISCARDED + counted (a contamination
   candidate — the Cretu micro-model defense; any one window's influence ≤ 1/K
   by construction, the Kloft–Laskov bounded-influence principle)
3. candidate = CurveVersion{v+1, prev: frozen v, drift: compare(candidate, v)}
4. THE GATE: drift ≤ derived bound ⇒ PUBLISH — ingest the CurveVersion through
   §4's own pipeline (the fitter is just another lane producer; one landing
   path for everything); the index commit fires detection's watch.
   drift > bound ⇒ WITHHELD: a consult claim to the Archivalist with the drift
   report — publication only via ApproveDriftPublication. Detection continues
   on frozen v meanwhile. THIS is the boiling-frog stopper: the baseline
   cannot slide silently at ANY rate, because every step is measured against a
   frozen predecessor and large steps need judgment — and the judge's input is
   the drift REPORT, never the (possibly poisoned) data's own plausibility.
```

**Why admission is model-independent (structural, AR4)**: exclusion marks come
from lifecycle facts (handoff spans, incident spans, boots, probes —
auto-authored from ledger/lifecycle records) or from the Archivalist's
provenance judgment. **No path exists from the fitted model to the admission
decision** — filter-then-retrain loops train the filter on yesterday's poison
(the boiling-frog receipt); we sever the loop instead of tuning it.

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
| F13 | The FTS index is lost/corrupt | search availability only | derived-state rebuild: segment checkpoints + tail re-index from the key families; documents untouched (they are the truth) |
| F14 | The embedding service backlogs or its egress budget exhausts | semantic-search freshness | search degrades to text-only for the lagging span, counted; the backlog drains at pace — never blocks ingest |

**Durability, restated as the invariant**: every acked artifact is on a
replicated (or N=1-fsynced) log or in R content-addressed copies; every
recovery is replay or re-pull by name; **no archive component holds
unreplayable state** — the same invariant STORE and the collector already
carry, instantiated here.

## 11. Refusal & loss taxonomy (closed)

`ExcludedSpan | VoteDiscard | DriftWithheld | UnapprovedSeed | ImportFallback |
LaneWait | OrphanSwept | UnknownDocKind | IndexUnavailable(typed) |
SearchLag(counted freshness) | SemanticDegraded(text-only span)` — one
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
| Search freshness bound | index-task backlog target ÷ doc rate | measured doc rates, investigation-latency need |
| FTS segment-checkpoint cadence | rebuild-time bound ÷ measured re-index rate | re-index throughput, RTO target |
| Embedding pace/budget | per-session egress budget share ÷ per-doc embed cost | gateway metering, session budget |

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

Session `s9`; pair `(engineer, refactor)`.

1. **Cold start**: `s9` forked from lineage node `L3`; at create it imported
   `L3`'s `LineageSeed` (TRANSFER, provenance chain verified) — the Engineer's
   detectors birth on seed-v0 curves via the §8 path (D1 index lookup → D2
   serving fetch → D3 prefix watch).
2. **Collect**: the fitter's cadence pulls the session's engineer/refactor
   series from the collector (query class, session grant); stats accumulate in
   K=6 sub-windows; a handoff at 14:00 auto-authors
   `ExclusionMark{Handoff, 13:55–14:10}` — `mark#7` in the §7 example curve's
   FitMeta; those observations never enter.
3. **Refit**: at cadence, six sub-window fits vote; drift vs seed-v0 is small
   (the workload matches its ancestor); v1 publishes through §4's own pipeline
   — bytes land content-addressed, then the `CurveByPair` row commits, and the
   detection substrate's watch fires (D4's atomic swap); risk adjustment now
   runs on *this* session's own normal.
4. **The attack variant**: a Bar-A-compromised Engineer slowly pads its
   latencies, hoping to drag its baseline up so real degradation later hides
   (the boiling frog — the receipt: 5%/week defeats naive retraining). Here:
   its skewed spans dominate two of six sub-windows → both **deviate from the
   vote and are discarded, counted** (influence capped at 2/6 even before
   discard); the surviving fit still drifts past the bound against the frozen
   §7 example curve → **withheld**, a consult claim reaches the Archivalist
   with the drift report and the two discard flags; the Archivalist prunes the
   spans (`ArchivalistJudged` marks), the clean refit publishes — and
   throughout, detection judged the agent against **frozen v1**: the padding
   registered as *deviation from normal*, exactly what HANDOFF exists to
   catch, and the poisoned data never became normal. Blast radius even on
   total failure of every guard: `s9`'s own curves — no other session, no
   other user (§1's scoping law).
5. **Finalize**: at archive-finalize the Archivalist approves the seed export;
   one `SeedManifest` referencing v4's hash with the L3-ancestry chain seals
   and pins (a GC root until the lineage retires). The final flushes landed at
   each pod's teardown against the lane's acks (§4 step 1); months of
   narration and summaries are indexed; and the Archivalist answered "how did
   this compare to L3's run?" from the seed chain it curated (§9's
   `seed_chain`).

## 15. Amendments landing with acceptance

- `MONITORING.md` §6/§13 — the flush's destination and the teardown gate named
  precisely: **the archive ingest service's durable ack** (not "the
  Archivalist"); the Scribe's outbound enumerates
  narration/summary/final-flush → the ingest lane.
- `HANDOFF.md` §3/§4/§11 — `RefCurveRef = (pair, version, ContentHash)` bound
  to this index (§8's path); the cold-start ladder (§8 here) replaces "fleet
  priors"; the flagged homes riders (R4-OQ-a / R2-OQ-c) close: curves live
  HERE; incidents/handoffs/probes auto-author exclusion marks.
- `SESSIONS.md` §2 — the colocation list gains the archive services (ingest
  lane + applier, fitter, index); archive-finalize includes the seed-export
  approval + seal.
- `STORE.md` §16 — the archive-index instance row (B-tree, in-order; the §6
  key families and the prefix range-watch named).
- `OBJECT_TIER.md` — the `archive` storage class registration (boot-validated,
  OT11) **and the index-referenced-roots GC rule + sealed-seed pins**.
- `AGENTS.md` — the Archivalist's roster row gains "administers the archive
  plane; provides/facilitates investigation queries"; `CONTEXT.md` gains
  Archive plane / Reference curve / Lineage seed entries (same commit —
  glossary-wins).
- `LEDGER.md` §8 — a pointer: the retired-proof archive's infrastructure is
  this spec's store/index (the `ProofByScope` key family).
- `RANK.md` / the score service — unchanged, stated (reputation ≠ baselines;
  different consumers, different state).
- `VECTOR_INDEX.md` — the per-session archive instance named as an
  instantiation (its spec is instance-ready; a one-line consumers note).
- `REGISTRY.md` — the doc-kind registry's declared-text-fields attribute
  (which fields of which kinds index; closed, boot-validated).
- The knowledge plane (`FOREST.md` / the D-6 branch when it opens) — the
  promotion flow's receiving side: a knowledge contribution referencing an
  archive doc hash; nothing else crosses.
- `GAPS.md` — the baseline-store exchange closes; MONITORING §18's R4-OQ-a/c
  and R2-OQ-c riders strike.

## 16. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| AR1 | **The teardown gate is a service ack**: no agent turn exists on the flush/teardown path (architecture test); ack latency is service-grade (ratchet) | pod lifecycle coupled to LLM availability |
| AR2 | **One collection path**: the fitter holds only bounded sufficient statistics; no archive component stores raw series points (architecture + memory test) | a second TSDB; double collection |
| AR3 | **Session isolation, structural**: no read/write path crosses a session fence except the lineage-seed import at create, provenance-chain-verified (architecture test + authz fuzz) | cross-tenant baseline flow; the poisoning blast radius escaping |
| AR4 | **Model-independent admission**: no data path from fitted curves to exclusion/admission decisions (architecture test); exclusion reasons are lifecycle facts or Archivalist claims | the boiling-frog filter-then-retrain loop |
| AR5 | **The drift gate**: no CurveVersion publishes with drift > bound absent an `ApproveDriftPublication` claim; detection serves frozen versions while withheld (fuzz: injected drift at every rate — fast AND slow — never publishes silently) | silent baseline slide at any speed |
| AR6 | **Bounded influence**: any single sub-window's effect on published params ≤ 1/K before discard, zero after (contamination fuzz vs oracle) | one poisoned slice steering the curve |
| AR7 | **Robust fitting**: median/MAD from histogram quantiles; no mean/variance estimator exists in the fitter (audit) — ANTIDOTE's lesson as law | fragile-estimator poisoning |
| AR8 | **The inheritance ladder**: current → seed → default resolution exact (§8's D1–D2); a detector is never blocked by a missing curve (birth fuzz); seed provenance chains verify or the import falls back (counted) | cold-start deadlock; unprovenanced inheritance |
| AR9 | **Agents act as claims**: every Archivalist directive is a claim; zero out-of-band control paths into the services (structural) | invisible curation authority |
| AR10 | **Idempotent ingest**: redelivery/reorder fuzz ⇒ single store+index effect (content-hash keying); crash at every applier point recovers exactly | duplicate documents; lost flushes |
| AR11 | **Plane purity**: the collector, ledger, and knowledge planes are untouched (no new writes to any of them from this plane; architecture test) | the retrofit failure mode, recurring |
| AR12 | `N=1` ≡ fleet; every §12 constant derived at its definition site; every §13 derivation asserted | modes; magic numbers |
| AR13 | **Bytes-before-index**: a dangling index reference is unrepresentable (crash-fuzz at every applier point); orphans are swept, counted, and bounded | a reference to nothing; unbounded orphan growth |
| AR14 | **Golden curves**: the §7 example (and a conformance set) round-trips serialization byte-identically; the HANDOFF join (μ/σ/k derivation from BucketParams) matches the oracle | wire drift; a mis-derived risk adjustment |
| AR15 | **The durability chain**: acked-⇒-replayable at every R including R=1 (crash injection per §10's F-rows, each row a named test); recovery is replay-or-repull only — no bespoke path | unreplayable state; a secret recovery mechanism |
| AR16 | **Query exactness**: every §9 read is one bounded index range scan + hash fetches (measured; no scan-the-world path exists); watches fire exactly the affected prefix subscribers | O(session) queries; watch storms |
| AR17 | **Search is a derived projection**: destroying either search index and rebuilding yields equivalent results (differential); no search structure is ever a truth source or a GC root beyond its own checkpoints | search state promoted to truth |
| AR18 | **Search is scope-fenced**: session-ambient like every read; a cross-session hit is unrepresentable (authz fuzz across sessions and users) | the searchable plane leaking across fences |
| AR19 | **Async indexing**: the index tasks never block ingest, the ack, or the applier (measured under indexing backlog); freshness lag is bounded, derived, and visible | search coupling the teardown gate |

## 17. Test matrix (SIM)

| Test | Asserts |
|---|---|
| Teardown-gate fuzz | AR1 (kill/partition at every flush point; teardown waits visibly, proceeds only on ack) |
| Memory/points audit | AR2 (stats bounded under unbounded signal volume) |
| Isolation fuzz | AR3 (every cross-session access attempt refused; seed import the only survivor, chain-verified) |
| Boiling-frog suite | AR4/AR5 (slow-ramp poisoning at the literature's rates ⇒ withheld/discarded, never published; the frozen version serves throughout) |
| Contamination sweep | AR6/AR7 (0–100% poisoned windows vs oracle; influence bound holds) |
| Birth ladder fuzz | AR8 (all three provenance paths; missing/corrupt seeds fall back counted) |
| Directive audit | AR9 (every service config change traces to a claim) |
| Ingest crash fuzz | AR10/AR13 (every applier step boundary × redelivery; orphan sweep bounded) |
| Plane-purity walk | AR11 |
| Golden-curve conformance | AR14 (serialization round-trip; the HANDOFF μ/σ/k join vs oracle) |
| The F1–F12 walk | AR15 (each §10 row seeded and killed at its point; recovery = replay-or-repull only) |
| Query/watch exactness | AR16 (fanout ≤ index resolution; prefix-exact watch firing) |
| Search differential | AR17 (destroy-and-rebuild both indexes ⇒ equivalent results; F13/F14 rows) |
| Search scope fuzz | AR18 (cross-session/cross-user search attempts unrepresentable) |
| Indexing backlog | AR19 (ingest/ack latency flat under saturated index tasks; freshness lag visible + bounded) |
| Laptop parity | AR12 (every §13 derivation asserted at N=1, incl. the R=1 crash-injection gate) |

## 18. References

**Per-entity baseline practice**: Elastic `partition_field_name` ("completely
independent baselines for each value of this field"); CloudWatch per-metric
models + excluded-time-ranges training hygiene; Datadog suppression seasons;
Azure per-series statelessness — universal, never cross-tenant. **Cold start**:
Steiner 2000 (risk-adjusted CUSUM — a population risk model, no per-entity
history needed); LC-CUSUM (Biau 2008 — default-distrust: presumed
not-in-control until the entity's own data proves otherwise); Efron–Morris /
CMS hierarchical shrinkage (the pooling alternative, deliberately not taken —
ours is single-owner lineage inheritance, flagged as precedent-free but
principle-clean). **Poisoning**: ANTIDOTE (Rubinstein et al., IMC'09 — 10%
chaff → 8× evasion, 20% → near-random; robust estimators as the defense); the
boiling-frog result (5%/week over 3 weeks → 50% FNR while rejections stay
quiet — filter-then-retrain defeats itself); Kloft–Laskov (bounded windows ⇒ a
critical influence ratio ≈0.15); Cretu et al. (disjoint micro-model voting);
NIST AI 100-2 (the poisoning taxonomy). **The substrate lineage, load-bearing
in-place**: OBJECT_TIER's Tectonic shape (copysets, seal-then-encode EC cold
tail, scrub); MERGE §0's blob/serving picture (the EdenFS role: pull-by-hash,
verify, keep); STORE's B-tree/watch/recovery machinery and its §16 profile
table; WAL's measured fsync anchors (PLP µs / consumer ms / macOS
F_FULLFSYNC); QUEUE's environment-derived durability; TRANSFER's chunked
verified movement. Companions as enumerated in §15.
