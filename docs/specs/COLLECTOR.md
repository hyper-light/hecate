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
AbsenceIs), `HANDOFF.md` (primary live consumer), `IAM.md` (query gate), `CACHE.md`/
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
enum OpClass { Verdict, Lifecycle, Audit,                 // never-shed, durable
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
    dims: BoundedDims,          // declared bounded dimensions ONLY (≤ D_max, derived);
    hash: u64,                  //   the H8 walk rejects any unbounded dim at CI
}

// ---- roll-up state (per admitted series) ----
struct ExpHistogram {           // §5 — full impl there
    scale: i8, zero_count: u64,
    buckets: Vec<u64>, index_offset: i32,
    count: u64, sum: f64, min: f64, max: f64,
    exemplars: RingBuf<ClaimUid, N_EX>,   // N_EX derived; latest-wins, bounded
}
enum SeriesState { Counter(u64), Gauge(f64), Histo(ExpHistogram) }

// ---- the node collector (one per node; owns every per-node shard) ----
struct NodeCollector {
    shards: Vec<CollectorShard>,       // N = derived core share; series hash-owned
    op_log: QueueProducer,             // the ONE scoped operational log (QUEUE instance)
    own_log: WalLogicalLog,            // the collector's OWN durable state: capture
                                       //   cursors + watermarks (§10) — small, node-local
    uplink: UplinkTask,                // §7 — ships interval deltas to the region tier
}
struct CollectorShard {                // single-owner: no lock exists in this struct
    registry: SeriesRegistry,          // §6 — the label→slot chokepoint
    series: Vec<SeriesState>,          // dense, indexed by SeriesIdx
    hot: CacheHandle,                  // CACHE instance: recent raw events + rows
    dirty: BitSet,                     // series touched since last uplink interval
    drops: DropCounters,               // §12 — one counter per taxonomy category
}

// ---- the region tier ----
struct RegionCollector {
    merged: Vec<CollectorShard>,       // same shard type — federation reuses the node's
    assemblers: Vec<Assembler>,        //   machinery; §8
    query: QueryService,               // §9/§10; reads merged + hot + cold, never ingest
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
               Verdict|Lifecycle|Audit ─▶ op_log.append(class=NeverShed)   // durable FIRST
               ClaimMetric             ─▶ op_log.append(class=Standard)    //   then hot
               Telemetry|Span          ─▶ hot only (durable only via §7 interval blocks)
4. REDUCE    Measure ⇒ idx = registry.admit(&key); series[idx].record(v); dirty.set(idx)
             Event   ⇒ hot.put(event_key, record)
             Span    ⇒ keep-flag? forward to assembler route : hot-only (TRACING §5)
5. DELIVER   live FANOUT: class-filtered, scope-filtered push to the bound four (§9)
```

Two orderings are load-bearing: **durable-before-hot** for never-shed classes (a
verdict is on the log before anything can observe it — a crash between 3 and 4 loses
only the hot copy, re-derived on read), and **admit-before-record** (no measurement
ever touches series state except through the §6 chokepoint).

## 4. The scoped operational log (D1)

One QUEUE instance; `OpClass` maps onto its delivery machinery:

| OpClass | QUEUE delivery | Durability | Retention | Why |
|---|---|---|---|---|
| Verdict, Lifecycle, Audit | **never-shed, reserved slots** (the PROTOCOL reserved-capacity law) | fsync-ack (environment-derived ω, WAL §5) | Session: with session → archive. System: fleet → cold | a flood must not starve a hard-block; audit is evidence |
| ClaimMetric | standard at-least-once | group-commit | derived (dashboards horizon) | derived work metrics; late shed counted |
| Telemetry, Span | **opt-in lossy** (the QUEUE lossy class, declared) | none on the item; durability via §7 sealed blocks | hot-ring retention → interval blocks → cold | pure telemetry is re-derivable signal, never proof |

- **Isolation is the class, not a substrate**: CL3's flood test — 100K/s of Telemetry
  while a Verdict lands — passes because reserved slots are capacity the sheddable
  class *cannot occupy*, enforced in the QUEUE instance, not by this spec's prose.
- **Retention executes by scope**: `Session(uid)` partitions retire when the session's
  archive seals (SESSIONS' lifecycle, not a second GC); `System` partitions cool to
  OBJECT_TIER on a derived age/size trigger as content-addressed sealed segments.

## 5. The roll-up engine (D4)

Aggregation state that must merge **exactly** across tiers. Counters/sums: integer/
float addition. Distributions: **exponential-bucket histograms** — base `2^(2^−scale)`,
bucket `i` covers `(base^i, base^(i+1)]`, relative error `α = (base−1)/(base+1)`.

**Scale derives from anchors** (definition site: the metric registry entry): given
target `α` and span `[lo, hi]`: `scale = min s : (2^(2^−s)−1)/(2^(2^−s)+1) ≤ α`;
buckets = `log2(hi/lo) × 2^scale`. Worked: α=1%, 1 ns→1 day (46.3 octaves) ⇒ scale 5 ⇒
~1,482 buckets ≈ 12 KB. (The OTel default of 160 buckets would force 17% error over
that span — bucket count is derived, never defaulted; CL4.)

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

Why not the alternatives (receipts): **t-digest is banned** — no proven error bound,
adversarially unbounded (Cormode et al.), order-dependent merge: a tiered roll-up
cannot stand on it. HDR is exact but ~311 KB at this span/precision vs ~12 KB.
Fixed-γ DDSketch has the guarantee but not cross-resolution merge; exponential
histograms are the same guarantee family *plus* perfect subsetting, and they are the
OTel/Prometheus interchange form our vocabulary already targets.

## 6. The cardinality limiter (D4b)

**Primary defense — bounded by construction**: `SeriesKey` is closed (§2); per-object
ids are H8-forced out of labels into bounded exemplars. This is Monarch's position
(950 B series, *no* cap — bounded by schema + 36:1 collection aggregation).

**Backstop — aggregate-into-overflow, loud** (per `(scope, metric)`, in the shard):

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

The uplink is an interval shipper, not a stream mirror:

- **What**: for each dirty series (the `dirty` BitSet), one `SeriesDelta` — `(SeriesKey,
  state-delta)`: counter deltas as integers; histograms **downscaled to the tier's
  derived resolution** then shipped as sparse `(index, count)` pairs; plus the interval's
  sealed **event/span block ref** (content hash) if one sealed. Never raw events upward.
- **When**: interval `T_up` derives from the uplink byte budget:
  `T_up = Σ dirty-series-bytes / uplink_budget_bytes_per_sec`, clamped by the staleness
  bound consumers declared (HEALTH freshness). Recomputed as the anchors drift.
- **Wire**: class-1 sheddable datagrams under the PROTOCOL MTU budget; a lost interval
  is *absorbed* — the next interval ships state-deltas since the last **acked**
  interval (cumulative-since-ack), so loss costs latency, never correctness; sustained
  loss trips AbsenceIs staleness on the region side (HEALTH: staleness is data).
- **At the region**: `merge_from` per series (§5 — exact), assembler routing for spans
  (§8), and the region's own shard set serves rolled-up queries. Fan-in is bounded by
  **node count** (one uplink per node, H6), never pod count.
- `N=1`: the uplink target is the node itself — the same code path with a loopback
  hop, no mode.

## 8. The trace assembler (D5)

Kept spans (TRACING §5 head decision) arrive at the region tier; routing is
**`weighted_hrw(trace_id, roster)`** — the CACHE's placement mechanism reused; HRW
re-routes exactly a dead assembler's share (provably optimal K/N), no routing table.

```rust
struct Assembler {
    slots: DetHashMap<TraceId, TraceSlot>,  // capacity = derived(throughput × W)
    window: Duration,                       // W = p99 trace duration × derived margin
    timers: TimingWheel<TraceId>,           // the CACHE's ordered wheel, reused
}
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
spec, not a subscription.

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
- **Pushdown**: `Resolution::Raw` within the hot horizon executes at the owning
  node(s); rolled-up ranges execute at the region's merged shards; a range spanning
  both fans to at most `nodes(scope)` sub-queries (bounded by node count) and merges
  via §5 (exact) — partial sub-query failures surface as typed per-tier gaps, never
  silently absent (AbsenceIs).
- **Structurally off ingest** (CL7): the `QueryService` is a separate task class with
  its own budget; no query path touches an ingest queue (architecture test) — an
  investigation storm cannot degrade the telemetry it investigates.

## 10. Claims-work capture + the join (D3+)

**Capture** — an ordinary cursor consumer of the ledger's delta stream (`LEDGER` §8;
"the log is the outbox"), one per session:

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
        }                                      // `applied` is bounded by LIVE claims
        // ONE atomic append to own_log: {cursor', applied-deltas}. Crash ⇒ replay
        // from the committed cursor; watermarks turn every reprocessed delta into
        // the `continue` above. Exactly-once effect, no 2PC, ZERO ledger writes.
        self.own_log.append_atomic(&CaptureCheckpoint {
            cursor: self.cursor.advanced(deltas), applied: self.applied_delta() })
    }
}
```

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

## 11. Failure & recovery matrix

| What dies | What is lost | Counted where | What recovers, from where |
|---|---|---|---|
| A source ring overflows | oldest unpersisted telemetry | `drops[RingOverrun]` + in-band gap records | nothing — lossy class; gaps surface in assembled traces (§8) |
| A collector shard task | hot tail since last hot write | `drops[ShardRestart]` | shard restarts; registry rebuilt from hot's live series; series re-admit |
| The node collector | hot store + registry + dirty set | `drops[NodeCollectorLoss]` | op_log (durable classes) intact; own_log replays capture cursors/watermarks (§10 ⇒ exactly-once holds across the crash); series re-admit; overflow membership may differ (§6, stated) |
| The uplink / an interval | one interval's latency | absorbed (cumulative-since-ack, §7) | next acked interval carries the delta; sustained ⇒ region AbsenceIs staleness |
| An assembler | its open windows | `SealReason::AssemblerLost` rows | HRW re-routes exactly its share; survivors seal partial rows incomplete |
| The region collector | merged hot + open windows | `drops[RegionLoss]` | node tiers unaffected (autonomy); region re-merges from next intervals; cold blocks + op_log intact |
| The QUEUE log's node | per QUEUE's own spec | — | QUEUE durability (environment-derived replication); not this spec's mechanism |

The invariant across every row: **proof-grade classes (Verdict/Lifecycle/Audit,
capture checkpoints) live on durable logs and survive; telemetry-grade loss is
bounded, counted, and visible** — never silent, never blocking work.

## 12. The drop taxonomy (closed — an uncategorized drop is a bug)

`Malformed | RingOverrun | ShardRestart | NodeCollectorLoss | RegionLoss |
UplinkShed | QueueShed(class) | CardinalityFolded | TraceEvicted | AssemblerLost |
QueryPartial(tier)` — one counter each, all scope-tagged, all queryable as ordinary
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
4. **Uplink** (§7): at `T_up`, the dirty series ship as sparse histogram deltas;
   the region `merge_from`s them — exact at the region's scale.
5. **Assembly** (§8): the trace's spans HRW-route to assembler `A3`; the window
   closes; `TraceRow{complete: true}` seals to hot.
6. **Detection** (HANDOFF): the region's Tier-1 envelope for `vfs.mount` trips its
   residual-CUSUM; the fully-enriched deterministic alert reaches the Scribe.
7. **Investigation** (§10): the Scribe runs `join_work(C47)` under its own
   capabilities: skeleton (posted 14:01, testament 14:09, `trace_refs=[T]`), trace `T`
   (the 5.8 s `vfs.mount` span), the exemplared series. Answer: *the claim was slow
   because its mount was* — one call, two planes, zero fusion.
8. **A failure variant**: had assembler `A3` died mid-window, `C47`'s row seals
   `AssemblerLost/incomplete` on a survivor; `join_work` returns the trace with its
   typed gap; the *metrics* (steps 3–4, durable + exact) still carry the 6-minute
   edge — detection never depended on the lossy trace.

## 15. Laptop degenerate

`N=1`: the node tier is the region tier (loopback uplink, same code); one assembler;
one shard set; the same formulas produce laptop numbers from laptop anchors. Zero
modes anywhere (CL12).

## 16. Amendments landing with acceptance (one coordinated sweep)

`IAM.md` §11 — "two streams" → two scope-classes of the one log. `LEDGER_CORE.md` §2 +
`LEDGER.md` §2 — `trace_refs` in the system-written lifecycle record. `PLATFORM.md` §7
— the Logs home points here. `GAPS.md` — Branch 39 → SPEC-WRITTEN (+ header count).
`TRACING.md` §6 — assembler cross-reference. `SCHEDULER.md`/`AUTOSCALING.md` —
decision logs bind to the operational log. (The MONITORING/TRACING per-subsystem span
sweep stays gated on those specs' acceptance.)

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
