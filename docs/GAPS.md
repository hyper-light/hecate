# The Gap Ledger — Branch 29 (authoritative, kept current)

Status: first full pass executed 2026-08-17 (direct read of every file in the
repo: CONTEXT.md, README.md, 5 architecture docs, 5 ADRs, 20 specs, GRILLING.md
complete). Rubric per the branch charter: research on file? spec exists? test
matrix? acceptance criteria? laptop degenerate stated? open decisions named?
Classification: `undesigned | designed-unspecced | specced-untested |
decision-open | drift (owed-and-forgotten)`. **A stale gap ledger is itself a
gap**: every branch acceptance, spec verdict, or tripwire firing updates this
file in the same change.

## 0. The one global fact

**No code exists.** The repo is docs-only (zero Cargo.toml, zero .rs). Every
spec below — including the nine ACCEPTED ones — is therefore
**specced-untested**: every "permanent CI gate" is an obligation, not a fact.
The walking skeleton has not started. This is the known, accepted state
("first light is far behind the wheel count"), recorded here so the ledger's
other classes are read against it.

## 1. Component inventory

| Spec | Status (header) | Tests | AC | Laptop degenerate |
|---|---|---|---|---|
| RUNTIME.md | presented (Br 1) | T1–T8 | 7 | implicit (shard formula) |
| WAL.md | presented (Br 2) | W1–W8 | 7 | implicit (1-replica group) |
| PROTOCOL.md | presented (Br 3) | P1–P13 | 9 | not stated |
| MERGE.md | presented (Br 4) | M1–M12 | 9 | not stated |
| VFS.md | presented (Br 5) | V1–V11 | 8 | not stated |
| PODS.md | presented (Br 6) | T1–T19 | 13 | yes (formula-derived) |
| AGENTS_RUNTIME.md | presented (Br 7) | R1–R11 | 6 | not stated |
| RANK.md | presented (Exch 8) | K1–K8 | 5 | not stated |
| SCHEDULER.md | presented (§9b accepted inline) | SCH1–15 | 8 | yes (shard=1, SCH9) |
| FOREST.md | presented + PROVISIONALLY DIRECTED ×2 | F1–F21 (no F20) | 6+4b | §5b "local", not named laptop |
| SERVING.md | ACCEPTED 2026-08-16 | FS1–FS15 | 10 | yes (§6, AC-9) |
| SESSIONS.md | ACCEPTED 2026-08-16 | SES1–SES13 | 8 | yes (§9, SES11) |
| LEDGER_CORE.md | ACCEPTED 2026-08-16 | L1–L15 | 6+1b | n/a (WAL owns) |
| AUTOSCALING.md | ACCEPTED 2026-08-16 | A1–A11 | 5+1b | yes (AC-5) |
| REGISTRY.md | ACCEPTED 2026-08-16 | G1–G14 | prose | yes (§4, §5b) |
| SKILLS_API.md | ACCEPTED 2026-08-16 | S1–S9 | prose | not stated |
| HEALTH.md | ACCEPTED 2026-08-16 | H1–H8 | prose | not stated |
| SIBYL.md | ACCEPTED 2026-08-16 | WV1–WV10 | 6 | scale-to-zero only |
| OBJECT_TIER.md | presented (Br 24) | OT1–OT15 | 8 | yes (§10, OT15) |
| VECTOR_INDEX.md | accepted-in-session 2026-08-17 (see D-9) | VX1–VX12 | 6 | yes (§6, VX12) |

Architecture set (AGENTS/LEDGER/PLATFORM/SKILLS/SUMMONING + CONTEXT + ADRs
0001–0005): law-level, no test matrices by design.

## 2. Decision-open (blocking decisions, named owners)

- **D-1 Consensus (Branch 20) — the widest dependency in the tree.**
  Direction **RATIFIED 2026-08-17** after the user's etcd challenge was
  answered by the layer-classification dossier (every challenged failure
  mode traced to etcd-server/boltdb/watch, etcd-raft-library, or
  single-group-topology; the library record short and enumerable; Meta-scale
  practice table). Ratified form = the five decisions + four amendments:
  (2a) "CRDB-lineage dialect" exemplar naming, (2b) bug-record-as-
  conformance-suite, (3-addendum) explicit conf-change activation semantics
  + #12359 countermeasures, (5a) deterministic whole-cluster simulation
  gate. **CLOSED 2026-08-17**: `CONSENSUS.md` + `FAULTS.md` accepted and
  written with three in-exchange delta sets (split-brain assembly + the
  fabric-is-liveness-only law; actor-architecture position; cross-region —
  failure-domain tree, meta tree, epoch-scoping law, async content-only
  cross-region durability, FlexiRaft rejected for the meta plane).
  **Rider closed 2026-08-17**: the cross-region verification dossier landed
  (A–E confirmed on primary text; F+G corrected), §7 was reopened per the
  rider and re-settled with the accepted six-amendment set (FlexiRaft
  two-branch rewrite, lease-shadow law, externalization-fencing law, region
  rejoin protocol, async-pole honesty, receipts strengthening; CN15/CN16 +
  F7a–d). Branch 27 narrows to the §6 writer-roster audit at build time. Consumed by: WAL §5 (the only commit
  path "at every replica count"), SERVING §6 inventory map, SCHEDULER §1 meta
  group, REGISTRY §5 replicated revision (which dangles a reference to the
  nonexistent `CONSENSUS.md`), OBJECT_TIER §4 placement map, LEDGER_CORE §2
  append API. Branch 27 (leader-election revisit) deliberately re-derives part
  of its scope — settle together.
- **D-2 `WIRE_FORMAT.md` — CLOSED 2026-08-17.** `WIRE_FORMAT.md` +
  `TRANSFER.md` accepted and written ("accepted for the sake of output");
  PROTOCOL §6's process gate is satisfied, PROTOCOL §4 carries the
  flow-control amendments, OBJECT_TIER §2 gains the staging pack role.
  Branch 26 (multi-modal media) narrows to content **policy** only:
  class-assignment, content-type verification, EXIF hygiene, parser
  sandboxing, the per-class chunk-policy table, media descriptor documents —
  it inherits a settled transport.
- **D-3 Encryption × dedup — CLOSED 2026-08-17** ("approved."): OBJECT_TIER
  §9 settled — scope-salted convergent encryption validated against the
  full attack literature, four hardenings as law (256-bit random salt +
  BLAKE3 keyed mode; write-closed global domain + possession-proof IDs;
  chunk-size hygiene w/ the eprint 2025/558 caveat; crypto-erase hierarchy
  killing derivability), RCE split recorded as tripwire option, DupLESS +
  no-dedup rejected with receipts, OT16–OT19 added, AC-6 lifted (gate now
  practical: hardenings implemented + tests green). Branch 25 inherits the
  wrap structure; Branch 28 sits above, untouched.
- **D-4 FOREST whole-spec verdict.** Retention + retrieval hybrids
  PROVISIONALLY DIRECTED; full acceptance gated on reconciliation against
  ECOLOGY/EMERGENT_FOREST/EMERGENT_AGENCY — **files that live in the Sylk
  repo, not this one** (import or pin them, or the gate is unauditable here).
- **D-5 Branch 14 (handoff detection math).** HEALTH.md carves out context-fit
  accounting + threshold derivation for it by name; AGENTS_RUNTIME triggers
  and the Scribe's central duty rest on it. Research LANDED ×2 (GRILLING
  reports section: Sylk post-mortem — 0 performance handoffs in 9,780 WAL
  observations over 3 months; detection-literature verdict = risk-adjusted
  CUSUM). **The spec is what remains owed** — the five-tier pipeline exists
  only in a research report.
- **D-6 Branch 22 graph side.** Vector side spec'd (VECTOR_INDEX.md); the
  Glean-lineage stacked-DB exchanges remain open; FOREST symbol marks are
  "absent until then." Includes the OPEN vorpal instance-model decision
  (embedded-lib vs session worker vs KG-service pod) and the upstream patch
  list (Manifest::from_entries, content-source hook, xxh3 I3, scoped-interner
  R1, knob parameterization).
- **D-7 Branch 25 ↔ existing wire-security text.** LEDGER.md §7.3 (per-message
  PSK-derived keys, "mTLS beneath") and PROTOCOL.md §2 (per-pod summon-minted
  HKDF keys, HELLO pinning, no mTLS) describe different key models; ADR-0002
  still says the protocol spec "lives in LEDGER.md §7". Branch 25 must
  reconcile all three (PROTOCOL.md is the ratified baseline).
- **D-8 Biscuit grant machinery has no home spec.** SESSIONS §2 and SIBYL §5
  depend on it; SIBYL's status line cites "`PROTOCOL.md` (grants)" but
  PROTOCOL contains no grants material. Assign a home (likely Branch 25 or a
  SESSIONS rider).
- **D-9 VECTOR_INDEX.md status confirmation.** The design was approved
  in-message and the spec written on "do it" — but standing rule 2 (specs
  shown in-message before file write) was not literally followed for the
  formatted spec. The header says ACCEPTED; the user should confirm or demote
  to presented. (OBJECT_TIER.md correctly says presented.)

## 3. Undesigned (open branches, charter only)

15 steering · 17 remote client/terminal (the entire presentation plane —
no spec anywhere) · 18 continuity/conversation · 23 document DB ·
25 wire security · 26 multi-modal media · 27 leader-election revisit ·
28 secrets · 30 fleet fault detection/recovery · 31 replica handling ·
32 node lifecycle · walking skeleton (final).

**Unbranched gap found by this pass**: the **provider gateway** — LLM request
shaping, streaming, retry/backoff, rate limits, provider errors, failover
mechanics. PLATFORM §2/§3 state the law (one ModelConfig authority; failover
semantics) and RUNTIME §5 gives it a thread pool, but no branch or spec owns
the machinery. Every agent turn crosses it. Recommend: new branch, or fold
into Branch 14's execution half.

## 4. Drift (owed-and-forgotten) — corrected or to-correct

Corrected in the same change as this ledger's first pass (mechanical
doc-sync, no design content):

- **C-1 Fabric vocabulary** (ratified: the fabric plane is deleted; "shared
  façades" replaces "fabric façades"): AGENTS.md §3.8 ("and the fabric") + §4,
  SKILLS.md §5 + §6 heading, SKILLS_API.md §3 — swept.
- **C-2 RANK.md §2** "one synchronous query to the score service" contradicted
  ACCEPTED LEDGER_CORE sub-decision (c) (event-carried snapshots; "no
  synchronous query escapes the core") — aligned to snapshots.
- **C-3 ADR-0002 stale pointer** ("specification lives in LEDGER.md §7") —
  now points at PROTOCOL.md; LEDGER.md §7.3 annotated that PROTOCOL.md §2 is
  the ratified key model pending Branch 25.
- **C-4 AGENTS.md** "The nine agents in this document" vs the ten-agent
  roster — corrected to ten.
- **C-5 VFS.md §7** "registry (open branch)" — REGISTRY.md has been ACCEPTED;
  reference updated.
- **C-5a CONTEXT.md L3** "hosts a fixed roster of agents" vs the ratified open
  roster (AGENTS.md L3, REGISTRY custom agents) — corrected to open roster.
  Note the authority inversion this fixed: AGENTS.md defers to the glossary
  ("where this document and the glossary disagree, the glossary wins"), so
  the stale glossary line was technically law.
- **C-5b SUMMONING.md admission rule** "the roster is closed; a summon naming
  anything else is refused" vs open roster — corrected to registry-known
  (shipped or Guardian-staged custom).
- **C-5c Retired-"workspace" sweep** (SESSIONS.md AC-2 grep gate, standing
  rule 7): live design-vocabulary uses swept in AGENTS.md (×3), SUMMONING.md
  (×4), SKILLS.md (×2), and SESSIONS.md §3 itself ("Session workspace
  state"). Code identifiers (`Capabilities::WORKSPACE_RW`) and Sylk
  historical mentions left as-is.
- **C-5d GRILLING bookkeeping**: VECTOR_INDEX.md added to the SETTLED table
  (it was recorded only inside Branch 22); OBJECT_TIER.md added to ON THE
  TABLE (it was recorded only inside Branch 24); Branch 21's stale trailing
  "Next: (b) overlay representation" pointer annotated as history.

Remaining drift, needs a decision or a sweep (not mechanically safe):

- **C-6 Branch-label collision**: SERVING.md and SCHEDULER.md both claim
  "grilling Branch 21." History knows which is which; the labels should be
  disambiguated once in GRILLING.md.
- **C-7 Status-line authority**: GRILLING's SETTLED table lists RUNTIME, WAL,
  PROTOCOL, MERGE, VFS, PODS, AGENTS_RUNTIME, RANK, SCHEDULER as settled while
  their file headers still read "presented for acceptance." One authority must
  win; recommend updating headers upon explicit acceptance verdicts, and until
  then reading the table as direction-settled rather than spec-accepted.
- **C-8 Test-ID hygiene**: RUNTIME and PODS both use T-prefixed IDs (T1–T8 vs
  T1–T19); FOREST skips F20 and keeps F12–F14 in prose; PODS T18/19 and
  SCHEDULER SCH13–15 live outside their matrices. Cosmetic until cross-spec
  citations ambiguate; fold into the next touch of each file.
- **C-9 "Work plan on file" phrasing**: GRILLING says "Work plan W1–W7 on
  file" (vector) and "S1–S8 on file" (object tier) — the plans' substance is
  baked into the two specs, but no standalone plan artifact exists in the
  repo; the phrasing should not imply one.
- **C-10 ADR hygiene**: the five ADRs carry no Status/Date headers; four
  offered ADRs remain unwritten (sessions/lineage+landing engine,
  deterministic optimism, forest, open roster/offices) — and this pass adds
  two candidates: the two-planes object-tier verdict and
  TS/Python-as-bindings-never-runtimes, both user-corrected one-way doors
  currently recorded only in GRILLING/spec prose.

## 5. Residual magic-number surface (against the derivation doctrine)

- WAL.md acceptance factors: recovery ≥ **0.5×** device read bandwidth,
  throughput ≥ **0.8×** model, macOS ack ≤ **1.5×** measured, model-vs-measured
  within **20%** — multipliers over measured anchors whose own values carry no
  derivation.
- The shared "**>10%** regression fails CI" bar (RUNTIME, MERGE, PODS,
  SCHEDULER) — one hand constant repeated four times.
- RUNTIME.md provisional ≥1M cycles / ≤1µs p99 — explicitly flagged
  provisional-pending-baseline (compliant, listed for completeness).
- SERVING.md `reclaim_headroom(20 ranges)` — the weakest derivation in that
  file by its own framing.
- FOREST.md PPR α = 0.15 — flagged canonical-start + re-fit milestone
  (compliant, listed).

Disposition: each either gains a derivation at its definition site or is
explicitly ratified as a shape constant; the ledger tracks them until then.

## 6. Fit-before-influence milestones (cannot activate without data campaigns)

- FOREST AC-4: co-fit of both retention halves from Hecate's own event
  stream — observe-mode is mandatory until it exists.
- VECTOR_INDEX §7/AC-3: lineage-scale recall/latency fit precedes any recall
  claim; SOAR-variant gate (VX11) rides the same harness.
- Every ratcheted floor and commissioning-derived τ across the corpus assumes
  a **first CI baseline** that requires running code (see §0).

## 7. Armed tripwires (metrics must exist from day one)

ADR-0005/MERGE: p99 intervening-deltas-per-merge reopens eg-walker; MERGE:
rebase-livelock rescoping; SERVING §3: overlay index-rebuild vs pod-resume
budget reopens the checkpoint decision; VECTOR_INDEX §5: predicate-selectivity
reopens filtering; PODS §4b: Architect consult latency ⇒ record-replicas;
PODS §2/AC-4: WHP/HVF DAX is in-scope fork work, tracked.

## 8. External dependencies and port hazards

- **libkrun fork**: three-platform DAX + splice (WHP the risk cell) — unbuilt,
  day-one required by PODS AC-4 / SERVING §7.
- **vorpal upstream patches** (Branch 22 list): 4 commits incl. xxh3 identity
  (I3) + scoped interner R1; process-wide interner is the named multi-session
  hazard until landed.
- **Sylk port hazards** (component survey, on file): BeamSearchBBQ never
  traverses the graph it builds; deterministic RNG machinery exists unused
  while live paths use unseeded rand; maintenance signals trigger nothing;
  IVF WAL unwired in one of two places. The VECTOR_INDEX build (W1) must
  treat the Sylk code as architecture-reference only — none of these can
  survive the port.
- **FOREST reconciliation corpus** outside this repo (D-4).

## 9. Blocking order toward the walking skeleton

1. ~~**D-2 WIRE_FORMAT.md**~~ CLOSED 2026-08-17 (`WIRE_FORMAT.md` +
   `TRANSFER.md` accepted; P0 wire unblocked by process rule) →
2. ~~**D-1 CONSENSUS.md + FAULTS.md**~~ CLOSED 2026-08-17 (specs accepted
   and written; §7 receipts-verification rider open; Branch 27 → roster
   audit) →
3. Accept-or-amend the presented foundation set (RUNTIME, WAL, PROTOCOL —
   C-7's status authority) →
4. First code: runtime + SIM + wire (P0/P1), turning §0 from fact into
   history and §5/§6's baselines into numbers →
5. D-5 (Branch 14), ~~D-3~~ (closed — §9 hardenings must be *implemented* +
   OT16–OT19 green per the practical gate), Branch 25 — before agents run
   against real providers with real content →
6. Everything else per the branch tree; this ledger re-audits at each rung.
