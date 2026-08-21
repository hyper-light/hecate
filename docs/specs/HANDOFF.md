# SPEC: HANDOFF — detection, adjudication, and agent replacement

Status: presented for acceptance 2026-08-20. The design was ACCEPTED 2026-08-19
(GRILLING.md) conditional on folding the conduct-family arc lane (interior
boundary-pressure detection math) — folded here as §6. Companion to
`MONITORING.md` (the observability plane this consumes — telemetry, the score
service, the interior warden/sensor streams, the VMM lie-detector),
`HEALTH.md` (content-free law H8, the fresh-context probe H3, AbsenceIs),
`LEDGER_CORE.md` / `MATERIALIZER.md` (the claims graph a successor reconstructs
from), `PODS.md` (drain-at-handoff, `key_epoch`), and `AGENTS_RUNTIME.md`
(UID-chain continuity, the parked-turn resume).

The cardinal rule of this spec: **replacement, not repair.** A degrading agent
is not coaxed back on track; a fresh-context successor takes over its claims. The
harness detects the degradation deterministically, the Scribe judges it, the
Guardian adjudicates it, and the successor reconstructs from durable state.

## 1. The two handoffs

| | **Context handoff** | **Performance handoff** |
|---|---|---|
| Trigger | **Deterministic** — provider-authoritative full-context accounting crosses the derived budget | **Detected** — the detector suite (§5/§6) fires → alert → Scribe-judged → Guardian-adjudicated |
| Authority | **Scribe-unilateral** (no adjudication; it is not a fault) | Guardian (§9), on the Scribe's evidence-backed request |
| Frequency | Routine, every long task | **Rare** (the false-alarm budget δ bounds it, §5) |
| Model tier | Same model | May escalate `ModelConfig` tier |
| Meaning | The window filled; continue the same work fresh | The incumbent is not making progress or has drifted; replace it |

Both end in the same **execution** (§10): a fresh-context successor reconstructs
from the claims graph + the Scribe's handoff brief and adopts the open claims.
The difference is only the trigger and the authority.

## 2. The metric suite

Signals are tiered by cost and coverage; **producers bind at boot or boot
fails** (chokepoint-registration law — an unregistered signal producer is a
startup failure, never a silent gap):

- **Tier 1 — deterministic, 100% of traffic**: token/latency/tool-call/error
  envelopes, stop reasons, claim-outcome deltas. Zero inference.
- **Tier 2 — repetition/progress + a sampled judge set**: n-gram/edit-distance
  repetition, claim-graph forward-progress rate, a rate-sampled LLM-judge score.
- **Tier 3 — extended**: deeper semantic probes, sampled thinnest.

Vocabulary is **OTel GenAI semantic conventions** (bounded-cardinality keys
only, per `MONITORING.md` §5). **Every signal carries a variance monitor** —
a signal whose own dispersion drifts is quarantined before it can poison a
detector. The **conduct metric family** (warden security verdicts + sensor
telemetry) is a first-class tier, specified in §6.

## 3. Baselines & risk adjustment

The confounder is **task difficulty**: a hard task looks like a degrading agent
on raw signals. It is cured **in the statistic**, never with per-task hand-tuned
thresholds:

- **Fitted reference curves per `(agent-type, task-class)`**, frozen as
  **versioned, logged artifacts** (the same input-logging discipline as the score
  service — replay-identical, auditable). New pairs start from **fleet priors**.
- **Risk-adjusted control charts** (Steiner risk-adjusted CUSUM): each
  observation is weighted by its expected difficulty, so a hard step raises the
  bar it must clear rather than tripping the alarm. This is the standard cure for
  the base-rate/heterogeneity confounder (Axelsson's base-rate fallacy is the
  failure this avoids — §6).
- **FIR head-start** `S₀ = h/2` (Fast Initial Response): a fresh detector after a
  handoff seeds at half the control limit, so a successor that is *also* bad is
  caught fast rather than paying the full run-length again.

## 4. The detection substrate

Detector state lives in the **colocation-unit detection substrate** — **not pod
RAM, not Scribe memory**. It is **checkpointed and re-derivable** from the logged
signal stream (survives a Scribe respawn or a node move), and it is **distinct
from the score service** (`MONITORING.md` §6): the score service answers "how
good is this agent" (reputation, demote-only); the detection substrate answers
"is this agent degrading right now" (change detection, replacement). Different
state, different math, different consumer.

## 5. The detector suite (performance / derailment / reliability)

Each phenomenon has a **matched statistic**, and every threshold derives from a
**per-session false-alarm budget δ** via the run-length identity
`ARL₀ = T/δ` (T = session horizon), **bootstrap-calibrated** on the fitted
reference (§3). **Zero hand-picked thresholds.**

| Phenomenon | Statistic | Why this one |
|---|---|---|
| **Context rot** (slow quality decay) | residual **EWMA / CUSUM** vs the learned reference curve | small persistent mean-shift; EWMA/CUSUM are the min-ARL detectors for it |
| **Intent shift** (the agent's objective drifts) | **GLR-CUSUM** + dispersion-CUSUM, **BOCPD as onset-evidence only** | unknown post-change mean ⇒ generalized-likelihood; BOCPD dates the onset but never triggers alone (evidence, not verdict) |
| **Derailment loops** (thrash/repetition) | **Page–Hinkley / ADWIN** | abrupt-onset, windowed — catches a loop the moment its rate breaks trend |
| **Reliability decay** (error/regression rate climbs) | **DDM / EDDM + risk-adjusted CUSUM** | drift-detection on a Bernoulli error stream, difficulty-weighted |
| **Confirmation** (before any alert) | **SPRT** | one sequential test converts "a chart tripped" into "confirmed at bounded error rates" — the false-alarm gate |

The chart trips → SPRT confirms → alert emits (§7). BOCPD contributes an onset
timestamp to the alert; it is never the trigger.

## 6. The conduct family (interior boundary-pressure)

Security conduct is detected on the **same substrate but as its own family** —
because the failure mode is different (an adversary, not a confounded-difficult
task) and the base rate is far lower (Axelsson: on a rare-event stream, even a
tiny false-positive rate drowns the true positives — so this family is **rare-
event math with mandatory risk-weighting**, never a raw trip counter).

**Three streams, three matched statistics:**

| Stream | Statistic | Note |
|---|---|---|
| Warden **policy denials** (pre-effect boundary refusals) | **risk-adjusted Bernoulli CUSUM** (Reynolds & Stoumbos + Steiner weight) | each denial weighted by its severity-class prior; benign boundary-brush is real, so the risk weight is load-bearing |
| **Tripwire firings / escalations** (rare discrete events) | **time-between-events (TBE) exponential CUSUM / Poisson CUSUM** | detects a *rate increase* in rare events without waiting for a count threshold |
| Sensor **behavioral aggregates** (syscall-rate, boundary-probe intensity) | **EWMA intensity** (feeds the existing residual-EWMA machinery) | continuous intensity, Ye-style audit-intensity monitoring |

- **δ on these discrete streams** is computed via **Markov-chain / Monte-Carlo
  run-length** (the closed-form ARL identity assumes a continuous statistic; the
  discrete Bernoulli/Poisson charts need the chain).
- **Severity is a CATEGORY, separate from RATE.** Categories =
  {interior-boundary, egress, scope-violation}. **Per-category charts, category-
  specific `k`/`R`** — **never collapsed to one trip counter** (collapsing loses
  the category signal an adjudicator needs and re-introduces the base-rate
  problem).
- **The replacement line.** The warden **already denied** the action pre-effect,
  so **no damage occurred** — therefore a conduct alarm is **actor-level**: "this
  agent's pattern is no longer consistent with its role ⇒ replace / escalate,"
  *not* "an attack succeeded." Conduct detection drives handoff, not incident
  response.
- **The Guardian boundary.** A **pattern** of boundary pressure ⇒ **performance
  handoff** (replace the actor). A **single confirmed-hostile act** ⇒ **Guardian
  hard-block** — **enforcement, not detection** (pattern detectors are evadable;
  a confirmed hostile primitive is stopped at the warden, not charted). The
  "boundary-pressure" phenomenon row carries its own runbook line (§8).
- **Base rates are learned** per `(agent-type, task-class)` (`λ₀`/`p₀`) with
  Steiner weighting, **mandatory** — universal conduct thresholds are incoherent
  (a security agent probing boundaries is normal; a formatter doing so is not).

## 7. Alerts

The detector emits a **fully-enriched, deterministic** alert — **the detector
computes ALL context; no agent ever derives severity, frequency, duration, or
onset**:

```
{ phenomenon, fingerprint, status,
  severity,        // burn-rate ladder (multi-window multi-burn-rate)
  frequency, onset, duration, trajectory,
  evidence,        // content-free per HEALTH H8
  runbook_ref }
```

**Dedup / inhibit at emission**; **1:1 alert-to-incident** (an incident is the
durable object the Scribe consumes). `severity` is a **burn-rate ladder** (Google
SRE multi-window/multi-burn-rate) computed against δ — fast burn = page-now, slow
burn = annotate. `evidence` is a content-free bundle (HEALTH H8 type-walk: no
transcript, no key, no body).

## 8. Scribe-as-SRE

The Scribe consumes enriched **incidents** (never raw signals — it does not
re-derive anything the detector already computed) and decides **only which
runbook action** to take:

1. **observe / annotate** — record on the history stream, no handoff.
2. **narrate** — surface to the user/session narration.
3. **corrective consult** — a `consult_peer` to the incumbent (the in-band nudge,
   still repair-flavored — used only for low-severity progress dips).
4. **request a performance handoff** — with a content-free **evidence bundle**
   (HEALTH H8), to the Guardian.
5. **escalate to Guardian** — for the conduct family / hard-block boundary (§6).

**Runbooks are skills** (typed, registry-shipped) — the mapping from
`(phenomenon, severity)` to action is a versioned artifact, not Scribe ad-hoc
judgment. The Scribe *selects*; it does not *invent* the response verb.

## 9. Guardian adjudication

The Guardian makes an **SPRT-shaped decision** on the Scribe's request, and its
**single evidence request** is the **fresh-context probe** (HEALTH H3 — the one
sanctioned active probe):

- **Fresh succeeds where the incumbent thrashes** ⇒ the incumbent is degraded
  ⇒ **approve the handoff** (replace).
- **Fresh also fails** ⇒ the task itself is hard, not the agent ⇒ **deny the
  handoff**; the corrective instead **targets the claims** (the architect authors
  a corrective claim — re-scope/decompose — per the corrective-authority law),
  not the actor.

This is the structural cure for the difficulty confounder at the decision layer,
mirroring the risk-adjustment cure at the statistic layer (§3): the probe
*distinguishes a bad agent from a bad task* by experiment.

## 10. Execution of a handoff

Both handoff kinds converge here. The successor is a **fresh-context agent that
reconstructs from durable state** — it is never handed the predecessor's
transcript:

1. **Reconstruct** from the **claims graph + the Scribe's handoff brief at the
   apply-watermark**. Death handoffs additionally include the **drained ring
   tail** (`PODS`/`MONITORING` §3 tail-drain).
2. **Adopt** *all* the predecessor's open claims under **UID-chain continuity**
   (`AGENTS_RUNTIME` — the successor is the same logical agent, next UID link);
   each claim keeps its lifecycle state and the successor drives it to its natural
   terminal.
3. **No claim is force-closed and no status is invented at a handoff** — the
   canonical claim-status vocabulary is unchanged (`LEDGER` "one status
   vocabulary"; `IsTerminal` is defined over it directly), and **only an agent
   authors a claim's terminal** (agents own their actions). A genuinely moot claim
   is **revoked or superseded by the responsible agent** as a work decision, never
   mechanically "drained" by the harness. (Which pod embodies a logical agent
   across a handoff is **cluster state in the consensus/registry plane, never claim
   state** — the ledger carries agent work only.)
4. **Re-attach volumes** under a **bumped `key_epoch`** (`PODS` — the predecessor's
   leases fence off; no stale writer).
5. **Model tier**: context handoff = same model; performance handoff **may
   escalate `ModelConfig` tier**.
6. **Parked in-flight turn resumes**; **suppressed testament flushes prevent
   duplicate testimony** (the parked-turn-must-yield + testament-suppression
   laws — no double claim, no double answer).
7. **Detector FIR-seeds** from the checkpointed statistic (§3 — a bad successor
   is caught at `S₀ = h/2`, not a full run-length later).
8. **Predecessor trajectory archived with provenance** (auditable; feeds the
   fitted reference curves).

## 11. Laptop ≡ fleet

`N=1` runs the identical stack: the detection substrate is a task in the one
colocation unit, the Scribe rides the one primary's VM, the Guardian is the one
Guardian, the successor spawns in the same pod lifecycle. No mode, no fan-in, no
degraded path.

## 12. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| HA1 | **Two triggers, correct authority**: context = deterministic + Scribe-unilateral; performance = detected + Guardian-adjudicated. No performance handoff without an SPRT-confirmed alert | a handoff on a whim; a context handoff blocked on adjudication |
| HA2 | **Replacement, not repair**: a handoff always ends in a fresh-context successor adopting claims — the incumbent is never patched in place | in-place "fix the agent" flows that mask degradation |
| HA3 | **Zero hand-picked thresholds**: every threshold derives from δ via `ARL₀ = T/δ`, bootstrap-calibrated; the conduct-family δ uses Markov-chain run-length | a magic threshold; a mis-calibrated rare-event chart |
| HA4 | **Difficulty confounder cured twice**: risk-adjusted (Steiner) at the statistic AND the fresh-context probe at the decision — a hard task denies the handoff and targets claims | a hard task mistaken for a bad agent (and vice-versa) |
| HA5 | **Detector computes all context**: severity/frequency/onset/duration/trajectory are in the alert; no agent derives them; the Scribe selects a runbook action only | an agent inventing severity; a renderer computing an incident field |
| HA6 | **Conduct family is per-category rare-event math**: separate charts per {interior-boundary, egress, scope}, risk-weighted, never one trip counter; pattern ⇒ handoff, confirmed-hostile ⇒ Guardian hard-block | the base-rate fallacy; a collapsed counter; charting an act that should be blocked |
| HA7 | **Evidence is content-free** (HEALTH H8 type-walk on every alert/brief/bundle) | a transcript or key leaking through a handoff |
| HA8 | **Execution is adoption-clean**: all open claims adopt under the UID chain with no claim force-closed and no status invented (the claim-status vocabulary is unchanged), volumes re-attach under bumped `key_epoch`, testament flush suppressed, detector FIR-seeds | duplicate testimony; a stale writer; a lost claim; lifecycle leaking into claim status |
| HA9 | **Detector state is substrate-resident + re-derivable**, distinct from the score service; survives Scribe/node loss | detector state lost with a pod; conflating reputation with change-detection |
| HA10 | `N=1` == fleet stack (no mode) | a degraded single-node detection path |

## 13. Test matrix (SIM)

| Test | Asserts |
|---|---|
| Rot injection | HA3/HA5 (a slow-decay reference deviation ⇒ EWMA/CUSUM trip at the δ-derived ARL, fully-enriched alert) |
| Hard-task decoy | HA4 (a genuinely hard task ⇒ fresh probe also fails ⇒ handoff denied, corrective targets claims) |
| Loop fuzz | HA3 (repetition/derailment ⇒ Page–Hinkley/ADWIN onset within window) |
| Conduct rare-event | HA6 (denial/tripwire streams per category ⇒ risk-adjusted Bernoulli/Poisson CUSUM; a single confirmed-hostile primitive ⇒ Guardian hard-block, not a chart) |
| Base-rate stress | HA6 (a boundary-probing security agent vs a probing formatter ⇒ learned per-pair base rates decide, no universal threshold) |
| Handoff execution | HA2/HA8 (successor reconstructs at watermark; all open claims adopted, none force-closed; `key_epoch` bumped; no duplicate testament) |
| Death handoff | HA8 (predecessor death ⇒ ring tail drained into the brief; successor adopts) |
| Content-free CI | HA7 (H8 type-walk on alert schema, handoff brief, evidence bundle) |
| Substrate survival | HA9 (Scribe respawn / node move ⇒ detector re-derives from the logged stream, FIR-seeds) |
| Laptop parity | HA10 (`N=1` == fleet) |

## 14. References

Page 1954 (CUSUM); Roberts 1959 (EWMA); Lorden 1971 / Lai 1995 (GLR-CUSUM);
Adams & MacKay 2007 (BOCPD); Page 1957 (Page–Hinkley); Bifet & Gavaldà 2007
(ADWIN); Gama 2004 (DDM) / Baena-García 2006 (EDDM); Wald 1945 (SPRT); Steiner
2000 (risk-adjusted CUSUM); Reynolds & Stoumbos 1999/2000 (Bernoulli CUSUM);
Brook & Evans 1972 (Markov-chain ARL); Lucas & Crosier 1982 (FIR); Axelsson
1999/2000 (the base-rate fallacy in intrusion detection); Ye 2002/2003 (EWMA on
audit-event intensity); Google SRE Workbook (multi-window multi-burn-rate
alerting); OpenTelemetry GenAI semantic conventions. Companions: `MONITORING.md`,
`HEALTH.md`, `LEDGER_CORE.md`, `MATERIALIZER.md`, `PODS.md`, `AGENTS_RUNTIME.md`.
