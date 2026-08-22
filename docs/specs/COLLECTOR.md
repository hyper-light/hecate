# SPEC: COLLECTOR — the observability pipeline (ingest → roll up → store → serve)

Status: presented for acceptance 2026-08-22. Settles Branch 39 (D1–D6 worked in-session,
GRILLING.md): D1 one scope-tagged operational log (user), D2 two-class consumer model
(user), D3 query-layer ledger integration "D3+" (user), D4 exponential-bucket roll-ups +
overflow cardinality backstop (research-settled), D5 weighted-HRW trace assembly
(research-settled), D6 hecate-rt-native thread-per-core pipeline (research-settled).
Research receipts on file: Monarch/Gorilla/Scuba/Dapper/Canopy/Scribe; OTel Collector +
Vector; OTAP dataflow engine; Karger/HRW/jump/Maglev; DDSketch/t-digest/HDR/exponential
histograms; Prometheus/OTel/Mimir cardinality mechanics. Companions: `MONITORING.md`
(the emission plane), `TRACING.md` (spans + head sampling), `HEALTH.md` (content-free +
AbsenceIs), `HANDOFF.md` (the primary live consumer), `IAM.md` (the query gate),
`CACHE.md`/`QUEUE.md`/`FANOUT.md` (the substrate primitives), `OBJECT_TIER.md` (cold),
`LEDGER_CORE.md`/`LEDGER.md` (the delta stream + the one ledger-side amendment).

## 1. Role

Every chokepoint emits measurements, events, and spans (`MONITORING.md`, `TRACING.md`).
The collector is the machinery that **gathers** them (per node), **reduces** them
(roll-up, sampling-keep, cardinality bounds), **stores** them (hot in RAM, durable on
the scoped operational log, cold in the object tier), and **serves** them (live streams
to four consumers; an IAM-gated query surface for everyone else). It is never on a claim
path, never a work authority, and loses nothing silently — every drop is counted and
categorized.

## 2. Pipeline shape — composition + four new parts

The collector is **composed from the accepted primitives** — no second telemetry
substrate exists (CL1):

| Function | Instance |
|---|---|
| Durable stream | **QUEUE** over the scoped operational log (§3) — at-least-once for system-critical classes, opt-in lossy for pure telemetry |
| Hot series/state store | **CACHE** (the per-node hot ring, Gorilla-class compression, derived retention) |
| Live delivery | **FANOUT** (class-tagged streams to the live consumers) |
| Cold archive | **OBJECT_TIER** (content-addressed sealed blocks) |

The genuinely new code is exactly four parts: the **roll-up engine** (§4), the
**cardinality limiter** (§5), the **trace assembler** (§6), and the **query surface**
(§7/§8). Execution model is hecate-rt's own sharded single-owner runtime —
thread-per-core, shared-nothing, telemetry data never crossing cores on a hot path,
bounded channels everywhere (the OTAP receipt: this shape does 2.47M logs/s/core vs
121K on the row path, 14.6× on 16 cores — taken as a shape receipt, not a dependency).

## 3. The operational log (D1)

**One log.** Every durable record carries the tag `(scope, failure_domain, provenance)`:

```rust
struct OpRecord {
    scope: Scope,               // session(uid) | system(region|root) — routing,
                                // retention, and authz key: the reference IS the route
    class: OpClass,             // closed enum: verdict | lifecycle | telemetry |
                                //   span | claim_metric | audit — delivery class derives
    failure_domain: DomainRef,  // node < AZ < region (the CONSENSUS tree)
    provenance: Provenance,     // host_observed | guest_reported
    body: OpBody,               // H8-walked: numbers, durations, closed enums,
                                //   opaque ids only — never content
}
```

- **Routing/retention by scope**: `session(uid)` records live in the session's region,
  are readable under session scope, and retire/archive with the session; `system`
  records live node/region-local for the fleet lifetime, cooling to `OBJECT_TIER` on
  derived cadence. No second substrate encodes what the tag already says.
- **Isolation is a delivery-class property**: `verdict`/`lifecycle`/`audit` classes ride
  the **never-shed reserved-slot class** (the PROTOCOL reserved-capacity law) — a
  workload telemetry flood physically cannot occupy their capacity (CL3's flood test:
  100K events/s of session telemetry; warden hard-block p99 delivery flat).
  `telemetry`/`span` classes are sheddable with **counted, categorized** drops.
- `IAM.md` §11's "session stream / operational stream" language reads as the two
  scope-classes of this one log — a clarifying amendment lands with acceptance (§12).

## 4. The roll-up engine (D4)

Aggregation state that must merge **exactly** across tiers, chosen by proof:

- **Counters/sums/gauges**: plain integer/float addition — associative, commutative.
- **Latency/size distributions**: **exponential-bucket histograms** (the
  OTel/Prometheus native model). Base `2^(2^−scale)`; bucket `i` covers
  `(base^i, base^(i+1)]`; relative error `α = (base−1)/(base+1)`.
  - **Scale derives from anchors** (never hand-picked): given target error `α` and value
    span `[lo, hi]`, `scale = min s such that (2^(2^−s)−1)/(2^(2^−s)+1) ≤ α`; bucket
    count = `log2(hi/lo) × 2^scale`. Worked: α = 1%, span 1 ns → 1 day (46.3 octaves)
    ⇒ scale 5 ⇒ ~1,482 buckets ≈ 12 KB at 8-byte counts. (The OTel default of 160
    buckets would force 17% error over that span — bucket count is *derived*, CL4.)
  - **Merge = downscale-to-min(scale) + integer addition** — "perfect subsetting":
    buckets at scale s map exactly into any lesser scale, so heterogeneous-resolution
    sketches from different nodes merge with **zero added error**, in any order, over
    any tree. This is the property fixed-γ DDSketch lacks and the reason t-digest is
    **banned here**: it has no proven error bound, is adversarially unbounded (Cormode
    et al.), and its merge is order-dependent — a tiered roll-up cannot stand on it.
- **Multi-resolution retention**: raw resolution at the node; each federation hop up the
  failure-domain tree may downscale (derived resolutions per tier); the merge stays
  exact at every hop.

## 5. The cardinality limiter (D4b)

- **Primary defense — bounded by construction**: the label tuple is closed —
  `(principal-UID, op-enum, failure-domain)` plus declared bounded dimensions; every
  per-object id (chunk hash, key, request id) is H8-forced out of the label set and
  rides only as a bounded **exemplar** (latest N per series, N derived). This is the
  Monarch position: 950 B series with *no* cap, bounded by schema + aggregation.
- **Backstop — aggregate-into-overflow, loud**: per `(scope, metric)`, an **exact
  admitted-series registry** at the ingest chokepoint (the enforcement needs exact
  membership; a sketch cannot say *which* series is new). Cap = derived from the tier's
  memory budget ÷ per-series cost. On exceed: the excess series' measurements **fold
  into one overflow series** (`overflow=true`) — totals stay exactly correct,
  attribution degrades — and the fold is **counted and alarmed as a health signal**
  (nothing silent). The alternatives are rejected by doctrine: drop-new-series makes
  new pods silently vanish (loud-failure violation); atomic whole-batch reject destroys
  good data with bad.
- **Detector — HyperLogLog per scope** (~12 KB at <1% error): cheap fleet-wide distinct
  tracking feeding capacity planning and the alarm *before* the cap trips.

## 6. The trace assembler (D5)

- Kept spans (`TRACING.md` §5 head decision) route to a regional assembler by
  **weighted HRW hash over `trace_id`** against the fenced assembler roster — the
  **same placement mechanism the CACHE already uses**, reused (one mechanism, no new
  machinery). HRW's disruption is provably optimal: an assembler's death re-routes
  exactly its own share of traces (K/N) and nothing else; no routing table exists.
- Assembly window derives from measured p99 trace duration; capacity from throughput ×
  window. A trace is stored as **one row keyed by `trace_id`** (the Dapper shape): hot
  first, sealed to `OBJECT_TIER` on retention cadence. A trace with counted span-loss
  is **marked incomplete, never silently whole** (TR8 carried through). In-flight
  windows on a dead assembler are lost-and-counted — lossy-tolerant by class, never on
  a work path.

## 7. The consumer surface (D2) — two classes, mechanically

**Live class — the closed four, on/near the stream.** Scribe (handoff judgment,
scope-filtered to *its primary only*), the score service (the ordered outcome stream),
the Guardian (conduct/resource), the Guide (orchestration visibility). Mechanics: a
FANOUT instance delivers class-tagged streams; each consumer **binds at boot or boot
fails** (the chokepoint-registration law — the consumer set is closed structurally, not
by convention); live delivery rides reserved capacity. **No fifth live consumer exists**;
adding one is a spec change here, not a subscription.

**Query class — the stored plane, off the ingest path.** One gated API:

```rust
trait ObservabilityQuery {
    /// Rolled-up series: selector over the closed label vocabulary; resolution
    /// picks the tier (pushdown — the query evaluates at the lowest tier holding
    /// the data, node for recent-raw, region for rolled-up; Monarch's shape).
    fn read_series(&self, scope: Scope, sel: LabelSelector, range: TimeRange,
                   res: Resolution) -> Result<SeriesSet>;
    /// Durable events by class, cursor-paged from the scoped log.
    fn read_events(&self, scope: Scope, class: OpClass, range: TimeRange,
                   cursor: Option<Cursor>) -> Result<EventPage>;
    /// One assembled trace (marked complete|incomplete).
    fn read_trace(&self, trace_id: TraceId) -> Result<AssembledTrace>;
    /// The D3+ join — §8.
    fn join_work(&self, claim: ClaimUid) -> Result<WorkExecutionView>;
}
```

- **Every call crosses the IAM `observability` capability at the serving edge** (the
  PEP): Scribe → its primary's scope only; Guardian broad; the user per SafetyPolicy;
  the Archivalist per its grant (its wiring lands in the agents' spec — the collector
  exposes the surface, each consumer's contract lives with the consumer).
- **Structurally off the ingest path** (CL7): query execution is a separate task class
  with its own budget; no query code path touches an ingest queue (architecture test),
  so an investigation storm cannot degrade the telemetry it is investigating.

## 8. Claims-work capture + the join (D3+) — integration at the query layer

**Capture — the collector is an ordinary cursor consumer of the ledger delta stream**
(the `LEDGER.md` §8 mechanism; "the log is the outbox"). Mechanics:

- One cursor per session's delta stream, durable in the **collector's own state**
  (never the ledger); watermark semantics; resume-from-cursor on restart.
- Delta delivery is at-least-once; metric effect is **exactly-once** via transition
  identity: each derived update is keyed `(claim_uid, lifecycle_transition)` and
  deduped over a window derived from the redelivery horizon — a redelivered delta
  cannot double-count (CL8).
- **The derived metric family** (all content-free; claim UID as bounded exemplar):
  `claim_posted_total`, `claim_transition_duration{edge}` (exp-histogram per lifecycle
  edge), `time_to_testament`, `validation_outcomes{result}`, `park/resume_total`,
  `claim_coherence` (activity-vs-assignment, the HEALTH §1 signal). The ledger is
  observed; it is never written, sampled into, or mirrored as content.

**The one ledger-side amendment**: the runtime stamps **`trace_refs`** — the trace ids
of the operations that serviced a claim — into the **system-written** portion of the
claim's lifecycle record (beside timestamps/status in `ClaimLifecycle`; bounded array,
runtime-authored like every lifecycle field, never agent content). The dispatch-side
link (`TRACING.md` §1) already exists; this completes the reference **both ways** at
first class. Lands with acceptance (§12).

**The join — `join_work(claim_uid)`**, executed entirely in the query layer:

1. Read the claim's **skeleton** from the ledger's own authorized read surface —
   lifecycle timestamps, status history, `trace_refs`. (Ledger-read capability.)
2. Read the operational plane for those `trace_refs` (assembled traces) and the
   UID-exemplared series. (Observability capability.)
3. Compose `WorkExecutionView { lifecycle_timeline, per_edge_durations,
   traces: Vec<AssembledTrace>, series: SeriesSet }`.

**Privilege-safe by construction (CL9)**: the join composes only what the caller could
read from each plane separately — **both** capabilities are checked, per plane; the
observability capability alone never reads ledger content through the join, and
vice-versa. No capability bridge exists (architecture test + authz fuzz). Neither store
holds the other's data — integration at the query layer, separation at the storage
layer. Worked example: "claim 47 was slow" → `join_work(47)` → posted 14:01, testament
14:09; `per_edge_durations` shows 6 min in `progressed`; `traces[0]` shows the VFS
mount span at 5.8 min → the answer, one call, two planes, zero fusion.

## 9. Tiering & federation

Node-local first: ingest, roll-up, and recent-raw serving at the node; **federate up
the failure-domain tree (node → region) only where an upper tier exists**; fan-in is
bounded by **node count, never pod count** (HEALTH H6); cross-node liveness rides the
existing gossip piggyback. Trace assembly and rolled-up regional serving live at the
region tier. Nothing global is on any write path — the global tier (sibyl branch) is
query federation only, deferred.

## 10. Overload

Refuse-first, never OOM: a derived memory bound refuses upstream (counted) before
exhaustion; sheddable classes shed **counted by category** (the drop taxonomy is
closed — an uncategorized drop is a bug); never-shed classes hold reserved capacity;
backpressure never reaches a claim path (CL2). The QUEUE instance's environment-derived
durability applies — laptop and fleet differ by derivation, never by mode.

## 11. Laptop degenerate

`N=1`: the node tier is the region tier; the assembler, registry, and query surface run
in the one collector; the same derivations produce laptop numbers from laptop anchors.
Zero modes.

## 12. Amendments landing with acceptance (one coordinated sweep)

`IAM.md` §11 — "two streams" → two scope-classes of the one log. `LEDGER_CORE.md` §2 +
`LEDGER.md` §2 — `trace_refs` in the system-written lifecycle record. `PLATFORM.md` §7 —
the Logs home points here. `GAPS.md` — Branch 39 → SPEC-WRITTEN (+ header count).
`TRACING.md` §6 — assembler cross-reference. `SCHEDULER.md`/`AUTOSCALING.md` —
operational-log binding for their decision logs. (The MONITORING/TRACING per-subsystem
span sweep remains gated on those specs' acceptance, unchanged.)

## 13. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| CL1 | **Composition**: durable = QUEUE, hot = CACHE, delivery = FANOUT, cold = OBJECT_TIER; no second telemetry primitive (architecture test) | a parallel telemetry stack |
| CL2 | **Never on a claim path**: no ingest/roll-up/query path touches a ledger or claim hot path; backpressure cannot reach work (architecture test) | telemetry backpressuring work |
| CL3 | **One scoped log + class isolation**: scope tag mandatory; a 100K/s workload flood leaves never-shed class p99 delivery flat (measured) | a second substrate; flood starving a verdict |
| CL4 | **Merge exactness**: tier-order-free, downscale+add histogram merges byte-identical vs a serial oracle; scale/bucket counts derived from (span, α) anchors at definition sites | silent merge error; hand-picked buckets |
| CL5 | **Cardinality backstop**: overflow fold keeps totals exact; the fold is counted + alarmed; no silent new-series drop exists; the admitted-set registry is exact; HLL within its error bound | vanishing new pods; quiet attribution loss |
| CL6 | **Assembly disruption**: an assembler's death re-routes exactly its HRW share; incomplete traces marked; window/capacity derived | global re-shuffle; fabricated completeness |
| CL7 | **Two-class consumers**: live = the closed four, boot-bound; every query crosses the IAM PEP; a query storm leaves ingest throughput flat (measured isolation) | a fifth live consumer; an ungated read; queries degrading collection |
| CL8 | **Exactly-once metric effect**: delta redelivery fuzz ⇒ zero double-counts (transition-id dedup); cursor crash/resume replays clean | double-counted claim metrics |
| CL9 | **Join privilege-safe**: `join_work` composes only per-plane-authorized reads; both capabilities checked; no bridge (architecture test + authz fuzz) | the join as a capability laundry |
| CL10 | **Drop honesty**: the drop taxonomy is closed and exhaustive; every drop counted by category; unknown-drop = bug | silent telemetry loss |
| CL11 | **Fan-in bounded by node count**: 10× pod growth leaves collector message rate bounded by nodes (with PODS T10) | telemetry self-DDoS |
| CL12 | **Laptop ≡ fleet**: `N=1` runs the identical pipeline; every constant derived from a physical anchor | mode creep; magic numbers |

## 14. Test matrix (SIM)

| Test | Asserts |
|---|---|
| Flood isolation | CL3 (workload flood vs never-shed p99) |
| Merge differential | CL4 (random merge trees vs serial oracle, mixed scales) |
| Overflow sweep | CL5 (cap trip ⇒ exact totals, counted+alarmed fold; registry exactness) |
| Assembler death fuzz | CL6 (kill at every window point; HRW share re-route; incomplete marking) |
| Query-storm isolation | CL7 (saturating queries; ingest flat; PEP coverage walk) |
| Redelivery fuzz | CL8 (delta duplication/reorder ⇒ single-count; cursor crash/resume) |
| Join authz fuzz | CL9 (every capability combination; composition-only property) |
| Drop taxonomy sweep | CL10 (every shed path lands in a category; unknown = fail) |
| Fan-in scale | CL11 (pods ×10, nodes fixed ⇒ flat) |
| Laptop parity | CL12 |

## 15. References

Monarch (VLDB'20: zone-autonomous, 36:1 collection aggregation, pushdown, no global
write fan-in); Gorilla (VLDB'15: hot-in-RAM 26 h → cold, 1.37 B/point); Scuba/Scribe
(the buffered decoupler, 2.5 TB/s in); Dapper/Canopy (head sampling, trace-as-one-row,
out-of-band); OTel Collector (memory-limiter-first, loadbalancing→tailsampling tiers) +
Vector (backpressure-default channels); OTAP dataflow (thread-per-core shared-nothing
Rust, 20×/core — shape receipt); Karger '97 / Thaler-Ravishankar HRW '98 (optimal K/N
disruption) / Lamping-Veach jump / Maglev NSDI'16; DDSketch (VLDB'19) / Cormode et al.
(t-digest unboundedness) / OTel-Prometheus exponential histograms (perfect subsetting);
Prometheus scrape limits / OTel overflow attribute / Mimir-VM drop-new-series (rejected)
/ HLL (Flajolet '07, 1.04/√m). Companions: `MONITORING.md`, `TRACING.md`, `HEALTH.md`,
`HANDOFF.md`, `IAM.md`, `CACHE.md`, `QUEUE.md`, `FANOUT.md`, `OBJECT_TIER.md`,
`LEDGER.md`, `LEDGER_CORE.md`.
