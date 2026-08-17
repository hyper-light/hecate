# Hecate

Hecate is a multi-agent coding harness written in Rust. It hosts a fixed roster of agents as microVM-isolated, network-addressable workloads, coordinates their work through a durable claims ledger, and inherits its architecture (not its code) from Sylk.

## Language

### Claims

**Ledger**:
The durable proof of work: work required (claims), work claimed (receipt), and work completed or failed (testaments — judged by validations, evidenced by artifacts). Nothing else. Configuration belongs in config; operational events in logs; working state in its owning service.
_Avoid_: board, journal, queue, database

**Claim**:
A precise, atomic assertion or item of directed work issued by one participant against another, carrying the validations that define its satisfaction.
_Avoid_: task, message, request

**Testament**:
The uniform, immutable response to a claim — the closing commit after its artifacts have streamed in. Corrections supersede or amend; they never mutate.
_Avoid_: response, result, reply

**Validation**:
A single atomic means of verifying a claim, paired with a quality bar — an instruction to the evaluator, not a status flag.

**Artifact**:
A piece of typed evidence attached to a testament. Errors are artifacts: failures are reported as evidence, not thrown.

**Delta**:
An immutable fact emitted after a ledger mutation commits — authoritative and self-sufficient, never a hint or a UI decoration.
_Avoid_: event, notification

**Participant**:
Any entity that can issue, receive, or evaluate claims — agent, deterministic service, system runtime, or external actor (user, CI). Wire format and lifecycle never branch on the category.

**Affordance**:
Whether a tool call is legal, derived from graph state: the target's lifecycle precondition and the work node's dependency satisfaction. The response to an unmet affordance is inform or yield — refusal is reserved for structural invariants.

### Runtime

**Lineage**:
The fork tree over a body of work — baseline manifests, fork relations, and its materialization target (a local tree or a source-control ref). Sessions attach to lineage nodes; the lineage outlives its sessions; the materialization lease is lineage-scoped.
_Avoid_: workspace, repo binding

**Session**:
The isolation and namespace unit: an independent workstream attached to a lineage node, born template-stamped (never bare) with its own colocation unit, key root, and pods — nothing inside a session is reachable from another absent a brokered grant. Forkable, mergeable via landing, disposable; proof outlives it in the archive.
_Avoid_: workspace, environment

**Summon**:
A claim requesting allocation of a workload — pods, VFS volumes, permissions, network endpoints, agent assignment, health validation. Issued by an orchestrating agent (the Guide, the autoscaler as system participant), **executed by the scheduler**, gated by Guardian admission validations on the same claim, and monitored and evaluated by its issuer like any work. No agent allocates directly.
_Avoid_: spawn, activate, mint

**Pod**:
The unit of agent placement — a microVM running one agent, with its volumes and network identity. The VM boundary is the isolation guarantee.
_Avoid_: container, process, goroutine

**Soft gate**:
A Guardian check that may deny within bounded, declared rules or request more evidence a bounded number of times, but cannot block indefinitely. Summons and performance-driven handoffs are soft-gated.

**Warden**:
The Guardian's per-pod enforcement daemon — host-side and deterministic — deciding every boundary crossing pre-effect from compiled local policy (SafetyPolicy, role profile, bundle capabilities, active claim scopes). What policy cannot answer is held and escalated; verdicts compile back with provenance. Fail-closed: a dead warden is a frozen pod.

**Sensor**:
The guest-kernel telemetry probe inside each pod, streaming early behavioral signals to the warden. Tighten-only: its signals can narrow a pod's world, never widen it. Silence fails closed.

**Hard block**:
The Guardian's absolute stop authority — over tool and skill invocations, external network calls, excessive pod/resource/VFS allocation, and errant syscalls from within pods.

**Handoff**:
The replacement of an agent instance triggered by context exhaustion or performance degradation. Nothing else is a handoff.
_Avoid_: failover, model swap

**Context handoff**:
A handoff triggered by hitting the context threshold. Scribe-initiated, unilateral, not subject to approval.

**Performance handoff**:
A handoff triggered by degraded performance. The Scribe requests it; the Guardian approves, and may soft-gate by requesting more evidence at most once.

**Failover**:
Switching an agent to its alternate model when its primary provider fails. An operational event driven by config — logged, not a handoff, not ledger state.

**Lease**:
An optimistic, expiring write-basis snapshot used to guide work and skip merge effort where changes are provably disjoint. A work-reduction aid — never a substitute for real conflict detection at the merge.

**Merge gate**:
The single path by which completed work reaches disk. Work streams as increments: each increment's validations pass and it merges into green immediately at machine speed; the claim's whole-work validations — owned by the Arbiter, joined by the Architect where design judgment is needed — gate the disk commit (auto- or user-approved). Failures fix forward via superseding increments — green is never rolled back in place. There is no post-merge audit loop.
_Green_ = increment-validated work; _disk_ = claim-satisfied work.

### Skills

**Office**:
A structural role contract the harness defines — merge-gate evaluator, protection judge, summoner, sidecar narrator — whose consequences are machinery, not personality. The registry binds agents to offices; enforcement attaches to the office, never to its holder.

**Registry**:
The slow plane and the extension surface: the declarative catalog of everything summonable and installable — agents (shipped and custom), skills, tools, MCP servers, provisionable libraries — versioned, content-addressed, Guardian-staged on entry, and resolved into pinned bundles at summon time. Shipped and custom entries differ by publisher and provenance, never by mechanism. Never a runtime authority: it cannot route, gate a transition, or author claims.

**Skill**:
A typed, code-defined capability authored against the harness API and published over MCP as tools plus a `skill://` instructional resource. Never raw markdown at the source. Built-ins are compiled Rust; user skills may be declared via TypeScript/Python bindings, loaded only after Guardian validation.

### Authority

**Rank**:
An agent's per-domain authority ordering, shipped as a static matrix with the harness — not user-editable. A lower-ranked agent may challenge a higher-ranked agent for clarification but cannot override, invalidate, or ignore its feedback. Effective authority is modulated by the agent's tracked performance: a poorly-performing higher rank cannot force compliance.
_Avoid_: hierarchy, seniority

**SafetyPolicy**:
The single user-owned configuration object driving every Guardian gate decision: trust mode, auto-approve ceiling, disk-write mode, network egress. Enabling low-trust drastically lowers the auto-approve ceiling. A config item, not ledger state.

### Agents

**Guide**:
The user's primary conversational agent. Summons and orchestrates all other work and issues work claims; there is no separate orchestrator.

**Arbiter**:
The merge-gate authority and the running sanity check on the cumulative big picture: a continual daemon agent that analyzes work as it merges — quality, coherence, adherence to user directives, robustness, efficiency, performance, correctness — owns whole-work validation at the gate, adjudicates merge conflicts above the author-rebase fast path, and issues unified feedback. Consults the Guide and Architect for intent; may challenge anyone, the user included, with evidence. Writes no code.

**Architect**:
The principal design specialist. Sets direction, produces plan artifacts on demand, incorporates external research, authors corrective actions, and joins merge-gate validation where needed.

**Guardian**:
The system-protection agent. Soft-gates summons (admission control), gates skill/tool invocations with risk-based auto-approval per the SafetyPolicy, hard-blocks threats, and watches resource and VFS health.

**Inspector**:
The adversarial reviewer. Challenges any agent except the Guardian; recommends and pushes back; writes to no system.

**Engineer**:
The sole implementer of code and tests. Submits testaments with artifacts — including the Inspector's approval artifacts where required — against the claims it received; does not merge.

**Archivalist**:
The ground-truth agent: record keeper, code knowledge, and deep investigation (debuggers, profiling, tracing, log ingest). Read-only toward code. Absorbs Sylk's Librarian.

**Scribe**:
The sidecar attached to every other agent: narrates its primary's actions, serves localized history, monitors performance, and initiates handoffs.

**Sibyl**:
The user's workstream agent, above sessions: judges which sessions and experiments should exist — forking variants, stopping generation, arbitrating materialization, brokering cross-fence grants — and touches no work inside any session. Content-blind by default; instances partition judgment by lineage; all authority exercised as user-plane claims.
_Avoid_: steward, orchestrator, session manager

**Designer**:
The on-demand multimodal agent: ingests and produces non-code media, mocks, and wireframes into isolated VFS volumes, outside the merge machinery. Produces A/B variants of non-code outputs for the user to judge. Does not implement code.
