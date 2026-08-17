# Hecate Design Tree — Grilling Ledger (resume file)

Snapshot: 2026-08-16, end of spec-level session 2. Resume from here. An item is
**settled** only when its spec was shown and accepted; drafted-but-unaccepted
specs are **on the table**; branches without specs are **open**.

## Standing rules (user-established; enforce every exchange)

1. **Ledger scope test**: the ledger = proof of work — claims, testaments,
   validations, artifacts, nothing else. Config→config; ops→logs; working
   state→its owning service. (User corrected twice; never again.)
2. **One decision per exchange, worked to settlement.** No bundle ratifications.
   Assent without a shown spec = direction only, spec owed. Specs are shown
   IN-MESSAGE before any file is written (violated once with the Sibyl draft —
   deleted and re-presented; do not repeat).
3. **Research before argument** for every substantial decision; receipts inline.
4. **Maximal test**: every design examined for maximally correct/robust/
   performant/efficient at BOTH laptop and Meta scale; laptop is always the
   derived degenerate of one formula family — no modes, ever.
5. **No ambient anything crosses a session fence.** Cross-session = same-user
   Archivalist recall or Guardian-staged registry publication only.
6. **Agents never allocate**: they issue claims; machinery executes; issuers
   monitor/evaluate. Judgment above, deterministic consequence at chokepoints.
7. **Coined names are provisional** until mechanisms settle and the glossary
   captures them. "Workspace" is RETIRED (grep-gated) → lineage / session /
   work volume.
8. **User review is a first-class gate** (default prompt for materialization).
9. Constants derive from anchors with derivations at definition sites; floors
   ratchet from first CI baseline; observe-mode-first for any new influence.

## SETTLED (spec shown + accepted)

| Spec | Content anchor |
|---|---|
| `docs/specs/RUNTIME.md` | own sharded async runtime, deterministic-by-construction, SIM driver, no-Arc/arena doctrine, io_uring day-one, lint wall |
| `docs/specs/WAL.md` | per-session logical logs over derived-ω streams, always-full durability, chained CRC + torn/corrupt discrimination, consensus-API-only commit path |
| `docs/specs/PROTOCOL.md` | dual-stack UDP/TCP, per-pod HKDF keys + AAD headers, HLC64 + 24B fencing, counter nonces, credit delta streams, hecate-wire (Rust-only, canonical-or-reject, compiler-enforced evolution). OWED at build time: WIRE_FORMAT.md before codec implementation |
| `docs/specs/MERGE.md` + ADR-0005 | canonical rebase + pure deterministic verdict, byte-exact intervals on declared ops, reject-to-corrective, Arbiter gate + frontier service, no LLM in serializer |
| `docs/specs/VFS.md` | one BLAKE3 CDC chunk store, manifests as layers, three volume roles (work volume/green/tools), virtio-fs serving, tool plane + 3 Guardian gates, content-addressed distribution |
| `docs/specs/PODS.md` | microVM pods, manifest-projection rootfs + DAX day-one all platforms, hecate-init 5 duties, warden+sensor (§6), warm tiers + reseed-on-resume, autoscaling classes (§4b; Architect=serialized-judgment), NO work-bearing memory ever persisted |
| `docs/specs/AGENTS_RUNTIME.md` | serial turn/instance, park-on-consult AND long tools, hold-teardown at human latency, brief+claims handoff (volume re-binds; no transcript), warden-topology skills, R-series |
| `docs/specs/RANK.md` | domain enums, derived bindingness, override-refuse as sole enforcement, score service (prevalence/specificity/trust, demote-only, observe-first). A1–A5 applied to LEDGER.md (single vocab; closed enums+bijection; retirement=custody transfer to Archivalist archive, anti-tombstonic; deadlines as replay inputs; layered scope map) |
| `docs/specs/SCHEDULER.md` | sharded deterministic evaluation-log spine; **deterministic optimism** (parallel intent-aware speculative planners, logged outputs, serial pure applier); content-keyed memoization + snapshot-page/chunk locality scoring; gang-at-admission; Borg bands, hard limits; §9b request lifecycle (amendment=supersession-with-reuse; disposition-retry partials; issuer judges sufficiency) |
| `docs/specs/SIBYL.md` | the 10th agent (name user-ratified): workstream judgment above sessions, lineage-partitioned instances (never global), judgment/machinery split, experiment-as-claim-tree, content-blind, grant brokering (Biscuit), user-plane ledger. AGENTS.md + glossary landed |
| Architecture set | `docs/architecture/{AGENTS,SUMMONING,LEDGER,SKILLS,PLATFORM}.md`, `CONTEXT.md`, ADRs 0001–0005 — amended throughout this session (open roster/offices, Arbiter, summon-as-claim, retirement, work volume, ten agents) |

## ON THE TABLE (drafted + shown; awaiting acceptance — settle ONE at a time)

1. `docs/specs/SESSIONS.md` — whole (lineage first-class, per-session pods,
   three-layer landing engine + jj conflict algebra, conflict deposits, review
   gates, 6-stage evaluation funnel with numbers, lifecycle/churn/GC, floors).
2. `docs/specs/LEDGER_CORE.md` — + sub-decisions (a) apply-on-ack, (b) no outbox
   (log+cursors), (c) event-carried score snapshots.
3. `docs/specs/AUTOSCALING.md` — + sub-decisions (i) ratio-law-only,
   (ii) scale-to-zero for idle daemons.
4. `docs/specs/REGISTRY.md` v2 — syllium-informed; ref-CAS sole mutation; watch
   API; schema-doc kinds; §4b materialization path.
5. `docs/specs/SKILLS_API.md` — one derive → five artifacts; S6 surface counts.
6. `docs/specs/HEALTH.md` — one plane (Sylk ran four); no authority.
7. `docs/specs/FOREST.md` — Z-set field engine, ACT-R/FSRS/MMAS/Parunak/PPR
   dynamics, primary-by-construction, observe-mode value gate, session-isolated
   (global-forest tier DELETED as data-leak; user correction).

## OPEN BRANCHES (no spec)

- **14 Handoff detection math** — context accounting (provider usage vs local
  estimate; what counts), threshold derivation, GP/UCB vs changepoint (CUSUM/
  EWMA) for performance dropoff, evidence-bundle assembly. RESEARCH FIRST.
- **15 Steering machinery** — mid-task user guidance: interrupts as
  supersession, priority hints as claim fields, turn-level injection.
- **17 Remote client + terminal** — seam remote binding: attach/detach, view
  subjects (pane=subscription), input lease mechanics, cursor resume, offline
  queue, presentation plane rendering from deltas.
- **18 Continuity + conversation** — carry-forward/recall over the archive
  (same-user path partially shaped in SESSIONS/FOREST), Guide conversation model.
- **20 Consensus + fault matrix** — direction argued, UNRATIFIED: per-session
  Raft-family groups (5 improvements over hyperscale: homogeneous nodes,
  pods-never-gossip liveness, work-liveness-to-ledger, consensus-as-pure-log,
  AD-52 baseline). Raft-implementation-practice research owed, then
  CONSENSUS.md + FAULTS.md (failure×obligation matrix, crash-fault scope).
- **Walking skeleton** — final branch; re-presents against completed tree
  (P0 wire → P1 runtime → P2 spine → P3 pod leg → P4 first agent → P5 first
  merged change; now must thread Sibyl/home-session/lineage into first light;
  each rung carries fault-matrix cells).
- Small owed: full "Guide summons" language sweep (key sites corrected; grep
  pass owed); ADR candidates (sessions/lineage+landing engine; deterministic
  optimism; forest; open roster/offices) — offer per ADR rules.

## Cost ledger (accepted burdens; check every new decision against these)

Owned wheels: runtime+SIM, claims protocol, hecate-wire codec, merge engine +
verdict theorem, Z-set field engine, forked VMM stack (WHP = risk cell), sharded
scheduler. Compounding: walking-skeleton first light is far behind the wheel
count — acknowledged repeatedly, accepted under "we do not fear complexity."
Other standing costs: encrypt-always CPU; per-increment validation; max/ultra
primary models; full-machinery-locally (degenerate consensus, session infra
floor — ratcheted budget); shard-local placement optimality (slow rebalancer);
two-phase arena lookups; tokio ecosystem cut off (blocking rustls egress).

## Research reports on file (in-conversation; summaries baked into specs)

Sylk surveys (agents ×3, VFS/OT, Tool VFS); hyperscale protocol (+AD-52); CLAIMS
corpus distillation; cross-platform microVM (libkrun/WHP lineage); Rust
runtime/DST; WAL/fsync/group-commit; codec landscape (zerocopy/postcard/borsh);
OT correctness (TP1/TP2 record, diff3 formal, judge biases); syllium
agentregistry implementation; workspace/namespace orchestration (CitC/EdenFS/
Capsule/prebuild pools); parallel workstreams + land queues + Chubby/Biscuit;
scheduler architectures (Borg/Omega/Twine/Nomad/K8s, read directly);
divergence/merge (jj algebra, eg-walker, mergiraf numbers, 267K-merge overlap
study, agentic-PR conflict rates); selection-gap funnel (CodeMonkeys/OpenHands/
S*/RTV/PDR numbers; composition correction).
