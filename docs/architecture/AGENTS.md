# Hecate Agents

Hecate runs a fixed roster of eight agents. There is no dynamic agent registration and no
capability taxonomy: the roster is closed, roles are law, and discovery of "who can do X"
is the Guide's judgment informed by this document's authority model. Every agent is a
workload in a microVM pod (see `SUMMONING.md`), communicates exclusively over the pod
network, and participates in the claims ledger as a first-class participant (see
`LEDGER.md`).

Terminology in this document follows `../../CONTEXT.md`. Where this document and the
glossary disagree, the glossary wins.

## 1. Roster

| Agent | Role in one line | Primary model | Alternate model | Reasoning |
|---|---|---|---|---|
| Guide | The user's conversational primary; summoner and orchestrator | Claude Sonnet 5 | GPT 5.6 Pro Luna | max / ultra |
| Architect | Principal design specialist; research; corrective author | Claude Fable 5 | GPT 5.6 Pro Sol | max / ultra |
| Guardian | System protection: admission, gating, resources, VFS health | Claude Opus 5 (1M) | GPT 5.6 Pro Sol | medium — low-trust raises to max / ultra |
| Inspector | Adversarial reviewer of every agent except the Guardian | Claude Opus 5 (1M) | GPT 5.6 Pro Sol | xhigh |
| Engineer | Sole implementer of code and tests | Claude Opus 5 (1M) | GPT 5.6 Pro Sol | high |
| Archivalist | Ground truth: records, code knowledge, deep investigation | Claude Opus 5 (1M) | GPT 5.6 Pro Sol | xhigh |
| Scribe | Sidecar narrator, history server, handoff initiator | Gemini 3.7 Flash | — | low, narrative-tuned |
| Designer | On-demand multimodal producer (never code) | Gemini 3.7 Flash | — | model default |

Model rules (mechanics in `PLATFORM.md`):

- The user picks the primary per agent; the alternate exists **only** for failover.
  Failover is an in-place swap at a turn boundary, sticky until the current claim reaches
  a terminal state, then reverts to primary. It is logged, never ledger state, and it is
  not a handoff.
- Reasoning effort resolves **per stage, per request**. An agent's headline effort applies
  to its substantive work; internal stages (classification, routing, commentary) are
  pinned cheap in the stage catalog. Sylk lesson: letting a session-level effort override
  leak into routing stages made every message pay a heavyweight call just to be routed.
- There is exactly one authority for model configuration (`PLATFORM.md` §2). Sylk ran
  three contradictory sources; Hecate runs one.

## 2. The authority model: rank

Any agent may **consult** or **challenge** any other agent except the Guardian. The
system is built so agents constantly push each other to do better — an engineer may
challenge another engineer, the Architect may challenge an Inspector. What keeps this
from being chaos is **rank**.

### 2.1 Semantics

- Rank is a **static role × domain matrix**, shipped with the harness. It is not
  user-editable: a user-tuned authority matrix is a misbehaving-system generator.
- A lower-ranked agent may always challenge a higher-ranked agent **for clarification**.
  Clarification challenges bypass rank checks entirely.
- A lower-ranked agent can never **override, invalidate, or ignore** a higher-ranked
  agent's feedback in that domain. An override-shaped testament from a lower-ranked agent
  against binding higher-ranked feedback is rejected by the ledger as a structural
  invariant violation — one of the narrow Refuse cases in the affordance model.
- Rank is **per-domain**, not global. The Archivalist outranks the Engineer on what is
  actually on disk; the Engineer outranks the Archivalist on the intent of its own work
  with respect to what is on disk.
- The user, as an external participant, outranks every agent in every domain.

### 2.2 Performance modulation

A tracked performance score — computed by a harness service (`PLATFORM.md` §6) from
ledger-observable outcomes (validation pass rates, challenge outcomes) weighted by
prevalence, specificity, and trust, with each agent's Scribe as the per-agent signal
source — modulates rank's **bindingness, never its order**:

- A poorly-performing higher-ranked agent's feedback demotes from *binding* to
  *advisory*. A properly-performing engineer is not forced into compliance with a
  failing inspector "just because."
- Order never inverts. No score makes an engineer able to override an inspector; the
  obligation to comply is suspended, not transferred.
- The score is harness state, derived on demand — never stored on the ledger, never
  user-visible as a leaderboard.

The Scribe is deliberately the signal source and **not** the score authority: it
initiates handoffs on the same data, and holding both powers would let one sidecar
manufacture the evidence for its own trigger.

### 2.3 The rank matrix (FINAL — user-approved 2026-08-15)

Rank 1 is highest. The authoring agent's supremacy in the *authorship* domain is
per-claim: whoever authored the work under discussion holds rank 1 there.

| Domain | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| System safety | Guardian | — (unchallengeable) | | |
| Design direction | Architect | Guide | Inspector | Engineer, Designer |
| Code correctness (review) | Inspector | Architect | Engineer | Archivalist |
| Authorship intent (own work) | the author | Inspector | Architect | |
| Ground truth (disk, history) | Archivalist | Engineer | Inspector | |
| Agent-local history | that agent's Scribe | Archivalist | | |
| Multimodal design | Designer | Architect | Guide | |
| User intent & orchestration | Guide | Architect | | |

### 2.4 Mechanics

Consults and challenges are claims (`ActionType: consultation | challenge`), inherited
from Sylk's fabric: parented, deadline-bearing, receipt-validated, with parking/yield so
a consulting turn frees its replica instead of blocking (cyclic consults are legal and
resolved by the claims graph's SCC machinery — `LEDGER.md` §4). A challenge targets an
**activity or artifact with concrete evidence**, never an agent by reputation.

## 3. The agents

### 3.1 Guide

The user's primary agent, and the only orchestration authority — there is no
Orchestrator in Hecate.

- **Summons** all other work (`SUMMONING.md`): allocates pods, volumes, permissions, and
  network; assigns agents; validates health. Summons persist as claims, soft-gated by the
  Guardian.
- **Issues work claims** and **validates the resulting testaments** at the merge gate
  (`LEDGER.md` §6), pulling in the Architect where design judgment is needed.
- Chooses pod composition by judgment, informed by the other agents (it may consult
  before summoning): an architect pod for design conversations, inspector + engineer for
  a bug fix, a lone engineer when the work is simple.
- Absorbs the orchestration machinery: DAG sequencing, dispatch gating, and progress
  tracking are ledger-driven bookkeeping the Guide owns, not a separate agent's judgment.
- Holds no write capability of any kind. Its cheap internal stages (intent
  classification, routing) run at pinned low effort regardless of its conversational
  effort.

### 3.2 Architect

The principal design specialist — deliberately fluid where Sylk's was rigid.

- Produces **plan artifacts on demand**, not as the mandatory output of a protocol. There
  is no plan state machine driving its behavior, no mandatory phase script, no keyword
  bypass, no deterministic fallback planner, and no censor rewriting its prose. Design
  constraints are expressed as validations on plan claims; drift information is computed
  cheaply and *informs* the model rather than gating it.
- **Grills the user**: pushes back on an idea until it is a fully realized system, sets
  direction, and standardizes tooling and library choices across work.
- **Researches**: provider-native web search plus the secured fetch pipeline
  (Guardian-inspected quarantine before any fetched content is citeable or ingested).
  Research papers are artifacts it authors or requests, not a separate agent's product.
- Is the **canonical author of corrective actions**: validation failures and rejections
  converge on the Architect, which authors fix claims. Monitors do not author fixes.
- Joins merge-gate validation where the Guide needs design judgment; recommends and
  assigns work to other agents via routed-work claims; gives feedback and answers
  implementation questions with design-direction rank.

### 3.3 Guardian

System protection with agentic intelligence — an armed advisor with real stop authority,
not a bank of dumb gates, and equally not "purely advisory."

- **Soft gates** (bounded, declared rules; may request more evidence a bounded number of
  times, cannot block indefinitely): summon admission — known agent type, sane resource
  ask, anti-DoS (a K8s admission controller in spirit) — and performance handoffs (one
  evidence request maximum).
- **Hard blocks** (absolute): tool and skill invocations, external network egress
  (enforced at the host network stack every guest packet traverses), excessive
  pod/resource/VFS allocation, and errant syscalls from inside pods (enforced by the VM
  boundary and the device surface the Guardian polices).
- **Skill/tool gating** is risk-analyzed and auto-approvable per the user's
  `SafetyPolicy` (`PLATFORM.md` §1). Low-trust mode drastically lowers the auto-approve
  ceiling and raises the Guardian's own reasoning to max/ultra.
- Operates the **three substrate gates** (`SUMMONING.md` §6): provision (full transitive
  closure + provenance inventory before any bytes are fetched), sandbox capability
  (verdicts include APPROVED_WITH_CAVEATS — capability downgrade, not just allow/deny),
  and disk fallback. Policy lives in Guardian configuration; the substrate is mechanism.
- Watches **resources and VFS health**: memory budgets, pod spin-up rates, volume
  allocation, quarantine state. In Sylk the resource machinery existed and the guardian
  was never wired to it; in Hecate the Guardian is its primary consumer.
- Every Guardian decision is expressed on the ledger as a validation on the claim it
  gates — there is no separate approval envelope. Every gate decision cites the
  SafetyPolicy field it applied.
- The Guardian cannot be challenged and appears in no challenge target list.

### 3.4 Inspector

The adversarial reviewer. Its job is to poke holes: in implementations, designs,
approaches, and hypotheses — of any agent except the Guardian.

- **Writes to no system.** No workspace writes, no VFS volume writes, no merge or
  finalization verbs, no side-effecting execution. This is structural (the write skills
  do not exist in its pod), not prompt discipline. Sylk's global inspector held
  `workspace_write` and the pipeline inspector held the terminal merge verbs; Hecate
  closes both.
- Reviews with evidence: challenges cite the activity or artifact at fault and carry
  concrete findings. Its approval artifacts ride the Engineer's testament into the merge
  gate; its analysis is binding per rank (code-correctness rank 1), subject to
  performance demotion like everyone else.
- May comment on pull requests through an external, Guardian-staged MCP integration —
  commentary is its one outward-facing act, and it is not a write to any Hecate system.
- Runs read-only analyzers and analysis execution; test *execution* belongs to the
  Engineer.

### 3.5 Engineer

The beating heart: implementation and test in one agent.

- **Sole writer of code**, including test code — Sylk's Tester is absorbed. The red/green
  discipline is internal and streamed: failing-test increments, then implementation
  increments, through the streaming merge gate (`LEDGER.md` §6).
- Writes through leased-basis VFS skills into its pod volume. Leases are guidance and
  work reduction (provably disjoint changes skip merge effort) — never the conflict
  authority; the OT merge detects conflicts for real.
- Submits **testaments with artifacts** — including the Inspector's approval artifacts
  where the claim requires them — against the claims it received. It does not merge and
  does not touch disk; the merge gate does.
- Obeys the Architect, Guardian, and Inspector absolutely, as rank makes structural: it
  satisfies the exact constraints those agents set, enacting their feedback and the
  user's to the highest degree. Its own rank 1 is authorship intent — it is the authority
  on what its work *means*.
- Toolchain (compilers, linters, test runners, LSP) lives in its guest image and runs
  against the guest mount; tool provisioning rides the substrate with Guardian gates.
- Engineers may consult and challenge other engineers; multi-engineer summons are
  legal and expected for parallel work, with claims scoping and OT keeping them honest.

### 3.6 Archivalist

The ground-truth agent — Sylk's Archivalist and Librarian married into one purpose:
determining what is actually true, whether in an external repo, local code, or Hecate's
own history.

- **Record keeper**: ingests events, maintains chronology, highlights important events,
  informs of changes, serves cross-session and cross-agent history.
- **Code knowledge**: repository search, symbol graphs, repo briefs, package cloning
  (its one deliberate write exception, to its own package store) — the fleet's most
  consulted agent.
- **Deep investigation**: debuggers, memory profiling, tracing, log ingest and parsing —
  typed skills over local instruments in its guest image. This is what gives "ground
  truth" teeth beyond search.
- Read-only toward code by role, with explicit per-view reads (disk / green / pipeline)
  so layer confusion is impossible.
- For "what has agent X been doing lately," agents are taught that X's Scribe likely has
  the freshest answer — the Archivalist is the authority for anything beyond a Scribe's
  window. This is prompt discipline, not a routing law.

### 3.7 Scribe

A sidecar attached to **every other agent** — eight primaries, each with its Scribe.

- **Narrates**: a running, structured account of its primary's actions, successes,
  failures, and outputs, streamed to the Archivalist and the fabric.
- **Serves localized history**: peers consult a Scribe directly for its primary's recent
  activity; the Scribe answers from its window and hands off to the Archivalist beyond
  it.
- **Monitors performance**: consumes the health plane's per-agent signals
  (`PLATFORM.md` §5) and is the per-agent signal source for the performance score.
- **Initiates handoffs** — the empowerment Sylk's read-only scribes lacked:
  - *Context handoff*: the primary hit its context threshold. Scribe-initiated,
    unilateral, no arguing.
  - *Performance handoff*: the primary is degrading or acting against user intent. The
    Scribe submits the request to the Guardian, which may soft-block by requesting more
    evidence exactly once — it cannot outright block a performance handoff.
- Carries continuity across the swap: the successor inherits the predecessor's UID chain
  and a "previously, on this agent" narrative digest.
- Writes to no system except its own narration stream and the Archivalist's intake.

### 3.8 Designer

The on-demand multimodal agent — what lets Hecate understand more than code.

- Summoned by the Guide specifically for multimodal work: ingesting and analyzing audio,
  video, and images; generating mock UIs, wireframes, visual examples; assessing
  accessibility on actual rendered output.
- **Does not implement code.** Engineers do. The Designer's output is non-code media and
  design artifacts.
- Operates **outside the merge machinery**: output is isolated to its VFS volumes, never
  versioned through OT. When input/output size exceeds what its volume budget allows
  (a derived threshold, never a literal constant), it must seek Guardian approval before
  disk ingest or output, through quarantine-style staging — "approved to exist on disk"
  and "approved to enter the workspace" are two separate decisions.
- **A/B testing** is its signature move: N variants of a design, visualization, or mock,
  presented for the **user** to judge. Agent assessments (accessibility, token
  consistency) attach to variants as advisory validations; the user's choice is recorded
  as a testament.

## 4. What no agent gets

- **Dozens of tools.** Each agent surfaces a small handful of well-worded skills: the
  shared fabric façades (claims, consult/challenge, history) plus its role façades, with
  progressive disclosure behind them (`SKILLS.md` §5). Sylk's architect surfaced 31
  tools in its first turn; that number is the cautionary tale.
- **A second workflow authority.** All work coordination is ledger truth. No agent's
  synchronous reply, progress text, or route response completes work.
- **Ledger access for non-ledger things.** Config is config, operational events are
  logs. The ledger is claims, testaments, validations, and artifacts — nothing else.
