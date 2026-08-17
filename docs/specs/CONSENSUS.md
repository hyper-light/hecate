# SPEC: consensus — the commit authority

Status: ACCEPTED 2026-08-17 (direction ratified after the etcd challenge was
answered by the layer-classification dossier; spec accepted with three delta
sets worked in-exchange: split-brain assembly + fabric law, actor-architecture
position, cross-region). Amendments carried: (2a) CRDB-lineage exemplar
naming; (2b) bug-record-as-conformance-suite; (3-addendum) conf-change
activation semantics + #12359 countermeasures; (5a) deterministic
whole-cluster simulation (in `FAULTS.md`). Consumed by: WAL §5 (the sole
commit path at every replica count), SERVING §6 inventory map, OBJECT_TIER §4
placement map, SCHEDULER §1 meta group, REGISTRY §5 replicated revision,
LEDGER_CORE §2 append API. Resolves most of Branch 27 by construction (§6).
Companion: `FAULTS.md` (fault scope, dispositions, nemesis matrix, the
simulation gate).

## 1. Topology: the meta tree + N per-session groups

**The failure-domain tree is first-class**: node < AZ < region, discovered at
boot and versioned in the inventory map. Placement, quorum spread, and meta
authority are all expressed against this tree. A laptop is a depth-one tree
with a single leaf — every collapse below is tree-derived, never a mode.

- **The meta tree — one meta group per level of the tree that exists.**
  The **root group** (spans regions; low-rate, latency-tolerant) owns the
  region directory, cross-region placement policy, root-scoped refs (lineage
  heads, registry publications), and root-scoped epochs. **Per-region
  groups** own the region's host-inventory map, the region's session-group
  directory, region-scoped epochs/leases, and the region's durable-plane
  copyset map. Same core, same code at every level; on a laptop
  root ≡ region ≡ one group. Every fencing token and writer epoch in the
  system is minted by exactly one meta-tree group per §6's scoping law.
  Group membership, configuration, and reconfiguration live as ordinary
  committed records in the owning directory (the Delos VirtualLog shape:
  reconfiguration is data in the control plane, never a side protocol).
- **Session groups** (one per session) own that session's WAL commit — the
  per-session logical logs of WAL §5. Independent commit order, independent
  failure domain; a wedged session group harms exactly one session.
- **The colocation law extends to consensus**: a session's consensus group is
  part of its colocation unit — replicas placed within the session's region,
  spread across its interior failure domains (AZ/node). **No synchronous WAN
  round-trip exists on any session hot path** — WAL commit, serving, merge
  gate, warden verdicts (Physalia's placement principle as law: consensus
  colocated with the failure domain of the resource it governs).
- **Liveness is amortized to node level — no per-group heartbeats exist,
  ever.** Nodes participate in one **node-liveness fabric** per region: each
  node claims support once per derived interval with a claim that is
  **disk-write-backed** (a node with a stalled disk cannot claim support —
  CRDB's gray-failure detection, adopted as law). A session-group leader's
  authority is fortified by its node's current support epoch: it cannot lose
  leadership while support holds and loses it deterministically when support
  lapses. Idle groups tick nothing, send nothing, cost nothing — designed
  in, not retrofitted (TiKV #10017 is the named retrofit regression; CS11).
- Group placement/rebalancing is a scheduler concern executed via meta-tree
  reconfiguration records; this spec owns only the record semantics.

## 2. The core: Raft, CRDB-lineage dialect, pure

- **One pure algorithmic core**, used by every group at every tree level
  identically. Exemplar = the etcd-raft interface shape as extended by
  cockroachdb/raft (amendment 2a); tikv/raft-rs is the Rust-portability
  proof. **Exemplars, never dependencies** — the core is ours, in our
  runtime, under our lint wall, with zero etcd/CRDB/TiKV code.
- **IO-as-data, deterministic**: the core is a state machine
  `step(Message) → {outbound: Vec<Message>, to_append: Vec<Entry>,
  state_delta}`. Same state + same input ⇒ same output, always. Time enters
  only as logical `Tick` messages; election randomization is seeded and
  injected. No clock, no channel, no IO inside the core — this is what makes
  `FAULTS.md` §4's whole-cluster simulation cheap; the two are one design.
- **AsyncStorageWrites shape from day one**: storage and network effects
  leave the core as request messages and return as response messages (the
  interface CockroachDB authored for exactly our scale; 28% latency receipt
  on file). There is no synchronous Ready/Advance path to deprecate later.
- **Two persistence laws, spec-level, conformance-gated** (the v3.5 class
  made unrepresentable):
  1. **Entries-then-HardState**: log entries are durable before the
     HardState (term/vote/commit) that references them.
  2. **No message emission before covering durable state**: no vote, no
     append-response, no commit advance leaves the node before the state
     that justifies it is durable. The host's applied/durability watermark
     advances **inside the same transaction** as the applied effects — never
     a shared mutable index a background commit can race (the exact v3.5
     mechanism, named).
- **The actor position, owned**: this core *is* the actor model in its
  disciplined form — `step(Message)` actors with single-owner state and
  message passing only, as are the runtime's sharded single-owner tasks.
  Five Akka-style laxities are refused, each by standing doctrine: unbounded
  mailboxes (bounded queues + credit are law), untyped messages
  (hecate-wire is the only wire), supervision-as-blind-restart (panics are
  evidence testaments; restarts are typed lifecycle), location transparency
  that hides failure (failure is typed and loud), fire-and-forget delivery
  as the default contract (delivery semantics are per-plane and witnessed
  where it matters). Akka cluster-sharding's role — huge entity populations
  with liveness amortized above the entity — is played by session groups
  over node liveness, in consensus-grade form.

## 3. Elections, liveness, and reads

- **PreVote AND CheckQuorum together, always** — either alone has a proven
  liveness hole (Decentralized Thoughts omission analysis; the Cloudflare
  6-hour outage as the production case). Both are on unconditionally; there
  is no configuration to get wrong.
- **Leadership transfer bypasses PreVote** — the documented carve-out,
  adopted explicitly (the transfer target must win immediately despite a
  healthy leader); CS6 asserts transfers complete under active CheckQuorum.
- **Fortified leadership** (§1): a leader supported by the node-liveness
  fabric ignores election timeouts from partitioned minorities; every
  step-down path (support lapse, explicit transfer, joint-config exit)
  de-fortifies explicitly (CRDB #129098's bug class; CS12).
- **Reads: ReadIndex only, v1.** A read is serviced at or above a commit
  index confirmed by the current leader's quorum round. Learners are
  first-class ReadIndex clients (CS4). **Lease reads do not exist**: they
  import a wall-clock axiom the doctrine bans; if fortification later makes
  local reads provable from the support fabric alone, that arrives as its
  own spec amendment with its own proof obligations — never as a flag.

## 3b. Split brain, structurally

Split brain is four distinct attacks; each dies at a named layer:

| Attack | Layer that kills it | Test |
|---|---|---|
| Two leaders committing in one group | Quorum intersection — coexisting leaders are in different terms; the older term cannot commit (its quorum overlaps the new one). Raft's core theorem; needs no liveness help | CN1 |
| Zombie leader serving stale reads | ReadIndex-only (§3) — every read needs a quorum confirmation a deposed leader cannot get. This is why lease reads were rejected | CN10 |
| Paused-and-resumed standing writer | Epoch fencing enforced **at the resource** (§6) — the split brain no consensus algorithm sees, closed where it happens (Kleppmann's argument; ZippyDB's shipped shape) | CN8 |
| Actors on stale topology | Versioned, fenced, epoch-consumed maps (SERVING §6, OBJECT_TIER §4) — stale-epoch writes refused by the same token discipline | CN12 |

**The fabric law**: **the node-liveness fabric is liveness-only; no safety
property depends on it.** Fortification defers elections and amortizes
heartbeats — it never authorizes a write, a read, or a commit without the
underlying quorum. Worst-case arbitrary fabric misbehavior (contradictory,
stale, withheld, or forged-within-scope support claims) degrades election
latency and nothing else (CN11). This is deliberately stronger than CRDB's
Leader Leases, which put the fabric on the read-safety path to earn local
reads; having declined lease reads, we keep the fabric off the safety path
entirely — the named spot where a future "optimization" would quietly
reintroduce the hole.

**Rejected-alternative record**: heuristic split-brain resolvers exist only
where membership lacks a quorum authority. Akka Cluster's AP-gossip
membership required deprecating `auto-down` after production split brains and
shipping the SBR heuristic menu (keep-majority/static-quorum/keep-oldest/
down-all, each with documented wrong-decision scenarios) — whose most robust
strategy, lease-majority, acquires a lease from the Kubernetes API, i.e.
borrows etcd; Elasticsearch's Zen `minimum_master_nodes` split brains
(Jepsen-documented loss) were fixed only by the 7.x Raft-style rewrite. With
Raft-owned membership the quorum *is* the resolver — deterministic, not
heuristic — and the both-sides-running window SBR concedes is exactly what
layer-3 fencing closes. This design never enters the regime where a resolver
is needed.

## 4. Reconfiguration

- **Joint consensus for all voter-set changes.** Single-server fast paths
  are permitted only with **Ongaro's guard as law**: a leader may not
  propose any configuration change until it has committed an entry (the
  term-opening no-op) in its own term (CS7).
- **Learners with promotion gating**: new members join as learners;
  promotion requires a derived catch-up threshold (lag below
  `k × append_batch`, derivation at the definition site); **voters are never
  demoted directly — demotion routes through learner** (half of the #12359
  countermeasure, API-level unrepresentable).
- **Activation semantics: apply-time, with the countermeasures as law**:
  the dialect's apply-time semantics keeps one apply path — configuration
  changes flow through the same committed-then-applied machinery as all
  state, preserving the pure-core interface; append-time would diverge from
  both exemplar forks and forfeit their fixes' conformance value. The
  #12359 hole is closed structurally: **vote and pre-vote messages carry
  conf-commit metadata** (index/term of the sender's latest committed
  configuration), making promoted-but-unaware voters and
  demoted-but-unaware quorums detectable (CS1).
- **Reconfiguration is data** (§1): every membership change is a committed
  record in the owning group and mirrored as a directory record in its
  meta-tree parent; recovery and observers replay records — no out-of-band
  membership truth exists.

## 5. Log storage boundary

- The core sees an abstract log; the host owns storage using WAL.md's
  measured durability primitives over a **dedicated log store**
  (raft-engine's lesson: consensus logs are append-heavy, prefix-truncated,
  group-multiplexed — not general KV). No mmap-whole-DB, no stop-the-world
  maintenance (the boltdb anti-patterns, named).
- **Truncation and snapshots are host-owned** with slow-vs-dead follower
  discrimination (CRDB tech note): a slow follower holds truncation within
  a derived debt bound; a dead one (node liveness says so) releases it.
  Snapshot transfer rides the transfer plane (`TRANSFER.md`) — chunked,
  verified, resumable; never a bespoke path.
- Applied-state checkpoints and log prefixes retire together under the
  checkpoint-retention invariant (no prefix drops while any recovery path
  needs it).

## 6. Single-writer subsystems (Branch 27, resolved by construction)

- **CAS-first**: where the commit is one ref swap and writers are
  intermittent — registry refs, generation pointers, landing heads,
  placement-map versions — there is **no election and no lease**:
  election-free CAS on the consensus-backed ref (`set_ref_if`), with the
  Lance-style outcome classification (rebasable / retryable / conflict) as
  the typed result.
- **Standing writers** — merge serializer, ledger sequencer, and any future
  open-write-stream holder — hold a **meta-tree lease in Chubby's
  coarse-grained shape** (keepalives, grace period) **plus an epoch fencing
  token enforced at the resource** — non-negotiable, because a
  paused-and-resumed writer defeats any lease alone (§3b layer 3). Every
  write the resource accepts checks the token; a stale token is a typed
  refusal.
- **The epoch-scoping law**: an epoch/fencing authority lives in the
  **smallest failure domain that contains every legal holder of the fenced
  resource**. A merge serializer's holders all live in the session's region
  ⇒ region-group epoch — if the region dies, resource and authority die
  together, so no resurrection is possible. Lineage heads and registry
  publications have holders anywhere ⇒ root-group epochs, WAN-committed —
  acceptable because those are human-cadence CAS operations.
- Boot validates the roster: every subsystem is classified CAS-first or
  lease+fence with its epoch scope; an unclassified writer fails startup
  (chokepoint law). Branch 27's remaining scope = auditing this roster
  against the actual subsystem list at build time.

## 7. Cross-region

**Evidence provenance (honest, per doctrine)**: FlexiRaft's region-local
commit window is PRIMARY (CIDR'23, on file in the Branch-20 dossier); the
Physalia placement principle, Spanner leader-placement practice, Chubby's
global-cell shape, and the async geo-replication pole (S3 CRR, DynamoDB
global tables) are established literature **not re-verified this session**;
the epoch-scoping law and the no-session-failover derivation are OWN
SYNTHESIS from those principles plus our accepted loss formula. A
verification research pass is in flight (2026-08-17); a refuting finding
reopens this section — until it lands, §7 is ratified direction with
receipts pending confirmation.

- **Session groups never span regions** (§1 colocation law). Intra-session
  durability is region-interior quorum; cross-region durability is the
  durable plane's job.
- **Cross-region durability is asynchronous and content-only**: sealed
  immutable content replicates cross-region per root placement policy
  (copysets against the failure-domain tree) — no consensus per chunk,
  verification intrinsic to content addressing (the S3-CRR/global-tables
  pole, which is correct precisely because our cross-region objects are
  immutable).
- **Sessions do not fail over across regions.** A region loss kills its
  sessions; sealed/landed work survives in the durable plane; sessions
  re-summon from lineage + archive elsewhere. Unlanded work in the lost
  region is the existing bounded loss class — OBJECT_TIER §3's formula
  verbatim with `correlated_event_rate` = region-loss rate and
  `exposure_window` = seal→cross-region-replication lag — re-derivable by
  agent effort, user-visible, never existential. Live cross-region failover
  is rejected: it would put WAN in the hot path to defend against an event
  the loss formula already prices.
- **FlexiRaft-style flexible quorums are rejected for the meta plane**: a
  region-local commit window on epoch state can lose the latest mints on
  region failure, and fencing safety rests on epoch monotonicity. The
  epoch-scoping law makes them unnecessary: state only region-local actors
  touch is region-scoped to begin with; genuinely global state commits on
  a global quorum at human cadence. (Recorded as compatible future work
  only if a latency-sensitive, genuinely-global write class ever appears.)
- Region partition consequences are enumerated and closed: everything
  region-local is unaffected (that is the point of §§1/6/7); root-group
  operations from a minority region stall (cross-region placement changes,
  root-ref CAS, global publications — all human-cadence). **Nothing on any
  session path may appear in that stall list** — an architecture test
  (CN13), not prose.

## 8. The laptop degenerate

A 1-voter configuration of the same core on a depth-one failure-domain tree —
no mode, no branch: quorum ack degenerates to own durable append (WAL §5
unchanged); root ≡ region ≡ one meta group; the fabric is one node
supporting itself; cross-region machinery is inert because the tree has no
second region. **The N=1 crash-injection gate is specific and permanent**:
the v3.5 corruption showed *no symptoms* in single-replica mode, so the §2
watermark-atomicity law is CI-gated under crash injection at N=1 explicitly —
the configuration where the bug class hides is where we hunt it.

## 9. The conformance suite (amendment 2b — the bug record as executable tests)

Named, permanent, seed-replayable in SIM; each cites its source:

| # | Test | Source |
|---|---|---|
| CS1 | #12359 leaderless scenarios (promoted-unaware voter; demoted-unaware quorum) fail without conf-commit metadata, pass with it | etcd #12359 (closed stale) |
| CS2 | Isolated node with smaller term rejoins and catches up (no PreVote stuck-state) | etcd #8243 |
| CS3 | Higher-term/lower-index replica never wedges an election | etcd #8501 |
| CS4 | ReadIndex from a learner is serviced | etcd #10589 |
| CS5 | Probe/reject/hint exchanges converge; no leader-follower stall loop | etcd #13418 |
| CS6 | Leadership transfer completes under active PreVote+CheckQuorum (bypass carve-out) | dialect raft.go |
| CS7 | Concurrent single-server changes across a term boundary cannot commit through non-overlapping quorums (Ongaro guard) | raft-dev 2015 |
| CS8 | The omission matrix: partial connectivity, leader-cut-from-majority, per-link asymmetric partitions each reach stable leadership in bounded elections | Decentralized Thoughts; Cloudflare/HAOC'21 |
| CS9 | Entries-then-HardState: crash between the two ⇒ recovery never observes HardState referencing missing entries | §2 law 1 |
| CS10 | Watermark atomicity: crash at every point in apply ⇒ no committed entry ever skipped on recovery, at N=1 and N=3 | v3.5 postmortem |
| CS11 | Idle-group correctness: an idle group reports true peer state through node liveness (no false down-peers) | TiKV #10017 |
| CS12 | De-fortification on every step-down path (support lapse, transfer, joint-config exit) | CRDB #129098/#135078 |

## 10. Test matrix (beyond conformance)

| # | Test | Catches |
|---|---|---|
| CN1 | Linearizability over randomized workloads under the full FAULTS.md nemesis matrix, meta tree + session groups | safety, whole-system |
| CN2 | Idle-cost ratchet: N idle session groups ⇒ measured ~zero ticks/messages/CPU (bounded by the fabric interval alone) | per-group liveness creep |
| CN3 | Stalled-disk node cannot claim support; its groups elect elsewhere within the derived bound | gray failure |
| CN4 | Membership churn fuzz: joint entries/exits, promotions, crashes mid-change ⇒ exactly one committed configuration lineage | reconfiguration divergence |
| CN5 | Determinism: same seed + inputs ⇒ byte-identical core outputs across platforms | SIM validity; the REAL≠SIM class |
| CN6 | Truncation-vs-slow-follower: debt-bounded retention; dead follower releases; recovery snapshot-fills via TRANSFER.md | log-retention deadlock/leak |
| CN7 | CAS-first subsystems under contention: outcome classification exact; no livelock; no hidden election on the path (architecture test) | machinery creep |
| CN8 | Fencing: paused-and-resumed lease holder's writes refused at the resource by token, under maximal pause fuzz | the Kleppmann class |
| CN9 | 1-voter ≡ N-voter observable semantics for every client-visible API (differential test) | laptop-vs-fleet drift |
| CN10 | ReadIndex freshness: a read never returns state older than any write acked before it, under partition fuzz | stale reads (the k8s #59848 class) |
| CN11 | Fabric-fault injection: arbitrary support-claim corruption (contradictory/stale/withheld/forged-within-scope) ⇒ linearizability holds unconditionally; only election latency degrades, bounded and measured | the fabric law (§3b) |
| CN12 | Stale-epoch actor: any actor holding a superseded epoch (map version, lease token, key epoch) has every write refused at every resource; fuzzed across all epoch kinds | topology split brain |
| CN13 | Region partition: every session-local operation unaffected; the root stall list exactly matches §7's closed enumeration (architecture test) | WAN leaking into hot paths |
| CN14 | Region loss: unlanded-work loss ≤ the OBJECT_TIER §3 formula's bound at measured replication lag; sessions re-summon from lineage + archive with sealed work intact | the loss class drifting from its price |

## 11. Acceptance criteria

1. No per-group heartbeat, tick, or timer exists for idle groups (CN2
   ratchet, permanent).
2. §2's two persistence laws hold under crash injection at every N, N=1
   named (CS9/CS10 CI gates).
3. PreVote+CheckQuorum are unconditional; no flag can disable either.
4. All CS1–CS12 green before the core carries its first real commit; the
   suite is append-only.
5. Voter demotion is unrepresentable except via learner (API-level).
6. Every single-writer subsystem is classified at boot with its epoch scope;
   unclassified fails startup.
7. Wall-clock appears nowhere in the core or its correctness arguments
   (architecture test).
8. The core has zero etcd/CRDB/TiKV code; exemplar provenance is doc-only.
9. **The fabric is deletable**: no safety property, proof argument, or test
   oracle references the node-liveness fabric — removing it from the model
   leaves every safety test passing (architecture-level check; CN11 is the
   dynamic form).
10. No synchronous WAN round-trip on any session hot path (CN13 permanent);
    epoch authorities placed per the §6 scoping law, boot-validated.
11. Meta-tree depth is derived from the failure-domain tree; no
    region/laptop mode flag exists anywhere (architecture test).
