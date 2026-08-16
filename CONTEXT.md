# Hecate

Hecate is a multi-agent coding harness written in Rust. It hosts a fixed roster of agents as microVM-isolated, network-addressable workloads, coordinates their work through a durable claims ledger, and inherits its architecture (not its code) from Sylk.

## Language

### Claims

**Ledger**:
The durable store owning claims, testaments, and their validations and artifacts — and nothing else. Configuration belongs in config; operational events belong in logs.
_Avoid_: board, journal

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

**Summon**:
The Guide's act of allocating a workload: pods, VFS volumes, permissions, and network endpoints, assigning an agent to each pod, and validating health and reachability. Analogous to creating a Kubernetes Deployment. Summons are persisted as claims.
_Avoid_: spawn, activate, mint

**Pod**:
The unit of agent placement — a microVM running one agent, with its volumes and network identity. The VM boundary is the isolation guarantee.
_Avoid_: container, process, goroutine

**Soft gate**:
A Guardian check that may deny within bounded, declared rules or request more evidence a bounded number of times, but cannot block indefinitely. Summons and performance-driven handoffs are soft-gated.

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
The single path by which completed work reaches disk. Work streams as increments: each increment's validations pass and it OT-merges into green immediately; the claim's whole-work validations gate the disk commit (auto- or user-approved). Failures fix forward via superseding increments — green is never rolled back in place. There is no post-merge audit loop.
_Green_ = increment-validated work; _disk_ = claim-satisfied work.

### Skills

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
The user's primary conversational agent. Summons and orchestrates all other work, issues work claims, and validates the resulting testaments at the merge gate; there is no separate orchestrator.

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

**Designer**:
The on-demand multimodal agent: ingests and produces non-code media, mocks, and wireframes into isolated VFS volumes, outside the merge machinery. Produces A/B variants of non-code outputs for the user to judge. Does not implement code.
