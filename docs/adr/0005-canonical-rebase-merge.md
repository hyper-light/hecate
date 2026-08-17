# Canonical-rebase with a deterministic conflict verdict, not symmetric OT

Hecate's merge engine is not classic operational transformation. Each increment
declares its base green version; the per-session merge serializer position-maps its
operations one-directionally through the canonical deltas between base and head, then
runs a **pure, deterministic conflict verdict**: disjoint ⇒ splice into green;
identical-both-sides ⇒ accept via content identity; overlapping or ambiguous ⇒
**reject into a corrective claim** carrying the exact conflict window. There are no
symmetric transform pairs, no TP1/TP2 obligations, and no auto-merge of divergent
intents — and no LLM anywhere in the serializer's path.

## Why not symmetric OT

The falsification record: every published OT algorithm requiring TP2 (dOPT, adOPTed,
SOCT2, SDT) was later shown incorrect, including two machine-checked proofs that were
themselves invalid; TP1+TP2 is provably unsatisfiable for plain insert/delete on
strings. Under a central serializer TP2 is vacuous (Jupiter/Wave) and even TP1 is
unnecessary if submitters rebase instead of symmetric-transforming (the
ProseMirror/CodeMirror precedent). We keep the smaller machine whose obligations we
can actually prove: position-mapping composition, and verdict purity (the verdict is
a deterministic function of canonical history + increment — the property classic OT
never states because classic OT never rejects).

## Why reject at all

Auto-merge is safe when an attentive human sees the merged result instantly; Hecate's
authors are agents that testified and moved on — a silent interleave produces code
nobody wrote or reviewed, breaks the green invariant (what enters green must be what
was validated), and launders a claims-scoping failure into plausible corruption. The
kinship is Pijul (conflicts as first-class objects with a workflow), not git: our
conflicts are declared-operation-exact (no diff3 inference pathologies), hot
(millisecond divergence windows, not weeks), and resolved by the authoring agent or
the Arbiter with machine-precise evidence — never by a cold human at conflict markers.

## Considered Options

- Symmetric TP1 OT (Wave-style): generality with a thirty-year record of published
  incorrectness, buying nothing under a total order.
- eg-walker (Gentle & Kleppmann 2024): solves long-divergence merge cost our
  streaming gate structurally prevents, and always auto-merges — no reject path
  exists. **Tripwire recorded**: if p99 intervening-deltas-per-merge crosses a
  measured threshold (offline/long-lived divergence appears), this branch reopens
  with eg-walker as the leading candidate.
- Agentic resolution inside the serializer: rejected — model latency and
  nondeterminism in the one component whose output must be a replayable pure
  function. Agentic judgment lives above the verdict, in the Arbiter.
