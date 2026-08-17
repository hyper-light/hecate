# SPEC: the Forest — the common root system

Status: presented for acceptance (grilling branches 12+13+16 combined). Ratified
context: the fabric *plane* is deleted (no second emission path); its *purpose* —
harness-wide awareness and organic knowledge growth — is promoted to this
subsystem, **primary by construction**. Research on file (GRILLING.md): DBSP/Z-set
incremental derivation; ACT-R activation; FSRS stability; ACO/MMAS + Parunak
pheromone fields; HippoRAG PPR; Graphiti bi-temporal invalidation; the
context-pollution and stigmergy-lock-in counter-evidence; the Karst 2023 caution
(the mycorrhizal metaphor names topology and intent, never evidence).

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
   traces.
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

- **Trace/trail retention — ACT-R base-level activation** (power-law, the 30-year
  law): `B = ln(n/(1−d)) − d·ln(L)` (optimized-learning O(1) form; keep the k most
  recent touch timestamps exact). Start `d = 0.5` (the canonical fit); parameters
  are config, re-fit from our own event stream once it exists. Power-law, not
  exponential — exponential over-forgets old-established knowledge (the
  generative-agents baseline's documented weakness).
- **Reinforcement — FSRS-shaped, outcome-graded**: stability grows saturatingly
  (`S^(−w)` damping — established trails grow slower), most near the edge of
  forgetting, and **graded by outcome quality, never raw usage** (ACO's `Q/L`
  lesson): a validated outcome (satisfied claim, upheld challenge) deposits;
  failed/corrected outcomes deposit *negatively*; mere repetition deposits
  nothing. **MMAS clamps** `[τ_min, τ_max]` bound every trail — no trail becomes
  unquestionable, no lock-in flywheel (the stigmergy pathology, answered).
- **Ambient spread — Parunak's field equations** over the mark graph:
  `s(p,t) = E·[(1−G)·(s(p,t−1)+d(p,t)) + g(p,t)]` with neighbor inflow `g` — two
  difference equations, provably convergent to a fixed point (deposit inflow
  balances evaporation), robust to 10–100× parameter variation. Flavors =
  knowledge kinds (precedent, warning, contradiction, tooling), signed
  combination at read.
- **Query-time retrieval — Personalized PageRank** from the query's marks with
  **node-specificity weighting** (`−ln(fan)` — ACT-R's fan effect, IDF, and
  HippoRAG's specificity are the same correction, three ways): the cross-domain
  weighted search of branch 13, one convergent multi-hop diffusion instead of
  iterative retrieval (HippoRAG's measured +20 R@5-class gains and 10–30× cost
  advantage are the receipts).
- **Consolidation — sleep-time reflection**: activation-gated (accumulated
  importance since last pass, the generative-agents trigger), run in the field
  service's idle work: synthesize candidate abstractions **with mandatory
  citations to traces**, feeding promotion (§4). Uncited synthesis is
  unpromotable by construction.

## 4. Primary by construction (the claims integration)

The fabric failed as a secondary system; the field cannot be one:

1. **Validation priors ride claim creation**: the field pushes advisory snapshots
   (cluster validation patterns per scope/action-type) as event-carried inputs to
   the ledger core; composition happens at post time with `contributed_by`
   provenance. Snapshot age is a health signal.
2. **The ambient digest is a mandatory context-assembly stage** (`AGENTS_RUNTIME`
   §5): always runs, relevance-gated by field weights (decay × distance ×
   strength), hard token budget — an entry must displace nothing more relevant
   than itself (the context-pollution evidence is binding: the field's job is
   mostly to withhold).
3. **Rank inputs**: prevalence/specificity/trust are field aggregates — prevalence
   = outcome-weighted trail strength; specificity = evidence quality
   (artifact-backed vs narration-only provenance); trust = FSRS-style stability of
   the agent's outcome history per domain. Pushed as snapshots to the score
   service (`RANK.md` §4's machinery, delivered).
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
  re-derivability is the guarantee, not the boot mechanism). Derived state —
  **never in the truth plane**: no consensus, no replication; node loss costs
  recompute, zero knowledge. LLM spend is consolidation/curation only —
  idle-budgeted, Scribe-class models, scale-to-zero when idle.
- **Sessions are isolation boundaries; the session field is the only field.**
  There is no global forest tier, no ambient cross-session sync — advisories
  derive from a session's work, and osmosis across the fence is a data-leak
  channel by construction. Knowledge crosses sessions only by deliberate,
  governed paths:
  1. **Same-user continuity**: promoted advisories retire to the archive; a
     user's new session recalls **its own user's** prior knowledge via the
     Archivalist (cross-session recall / carry-forward) — pull-shaped,
     provenance-visible. Optional field-seeding at session open draws only from
     that user's own archived advisories.
  2. **Publication, not sync**: sharing beyond the user means exporting an
     advisory as a **registry artifact** — Guardian staging,
     inventory-from-content, label-scoped visibility, explicit approval. Knowledge
     crosses isolation boundaries exactly like skills and tools do: as catalog
     entries someone chose to publish and someone else chose to install. Shipped
     default patterns are this same tier, vendor-published.
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
| F7 | Decay realism: old-established advisories outlive recent-noise trails (power-law vs exponential differential test) | over-forgetting the load-bearing old truths |
| F8 | Snapshot purity: ledger-core composition and score service read only pushed snapshots; verdicts replay identically (with L12/K-series) | purity leaks |
| F9 | Curation gate: no promotion without a curator testament with citations; observe-mode provably influences nothing (structural) | self-promoting knowledge; silent early influence |
| F10 | Re-derivability: delete field state, replay streams ⇒ byte-identical field | hidden state in the soil |
| F11 | PPR retrieval: multi-hop associative queries beat embedding-only baseline on a session-corpus benchmark (ratcheted) | paying for a graph that doesn't retrieve |

## 7. Acceptance criteria

1. F1, F2, F9, F10 permanent CI gates — the field is correct, alive, governed, and
   stateless-recoverable, or it doesn't ship.
2. **The value gate**: influence stays in observe-mode until measured deltas
   (corrective rates, conflict recurrence, redundant-consult volume) justify each
   surface — digests, priors, and scores gate independently. If the soil doesn't
   move the numbers, it stays dark; the spec's success is falsifiable.
3. No emission path: grep-proof — no agent-facing verb writes to the field.
4. All dynamics parameters (d, clamps, E/G per flavor, budgets, windows) are
   config with derivations; re-fit from our own event stream is a stated milestone.
5. Ledger-scope rule holds: weights are service state; promotions/curation/
   influence are claims-grade; snapshots are inputs; freshness is health.
6. The fabric vocabulary is gone: "shared façades" replaces "fabric façades";
   `causal_trace` is ledger traversal; no subsystem named fabric exists.
