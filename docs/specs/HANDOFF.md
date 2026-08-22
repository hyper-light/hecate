# SPEC: HANDOFF — detection, adjudication, and agent replacement

Status: presented for acceptance 2026-08-22 (rewritten to the COLLECTOR bar). The
DESIGN was accepted 2026-08-19 (the accepted-design statement §7 + arc lane C's
conduct math, on file in GRILLING.md), corrected in-session (the `drained`
retraction — handoff is adoption, never force-close) and integrated since (the
detection substrate is a *stage* of the collector pipeline — COLLECTOR §9,
accepted). This rewrite adds the mechanics: the detector state and its exact
updates, the δ→threshold derivation chain, the incident and execution state
machines (crash-stepped), the double-handoff race, and the worked case. Companions:
`MONITORING.md` (the plane; the authority streams; the score service),
`COLLECTOR.md` (ACCEPTED — the substrate runs as its stage; incidents are
`OpClass::Incident`), `HEALTH.md` (H8 evidence; the H3 fresh-context probe),
`LEDGER_CORE.md`/`MATERIALIZER.md` (the claims graph a successor reconstructs
from), `PODS.md` (`key_epoch`, teardown), `AGENTS_RUNTIME.md` (UID chain, the
parked-turn resume), `TRACING.md` (successor traces; `trace_refs`).

The cardinal rule: **replacement, not repair.** A degrading agent is not coaxed
back on track; a fresh-context successor takes over its claims.

## 1a. The whole machine, in plain terms

A baseball bullpen. The **scoreboard and radar gun** (the detectors) track the
starter's velocity and command with calibrated instruments — the alarm line is set
from the pitcher's *own* historical curves, adjusted for the lineup he's facing
(risk adjustment: a hard task is not a bad agent), and the club has decided in
advance how many false alarms per season it will tolerate (the false-alarm budget
δ — every threshold derives from it, none is a hunch). A single wild pitch doesn't
trigger anything (SPRT confirmation separates a blip from a trend). When the trend
confirms, the **pitching coach** (the Scribe) doesn't grab a glove — he picks one
play from a laminated card (the runbooks: observe, visit the mound, warm the
bullpen, call for the reliever). The **manager** (the Guardian) makes the call,
and his one decisive test is telling: *send the fresh arm to warm up and watch him*
(the fresh-context probe) — if the reliever also struggles against this lineup,
the problem is the lineup, not the starter, and the starter stays while the
game-plan changes (deny the handoff; correct the claims). When the call is made,
the reliever **inherits the runners** — the starter's open claims transfer
exactly as they stand, on the same box score line (the UID chain); nobody erases
baserunners to make the change of pitcher tidy (the `drained` retraction). And the
new pitcher is watched *more* closely for his first batters (FIR seeding — a bad
reliever is caught fast, not given a fresh full leash).

## 1b. Terms this document uses (reading guide)

- **Context handoff** — deterministic replacement when the context window fills;
  routine; Scribe-unilateral; same model.
- **Performance handoff** — detected-then-adjudicated replacement of a degrading
  agent; rare by budget; may escalate model tier.
- **Detector** — a per-(agent, phenomenon) statistic with a derived threshold;
  trips, then SPRT-confirms, then alerts.
- **δ (the false-alarm budget)** — alarms-per-session the operator accepts; the
  single knob every threshold derives from (`ARL₀ = T/δ`).
- **FIR seeding** — starting a fresh detector at `S₀ = h/2` so a bad successor is
  caught in half the run length.
- **Incident** — the durable, fully-enriched alert object (`OpClass::Incident`,
  never-shed); 1:1 with its alert.
- **Runbook** — a typed, registry-shipped skill mapping `(phenomenon, severity)`
  to one of five actions; the Scribe *selects*, never invents.
- **Fresh-context probe** — HEALTH H3's single sanctioned experiment: a fresh
  agent attempts the same work; incumbent-vs-fresh divergence separates
  bad-agent from bad-task.
- **Adoption** — the successor taking the predecessor's open claims under the
  same logical-agent UID chain, states untouched.

## 2. The two handoffs

| | **Context handoff** | **Performance handoff** |
|---|---|---|
| Trigger | deterministic — provider-authoritative full-context accounting crosses the derived budget | detected (§5/§6) → confirmed → judged → adjudicated |
| Authority | Scribe-unilateral (not a fault; no adjudication) | Guardian (§8), on the Scribe's evidence-backed request |
| Frequency | routine, every long task | rare — bounded by δ |
| Model | same | may escalate `ModelConfig` tier |
| Meaning | the window filled; continue fresh | the incumbent is degrading; replace it |

Both converge on §9's execution. The difference is only trigger and authority.

## 3. Data model

```rust
// ---- detector state (per (agent_uid, phenomenon); lives in the substrate) ----
struct Detector {
    phenomenon: Phenomenon,          // closed enum (§5 table)
    reference: RefCurveRef,          // versioned fitted curve artifact (per
                                     //   (agent-type, task-class); fleet prior
                                     //   until fitted) — home: §11 rider
    s: f64,                          // the running statistic (CUSUM S / EWMA z / …)
    h: f64,                          // trip threshold — DERIVED (§4), never set
    fir: bool,                       // seeded at S₀ = h/2 post-handoff
    confirm: Option<SprtState>,      // open only between trip and verdict
}
struct SprtState { llr: f64, a: f64, b: f64 }   // ln((1−β)/α), ln(β/(1−α))

// ---- the substrate (a per-session stage of the collector pipeline) ----
struct DetectionSubstrate {
    detectors: DetHashMap<(AgentUid, Phenomenon), Detector>,
    applied: LogSeq,                 // watermark over the ordered signal stream
    own_log: WalLogicalLog,          // checkpoint {applied, detector states} —
}                                    //   ONE atomic record; recovery = replay
                                     //   (the ClaimsCapture pattern, verbatim)

// ---- the incident (durable; OpClass::Incident, never-shed — COLLECTOR §4) ----
struct Incident {
    phenomenon: Phenomenon,
    fingerprint: Fingerprint,        // dedup identity: (agent_uid, phenomenon,
                                     //   onset-window) — re-trips fold, not spam
    status: IncidentStatus,          // §7's state machine
    severity: Severity,              // the burn-rate ladder (§7) — COMPUTED
    frequency: u32, onset: Hlc, duration: Duration,
    trajectory: Trend,               // worsening | stable | recovering (computed)
    evidence: EvidenceBundle,        // content-free (H8): statistic series refs,
                                     //   threshold, reference-curve version,
                                     //   exemplar claim UIDs, trace ids — refs only
    runbook: RunbookRef,             // the registry-shipped skill for this row
}
// THE DETECTOR COMPUTES EVERY FIELD. No agent ever derives severity, frequency,
// onset, duration, or trajectory — the Scribe consumes, selects, requests.

// ---- the handoff execution record (crash-stepped; §9) ----
struct HandoffExec {
    kind: HandoffKind,               // Context | Performance{tier_escalation}
    predecessor: AgentUid, successor: AgentUid,   // same chain, next link
    step: ExecStep,                  // the §9 state machine position — DURABLE
    brief: BriefRef,                 //   (a lifecycle record: crash ⇒ resume step)
}
```

## 4. Thresholds — the derivation chain (zero hand-picked numbers)

Every threshold comes from one operator-owned quantity: **δ, the per-session
false-alarm budget**.

```
δ (alarms/session, operator policy)
  → ARL₀ = T / δ            (T = session horizon in observations: the required
                             average run length between false alarms)
  → h    = solve ARL₀(h, k) (the trip threshold: for continuous statistics via
                             the standard ARL approximation; for the discrete
                             conduct streams via the Markov-chain / Monte-Carlo
                             run-length — the closed forms assume continuity)
  → bootstrap-calibrate     (resample the agent-type's own reference residuals;
                             adjust h until the empirical run length ≥ ARL₀ —
                             distributions here are not textbook-normal)
  → S₀ = h/2                (the FIR head-start after every handoff)
k (the CUSUM slack) derives from the reference curve: k = Δ/2 where Δ is the
smallest shift worth alarming on — itself derived from the handoff cost vs the
degradation cost at the measured curves, not chosen by feel.
```

**Risk adjustment** cures the difficulty confounder *in the statistic*: each
observation is weighted by its expected difficulty from the reference curve
(Steiner's risk-adjusted CUSUM) — a hard step raises the bar it must clear
instead of tripping the alarm. Reference curves are **versioned, logged
artifacts** per `(agent-type, task-class)`, frozen and replayable; new pairs
start from fleet priors. **Every signal carries a variance monitor** — a signal
whose own dispersion drifts is quarantined before it can poison a detector.

## 5. The detector suite (phenomenon → matched statistic → exact update)

| Phenomenon | Statistic | The update (per observation x) |
|---|---|---|
| **Context rot** (slow quality decay) | residual EWMA/CUSUM vs the reference | `r = x − μ_ref(t)`; `S = max(0, S + r − k)`; trip at `S ≥ h` |
| **Intent shift** (objective drifts; post-change mean unknown) | GLR-CUSUM + dispersion-CUSUM; BOCPD as onset evidence ONLY | GLR: `max over candidate shifts of the log-likelihood`; BOCPD dates the onset for the alert — it never triggers alone |
| **Derailment loops** (thrash/repetition) | Page–Hinkley / ADWIN | PH: `m = min(m, M)`, `M += x − x̄ − δ_ph`; trip at `M − m ≥ h` |
| **Reliability decay** (error rate climbs) | DDM/EDDM + risk-adjusted Bernoulli CUSUM | `S = max(0, S + W_t)` with `W_t` the Steiner risk-adjusted score of success/failure at difficulty `p_t` |
| **Confirmation** (before ANY alert) | SPRT | `llr += ln(f₁(x)/f₀(x))`; alert at `llr ≥ a`, reset at `llr ≤ b`; `a,b` from declared (α, β) |

The chart trips → SPRT opens → confirms (alert) or resets (a blip, counted).
BOCPD contributes `onset`; it is never the trigger.

**The signal tiers feeding these** (producers bind at boot or boot fails):
Tier 1 — deterministic envelopes on 100% of traffic (tokens, latency, tool
calls, stop reasons, claim-outcome deltas). Tier 2 — repetition/progress + a
rate-sampled LLM-judge score. Tier 3 — extended semantic probes, sampled
thinnest. Vocabulary = the OTel GenAI conventions, bounded-cardinality,
`HostObserved`-filtered (the substrate reads authority streams only — MONITORING
MO2, enforced by the landed provenance dimension).

## 6. The conduct family (interior boundary-pressure — rare-event math)

Same substrate, own family: the failure mode is an adversary, not a confounded
task, and the base rate is far lower (Axelsson: on rare-event streams even tiny
false-positive rates drown true positives — so this family is risk-weighted
rare-event math, never a raw trip counter).

| Stream | Statistic | Note |
|---|---|---|
| Warden policy denials (pre-effect refusals) | risk-adjusted **Bernoulli CUSUM** | each denial weighted by its severity-class prior; benign boundary-brush is real |
| Tripwire firings / escalations | **time-between-events exponential / Poisson CUSUM** | detects a rate *increase* in rare events without waiting for a count |
| Sensor behavioral aggregates (syscall-rate, probe intensity) | **EWMA intensity** | Ye-style audit-intensity monitoring |

- **Per-category charts** — {interior-boundary, egress, scope-violation} — with
  category-specific `k`/`h`; never collapsed into one counter (collapsing loses
  the category signal and re-imports the base-rate fallacy).
- **δ on these discrete streams** uses the Markov-chain run-length (§4's note).
- **The replacement line**: the warden already denied pre-effect — no damage
  occurred — so a conduct alarm is **actor-level** ("this agent's pattern no
  longer fits its role ⇒ replace/escalate"), not incident response.
- **The Guardian boundary**: a *pattern* ⇒ performance handoff; a *single
  confirmed-hostile act* ⇒ **Guardian hard-block** — enforcement, not detection
  (pattern detectors are evadable; a confirmed hostile primitive is stopped at
  the warden, not charted).
- **Base rates are learned per (agent-type, task-class)** — a security agent
  probing boundaries is normal; a formatter doing so is not. Universal conduct
  thresholds are incoherent; the per-pair curves are mandatory.

## 7. The incident lifecycle

```
DETECTED (chart trip) ──SPRT──▶ CONFIRMED ──▶ ALERTED (Incident emitted:
   │                     │                     OpClass::Incident, never-shed,
   │                     └─reset─▶ (counted    deduped by fingerprint — a re-trip
   │                        blip; no alert)    FOLDS: frequency++, trajectory
   ▼                                           recomputed — never a second incident)
JUDGED (the Scribe selects a runbook action, §8)
   ├─ observe/annotate ──▶ RESOLVED(observed)         (severity low; logged)
   ├─ narrate          ──▶ RESOLVED(narrated)
   ├─ corrective consult ─▶ WATCHING (detector keeps running; improvement ⇒
   │                        RESOLVED(recovered); else re-JUDGED at next fold)
   ├─ request handoff  ──▶ ADJUDICATING (Guardian, §8) ──approve──▶ EXECUTING (§9)
   │                                                   └──deny──▶ RESOLVED(task-hard;
   │                                                        corrective targets claims)
   └─ escalate (conduct) ─▶ ADJUDICATING (hard-block path per §6's boundary)
EXECUTING ──▶ RESOLVED(replaced)  — the detector FIR-seeds for the successor
```

**Severity is the burn-rate ladder** (multi-window, multi-burn-rate against δ):
`burn = observed alarm-budget consumption rate ÷ budgeted rate`, evaluated over a
fast and a slow window; fast-burn ⇒ page-now severities, slow-burn ⇒ annotate.
Computed by the detector, like every field.

## 8. Judgment and adjudication

**The Scribe as SRE**: consumes enriched incidents (never raw signals — it
re-derives nothing) and **selects one of the five runbook actions** — the
runbooks are typed, registry-shipped skills keyed `(phenomenon, severity)`;
selection is judgment, the menu is versioned artifact. A handoff request is a
**claim** (the Scribe's request enters the ledger like all authority — with the
content-free evidence bundle attached by reference).

**The Guardian**: an SPRT-shaped decision whose **single evidence request is the
fresh-context probe** (HEALTH H3): summon a fresh agent against the same work.

- Fresh succeeds where the incumbent thrashes ⇒ the incumbent is degraded ⇒
  **approve** (replace).
- Fresh also fails ⇒ the task is hard, not the agent ⇒ **deny**; the corrective
  targets the *claims* (the architect authors the re-scope/decompose — the
  corrective-authority law), and the incident resolves `task-hard`.

This is the difficulty confounder cured a second time, at the decision layer, by
experiment — mirroring §4's cure at the statistic layer. The probe is ungameable
by the incumbent: it does not participate in it.

## 9. Execution — adoption, crash-stepped

The `drained` retraction, restated as law: **no claim is force-closed and no
status is invented at a handoff.** The successor adopts *all* open claims under
UID-chain continuity and drives each to its natural terminal; a genuinely moot
claim is revoked/superseded by the responsible agent as a work decision, never
mechanically closed by the harness. (Which pod embodies the logical agent is
cluster state in the registry/summoning plane — never claim state.)

```
X1 SUMMON     the successor summons through the standard flow (same AgentRole,
              next UID link; Performance may escalate ModelConfig tier).
              IDEMPOTENT + SERIALIZED: the HandoffExec record is keyed by the
              predecessor UID — a second alert folding in (§7) or a concurrent
              context-trigger CANNOT start a second execution; one chain, one
              in-flight handoff (the double-handoff race, closed by the durable
              step record, not by luck)
X2 RECONSTRUCT the successor rebuilds from the claims graph at the apply
              watermark + the Scribe's brief (death handoffs include the drained
              ring tail — MONITORING §13)
X3 ADOPT      all open claims re-associate to the chain (states untouched);
              satisfaction monitors re-arm; the accumulator's suppressed
              testament flush prevents duplicate testimony at resume
X4 RE-ATTACH  volumes re-attach under a bumped key_epoch (predecessor leases
              fence off — a zombie predecessor's writes die at the resource)
X5 RESUME     the parked in-flight turn resumes from the ledger; successor
              operations root fresh traces (TRACING §5 — the claim's trace_refs
              accumulates both sides)
X6 SEED       the successor's detectors FIR-seed at S₀ = h/2 from the
              checkpointed statistics — a bad successor is caught in half a run
              length, never given a fresh full leash
X7 ARCHIVE    the predecessor's trajectory archives with provenance (feeds the
              reference curves); its pod tears down flush-gated (MONITORING §6)
crash at any step: the HandoffExec record is durable lifecycle state — the
              execution fast-forwards from `step` (each step idempotent; the
              PLATFORM §4 multi-step law). A crash between X1 and X4 leaves the
              predecessor fenced-or-fencing and the successor incomplete — the
              record's owner (the summoning flow) resumes it; no state is lost
              because every step reads/writes only durable planes.
```

## 10. Failure & recovery matrix

| What fails | Effect | Counted where | Recovery |
|---|---|---|---|
| The detection substrate | detection pauses for its session | substrate lifecycle events | checkpoint (own_log) + replay of the logged signal stream ⇒ byte-identical detectors; FIR state preserved in the checkpoint |
| The Scribe mid-incident | judgment pauses | Scribe respawn counters | the Incident is durable (never-shed lane); the respawned Scribe re-consumes it — selection is idempotent (the runbook action is recorded on the incident) |
| The Guardian unavailable | adjudication holds | escalation-queue latency (its own autoscale signal) | the request claim waits; the incumbent keeps working (a handoff deferred is degradation continued, priced and visible — never a default-approve) |
| The probe fails to launch / times out | no evidence | probe outcome counters | adjudication holds; retry through the ordinary summon flow; a probe that cannot run is itself a capacity signal |
| Handoff execution crash | none durable | ExecStep lifecycle | fast-forward from the durable step (X-machine); idempotent steps |
| Two triggers race | — | fold counters | X1's serialization: one in-flight execution per chain, the second folds |
| Reference-curve artifact missing | detection degrades to fleet priors | artifact-miss counters | priors are the declared cold-start path; the miss is visible, never silent |
| A gamed detector (Bar-A incumbent aware of thresholds) | one chart evaded | — | per-pair learned baselines + multiple phenomena + the conduct family's actor-level framing: evading one chart is not escaping the panel; and the probe (§8) is outside the incumbent's reach |

## 11. Derived constants + the flagged homes

| Constant | Formula | Anchors |
|---|---|---|
| δ | operator policy (the ONE input) | alarm-tolerance per session |
| ARL₀, h, S₀ | the §4 chain (`T/δ`; bootstrap; `h/2`) | session horizon, reference residuals |
| k per phenomenon | Δ/2; Δ from handoff-cost vs degradation-cost at the curves | measured costs |
| SPRT a, b | ln((1−β)/α), ln(β/(1−α)) | declared (α, β) per phenomenon |
| Burn windows | fast/slow from δ consumption dynamics | measured alarm dynamics |
| Judge-sample rate (Tier 2) | judge budget ÷ traffic | judge cost, traffic census |
| Probe budget | derived from the summon budget class | summon-to-ready anchors |

**Flagged homes (open riders, shared with MONITORING §18)**: the reference-curve
artifacts and the substrate checkpoint's storage class (R4-OQ-a/b — one ruling
covers both); fleet priors' cross-session home (R2-OQ-c).

## 12. Worked example — context rot, end to end (and the denied variant)

The Engineer `E7` is 3 hours into a refactor.

1. **Signals**: Tier-1 envelopes stream to session s9's substrate (its colocation
   stage): tool-call coherence and progress-rate residuals against `E7`'s
   `(engineer, refactor)` reference curve, difficulty-weighted.
2. **Drift**: over 40 observations the residual EWMA sags; the CUSUM climbs:
   `S: 0 → 2.1 → 4.7 → 7.9`. With δ = 2/session and T = 10⁴ observations,
   ARL₀ = 5,000; bootstrap on this pair's residuals put `h = 7.4` — `S ≥ h`
   trips.
3. **Confirm**: SPRT opens (α = β = 0.01 ⇒ a ≈ 4.6); eleven further observations
   push `llr` past `a`. Confirmed — not a blip.
4. **The incident**: `{phenomenon: ContextRot, severity: fast-burn (the trip
   consumed a session's budget in 20 min), onset: BOCPD's date 38 observations
   back, trajectory: worsening, evidence: statistic refs + curve version + two
   exemplar claim UIDs, runbook: RB-rot-2}` — emitted never-shed, deduped by
   fingerprint.
5. **Judged**: the Scribe (consuming the incident, not raw signals) selects
   action 4: request a performance handoff, evidence bundle attached.
6. **Adjudicated**: the Guardian launches the fresh-context probe: a fresh
   Engineer attempts the current claim. The fresh agent advances it cleanly in
   9 minutes where `E7` thrashed for 40. Approve.
7. **Executed**: X1–X7 — successor `E7'` (same chain), reconstructs at the
   watermark with the brief, adopts the four open claims untouched, volumes
   re-attach at the bumped epoch, the parked turn resumes, detectors FIR-seed at
   `h/2 = 3.7`, `E7`'s trajectory archives into the reference corpus.
8. **The denied variant**: in step 6 the fresh agent *also* thrashes — the
   refactor's dependency graph is genuinely pathological. Deny; the incident
   resolves `task-hard`; the architect authors the corrective claim
   (decompose the refactor); `E7` continues on the re-scoped work — the agent
   was never the problem, and no handoff churned it. The two cures (§4's
   statistic, §8's probe) both fired exactly as designed.

## 13. Laptop degenerate

`N=1`: the substrate is a stage in the one collector's colocation unit; the one
Guardian adjudicates; the probe summons through the one pool; identical stack,
zero modes.

## 14. Integration (every companion touchpoint)

- **MONITORING** — the authority streams (MO2) feed the substrate; the Scribe's
  judge loop and the brief/tail-drain are its §6/§13; the score service is a
  *separate* consumer (reputation ≠ change detection — different state, math,
  and consumer; both read the same ordered streams).
- **COLLECTOR** (accepted) — the substrate is its pipeline *stage*
  (stage-not-consumer); incidents are `OpClass::Incident` on the never-shed
  lane; `join_work` is the investigator's pivot from any incident's exemplars.
- **HEALTH** — H8 walks the evidence bundle; H3 is the probe's charter; variance
  monitors ride the plane.
- **LEDGER / LEDGER_CORE / MATERIALIZER** — the claims graph is the
  reconstruction source; adoption preserves the one status vocabulary; the
  apply watermark is the brief's anchor.
- **AGENTS_RUNTIME** — the UID chain; the parked-turn resume; the suppressed
  testament flush; §17's handoff-sequence amendment (joint with MONITORING).
- **PODS / SESSIONS / SCHEDULER** — summon flow, `key_epoch`, flush-gated
  teardown; the substrate's colocation home (landed).
- **TRACING** — successor traces root fresh; `trace_refs` accumulates both
  sides; incident evidence carries trace ids as refs.
- **RANK / PLATFORM** — Guardian-can-deny and the consumer-role corrections land
  in MONITORING §17's joint sweep; RANK's demote-only reputation stays disjoint
  from this spec's replacement decisions.
- **SKILLS / REGISTRY** — runbooks are ordinary typed skills, registry-shipped;
  reference curves and probes are versioned artifacts (homes: §11 riders).
- **FAULTS / SIM** — every state machine here is crash-stepped and seeded; the
  worked example is a replayable SIM scenario.

## 15. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| HA1 | **Two triggers, correct authority**: context = deterministic + Scribe-unilateral; performance = SPRT-confirmed + Guardian-adjudicated; no handoff exists without one of the two | a handoff on a whim; a blocked context handoff |
| HA2 | **Replacement, not repair**: every approved handoff ends in a fresh-context successor adopting claims; no in-place repair flow exists | masked degradation |
| HA3 | **The derivation chain**: every threshold traces δ → ARL₀ → bootstrap-h → S₀ (definition sites); conduct-family δ via Markov run-length; zero literals (audit) | a magic threshold; a mis-calibrated rare-event chart |
| HA4 | **The confounder cured twice**: risk-adjusted statistics AND the probe at the decision — the hard-task decoy (SIM) denies the handoff and targets claims | hard task read as bad agent, and vice versa |
| HA5 | **The detector computes everything**: severity/frequency/onset/duration/trajectory in the incident; the Scribe only selects; fold-on-dedup (one incident per fingerprint) | agent-derived severity; incident spam |
| HA6 | **Conduct = per-category rare-event math**: three categories, risk-weighted, never one counter; pattern ⇒ handoff, confirmed-hostile ⇒ hard-block (the boundary test) | the base-rate fallacy; charting what should be blocked |
| HA7 | **Evidence content-free**: H8 walks the bundle, the brief, the incident (CI) | a transcript in an alert |
| HA8 | **Adoption-clean execution**: all open claims adopt, none force-closed, no status invented; key_epoch bumped; testament flush suppressed; FIR-seeded (X-machine fuzz) | duplicate testimony; a stale writer; invented lifecycle |
| HA9 | **Substrate re-derivable**: checkpoint + logged-stream replay ⇒ byte-identical detectors incl. FIR state; distinct from the score service (architecture test) | detector state lost with a pod; reputation/detection conflation |
| HA10 | **Serialized execution**: the double-trigger race yields exactly one in-flight handoff per chain (durable-step keying, fuzzed) | competing successors |
| HA11 | **Crash-stepped execution**: kill at every X-step ⇒ fast-forward completes exactly once | a half-executed handoff |
| HA12 | `N=1` ≡ fleet; every §11 constant derived | modes; magic numbers |

## 16. Test matrix (SIM)

| Test | Asserts |
|---|---|
| Rot injection | HA3/HA5 (the §12 scenario as a seeded SIM: trip at the derived run length; enriched incident) |
| Hard-task decoy | HA4 (fresh probe also fails ⇒ deny ⇒ architect corrective) |
| Loop fuzz | HA3 (PH/ADWIN onset within window) |
| Conduct rare-event | HA6 (per-category charts; single confirmed-hostile ⇒ hard-block not chart) |
| Base-rate stress | HA6 (probing security agent vs probing formatter — learned pairs decide) |
| Blip storm | HA5 (trips that SPRT-reset ⇒ zero alerts, counted; fingerprint folding under re-trips) |
| Execution fuzz | HA8/HA10/HA11 (kill every X-step; double-trigger race; adoption invariants; no duplicate testament) |
| Death handoff | HA8 (predecessor death ⇒ tail-drained brief ⇒ successor adopts) |
| Substrate replay | HA9 (checkpoint/replay determinism; FIR preservation) |
| Content-free CI | HA7 |
| Laptop parity | HA12 |

## 17. References (load-bearing few)

Page 1954 (CUSUM); Roberts 1959 (EWMA); Lorden 1971 / Lai 1995 (GLR); Adams &
MacKay 2007 (BOCPD); Page 1957 (PH); Bifet & Gavaldà 2007 (ADWIN); Gama 2004 /
Baena-García 2006 (DDM/EDDM); Wald 1945 (SPRT); Steiner 2000 (risk-adjusted
CUSUM); Reynolds & Stoumbos (Bernoulli CUSUM); Brook & Evans 1972 (Markov-chain
ARL); Lucas & Crosier 1982 (FIR); Axelsson 1999 (the base-rate fallacy); Ye
2002/2003 (audit-intensity EWMA); the Google SRE workbook (multi-window
burn-rate). Companions as enumerated in §14.
