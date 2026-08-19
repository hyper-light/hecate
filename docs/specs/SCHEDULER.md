# SPEC: the scheduler — sharded deterministic spine, speculative planners

Status: presented for acceptance (grilling Branch 21-scheduler — label
disambiguated from SERVING's Branch 21 per C-6; direction ratified).
Heterogeneity amendment (§1 node classes, §5a typed vector + two-axis
repulsion, §5b epoch-frozen coefficients, §6 typed-budget coherence,
SCH16–21, AC-9/10) ACCEPTED 2026-08-18.
References: research on file (GRILLING.md) — Borg/Omega/Twine papers read directly,
Nomad evaluation-broker + C1M/C2M numbers, K8s scheduling framework/QueueingHint/
coscheduling record, Kueue/Volcano admission-gang lineage. Companions: `PODS.md`
(tiers, warden), `AUTOSCALING.md` (targets), `LEDGER.md` (summon claims),
`RUNTIME.md` (the loop's home).

## 1. Architecture

- **Shards.** The fleet's nodes partition into disjoint shard node-sets. Each shard
  runs **one deterministic decision loop** (single-owner hecate-rt task) over its
  own **totally-ordered evaluation log**. Placement in a shard is a pure function
  of that log's prefix; replay re-runs the log. Shards never share mutable state —
  cross-shard conflicts are unrepresentable, not resolved.
- **Node classes.** Every node belongs to exactly one **class** — the
  identical-machine equivalence key, declared in the registry. An unclassified
  node fails fleet join at boot (chokepoint-coverage law); heterogeneity exists
  *between* classes, never inside one. Class membership and class→purpose binding
  are versioned meta-group state (entitlement shape: rebind is an explicit logged
  event, proposed by the rebalancer or operator, never a discovered condition). A
  class rebind applies the target class's **host profile** (kernel/sysctl/storage/
  VMM settings — Twine Sidekick shape) through the Branch-32 actuator; a machine
  mid-apply carries the `rebinding` map state and takes no work. Receipts: Twine
  entitlements + host profiles (11% web-tier throughput from OS tuning;
  per-pool customization — global hugepages "would lead to unusable memory");
  Borg §5.2 (segregation costs 20–30% more machines — classes stay few,
  membership stays fluid).
- **Shard count is derived** (per-shard arrival rate and pure-function throughput
  against measured anchors); the formula yields **1 on a laptop** — the degenerate
  form, same code. Receipts: Twine shards to 1M machines/region (largest shard
  ~170K machines, 40 cores); Nomad's single applier measured 1,500–3,750
  placements/s; Borg's online pass over a 10k-machine queue &lt; 0.5s.
- **Sessions key to shards** (a session's colocation unit and pods live in one
  shard — Twine's job-fits-one-shard rule). Node↔shard assignment moves through
  the **meta consensus group** on the slow plane, proposed by the rebalancer (§8),
  never on the placement fast path.
- **Boundaries**: summon/teardown claims and their testaments live on the ledger;
  the evaluation log, plans, and versioned node state are the scheduler's own
  re-derivable service state; every decision's input vector goes to operational
  logs. The scheduler is a **system participant**: it receives summon claims and
  testifies allocations.

## 2. Intake

The shard's evaluation log is fed by, in arrival order:

1. **Summon and teardown claims** — cursor-consumed from the ledger (the scheduler
   is a projector; a stuck cursor is a health alarm). Guardian admission rides each
   summon claim as validations; the scheduler executes only claims whose admission
   validations passed.
2. **Node telemetry deltas** — capacity, health, pool state, **inventory-map
   state transitions** (`cordoned`/`draining`/`rebinding`/`commissioning` — the
   node repulsion axis), and **coefficient epochs** (§5b) (node-level, bounded
   fan-in per `PODS.md`).
3. **Planner outputs** (§3) — plans stamped with the state version they saw.
4. **Rebalancer proposals** (§8) — ordinary evaluations.

Requeue is **reason-keyed** (QueueingHint's GA design): work parks under its
rejection reason — `no_budget`, `no_colocation_slot`, `pool_empty`,
`version_conflict`, `admission_pending` — and re-enters only on events that can
clear that reason. No periodic flush-everything exists (the documented churn-storm
generator). Backoff derives from **logged timestamps**, never wall clock, so replay
holds.

## 3. Planners: deterministic optimism

Planning and committing are separated; only committing must be serial.

- **Planners are parallel speculative proposers** — free to be expensive,
  concurrent, even model-assisted. A plan = `{placements, state_version_seen,
  intent_horizon}`. Plans enter the log as inputs; **the log captures what the
  racing planners produced**, so replay determinism never requires generation
  determinism (the same discipline the ledger applies to agents).
- **Intent-aware speculation**: planners read the *declared future* — teardown
  claims, autoscaler targets, handoff triggers visible on the ledger ahead of
  execution — and may plan into capacity that is declared-but-not-yet-freed. The
  applier's in-order validation confirms or rejects when reality arrives.
  Mis-speculation costs one deterministic rejection and a replan evaluation, never
  a stall. Speculation accuracy is a first-class ratcheted metric.
- Laptop degenerate: one planner, invoked inline by the loop — same code, no
  concurrency, plans still logged.

## 4. The applier: one pure function

Per evaluation, in log order: validate the plan against current versioned node
state (**per-node version check** — Omega's sequence numbers, load-bearing) →
commit atomically or reject deterministically → emit effects (provision orders,
testament content) and the decision record. Properties:

- Rejections are pure: the same log prefix rejects the same plan identically on
  replay. Rejected plans enqueue a replan evaluation with the conflict as reason.
- Every committed plan is stamped with the state version it was validated against
  — replay divergence is detectable at the exact decision.
- Validation is µs-class (version compares + vector arithmetic); the applier is
  never the latency.

## 5. Scoring and memoization

- **Score every candidate in the shard — no sampling.** Sampling exists for 5k
  heterogeneous nodes and injects banned nondeterminism; its benefit inverts when
  feasibility is scarce (kubernetes#108606). Equivalence bounds the cost instead.
- **Content-keyed memoization**: plans memoize on `(bundle hash, constraint set,
  state-version window)` — a storm of identical replica summons computes one plan
  shape and applies it N times. Borg's equivalence classes upgraded from
  "probably identical" to provably identical; Twine's &gt;99% allocation-cache hit
  rate is the expectation to ratchet against.
- **Scoring dimensions**, each measurable: **snapshot-page locality** (a clone on
  the node holding its snapshot's CoW pages costs near-zero incremental memory —
  `PODS.md` density, now steering placement), **chunk-cache locality** (the
  session's manifests name their bytes; place pods where their chunks are),
  **budget headroom** (Borg's stranded-resource hybrid: minimize stranding, keep
  burst headroom), and colocation/spread constraints. Weights derived, with
  derivations at definition sites.

## 5a. Requirements and feasibility

- **Typed resource vector.** Every summon claim's requirements are
  `(kind, type, quantity)` entries — v1 vocabulary from the D-13 derivation
  pass: `cores`, `mem`, `storage_cap(nvme)`, `storage_write_bw(nvme)`;
  derivations live at the consumer specs' definition sites (PODS §2,
  OBJECT_TIER §5/§7, Branch 37). The discriminator is law: *consumed* (two
  pods can exhaust it) ⇒ typed vector entry, budget-checked at admission and
  fit-checked at placement — one bookkeeping system, never a label beside a
  counter (the K8s DRA lesson taken at design time; Slurm GRES shape).
  *Matched-only* (CPU generation/ISA, region, plane role) ⇒ class attribute,
  feasibility predicate only. The accelerator kind is structurally provided
  for and **unminted** — no consumer exists in the tree; minting follows a
  consumer, never precedes one. `storage_write_bw` is a dual-reader value:
  admission accounts it, OBJECT_TIER's OT13 endurance servo enforces it at
  runtime — one derivation site, two readers.
- **Feasibility is three pure predicates over logged inputs**, evaluated in
  order: **class selection** (requirement vector + class attributes name the
  candidate classes), **class repel** (registry-declared per-class `repel`
  sets — the design-intent axis; admittance derives from consumption of the
  class's protected resource, stamped by Guardian admission — never
  hand-written), **map admit** (the operational axis: the fenced inventory
  map's node state is the *only* per-node exclusion authority —
  `cordoned`/`draining`/`rebinding`/`commissioning`; operator cordon is an
  auto-disposed but epoch-bumped map proposal — the immediate escape hatch,
  with fencing, reason, and lifecycle; free-floating per-node taints are
  unrepresentable). No `NoExecute` exists on either axis: repel/state changes
  emit rebalancer proposals → §8 consent moves. Receipts: K8s duality
  doctrine + the dedicated-nodes three-part recipe; Nomad's node-pools
  concession ("constraints… do not easily prevent other jobs"); K8s
  production convergence — per-node taints are control-plane-authored from
  conditions ("the Kubernetes control plane automatically creates taints
  that match the conditions affecting the node"), cordon is the operator
  hatch ("does not affect existing Pods").

## 5b. Performance coefficients

- **Epoch-frozen performance coefficients.** The scorer carries a
  `(workload-class × node-class)` coefficient matrix as a versioned input on
  the evaluation log (same channel as telemetry deltas); decisions after an
  epoch's log position use it, replay sees the epoch it saw. **Activation is
  gated** (fit-before-influence, the FOREST AC-4 pattern): the matrix is
  identity (1.00) until the first commissioning campaign populates epoch 1
  from the ratchet harness's per-class benchmarks — `commissioning`-state
  nodes are where coefficient campaigns run. Hand-authored coefficients are
  banned (constants-from-data); the native Paragon/Quasar classifier is
  rejected on applier purity + SCH1 (receipts: 98%-vs-62% target attainment
  and 62%-vs-15% utilization are the prize; online SGD in the placement path
  is the banned form).

## 6. Admission and gangs

- **Gang at admission, never at placement.** A session's core-service unit admits
  as **one atomic transaction**: whole-unit feasibility (colocated ⇒ a single-node
  fit check — exact *because every candidate node is identical*; this exactness is
  load-bearing, and the pending heterogeneous-placement amendment must preserve it
  by scoping the fit check to a single identical-node class selected before the
  check, never by admitting per-node variance inside it — open item, GRILLING
  heterogeneous-placement exchange), reserve all or none against derived
  budgets, then place. Spreadable pods commit incrementally afterward (Omega:
  incremental default; all-or-nothing only at gang granularity). Partial
  reservations are unrepresentable — the coscheduling Permit-wait pathology class
  (timeouts, thresholds, "we cannot support group preemption") cannot occur.
- **Budgets are admission-time vector checks only** (Borg quota discipline) — the
  placement path never consults quota; a budget change takes effect at the next
  admission, never mid-placement. Budgets are checked against the **typed**
  vector (§5a); admission and placement read the same entries, so an admitted
  claim can never park `pool_empty` on a type the budget counted as fungible
  (the K8s DRA two-bookkeeping drift, structurally excluded).
- Saturation is loud: `budget_exhausted` is a counted outcome on the summon claim,
  never a silent queue.

## 7. Bands and preemption

| Band (high→low) | Content | Preemptible by |
|---|---|---|
| session-core | colocation units (ledger core, serializer, services) | nothing |
| session-pods | assigned agent pods | nothing (drain via consent, §8) |
| warm-pool | generic pre-provisioned VMs, prebuilt session skeletons | session-core, session-pods |
| best-effort | prefetch, background fills | everything above |

- **No preemption within or into the top bands** (Borg's cascade-killer). Victims
  come only from designated bands; a preemption that cannot be satisfied from them
  is a **loud admission failure**, never a "best-effort" violation (K8s
  PDB-during-preemption semantics rejected).
- Disruption limits are hard; preempted warm capacity re-enters via the
  autoscaler's replenishment, not the victim's own requeue.

## 8. Rebalancing and moves

- The **rebalancer** is an asynchronous proposer (Twine ReBalancer / descheduler
  shape): it reads drift (spread staleness, locality decay, shard imbalance) and
  emits **ordinary evaluations** into the same log — never a second placement
  authority. Node↔shard reassignment goes through the meta group.
- **Moves are kill-and-reschedule with consent** (Borg and Twine both abandoned
  live migration): before moving an assigned pod, a TaskControl-style hook asks
  the session's controlling agent to approve/sequence/delay; notice is
  best-effort by design (Borg's ~80% delivery realism) — the machinery survives
  unconsented loss via the standard claim-redelivery path.

## 9. The summon pipeline (execution of a committed plan)

Fast-forward idempotent steps, each self-checking, typed failure artifacts with
dispositions at every boundary:

```
1 claim validated (admission validations passed)      — else: reject w/ reasons
2 plan committed (§4)                                  — else: replan/park by reason
3 capacity bound (session entitlement debit)           — crash ⇒ resume at 3
4 pods provisioned via warm tiers (PODS §4)            — pool-claim validity checked
5 assignment binding (keys, volumes, identity, warden) — atomicity per PODS T12
6 health validation (boot, reachability, mounts, sensor)— fail ⇒ unwind 5..3, retry
                                                          per disposition
7 testament posted (allocation record + evidence)      — issuer evaluates
```

Unwind is the reverse fast-forward: a crash at any boundary resumes at the missing
half; no orphaned capacity survives (leak scan, SCH10).

## 9b. The request lifecycle (Guide ↔ scheduler) — ACCEPTED

The summon claim's state profile (canonical lifecycle, summon-mapped):
`generated` (composable pre-approval) → `posted` (admission validations attach) →
`received` (in the evaluation log) → `progressed*` (pipeline steps as the progress
vocabulary: `admission_validated → planned → capacity_bound → provisioning[per-pod
tier/node] → binding → health_validating`, N-of-M sub-progress) → testament
(allocation record or failure with dispositions) → issuer inspection validation →
`satisfied`.

- **Delivery classes**: progress = Observation (sheddable); resolution = Directed
  (never shed). The issuer registers its expectation at post and never parks its
  conversation on a summon.
- **Amendment = supersession with reuse** (accepted): the successor claim
  `supersedes`; content-addressed pod specs make matching allocations provably
  transferable; only the delta provisions/unwinds. In-place mutation is
  unrepresentable. Post-satisfaction changes are new summon/teardown claims.
- **Partial failure = disposition-driven auto-retry within the deadline, then
  issuer judgment** (accepted): the scheduler retries `retryable` failures through
  the tiers, testifies the final full/partial/failed state with per-pod evidence;
  **allocation sufficiency is issuer judgment** — accept-partial, remainder-claim,
  or cancel. No silent partials exist.
- **Cancel** unwinds via reverse fast-forward (SCH10 leak scan), counted outcome,
  durable artifacts. Deadlines are durable, derived from tier budgets; expiry is a
  counted timeout, never a hang.
- Tests: SCH13 amendment-reuse exactness (content-identity transfer, delta-only
  provisioning); SCH14 partial-testament completeness (per-pod evidence +
  dispositions; issuer paths exercised); SCH15 cancel/deadline accounting (unwind
  + leak scan + five-outcome completeness).

## 10. Test matrix (failure each catches)

| # | Test | Catches |
|---|---|---|
| SCH1 | Replay determinism: identical evaluation log (racing planner outputs recorded) ⇒ byte-identical placement state and decisions, across platforms and seeds | the entire spine |
| SCH2 | Gang atomicity: adversarial concurrent session admissions ⇒ zero partial-reservation states ever observable; saturation ⇒ counted `budget_exhausted` | hoarding deadlock; silent saturation |
| SCH3 | Churn storm: mass unschedulable + node churn ⇒ parking by reason, requeue only on clearing events, bounded scheduler work per event | the pre-QueueingHint burn |
| SCH4 | Preemption strictness: victims only from designated bands; infeasible ⇒ typed admission failure; hard disruption limits hold under fuzz | best-effort semantics returning |
| SCH5 | Planner races: N planners racing ⇒ log captures all outputs; applier verdicts identical on replay; version-conflict rejections deterministic | optimism breaking replay |
| SCH6 | Intent speculation: declared teardown ahead in log ⇒ plan into freed capacity validated on arrival; mis-speculation ⇒ one rejection + replan, no stall; accuracy metric emitted | speculation as a correctness risk |
| SCH7 | Locality: clone placements prefer snapshot-page nodes (measured incremental-memory delta); chunk-locality preference measured; headroom respected | locality dimensions as decoration |
| SCH8 | Memoization: identical-bundle summon storm ⇒ one plan computation, N applications; version-window keying makes staleness unrepresentable | cache staleness; storm recompute |
| SCH9 | Laptop degenerate: derived shard count = 1, inline planner; the full SCH suite passes in degenerate config unchanged | mode divergence |
| SCH10 | Pipeline unwind: crash injected at every step boundary ⇒ resume-at-missing-half or clean unwind; leak scan finds zero orphaned capacity/keys/volumes | half-summoned limbo |
| SCH11 | Consent moves: rebalancer proposals ride the log; no unconsented assigned-pod kill; unconsented-loss path recovers via claim redelivery | a second authority; migration ghosts |
| SCH12 | Admission/placement separation: no budget check exists in the placement path (architecture test); quota changes bind at next admission only | quota leaking into placement |
| SCH16 | Class-scoped exactness: gang fit on a mixed fleet is exact within each class; memoization keys include class; SCH8's storm property holds per class | heterogeneous bin-packing regressions; wrong-class cache hits |
| SCH17 | Repulsion axes: work declaring nothing never lands on a repelling class; cordon mid-gang ⇒ deterministic version-conflict rejection + replan; `commissioning` admits only benchmark-class claims; no eviction path exists (architecture test: no NoExecute analogue) | undeclared work filling protected capacity; taint sprawl; eviction sneaking in |
| SCH18 | Typed-vector coherence: admission budget and placement fit read identical typed entries; a claim admitted on type X can never park `pool_empty` on X-typed exhaustion that admission saw as free | the K8s DRA two-bookkeeping drift |
| SCH19 | Coefficient epochs: identity matrix ⇒ provably no-op vs pre-amendment scorer; epoch bump mid-log ⇒ decisions split exactly at the log position; replay epoch-pinned (SCH1 extension) | coefficients breaking determinism; silent activation |
| SCH20 | Rebind lifecycle: class rebind ⇒ `rebinding` state repels all work, profile-apply converges or unwinds via map states, node re-enters placement only after commissioning passes | half-reshaped machines taking work |
| SCH21 | Laptop degenerate (heterogeneity): one node, one class, identity coefficients; cordon on the only node ⇒ loud total refusal, counted | mode divergence; silent laptop stall |

## 11. Acceptance criteria

1. SCH1, SCH2, SCH5 permanent CI gates — deterministic, deadlock-free, optimism
   captured in the log.
2. No sampling code exists in scoring; every candidate scored, equivalence-bounded
   (architecture test).
3. The applier contains no IO, clock, RNG, or model call (runtime lint wall +
   architecture test); planners may be arbitrarily rich — their outputs are inputs.
4. All constants (shard formula, band table, backoffs, weights, budgets) derived
   with derivations at definition sites.
5. Five-outcome accounting (`served / budget_exhausted / canceled / timeout /
   error`) on every summon claim; zero uncounted outcomes.
6. Ledger-scope boundaries hold: claims/testaments on the ledger; log/plans/state
   re-derivable service state (delete + replay ⇒ identical); decisions in logs.
7. Ratcheted metrics from first baseline: placement latency p50/p99, speculation
   accuracy, locality hit rates, memoization hit rate; &gt;10% regression fails CI.
8. The degenerate config (1 shard, inline planner) is a first-class CI target
   running the entire suite.
9. The typed-vector discriminator is enforced structurally — no unaccounted
   consumable, no accounted attribute (architecture test, with SCH18).
10. Per-node exclusion has exactly one authority — architecture/grep gate: no
    repel/taint field exists outside class definitions and inventory-map
    states.
