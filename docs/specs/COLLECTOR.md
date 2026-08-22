# SPEC: COLLECTOR — the observability pipeline (ingest → roll up → store → serve)

Status: presented for acceptance 2026-08-22 (rewritten to corpus rigor after the
first presentation was rejected for missing implementation depth). Settles Branch 39
(D1–D6 worked in-session, GRILLING.md): D1 one scope-tagged operational log (user), D2
two-class consumer model (user), D3 query-layer ledger integration "D3+" (user), D4
exponential-bucket roll-ups + overflow cardinality backstop (research), D5
weighted-HRW trace assembly (research), D6 hecate-rt-native thread-per-core pipeline
(research). Research receipts on file: Monarch/Gorilla/Scuba/Dapper/Canopy/Scribe;
OTel Collector + Vector; OTAP dataflow; Karger/HRW/jump/Maglev; DDSketch/t-digest/
HDR/exponential histograms; Prometheus/OTel/Mimir cardinality. Companions:
`MONITORING.md` (emission), `TRACING.md` (spans/head-keep), `HEALTH.md` (content-free,
AbsenceIs), `HANDOFF.md` (the detection stack — a stage of this pipeline, §9), `IAM.md`
(query gate), `CACHE.md`/
`QUEUE.md`/`FANOUT.md` (substrate), `WAL.md` (logical logs), `OBJECT_TIER.md` (cold),
`LEDGER_CORE.md`/`LEDGER.md` (delta stream + the one ledger-side amendment).

## 1. Role

Every chokepoint emits measurements, events, and spans (`MONITORING.md`,
`TRACING.md`). The collector **gathers** them (per node), **reduces** them (roll-up,
keep-decisions, cardinality bounds), **stores** them (hot in RAM, durable on the one
scoped operational log, cold in the object tier), and **serves** them (live streams to
the closed four; an IAM-gated query surface for everyone else). It is never on a claim
path, never a work authority, and loses nothing silently — every drop lands in the
closed taxonomy (§12) with a counter.

It is **composed from the accepted primitives** — QUEUE (durable stream), CACHE (hot
state), FANOUT (live delivery), OBJECT_TIER (cold) — plus exactly four new parts: the
**roll-up engine** (§5), the **cardinality limiter** (§6), the **trace assembler**
(§8), and the **query surface** (§9/§10). Execution is hecate-rt's sharded
single-owner model: one owner task per shard, telemetry never crossing shards on a hot
path, bounded channels everywhere (the OTAP shape receipt: 2.47M logs/s/core vs 121K
on the row path — shape, not dependency).

## 1a. The whole machine, in plain terms

Think of a national electricity utility. Every appliance has a **meter**
(a chokepoint emitting measurements). The **neighborhood substation** (the node
collector) doesn't forward every tick of every meter to headquarters — it keeps
running totals locally (the roll-up) and periodically reports **absolute meter
readings** upward. The **regional utility** (the region tier) files each
neighborhood's latest readings and can total across neighborhoods at any time.
Auditors (the query surface) examine the filed records at the office — they never
stand in the substation slowing the metering down. Fraud detection (the HANDOFF
stack) runs *inside* each neighborhood's substation, watching its own meters
continuously — it is part of the metering machinery, not another customer of it
(§9's stage-not-consumer rule).

The analogy carries the design's three least-obvious choices:

- **Why absolute readings, not "usage since last report" (§7):** real meters report
  cumulative totals precisely so a *lost report* can never mis-bill you — the next
  reading carries the truth on its own. A "usage-since" report that gets delivered
  while its acknowledgment is lost would be double-billed. Same here: absolute
  snapshots + replace-on-apply make loss and re-delivery harmless by construction.
- **Why totals at the substation, not raw ticks upward (§5, §7):** aggregating at
  the edge is what makes a million meters affordable — Monarch's measured 36:1
  reduction at ingest is this exact move.
- **Why auditors stay in the office (§9):** an audit, however heavy, must never slow
  the metering. Query load is structurally separated from ingest.

## 1b. Terms this document uses (reading guide)

- **Series** — one named stream of numbers with fixed labels (`SeriesKey`), e.g.
  "vfs.mount latency for Engineer-pod-7 on node-3." The unit of roll-up state.
- **Roll-up** — replacing a stream of raw values with a compact running summary
  (a counter, or a histogram of the distribution).
- **Dirty bit** — a per-series flag meaning "changed since the region last confirmed
  receiving it"; cleared only on that confirmation (§7).
- **Watermark** — the highest position already processed; anything at or below it is
  known-done and can be skipped on re-delivery (§10). A stamped-mail ledger: record
  the highest stamp number processed per sender, discard re-delivered lower stamps
  unopened.
- **Exemplar** — a bounded sample of opaque ids (here: claim UIDs) riding on a series
  so an investigator can pivot from a statistic to a concrete case.
- **Seal** — the moment a mutable in-progress thing (a trace window, a log segment)
  becomes an immutable record.
- **Cursor** — a durable bookmark into a stream; resuming from it re-reads exactly
  what follows it.
- **HRW routing (§2b)** — a deterministic lottery: every (trace, assembler) pair
  computes a score from a hash; the trace goes to its highest scorer. Remove one
  assembler and only *its* traces move — nobody else's ticket changes.
- **PEP** — the policy-enforcement point: the single place a read crosses IAM's
  authorization check (`IAM.md`).

## 2. Data model

```rust
// ---- the record (every durable operational event) ----
struct OpRecord {
    scope: Scope,               // routing + retention + authz key ("the reference IS
                                //   the route"); stamped by the emitting chokepoint
    class: OpClass,             // delivery + retention class; closed enum (§4 table)
    failure_domain: DomainRef,  // node < AZ < region (the CONSENSUS tree position)
    provenance: Provenance,     // HostObserved | GuestReported (MONITORING §8)
    at: Hlc,                    // emission stamp (the runtime's HLC)
    body: OpBody,               // H8-walked; no unbounded string/bytes exists below
}
enum Scope   { Session(SessionUid), System(DomainRef) }   // Session dies/archives with
                                                          //   its session; System = fleet
enum OpClass { Verdict, Lifecycle, Audit, Incident,       // never-shed, durable
                                                          //   (Incident = the detection
                                                          //   substrate's enriched alerts
                                                          //   — evidence-grade, §9)
               ClaimMetric,                               // durable, sheddable-late
               Telemetry, Span }                          // lossy-tolerant, sheddable
enum OpBody {                                             // one variant per class family
    Measure { series: SeriesKey, value: f64 },            //   → roll-up engine
    Event   { kind: EventKind, fields: BoundedFields },   //   closed kinds, bounded tags
    Span    (SpanRecord),                                 //   TRACING §3 shape, verbatim
}

// ---- series identity (the closed label vocabulary) ----
struct SeriesKey {
    metric: MetricId,           // closed registry (boot-validated, like chokepoints)
    principal: PrincipalUid,    // opaque uid — never a name/path
    op: OpEnum,                 // closed per-subsystem op vocabulary
    domain: DomainRef,
    provenance: Provenance,     // HostObserved | GuestReported — a SERIES DIMENSION,
                                //   so the authority/enrichment split (MONITORING
                                //   MO2) SURVIVES the roll-up: a guest-reported
                                //   measure can never launder into a host-observed
                                //   series; detection reads HostObserved series only
    dims: BoundedDims,          // declared bounded dimensions ONLY (≤ D_max, derived);
    hash: u64,                  //   the H8 walk rejects any unbounded dim at CI
}
// EventKind and BoundedFields are closed-registry types like MetricId: kinds are
// boot-validated registry entries; fields are (closed-enum key → numeric | enum |
// opaque-id) pairs with a derived count bound — the H8 walk covers both by type.

// ---- roll-up state (per admitted series) ----
struct ExpHistogram {           // §5 — full impl there
    scale: i8, zero_count: u64,
    buckets: Vec<u64>, index_offset: i32,
    count: u64, sum: f64, min: f64, max: f64,
    exemplars: RingBuf<ClaimUid, N_EX>,   // N_EX derived; latest-wins, bounded
}
// ---- the TIME dimension: a series is windows, not one lifetime aggregate ----
struct WindowedSeries {
    windows: RingBuf<(WindowStart, Aggregate)>, // time-bucketed; per-tier window width
                                                //   W_res derived (§5b); ring length =
                                                //   tier retention ÷ W_res — bounded
    current: Aggregate,                         // the open window, filling
    restart_epoch: u32,                         // bumps on collector restart — cumulative
                                                //   counter resets are DETECTABLE, never
                                                //   silently read as negative rates
}
enum Aggregate { Counter(u64),                  // cumulative total AT WINDOW CLOSE (the
                                                //   meter reading); rate = diff across
                                                //   windows, reset-aware via epoch
                 Gauge{ last: f64, min: f64, max: f64 },
                 Histo(ExpHistogram) }          // the WINDOW's value distribution

// ---- the node collector (one per node; owns every per-node shard) ----
struct NodeCollector {
    shards: Vec<CollectorShard>,       // N = derived core share; series hash-owned
    op_log: OpLogLanes,                // the ONE logical operational log = three
                                       //   class-lane QUEUE instances (§4):
                                       //   {critical, standard, telemetry}
    own_log: WalLogicalLog,            // the collector's OWN durable state: capture
                                       //   cursors + watermarks (§10) — small, node-local
    uplink: UplinkTask,                // §7 — ships interval deltas to the region tier
}
struct CollectorShard {                // single-owner: no lock exists in this struct
    registry: SeriesRegistry,          // §6 — the label→slot chokepoint
    series: Vec<SeriesState>,          // dense, indexed by SeriesIdx
    hot: CacheHandle,                  // CACHE instance: keyed lookups (trace rows,
                                       //   latest-event-by-key)
    events: EventRings,                // per-(scope,class) bounded deques — recent
                                       //   events in arrival order (read_events' hot
                                       //   horizon; durable classes ALSO cursor-read
                                       //   from the op log beyond it)
    dirty: BitSet,                     // series touched since last ACKED uplink (§7 —
                                       //   cleared on ack, not on ship)
    drops: DropCounters,               // §12 — one counter per taxonomy category
}

// ---- the region tier (sharded; §9b) ----
struct RegionShard {                   // one of R instances; R derived (§9b); owns the
    id: RegionShardId,                 //   series whose hash lands in its range
    epoch: Epoch,                      // instance epoch — bumps on (re)placement; the
                                       //   nodes' reseed trigger (§9b)
    merged: CollectorShard,            // same shard type — federation reuses the node's
                                       //   machinery; holds per-(node, series) absolutes
    index: SeriesIndex,                // §9a — exact inverted postings for fanout pruning
}
struct SeriesIndex {                   // EXACT, not probabilistic — the closed label
                                       //   vocabulary makes Monarch's field-hints index
                                       //   trivial: every dimension is bounded
    postings: DetHashMap<(DimId, DimValue), SeriesIdSet>,  // dimension-value → series
    by_node: DetHashMap<SeriesIdSet, NodeSet>,             // …and which nodes hold raw
}
struct Assemblers { ring: Vec<Assembler> }   // HRW-owned by trace_id (§8)
struct QueryService {                  // stateless executors; count derives from query
    budget: QueryBudget,               //   load; reads region shards + nodes + cold —
}                                      //   never an ingest queue (§9)
struct Completeness {                  // every query result carries one (§9a)
    leaves_expected: u32, leaves_reported: u32,
    freshness: (Hlc, Hlc),             // min/max source freshness in the merge (H7)
    estimated: bool,                   // true if any input was a sampled source (§9a)
}

// ---- trace assembly (§8) ----
enum TraceSlot { Open { spans: Vec<SpanRecord>, first_seen: Tick, gaps: u32 } }
struct TraceRow { trace_id: TraceId, spans: Vec<SpanRecord>,   // sorted (parent, start)
                  complete: bool, seal_reason: SealReason }
enum SealReason { WindowClosed, Evicted, AssemblerLost }       // all three counted

// ---- claims capture (§10) ----
struct ClaimsCapture { cursor: DeltaCursor,
                       applied: DetHashMap<ClaimUid, LogSeq> } // bounded by LIVE claims
struct ClaimSkeleton {                 // what the ledger's read surface returns to the
    claim: ClaimUid, scope: Scope,     //   join — lifecycle METADATA only, zero content
    timeline: Vec<(LifecycleEdge, Hlc)>,
    trace_refs: BoundedVec<TraceId>,   // system-written (the §16 ledger amendment)
}
struct WorkExecutionView { lifecycle: Vec<(LifecycleEdge, Hlc)>,
                           per_edge: Vec<(LifecycleEdge, Duration)>,
                           traces: Vec<Result<TraceRow, TraceReadError>>,
                           series: SeriesSet }
```

Ownership facts the types carry: a `CollectorShard` is single-owner (one task) — the
roll-up hot path has no lock because nothing shares the struct. `own_log` is the only
durable state the collector itself authors (cursors/watermarks); everything else is
re-derivable (hot, registry, dirty) or already durable elsewhere (the op log, cold
blocks).

## 2b. Routing — the four placement functions (all of them, nothing implicit)

```
measure → shard:      shard_of(k: &SeriesKey) = k.hash % N_shards
                      (stable within a node; N_shards = derived core share; a series
                       lives its whole life on one shard — the single-owner premise)

event   → ring:       events[(record.scope, record.class)] on the shard that drained
                      the source ring (source→shard assignment is fixed at BIND)

record  → log:        op_log partition key = hash(record.scope)
                      (the QUEUE instance's partition key — scope IS the route)

span    → assembler:  a* = argmax over roster n of  ( −w_n / ln(u_n) ),
                      u_n = H64(trace_id ‖ n.id) / 2^64
                      (weighted rendezvous/HRW — the SAME placement mechanism CACHE
                       and SERVING already mandate; the −w/ln(u) logarithmic form is
                       DEFINED HERE as the corpus's canonical formula — pattern by
                       canonical example — so only a changed node's score changes;
                       membership change re-routes exactly K/N)
```

Every routed hop above is fenced by the roster epoch it was computed against
(stale-epoch delivery is refused + re-routed, the corpus's standard fence discipline).

## 3. The node collector — lifecycle and the ingest tick

**Component lifecycle** (one owner task per node drives it):

```
BOOT ──validate registries──▶ BIND ──all bound──▶ RUN ──drain order──▶ DRAINING ──▶ DOWN
        metric ids, class map,   live four (§9),   (tick loop below)   flush uplink,
        span roster (TRACING)    sources, uplink                       seal hot, close logs
   any unregistered participant ⇒ typed BOOT FAILURE (chokepoint law — never degrade)
```

**The ingest tick** (per shard; doorbell-driven, batch-drained — no polling):

```
sources fire doorbells:  host hot-ring (MONITORING §5)   Scribe flows (guest interior)
                         VMM/warden/sensor/gateway rings  ledger delta stream (§10)
        │
        ▼
1. DRAIN     batch = ring.drain_available()          // bounded batch, self-paced
2. DECODE    OpRecord::decode(bytes)?                //   malformed ⇒ drop(Malformed)+count
3. ROUTE     match record.class:
               Verdict|Lifecycle|Audit ─▶ op_log.critical.enqueue(rec)    // durable FIRST
               ClaimMetric             ─▶ op_log.standard.enqueue(rec)    //   then hot
               Telemetry|Span          ─▶ hot only (durable only via §7 interval blocks;
                                          the op-telemetry lane carries interval refs)
4. REDUCE    Measure ⇒ idx = registry.admit(&key); series[idx].record(v); dirty.set(idx)
             Event   ⇒ events[(scope, class)].push(record)   // bounded deque, §2;
                                                             //   overflow ⇒ RingOverrun
             Span    ⇒ keep-flag? forward to assembler route : hot-only (TRACING §5)
5. DELIVER   live FANOUT: class-filtered, scope-filtered push to the bound four (§9)
```

Two orderings are load-bearing: **durable-before-hot** for never-shed classes (a
verdict is on the log before anything can observe it — a crash between 3 and 4 loses
only the hot copy, re-derived on read), and **admit-before-record** (no measurement
ever touches series state except through the §6 chokepoint).

## 3a. The ingest architecture, end to end (what runs where, what connects them)

```
GUEST (one microVM per pod)                HOST (per node)
┌────────────────────────────┐
│ primary container          │
│   runtime emitters ─────── memfd history ring ──▶ drained on the Scribe flow
│   (turn/tool/claim events, │  (MONITORING §3: one-way, enrichment-class)
│    interior spans)         │
│ Scribe container ───────── vsock Scribe flow ───▶ │
│ sensor (guest kernel eBPF)─ vsock sensor chan ──▶ │ warden (host-side, per pod)
└────────────────────────────┘                      │   verdicts ──▶ host rings
  VMM device counters (fork) ───────────────────────▶ host rings   (HostObserved)
  host-truth (/proc, cgroups, steal-time) ──────────▶ host rings
  gateway · scheduler · autoscaler · serving ·      ▶ host rings
  store · queue · consensus chokepoints (host procs)
                                                    │ doorbells (no polling)
                                                    ▼
                     NODE COLLECTOR — a per-node harness service (structural,
                     like the warden; not scheduled work). Shards by
                     hash(SeriesKey); runs the §3 tick:
                       ├─ op-log lanes (3 × QUEUE) ──▶ WAL logical logs
                       ├─ hot (CACHE) + event rings (recent horizon)
                       ├─ kept spans ──▶ assembler route (§2b HRW)
                       └─ uplink (absolute snapshots, §7)
                                                    │
     REGION TIER (per region; placed by the scheduler, fenced by the region
     meta group's rosters)                          ▼
       region shards × R (hash-aligned, §9b) ◀── UplinkInterval (class-1)
       assemblers (trace-id HRW, §8)         ◀── kept spans (class-1)
       query executors (stateless, §9a)      ◀── ObservabilityQuery (reliable)
       sealed blocks ──▶ OBJECT_TIER (content-addressed cold)

     COLOCATION UNIT (per session, on its colocation node): the capture task
     (§10) + the detection substrate (§9, a stage) — session-scoped machinery
     beside the ledger core, reading the plane in-place.
```

The tier boundaries carry the research directly: aggregate-at-the-edge before
anything crosses a wire (Monarch's 36:1), regional autonomy with no global write
fan-in (Monarch zones), hot-in-RAM → durable log → cold blocks (Gorilla's tiering),
and out-of-band collection — no arrow above sits on any work path (Dapper).

## 3b. The networking, hop by hop

Every hop names its transport, PROTOCOL plane/class, and security posture — no
arrow in §3a is unspecified:

| Hop | Transport | Plane / class / archetype | Security & admission |
|---|---|---|---|
| runtime → history ring | memfd ring + eventfd doorbell (intra-VM) | not a network hop (MONITORING §3) | kernel fd custody; enrichment-class by law |
| Scribe flow, sensor → host | **vsock** (guest↔host only — the PODS channel inventory; never claims/tools) | framed PROTOCOL, observability streams | per-workload flow keys (WIRE_SECURITY — a compromised primary cannot forge its Scribe); health-plane reserved slots |
| host chokepoints → node collector | in-process bounded channels (same node, no wire) | — | bounded queues + counted shed (the runtime law) |
| node → region: `UplinkInterval` | UDP datagrams (the claims-plane dual stack) | control plane, **class-1 Observation (sheddable)**, `supersession` archetype (§7) | envelope keys + node identity; MTU-derived budget; loss absorbed by design |
| node → assembler: kept spans | UDP datagrams | class-1 Observation, sheddable | same; loss ⇒ counted gap records ⇒ `incomplete` rows (§8) — never retransmitted |
| live FANOUT → the four | FANOUT's own delivery (reliable durable push, its spec) | FANOUT reliable-push; never-shed carriage for incident/verdict classes | the sealed topic (§9); scope filters stamped at bind |
| queries ↔ executors | **hecate-quic** sessions (reliable, credit-governed streams) | session plane, StreamData class | Noise session identity + the IAM PEP at the serving edge; per-principal budgets (§9a) |
| capture ← ledger deltas | the ledger's delta-stream subscription (hecate-quic ordered stream) | ordered-log archetype (the existing delta-stream lane) | `claim_plane.subscribe_deltas`; cursor + credit |
| sealed blocks → OBJECT_TIER | the durable-plane write path (bulk via TRANSFER) | bulk class (Lane-A passthrough) | content-addressed; OBJECT_TIER admission, `telemetry` class (§16) |

Two properties fall out of the table rather than being asserted: **nothing
telemetry-grade rides a reliable/retransmitting lane** (class-1 + supersession
everywhere on the firehose — loss is absorbed or honestly marked, never queued
against work), and **everything crossing the guest boundary uses the channels the
pod anatomy already defines** — this spec adds zero guest-visible surface.

## 3c. Boot order, dynamic sources, self-observation, and the resource envelope

**Boot order (no circular dependency).** Node boot: WAL → the three QUEUE lanes →
node collector BOOT/BIND → sources begin registering. Emissions *before* the
collector binds are not lost-by-design: every source is a **bounded ring that
buffers** (oldest-overwritten, counted) — the collector drains late and the gap is
an ordinary `RingOverrun` count, never a special boot mode. The collector depends
only on WAL+QUEUE below it; nothing below it depends on the collector (observation
is never load-bearing for boot — a node boots dark-but-working if the collector
fails, and the *node health plane* reports that, per HEALTH's independent liveness).

**Sources attach dynamically.** BIND validates *registries* (metric ids, classes,
the span roster) — the closed vocabularies. The *source set* is runtime-dynamic:
a pod summon registers its rings with the node collector (a lifecycle event on the
control channel), teardown detaches them; host services register at their own boot.
Attach/detach are counted lifecycle events; an unregistered *vocabulary* fails
boot, an attaching *source* is ordinary runtime.

**Self-observation (bounded by construction).** The collector's own operations —
the ingest tick, uplink, query execution, reseed — are chokepoints like any other:
they emit measures/spans **into their own node's shards** under `System` scope. The
recursion terminates structurally: a measurement about a measurement lands in a
roll-up bucket (the terminal form) and generates no further emission — depth is
exactly one. Its own drop counters (§12) are the observability *of* the
observability plane; a collector that cannot report its own drops is what CL10's
CI walk exists to prevent.

**The resource envelope (the collector pays rent like everyone else).** The node
collector's total budget — Σ shard series state + event rings + hot CACHE + uplink
buffers + assembler slots (region nodes) — is a **derived fraction of node
resources**, anchored on a measured overhead ceiling (the receipts: Dapper's
daemon <0.3% of a core, Canopy's backend <0.1% of the datacenter — our ceiling is
derived from the same class of measurement, not copied). Two enforcement edges:
the **scheduler accounts the collector's share in node admission** (pods are
admitted against the remainder — the collector cannot be squeezed into OOM by
admission), and the collector **self-limits at its ceiling** (refuse-first §10 —
over budget it sheds sheddable classes, counted, and never grows past the
envelope). The budget formulas live in §13 with the rest.

## 4. The scoped operational log (D1)

**One logical log, realized as three class-lane QUEUE instances.** QUEUE's
opt-ins are *per-instance declared workload properties* (its own model — a queue
declares what it is; there is no per-message delivery class in QUEUE, deliberately).
So the operational log is one *logical* log whose `OpClass` families map onto three
instances of the one primitive, each with its declared property — zero change to
QUEUE's model:

| Lane (QUEUE instance) | OpClass families | Declared property | Durability | Retention | Why |
|---|---|---|---|---|---|
| `op-critical` | Verdict, Lifecycle, Audit, Incident | default (at-least-once), admission-reserved carriage | the environment-derived default — the strongest the failure-domain tree affords (QUEUE §4); WAL's one always-full ack policy | Session: with the session → archive. System: fleet → cold | a flood must not starve a hard-block; audit and incidents are evidence |
| `op-standard` | ClaimMetric | default (at-least-once) | same single WAL policy (naturally batched — there is no separate "group-commit" tier, WAL §4) | derived (dashboards horizon) | derived work metrics; late shed counted |
| `op-telemetry` | Telemetry, Span | **declared lossy** (QUEUE §10's opt-in: reconstructible/loss-tolerant) | self-ack; loss priced Degraded, never silent | hot horizon → §7 interval blocks → cold | pure telemetry is re-derivable signal, never proof |

- **Still D1's one log**: the "one scope-tagged operational log" decision bars a
  *second substrate* (a session store forked from a system store) — the three lanes
  are class partitions of the one logical log, invisible at the API (`read_events`
  already takes `class`; no cross-class ordering was ever promised; scope remains the
  routing/retention/authz key on every lane).
- **Isolation mechanics, precisely**: never-shed is a *transport-admission* property —
  `op-critical` appends ride the PROTOCOL reserved-slot admission groups (the law
  lives at transport admission, PROTOCOL §7.4, not inside queue storage), and the
  lane's own capacity is not shared with the sheddable lanes *because it is a
  separate instance*. CL3's flood test — 100K/s of Telemetry while a Verdict lands —
  passes structurally: the flood is on `op-telemetry`; it cannot occupy `op-critical`
  capacity at either the transport or the storage layer.
- **Retention executes by scope, through QUEUE's own machinery**: `Session(uid)`
  partitions retire at the session's archive-**finalize** transition (SESSIONS'
  lifecycle word) — the archive-exfiltration consumer acks through the end of the
  partition, the ack floor reclaims it (QUEUE's existing watermark reclaim), and a
  small `close_partition` verb seals it (a listed QUEUE amendment, §16). `System`
  partitions cool to OBJECT_TIER through **QUEUE §7's own cold tier** — the trigger
  is QUEUE's environment-derived one; this spec adds no second cooling authority.

## 5. The roll-up engine (D4)

Aggregation state that must merge **exactly** across tiers. Counters/sums: integer/
float addition. Distributions: **exponential-bucket histograms** — base `2^(2^−scale)`,
bucket `i` covers `(base^i, base^(i+1)]`, relative error `α = (base−1)/(base+1)`.

**Scale derives from anchors** (definition site: the metric registry entry): given
target `α` and span `[lo, hi]`: `scale = min s : (2^(2^−s)−1)/(2^(2^−s)+1) ≤ α`;
buckets = `log2(hi/lo) × 2^scale`. Worked: α=1%, 1 ns→1 day (46.3 octaves) ⇒ scale 5 ⇒
~1,482 buckets ≈ 12 KB. (The OTel default of 160 buckets would force 17% error over
that span — bucket count is derived, never defaulted; CL4.)

*The ruler analogy* (why cross-resolution merging is exact): scales are rulers whose
tick marks nest — every millimeter mark falls exactly on a centimeter ruler's grid,
so re-reading a fine measurement on the coarser ruler is rounding-free re-binning,
not re-measuring. Two nodes can histogram at different precisions and the region
still combines them with zero added error: fold the finer one's ticks onto the
coarser grid (`downscale_to`), then add counts. A ruler whose marks *don't* nest
(fixed-γ DDSketch at a different γ, or t-digest's centroids) can't do this — that is
the entire selection argument.

```rust
impl ExpHistogram {
    /// Bucket covering v. scale ≤ 0 is pure bit extraction — no transcendental.
    fn index(v: f64, scale: i8) -> i32 {
        if scale <= 0 { ieee_exponent(v) >> (-scale) }        // 2^−scale octaves/bucket
        else { (v.log2() * (1i64 << scale) as f64).ceil() as i32 - 1 }
    }
    fn record(&mut self, v: f64) {                            // O(1); the shard owns us
        self.count += 1; self.sum += v;
        self.min = self.min.min(v); self.max = self.max.max(v);
        if v <= self.zero_threshold() { self.zero_count += 1; return; }
        *self.slot(Self::index(v, self.scale)) += 1;          // in-window by derivation:
    }                                                         //   [lo,hi) fixed at registration
    /// Bucket i at scale s lands EXACTLY in i>>1 at s−1 (perfect subsetting):
    /// downscale is pairwise integer folding — zero added error.
    fn downscale_to(&mut self, t: i8) {
        while self.scale > t {
            for i in (0..self.buckets.len()).rev() { self.fold_into(i >> 1, i); }
            self.index_offset >>= 1; self.scale -= 1;
        }
    }
    /// Tier merge: align to min(scale) + integer add. Associative + commutative
    /// ⇒ any merge tree, any arrival order, byte-identical result (CL4).
    fn merge_from(&mut self, other: &ExpHistogram) {
        let s = self.scale.min(other.scale);
        self.downscale_to(s);
        let o = other.at_scale(s);                            // copy-fold; other immutable
        self.add_aligned(&o); self.zero_count += o.zero_count;
        self.count += o.count; self.sum += o.sum;
        self.min = self.min.min(o.min); self.max = self.max.max(o.max);
    }
}
```

**The series lifecycle** (per key, on its owning shard):

```
UNKNOWN ──admit: miss + room──▶ ADMITTED ──record()──▶ DIRTY ──uplink ACK──▶ ADMITTED
   │            ▲                    ▲                   │        (dirty bit clears;
   │            └──admit: hit────────┘                   └─record─┘  state persists)
   │
   └──admit: miss + registry full──▶ FOLDED (measurements land on the overflow
                                     series; counted + alarmed; §6 — terminal until
                                     capacity returns or the metric is re-registered)

Retire: Session-scoped series die with their session's archive seal; System-scoped
series live until their metric is deregistered (a registry change, never runtime GC).
```

**Implementation notes an implementer actually needs:**

```rust
#[inline] fn ieee_exponent(v: f64) -> i32 {   // floor(log2 v), v > 0: biased-exponent
    ((v.to_bits() >> 52) & 0x7ff) as i32 - 1023   // bit extraction; subnormals fall
}                                                  //   into the zero bucket below

fn slot(&mut self, i: i32) -> &mut u64 {           // dense window addressing
    debug_assert!(self.in_window(i));              // guaranteed: [lo,hi] fixed the
    &mut self.buckets[(i - self.index_offset) as usize]   // window at registration
}
```

- **Domain**: `Measure` values are durations/sizes — non-negative by construction; a
  negative value is `Malformed` at decode (step 2), never a histogram concern.
- **`zero_threshold = lo`** (the registered span floor): `v ∈ (0, lo]` counts in
  `zero_count` — no bucket below the span exists.
- **`v > hi`**: clamp into the top bucket **and count** `drops[RangeClamped]` (§12) —
  the value is not lost, the clamp is not silent, and a clamp rate above the derived
  alarm line means the registered span anchor has drifted (re-derive, don't widen
  silently).
- `index_offset` initializes to `index(lo, scale)`; the window never moves after
  registration — `record` is allocation-free for the series' whole life.

Why not the alternatives (receipts): **t-digest is banned** — no proven error bound,
adversarially unbounded (Cormode et al.), order-dependent merge: a tiered roll-up
cannot stand on it. HDR is exact but ~311 KB at this span/precision vs ~12 KB.
Fixed-γ DDSketch has the guarantee but not cross-resolution merge; exponential
histograms are the same guarantee family *plus* perfect subsetting, and they are the
OTel/Prometheus interchange form our vocabulary already targets.

## 5b. The time dimension — a series is windows (the part a lifetime aggregate can't do)

A `TimeRange` query is unanswerable against one lifetime aggregate; the store of
record for a series is **time-bucketed windows** (`WindowedSeries`, §2 — the
Gorilla/Monarch model):

- **Window width `W_res` is per-tier and derived**: node tier at raw resolution
  (`W_raw` from the hot-horizon budget ÷ per-window cost); each federation tier may
  widen (`W_region ≥ W_raw`), and older ranges widen further (multi-resolution
  retention). **Downsampling over time = the §5 merge over adjacent windows** —
  histograms merge exactly (perfect subsetting applies over time exactly as over
  scale), counters take the last cumulative reading, gauges merge (last, min, max).
  One merge, three uses: cross-scale, cross-node, cross-time.
- **Windows close on HLC boundaries** (`window_start = at − (at mod W_res)`), so
  every node cuts the same instants and cross-node window merge aligns without
  negotiation. A closed window is **immutable** — which is what makes the §7
  per-window replace idempotent and re-ships byte-identical.
- **Counters are meter readings**: the window stores the cumulative total at close;
  a rate over `[t1, t2)` is the difference of readings, and `restart_epoch` makes a
  collector restart's reset **detectable** — a reading from a newer epoch never
  differences against an older one (the Prometheus counter-reset lesson, made
  structural instead of heuristic).
- **Late data** (a measurement arriving after its window closed — clock skew, a
  slow drain): lands in the **current** window and increments
  `drops[LateArrival]` — never reopens an immutable window (reopening would break
  the replace idempotence and the region's merge stability). The counted rate is
  the skew alarm.
- **Schema evolution**: a metric's registered `(span, α)` change bumps the series'
  registry version; old windows keep their scale, new windows take the new one, and
  any query merging across the boundary downscales to the common scale — exact, by
  the same subsetting property. No migration, no dual-write.

## 5c. The tier-ownership invariant (no window counted twice)

A window interval is **owned by exactly one tier at query time**: the planner splits
every `TimeRange` at the derived hot-horizon boundary and the cold boundary — windows
younger than the horizon resolve at the owning **nodes** (raw), older-than-horizon at
the **region shards**, colder-than-retention in **sealed blocks** — and a window
never satisfies a query from two tiers (CL16). The boundaries are derived instants,
not races: a window in transit (closed at the node, not yet acked regional) is served
by the node until the region's ack watermark covers it.

## 6. The cardinality limiter (D4b)

**Primary defense — bounded by construction**: `SeriesKey` is closed (§2); per-object
ids are H8-forced out of labels into bounded exemplars. This is Monarch's position
(950 B series, *no* cap — bounded by schema + 36:1 collection aggregation).

**Backstop — aggregate-into-overflow, loud** (per `(scope, metric)`, in the shard).
*The coat-check analogy*: a cloakroom with a fixed number of numbered hooks. When the
hooks run out, additional coats still go in — onto one communal rack. **No coat is
ever turned away** (every measurement is counted; totals stay exact); what degrades
is *retrieval by ticket* (you can no longer ask "which series was that?" for the
communal ones — attribution, not data, is what overflows). The attendant counts every
communal coat and rings a bell the first time the rack is used:

```rust
struct SeriesRegistry {
    admitted: DetHashMap<SeriesKey, SeriesIdx>, // EXACT membership — enforcement must
                                                //   know WHICH key is new; sketches can't
    cap: usize,                                 // derived: shard memory budget ÷
                                                //   sizeof(SeriesState at this scale)
    overflow: SeriesIdx,                        // pre-created at metric registration,
                                                //   labels {overflow:true} — never late
    folded: u64,                                // distinct keys folded (§12 category)
    hll: Hll,                                   // registers from target error (1.04/√m);
}                                               //   observes ALL keys, admitted or not

impl SeriesRegistry {
    /// The ONLY path from a label tuple to a series slot.
    fn admit(&mut self, key: &SeriesKey) -> SeriesIdx {
        self.hll.observe(key.hash);
        if let Some(&i) = self.admitted.get(key) { return i; }
        if self.hll.estimate() > self.alarm_line() {          // derived fraction of cap:
            raise_health(CardinalityPressure);                //   loud BEFORE folding
        }
        if self.admitted.len() < self.cap {
            let i = self.alloc(key);
            self.admitted.insert(key.clone(), i);
            return i;
        }
        self.folded += 1;                                     // counted (§12)…
        if self.folded == 1 { raise_health(CardinalityOverflow); }  // …and alarmed
        self.overflow                                         // totals exact; attribution
    }                                                         //   degrades; NEVER a drop
}
```

The rejected dispositions are **unrepresentable**: no drop path exists (every
measurement lands in some series — Mimir's drop-new-series silently vanishes new
pods), and no whole-batch reject exists (Prometheus's `up=0` destroys good data with
bad). **Recovery semantics** (§11): the registry is re-derivable — rebuilt from the
hot store's live series on restart; after a node death that also loses hot, keys
re-admit organically and *which* keys hold admitted slots may differ across the crash.
Totals stay exact; attribution stability across node death is best-effort — stated,
not hidden (telemetry class; Verdict/Audit never depend on the registry).

## 7. Federation — what actually moves node → region

The uplink is an interval shipper of **absolute series state**, not a stream mirror
and not a delta protocol:

```rust
struct UplinkInterval {
    node: NodeId, roster_epoch: Epoch,       // fenced (§2b)
    seq: u64,                                // monotone per node; gaps legal
    series: Vec<(SeriesKey, WindowSnap)>,    // ABSOLUTE state per dirty series, PER
                                             //   WINDOW: every CLOSED window since the
                                             //   receiver's last-known, plus the open
                                             //   window marked partial. Replace-apply
                                             //   keys on (node, series, window_start) —
                                             //   idempotent per window; a re-shipped
                                             //   closed window is byte-identical
                                             //   (closed = immutable)
    sealed_refs: Vec<ContentHash>,           // event/span blocks sealed this interval
}
```

**The uplink state machine** (one per node):

```
ACCUMULATING ──T_up fires──▶ SHIP(seq=n: absolute snap of every DIRTY series)
      ▲                            │
      │                       IN_FLIGHT(n)
      │                        │        │
      │   ack(n): clear the    │        │ loss / timeout (derived from measured RTT):
      │   shipped series'  ◀───┘        │ NOTHING is resent —
      └── dirty bits                    └──▶ ACCUMULATING (bits still set; the NEXT
                                             interval re-ships current absolutes)
```

- **Idempotent by construction**: the region applies an interval by **replace**, keyed
  `(node, series)` — `region[(node, key)] = snap` if `seq` > the stored seq for that
  node, else discard. Re-delivery, re-ship after a lost ack, reordering: all safe —
  replace is idempotent; a stale `seq` is simply discarded.
  - *Rejected alternative, recorded*: shipping **deltas** since the last ack. It
    double-counts on the ack-lost-but-interval-received path (the node re-ships
    changes the region already merged) unless a base-sequence negotiation is added —
    a protocol to get wrong, for bytes we don't need to save. Absolute-replace has no
    such path. Correctness over wire thrift (the doctrine's ordering).
- **Cross-node aggregation happens at read/roll-up, not at apply**: the region holds
  per-`(node, series)` latest absolutes; a regional series value = `merge_from` across
  the node entries (§5 — exact, any order). A dead node's entries freeze and retire
  with node liveness (the fabric's verdict, not a timer here).
- **When**: `T_up = Σ dirty-series-bytes / uplink_budget_bytes_per_sec`, clamped by the
  staleness bound consumers declared (HEALTH freshness); recomputed as anchors drift.
- **Wire**: class-1 sheddable datagrams under the PROTOCOL MTU budget; an interval
  larger than the datagram budget splits by series (each fragment a complete,
  independently-appliable `UplinkInterval` sharing `seq` — replace semantics make
  partial arrival safe). Sustained loss trips AbsenceIs staleness region-side.
  **`UplinkInterval` registers as a message kind under the `supersession` archetype**
  (a newer absolute for the same `(node, series)` supersedes an older one; nothing is
  ever retransmitted — exactly supersession's contract) in PROTOCOL's boot classifier
  (§16 amendment; an unclassified kind fails startup, PROTOCOL's law).
- **Fan-in bounded by node count** (one uplink per node, H6), never pod count.
- `N=1`: the uplink target is the node itself — same code path, loopback hop, no mode.

## 8. The trace assembler (D5)

Kept spans (TRACING §5 head decision) arrive at the region tier; routing is
**`weighted_hrw(trace_id, roster)`** (the §2b function — the CACHE's placement
mechanism reused; a membership change re-routes exactly the departed share, K/N).

**The trace-slot state machine** (per `trace_id`, on its HRW-owned assembler):

```
(no slot) ──first span──▶ OPEN ──span──▶ OPEN   (append; in-band gap records → gaps+=1)
              │
              ├── window W expires ─────▶ SEAL(WindowClosed)
              │                            complete = (gaps == 0 ∧ has_root)
              ├── capacity eviction ────▶ SEAL(Evicted)        incomplete, counted
              └── assembler dies ───────▶ state lost; survivors that receive later
                                          spans open a fresh slot ▶ SEAL(AssemblerLost)
                                          incomplete, counted

SEAL is terminal: row → hot (CACHE) → OBJECT_TIER on retention; the slot is removed.
A span arriving AFTER its trace sealed opens a new slot that will itself seal
incomplete (no root) — late spans never resurrect a sealed row (rows are immutable).
```

```rust
struct Assembler {
    slots: DetHashMap<TraceId, TraceSlot>,  // capacity = derived(throughput × W)
    window: Duration,                       // W = p99 trace duration × derived margin
    timers: TimingWheel<TraceId>,           // the same ordered-wheel mechanism CACHE
}                                           //   uses internally (shared component in
                                            //   the runtime, not a CACHE export)
impl Assembler {
    fn on_span(&mut self, s: SpanRecord) {
        debug_assert_eq!(weighted_hrw(s.trace_id, roster()), self.id);  // fenced route
        match self.slots.entry(s.trace_id) {
            Vacant(e)   => { e.insert(TraceSlot::open(s));
                             self.timers.arm(s.trace_id, self.window); }
            Occupied(e) => e.get_mut().push(s),     // in-band gap records counted here
        }
        if self.slots.len() > self.capacity() {     // bounded, never grows silently:
            let t = self.timers.oldest();
            self.seal(t, SealReason::Evicted);      //   oldest seals early, counted
        }
    }
    fn on_expiry(&mut self, t: TraceId) { self.seal(t, SealReason::WindowClosed) }
    fn seal(&mut self, t: TraceId, why: SealReason) {
        let slot = self.slots.remove(&t).unwrap();
        let complete = slot.gaps == 0 && slot.has_root()
                       && why == SealReason::WindowClosed;
        self.hot.put(t, TraceRow { trace_id: t, spans: slot.sorted(),   // (parent, start)
                                   complete, seal_reason: why });
    }                                               // hot → OBJECT_TIER on retention
}
```

Membership change: a surviving assembler receiving a mid-trace span with no slot opens
one; the earlier spans died with the lost node's window and the row seals
`AssemblerLost`, incomplete — **counted, never silently whole** (TR8 carried through).

## 9. The consumer surface (D2)

**Live class — the closed four**, structurally:

```rust
const LIVE: [LiveConsumer; 4] = [Scribe, ScoreService, Guardian, Guide];
fn bind_live(reg: &mut FanoutRegistry) -> Result<(), BootError> {
    for c in LIVE {
        reg.bind(c, c.class_filter(), c.scope_filter())?;  // missing ⇒ typed boot fail
    }                                                      // Scribe's scope_filter =
    reg.assert_exactly(Class::Live, &LIVE)                 //   its primary ONLY, stamped
}                                                          // a fifth binder ⇒ boot fail
```

Delivery is the FANOUT instance (reliable-push default), class- and scope-filtered at
the emitter, riding reserved capacity. Adding a live consumer is an amendment to this
spec, not a subscription — and that is closed at **both** layers: the boot assertion
above catches a fifth binder at startup, and **the live topic is sealed** — no
principal holds `topic.create_subscription`/`subscribe` on it (an IAM policy fact +
a FANOUT sealed-topic amendment, §16), so the runtime-open subscription surface FANOUT
normally offers does not exist here. Boot-closed *and* runtime-closed.

**The detection substrate is a stage of this pipeline, not a consumer of it.** The
HANDOFF detection substrate (per-session, resident in the session's colocation unit —
the accepted placement) is pipeline machinery, exactly like the roll-up engine: it
consumes its session's live streams *in-plane* — filtered to `HostObserved`
provenance only (the MO2 law: detection reads authority streams; the `provenance`
series dimension in §2 is what makes this filterable after roll-up) — computes its
detector statistics, and **emits enriched incidents back into the plane**, which
reach the Scribe through the Scribe's own live binding (one of the four). Detection
therefore never appears in the consumer roster: the four consume the plane's
*outputs* (incidents included); the substrate is part of what produces them. This is
the reconciliation of HANDOFF §4 ("distinct from the score service, not pod RAM, not
Scribe memory") with the closed four — neither list changes.

**Query class — the stored plane, off the ingest path**:

```rust
trait ObservabilityQuery {
    fn read_series(&self, caller: &Principal, scope: Scope, sel: LabelSelector,
                   range: TimeRange, res: Resolution) -> Result<SeriesSet>;
    fn read_events(&self, caller: &Principal, scope: Scope, class: OpClass,
                   range: TimeRange, cursor: Option<Cursor>) -> Result<EventPage>;
    fn read_trace (&self, caller: &Principal, t: TraceId) -> Result<TraceRow>;
    fn join_work  (&self, caller: &Principal, claim: ClaimUid)
                   -> Result<WorkExecutionView>;            // §10
}
```

- **Every call crosses the IAM `observability` capability at the serving edge** (the
  PEP): Scribe → its primary's scope; Guardian broad; user per SafetyPolicy;
  Archivalist per its grant (wired in the agents' spec — the collector owns the
  surface, each consumer's contract lives with the consumer).
- **Execution** is §9a's model (plan → prune → tree → merge → completeness); the
  region tier it reads is §9b's sharded, reseedable projection.
- **Structurally off ingest** (CL7): the `QueryService` is a separate task class with
  its own budget; no query path touches an ingest queue (architecture test) — an
  investigation storm cannot degrade the telemetry it investigates.

## 9a. Query execution — plan, prune, tree, merge, honesty

The research this section stands on: Monarch's pushdown + field-hints index (fanout
pruned 99.5% at zone level; disabling it cost 10×) and Scuba's aggregation tree
(fanout 5, 10 ms leaf timeouts, **best-effort with the completeness printed on the
result** — "Only 94.6% of all samples were processed"). Both imported, with one
upgrade our closed vocabulary buys: the index is *exact*, not probabilistic.

**1. Plan.** `read_series(scope, sel, range, res)` splits by tier ownership — the
§5c invariant: every window interval in `range` is assigned to **exactly one** tier
(no window counted twice; in-transit windows resolve to the node until the region's
ack watermark covers them):

```
range ∩ hot-horizon(scope)   → NODE sub-queries (raw windows, at the owning nodes)
range ∩ rolled(scope)        → REGION-SHARD sub-queries (merged windows)
range ∩ cold(scope)          → COLD sub-queries (sealed blocks by ref, OBJECT_TIER)
```

The same three-way split plans `read_events` (event rings → durable-lane cursors →
sealed event blocks) and `read_trace` (assembler hot rows → sealed trace rows) —
one planner, three result shapes.

**2. Prune (the fanout killer).** The selector is resolved against the
`SeriesIndex` — exact inverted postings per closed dimension (`metric`, `principal`,
`op`, `domain`, `provenance`, declared dims). Intersection of the selector's posting
sets names the exact series set; `by_node` names the exact node set holding raw
data. **A query touches only the shards and nodes the index names** (CL14) — never
a broadcast. Monarch needed trigram fingerprints because its fields are open
strings; ours are closed registries, so the index is small (postings over bounded
vocabularies), exact, and rebuilt-with-the-shard (it is derived state).

**3. Tree.** Sub-queries fan through an **aggregation tree of derived fanout `F`**
(`F` from per-hop merge cost vs latency budget — the Scuba shape; depth
`log_F(targets)`); every interior node merges partials with the *same* §5 merge
(exact, order-free), so the tree adds latency structure, never error.

**4. Leaf discipline.** Each leaf has a **derived timeout** (from the tier's measured
response distribution); a leaf that misses it is *omitted and counted* — the query
never hangs on a straggler (Scuba's 10 ms rule, derived instead of literal).

**5. Honesty — every result carries `Completeness`.** `leaves_reported /
leaves_expected`, the merge's `(min, max)` source freshness (H7: staleness is data
the consumer judges — a dead node's frozen absolutes are visibly stale from the
moment its uplink lapses, not first at the liveness verdict), and `estimated`.
**A partial result that doesn't say it's partial is the failure class** (CL14); the
Scuba warning line — "only 94.6% processed, sums will be low" — is the contract,
machine-readable.

**6. Sampled-source compensation.** Series derived from head-kept traces (TRACING
§5) carry their keep-rate in the metric registry; rate/count estimates from them
scale by `1/keep_rate` and set `estimated: true` (Scuba's `sample_rate`
compensation, made explicit). Series from 100%-kept classes and all durable-class
events are exact and never marked.

**7. Cost bounding (the LIST-blowup class).** Three structural bounds, all derived:
a selector must resolve through the index to a **bounded series set** before
execution (an unresolvable/unbounded selector is a typed refusal, not a scan);
results stream in **bounded chunks** with a cursor (no whole-result
materialization — the KEP-3157 lesson: "16 informers took down the cluster");
per-principal **query budgets** admission-gate concurrent cost at the serving edge
(IAM-attributed, so an investigation storm is throttled per principal, not
collapsed globally).

## 9b. The region tier — sharding, reseed, and why there are no replicas

**Sharding.** The region tier is `R` **region shards**, partitioned by
`SeriesKey.hash` — the *same* hash-partition function the node shards use, so a
series has one home at every tier. `R` derives from the region's admitted-series
count × per-series cost ÷ per-instance memory budget. Each node's uplink **cuts its
interval fragments along region-shard boundaries** (§7's by-series fragmenting,
aligned to the shard ranges), so a region shard receives exactly its own series
from every node — fan-in per shard stays bounded by node count (H6), and no region
instance sees the whole region's series. Assemblers shard separately by
`trace_id`-HRW (§8); query executors are stateless and scale by query load.

**Why no replicas — the projection argument.** A region shard holds only
**re-derivable state**: per-`(node, series)` absolutes whose source of truth is the
nodes (which hold current state and re-ship it), plus an index derived from those
absolutes. This is the same class as the materializer's read projections (STORE's
"reconstructible projection" precedent): durability lives in the op-log lanes, the
cold blocks, and the nodes' own state — **replicating the projection would buy
availability-during-reseed at the price of a consensus group per shard**, for data
that is by definition seconds-stale telemetry. Rejected; availability during reseed
is handled honestly by `Completeness` instead.

**Reseed (the recovery mechanic, exact).** A region shard's `epoch` bumps on any
(re)placement. Nodes observe the bump (the shard roster is a watched, fenced map —
the standard epoch-consumed-map discipline):

```
region-shard lifecycle:   PLACED(epoch′) ──▶ RESEEDING ──▶ LIVE
                                              ▲      │
node side, on epoch′:  mark ALL admitted      │      └ converged when every live
series owned by that shard DIRTY ──▶ normal   │        node's reseed interval is
uplink machinery re-ships absolutes ──────────┘        applied (per-node seq seen)
```

No new protocol exists: reseed **is** the §7 uplink with every relevant dirty bit
set — replace-apply makes it idempotent, arrival order free. During RESEEDING the
shard serves queries with `Completeness` showing the gap (leaves_reported over
expected + stale freshness), never a silent hole. The old instance's state needs no
handoff — it is discarded (the nodes are the source).

**Cold reads.** Queries over cold ranges resolve sealed-block refs from the op-log
lanes (each sealed interval's `sealed_refs`, §7) and read the content-addressed
blocks from OBJECT_TIER directly — the region shard indexes refs, never proxies
block bytes.

## 10. Claims-work capture + the join (D3+)

**Capture** — an ordinary cursor consumer of the ledger's delta stream (`LEDGER` §8;
"the log is the outbox"), one per session. Its **home is the session's colocation
unit** (beside the detection substrate — a SESSIONS §2 service-list amendment, §16),
its standing is IAM's existing `claim_plane.subscribe_deltas` action at the ledger
serving edge, and its durable state rides the colocation node's `own_log`:

```rust
impl ClaimsCapture {
    fn on_batch(&mut self, deltas: &[Delta]) -> Result<()> {
        for d in deltas {
            let w = self.applied.entry(d.claim_uid).or_insert(LogSeq::ZERO);
            if d.log_seq <= *w { continue; }   // redelivery — already counted (CL8).
                                               // Dedup key = the ledger's OWN per-claim
                                               // total order: no vocabulary, no window,
                                               // nothing to tune or get wrong.
            self.derive(d);                    // claim_posted_total; per-edge
                                               //   claim_transition_duration histos;
                                               //   time_to_testament; validation_outcomes;
                                               //   park/resume; claim_coherence; exemplar
            *w = d.log_seq;
            if d.is_terminal_released() { self.retire.push(d.claim_uid); }
        }
        self.applied.retain(not_retired());    // retirement lands in the SAME checkpoint
                                               //   that records the terminal — no window
                                               //   where a redelivered terminal re-counts
        // ONE atomic append to own_log: {cursor', the FULL applied map}. The map is
        // bounded by LIVE claims (small), so a full snapshot per checkpoint buys
        // single-record recovery — read the LAST checkpoint, nothing replayed from
        // older ones. Crash ⇒ resume the delta stream from that cursor; the
        // watermarks turn every reprocessed delta into the `continue` above.
        // Exactly-once effect, no 2PC, ZERO ledger writes.
        self.own_log.append_atomic(&CaptureCheckpoint {
            cursor: self.cursor.advanced(deltas), applied: self.applied.clone() })
    }
}
```

**The capture state machine** (one task per session stream):

```
BOOT ──read LAST CaptureCheckpoint from own_log──▶ REPLAY(subscribe delta stream
   (none ⇒ cursor = stream start, applied = ∅)      at checkpoint.cursor)
        │                                                │
        │             typed RESYNC (cursor below the stream's retention — the
        │             projector contract's mandatory path): reset applied = ∅,
        │             re-derive from the stream's re-seed point; the re-derived
        │             series REPLACE the capture-owned series wholesale (one
        │             writer, §10's ownership rule — never merged)
        ▼ caught up to the live edge
   STREAMING ──batch arrives──▶ DERIVING (the loop above) ──append checkpoint──▶ STREAMING
        │
        crash at ANY point ⇒ BOOT.
```

**The derive-vs-checkpoint crash window, closed.** A crash *between* `derive` and the
checkpoint append leaves the in-memory series holding effects the durable watermark
does not record — which would double-count if that state survived into replay. It
never does: **capture-derived series are owned exclusively by the capture task**, and
BOOT unconditionally **rebuilds them by replay** from the last checkpoint's cursor —
it never merges with pre-crash in-memory state (there is none after a restart, and a
surviving shard's copy of a capture-owned series is discarded at capture BOOT, not
merged). Re-derivation is safe because `derive` is a pure function of the delta —
replaying the uncheckpointed suffix reproduces the exact effects once. One writer,
one recovery source, no double-count path (CL8's crash-fuzz covers precisely this
window).

**The one ledger-side amendment** (§16): the runtime stamps **`trace_refs`** into the
**system-written** lifecycle record (beside timestamps/status in `ClaimLifecycle` —
runtime-authored, bounded, never agent content), completing the TRACING §1 cross-link
at first class.

**The join** — integration at the query layer, separation at the storage layer:

```rust
impl ObservabilityQuery for QueryService {
    fn join_work(&self, caller: &Principal, claim: ClaimUid)
        -> Result<WorkExecutionView>
    {
        // 1. The ledger's OWN read surface, under the CALLER's ledger capability —
        //    the join holds no ledger authority of its own to lend.
        let skel = self.ledger_read.skeleton(caller, claim)?;
        // 2. Each trace under the CALLER's observability capability, per read;
        //    per-ref failures are typed entries, not a poisoned result.
        let traces = skel.trace_refs.iter()
            .map(|t| self.read_trace(caller, *t)).collect();
        // 3. The UID-exemplared series over the claim's own span.
        let series = self.read_series(caller, skel.scope,
                                      LabelSelector::exemplar(claim),
                                      skel.time_span(), Resolution::Raw)?;
        Ok(WorkExecutionView::compose(skel, traces, series))
    }   // No path takes anything but `caller`: a compromised query service can
}       // deny, never widen — it holds no capability of its own (CL9).
```

## 10b. Lifecycles — how collector machinery is born, lives, and dies

**A metric** (the vocabulary lifecycle): a subsystem's bundle declares its metrics
(`MetricId`, op vocabulary, dims, `(span, α)` anchors, keep-class for its trace
roots) as **REGISTRY documents**; publication flows through the registry's ordinary
watch — node collectors observe the new entry, shards accept `admit()` for it from
then on. **Deregistration** stops admission, retires the series at the tier
retention horizons, and the registry version stamps every window (schema evolution,
§5b). No metric exists outside the registry — the §3 boot validation is a read of
this same source.

**A session's observability** (born and dies with the session): the session-create
gang admission (SCHEDULER's colocation-unit transaction) includes the **capture
task** — it is home machinery like the ledger core, not an afterthought summon.
Live: §10's loop. Session close: the capture drains its stream to the close point,
appends its final checkpoint, and the archive-exfiltration consumer's ack-through +
`close_partition` retire the session's op-log partitions at archive-finalize (§4).
The session's series and windows age out at their horizons; its sealed blocks
follow the archive's lifecycle. **A session leaves nothing resident.**

**A node** (join/leave): join — the node collector boots with the node (§3c order),
sources attach, the uplink registers with its region shards (first intervals seed
its `(node, series)` entries). Drain — `DRAINING` (§3): stop intake, flush the
uplink, seal hot, final capture checkpoints, close logs; the region's entries for
the node go stale-visible (H7) and retire on the liveness verdict. Crash — §11's
matrix; the region's frozen entries are the crash's visible shadow until liveness
retires them.

**Region machinery** (shards/assemblers/executors): placed and re-placed by the
scheduler as ordinary work; every placement bumps the fenced roster epoch (§9b/§8);
reseed and HRW re-routing are the only migration mechanics — there is no state
handoff anywhere in this spec, by design (all region state is projection).

## 11. Failure & recovery matrix

| What dies | What is lost | Counted where | What recovers, from where |
|---|---|---|---|
| A source ring overflows | oldest unpersisted telemetry | `drops[RingOverrun]` + in-band gap records | nothing — lossy class; gaps surface in assembled traces (§8) |
| A collector shard task | hot tail since last hot write | `drops[ShardRestart]` | shard restarts; registry rebuilt from hot's live series; series re-admit |
| The node collector (restart) | hot store + registry + dirty set | `drops[NodeCollectorLoss]` | op_log (durable classes) intact; own_log replays capture cursors/watermarks (§10 ⇒ exactly-once holds across the crash); series re-admit; overflow membership may differ (§6, stated) |
| The node PERMANENTLY (own_log gone) | additionally: the capture checkpoints | `drops[NodeCollectorLoss]` | the re-summoned capture task has no checkpoint ⇒ full re-derivation from the delta stream (or its RESYNC re-seed point) — correct by the same replay purity, priced as recovery time, never as wrong counts |
| The uplink / an interval | one interval's latency | absorbed (dirty bits persist until ack, §7) | the next interval re-ships current absolutes; replace-apply makes any re-delivery safe; sustained ⇒ region AbsenceIs staleness |
| An assembler | its open windows | `SealReason::AssemblerLost` rows | HRW re-routes exactly its share; survivors seal partial rows incomplete |
| A region shard | its merged absolutes + index | `drops[RegionLoss]` | node tiers unaffected (autonomy); epoch bumps ⇒ nodes mark its series dirty ⇒ the ordinary uplink reseeds it (§9b — no handoff, no replica); queries meanwhile carry the gap in `Completeness`, never a silent hole |
| The QUEUE log's node | per QUEUE's own spec | — | QUEUE durability (environment-derived replication); not this spec's mechanism |

The invariant across every row: **proof-grade classes (Verdict/Lifecycle/Audit/
Incident, capture checkpoints) live on durable logs and survive; telemetry-grade
loss is bounded, counted, and visible** — never silent, never blocking work.

## 11b. Threat posture — when the collector itself is the compromised thing

The plane observes everything, so its own compromise must be priced (the
MONITORING §9 discipline applied to this spec's components):

- **A compromised node collector** lies **as its node, about its node** — it holds
  the node's harness identity and per-node envelope keys, so it cannot forge
  another node's uplink or speak for another node's series (the region keys
  entries by authenticated node identity). It holds **no IAM capabilities** — it
  cannot read the ledger, cannot query other scopes, cannot widen anything. Its
  blast radius is one node's telemetry being wrong — which cross-view validation
  is built to catch: its guest-vs-host divergence signals go quiet or incoherent,
  and the *other* host-observed surfaces about that node (VMM counters at the
  region, liveness fabric, scheduler telemetry) don't pass through it.
- **A compromised region shard** can serve wrong merges and wrong completeness for
  its series range — to **queries only**: detection does not read the region tier
  (the stage runs in each session's colocation unit on its own live streams, §9),
  the score service reads its ordered outcome stream, and nothing on any work or
  authority path consumes regional merges. Blast radius: dashboards and
  investigations over one shard range, bounded and re-seedable (kill it and the
  nodes rebuild the truth).
- **A compromised query service** can **deny, never widen** (§10's join argument,
  generalized): it holds no capability of its own; every read it performs is under
  the caller's checked capabilities per plane. Worst case: refused or garbled
  query results — visible, never an authority leak.
- **The trust root** for `HostObserved` provenance is the node harness identity
  chain — the same root the warden and the wire already stand on; this spec adds
  no new root and no new key custody beyond the per-node uplink identity.

Bar A / Bar B carry through from MONITORING §9 unchanged: everything guest-emitted
is `GuestReported` by construction (§2's provenance dimension) and nothing
authority-grade ever depends on it.

## 12. The drop taxonomy (closed — an uncategorized drop is a bug)

`Malformed | RingOverrun | ShardRestart | NodeCollectorLoss | RegionLoss |
UplinkShed | QueueShed(class) | CardinalityFolded | RangeClamped | LateArrival |
TraceEvicted | AssemblerLost | QueryPartial(tier)` — one counter each, all scope-tagged, all queryable as ordinary
series. CI walks every shed/loss code path and asserts it lands in exactly one
category (CL10); a new loss path without a category fails the build.

## 13. Derived constants (every one; definition site = where the formula lives)

| Constant | Formula | Anchors |
|---|---|---|
| Histogram `scale` / buckets | §5 | (span lo–hi, target α) per metric-registry entry |
| Registry `cap` | shard memory budget ÷ sizeof(SeriesState) | shard budget, scale |
| HLL registers / alarm line | target error (1.04/√m); derived fraction of cap | error target, cap |
| Exemplar `N_EX` | exemplar budget ÷ sizeof(ClaimUid) | per-series byte budget |
| Uplink `T_up` | Σ dirty bytes ÷ uplink budget, clamped by declared freshness | uplink b/s, HEALTH freshness bounds |
| Assembler `W` | p99 trace duration × margin | measured trace-duration distribution |
| Assembler capacity | kept-span throughput × W | measured keep rate |
| Keep baseline rates | kept-volume budget ÷ measured class volume (TRACING §5) | region capacity, class volumes |
| Hot retention | hot budget ÷ ingest byte rate | node memory share |
| Cold seal trigger | age/size from retention class | scope class policy |
| Region shards `R` | admitted-series count × per-series cost ÷ instance memory budget | region series census, instance budget |
| Tree fanout `F` | per-hop merge cost vs the query latency budget | measured merge cost, latency SLO |
| Leaf timeout | derived from the tier's measured response distribution | per-tier response p99 |
| Query budgets | per-principal concurrent-cost admission at the serving edge | executor capacity, principal class |
| Reseed convergence | every live node's post-epoch interval applied (per-node seq) | node census, `T_up` |
| Window widths `W_raw`/`W_region`/older | hot budget ÷ per-window cost; widened per tier by retention ÷ ring length | hot budget, per-window bytes, tier retentions |
| Hot-horizon boundary | node hot budget ÷ ingest rate, aligned to `W_raw` | node memory share, measured rate |
| Collector overhead ceiling | derived from measured per-signal cost × emission census (the Dapper/Canopy overhead-class measurement) | measured collector cost, node capacity |
| Collector node share | overhead ceiling + derived headroom; accounted by scheduler admission | the ceiling, admission model |

No literal constant exists in this spec's implementation; each formula's inputs are
measured anchors, recomputed as they drift (CL12).

## 14. Worked example — one slow claim, end to end

An Engineer services claim `C47` (scope `Session(s9)`); its VFS mount is slow.

1. **Emission**: the pod's chokepoints emit — `gateway.call` span (350 ms),
   `vfs.mount` span (5.8 s), warden `Verdict{allow}`, token counters — async to their
   rings; the turn's trace roots at the summon chokepoint, class = turn-op ⇒
   **keep=100%** (TRACING §5), flags propagate.
2. **Node tick** (§3): rings drain; the Verdict appends to the op log **never-shed,
   durable first**; measures hit `admit` → existing series → `record(5.8s)` lands in
   bucket `index(5.8, scale=5)`; `dirty` marks the series; spans carry keep ⇒ forward.
3. **Ledger deltas** (§10): `C47`'s transitions arrive on the capture cursor;
   `claim_transition_duration{edge=progressed}` records 6 min — with `C47` stamped as
   exemplar; the checkpoint `{cursor', C47→log_seq}` appends to own_log.
4. **Uplink** (§7): at `T_up`, the dirty series ship as absolute snapshots
   (`seq=n`); the region replaces its `(node, series)` entries — idempotent — and
   the regional value merges across nodes via §5, exact at the region's scale.
5. **Assembly** (§8): the trace's spans HRW-route to assembler `A3`; the window
   closes; `TraceRow{complete: true}` seals to hot.
6. **Detection** (HANDOFF): session s9's detection substrate — in its colocation
   unit, reading its own session's live `HostObserved` streams in-plane (§9's
   stage-not-consumer rule) — trips the `vfs.mount` residual-CUSUM; the
   fully-enriched deterministic incident enters the plane and reaches the Scribe
   through the Scribe's live binding.
7. **Investigation** (§10): the Scribe runs `join_work(C47)` under its own
   capabilities: skeleton (posted 14:01, testament 14:09, `trace_refs=[T]`), trace `T`
   (the 5.8 s `vfs.mount` span), the exemplared series. The series read executes per
   §9a: the index resolves the selector to exactly the s9/`vfs.mount` series on two
   region shards + the raw hot horizon on node-3; three leaves, one merge hop
   (`F` ≥ 3), all leaves report ⇒ `Completeness{3/3, fresh, estimated: false}`.
   Answer: *the claim was slow because its mount was* — one call, two planes, zero
   fusion, and the result says how complete it is.
8. **A failure variant**: had assembler `A3` died mid-window, `C47`'s row seals
   `AssemblerLost/incomplete` on a survivor; `join_work` returns the trace with its
   typed gap; the *metrics* (steps 3–4, durable + exact) still carry the 6-minute
   edge — detection never depended on the lossy trace.

## 15. Laptop degenerate

`N=1`: the node tier is the region tier (loopback uplink, same code); one assembler;
one shard set; the same formulas produce laptop numbers from laptop anchors. Zero
modes anywhere (CL12).

## 15a. Integration (every companion touchpoint, enumerated)

- **MONITORING** — the emission rings (§3a's sources) are its plane; the hot-ring
  role amendment (§16) makes the ring the source buffer and this spec the store.
  Provenance classing (§2's dimension) is its §8 law carried into series identity.
- **TRACING** — spans arrive in its §3 shape; the keep flag (§5) decides assembler
  forwarding; §8 is the assembly TRACING §6 defers; TR8's incomplete-marking is CL6.
- **HANDOFF** — the detection substrate is a stage of this pipeline (§9), reading
  `HostObserved` streams in-plane; its incidents reach the Scribe via the Scribe's
  live binding. Its detector-state checkpointing is its own spec's concern.
- **WAL** — the op-log lanes are QUEUE-over-WAL; `own_log` is a registered
  logical-log client with the `capture_checkpoint` record kind (§16); checkpoint
  cadence/format are client-owned per WAL's floor contract.
- **QUEUE** — three declared-property lane instances (§4); `close_partition` at
  archive-finalize (§16); the cold tier is QUEUE §7's own.
- **CACHE** — the hot store (its spec names "the collector hot-ring" as a client);
  the timing wheel and weighted-HRW are shared runtime mechanisms, with the
  canonical HRW formula defined at §2b.
- **FANOUT** — live delivery on a sealed topic (§16); incident/verdict classes ride
  never-shed carriage.
- **OBJECT_TIER** — the `telemetry` storage class + op-log-referenced GC liveness
  root (§16); sealed blocks are ordinary content-addressed durable-plane objects.
- **PROTOCOL / WIRE_SECURITY** — §3b's hop table: class-1 Observation carriage,
  the `UplinkInterval` supersession-archetype registration (§16), per-workload flow
  keys at the guest boundary, reserved slots for the health/observability plane.
- **IAM** — the `observability` capability gates every query at the serving-edge
  PEP (§9); per-principal query budgets; the capture task stands under
  `claim_plane.subscribe_deltas`; the §4-row amendment (§16).
- **LEDGER / LEDGER_CORE** — the capture is an ordinary delta-stream cursor
  consumer ("the log is the outbox"); `trace_refs` lands in the system-written
  lifecycle record; the skeleton read rides the serving edge's metadata split; zero
  ledger writes, no second authority (§10).
- **SESSIONS** — session-scoped retention keys off archive-finalize (§4); the
  capture task and detection substrate live in the colocation unit (§16 list
  amendment); a session's telemetry dies with its session, like everything else.
- **SCHEDULER** — region shards, assemblers, and query executors are scheduled
  tasks (placement via the ordinary admission path); the node collector is a
  structural per-node harness service (like the warden), not scheduled work.
- **CONSENSUS** — the region-shard and assembler rosters are fenced placement-map
  versions owned by the region meta group (CAS-first, §6's existing class — no new
  epoch kind); every §2b route checks its roster epoch.
- **HEALTH** — H6 bounds fan-in by node count; H7's `(value, freshness)` rides every
  merged read; H8's type-walk covers every record and span type; AbsenceIs marks
  uplink lapse and query partials.
- **RUNTIME** — every task here is bounded and tracked (no untracked goroutines' Rust
  equivalent); shard state is single-owner; hashing/tiebreak via the seeded driver.

## 16. Amendments landing with acceptance (one coordinated sweep)

**Substrate registrations** (the reconciliation found the first draft amended none of
the five primitives it composes from — the CACHE/QUEUE/FANOUT-acceptance precedent
requires all of these):

- `QUEUE.md` — a `close_partition` verb (seal a partition at session
  archive-finalize; reclaim rides the existing ack-floor watermark). The three op-log
  lanes themselves need **no** model change (per-instance declared properties, §4).
- `FANOUT.md` — the **sealed topic**: a topic may declare closed membership at
  registration; `create_subscription`/`subscribe` on it are unrepresentable (not
  merely IAM-denied). The live-consumer topic declares it.
- `WAL.md` §3/§6 — the `capture_checkpoint` record kind + the collector capture task
  as a registered logical-log client; the writer boot-classifies (chokepoint law).
- `OBJECT_TIER.md` §1 — a `telemetry` storage class (cold interval blocks, sealed
  trace rows, cooled System partitions); its GC liveness root = **op-log-referenced
  sealed refs** (the exact parallel of QUEUE §7's partition-log-referenced bodies
  root). Without both, cold writes fail boot (OT11) and surviving blocks get swept.
- `PROTOCOL.md` §3 — `UplinkInterval` registered under the `supersession` archetype,
  class-1 carriage (§7); the boot classifier gains the kind.

**Planes**:

- `MONITORING.md` §5 — the hot-ring role reconciled: the emission ring is the
  *source buffer* (bounded, doorbell-drained); the collector's shard structures own
  Gorilla-class storage, retention, and federation (which §5's "the collector
  consumes this plane" already anticipated — the wording moves, the machinery
  doesn't fork).
- `IAM.md` §4 — the `observability` capability row: actions become
  `read_series`/`read_events`/`read_trace`/`join_work` (+ `read_health` unchanged),
  PEP = the collector query serving edge; the capture task's standing named under
  `claim_plane.subscribe_deltas`. §11 — "two streams" → two scope-classes of the one
  log.
- `SESSIONS.md` §2 — the colocation-unit service list gains the **capture task** and
  names the **detection substrate** (already placed there by MONITORING/HANDOFF but
  absent from the closed list).
- `LEDGER_CORE.md` **§1** (the `ClaimSlot`/`ClaimLifecycle` definition site — not §2)
  + `LEDGER.md` §2 — `trace_refs` in the system-written lifecycle record; plus the
  **skeleton read** (`claim lifecycle-metadata read`) named on the serving-edge read
  surface, and released-visibility confirmed in the delta vocabulary (capture's
  `is_terminal_released()` needs it observable).
- `TRACING.md` §6 — assembler cross-reference; §1 — the singular "carries the
  `trace_id`" sentence updated for the plural lifecycle-resident `trace_refs`.
- `PLATFORM.md` §7 — the Logs home points here. `GAPS.md` — Branch 39 →
  SPEC-WRITTEN (+ header count). `SCHEDULER.md`/`AUTOSCALING.md` — decision logs
  bind to the operational log.

(The MONITORING/TRACING per-subsystem span sweep stays gated on those specs'
acceptance, unchanged.)

## 17. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| CL1 | **Composition**: durable = QUEUE, hot = CACHE, delivery = FANOUT, cold = OBJECT_TIER; no second telemetry primitive (architecture test) | a parallel telemetry stack |
| CL2 | **Never on a claim path**: no ingest/roll-up/query path touches a ledger or claim hot path; backpressure cannot reach work (architecture test) | telemetry backpressuring work |
| CL3 | **One scoped log + class isolation**: scope tag mandatory; a 100K/s telemetry flood leaves never-shed p99 delivery flat (measured) | a second substrate; a flood starving a verdict |
| CL4 | **Merge exactness**: random merge trees ≡ serial oracle, byte-identical, mixed scales; scale/buckets derived from (span, α) at definition sites | silent merge error; hand-picked buckets |
| CL5 | **Cardinality backstop**: fold keeps totals exact, counted + alarmed; no silent new-series drop is representable; registry exact; HLL within bound; post-crash re-admit semantics hold (§6) | vanishing new pods; quiet attribution loss |
| CL6 | **Assembly disruption**: assembler death re-routes exactly its HRW share; partial rows seal `AssemblerLost`, incomplete, counted; window/capacity derived | global re-shuffle; fabricated completeness |
| CL7 | **Two-class consumers**: live = exactly the four, boot-bound both directions; every query crosses the IAM PEP; a query storm leaves ingest flat (measured isolation) | a fifth live consumer; an ungated read; queries degrading collection |
| CL8 | **Exactly-once metric effect**: delta redelivery/reorder fuzz ⇒ zero double-counts (per-claim log_seq watermarks); crash between derive and checkpoint replays clean | double-counted claim metrics |
| CL9 | **Join privilege-safe**: composes only per-plane caller-authorized reads; both capabilities checked; no bridge (architecture test + authz fuzz) | the join as a capability laundry |
| CL10 | **Drop honesty**: §12's taxonomy is exhaustive — CI walks every shed/loss path into exactly one category; unknown-drop fails the build | silent telemetry loss |
| CL11 | **Fan-in bounded by node count**: 10× pod growth ⇒ collector message rate bounded by nodes (with PODS T10, HEALTH H6) | telemetry self-DDoS |
| CL12 | **Laptop ≡ fleet**: `N=1` runs the identical pipeline (loopback uplink); every constant appears in §13 with formula + anchors | mode creep; magic numbers |
| CL13 | **Recovery matrix holds**: kill-fuzz each §11 row ⇒ the stated loss (counted, in-category) and the stated recovery, nothing more lost, nothing silent | undocumented loss; recovery drift |
| CL14 | **Query honesty + pruning**: every result carries `Completeness` (a partial that doesn't say so is the named failure); a query touches only index-named shards/nodes (measured fanout ≤ index resolution); an unbounded selector is a typed refusal; results stream chunked under a derived memory bound; sampled-source results marked `estimated` with `1/keep_rate` compensation | silent partials; broadcast fanout; the LIST memory blowup; unmarked estimates |
| CL15 | **Reseed correctness**: kill/re-place a region shard at any point ⇒ nodes re-ship via the ordinary uplink on the epoch bump; the shard converges to byte-identical merged state vs an oracle; queries during reseed carry the gap in `Completeness` | a reseed protocol fork; silent post-recovery holes |
| CL16 | **Windowed time is exact**: any `TimeRange` at any resolution ≡ a serial oracle over the raw stream (window merges exact; counter rates reset-aware via `restart_epoch`; no window satisfied from two tiers — §5c; late arrivals counted, never reopening a closed window) | unanswerable/ wrong range queries; double-counted windows; silent counter resets |
| CL17 | **Self-observation bounded + envelope held**: the collector's own chokepoints emit (coverage walk includes them); recursion depth is exactly one; total resource use never exceeds the derived envelope under any load (self-limits shed counted); scheduler admission accounts the collector share | an unobservable observer; recursive blowup; the collector squeezing pods (or vice versa) |
| CL18 | **Lifecycle completeness**: metric register/deregister round-trips through REGISTRY (admission follows the watch; retirement at horizons); session create/close summons and drains the capture with its partitions closed at archive-finalize; a closed session leaves zero resident collector state (scan) | orphaned series; a session leaking observability residue; out-of-registry metrics |

## 18. Test matrix (SIM)

| Test | Asserts |
|---|---|
| Flood isolation | CL3 (telemetry flood vs never-shed p99) |
| Merge differential | CL4 (random merge trees × mixed scales vs serial oracle) |
| Overflow sweep | CL5 (cap trip ⇒ exact totals, counted+alarmed; crash ⇒ re-admit semantics) |
| Assembler death fuzz | CL6 (kill at every window point; share re-route; incomplete marking) |
| Query-storm isolation | CL7 (saturating queries; ingest flat; PEP coverage walk) |
| Redelivery fuzz | CL8 (dup/reorder/crash-replay ⇒ single-count) |
| Join authz fuzz | CL9 (every capability combination; composition-only property) |
| Drop-taxonomy walk | CL10 (every loss path → exactly one §12 category) |
| Fan-in scale | CL11 (pods ×10, nodes fixed ⇒ flat) |
| Recovery kill-fuzz | CL13 (each §11 row, at every step boundary) |
| Query suite | CL14 (completeness on induced leaf timeouts/losses; fanout ≤ index resolution; unbounded-selector refusal; chunked-stream memory ratchet; keep-rate compensation vs oracle) |
| Reseed fuzz | CL15 (kill/re-place at every reseed point; converged-state differential; completeness during the gap) |
| Time differential | CL16 (random ranges × resolutions × tier boundaries × restarts vs the serial oracle; late-arrival and in-transit-window fuzz) |
| Envelope stress | CL17 (emission storms at every mix ⇒ envelope held, sheds counted; the coverage walk includes the collector's own chokepoints) |
| Lifecycle sweep | CL18 (metric register/deregister; session create→close→archive scan for residue) |
| Laptop parity | CL12 |

## 19. References (load-bearing few)

Monarch (VLDB'20 — zone autonomy, 36:1 aggregation-at-ingest, pushdown, no global
write fan-in). Gorilla (VLDB'15 — hot-in-RAM → cold tiering). Dapper/Canopy — head
keep, trace-as-one-row, out-of-band collection. OTel Collector — memory-limiter-first,
the LB→tail-sampling two-tier (its trace-affinity constraint; we take head-keep
instead). OTAP dataflow — thread-per-core shared-nothing Rust (shape receipt).
Thaler-Ravishankar HRW '98 — optimal K/N disruption (vs Karger ring / jump / Maglev,
dossier on file). OTel/Prometheus exponential histograms — perfect subsetting;
DDSketch (VLDB'19) — the relative-error family; Cormode et al. — t-digest's
unboundedness (the ban). OTel overflow attribute — disposition (b); Prometheus scrape
limits / Mimir drop-new-series — the rejected (a)/(c). Flajolet '07 — HLL 1.04/√m.
Companions: `MONITORING.md`, `TRACING.md`, `HEALTH.md`, `HANDOFF.md`, `IAM.md`,
`CACHE.md`, `QUEUE.md`, `FANOUT.md`, `WAL.md`, `OBJECT_TIER.md`, `LEDGER.md`,
`LEDGER_CORE.md`.
