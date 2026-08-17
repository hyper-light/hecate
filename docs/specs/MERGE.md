# SPEC: the merge engine — canonical rebase, deterministic verdict, Arbiter gate

Status: presented for acceptance (grilling Branch 4; direction ratified, ADR-0005).
References: OT correctness research on file (GRILLING.md); Jupiter/Wave serializer
topology; ProseMirror rebase precedent; Pijul conflict-as-first-class; MongoDB Realm
model-based testing; Sylk merge fault family (F2/F3/F4/F6/F9/F10).

## 1. Model

Per session: one **merge serializer** — a single-owner task (hecate-rt) that totally
orders all merges into green. Inputs are **increments**:

```
Increment {
  claim: ClaimRef,                 // the work this increment belongs to
  base: GreenVersion,              // declared, never inferred
  ops: Vec<FileOp>,                // the actual operations, hecate-wire encoded
  basis: Option<Lease>,            // disjointness fast-path evidence
}
FileOp = Edit { path, ops: Vec<ByteOp> }        // ByteOp = Insert{at, bytes} | Delete{range}
       | Create { path, content } | Remove { path }
       | Rename { from, to } | Mkdir { path }
```

Pipeline per increment, all inside the serializer, all deterministic:

```
map:     position-map ops through canonical deltas (base..head], one-directional
verdict: pure fn(canonical history, mapped increment) -> Accept | AcceptIdentical | Conflict(windows)
apply:   splice accepted ops into green (chunk-granular, VFS.md §5); bump green version
record:  merge-log record + apply commit atomically — a merge that cannot be
         recorded never applies (Sylk F6 closed)
```

## 2. Position mapping

- One-directional only: increment ops map **through canonical history**, never
  against each other. Mapping is per-path over the intervening deltas' byte effects:
  inserts shift positions, deletes contract them; an op whose anchor falls inside a
  concurrently deleted range is not mapped — it is a conflict class (§3).
- Mapping composes: `map(d1..d3) = map(d2..d3) ∘ map(d1..d2)` — a proven property
  (test M4), which is what makes batching and replay coherent.
- File-level ops map by path identity through renames; concurrent rename+edit maps
  the edit to the new path; concurrent rename+rename of one path is a conflict.

## 3. The verdict

A **pure, deterministic function** — no clock, no randomness, no IO, no model — of
(canonical history since `base`, mapped increment). Classes:

| Verdict | Condition | Consequence |
|---|---|---|
| Accept | all mapped ranges disjoint from intervening effect ranges | splice |
| AcceptIdentical | op content-identical to an intervening change (same range, same bytes) | no-op accept via content identity — diff3's "false conflict" class, auto-cleared |
| Conflict | range overlap or containment; edit anchored inside a concurrent delete; same-position concurrent inserts; concurrent rename/rename; create/create on one path with differing content | reject with windows |

- Detection is **byte-exact interval overlap on declared operations** — sweep-line
  over base-coordinate effect ranges, O((n+m) log(n+m)). No diff inference exists
  anywhere in the engine (the diff3 pathology family — phantom conflicts,
  instability, non-idempotence — is structurally unreachable).
- **Leases fast-path, never guard**: a valid basis proving path-disjointness from all
  intervening deltas skips map+verdict for those paths. A stale lease changes cost,
  never correctness.
- Verdict purity is the engine's central theorem: same (history, increment) ⇒ same
  verdict, on any shard, any platform, any replay, any seed.

## 4. Conflict windows and the corrective path

- A `Conflict` carries **windows**: per path, the byte ranges of both sides' ops plus
  the refs of the claims/deltas that produced the intervening changes — evidence, not
  markers. Detection granularity is bytes; **presentation** granularity is line runs,
  optionally labeled with the enclosing tree-sitter node — labeling only, never
  AST-based auto-resolution (measured false-merge record).
- **Fast path** (first conflict on a region, single author): corrective claim to the
  authoring Engineer — rebase against the window, resubmit. Seconds, no agent
  adjudication.
- **Escalation** (repeated conflict on a region, or cross-engineer): the **Arbiter**
  adjudicates with full claims context and authors the corrective routing — who
  rebases, what gets rescoped, or a specified unified change implemented by an
  Engineer. Escalation thresholds are derived from observed conflict recurrence, not
  constants.
- Rejects are **non-blocking**: the serializer emits the verdict and proceeds; the
  corrective is asynchronous. No head-of-line stall.

## 5. The Arbiter gate flow

- **Frontier service** — a deterministic harness service in the session's colocation
  unit, beside the serializer. Consumes the **merge log** (VFS-subsystem state, not
  the ledger); owns the reviewed-through cursor and the scope→findings working index
  as its own re-derivable state; batches contiguous green versions into
  scope-coherent review units; **issues review claims** as a system participant; and
  serves hot-context queries ("prior findings for scope X") to Arbiter replicas over
  the protocol — Arbiter replicas are separate microVMs; their shared context is this
  service, by construction.
- **The ledger carries only its four things**: review claims (at-most-once dispatch,
  lease-expiry redelivery across replicas) and closing testaments whose finding
  artifacts are the evidence. History flows to the Archivalist through normal record
  paths.
- **Streaming analysis**: Arbiter replicas review as-it-merges, so the whole-work
  verdict at claim close is largely precomputed.
- **Gate**: on the work claim's closing testament, the **Arbiter evaluates** the
  whole-work validations (quality, coherence, adherence to user directives,
  robustness, efficiency, performance, correctness — Architect joining on design
  questions; Guardian safety and SafetyPolicy user disk-approval alongside). The gate
  itself is a chokepoint where the verdict's structural consequence fires — validated
  ⇒ per-descriptor disk commit unlocks — never an evaluator.

## 6. Contention control and tripwires

- Same-scope work is serialized **above** the engine: claims scope entries +
  `depends_on` sequencing + lease ordering. The engine's rejects are the residue
  after three prevention layers.
- Ledger-visible tripwires (derived thresholds, measured baselines):
  - sustained rebase-retry rate on a region ⇒ Arbiter adjudication escalates and
    scoping is revisited (livelock guard);
  - p99 intervening-deltas-per-merge ⇒ reopens the eg-walker branch (ADR-0005) with
    data in hand.

## 7. Test matrix (failure each catches)

| # | Test | Catches |
|---|---|---|
| M1 | Verdict purity: same (history, increment) ⇒ identical verdict across shards, platforms, replays, seed sweeps | nondeterministic rejection — racy conflicts |
| M2 | Oracle fuzz: random op sets vs an independent brute-force interval checker — zero false accepts (overlap merged) and zero false rejects (disjoint refused) | silent interleaving; phantom conflicts |
| M3 | Replay equivalence: green state is a pure function of the merge log — replay from any snapshot reproduces byte-identical green | hidden serializer state |
| M4 | Mapping composition property: `map(a..c) == map(b..c) ∘ map(a..b)` over generated histories | incoherent batching/replay |
| M5 | AcceptIdentical: concurrent identical edits auto-clear via content identity; near-identical do not | false-conflict regression; sloppy identity |
| M6 | Apply/record atomicity under SIM power-cut sweep: no applied-but-unrecorded merge exists at any cut point | the Sylk F6 orphan-merge class |
| M7 | Deterministic ordering: merge-log records, paths, and window lists identically ordered across runs | map-iteration nondeterminism (Sylk F10) |
| M8 | Rename matrix: rename+edit, rename+rename, create/create, edit-in-delete — each lands in its specified class | file-op edge cases |
| M9 | Frontier at-most-once: replica crash/lease-expiry fuzz — every green version reviewed exactly once; cursor re-derivation from merge log reproduces identical service state | duplicate/lost review; unrecoverable frontier |
| M10 | TLA+ serializer model + model-based test generation against the implementation (Realm pattern) | protocol-level ordering bugs the unit tests can't reach |
| M11 | diff3/git corpus calibration: verdicts compared, divergences *reported* (never gated) | drift from human merge intuition, without inheriting the unstable oracle |
| M12 | Architecture test: the serializer crate has no provider/LLM dependency; no await on any agent in map/verdict/apply/record | judgment leaking into the hot path |

## 8. Acceptance criteria

1. M1/M2 CI-gated permanently: verdict purity and zero-false-accept/reject against
   the oracle across the standing seed sweep.
2. M6 power-cut sweep: apply and record are atomic — no cut point yields divergence.
3. No silent interleave path exists: every overlap class terminates in Conflict;
   grep-proof: no code path applies overlapping mapped ops.
4. No LLM, clock, RNG, or IO in map/verdict — enforced by the runtime lint wall plus
   M12.
5. Frontier service state is fully re-derivable (delete state, replay merge log,
   byte-identical index and cursor).
6. Review claims and finding testaments are the only ledger objects the review
   pipeline creates (standing ledger-scope rule).
7. Conflict windows are byte-exact; AST appears only in presentation labels.
8. Throughput floors ratcheted from first CI baseline (merges/sec at fixed increment
   size; verdict µs p99); regression >10% fails CI.
9. Tripwire metrics emitted from day one; thresholds derived, with derivations at the
   definition sites.
