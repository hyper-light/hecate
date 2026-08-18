# SPEC: the Sibyl — the workstream agent

Status: ACCEPTED 2026-08-16 (name ratified by the user; spec shown in-message and
accepted with three revisions folded). The tenth role. Companions: `SESSIONS.md`
(lineages, landing, review), `SCHEDULER.md` (summon flow), Branch 25 (grants — owed; home assigned by D-8, 2026-08-18).

## 1. Role

The user's per-user agent **above sessions** — the first thing a terminal attaches
to, and the only agent whose domain is **workstreams rather than work**. The Sibyl
judges which sessions and experiments should exist: spawning, forking, suspending,
closing; composing A|B|…|N variant experiments and their evaluator sessions;
arbitrating who may materialize; brokering what crosses a session fence. It never
touches the work inside a session.

- **Scope: one owner.** A Sibyl sees only its own user's estate — catalog,
  lineages, lifecycle state. The isolation law needs no exception for it.
- **Instances partition by lineage (Revision 1).** Workstream judgment is
  lineage-local, so **a lineage's judgment serializes through exactly one Sibyl
  instance at a time** — assignment via at-most-once claims with lease-expiry
  redelivery (the frontier-service pattern). Quiet lineages pool onto shared
  instances; hot lineages get dedicated ones; instance count derives from
  active-lineage load. No configuration yields a global — or per-user-global —
  Sibyl at scale: no one instance handles all sessions, even one owner's.
  Estate-wide mutations serialize per target through the same claim machinery.
- **Home**: the home session (`SESSIONS.md` §2) — no lineage, the user-plane
  ledger, the catalog. Scale-to-zero between uses; the one-command boot flows
  through it invisibly.
- **Models**: Guide-class judgment surface — Claude Sonnet 5 (max) / GPT 5.6 Pro
  Luna (ultra); user-picked primary, failover-only alternate; Scribe attached.
- **Scaling class**: load-driven **by lineage partition** (amends the roster
  table's serialized-judgment placement: serialization is per lineage, scaling is
  per estate).

## 2. Judgment vs machinery (Revision 2)

The agent thins; the services fatten. **Deterministic user-plane services** own:
the catalog, TTL/GC sweeps, lease mechanics, grant-token issuance mechanics, and
churn bookkeeping — re-derivable state, health-monitored, exactly like the
frontier service. A storm of forks and teardowns is service throughput, not agent
turns.

The Sibyl's cycles are **judgment only**:
1. **Experiment composition** — which variants, from which lineage node, on which
   templates, under what budget.
2. **Stop-rule decisions** — consuming the evaluation funnel's measured signals
   per experiment to decide when to stop spawning variants (critic-gated
   stopping over fixed-N; the curves are the receipts).
3. **Arbitration** — materialization-lease calls between competing sessions.
4. **Grant approvals** — the judgment on what crosses a fence; issuance is
   machinery.
5. **Adoption recommendations** — winner / disjoint composition / regeneration
   (per `SESSIONS.md` §7), presented through the review gates the user rules on.
6. **Template selection defaults and estate hygiene judgment** — what to prune,
   what to archive; the sweeps themselves are services exercising SES9's
   never-lose-work guarantee.

## 3. The experiment, first-class (Revision 3)

`Experiment = (lineage node, purpose, N variant sessions, evaluator session,
budget, stop-rule state, verdict)` — represented on the **user-plane ledger as a
claim tree**: the experiment claim; variant summon sub-claims; the evaluation
claim; the adoption/materialization claim — all `caused_by`-linked. This buys,
with existing machinery:

- Full proof and monitoring of an experiment's life; orphan sessions impossible.
- Funnel signals consumed per experiment for stop decisions.
- PDR-regeneration as a Sibyl-spawned, summary-conditioned variant **within the
  same tree**.
- Failure handling as ordinary claims: a dead evaluator is a failed claim with a
  disposition (re-summon); budget exhaustion is a counted outcome surfaced to the
  user.
- The user's review gate anchored to the tree's adoption claim.

## 4. Session lifecycle as claims

Every create/fork/suspend/resume/close/archive is a claim on the user-plane
ledger, executed through the standard summon flow: the Sibyl requests, **the
scheduler places and provisions** (a session's core unit is the gang-admission
transaction), Guardian admission validates, the Sibyl monitors and evaluates. It
allocates nothing directly. In-session Guides relay workstream requests ("fork
this") to the Sibyl as claims — the Guide cannot fork directly.

## 5. Grants

Cross-fence access (an evaluator reading variants' greens and result artifacts)
is Sibyl-brokered: **Biscuit-shaped capability tokens** — offline-verifiable
against the Sibyl's public key, holder-attenuable, expiry- and fencing-bound,
with third-party blocks encoding approval chains ("materialization requires the
evaluator's signed verdict block"). Grants scope to **named manifest refs**,
never "session access." Issuance mechanics are service work; the grant decision
is Sibyl judgment; consequential grants default to SafetyPolicy review postures.

## 6. Boundaries

- **Content-blind by default**: catalog metadata and lifecycle state only —
  never session content; **no session key material** (grants confer access via
  the granted session's own machinery). A compromised Sibyl can misdirect
  lifecycle but read nothing, and every misdirection is a user-plane claim in
  plain sight.
- **No work authority**: no work claims inside sessions, no override of
  in-session judgment, no rank in any work domain. Rank: **Workstreams — Sibyl
  1, Guide 2, Architect 3**; the user supreme, as everywhere.
- **No immunity**: summon requests pass Guardian admission; scribed, scored,
  challengeable. The Sibyl is not the Guardian.

## 7. Test matrix (failure each catches)

| # | Test | Catches |
|---|---|---|
| WV1 | Content-blindness structural: no code path from Sibyl to session content, keys, or overlays; brokered grants are for others and logged | the estate agent becoming a skeleton key |
| WV2 | Lifecycle completeness: every session state change traces to a user-plane claim with the Sibyl (or user) as issuer | ghost lifecycle acts |
| WV3 | Lease arbitration: single holder per target under concurrent requests; fencing kills stale holders; handovers recorded | disk split-brain via the arbiter itself |
| WV4 | Grants: attenuation-only; expiry/fencing supersession kill access; declared third-party blocks required; revocation fails closed | undead access |
| WV5 | Relay flow: in-session "fork this" reaches the Sibyl as a claim; the Guide cannot fork directly | a second lifecycle authority |
| WV6 | Estate economics: instance count derives per active lineage; scale-to-zero verified; one-command boot budget met with the Sibyl in the path | the user plane as resident tax |
| WV7 | No work authority: the Sibyl cannot post into a session's ledger (structural); workstream rank grants nothing in work domains | scope creep into work |
| WV8 | Lineage-judgment exclusivity: concurrent requests on one lineage serialize through one instance; assignment redelivers on instance death; dual judgment never occurs | forked workstream authority |
| WV9 | Experiment-tree completeness: every variant, evaluation, and adoption traces into its experiment claim tree; orphan sessions impossible | untracked experiments |
| WV10 | Judgment/machinery split, structural: no O(estate) computation and no churn-path operation executes in the agent; a fork/destroy storm completes with zero Sibyl turns beyond the initiating decision | the agent as throughput bottleneck |

## 8. Acceptance criteria

1. WV1, WV3, WV5, WV8 permanent CI gates.
2. All Sibyl authority is exercised as user-plane claims — zero out-of-band
   lifecycle paths exist.
3. Content-blindness is structural (module reachability, not policy).
4. `AGENTS.md` carries the tenth role, roster row, and Workstreams rank row in
   the same change as this acceptance; the glossary carries the name.
5. Every duty's budget (stop-rule curves, TTL warnings, boot latency, instance
   derivation) derives from stated anchors.
6. Instance↔lineage assignment is claims-based with measured redelivery; no
   configuration yields a global or per-user-global Sibyl at scale.
