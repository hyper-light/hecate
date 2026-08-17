# SPEC: the vector index — sealed IVF+Vamana generations, exact overlays

Status: ACCEPTED 2026-08-17 (in-session user approval, "pending the
filesystem research" condition resolved by `OBJECT_TIER.md`'s two-planes
factoring). This spec is the **vector side** of Branch 22 — the "IVF+Vamana
pair" its design exchanges were armed for; the graph-side (Glean-lineage
stacked-DB) exchanges remain open and compose with this spec via the
colocation law. Research on file (GRILLING.md Branch 22): DiskANN family
(DiskANN/FreshDiskANN/SPANN/SPFresh/OOD-DiskANN/ParlayANN/PipeANN, primary
texts), IVF routing + quantization + filtering receipts (FAISS wiki/paper,
SOAR, RaBitQ, ACORN/Filtered-DiskANN, Big-ANN'23), production architectures
(turbopuffer/Pinecone/Lance/Milvus/Vespa/Qdrant), DistributedANN/BatANN.
Substrate inherited from Sylk's `core/vectorgraphdb/vamana/ivf`
(architecture, not code).

## 1. Shape

A corpus is served as **immutable content-addressed generations** plus
**per-session exact-search overlays**. A generation is three sealed artifact
kinds on the durable plane (lineage class, `OBJECT_TIER.md` §4):

1. **Routing artifact** — centroids + cell→artifact map. Small by
   construction (`K ≈ (15–20)·√N` derived — tens of MB at 10⁸ vectors);
   replicated everywhere including the laptop (popularity-mirrored content,
   not special machinery).
2. **Cell artifacts** — per-cell full vectors + RaBitQ codes + Vamana
   adjacency, co-located so exact rerank rides the same read (the DiskANN
   §3.5 layout law). Cells (or cell-groups, count derived from fleet and
   artifact-size anchors) are the placement units.
3. **Generation manifest** — artifact list + parameters + the **pinned
   embedding model+version** (a generation is reproducible only if the
   embedder is pinned; re-baseline-on-model-change is a priced, scheduled
   event, never a drift).

The mutable pointer is a registry-contract ref (`set_ref_if`), flipped only
after placement (`OBJECT_TIER.md` §4 ladder). Old and new generations serve
concurrently under revision-floor reads; unreachable generations are
mark-swept.

**No incremental index mutation exists.** The banned mechanisms are named
with their reasons: FreshDiskANN StreamingMerge and SPFresh LIRE are
arrival-order-dependent (un-content-addressable, irreproducible) and
converge to recall **below** a fresh static build; Milvus-shaped
growing/sealed streaming machinery is the right shape with machinery this
architecture already has as overlays; their motivating premise — rebuilds
costing days at 10⁹ scale — is false at lineage scale (`k_build ≈ 1.7
core-ms/vector`, ParlayANN anchor: a 10⁷-vector rebuild is minutes on a
workstation). The crossover to in-place schemes (≈ N ≥ 10⁹ × ~1%/day churn
× sub-day freshness) is not Hecate's regime; bursty updates at
merge-gate/landing events are natural re-baseline points.

## 2. The deterministic build

- **Balanced hierarchical clustering** with the balance term in the
  objective (SPANN's multi-constraint form) and a derived cell-size cap,
  split-at-cap during the build. **Balance is a load-bearing requirement of
  placement, not an optimization**: cell-size skew's effect on load is
  quadratic (FAISS 1T receipt: <10 lists at >600× skew → 120 s queries).
- **Closure multi-assignment** of boundary vectors: the ε₁ distance-ratio
  rule + RNG-rule pruning of same-direction replicas + a derived replica
  cap (~1.2× storage at SPANN's operating point). Closure serves three
  duties at once: boundary recall, per-cell graph connectivity (DiskANN's
  own merged build), and determinism — an FP near-tie vector lands in
  *both* cells, converting tie nondeterminism into correctness-neutral
  duplication. The **SOAR-decorrelated variant** (rank eligible spill cells
  by residual decorrelation) ships **only behind a benchmark** against
  plain ε₁-closure — it is a novel composition, approved conditionally.
- **Per-cell Vamana** built ParlayANN-style: prefix-doubling batches
  against immutable pre-batch snapshots, reverse edges applied by semisort
  in canonical order, pinned iteration order. Determinism is free (1.2×
  faster than the reference build; quality within 1%). Build workers are
  stateless: (vector set in) → (sealed graph artifact out); **build
  verification is a content-hash comparison** — byte-identical on any
  node, CI-gated cross-platform.

## 3. Routing and query

- **Assignment and routing use exhaustive centroid scan** with a pinned
  kernel and fixed tie-break (lowest cell id) — never graph-assisted
  (accuracy and reproducibility receipts both). Deterministic given the
  generation.
- **Query fanout is ε₂-adaptive** (SPANN's query-side pruning: probe cell
  ij iff `d(q,c_ij) ≤ (1+ε₂)·d(q,c_i1)`) — per-query fanout instead of a
  fixed nprobe; the 6.36-of-32-machines / 80.3%-saved receipt is the entire
  distributed-efficiency case.
- **Per cell**: quantized traversal (RaBitQ/BBQ) + **error-bound-driven
  exact rerank** — a candidate is dropped iff its provable distance lower
  bound exceeds the current best exact distance. Rerank depth is thereby
  derived per query, not configured; "exact rerank always" becomes
  provable (unbiased estimator + bound), and one magic number is deleted.
- **Cross-cell**: merge top-k across probed cells ∪ exact overlay scan −
  tombstones.

## 4. Overlays and re-baseline

- Per-session overlay = **WAL-journaled flat segment** (exact search only —
  the session fence bounds it; consistent with `FOREST.md` §3's no-ANN
  law) + tombstone bitmap over the sealed baseline. Deletes never touch
  sealed artifacts. A crash between re-baselines loses nothing (the
  journal is load-bearing — the unwired-IVF-WAL lesson honored).
- **Re-baseline trigger is a formula, never a cliff**:
  `c_scan·|overlay| ≥ β·c_indexed(N)` (β derived) — turbopuffer's 128 MiB
  visibility cliff converted into a derived trigger — with merge-gate
  commits and landings as the natural event points. Re-baseline consumes
  the journal, builds the next generation (§2), places it (durable plane),
  flips the ref.

## 5. Placement, serving, isolation

- Generations are **lineage-class** content: copyset-map placement, scrub,
  EC tail per `OBJECT_TIER.md` §4. Query-node warm copies are **cache
  role** (`OBJECT_TIER.md` §5): sealed immutability means zero
  invalidation logic; admission is the endurance-governed, declared-future
  kind (a probe plan is a declared working set).
- **Colocation law** (shared with the graph side): overlays are served
  where their base generation is resident; placement key = base
  generation, entering scheduler locality scoring.
- **Realm/tenant isolation = generation-lineage-per-scope** (the
  turbopuffer namespace-per-query-scope pattern): tenant predicates never
  enter the hot index. Session-private vectors exist only in that
  session's overlay.
- **Predicate filtering inside a corpus** (symbol kind, path scope):
  cell-level metadata bitmaps + post-filter under adaptive fanout.
  ACORN/Filtered-DiskANN machinery is billion-scale medicine, deferred
  with a **tripwire**: measured predicate selectivity low enough that
  post-filtering wastes most of each probe reopens the decision.

## 6. Laptop degenerate

All cells local under the trivial placement map; the routing artifact was
resident anyway; overlays are session-local by construction; cold start on
a fresh machine = fetch ref → routing artifact → demand-fill cells. Same
formulas, no modes.

## 7. Fit milestones (constants from our data)

ε₁, ε₂, β, the cell-size cap, the closure replica cap, and cell-group
granularity are all derivable — and none are derivable from the literature
alone: every published number is billion-scale benchmark data
(SIFT1B-class), not code-embedding corpora at lineage scale (10⁵–10⁸).
**The lineage-scale recall/latency fit on our own corpora is the stated
first milestone** (the FOREST.md co-fitting pattern); the SOAR-variant
benchmark (§2) rides the same harness.

## 8. Non-goals (named, with reasons)

FreshDiskANN merge machinery, LIRE split/merge/reassign, growing/sealed
segment pipelines and MQ handoff, per-label filtered graphs, HNSW anywhere,
any second freshness mechanism beside the overlay, and
global-graph-over-KV distribution (DistributedANN's regime — revisit only
past ~10⁹–10¹⁰ vectors per corpus with sustained high QPS; its 6× claim is
single-sourced). Each exclusion is an order-dependence, wrong-scale-premise,
or duplicated-shape reason recorded in Branch 22.

## 9. Test matrix (failure each catches)

| # | Test | Catches |
|---|---|---|
| VX1 | Build determinism: same corpus + parameters + embedder pin ⇒ byte-identical artifact set, cross-platform, cross-run (content-hash comparison) | irreproducible generations; platform forks |
| VX2 | Routing determinism: permuted inputs and platforms ⇒ identical probe sets and tie-breaks | FP-tie divergence; graph-assisted assignment creep |
| VX3 | Balance: cell-size cap honored at build; measured skew within derived bound; placement load tracks the bound | the quadratic-skew cliff |
| VX4 | Closure near-tie property: vectors within the tie band land in all eligible cells; recall at boundaries ≥ derived floor vs exact oracle | boundary recall loss; tie nondeterminism |
| VX5 | Recall floor: end-to-end recall@k vs exact oracle on the fit corpora, ratcheted from first baseline | silent quality regression |
| VX6 | Rerank bound honesty: no candidate dropped whose true distance beats the returned set (property, per query fuzz) | the error bound being decorative |
| VX7 | Overlay crash: kill between re-baselines ⇒ WAL replay reproduces overlay + tombstones exactly | fresh-data loss |
| VX8 | Trigger fidelity: re-baseline fires at the formula point, not before/after (synthetic growth sweep) | cliff behavior; over-eager rebuilds |
| VX9 | Generation swap: old+new served concurrently under revision-floor reads; no query observes a torn generation | torn-pointer reads |
| VX10 | GC: unreachable generations collected; reachable never (ties OT9) | leak-forever / dangling artifacts |
| VX11 | SOAR-variant gate: decorrelated closure ships only if ≥ plain ε₁-closure on the fit benchmark | novel composition on faith |
| VX12 | Laptop first-light: build+serve on N=1 within derived budget; identical formula outputs vs fleet mode | mode creep |

## 10. Acceptance criteria

1. **No mutation path into sealed artifacts exists** (structural test);
   the overlay is the only freshness mechanism.
2. VX1 (build determinism) and VX7 (overlay durability) are permanent CI
   gates from first light.
3. Every constant (K, ε₁, ε₂, β, caps, cell-group size) carries its
   derivation at the definition site; the lineage-scale fit (§7) precedes
   any recall claim.
4. The embedder pin is in every generation manifest; a generation without
   one fails validation.
5. The SOAR-decorrelated variant is benchmark-gated (VX11); plain
   ε₁-closure is the default until it wins.
6. Storage rides `OBJECT_TIER.md` exclusively — no second storage
   contract, no private placement, no direct disk paths.
