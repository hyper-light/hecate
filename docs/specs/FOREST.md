# SPEC: the Forest — the common root system

Status: presented for acceptance (grilling branches 12+13+16 combined). The
§3 retention hybrid and three-signal retrieval hybrid are PROVISIONALLY
DIRECTED (2026-08-16) — full acceptance pending reconciliation against the
complete Sylk forest design corpus (ECOLOGY.md, EMERGENT_FOREST.md,
EMERGENT_AGENCY.md — read in full 2026-08-16); the four audit corners and
exactness amendments are applied. Ratified context: the
fabric *plane* is deleted (no second emission path); its *purpose* —
harness-wide awareness and organic knowledge growth — is promoted to this
subsystem, **primary by construction**. Research on file (GRILLING.md):
DBSP/Z-set incremental derivation; the decay-model landscape report (ACT-R
honestly examined and replaced); ACO/MMAS + Parunak pheromone fields; HippoRAG
PPR; Graphiti bi-temporal invalidation; the context-pollution and
stigmergy-lock-in counter-evidence; the Karst 2023 caution (the mycorrhizal
metaphor names topology and intent, never evidence); the Sylk decay
post-mortem (15 traps → F21).

## 1. Shape

Three tiers over one per-session **field service** (deterministic hecate-rt task in
the session colocation unit):

1. **Traces** (episodic): derived, per event, from the three mandatory streams —
   ledger deltas (proof), scribe narration (weak signals), warden/health telemetry
   (reality at boundaries). **No emission path exists**: agents feed the soil by
   working. The field is a projector — a cursor consumer with RESYNC — so a dark
   field is a stuck-cursor alarm, never silence.
2. **Trails** (semantic): incrementally-maintained derived state — patterns,
   precedents, contradictions, cross-domain bridges — keyed by *marks* (scope
   entries, domains, symbols, action types) extracted deterministically from
   traces. **Mark extraction is a pure function over typed fields only**
   (amendment): ledger-delta fields, the narration envelope's structured tags,
   telemetry's closed enums. Free-text bodies are stored in traces but **never
   parsed for marks** — LLM interpretation of text is confined to §3's
   consolidation stage (agentic, citation-bound, downstream of promotion
   gates). Symbol marks arrive once the knowledge graph (Branch 22) provides
   canonical symbol identity — absent until then, never improvised. **The
   field's input clock** (amendment): the three streams merge under the
   lexicographic key `(HLC64, stream_id, stream_seq)` — deterministic order,
   deterministic tie-break; F10 permutes arrival order and demands identical
   fields.
3. **Advisories** (promoted knowledge): trails that crossed promotion and survived
   agentic curation. **Only advisories influence anything.**

## 2. The engine: a purpose-built Z-set incremental core

- Hand-rolled from DBSP's operator calculus (linear map/filter free; closed-form
  incremental join; aggregate; distinct; threshold) over the session's totally
  ordered clock — the embedded-framework option was examined and rejected with
  receipts (DD's lattice machinery solves excluded problems; the `dbsp` crate is
  platform-internal churn). A few operators, single-owner, deterministic.
- **The golden property is the correctness harness**: after any update sequence,
  incremental state ≡ batch re-evaluation (F-oracle, CI-gated).
- **Retraction is algebraic**: negative weights cascade so a contradicted trail's
  derived influence vanishes — while the knowledge layer stamps Graphiti-style
  **bi-temporal validity** (`valid from/until`, `learned/expired`) so nothing is
  lost: superseded knowledge cools into history, never deletes (the standing
  doctrine, again).
- **Derived events are weight-sign/threshold transitions** the engine emits
  natively per step — threshold-exit included. Event-driven at intake and output;
  no polling, no CEP engine.
- **No partial state** (Noria's scar): a session's field materializes fully;
  overflow is a windowing decision in the same algebra, never an upquery protocol.

## 3. Dynamics (the formulas, chosen with receipts)

Each mechanism uses the law with the strongest empirical record for its job:

- **Retention + reinforcement — the intensity × durability hybrid**
  (PROVISIONALLY DIRECTED 2026-08-16 — full acceptance pending the
  full-forest-design reconciliation (ECOLOGY/EMERGENT_FOREST/EMERGENT_AGENCY);
  replaces the ACT-R + FSRS + MMAS stack; receipts: decay-landscape
  report — ACT-R's form measured below a constant-prediction baseline on 350M
  reviews; three literatures converge on the multiscale decayed-trace object;
  DSR family = best measured bounded-state model — and the Sylk decay
  post-mortem's 15 traps):
  - **Intensity (attention)** — K exponential registers per outcome channel
    (positive; negative on its own slower ladder), one last-touch logical
    timestamp. K and the geometric rate ladder are **derived**: fastest rate
    from the observed intra-burst gap quantile, slowest from the archive
    horizon, `K = O(log range)` (Beylkin–Monzón bound). Touch:
    `trace_k ← trace_k·r_k^Δ + gain_ch·(1 − trace_k/τ_max,k)` — the saturating
    gain fuses the MMAS clamp, FSRS's `(1−R)` gating, and MCM's state-gated
    boost: bursts saturate fast scales instead of banking log-credit; τ_max is
    an invariant by construction. Read: lazy, pure, integer-tick fixed-point
    (square-and-multiply); power tail via readout weights `w_k ∝ λ_k^d`.
  - **Durability (validity)** — per-trail `(D, S, last-touch)`, FSRS-shaped:
    validated outcomes grow S saturatingly, gated by `(1−R)` (spacing-aware,
    burst-discounted); **contradiction collapses S multiplicatively** (the
    lapse branch — path-dependent validity no linear ladder can express);
    `R(t,S)` is an inverse square root (fixed-point friendly). All DSR
    parameters **re-fit from our own event stream — flashcard priors are
    starting points, never shipped constants**.
  - **The consumer map (declared, closed — F19)**: ranking = `intensity × R^γ`
    (γ fitted); digest admission = TinyLFU-style **duel** on rank-density per
    token against the current digest's weakest member (mostly-withhold as
    comparison, not absolute bar); retirement = rank-density below its derived
    floor for a derived duration (crossing time predicted — Soar's trick);
    consolidation = **S crossing its threshold**. Contradiction *mass* is the
    **curation-attention signal**: a contradicted trail gets hotter for
    curators while its influence collapses.
  - **One machine**: a single owner module (lint wall — no `exp(−`/`pow(age`
    outside it), one input clock, both halves **co-fitted** on the same
    self-supervised targets from the session's own logs (convex GLM readout
    for intensity; bounded SGD for the DSR parameters). Negative-evidence
    decay rates are flagged honestly as design-not-literature — our logs are
    the only oracle, and the observe-mode value gate requires that fit before
    any influence.
- **Ambient spread — Parunak's field equations** over the mark graph:
  `s(p,t) = E·[(1−G)·(s(p,t−1)+d(p,t)) + g(p,t)]` with neighbor inflow `g` — two
  difference equations, provably convergent to a fixed point (deposit inflow
  balances evaporation), robust to 10–100× parameter variation. Flavors =
  knowledge kinds (precedent, warning, contradiction, tooling), signed
  combination at read.
- **Query-time retrieval — the three-signal hybrid** (PROVISIONALLY DIRECTED
  2026-08-16 — full acceptance pending the full-forest-design reconciliation;
  receipt: HippoRAG — the source of our PPR numbers — is itself dense+PPR;
  PPR-alone was never what was measured):
  1. **Structural — Personalized PageRank** from the query's marks with
     **node-specificity weighting** (`−ln(fan)` — the fan effect, IDF, and
     HippoRAG's specificity are the same correction, three ways): multi-hop
     association, the signal neither of the others can produce. **Exact
     implementation**: forward push (Andersen–Chung–Lang) — touched mass
     O(1/(α·ε)) independent of graph size; personalization vector = query
     marks weighted by specificity, normalized; push order = sorted node
     keys; fixed-point Q32.32; α config (canonical 0.15 start, re-fit
     milestone); ε **derived** — the coarsest value whose score error cannot
     reorder anything near the digest floor θ.
  2. **Dense semantic** — embeddings over trail/advisory/trace text, computed
     at ingest off the turn path (pinned model+version ⇒ deterministic
     vectors; derived, re-derivable, session-local). **Exact search only —
     no ANN, ever**: the session fence bounds every corpus, so brute-force
     cosine suffices; the approximation and insertion-order machinery that
     plagued Sylk's vector stack is structurally unnecessary. This is also
     what makes Scribe narration's free text reachable at query time
     (the typed-marks determinism fix stores it but cannot key it).
  3. **Lexical** — BM25-class exact-term matching over the same session
     corpus (error strings, flags, symbol literals — where dense retrieval
     is measurably weakest), riding the document DB's index machinery
     (Branch 23).
  - **Fusion**: deterministic weighted combination, reciprocal-rank fusion
    as the untrained baseline, weights **fitted** by the standing GLM
    discipline; the §3 retention hybrid (intensity × R^γ) weights every
    candidate regardless of surfacing signal.
  - **Federation seam**: retrieval spans knowledge organs — Forest trails,
    the knowledge graph (Branch 22), documents (Branch 23) — each exposing
    `(candidate, score, provenance)` under the same fusion + decay layer.
    Session-scoped; zero network on the turn path; organ internals stay
    their branches' business.
- **Consolidation — sleep-time reflection**: triggered by accumulated
  importance (activation-weighted mass of new traces since last pass;
  threshold from the commissioning distribution, ratcheted), scheduled by the
  **paced-debt discipline (amendment — never idle-only work)**: crossing the
  derived threshold interleaves consolidation with intake at a derived
  priority; idle merely runs it sooner. Synthesizes candidate abstractions
  **with mandatory citations to traces**, feeding promotion (§4). Uncited
  synthesis is unpromotable by construction.

## 4. Primary by construction (the claims integration)

The fabric failed as a secondary system; the field cannot be one:

1. **Validation priors ride claim creation**: the field pushes advisory snapshots
   (cluster validation patterns per scope/action-type) as event-carried inputs to
   the ledger core; composition happens at post time with `contributed_by`
   provenance. Snapshot age is a health signal; pushes ride threshold-crossing
   transitions natively, with a **max-age bound derived from the health plane's
   freshness class** (amendment) — snapshot age can never silently exceed what
   consumers assume.
2. **The ambient digest is a mandatory context-assembly stage** (`AGENTS_RUNTIME`
   §5): always runs, relevance-gated by the §3 consumer map (rank-density
   duels), hard token budget — an entry must displace nothing more relevant
   than itself (the context-pollution evidence is binding: the field's job is
   mostly to withhold). Admission floor **θ derives from observe-mode score
   distributions** (amendment) — an empty digest is a common, correct outcome;
   entries admitted in deterministic order (score, node-key tie-break).
3. **Rank inputs**: prevalence/specificity/trust are field aggregates — prevalence
   = outcome-weighted trail strength; specificity = evidence quality
   (artifact-backed vs narration-only provenance); trust = FSRS-style stability of
   the agent's outcome history per domain. Pushed as **advisory** snapshots to the
   score service — the score service alone computes reputation (`MONITORING.md`
   §8); field aggregates advise, never author (amended 2026-08-22).
4. **Promotions and invalidations are claims**: the field service (system
   participant) posts curation claims; curator agents (Archivalist-anchored
   consult façades) judge contradiction/bridge/promotion; the testament is the
   knowledge event — provenance-bearing, challengeable, proof. Field-internal
   weights never touch the ledger; knowledge with *influence* is always
   ledger-grade.
5. **The reinforcement loop closes through testaments**: turns attach an
   **influence artifact** (which advisories the digest carried); the field
   consumes testament outcomes + influence artifacts, so reinforcement is
   proof-driven and auditable end to end.

**Observe-mode has an exact meaning**: the field computes everything, posts no
promotion claims — nothing composes into validations, digests, or scores until the
gate lifts, per the standing validator/score rollout discipline.

## 5. Authority

The Forest observes and influences — priors, digests, scores — and **authors
nothing, gates nothing, holds no rank domain**. Advisory-only is structural: no
code path from field state to a claim transition exists except through a curator
agent's testament.

## 5b. Running it: local and fleet (two levels)

- **Session field**: one task in the colocation unit; RAM bounded by live-work
  window + clamps; **checkpoint + replay-since as the boot/failover path** (F10
  re-derivability is the guarantee, not the boot mechanism). **Checkpoint,
  exactly** (amendment): a hecate-wire document `{operator materializations,
  three input cursors, parameter epoch, engine version}`, content-addressed,
  host-local, never replicated; **invariant: checkpoint_horizon ≥
  max(oldest_replayable across all three streams)** — cadence derived from the
  tightest retention window, violation alarms loudly (a checkpoint older than
  replayable history is quietly-unrecoverable, the RESYNC-vs-rederivation
  cliff). Failover = load newest checkpoint + replay-since; checkpoint lost
  with the host ⇒ full re-derivation — priced, zero knowledge lost. Session
  migration ships the checkpoint with the colocation move or re-derives,
  whichever the move machinery finds cheaper. Derived state — **never in the
  truth plane**: no consensus, no replication. **Agent handoff is not this
  spec's**: HEALTH owns plumbing, `MONITORING.md`/`HANDOFF.md` own detection
  (accepted 2026-08-22 — supersedes "Branch 14"); the field
  contributes nothing to handoff decisions. LLM spend is consolidation/
  curation only — paced-debt-budgeted (§3), Scribe-class models, scale-to-zero
  when idle.
- **Sessions are isolation boundaries; the session field is the only field.**
  There is no global forest tier, no ambient cross-session sync — advisories
  derive from a session's work, and osmosis across the fence is a data-leak
  channel by construction. Knowledge crosses sessions only by deliberate,
  governed paths — which are **governed scope-lifts** in the authority plane's
  sense (`IAM.md` §7b derived-data law): a knowledge item inherits the
  most-restrictive scope set of its sources, and each door below is the explicit
  up-chain lift that re-scopes it (not a cross-fence reach — that is why "the
  session field is the only field" and these doors coexist):
  1. **Same-user continuity**: promoted advisories retire to the archive; a
     user's new session recalls **its own user's** prior knowledge via the
     Archivalist (cross-session recall / carry-forward) — pull-shaped,
     provenance-visible. Optional field-seeding at session open draws only from
     that user's own archived advisories. (The lift: promotion-to-archive
     re-scopes session→user; recall is ordinary up-chain visibility within the
     user scope, never a cross-fence grant.)
  2. **Publication, not sync**: sharing beyond the user means exporting an
     advisory as a **registry artifact** — Guardian staging,
     inventory-from-content, label-scoped visibility, explicit approval. Knowledge
     crosses isolation boundaries exactly like skills and tools do: as catalog
     entries someone chose to publish and someone else chose to install. Shipped
     default patterns are this same tier, vendor-published. (The lift:
     publication re-scopes to the published scope.)
  - **Ingestion is a registered emission surface** (`IAM.md` §7b; SECRETS §3
    when written): the field's trace-ingest path is registered at boot like any
    emission chokepoint, so nothing enters the field (or the archive, or a
    published artifact) unscanned. **Every advisory/trail/trace carries
    contributor identity + authority epoch** (H3-grade provenance) beyond
    today's snapshot-level `contributed_by` — the field's prevalence/specificity/
    trust weighting consumes verified provenance, so a poisoning contributor is
    attributable and down-weightable by contributor × epoch; influence stays
    advisory (the Forest authors nothing, gates nothing).
- **Practical rules**: (1) **no network on the turn path, ever** — digests serve
  from the session-local field; imported knowledge is present because it was
  installed/recalled, never looked up mid-turn; (2) **curation cost scales with
  novelty** (content-identity dedup within the session and at publication);
  (3) forgetting is the same FSRS-stability math, retirement into the archive.
- Tests: F12 — **isolation (structural)**: no session's field state, traces, or
  advisories are reachable from another session absent explicit same-user recall
  or installed published artifacts; F12b — same-user recall round-trip: advisory
  promoted in session A (user U) retrievable and seedable in session B (user U)
  via the Archivalist path, and NOT in session C (user V); F13 — turn-path
  isolation: context assembly performs zero network calls (structural); F14 —
  novelty economics: N duplicate promotions ⇒ one curation, prevalence N.

## 6. Test matrix (failure each catches)

| # | Test | Catches |
|---|---|---|
| F1 | Golden property: incremental field ≡ batch re-evaluation after arbitrary update/retraction sequences (oracle, seed-swept) | the entire derivation engine |
| F2 | **Propagation oracle**: a pattern established by validated outcomes in pod A measurably reaches pod B's ambient digest within a derived window | a decorative root system — the falsifier |
| F3 | Retraction cascade: contradiction event ⇒ derived influence gone from next snapshots/digests; bi-temporal history intact and queryable | ghosts influencing work; lossy invalidation |
| F4 | Lock-in fuzz: adversarial repetition without validated outcomes ⇒ trails stay within clamps, digest composition unchanged | the stigmergy flywheel |
| F5 | Outcome coupling: satisfied-claim influence strengthens advisories; corrected-work influence weakens them — verified through the influence-artifact trail | reinforcement decoupled from proof |
| F6 | Digest discipline: token budget never exceeded; relevance ordering matches field weights; empty digest when nothing clears threshold | context pollution |
| F7 | Decay realism: old-established advisories outlive recent-noise trails (the register ladder's power tail vs single-exponential differential test) | over-forgetting the load-bearing old truths |
| F8 | Snapshot purity: ledger-core composition and score service read only pushed snapshots; verdicts replay identically (with L12/K-series) | purity leaks |
| F9 | Curation gate: no promotion without a curator testament with citations; observe-mode provably influences nothing (structural) | self-promoting knowledge; silent early influence |
| F10 | Re-derivability: delete field state, replay streams ⇒ byte-identical field | hidden state in the soil |
| F11 | PPR retrieval: multi-hop associative queries beat embedding-only baseline on a session-corpus benchmark (ratcheted) | paying for a graph that doesn't retrieve |
| F15 | PPR determinism + ε derivation: permuted insertion orders, cross-platform ⇒ identical rankings; score error at ε provably below any reorder near θ | nondeterministic retrieval; hand-set ε |
| F16 | Ladder fidelity: register-ladder power-tail approximation error vs exact power-law oracle within the Beylkin–Monzón bound; K derivation honored | the mixture silently failing its own guarantee |
| F17 | Order dependence: permuted outcome sequences ⇒ different S (path-dependent), identical trace ladders (order-invariant) — each side against its own oracle | the two quantities blurring into one |
| F18 | Decisive collapse: one validated contradiction on an arbitrarily-massed trail ⇒ promotability and rank below derived bars while curation-attention rises | validity-by-arithmetic-offset (the conflation Sylk shipped) |
| F19 | Consumer-map closure: no consumer reads a quantity outside the declared map; composites declared in one place (architecture test) | emergent ad-hoc mixing |
| F21 | The Sylk trap suite: every decay function a contraction (0 ≤ decay ≤ 1, non-increasing, property-fuzzed); time units in the type; clock injected; traces persisted, scores always derived; one-owner lint wall; reinforcement-wired-first integration (search→use→raised activation); degenerate-signal canary (variance/entropy alarm on any fitted target); producer-existence for every input stream field | the 15 named Sylk decay traps, each individually |

## 7. Acceptance criteria

1. F1, F2, F9, F10 permanent CI gates — the field is correct, alive, governed, and
   stateless-recoverable, or it doesn't ship.
2. **The value gate**: influence stays in observe-mode until measured deltas
   (corrective rates, conflict recurrence, redundant-consult volume) justify each
   surface — digests, priors, and scores gate independently. If the soil doesn't
   move the numbers, it stays dark; the spec's success is falsifiable.
3. No emission path: grep-proof — no agent-facing verb writes to the field.
4. All dynamics parameters (rate ladder, d, γ, DSR params, clamps, E/G per
   flavor, budgets, windows, θ) are config with derivations; **co-fitting both
   retention halves from our own event stream is the stated first milestone**
   (no benchmark exists on machine agent-knowledge streams — the fit is the
   missing experiment, and observe-mode requires it before influence).
4b. F17/F18/F19/F21 are permanent CI gates alongside AC-1's set; the retention
   module is the sole owner of decay math (lint-walled).
5. Ledger-scope rule holds: weights are service state; promotions/curation/
   influence are claims-grade; snapshots are inputs; freshness is health.
6. The fabric vocabulary is gone: "shared façades" replaces "fabric façades";
   `causal_trace` is ledger traversal; no subsystem named fabric exists.
