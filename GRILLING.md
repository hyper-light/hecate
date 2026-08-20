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

**Status-honesty correction (2026-08-17, C-7 audit)**: file headers are the
single status authority; this table is an index. The audit found the table
over-claimed — the following rows are **DIRECTION-SETTLED ONLY (whole-spec
verdict owed; headers honestly say "presented")**: PROTOCOL
(Br 3) — **acceptance exchange OPEN 2026-08-17, held on the
class→transport question**: the audit's six amendments (fencing authorities
under the meta tree, HLC liveness-only, no-panic P7 fix, D-7 LEDGER/ADR-0002
reconciliation, D-8 grants→Branch 25, cluster-SIM + layer note) were
presented; the user then surfaced (1) the audit's real gap — the spec never
states the class→transport mapping — with the Serf/Consul lineage
clarified (correction recorded: Consul rides SWIM probes on UDP but Raft
RPCs + anti-entropy on TCP), and (2) the load-bearing challenge: bulk/
multi-media (class 6) arguably belongs on UDP — content addressing voids
the ordered-stream guarantee (TRANSFER's "assembly is by manifest, not
arrival"), so TCP HOL blocking is pure cost; missing-set = retransmit;
receiver-granted credits ≈ Homa-shaped receiver-driven pacing (the
published incast answer); the hard wheel = owning congestion control.
Research dispatched (Homa/NDP/QUIC-RFC9002/storage-plane practice/incast-CC
+ three-architecture reconciliation vs TRANSFER/PROTOCOL §4/FAULTS/
cross-region). MERGE (Br 4), VFS (Br 5), PODS (Br 6), AGENTS_RUNTIME
(Br 7), RANK (Ex 8), SCHEDULER (branch mislabeled "21" — C-6). WAL (Br 2):
**ACCEPTED 2026-08-17** ("amend and accept" — five audit amendments:
consensus-substrate clause (per-GROUP logical logs incl. meta tree, raft
record kinds, entries-then-HardState by append order, prefix-truncation
API w/ debt bound); FAULTS §2 disposition conformance
(rebuild-from-quorum when replicated, refusal = N=1 disposition,
universal-refusal path deleted); checkpoint ownership (WAL owns the floor
API only; clients own cadence/format); hecate-wire payload law +
CRC-is-transport-integrity-never-identity clause; cluster-SIM extension +
Branch 25 encryption-at-rest interlock flagged; W9–W11, criteria 8–9). RUNTIME (Br 1):
**ACCEPTED 2026-08-17** ("amend and accept" — five audit amendments: Driver
cancellation surface w/ guaranteed-completion semantics; the NO-PANIC LAW
(user: "we do NOT panic. Period. Ever." — clippy wall, typed errors
everywhere, panic=abort every profile, no catch_unwind anywhere,
binary symbol scan; LEDGER_CORE catch_unwind clause reconciled same
commit); task-lifecycle law (no untracked tasks, ownership-tree teardown,
admission-at-spawn); cluster-SIM clause (N simulated nodes, FAULTS §4
consumer contract); provider egress corrected to §5 external-boundary law —
ALPN h2-primary/1.1-fallback OWNED client (user pushback + Bedrock
h2-default receipt; "low-count streams" premise conceded wrong for a
multi-agent node) routed through the provider-gateway chokepoint w/
CONSENSUS §7 epoch check; T9–T13, criteria 8–11). Also verdict-owed outside this table: OBJECT_TIER (presented; §9 +
two-planes ratified), FOREST (provisionally directed; D-4), VECTOR_INDEX
(header over-claims ACCEPTED — the one reverse mismatch; D-9). Genuinely
accepted with user verdicts on record: SERVING, SESSIONS, LEDGER_CORE,
AUTOSCALING, REGISTRY v2, SKILLS_API, HEALTH, SIBYL, WIRE_FORMAT+TRANSFER,
CONSENSUS+FAULTS, OBJECT_TIER §9 (D-3).

| Spec | Content anchor |
|---|---|
| `docs/specs/RUNTIME.md` | own sharded async runtime, deterministic-by-construction, SIM driver, no-Arc/arena doctrine, io_uring day-one, lint wall |
| `docs/specs/WAL.md` | per-session logical logs over derived-ω streams, always-full durability, chained CRC + torn/corrupt discrimination, consensus-API-only commit path |
| `docs/specs/PROTOCOL.md` | dual-stack UDP/TCP, per-pod HKDF keys + AAD headers, HLC64 + 24B fencing, counter nonces, credit delta streams, hecate-wire (Rust-only, canonical-or-reject, compiler-enforced evolution). §6 process gate SATISFIED 2026-08-17 (WIRE_FORMAT.md written); §4 amended with the four flow-control clauses (stream+connection credit, absolute-offset credits, BDP-autotuned k×frame_cap windows + never-whole-object-in-credit, bulk delivery class) |
| `docs/specs/WIRE_FORMAT.md` + `docs/specs/TRANSFER.md` | ACCEPTED 2026-08-17 ("accepted for the sake of output"): one-value-one-encoding + rejection clause + negative vector per rule; LEB128 minimal-form, canonical NaN, no −0, canonical-encoding-ordered maps; two length domains as types (FrameLen frame-cap-bounded, ContentLen u64 — codec never binds content size; carriers follow bounds); ContentRef{root,len,class} with chunking-independent BLAKE3 tree root; ContentClass = chunking-policy AND verification-structure selector (class-aligned law: CDC → manifest of standalone chunk hashes; media → whole-blob tree + bao outboards for the three root-only cases); inline-vs-reference derive law (no unbounded bytes in ledger-content types); ancestor-hash evolution, trybuild-gated; WF1–WF10. Transfer: scoping theorem (addressed path = zero state, TR9); upload = offer → missing-set (batch_exists = dedup fast path, duplicate upload = zero bytes) → parallel verified streams (16 KiB derived groups, length untrusted until final group) → atomic ref-CAS (orphans nothing); ingest machine OPEN→STAGING→COMMITTING→COMMITTED with staging pack role (OBJECT_TIER §2 third role, lease-reclaimed, never placement-eligible), three witness rungs, chunking-at-commit determinism (TR3/TR10); bounds = formulas then carriers (max_content_len = manifest arithmetic; parts_cap BDP-clamped); TR1–TR10. Branch 26 narrowed to content policy |
| `docs/specs/MERGE.md` + ADR-0005 | canonical rebase + pure deterministic verdict, byte-exact intervals on declared ops, reject-to-corrective, Arbiter gate + frontier service, no LLM in serializer |
| `docs/specs/VFS.md` | one BLAKE3 CDC chunk store, manifests as layers, four volume roles (work volume/green/tools/scratch — scratch added by SERVING.md), virtio-fs serving, tool plane + 3 Guardian gates, content-addressed distribution |
| `docs/specs/PODS.md` | microVM pods, manifest-projection rootfs + DAX day-one all platforms, hecate-init 5 duties, warden+sensor (§6), warm tiers + reseed-on-resume, autoscaling classes (§4b; Architect=serialized-judgment), NO work-bearing memory ever persisted |
| `docs/specs/AGENTS_RUNTIME.md` | serial turn/instance, park-on-consult AND long tools, hold-teardown at human latency, brief+claims handoff (volume re-binds; no transcript), warden-topology skills, R-series |
| `docs/specs/RANK.md` | domain enums, derived bindingness, override-refuse as sole enforcement, score service (prevalence/specificity/trust, demote-only, observe-first). A1–A5 applied to LEDGER.md (single vocab; closed enums+bijection; retirement=custody transfer to Archivalist archive, anti-tombstonic; deadlines as replay inputs; layered scope map) |
| `docs/specs/SCHEDULER.md` | sharded deterministic evaluation-log spine; **deterministic optimism** (parallel intent-aware speculative planners, logged outputs, serial pure applier); content-keyed memoization + snapshot-page/chunk locality scoring; gang-at-admission; Borg bands, hard limits; §9b request lifecycle (amendment=supersession-with-reuse; disposition-retry partials; issuer judges sufficiency) |
| `docs/specs/SIBYL.md` | the 10th agent (name user-ratified): workstream judgment above sessions, lineage-partitioned instances (never global), judgment/machinery split, experiment-as-claim-tree, content-blind, grant brokering (Biscuit), user-plane ledger. AGENTS.md + glossary landed |
| `docs/specs/SERVING.md` | the serving machine (Branch 21, ACCEPTED 2026-08-16): two-representation law (per-pod log-structured overlay = journal + extent index; manifests-over-CAS everywhere else), ack=witness (group commit before reply, no fsck — recovery is replay), seal at increments (writeback drain → op-log derivation → CDC/BLAKE3 → CAS), green = manifest chain (extends never writes, EROFS structural, all-DAX shared pages, pin+re-bind), inode law (volume,path-entry stable per volume lifetime, serializable for handoff), digest-xattr honesty, weighted-HRW topology (chunk-groups + exception table, state-follows-compute, R_eff loud degenerate), mapping engine splice\|managed per platform, own FUSE-over-virtio layer on hecate-rt in the libkrun fork, scratch volume role. Riders landed: VFS.md (4th role + op-log clause), ADR-0005 amendment (one law: no auto-resolution anywhere; dispositions by author liveness), CONTEXT.md (Landing, Conflict value, Witness, Seal) |
| `docs/specs/SESSIONS.md` | ACCEPTED 2026-08-16 (verdict held for Branch 21, unblocked by SERVING.md): lineage first-class + single-holder fenced materialization lease; session = template-stamped isolation unit, per-session pods, home session hosts Sibyl; §3 physical contract = SERVING.md's machine; fork = O(manifest) + skeleton; three-layer landing engine (manifest prune → eg-walker replay as detector-only → jj conflict algebra, resolution-is-a-change); composition = declared-order pairwise, disjoint-or-verdict-clean + re-verification; resolver proposers version-pinned, validated, never silent; conflict deposits per-template; user review first-class (materialization = prompt + zero unresolved conflicts); 6-stage evaluation funnel with measured lifts (dedup/differential/hybrid/committee; composition-by-regeneration PDR; critic-gated early stopping); lifecycle fast-forward states; GC licensed by continuous exfiltration; scale-down floors ratcheted. Riders executed with SERVING.md commit |
| `docs/specs/LEDGER_CORE.md` | ACCEPTED 2026-08-16 (sub-decisions a/b/c; amended under maximal audit): single-owner core per session (ceiling priced + CI-measured), writer disjointness as struct layout, apply-on-ack with **effective-state checks** (arenas ⊕ pending, closes the pipelined-affordance/update-on-terminal race, L13 CI gate), per-parked-scope monitors + oracle fuzz (global SCC rejected as less verifiable; closure memory budgeted L15), no outbox — log+cursor projectors (typed RESYNC), event-carried score snapshots (bounded staleness priced), three-layer exactly-once stated (cursor + dedup window + content identity), retirement as PACED custody transfer (debt-driven interleave, never idle-work, L14), handler failures = typed error values → failure testaments (catch_unwind clause SUPERSEDED 2026-08-17 by RUNTIME §4b's no-panic law), L3 replay normalizes derived caches |
| `docs/specs/AUTOSCALING.md` | ACCEPTED 2026-08-16 (sub-decisions i ratio-law-only, ii scale-to-zero; amended under maximal audit): two instantiations (session + node) of one deterministic ratio target-tracking controller; signals restricted to LOAD-PROPORTIONAL classes (latency budgets enter via Little's-law target derivation, never as controller signals — architecture test); silence fails closed (freshness bound → hold + alarm, A11 gate); τ from ratcheted commissioning baseline, never continuously adaptive; asymmetric response + AIMD clamps + in-flight accounting; drain = graceful, parked scopes transfer via brief+claims handoff (A5 resume equivalence); scale-up through Guardian admission front door; work-driven roles get advisories to the Guide only (A8 structural); two loops at derived-apart cadences (A9 anti-resonance); decisions=logs, ledger=summon/teardown claims only, targets=config |
| `docs/specs/REGISTRY.md` v2 | ACCEPTED 2026-08-16 (amended under maximal audit, exact implementations): RawObject envelope, per-kind codecs the only typed boundary; **universal canonical encoding** — compiled kinds hecate-wire, schema-registered kinds via compiled `DocValue` type (i128 ints no floats, BTreeMap sorted-unique keys, dialect-proof hashing G11; closed schema subset, unknown keywords reject; append-only schema versions); three-state upsert (unchanged = zero writes); intent/observation split with resolvedSource carve-out; bundles = Merkle fingerprint + dependency snapshot + `resolved_at_revision`; **tenancy = scope-in-key** (Shipped\|Org\|User leading key component, authority in typed handles, publication = Guardian staging transition, G13 gate); **revision-floor reads** (session watch cursor as floor, serve_at_floor wait-or-forward, never stale, G14); storage = 6-op semantic contract (CAS put/get, ref-CAS sole mutation + unbypassable events, ordered scan, label index, forward/reverse ref index, event log) file-backed ≡ replicated (G10); external resumable watch (RESYNC discipline); Guardian staging = inventory-from-bytes content-bound approvals; no semantic search (pgvector fossil), no runtime authority, loud one-way doors |
| `docs/specs/SKILLS_API.md` | ACCEPTED 2026-08-16 (amended; USER CORRECTION captured: **TS/Python are authoring bindings, never runtimes** — no interpreter in any microVM): one Rust derive → five artifacts (wire codecs, MCP projection, skill:// resource, registry doc, dispatch glue — no second interpreter); bindings = registry-wide typed authoring SDKs generated from kind descriptors, output = canonical DocValue documents only, submitted via apply + Guardian staging; declared-skill invocation = COMPOSITION not code (closed DispatchTarget: Facade w/ pure field-mapping template \| ToolExec via provisioned Recipe — logic forbidden, static total verification at staging); arbitrary behavior enters only as provisioned tools through the tool plane; capabilities = closed harness-versioned bitset w/ compile_to_warden(), derived-not-trusted from dispatch targets (S9); built-ins stateless between invocations (lint); omission-is-absence surfaces, S6 count budgets; S1/S5/S6/S8 permanent (S8 = no-execution structural) |
| `docs/specs/HEALTH.md` | ACCEPTED 2026-08-16 (amended): one consolidated signal plane, no probes added, no authority ever (H4); per-class **AbsenceIs semantics** (Degraded = silence-is-the-signal \| Unknown = surfaced staleness, never frozen values; (value, freshness) delivery, H7); **content-free law extended by user direction** — operational measurements + opaque refs ONLY, never work content NOR ledger content (no claim/testament/validation/artifact content, no multi-media; no unbounded string/bytes field in any signal type — H8 type-walk gate); context-fit accounting = Branch 14's formula, this spec owns plumbing only; node rollup on gossip budget (H6); scribe triggers (context = threshold-is-evidence unilateral; performance = evidence bundle + single Guardian evidence request, second structurally impossible H3); observe-mode-first for new classes; H1/H4/H5/H8 permanent |
| `docs/specs/CONSENSUS.md` + `docs/specs/FAULTS.md` | ACCEPTED 2026-08-17 (Branch 20; ratified direction + amendments 2a/2b/3-addendum/5a + three in-exchange delta sets): meta tree (one group per failure-domain-tree level; root = region = one group on laptop) + N session groups; colocation law (no sync WAN on session hot paths — Physalia principle); node-liveness fabric (disk-write-backed support, fortified leadership, idle groups cost zero) with the **fabric-is-liveness-only law** (deletable-fabric acceptance criterion); pure core, CRDB-lineage dialect, IO-as-data + AsyncStorageWrites, entries-then-HardState + watermark-atomicity laws; core-as-disciplined-actor (five Akka laxities refused); PreVote+CheckQuorum unconditional, ReadIndex-only, transfer carve-out; split-brain four-layer table; joint consensus + Ongaro guard + learners-only demotion + apply-time conf changes w/ #12359 conf-commit metadata; dedicated log store, host-owned truncation/snapshots via TRANSFER.md; CAS-first vs lease+fence roster boot-validated + **epoch-scoping law**; cross-region = async content-only durability, no session failover (loss priced by OBJECT_TIER §3 formula), FlexiRaft rejected for meta plane [§7 receipts under verification — open rider]; CS1–CS12 conformance suite + CN1–CN14. FAULTS: closed scope (crash-recover + detected corruption + asymmetric omission + region events + fabric-fault; NOT Byzantine), CTRL dispositions (never silent truncation), 15-class nemesis vocabulary, deterministic whole-cluster simulation (seeded, BUGGIFY-biased, ratcheted budget, N=1 gate), boot-validated failure×obligation matrix, F1–F7 (F7 = region-heal/zombie-region) |
| Architecture set | `docs/architecture/{AGENTS,SUMMONING,LEDGER,SKILLS,PLATFORM}.md`, `CONTEXT.md`, ADRs 0001–0005 — amended throughout this session (open roster/offices, Arbiter, summon-as-claim, retirement, work volume, ten agents; Failure-domain tree + Epoch scope glossary entries 2026-08-17) |

## ON THE TABLE (drafted + shown; awaiting acceptance — settle ONE at a time)

1. `docs/specs/FOREST.md` — decay examination RESOLVED 2026-08-16: the
   **retention model is ACCEPTED — the intensity × durability hybrid**
   (alternatives (1)+(2); user pushed for the hybrid combination and the
   domination analysis confirmed it: (3) corrected-ACT-R dominated in every
   combination). Intensity = K derived exponential registers/channel,
   saturating gain (MMAS+FSRS+MCM fused), fixed-point lazy read, power tail
   w_k ∝ λ_k^d, convex GLM fit; durability = FSRS-shaped (D,S,R), collapse on
   contradiction, params re-fit never copied; declared consumer map (rank =
   intensity × R^γ; admission = TinyLFU duel per token; retirement =
   rank-density floor crossing; consolidation = S threshold); contradiction
   mass = curation-attention signal; one owner module, one clock, co-fitted.
   ALL amendments APPLIED to the spec: 4 audit corners (typed-field marks +
   Branch-22 symbol dependency; (HLC,stream,seq) merge; checkpoint-retention
   invariant + exact checkpoint doc + Branch-14 boundary; paced consolidation)
   + PPR forward-push exactness + digest floor θ + snapshot max-age + tests
   F15–F19, F21 (the 15 Sylk-trap suite) + acceptance 4/4b. **REMAINING before
   whole-spec verdict: the retrieval-hybrid exchange** (PPR-only
   under-implements the HippoRAG receipt — dense+PPR is what was measured;
   three-signal fusion: structural PPR + exact-search dense (session-bounded ⇒
   NO ANN ever) + lexical BM25 via Branch-23 machinery; fitted fusion weights;
   federation seam for Branches 22/23; narration free text becomes reachable).
   Presented, awaiting user verdict. — Z-set field engine, ACT-R/FSRS/MMAS/Parunak/PPR
   dynamics, primary-by-construction, observe-mode value gate, session-isolated
   (global-forest tier DELETED as data-leak; user correction).

## OPEN BRANCHES (no spec)

- **14 Handoff: the full pipeline** — WIDENED 2026-08-16 (user: Sylk's
  performance handoff "threw out some formulas, it never seemed to work
  correctly or trigger" — the decay disease again; demand = practical
  mechanisms end to end, not just math). Five sub-decisions, each settled
  exactly: (1) **gathering** — which per-turn/per-instance signals are
  collected, by what mechanism, at which chokepoints (HEALTH owns plumbing;
  this branch names the concrete collectors); (2) **weighing/classification**
  — how raw signals become graded evidence (windows, baselines, outcome
  grades); (3) **storage** — where performance data lives (Scribe working
  state vs health composites vs score service), durable vs re-derivable,
  retention; (4) **trigger** — the detection math (changepoint CUSUM/EWMA vs
  SPRT sequential testing vs Bayesian online changepoint; threshold
  derivation; why Sylk's never fired) + the evidence-bundle exact content for
  the single-Guardian-request flow (HEALTH §3); (5) **execution** — the
  brief+claims handoff mechanics in full (brief content, claim transfer,
  volume re-bind timing, model swap vs fresh instance, warm-up, in-flight turn
  disposition). Context-handoff accounting (provider usage vs local estimate)
  stays sub-decision (1)/(4) territory. RESEARCH DISPATCHED 2026-08-16 ×2:
  degradation-detection literature + Sylk handoff post-mortem.
- **15 Steering machinery** — mid-task user guidance: interrupts as
  supersession, priority hints as claim fields, turn-level injection.
- **17 Remote client + terminal** — seam remote binding: attach/detach, view
  subjects (pane=subscription), input lease mechanics, cursor resume, offline
  queue, presentation plane rendering from deltas.
- **18 Continuity + conversation** — carry-forward/recall over the archive
  (same-user path partially shaped in SESSIONS/FOREST), Guide conversation model.
- **20 Consensus + fault matrix** — direction argued (5 decisions: one meta
  group + N per-session groups w/ node-level liveness amortization; "Raft,
  etcd-raft dialect, pure core"; PreVote+CheckQuorum; CAS-first single-writer
  subsystems; crash-recover scope + N=1 crash-injection gate), UNRATIFIED and
  **CHALLENGED 2026-08-17** — user: "IMMEDIATE and severe concerns with using
  ETCD or using ETCD as any sort of example - it has well documented
  shortcomings and failure modes that do not scale up well to Meta scale
  work." Re-analysis owed as THE NEXT EXCHANGE: etcd's documented failure
  record (v3.5 apply/applied-index data inconsistency, boltdb/backend size
  limits, watch fan-out collapse, single-group throughput ceiling,
  small-voter-set ceiling, k8s-scale pain) vs Meta-scale practice
  (Delos/virtual consensus + loglets, FlexiRaft/MySQL-Raft, ZippyDB, Shard
  Manager; Spanner Paxos groups; TiKV/CRDB multi-raft; VSR/TigerBeetle) —
  explicitly separating etcd-the-system from etcd-raft-the-library-dialect;
  then re-present. **RE-PRESENTED AND RATIFIED 2026-08-17** ("accepted."):
  the five decisions stand WITH four amendments — (2a) exemplar renamed
  "Raft, CRDB-lineage dialect, pure core" (interface shape = etcd-raft as
  extended by cockroachdb/raft; tikv/raft-rs = Rust portability proof; both
  exemplars never dependencies); (2b) the (b)-class + protocol bug record
  ships as an executable conformance suite (named regression tests, never
  folklore); (3-addendum) explicit conf-change activation semantics with
  #12359 countermeasures as spec law (conf-commit metadata on votes, no
  direct voter demotion — route through learner); (5a) fault gate upgraded
  to deterministic whole-cluster simulation (FDB/TigerBeetle-VOPR posture;
  mutually reinforcing with pure-core IO-as-data). CONSENSUS.md + FAULTS.md
  drafts presented in-message; three in-exchange delta sets worked to
  acceptance (split-brain four-layer assembly + fabric-is-liveness-only law
  + Akka/Elasticsearch rejected-alternative record + CN11/CN12; core-as-
  disciplined-actor position with five named Akka-laxity refusals;
  cross-region — failure-domain tree first-class, meta tree = one group per
  tree level (laptop collapse by derivation), epoch-scoping law, async
  content-only cross-region durability + no-session-failover priced by the
  OBJECT_TIER §3 formula, FlexiRaft rejected for the meta plane, CN13/CN14
  + F7 region-heal). **SETTLED 2026-08-17** — both specs accepted and
  written ("accepted." ×2). RIDER CLOSED 2026-08-17: verification dossier
  landed (research index), §7 reopened per the rider, six-amendment set
  presented and ACCEPTED ("accepted") — FlexiRaft rejection rewritten
  (two-branch unavailability/forced-reconfig argument, dynamic mode only,
  static mode = same species as the root group), lease-shadow law
  (Chubby lock-delay; rate-derived margin; CN15), externalization-fencing
  law (every external side-effect channel = landing-class chokepoint
  carrying root-scoped epoch; CN16 + acceptance 10b), region rejoin
  protocol (terminal epoch on dead-declaration; rejoin under new epoch;
  fork-only ingestion; F7 extended a–d), async-pole honesty note
  (MRSC/Spanner/CRDB as the deliberate sync pole), receipts strengthened
  (RTC 15-min SLA quantifies exposure_window; Dynamo surfaced-siblings vs
  LWW anti-pattern; Physalia intra-AZ precision note). §7 RE-SETTLED.
- **21 FS implementation (the serving machine)** — **SETTLED 2026-08-16**:
  spec `docs/specs/SERVING.md` accepted whole; decision record below stands
  as history. OPENED 2026-08-16; user
  critique: EdenFS/CitC borrowings named but machinery never designed, and the
  laptop→fleet scale story unstated ("sharding — how?"). Decisions to settle,
  research-first: (a) write/witness model — **RATIFIED 2026-08-16: journal-
  first (Option C)**. The witness journal IS a session WAL log: FUSE_WRITE
  appends a content-bearing op, group-committed before the reply (ack = the
  witness; power-fail-safe, beats EdenFS's process-crash-only). Overlay =
  derived, rebuildable state (crash recovery = replay; no fsck). Epochs seal
  into CDC/BLAKE3 CAS snapshots at increments (OSTree/f4 demotion). Manifests
  keep the one-bit dirtiness contract (hash = clean | journal-ref = dirty).
  eg-walker op logs derived by diff at seal time, off the hot path, version-
  pinned (satisfies the SESSIONS.md VFS rider). Journal = FS-service working
  state, NOT ledger. Spec owed with the branch spec; (b) overlay
  representation — **ACCEPTED 2026-08-16**: exactly two representations.
  Mutable = per-pod log-structured work-volume overlay (per-volume journal +
  extent index; single authority; cross-volume reads unrepresentable; volume
  outlives pod, re-binds on handoff; no index checkpoint — rebuild bounded by
  seal cadence, checkpoint is the tripwire; dirty reads = FUSE_READ copies,
  DAX-for-dirty REJECTED as cross-volume leak via interleaved segments).
  Immutable = manifests-over-CAS everywhere else (baseline, green chain,
  seals, tools). Green = manifest chain, no journal: merge gate EXTENDS
  (never writes) — chain record (version, manifest hash, increment refs) is
  green's only WAL touch; serving instances compiled with no write path
  (EROFS structural); all-DAX read-only, cross-pod page sharing; pods pin
  green@version, re-bind at increment boundaries via manifest-diff targeted
  invalidations (EdenFS checkout steal). Scratch volume role rider on VFS.md
  (redirect paths unwitnessed, pod-local, die with pod). Increment submission
  forces guest writeback drain (FUSE_FSYNC sweep) before seal; (c) metadata
  model — **ACCEPTED 2026-08-16**: inode identity law = (volume, path-entry),
  monotonic per volume, stable for the VOLUME's lifetime (table serializes +
  re-binds with the volume — takeover steal; handoff invisible to (dev,inode)
  tooling); content identity = manifest-entry hash, re-bind = hash swap under
  stable inodes + targeted invalidations only (manifest diff), generation
  numbers guard reuse; manifest entries carry (type, mode, size, BLAKE3) —
  stat/readdir/ENOENT answered from manifest, zero fetch, no negative cache
  (manifests complete); tree nodes = CAS chunks, lazy on first readdir;
  content on open (presence check batched → DAX or extent read); digest
  xattr contract: BLAKE3 xattr on clean files, ABSENT while dirty (honest),
  feeds build tools + scheduler memoization; caching split: green/tools =
  infinite TTL + explicit invalidation at re-bind, work volume = writeback
  mode (sole-writer guest coherence, batches witnessed writes); prefetch =
  template eager sets at bind + sampled-access-derived glob profiles
  (observe-first, EdenFS ~1500-glob receipt), crawl detection → bounded
  cache-fill (SES7); (d) DAX policy — read-mostly
  windows; witnessing enforceability VERIFIED via research (per-inode
  dax=inode + FUSE_ATTR_DAX + EROFS on WRITE mappings, shipped mechanisms);
  REMAINING resolved — **(d) ACCEPTED 2026-08-16**: mapping engine = one
  trait, two modes — splice (zero-copy page share) | managed-window (boot-
  mapped window, daemon copies; zero runtime hypervisor calls; the one mode
  where DAX + full witnessing could coexist); KVM = splice, HVF = splice
  behind boot capability probe w/ managed fallback, WHP = managed until
  proven; window = 2 MiB × derived peak hot ranges + 20-range reclaim
  headroom, ceilinged by ~1.6% guest-RAM tax — all anchored in kernel
  constants; **(e) ACCEPTED 2026-08-16**: own FUSE-over-virtio protocol layer
  + backend trait native to hecate-rt, in-process device in the libkrun fork
  (vhost-user rejected: process model + sync trait + ENOSYS DAX); borrow
  structure not code (virtiofsd dispatch shape + zero-copy seam, libkrun
  3-platform mapping paths, EdenFS inode discipline); advertise multiqueue
  (5.5× receipt, Linux ≥6.10 guests); (f) scale topology —
  **ACCEPTED 2026-08-16**: one weighted-HRW placement function over a
  versioned, fenced host-inventory map (consensus-owned; consumes Branch 20's
  API, doesn't own it); chunk-groups as placement unit (count = devices ×
  target-groups-per-device ≈100–200, Ceph anchor) + explicit upmap-style
  exception table; R-way replication on the live tier, R_eff = min(R_target,
  distinct failure domains), degenerate durability LOUD (MinIO SNSD wording);
  erasure only in the Archivalist cold tail (f4); cache = DAX → host
  pack-volume store (append-only + in-RAM index, Haystack) → HRW peer →
  shield/origin, single-flight at every layer, popularity-triggered
  mirroring, never rehash-on-failure (Gutter); mutable = state-follows-
  compute (primary at the scheduler's colocation host; HRW = replica set:
  journal-ship to top-(R−1) successors, promotion order = the HRW list, no
  data-path election; HRW enters scheduler locality scoring as preference);
  hecate-wire gains batched-existence + group-granular fetch/repair verbs;
  laptop = inventory of one, identical formulas, no modes; (g) the
  single-guest-protocol advantage (Linux guest on every host OS ⇒ one serving
  protocol; EdenFS's FUSE/NFS/ProjFS three-protocol matrix structurally
  absent) — verify against libkrun/HVF/WHP findings. Research LANDED ×4:
  EdenFS internals (overlay thrift schema, inode dual-map, metadata-only
  journal, takeover, the 3-OS pain record); CitC/Piper (snapshot-on-save
  verbatim, <10-file overlay, 2011 read-tier recipe: stat from metadata +
  digests-as-xattrs, 500–800K QPS mostly build systems, zero-copy CI);
  virtio-fs/DAX (witnessing enforceable via per-inode dax=inode +
  FUSE_ATTR_DAX + EROFS on WRITE mappings — shipped mechanisms; in-process
  device dissolves reconnect; managed-window copy mode = portable fallback;
  multiqueue 5.5×; our fork = only 3-platform DAX in existence); sharded CAS
  (flat weighted HRW à la Buildbarn, chunk-groups + upmap exception table,
  pack volumes + batch existence checks, groupcache single-flight/mirroring,
  MinIO/Ceph/SeaweedFS parameter-degeneration no-modes receipts, MinIO FS-mode
  removal as the mode-bifurcation record). Next: (b) overlay representation.
- **22 The knowledge graph (code ground truth)** — ADDED 2026-08-16;
  **REDIRECTED 2026-08-16 (user): USE AND INTEGRATE ../vorpal — its KG
  implementation, adapted to distributed use.** Vorpal = the user's Rust
  ingest→index→search engine on a rebranded ast-grep: tree-sitter extraction
  across 28 languages ("sees everything", extraction-as-rules, no regex),
  code KG (defs as nodes; calls/imports/implements/of_type/references/
  containment edges), HONEST RESOLUTION (scope precedence, confidence labels
  LOCAL>CROSS_FILE>AMBIGUOUS, unresolved counted never faked, 100% P/R
  labelled eval suite), hybrid retrieval (exact/token + deterministic
  feature-hash lexical embeddings [Embedder trait, neural adapters optional]
  + graph in-degree, RRF-fused w/ per-channel provenance), incremental
  (per-file product cache + full relink ⇒ no stale nodes), MCP server.
  **Doctrine alignment is near-verbatim** (its locked decisions: 10⁹-LOC
  streaming/bounded-memory, deterministic core, Arc-free arenas +
  generational handles, single-writer-per-shard, blake3 external identity,
  custom segmented mmap format + io_uring, deterministic ANN build, CSR +
  masked-SpMV Datalog closure). Deep survey DISPATCHED (built-vs-planned,
  data model, incremental machinery, storage, fusion, REMOTE.md distribution
  design, integration seams — esp. VFS/manifest-fed ingest vs disk walks,
  per-session instances, embeddability). Hecate adaptation questions queued:
  per-session projection over green/lineage manifests; parse products
  content-addressed in the CAS (dedup below isolation line); relink scope
  under green advances; serving via Hecate protocol vs vorpal transport;
  vorpal MCP tools → skills/facades; vorpal's feature-hash embedder as a
  candidate for the Forest's lexical/dense channels; structural search
  (ast-grep rules) as an agent capability. Prior research-first list
  (Glean/Kythe/stack-graphs/SCIP/LSIF) demoted to comparative background.
  **SURVEY LANDED 2026-08-17** (tests run by the surveyor, green): mature
  single-machine substrate — KG/ingest/resolution/storage/search/MCP all
  built, byte-identical determinism ENFORCED by tests (streamed≡batch,
  sharded≡serial, spilled≡RAM, incremental-converges-to-scratch, content-id
  reproducible at kernel scale); honest-resolution eval 7 langs green;
  benchmarks: linux kernel 72.5K files → 2.75M nodes, cold 8.97s, warm 0.11s,
  one-file update 2.30s (**relink is FULL, O(corpus) — the incremental cost
  floor**); .vseg RAW-only (codec stack aspirational), content-addressed
  generations + atomic CURRENT swap + GC; u32 ceilings (2³² defs, 4GiB heap)
  checked with actionable errors. Distribution: wire/transport/agent fan-out
  fabric REAL (20/20 loopback), but distributed INDEXING 100% unwritten
  (no realm column/scoped resolution/product batching/merge driver/federated
  query; content_hash→xxh3 I3 fix pending). Integration seams: **VFS seam
  exists** (stream_apply takes caller FileStats + work closure, disk-free;
  extract_product pure) but build_index_full welded to Manifest::scan →
  upstream `Manifest::from_entries` + Verified-mode content hook (small
  patches); no external-diff API (diffs save parse only — relink full
  regardless); globals: process-wide leaked interner (biggest hazard for
  multi-session hosts), WARM_ROOTS, process-wide ANN_BUILD mutex, jemalloc
  as vorpal-index LIBRARY dep (check). **Hecate adaptation shape (draft, to
  settle)**: (i) per-lineage-baseline index generations are CAS-shareable
  below the isolation line (deterministic: same manifest ⇒ same generation
  bytes — receipts in-tree); (ii) session overlay over shared base + scoped
  resolution + federated RRF = the distributed adaptation (REMOTE.md D3),
  needed because full relink at monorepo scale is infeasible per edit —
  session-scale corpora relink in ms, the base/overlay split is the
  Meta-scale answer; (iii) parse products keyed by source_xxh3 → CAS product
  bank (dedup across sessions); (iv) instance model decision: embedded-lib
  (needs scoped-interner upstream) vs session-scoped worker process vs
  KG-service pod — OPEN; (v) 15 MCP tools → Archivalist/agent skills;
  structural search as agent capability; (vi) LexicalEmbedder + ModelProvenance
  learned:bool gate = candidate for Forest channels, provenance pattern
  matches doctrine. Upstream patch list: Manifest::from_entries, content-
  source hook, xxh3 identity (I3), scoped interner, budget/shard knobs as
  parameters not env vars. **INTERNER RESEARCH LANDED 2026-08-17** —
  recommendation R1, decision-ready: **per-build NameInterner instance +
  freeze-to-reader** (same 64-shard design instance-ized; freeze at the
  commit→link boundary into a lock-free FrozenNames — the lasso
  Rodeo→RodeoReader receipt: frozen readers scale ~flat to 24 threads vs
  ~29× slower through the concurrent map; DELETES 7 RwLock acquisitions
  from the hottest resolver loop = faster than today; reclamation = Drop,
  zero unsafe; handle-threaded explicitly — churn surface grep-verified
  tiny: 7 constructor call sites / 4 files / ~10 files total; rustc's
  scoped-TLS shape REJECTED deliberately — its own panic forces
  one-thread-per-session, incompatible with builds on a shared rayon pool;
  spill.rs untouched — create-read-delete lifetime is inside one build;
  determinism unchanged — nothing observable orders by NameId, verified).
  Every production compiler scopes interners this way (rustc session /
  Clang per-instance / V8 per-isolate / JSC per-VM; Roslyn's lossy cache
  not transplantable — can't mint stable ids). BONUS BUG FOUND: the
  process-wide table breaks insert_if_referenced's peek — "was this name
  interned by ANY build ever" vs "by this build" — cross-corpus vocabulary
  pollutes the referenced-only filter monotonically; R1 fixes it as a side
  effect. NOTE: vorpal's working tree already carries an uncommitted
  unsafe-reclaim_all first cut — R1 REPLACES that direction (no unsafe, no
  quiescence protocol, no ACTIVE_BUILDS plumbing). R2 = content-hash
  xxh3_64 NameIds as the composable END-STATE add-on when distributed
  indexing lands (zero-coordination intern scaling, intrinsically I3,
  Unison precedent; costs +40% Reference/+47% spill/+33% Symbol; 64-bit
  birthday math safe with per-build collision detection, 128-bit if ids
  ever become forever-global CAS keys); R1's seams are R2's substrate.
  R3 (global + reclamation machinery) and R4 (process-per-session only)
  rejected with reasons. Upstream shape: 4 commits incl. the I3
  KgWriter-DefaultHasher→xxh3 fix + pinned cross-build test vector.
  **USER PUSHBACK 2026-08-17: Neo4j and Java graph DBs EXCLUDED as
  references** (survey content stands only as cautionary evidence on
  mutation machinery). **The IVF + Vamana overlay architecture is the
  unique substrate** (Sylk core/vectorgraphdb: Vamana + IVF k-means + BBQ +
  mmap + IVF-WAL; vorpal crates/ann tiers + §10 end-state RaBitQ/PipeANN/
  ParlayANN/FreshDiskANN-SPFresh/ACORN) — distribution designed from ITS
  components, nothing sacrificed, complexity unweighted. RESEARCH
  DISPATCHED ×2: (i) component survey of both implementations (exact
  algorithms, the overlay's precise mechanics, WAL, maintenance signals,
  determinism seams); (ii) distributed vector-search anchored on the
  DiskANN family (SPANN centroid-routing + closure multi-assignment,
  SPFresh LIRE, ParlayANN deterministic builds, RaBitQ, ACORN) +
  non-Java production systems (Turbopuffer/Pinecone-serverless
  object-storage-native, Milvus segments, Qdrant; Vespa as contrast) —
  judged against the sketch: replicated-everywhere centroid routing tier;
  IVF cells as content-addressed HRW placement units; sealed per-cell
  Vamana artifacts (pinned-order builds); closure multi-assignment =
  boundary ghost-posting analogue; session overlays = exact-search flat
  segments merged at re-baseline; rerank vs full vectors in the OWN object
  tier; laptop degenerate. **COMPONENT SURVEY LANDED 2026-08-17**: "overlay"
  disambiguated ×3 — (a) Sylk IVF's inter-partition navigation tier (Vamana
  over partition reps, R=log₂P, SPLICED into the flat adjacency — should be
  materialized separately: a few-KB, separately-versioned inter-cell routing
  graph is exactly the distribution seam); (b) vorpal OverlayView = the real
  delta layer (FileRun content-addressed row-ranges, tombstone remap, 15%
  refusal ceiling, base∘remap ∪ overlay, never waits on ANN build);
  (c) EMERGENT_FOREST density layer = doc-only. SYLK FINDINGS (post-mortem
  class): **BeamSearchBBQ never traverses the graph it builds** — the
  Vamana graph is built/persisted/health-tracked but unused at query (only
  OptimizeGraph walks it); deterministic RNG machinery exists in 3 places
  UNUSED while the paths that matter use unseeded rand (RobustPrune
  reservoir-sampling, k-means rand.Perm, medoid/boundary sampling);
  maintenance signals (Gini/CV/Drift/Connectivity) trigger NOTHING (the
  real trigger = separate EMA health system, √n sampling, α=1/√n); the 4
  maintenance ops have zero production callers; ivf WAL unwired (sylkdir
  global_ivf_log IS wired = the O(delta) mechanism: watermark+fingerprint
  sidecar, torn-stitch→rebuild); vestigial dead quantizer/LSH paths
  reconstructed on load. VORPAL: ParlayANN-style deterministic build BUILT
  (bit-identical at any thread count, pinned by test; seeded xorshift,
  (dist,id) total orders, exact-integer i8 dots), zero-copy v5 format,
  provenance gating, rerank discipline — behind on IVF (none), RaBitQ,
  PipeANN/io_uring, ACORN (filters post-tier only), and derived params
  (65,536 tier cutoff + R=32/L=48/α=1.2 HARDCODED vs Sylk's fully
  data-derived ConfigForN — Sylk wins exactly once, here). SEALABLE:
  per-partition graphs (built in ISOLATION per worker — natural cells),
  partitions.bin CSR (contiguous per-partition byte ranges), centroids.bin
  + BBQ means (the routing table — replicate everywhere), 65536-record
  CRC64 shards, ann.bin/ann.files (base_stamp generation identity).
  MERGE PRIMITIVES EXIST: StitchBatch (O(√N) bulk segment-merge) +
  Stitcher (cross-shard graph join, √N boundary sampling). THREE
  PREREQUISITE FIXES for distribution: (1) global sequential uint32 IDs +
  package-global insertMu → partition-local ID spaces w/ translation (the
  nodeIDs[] sidecar already does it once) or range leasing; (2) positional
  partition indices → stable partition identities (content hash per cell +
  indirection) so cells seal/migrate independently; (3) de-splice the
  overlay routing graph. **DISTRIBUTION RESEARCH LANDED 2026-08-17 — sketch CONFIRMED with five
  sharpenings**: (1) centroid tier = sealed per-generation routing artifact
  (centroids + cell→artifact map), K ≈ (15–20)·√N derived — tens of MB at
  10⁸, genuinely replicate-everywhere incl. laptop; assignment/routing =
  EXHAUSTIVE centroid scan, pinned kernel, fixed tie-break (lowest cell id)
  — never graph-assisted (FAISS 1T + reproducibility receipts; deterministic
  -IVF-assignment literature does not exist, flagged); (2) **balance-by-
  construction is a LOAD-BEARING REQUIREMENT of HRW placement, not an
  optimization** — skew's effect on load is QUADRATIC (FAISS 1T law: <10
  lists >600× skew → 120s queries); SPANN's hierarchical balanced
  clustering (balance in the objective) + derived cell-size cap + split-at-
  cap during deterministic build; (3) ParlayANN determinism costs NOTHING —
  1.2× FASTER than reference build, quality within 1%; stateless build
  workers; **build verification = content-hash comparison** (an audit no
  mutable index can run); (4) closure multi-assignment (ε₁ rule + RNG-prune
  + ≤8 cap, ~1.2× storage) confirmed + UPGRADED: SOAR decorrelation term
  ranks which cells get replicas (naive two-closest spilling wastes the
  second chance — correlated residuals); ε₂ query-side dynamic pruning
  (SPANN's 6.36-of-32-machines = 80.3% saved — THE distributed-efficiency
  receipt); closure converts FP-near-tie nondeterminism into correctness-
  neutral duplication (elegant); (5) rerank depth DERIVED from RaBitQ
  provable error bounds (drop iff lower bound > current best; turbopuffer
  <1% reranked in prod) — 'exact rerank always' becomes provable.
  UPDATE-ABSORPTION VERDICT: deterministic re-baseline + WAL-journaled
  exact-search overlays DOMINATES on all four axes — fresh static build is
  the quality CEILING incremental schemes approximate from below
  (FreshDiskANN equilibrium below static; LIRE/StreamingMerge outputs
  arrival-order-dependent = un-content-addressable); k_build ≈ 1.7
  core-ms/vector (ParlayANN anchor) ⇒ 10⁷-vector lineage rebuild = ~5
  core-hours = minutes on a workstation; crossover to SPFresh-style
  in-place ≈ N≥10⁹ × ~1%/day churn × sub-day freshness — NOT Hecate's
  regime (bursty updates at merge-gate/landing = natural re-baseline
  points); re-baseline trigger derived: c_scan·|overlay| ≥ β·c_indexed
  (turbopuffer's 128MiB cliff converted to a formula); overlay WAL is
  load-bearing (the unwired-IVF-WAL lesson honored). Production
  convergence: object-truth camp (turbopuffer/Pinecone/Lance) vs node-
  resident camp (Vespa feed-block contrast case); ALL pain concentrates in
  mutable parts; index family follows storage medium — IVF where the
  network is, Vamana where the NVMe is: the substrate's shape CONFIRMED.
  Realm/tenant isolation = generation-lineage-per-scope (turbopuffer
  namespace-per-query-scope) — tenant predicates never enter the hot path;
  ACORN/Filtered-DiskANN = billion-scale medicine deferred. Alternatives
  ranked: global-graph-over-KV (DistributedANN 50B/1000 machines, 6×
  claim single-sourced) revisit only past ~10⁹–10¹⁰/corpus sustained-QPS;
  Milvus-shaped streaming machinery = right shape, machinery deleted;
  SPFresh = right answer to a premise Hecate doesn't have. Thin evidence
  enumerated. **Branch 22 evidence COMPLETE (graph + vector sides) —
  design exchanges ready to open.**
  **DISTRIBUTED-KG SYNTHESIS LANDED 2026-08-17 — base+overlay hypothesis
  CONFIRMED: it IS Glean's production architecture** (stacked DBs verbatim:
  "each layer can non-destructively add information to, or hide information
  from, the layers below"; delta→base refs by fact-ID arithmetic; ownership
  /slice hiding at 7% size / 2–3% indexing / <10% typical-query cost;
  orphan-prevention law; shard = whole DB stack COLOCATED by base; Janitor
  prefetch; central store + replicate-to-serving-caches; no consensus near
  data). FOUR SHARPENINGS the draft lacked: (1) **overlay visibility
  MASKING is the hard part, not distribution** — vorpal has zero slice
  machinery; adaptation: overlay records changed-file set, query-time base
  masking by provenance, base edges into masked nodes re-bind via stable
  eid=blake3(path:entityPath) — redirect if survives, honest dangling
  tombstone otherwise, confidence-labeled; NEVER compute derived tiers
  (ANN/postings) over stacks (Glean's derived-facts caveat) — per-overlay
  only; (2) overlay build unit = REVERSE-DEP CLOSURE of the edit (Glean's
  C++ fanout receipt), closure computable from prior generation's reverse-
  import edges, corpus-scale closures degrade loudly to baseline-rebuild
  scheduling; (3) COLOCATION LAW: overlay served where its base generation
  is resident — placement key = base generation, enters scheduler locality
  scoring; session-private products stay in session key root, CAS bank
  dedups only at-or-below baseline/green; (4) double-posted cross-realm
  edges + seal-baked global stats + hub-realm replication or scatter-gather
  silently degrades. Retained 'database' machinery: ref-CAS pointer w/
  revision-floor reads + concurrent old+new generation serving + GC
  new+prior — NOTHING else (no per-shard consensus/MVCC/txns/tombstones/
  online rebalancing/dynamic index maintenance). Merge/relink: overlays =
  mold philosophy (fast full relink of small corpus, 0.3–300ms derived);
  baselines = Glean philosophy (scheduled hierarchical rebuild per lineage
  advance, CAS product-bank sharing, warm 0.11s at linux scale); periodic
  re-baseline bounds drift (Lucene compaction cadence, derived from
  overlay/tombstone ratios); relink wall ≈4.8min/edit at Google scale =
  the quantitative overlay boundary. Thin evidence enumerated (8 items;
  subtree locality still the must-measure-at-seal). Branch 22 exchanges
  now armed pending the IVF+Vamana pair.
  **THE PAIR DELIVERED + ACCEPTED 2026-08-17**: `docs/specs/VECTOR_INDEX.md`
  (in-session user approval; storage dependency resolved by OBJECT_TIER.md's
  two-planes factoring — generations = lineage class on the durable plane).
  Sealed IVF+Vamana generations (routing artifact + cell artifacts +
  manifest w/ embedder pin), deterministic balanced build, ε₁-closure
  (SOAR-decorrelated variant benchmark-gated), exhaustive-scan routing +
  ε₂ fanout, bound-driven exact rerank, WAL-journaled exact overlays w/
  derived re-baseline trigger, colocation law shared with the graph side,
  VX1–VX12 matrix. Work plan W1–W7 on file (fit-from-our-data = stated
  first milestone — no literature below billion scale). Graph-side
  exchanges remain open and compose via the colocation law.
- **23 The document DB (records + full-text)** — ADDED 2026-08-16 (user: "as
  well as the document db"). The Archivalist's second organ: durable document
  records (papers from the academic handoff, design docs, session records,
  exported advisory documents) + full-text retrieval (BM25-class). Shape
  constraints from settled law: document BYTES live in the CAS as artifacts
  (ledger-referenced); the doc DB is the derived, re-derivable INDEX over them
  + typed metadata — session-scoped per the isolation law, user-archive index
  for same-user recall, publication via registry scopes like everything else.
  Interplay: Forest advisories cite documents; KG symbols link into docs.
  RESEARCH FIRST when opened: Tantivy internals (Rust segment architecture —
  fork-and-own candidate), Lucene segment/merge lineage, BM25/BM25F,
  incremental indexing + segment merges, snippet extraction; Bleve as the
  Sylk-planned reference.
- **24 The object tier (Hecate's own S3-level storage)** — ADDED 2026-08-17
  (user: "we need to *design* that storage in detail"). SERVING.md settled
  the topology (HRW chunk-groups, R-way, cache hierarchy, pack volumes,
  no-cloud-pairing law); this branch designs the storage system itself,
  database-grade. Decisions to settle, research-first: (a) durable write
  path — pack-volume format in detail (needle layout, seal/compact, in-RAM
  index rebuild-by-scan as truth w/ sidecar as optimization — the vorpal
  pack precedent; crash story: append+fsync vs WAL-machinery reuse);
  (b) replication protocol — write path for immutable content (any-copy-
  valid-by-hash simplifies: client-driven R-writes vs primary-driven vs
  chain replication; ack semantics/write quorum; read repair; hinted
  handoff vs re-replication); (c) erasure coding for the cold tail — code
  choice (RS(k+m) vs Azure LRC vs Clay), hot→cold migration (f4 pattern),
  reconstruction path + degraded reads; (d) scrub + repair — derived
  cadence, BLAKE3 verify, latent-sector-error receipts, repair scheduler
  riding the placement map, under-replicated-first prioritization;
  (e) failure-domain topology — domain declaration/discovery, hierarchical
  HRW levels, copyset-aware placement (data-loss-probability receipts);
  (f) capacity + lifecycle — GC of unreferenced content (liveness roots =
  manifests/ledger refs; exfiltration-licensed doctrine; refcount vs
  mark-sweep over manifests), per-tenant/session quotas + accounting,
  compaction reclaim; (g) API surface — put/get/batch-exists/range verbs
  on hecate-wire (extends the SERVING additions), streaming large objects
  (packs, generation segments); (h) metadata — volume→location index,
  placement-map epoch consumption (Branch 20 API), namespace/tenancy via
  registry-style scopes; (i) **encryption × dedup reconciliation** —
  **SETTLED 2026-08-17 as D-3** ("approved."): scope-salted convergent
  encryption + four hardenings landed in OBJECT_TIER §9, AC-6 lifted to
  practical gate, OT16–OT19 added (see GAPS.md D-3); original tension
  record follows as history. The
  open tension: encrypt-always + per-session keys breaks cross-session
  chunk dedup ('shared below the isolation line'); candidates: convergent
  encryption (hash-derived keys — dedup survives; known
  confirmation-of-file attacks to price), tenant-scoped dedup domains, or
  encrypted-at-rest-once with capability-gated access — MUST be settled,
  it decides the dedup story; (j) laptop degenerate — single-disk volumes,
  R_eff=1 loud, scrub still runs, identical formulas. RESEARCH FIRST when
  opened — **LEAD REFERENCE: Meta's Tectonic (FAST'21), per user direction
  2026-08-17 ("given our emphasis on speed, Tectonic is likely more
  appropriate")**: the exabyte-scale unified filesystem that consolidated
  Haystack/f4 blob storage + warehouse storage into one multitenant system
  — the very lineage (Haystack pack volumes, f4 hot/warm split) our
  SERVING topology already adopted, with per-tenant optimizations and
  disaggregated sharded metadata; study its client-driven architecture,
  metadata layering, placement, and tail-latency machinery first and
  measure every alternative against it. Then: Azure Storage
  (stream/partition layer split), S3 ShardStore (SOSP'21 — formally
  verified Rust LSM object store) + S3 strong-consistency retrofit, Ceph
  BlueStore internals, MinIO erasure/healing, Backblaze vaults (17+3), LRC
  (Huang), copyset placement (Cidon), chain replication (van Renesse),
  scrub/latent-sector-error studies (Bairavasundaram), convergent
  encryption (Tahoe-LAFS/DupLESS + attacks). Haystack/f4/groupcache receipts already
  on file. Underlies everything — sequences early in the walking skeleton.
  **RESEARCH LANDED 2026-08-17 (EdenFS-layer ↔ Tectonic-tier report)** —
  STRUCTURAL HEADLINE: Hecate gets Tectonic's fabric with ~⅓ of its
  metadata problem — Tectonic's Block layer (⅔ of ALL its metadata ops =
  "where does this block live") collapses into the HRW pure function +
  exception table; Name/File layers collapse into content-addressed
  manifests + registry refs. Total mutable tier metadata = inventory-map
  epoch (Branch 20) + exception table + refs. KEEP from Tectonic:
  client-driven data path (proxy "vastly less efficient"), dumb storage
  nodes (get/put/list/scan only), checksum-at-every-transformation (incl.
  RS inverse-check when EC lands; in-memory corruption "a regular
  occurrence" at scale). Tier map T0–T5 + the VFS.md reconciliation
  sentence (arena + pack store = RAM/NVMe tiers of ONE chunk store;
  movement = explicit lifecycle, never spill; EdenFS's two-overlapping-
  disk-caches admission = the cautionary receipt — ONE on-disk format,
  cache/origin as ROLES). Decision answers: (a) pack volume SETTLED —
  Haystack-shape framed chunks, BLAKE3-address-IS-the-checksum, in-RAM
  index w/ rebuild-by-scan as truth + trustless sidecar, batched fsync,
  torn tail self-drops via own hash, NO fsck; LSM/ShardStore rejected
  (mutable-key medicine — 16 formal-methods-caught bugs as the price
  receipt), BlueStore raw-block rejected (small-overwrite medicine;
  Haystack on XFS = 85% of raw throughput), file-per-chunk = measured
  anti-pattern; compaction = copy-forward; CacheLib 8-byte-hash escape
  hatch if index RAM drifts (derived); (b) write path = four rungs
  witnessed→sealed→PLACED (parallel idempotent PUTs, any-copy-valid-by-
  hash [composed Venti/OCI/Ambry — THIN, no single source], hedged
  reservations ~20% p99, ack=R_eff)→REFERENCED (placement strictly
  precedes reference ⇒ orphans-never-dangling); hedged reads at derived
  p95 (Tail-at-Scale 1800→74ms receipt); (cache) CacheLib whole-volume
  FIFO eviction (WA 1.5→1.05×), admission = endurance governor (TBW-
  derived servo; 44% fewer flash bytes; Tectonic-Shift PID 1.5–3.3×);
  summon claims/template eager-sets = declared-future admission (Shift
  pattern, native fit); (c) EC = seal-then-encode, LRC vs Clay table,
  HONEST: derive the crossover — replicated may dominate at small fleets,
  never adopt RS(10,4) by imitation; (d) scrub MANDATORY beyond verify-
  on-read (>60% of latent sector errors found ONLY by scrub; 3.45%/32mo
  LSE rate), derived cadence, reverse index (device→chunk-groups) for
  repair; (e) copysets: random R=3 @5K nodes = 99.99% loss under 1%
  correlated failure vs 0.15% copyset — **copysets × HRW composition is
  NOVEL (confirmed absent from literature) — needs own loss-probability
  math + SIM sweep**; Tectonic's block-group scar (80% groups write-
  unavailable at 5% nodes down) = the fixed-set trap to avoid;
  **WALKTHROUGH LANDED 2026-08-17**: the gap is STRUCTURAL — the copysets
  literature assumes placement-as-assignment (authority records decisions),
  the HRW literature assumes placement-as-computation and never priced
  correlated loss (its failure cost was a cache miss); HRW's per-key
  pseudorandomness ≡ random placement = the 99.99% column. The tension:
  few distinct R-sets (loss probability) vs many repair partners per node
  (scatter width/exposure window), under Cidon's CONSERVATION LAW
  (expected loss constant — copysets reshape frequent-small into
  rare-large events). PARTIALLY SOLVED BY ACCIDENT: chunk-group
  indirection already bounds copysets at ~group_count (~9% of triple
  space at 100 devices — better than random-over-chunks, far from
  Cidon's few hundred); and the authority objection DISSOLVES — a
  shuffle is a pure function of (inventory-map epoch, seed), locally
  derivable by every node: candidate lists from seeded shuffles,
  weighted HRW *within* the list, promotion order preserved —
  coordination-free placement survives, copyset count becomes a DESIGNED
  quantity. THREE WORK ITEMS (no precedent): (1) the loss formula for
  our shape — weighted nodes, hierarchical domains, small-N regime
  boundary (at N=5, C(5,3)=10 — machinery inert; derived fleet-size
  threshold below which bounding adds nothing; laptop far below it);
  (2) MOVEMENT ANALYSIS — the delicate part: candidate lists must be
  stable under single-node churn (fixed seeds, lists patched not
  rebuilt) or naive re-derivation breaks HRW's w/W movement bound;
  FS10 must hold WITH bounding; (3) scatter-width knob — choose S from
  repair-bandwidth anchors to meet the derived exposure-window bound,
  minimize copysets subject to it; SIM correlated-failure sweep (kill a
  domain, measure loss events + repair completion across seeds).
  Risk LOW (parts individually proven, oracle-testable in SIM); the
  reason for own derivation: the one claim that matters ("loss
  probability under a 1%-correlated event at OUR weights/domains/fleet
  = X") exists in no paper — X comes from a derivation at a definition
  site, never Cidon's Table 1 for someone else's cluster.
  **STORAGE-CLASSES REFINEMENT LANDED 2026-08-17** (resolves the
  per-class placement question): requirements genuinely DIVERGE per
  class — live VFS content (fast writes, short exposure, superseded at
  green-advance/landing) needs copyset math LEAST; archive/generations
  (existential loss) write in rare batches where bounded placement is
  affordable — the diagonal that dissolves the §(e) tension. VERDICT:
  **storage classes over ONE placement function, never two placement
  authorities** (two authorities = Sylk's two-content-stores fault
  class; breaks one-function law + laptop degenerate + FS10). The
  construction: place(group, class, epoch) = top_R(class) of
  weighted_HRW(candidate_set(class, group, epoch)) — live class:
  candidate_set = all nodes (pure HRW; copyset exposure ACCEPTED with
  its derivation written down: exposure window × write rate ×
  correlated-failure probability vs class loss cost); durable classes
  (generations/archive): shuffle-derived bounded lists (the copyset
  knob) + per-class R/EC/scrub; registry class: R for truth + mirrors
  for reach. Precedents: Tectonic per-call policy on one substrate
  (RS(9,6)/RS(3,3)/3-way-reencode through ONE Chunk Store —
  consolidation was the paper's thesis); Ceph one CRUSH + per-pool
  rules. Declaration point EXISTS: registry descriptors carry storage
  class, boot-validated (chokepoint law — undeclared kind fails
  startup). RESOLVES §(e): copyset work only needs correctness in the
  durable regime (batch, movement-tolerant = the easy case); the hard
  regime (high-rate churn + bounded lists) is no longer needed. **FINAL REFINEMENT (user's cut, agent-validated, 2026-08-17)**: the
  one-placement-function law = one AUTHORITY (a single pure function
  computed identically everywhere), not one policy — the function takes
  storage class as a durable input. THE LOSS INTEGRAL decides the
  disciplines: expected loss ∝ correlated-event rate × exposure time ×
  copyset coverage — (i) WORK class (green chains, sealed increments,
  session state: hours–days exposure, session-bounded blast radius) =
  pure weighted HRW unchanged, keeping locality/movement/zero-lookup
  where the serving path needs them; (ii) LINEAGE class (registry
  content + KG/vector generations + archives: months–years exposure,
  monotonic accumulation, cold ⇒ scrub-stretched windows) =
  copyset-bounded HRW HERE AND ONLY HERE; (iii) COLD TAIL = EC across
  domains (already a third discipline by prior decision — the per-class
  precedent was internal all along). DISSOLVES two of three work items:
  movement analysis (bounding now scoped to cold content = background
  re-placement paced by the repair scheduler, zero serving-path/FS10
  tension; work class keeps HRW's movement guarantee verbatim) and the
  loss derivation (narrowed to lineage-class parameters — the
  friendliest regime: cold, append-mostly, repair-paced). GUARD RAILS
  (the Sylk two-stores fault in a new coat, held out): class = property
  of the content's ROOT, recorded in manifest/descriptor at write time
  (registry storage-class hook exists), never a runtime heuristic,
  never a second authority — place(map_epoch, class, group_id) stays
  pure and deterministic on every node; class transitions ride EXISTING
  lifecycle boundaries only (landing/archival promote work→lineage;
  seal-then-reencode / f4 lock-then-migrate siblings; no new state
  machine); laptop degenerate CLASS-BLIND BY COLLAPSE — labels persist
  inert, so a laptop corpus later joining a fleet re-places correctly
  from recorded classes; cache roles orthogonal (class governs
  authoritative copies only). **SUPERSEDED BY THE TWO-PLANES VERDICT (user-driven convergence,
  2026-08-17)** — the copysets×HRW 'named gap' is WITHDRAWN as a
  research gap and recorded as a design lesson: it was a symptom of
  artificial unification — no coherent system needs both disciplines
  for the same data; factored correctly, each plane falls back on its
  own literature's PROVEN construction and the novel composition
  evaporates. THE TWO PLANES: **serving plane** (work volumes, green
  chains, tools, cache hierarchy, DAX) = weighted HRW, SERVING.md §6
  STANDS UNCHANGED — zero-lookup/locality/minimal-movement where the
  turn path needs them, short exposure, session-bounded blast radius;
  **durable plane** (registry content, KG/vector generations, lineage
  baselines, archives) = **assignment-based copyset placement AS
  PUBLISHED** (Cidon/Tiered-Replication construction, chosen scatter
  width, upmap exceptions, map-driven repair) over a small
  consensus-owned placement map — LEGITIMATE because nothing in this
  plane is on the turn path (registry resolution = summon/staging;
  generation fetch = background cache-fill; archival = background), so
  the zero-lookup requirement that forced placement-as-computation
  never applied; no new authority class (consensus already owns
  inventory map + refs); loss derivation = instantiate Cidon's formula
  with our parameters, not invent math. **THE ANTI-SYLK LAW RESTATED AT
  THE RIGHT LAYER**: the Sylk fault was an identity-layer fracture (two
  hash families) — the law lives BELOW placement: one content identity
  (BLAKE3), one CDC, one manifest encoding, one pack-volume engine, one
  wire verb set; dedup works across planes by construction; unified
  SUBSTRATE, separate FLEET DISCIPLINES (placement/durability/repair) —
  Tectonic's own factoring read correctly (unified chunk fleet + client
  library; per-tenant policy/metadata/redundancy kept separate). THE
  SEAM: content crosses at lifecycle boundaries only (seal =
  serving-plane; landing/archival/generation-publication/registry-
  provisioning = the durable-plane writes — same chunks, identity
  unchanged, placed per copyset map, ref flips; f4 lock-then-migrate);
  reads flow ONE direction (serving cache-fills FROM durable; never
  reverse); co-located small fleets need TrafficClass-style
  repair-vs-serving IOPS isolation (Tectonic Gold/Silver/Bronze);
  laptop = both planes collapse to the same local packs, plane labels
  inert. BRANCH 24 REFRAMES: 'design the durable plane as its own
  system' (what database-grade wanted); placement section = published
  copyset construction + consensus map; everything else delivered
  stands (pack format, four-rung write path, CacheLib governance,
  scrub/EC/GC, metadata collapse — now cleaner: the placement map is
  the one honest piece of placement metadata, and it's tiny). The
  storage-class parameter survives as the ROUTER of content to a plane
  at its lifecycle boundary. Honest cost: two fleet machineries to spec
  and test — but the second is SIMPLER than the composition it
  replaces. OWED: (1) durable-plane placement-map spec (Cidon
  instantiation, scatter width from repair anchors, map schema on
  consensus); (2) work-class acceptance derivation (exposure × rate ×
  loss-cost, written down); (3) SERVING.md cross-reference amendment
  (planes named, seam stated, §6 scoped to the serving plane); (4) SIM
  correlated-failure sweep per plane against its own bar; (f) GC =
  mark-and-sweep from roots (green chains + registry refs + seal
  manifests + generation pointers), NEVER cross-node refcounts; sweep =
  copy-forward; f4 crypto-erase composes with (i); (g) API = put/get/
  batch_exists/ranged_get/list/scan, NO append verb (large objects =
  ranged reads over manifest chunk lists); (h) only NEW metadata = the
  per-node reverse index (scan-derivable, sidecar-cached); (i)
  RECOMMENDATION (own settlement required): **scope-salted convergent
  encryption** — key = f(content hash, dedup-domain salt), domain = the
  legitimate sharing scope (lineage/user/global) = the isolation line;
  dedup survives within domain, salt defeats confirmation-of-file across;
  preserves crypto-erase per domain; (j) laptop degenerate clean via the
  format-role unification. Work plan S1–S8 on file; venue corrections
  noted (BlueStore SOSP'19, Shift ATC'23, LSE study SIGMETRICS'07).
  Branch 24 now DESIGN-READY: exchanges can open on the map above.
  **SPEC WRITTEN 2026-08-17**: `docs/specs/OBJECT_TIER.md` (presented for
  acceptance) — two planes over one substrate, pack-volume format +
  four-rung ladder + copyset map + scrub/EC/GC + seam + laptop, OT1–OT15
  test matrix; folds the four OWED items: (1) durable-plane placement-map
  section (Cidon instantiation, scatter width from repair anchors, map
  schema on consensus) = §4; (2) work-class acceptance derivation written
  down = §3; (3) SERVING.md cross-reference amendment landed (§6 scoped to
  the serving plane, planes + seam named; durable-origin bullet corrected)
  + VFS.md arena/pack-store tier reconciliation landed; (4) SIM
  correlated-failure sweep per plane = OT5 (permanent CI). Encryption ×
  dedup stays OPEN (spec §9 records the scope-salted-convergent
  recommendation; AC-6 blocks user content until settled).
- **25 hecate-wire encryption + security** — ADDED 2026-08-17 (user). The
  wire is the single protocol surface, so security lives in the protocol
  layer once, never per-subsystem (chokepoint law). Shape constraints from
  settled law: encrypt-always is an accepted cost-ledger burden; composite
  principals + scoped short-lived pod credentials (SUMMONING.md — agents
  never hold user credentials); warden decides boundary crossings
  pre-effect; sessions carry key roots (SESSIONS.md); the encryption ×
  dedup interlock (OBJECT_TIER.md §9) must compose with whatever key
  hierarchy this branch settles. Decisions: transport crypto + mutual
  authentication (node↔node, host↔pod, CLI↔harness), workload identity
  (who mints and attests a pod/agent/node principal), key hierarchy +
  rotation (session key root → channel keys; revocation on handoff/
  teardown), replay/downgrade defense in the codec's append-only evolution
  rules, and the pod-as-semi-trusted posture (sensor/warden asymmetry:
  tighten-only). RESEARCH FIRST when opened: Noise Protocol Framework
  (WireGuard lineage — static-key mutual auth without PKI ceremony) vs
  mTLS/rustls (note the cost-ledger blocking-rustls-egress constraint) vs
  QUIC; SPIFFE/SPIRE workload identity; ALTS (Google's
  service-to-service pattern); fencing/epoch interplay with Branch 20;
  key-rotation receipts from production systems.
- **26 Multi-modal media** — ADDED 2026-08-17 (user); **NARROWED 2026-08-17**
  by WIRE_FORMAT.md + TRANSFER.md acceptance: the transport is settled
  (submission, chunking, streamed vs multipart, resumability, witness
  semantics, ranged reads all live there — the branch inherits it). Remaining
  scope = content POLICY only: class-assignment policy, content-type
  verification (magic bytes vs declared), EXIF/metadata hygiene, parser
  sandboxing, the per-class chunk-policy table, media descriptor documents
  (MIME/dimensions/duration/codec referencing ContentRef). Original charter
  follows. Handling, submission,
  chunking, streamed vs multipart upload, encryption. Shape constraints:
  Designer volumes are work-volume-role outside merge machinery (VFS.md
  §3) with a Guardian-staged disk-overflow path; large-object *reads* are
  settled (ranged reads over manifest chunk lists — OBJECT_TIER.md §8);
  this branch owns the *write* mirror. Honest physics up front: CDC dedup
  is near-zero on compressed media (JPEG/MP4/PNG) — chunking policy must
  branch on content class (CDC for text/source, fixed-size framing for
  opaque media), with the policy recorded in the manifest, deterministic.
  Decisions: streamed vs multipart submission + resumability (witness
  semantics for a partial media upload — what is acked?), media manifest
  shape (progressive/streamable ordering), content-type verification
  (magic bytes vs declared — sniffing attacks), metadata hygiene (EXIF
  strip as a Guardian-gated default), parser sandboxing (image/video
  decoders are attack surface — decode only in deny-first pods),
  encryption per the §9 scope-salt model. RESEARCH FIRST: S3 multipart +
  ETag semantics, tus resumable-upload protocol, Google resumable
  uploads, content-sniffing attack receipts, ImageTragick-class parser
  CVEs, fixed-vs-CDC dedup measurements on media corpora.
- **27 Leader election revisit** — **NARROWED 2026-08-17** by CONSENSUS.md
  acceptance: the questions this branch chartered are answered by
  construction in CONSENSUS §6 (CAS-first vs lease+fence classification,
  epoch fencing at every resource, epoch-scoping law, boot-validated
  roster) and §1 (meta tree vs per-domain groups). REMAINING SCOPE = the
  build-time roster audit only: walk the actual subsystem list, classify
  every writer, confirm no subsystem needs an election the classification
  misses. Original charter follows. ADDED 2026-08-17 (user: "re-visit who
  needs leader election — in particular the tectonic-style FS for the
  registry and knowledge graph, the knowledge graph, knowledge forest,
  etc."). The audit roster and its current answers, to be re-derived not
  assumed: Branch 20's consensus group owns inventory map + refs +
  (now) the durable-plane placement map; ledger WAL rides the
  consensus-group API at every replica count (WAL.md §5 — leader =
  sequencer, 1-replica self-ack locally); per-session single-owner tasks
  (merge serializer, field service) are *ownership by construction*, not
  election; the Forest is explicitly no-consensus derived state (FOREST.md
  §5b); KG/vector generation pointers are ref-CAS. The question the
  two-planes lesson sharpens: **does ref-CAS + epoch fencing delete
  election needs the way HRW deleted Tectonic's Block layer?** — Tectonic
  itself runs *stateless* metadata services over a Paxos KV (no service
  leaders, consensus only in the substrate); Lance's conditional-PUT
  commits are election-free single-writer. Decisions: one consensus group
  vs per-domain groups (blast radius vs machinery count), lease-based
  single-writer vs election where a writer exists (merge serializer,
  landing heads, Sibyl arbitration), fencing tokens on every
  lease-holder effect, laptop degenerate (already: 1-replica group,
  same call path). RESEARCH FIRST: re-read Chubby/Biscuit notes on file;
  multi-raft sharding (TiKV) vs one group; ZippyDB shard ownership;
  Kleppmann fencing; epoch-based single-writer receipts.
- **28 Secrets handling** — ADDED 2026-08-17 (user): detection, storage,
  encryption. The structural law this branch must deliver: **secrets are
  structurally unable to enter durable proof** — the ledger, testaments,
  artifacts, scribe narration, Forest traces, and debug logs are all
  durable or derived-durable surfaces; redaction must happen at the
  emission chokepoints (witness/seal boundary, narration envelope,
  artifact attach), fail-closed, never as a post-hoc scrub. Shape
  constraints: pods receive scoped short-lived credentials (SUMMONING.md);
  the warden is the boundary enforcement point; registry Guardian staging
  inventories content — secret scanning joins that inventory; the durable
  plane's §9 scope keys are the storage substrate candidate. Decisions:
  detection mechanics (entropy + pattern + verified-provider probes;
  precision/recall targets — false positives poison agent workflows),
  disposition on detection (block vs redact vs quarantine, per surface),
  the vault (own encrypted store on the durable plane vs OS keychain
  locally — laptop degenerate), injection into pods (placeholder
  materialization at the serving boundary so agents see references, never
  values), rotation + revocation on session close/handoff, audit trail as
  claims. RESEARCH FIRST: gitleaks/trufflehog detection receipts, GitHub
  push-protection numbers, HashiCorp Vault / age / sops patterns (pattern
  only — no external dependency), per-OS keychain APIs, OWASP secrets
  guidance.
- **29 Authoritative gap analysis** — ADDED 2026-08-17 (user: "given all
  components"). Inventory-only branch, no new design: sweep every
  component (specs, branch entries, cost ledger, owed lists, ADRs)
  against a fixed rubric — research on file? spec exists? test matrix?
  acceptance criteria? laptop degenerate stated? fault-matrix cells?
  chokepoint coverage boot-validated? open decisions named with owners?
  — and classify every gap: undesigned / designed-unspecced /
  specced-untested / decision-open / owed-and-forgotten. Output = the
  authoritative gap ledger the walking skeleton re-presents against.
  Sequenced immediately before the walking skeleton; kept current from
  then on (a stale gap ledger is itself a gap).
- **30 Fault detection + recovery (fleet level)** — ADDED 2026-08-17
  (user). Scope: hosts and storage nodes — NOT pod drain, which is
  settled as one concept in two layers (AUTOSCALING A5 policy + PODS
  mechanism; agent replicas run inside pods). Shape
  constraints: the health plane is the signal substrate (HEALTH.md — one
  stream, judgment at the edges, content-free law); PROTOCOL.md already
  names a wire-level failure detector; the fenced, versioned inventory map
  (Branch 20) is the only authority that may declare a node's state —
  detection *proposes*, the map *disposes* (no component acts on its own
  suspicion; fencing epochs make stale actors harmless). Decisions:
  detection primitive (phi-accrual vs SWIM-style gossip vs
  lease-expiry-only — and whether the wire detector and fleet detector
  are one machine), **gray/fail-slow detection** (the hard case: a node
  that answers pings but serves at 1% speed — differential observability,
  peer-comparison latency ratios), declaration protocol (suspicion →
  quorum-confirmed → map epoch bump → fenced), recovery orchestration
  (who triggers what: durable-plane repair = map-driven under-replicated-
  first (OBJECT_TIER §4); serving-plane = successor promotion via the
  deterministic HRW order; session colocation-unit failover =
  checkpoint+replay paths already spec'd per subsystem), **recovery
  pacing** (repair storms are the named killer — Tectonic's 10%-
  reconstructed-reads cap and reservation-declines as the receipts;
  derived repair-bandwidth floors vs serving TrafficClass), and the
  laptop degenerate (detector runs, declarations are local no-ops,
  R_eff=1 loud). RESEARCH FIRST when opened: phi-accrual (Hayashibara),
  SWIM + Lifeguard (memberlist's false-positive fixes), gray failure
  (Azure differential-observability paper), fail-slow-at-scale (FAST'18
  — fail-slow hardware receipts), Ceph OSD heartbeat/mon declaration
  flow, correlated-recovery pacing receipts.
- **31 Replica handling** — ADDED 2026-08-17 (user). The two planes have
  distinct replica lifecycles and this branch owns both, plus the
  cache-warmth tier that is NOT replication: (i) **serving plane,
  mutable side** — journal-ship to top-(R−1) HRW successors, promotion
  by the deterministic order (SERVING.md §6): the promotion protocol
  needs its fencing story (epoch token on every successor effect;
  split-brain unrepresentable), divergence detection for shipped
  journals (chained CRC + seq continuity), and re-ship on successor
  loss; (ii) **durable plane** — copyset members (OBJECT_TIER §4):
  read-repair on verify-fail, map-driven re-replication
  (under-replicated-first), **hinted handoff rejected and recorded** —
  immutable self-verifying content re-places from any valid copy;
  hinting is a mutable-store concept with nothing to buy here; (iii)
  **cache warmth** (pinned query nodes, mirrored routing artifacts) —
  explicitly not replicas: loss = re-warm, never repair; the boundary
  stated structurally so cache copies never count toward R_eff.
  Decisions: R derivations per class (from the class loss integral +
  copyset math, at definition sites), read-repair semantics (inline vs
  queued), replica verification cadence tie-in to scrub, cross-domain
  placement invariants under exception-table pins, and rebuild-vs-
  serving isolation floors (shared with 30's pacing). RESEARCH FIRST:
  Dynamo read-repair + anti-entropy (as the contrast — what mutability
  forced), Cassandra hinted-handoff failure receipts, Ceph
  backfill/recovery throttling, TiKV replica scheduling.
- **32 Node lifecycle: resource provisioning, cordon/quarantine,
  drain/spindown** — ADDED 2026-08-17 (user). The inventory-map state
  machine for hosts/storage nodes — the operational verbs the fleet has
  implied but never specified. States and their laws: **provisioning**
  (join = probe-derived anchors first: WAL.md's ω derivation, device
  bandwidth/TBW, capacity, declared failure domain; admission
  Guardian-gated like any capability; a node without probe results
  cannot enter the map — constants-from-data made structural);
  **active**; **cordoned** (no new placements, serves existing reads;
  the safe default for suspicion and maintenance); **quarantined**
  (suspected-faulty escalation: serves nothing unverified, scrub-
  prioritized, contributions to R_eff excluded — feeds from 30's
  gray-failure verdicts); **draining** (re-place per plane discipline —
  durable: map-driven copy-out; serving: successor promotion + session
  colocation moves — then remove; drain completion is *verified
  emptiness*, never a timer); **retired/spun-down** (out of the map;
  re-join = full re-provisioning, no resurrection of stale state —
  generation-numbered node identity so a returning node's old chunks
  are re-inventoried by scan, never trusted). Transitions are map-epoch
  bumps (fenced, consensus-owned); weights follow state (cordoned
  weight→0 for new placement, unchanged for reads). **Two drain
  concepts, correctly factored (user correction 2026-08-17)**: (1)
  **pod drain** — one concept, two layers: policy (AUTOSCALING A5
  selects which replica pod, when) + mechanism (PODS init executes:
  finish-or-park claims, scribe flush, teardown) — agent replicas run
  inside pods, so "replica drain" IS pod drain, never a separate
  machinery; (2) **node drain** — this branch, independent: re-place
  data per plane discipline + move colocation units, which *causes*
  pod drains on the draining node as a consequence (node drain
  composes over pod drain, one direction, never a third machinery).
  Laptop:
  the single node is permanently active; cordon of the only node is a
  typed refusal. RESEARCH FIRST: Kubernetes cordon/drain semantics
  (naming precedent + eviction API), Ceph noout/norebalance/OSD
  out-vs-down distinction, Borg maintenance windows, Backblaze drive
  lifecycle stats, SMART predictive receipts (Google disk-failure
  paper — SMART's weak predictivity).
- **35 Git-compatible hosting of code** — ADDED 2026-08-18 (user). Hecate
  serves lineages as git-compatible repositories: clone/fetch/push against
  lineage heads and green state, backed by the object tier + lineage
  machinery — never a cloud-provider dependency (the no-cloud-pairing law;
  we host). Decisions to work: the object-model bridge (git SHA-1/SHA-256
  object identity vs our BLAKE3 CAS — mapping layer or dual-addressed
  store; pack-file generation from manifests), lineage↔ref mapping
  (lineage nodes as branches; landing vs push semantics — is a push a
  landing with conflict values? materialization as the fetch view?),
  wire protocols (smart HTTP + SSH, pack protocol v2), auth via the
  identity plane (enrollment identities, WIRE_SECURITY terminal path),
  where the git surface terminates (host-side service, never in pods),
  laptop degenerate (local repo = local materialization target, already
  law). RESEARCH FIRST: Sapling/EdenSCM (Meta's git-compatible
  client+server over EdenFS — THE lead reference), jj/jujutsu's git
  backend (already in our landing-engine lineage), gitoxide (Rust git
  implementation), Gitaly architecture, git pack protocol v2 +
  SHA-256-transition docs, GitLab/Forgejo hosting architectures.
- **33 Cross-node shared-volume attach (D-11)** — ADDED 2026-08-17
  (user: "have we even discussed the mechanics — we haven't"). Pods on
  different nodes attaching to the post-merge shared VFS volume:
  attach protocol, single-writer vs multi-reader fencing, coherence vs
  sealed-manifest snapshotting, carriage classes (bulk fill = QUIC per
  D-10; invalidation/lease control class TBD), laptop degenerate. Spec
  home = SERVING.md rider or own spec; settle before serving-plane
  implementation. Inherits D-10 carriage — does not reopen transport.
- **34 Distributed knowledge-forest access (D-12)** — ADDED 2026-08-17
  (user: "how do nodes query the knowledge forest? this isn't some
  arbitrary thing that exists in a vacuum"). Cross-node query/retrieval
  (request/response over QUIC per D-10), field-state/trace replication or
  sharding across nodes/regions, ordered (trace ingest) vs supersession
  (telemetry, bare UDP) split, Raft involvement for authoritative forest
  state (UDP control plane), retention locality, laptop degenerate.
  Settle with D-4 (FOREST whole-spec verdict). Inherits D-10 carriage.
- **36 Pod↔volume attachment lifecycle mechanics** — ADDED 2026-08-18
  (user; "digging into the mechanics ruthlessly"). The attachment object
  (VFS §3b, CONTEXT.md) worked to exact mechanics: the bind sequence step
  by step (claim validation → serving-layer instantiation → version pin →
  lease acquisition → warden scope-entry wiring → prefetch execution →
  virtio-fs mount handoff → accounting open); the attachment state machine
  (binding/bound/re-binding/draining/detached + failure states — bind
  refused, lease lost, version withdrawn, node evacuating); re-attach
  mechanics at increment boundaries and at pod migration; detach ordering
  vs pod teardown (what flushes, what drops, what survives); concurrent
  attachment limits + budgets (derived); attachment↔handoff interplay
  (context/performance handoff = re-attach under new epoch?); laptop
  degenerate. Every step gets its message flow, failure rows, and tests.
- **37 Volume provisioning lifecycle (both planes)** — ADDED 2026-08-18
  (user). How a volume comes to EXIST, per role, across the serving
  (EdenFS) and durable (Tectonic) planes: work volume provisioning at
  summon (journal allocation, extent index, budget charge); green
  provisioning at session create (chain genesis, session-group placement
  set); tools/Designer/scratch provisioning; the volume object's registry/
  directory home (who records that a volume exists — session directory?);
  version retention + withdrawal policy (which green versions stay
  attachable; interaction with merge-log truncation + GC roots); volume
  deletion/teardown across both planes (crypto-erase interplay, D-3);
  quotas + accounting rollup; provisioning failure modes (budget refusal,
  placement failure). Ruthless mechanics: exact allocation sequences,
  message flows, crash points.
- **32 Node lifecycle — WIDENED 2026-08-18** (user): now explicitly owns
  **node provisioning and abstraction expansion**: how a machine JOINS the
  fleet (enrollment identity mint, meta-tree/region-group registration,
  host stack bring-up order — store, wardens, QUIC endpoint, bare-UDP
  plane, boot classifiers — and what validates before the node accepts
  work); how the abstractions EXPAND over a new node (HRW weight
  introduction + movement bounds, copyset membership, scheduler shard
  assignment, cache warm-up policy); drain/decommission (attachment
  evacuation per Branch 36, journal-ship, lease handoff, copyset repair);
  node identity vs disk identity (the FAULTS disk-swap class); laptop
  degenerate = the one-node join is the boot path itself. Original
  charter (cordon/drain semantics, Ceph noout, Borg maintenance, SMART
  receipts) stands as the research-first list. Ruthless mechanics.
  CONSUMED-BY (2026-08-18): the SCHEDULER heterogeneity amendment
  (§1/§5a) consumes the host-profile actuator (class rebind = a mini
  node-join; convergence states in the inventory map) and the per-plane
  repair-suppression scopes (noout class) — mechanics owned here.
- **38 The laptop collapse (whole-system scale-down)** — ADDED 2026-08-18
  (user). The standing law — laptop = the DERIVED degenerate of the same
  code, no modes ever — has per-spec statements but no branch that works
  the whole-system collapse ruthlessly. Charter: (a) **the collapse map,
  end to end** — meta tree → one group (root ≡ region, depth-1
  failure-domain tree); session groups → 1-replica self-ack (WAL path
  unchanged); placement/copysets → R_eff=1 LOUD; green placement acks →
  self-ack; node-liveness fabric → self-support; hecate-quic → loopback
  sessions for terminal attach + in-process short-circuit for local
  delivery (router law); bare-UDP plane → loopback; **microVMs + wardens
  stay REAL** (the VM boundary is the isolation guarantee, not fleet
  machinery — never collapsed); serving → one store, arena + local pack;
  scheduler shard=1; autoscaler floors; forest/KG/vector local; single
  binary per ADR-0004. (b) **the resource envelope, derived** — pod/
  session capacity from machine anchors (RAM/cores/disk); per-pod microVM
  overhead measured per platform (libkrun/HVF/WHP); exhaustion = typed
  refusals, never swap/spill. (c) **process topology per platform** —
  what runs in which process on Linux/macOS/Windows; the cross-platform
  constraint as first-light gate. (d) **boot = the one-node join**
  (Branch 32's degenerate — same path, no special case). (e) **the
  no-modes validation discipline** — architecture test: no code path
  branches on scale, only on derived parameters; differential tests
  laptop ≡ fleet observable semantics (the CN9 pattern generalized
  system-wide); every spec's laptop-degenerate statement becomes a NAMED
  test — and the GAPS inventory's "not stated" column (PROTOCOL, MERGE
  pre-rewrite, VFS, AGENTS_RUNTIME, RANK, SKILLS_API, HEALTH) gets swept
  and filled as part of this branch. (f) **first-light budgets** —
  boot-to-serve on a reference laptop, ratcheted (OT15's discipline made
  system-wide). Ruthless mechanics; settles alongside the walking
  skeleton's P0.
- **39 Observability plane + mesh/pod telemetry integration** — ADDED
  2026-08-18 (user; surfaced during the heterogeneous-placement
  reconciliation sweep: the item had been discussed as appended but never
  recorded — the stale-ledger rule firing on the grilling log itself).
  Owns the operational-log/metrics/trace substrate that every spec's
  ratchet gates presuppose (SCHEDULER AC-7, OT15, RUNTIME baselines, the
  shared >10%-regression CI bars — all require it to exist before first
  light) and the mesh↔pod integration view: per-lane wire telemetry,
  seal-pipeline/enforcement-point counters, warden+sensor rollup as one
  observable system. Shape constraints: collection at existing
  chokepoints only (warden, sensor, applier decision records,
  parser-resident enforcement counters, hecate-quic lane stats — no new
  probes; HEALTH.md's consolidation discipline generalized); carriage per
  D-10 (telemetry = bare-UDP supersession class, already law);
  content-free law applies (operational telemetry never carries payload
  content — metadata-completeness extended to observation); cardinality
  and retention derived, never configured; operator query surface +
  terminal-path story; laptop degenerate = local ring buffers, same
  schema. Explicit non-scope: health judgment (HEALTH.md), fault
  declaration (Branch 30), detection math (Branch 14). RESEARCH FIRST:
  OTel data model as pattern-never-dependency, Monarch (VLDB'20) +
  Gorilla/Beringei for derived retention/compression receipts, eBPF
  zero-instrumentation collection receipts.
- **40 Universal caching (vault / registry / object-store read paths)** —
  ADDED 2026-08-18 (user). NOT greenfield — audit + unify + fill gaps:
  OBJECT_TIER already has CacheLib whole-volume FIFO + endurance-servo
  admission; VFS has the RAM-arena/pack tiers + EdenFS 4-tier read order;
  REGISTRY has revision-floor reads + bundle caching; SERVING has the
  attr/entry per-attachment validity. The branch owns the UNIFYING model
  (what is cacheable, coherence class per data kind — immutable-CAS
  cache-forever vs authority-state-never-stale-for-effects) and the VAULT
  gap: envelopes are immutable CAS content (cacheable freely, verified by
  name); authority/index state must NOT be cached stale for EFFECTS (the
  effect-fence handles it — the mount IS the secret cache, no second cache).
  Must compose with the non-interference law (per-class cache budgets, no
  cross-class eviction) + the single-surface law. RESEARCH FIRST: CacheLib
  (already on file), the immutability-deletes-coherence receipts (already
  on file), negative-caching hazards for secrets.
- **41 Vault credential rotation under replication** — ADDED 2026-08-18
  (user; "maximally correct… w.r.t. vault replication"). Depends on
  Branch 28 vault core. Owns: event-driven rotation mechanics (NIST 800-63B
  kills calendar rotation) under the replicated envelope/authority split;
  the AWS-Secrets-Manager version-staging primitive (AWSCURRENT/AWSPENDING/
  AWSPREVIOUS = atomic rotate: stage pending → test → promote); DYNAMIC
  secrets (Vault-style short-lived generated creds — the user's app DB cred
  minted per-lease); rotation coordination across the consensus-tree
  authority (rotate at the authority, propagate epoch, invalidate holders);
  rotation-vs-effect-fence interplay (a rotation IS an epoch bump). RESEARCH
  FIRST: AWS SM rotation/Lambda + version stages, Vault dynamic secrets +
  DB secret engines, rotation-under-async-replication (the meta-scale
  dossiers on file).
- **42 Vault credential types (AWS-Secrets-Manager parity)** — ADDED
  2026-08-18 (user; "support ALL of what AWS Secrets Manager supports by
  default"). Depends on Branch 28. The value model: opaque binary
  (SecretBinary), UTF-8 string, structured JSON k/v (the common case),
  plaintext — plus version-stages (shared with Branch 41) and per-secret
  resource policies (→ Branch 44 IAM). Precise mechanics: how each type
  seals into the envelope, how structured k/v is addressed/partially-read
  (field-level access?), size bounds (AWS SM caps 64KiB — ours derived),
  the type as metadata never affecting the effect-fence. RESEARCH FIRST:
  AWS SM value model + version stages + resource policies; Vault KV v2
  (versioned k/v) + the engine-per-type pattern.
- **43 Vault certificate issuance (ACM / PKI-engine analogue)** — ADDED
  2026-08-18 (user; "think AWS cert manager… precise mechanics"). A vault
  FEATURE, own branch for size. Owns: CA hierarchy (root/intermediate),
  issuance roles constraining what may be issued, leaf issuance +
  short-TTL-instead-of-CRL (the short-lived-cert school on file), ACME-like
  protocol for workload self-service, rotation/renewal, revocation
  (short-TTL + optional CRL/OCSP). KEY QUESTION: internal vs workload-facing
  — internally we use Noise (not X.509), so cert issuance is primarily a
  WORKLOAD feature (the user's services need TLS certs / the user's code
  needs a signing cert); does anything internal need X.509? Interlocks
  WIRE_SECURITY (identity plane) + Branch 44 (who may request issuance).
  RESEARCH FIRST: Vault PKI secrets engine, AWS Private CA + ACM, ACME
  (RFC 8555), SPIFFE SVID issuance, short-lived-cert practice (on file).
- **44 IAM — the universal permission plane** — ADDED 2026-08-18 (user;
  "effectively THE universal plane for managing permissions… the full
  gamut"). THE load-bearing authorization branch. **Unification mandate
  (not a sixth authority): Rank, SafetyPolicy, Guardian gates, Biscuit
  grants, and claim affordances each become a VIEW/INSTANCE of this one
  plane, or the branch says precisely why one cannot.** Full scope per the
  user: per-agent/per-pod/per-system role & secret allocation; **governing
  agent↔agent communication via policies + roles** (the PEP is the
  WIRE_SECURITY seal-once lanes + warden, already in place); **role
  assignment mechanics**; **role chaining/assumption** (STS-shape
  scope-down, confused-deputy avoidance); **using roles to govern external
  access** (egress, workload-identity-federation); **using roles + policies
  to govern the code repository** (Branch 35 lineage push/fetch/land,
  CODEOWNERS-as-policy, protected refs). Model question: ReBAC
  (Zanzibar-style relationship graph) as the universal substrate with
  RBAC/ABAC as views; policy language (Cedar — Rust-native + formally
  verified — is the lead candidate for our lint/verification wall); PDP on
  the consensus tree, PEPs already exist; deterministic evaluator =
  f(request, policy-epoch, relationship-snapshot) — versioned log inputs,
  effect-fenced (the meta-scale-secrets authz-consistency result applied).
  **UPSTREAM DEPENDENCY: reshapes Branch 28 grants, REGISTRY tenancy,
  cross-fence Biscuit grants — settle its model before those finalize.**
  RESEARCH LANDED 2026-08-18 (dossier in research index). **CHARTER
  CORRECTED BY THE USER (2026-08-18, verbatim): "we need to BUILD an IAM
  system. While it can integrate with portions of our framework, we have
  NO single, coherent control plane or device for managing roles,
  permissions, etc."** — the read-model framing was the architect's
  over-rotation, overruled and recorded: Hecate today has five enforcement
  mechanisms and ZERO management surface. Branch 44 BUILDS the first-class
  IAM system: (1) **the authority store** — roles, policies, role
  assignments, grants as first-class objects in the IAM plane's **own
  replicated store** (its own consensus group(s), scoped by the
  failure-domain tree like the vault index) — **never the ledger**; (2)
  **the management surface** — create/assign/attach/revoke roles and
  policies, role-assumption + chaining APIs, audit queries ("what can
  agent X touch", "who can touch resource Y" — the Zanzibar Read/Expand
  shape) — IAM-plane APIs with IAM-plane audit, **never claims**; (3) **the
  decision service (PDP)** — the deterministic evaluator
  f(request, policy-epoch, graph-snapshot), Cedar-shaped language (typed
  fail-closed variant), forbid-overrides + union-grants +
  intersection-boundaries + intersection-session algebra; (4) **compile-
  and-distribute** — decisions/policies compiled to the existing PEPs
  (warden, Guardian admission, merge gate, boot classifier, the ledger's
  claim-issuance guard — that last an IAM *consumer* enforcing on work
  operations, never IAM storage)
  with the measured invalidation SLO + epoch fencing (the effect-fence
  result applied whole); (5) **integration, not dissolution** — Rank/
  SafetyPolicy/Biscuit-grants/affordances become CONSUMERS governed by
  the plane (SafetyPolicy = a boundary-semantics policy the user owns;
  Rank = a shipped policy pack; Biscuit = the portable serialization of a
  plane decision; work facts — active claim scopes, session membership —
  enter only as PDP request-context attributes read at evaluation time:
  the ledger is never the authority store nor a store of any IAM object).
  **SECOND CORRECTION (user, 2026-08-18, verbatim): "the ledger is NOT
  for things like role and permissions control plane work. It is for
  driving agent work. Do NOT confuse the two."** — struck from the
  charter accordingly: claims-visible management ops, ledger-resident
  authority state, ledger-as-federated-relationship-source. The ledger
  drives and proves agent work; IAM is its own control plane with its
  own store, APIs, and audit. The dossier's unification map
  + Cedar/ReBAC/STS receipts stand as design inputs; the cannot-fold list
  stands (judgment, sensor tighten-only, user supremacy). Design exchange
  owed; vault-namespace dossier (LANDED 2026-08-18) feeds it (vault paths = one
  resource type IAM names).
- **Walking skeleton** — final branch; re-presents against completed tree
  (P0 wire → P1 runtime → P2 spine → P3 pod leg → P4 first agent → P5 first
  merged change; now must thread Sibyl/home-session/lineage into first light;
  each rung carries fault-matrix cells; consumes Branch 29's gap ledger).
- Small owed: full "Guide summons" language sweep — **DONE 2026-08-17**
  (grep pass run: one violation fixed — SUMMONING.md sandbox gate "every
  spawn" → "every sandbox summon"; remaining hits verified legitimate:
  process-level spawn in PODS/RUNTIME, deliberate session-creation
  vocabulary in SIBYL/SESSIONS, AGENTS.md's "no Orchestrator" denial);
  ADR candidates (sessions/lineage+landing engine; deterministic
  optimism; forest; open roster/offices) — offer per ADR rules.

## Cost ledger (accepted burdens; check every new decision against these)

Owned wheels: runtime+SIM, claims protocol, hecate-wire codec, merge engine +
verdict theorem, **landing engine (a second merge machine — distinct verdict
surface: eg-walker replay + jj conflict algebra; accepted deliberately, opposite
regime from the gate)**, **the serving machine (FUSE-over-virtio layer +
log-structured overlay + mapping engine; rides owned WAL/chunk-store/fork —
new surface, not a new stack)**, Z-set field engine, forked VMM stack (WHP =
risk cell), sharded scheduler. Managed-window mapping mode = deliberate
portability concession (one copy per 2 MiB miss on unproven platforms; the one
mode where DAX + full witnessing coexist). Compounding: walking-skeleton first light is far behind the wheel
count — acknowledged repeatedly, accepted under "we do not fear complexity."
Branch-20 acceptance costs (2026-08-17): minority-region root operations
stall during WAN partition (closed, enumerated, human-cadence list — CN13
polices it); region loss forfeits unlanded work within the measured
seal→replication lag (priced by the OBJECT_TIER §3 formula, ratcheted);
the meta plane is a tree of groups rather than one group (one
implementation, tree-derived, laptop-collapsed); the conformance suite
(CS1–CS12) is a permanent, append-only maintenance surface; fortification
is election-amortization only — the lease-read latency win CRDB harvests
from the same fabric is deliberately left on the table (fabric stays off
the safety path).
Other standing costs: encrypt-always CPU; per-increment validation; max/ultra
primary models; full-machinery-locally (degenerate consensus, session infra
floor — ratcheted budget); shard-local placement optimality (slow rebalancer);
two-phase arena lookups; tokio ecosystem cut off (blocking rustls egress);
**own S3-level object tier (user directive 2026-08-17: never pair to cloud
providers — the chunk store IS the object storage; two planes over one
substrate per the 2026-08-17 verdict — serving plane origin = authoritative
HRW groups, durable plane origin = consensus-owned copyset map
(OBJECT_TIER.md); erasure cold tail + scrub + repair owned; two fleet
machineries to spec and test, accepted — the second is simpler than the
composition it replaces; cloud only as an optional registry-declared
external import source, never a dependency; SERVING.md §6 amended twice)**.

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
S*/RTV/PDR numbers; composition correction); FS serving ×4 (EdenFS internals,
CitC/Piper, virtio-fs/DAX/libkrun, sharded CAS/placement — baked into
SERVING.md); **vector distribution ×3** (2026-08-17: DiskANN family primary
texts incl. DistributedANN/BatANN; IVF routing + quantization + filtering —
FAISS wiki verbatim, SOAR, RaBitQ, ACORN/Filtered-DiskANN, Big-ANN'23;
production architectures — turbopuffer/Pinecone/Lance/Milvus/Vespa/Qdrant —
baked into Branch 22 + VECTOR_INDEX.md); **storage ×3** (2026-08-17:
Tectonic FAST'21 full read + Haystack/f4 + Colossus/ShardStore contrasts;
EdenFS tier mechanics from repo docs — overlay/hgcache/indexedlog formats,
materialization states, takeover, pain list; node formats + caching + EC —
Haystack/ShardStore/BlueStore verdicts, CacheLib/Shift, copysets/LRC/Clay,
LSE/scrub — baked into Branch 24 + OBJECT_TIER.md; venue corrections noted
inline); **Sylk decay post-mortem** (2026-08-16, for the FOREST decay
examination): SEVEN mutually inconsistent decay impls, only one ACT-R-shaped
and it has a seconds-vs-hours unit bug (~4 nats; 17-day intended retrieval
window → 6.7 minutes actual; domain-dependent offset breaks cross-domain
comparability); reinforcement path never wired (traces empty → whole stack
degenerates to Score×0.7); learning primitive = EWMA mislabeled as posterior
(α+β→1, Confidence()→0 permanently after ~21 obs); half-life off-by-ln2 twice
contradictorily in one file; 4/7 impls exponential while docs forbid it; the
most detailed doc spec (Archivalist Knowledge Decay Protocol) never shipped;
6+ subsystems built-tested-unreachable. 15 named lessons → become named tests
in the successor decay spec. VERDICT IMPLICATION: Sylk is evidence about
implementation discipline, NOT evidence against ACT-R-the-model; the
best-fit question stays open pending the literature report. **Decay
literature report LANDED** (2026-08-16): ACT-R form scores BELOW a
constant-prediction baseline on the only large head-to-head (350M reviews:
LL 0.4033 vs 0.3945, AUC 0.52); three literatures converge (MCM/DASH,
marked Hawkes w/ exp-mixture power tails, LRFU/TinyLFU/forward-decay) on ONE
object: clamped signed multiscale decayed-trace score w/ saturating gain;
K=O(log range) registers (Beylkin-Monzón), DASH-recipe convex GLM fitting,
TinyLFU duel admission, Soar crossing-time retirement; FSRS = ranked alt #2
(lapse-collapse kept as negative-gain rule). Recommendation presented as the
FOREST retention-model exchange — awaiting user verdict. **Sylk handoff
post-mortem LANDED** (2026-08-16, for Branch 14): 0 performance handoffs in
9,780 WAL observations over 3 months — the doc'd detector (ShouldTakeAction,
peak zones, degradation thresholds) NEVER EXISTED (zero grep hits); shipped
trigger = GP.mean < 0.5 point comparison; 2 of 3 signal channels have ZERO
producers (StreamMetrics never assigned anywhere; behavior channel never
called); surviving signal 97.05% constant 1.0; threshold frozen at Beta(2,2)
prior = 0.5 across 9,204 checkpoints (split-brain profiles: learner's copy
updated, controller's read; plus zero-value bool gate skipping every update);
GP prior mean = constant 0.7 > threshold (trigger unreachable where data
sparse); context-size feature corrupt (83% of values <100 tokens — counted
msg content only); throttle armed BY the low-utilization bug; provenance
erased on the 7 real (context-limit) handoffs; the one green test runs a toy
regime with the confidence gate disabled; the real trend detector
(GetTrend/IsTrendingDown least-squares slope) exists with ZERO consumers.
16 named lessons → Branch 14 spec tests. **Branch 14 detection-literature
report LANDED** (2026-08-16): degradation is carried by accumulated context
(sharded-vs-oneshot −39%; aptitude −16% vs unreliability +112%) ⇒ replacement
is the right intervention class; best-evidenced signal = state-action
recurrence (MAST 17.14%, OpenHands 4/3/3/6 thresholds in prod — only
content-level detector shipping anywhere); NO production harness does
automated mid-task replacement (Hecate builds ahead of precedent);
Anthropic API has NO logprobs — entropy detectors unavailable and
wrong-direction for loops; the math verdict = **risk-adjusted CUSUM**
(Steiner 2000 — built for the case-mix/task-difficulty confounder that
killed Sylk) with h = ln(ARL0) thresholds DERIVED from a per-session
false-trigger budget δ (ARL0_i = T/δ_i, refined Brook-Evans/Monte-Carlo,
DPCLs if mix volatile); BOCPD rejected (no false-alarm guarantee = hand
constants again); fusion = priced K-of-N vote, never T²; Guardian
adjudication = SPRT-shaped with the **fresh-context probe** as the single
evidence request (the causal task-hard-vs-agent-degraded discriminator);
commissioning via self-starting + fleet priors + FIR head-start on reset.
Five-tier pipeline fully specified in the report. **Forest-design corpus
READ in full** (2026-08-16, user directive): ECOLOGY.md (antigenic field,
L-V competition, hybrids, photosynthesis invariant, disturbances, CSD,
forest-as-participant), EMERGENT_FOREST.md (interaction-nodes, valenced
edges, emergent density clusters + naming-as-gate, stages, PoI views,
C/N/P/W channels, BCM/Turing/allelopathy, open questions), EMERGENT_AGENCY
(cursor-in-baggage ambient, precedent→validation priors, stage→claim
severity, brittle→maintenance claims, contradiction→Architect remediation,
overrides-as-signal). FOREST hybrids marked PROVISIONALLY DIRECTED pending
the reconciliation exchange (presented). **Reconciliation research pass
DISPATCHED ×3** (2026-08-16, user directive — alternatives/mechanisms/
improvements before settlement): (A) structure layer — clustering at bounded
deterministic scale (HDBSCAN family vs Leiden/graph-community vs exact
linkage; fused embedding+edge similarity question), cluster labeling,
stage-band threshold/hysteresis derivation, PoI mechanisms (Kleinberg burst,
incremental betweenness, sleeping-beauties brittleness); (B) propagating
invalidity — CHALLENGE to the antigenic-field formulation: TrustRank/
Anti-TrustRank/Guha distrust as PPR-seed-set alternative (no learned head),
label spreading closed-form, the honest AIS record, incremental Fiedler/
λ_max monitoring, retraction-contamination + clone-defect propagation as
the receipt domain for whether invalidity actually propagates; (C) ecology
dynamics stress-test — L-V outside biology (predictive or merely
descriptive; simple supersession alternative), CSD false-positive record
(Boettiger-Hastings prosecutor's fallacy; data requirements), conservation
invariants prior art, multi-scale gain control (Go GC pacer, autovacuum).
**Track A LANDED 2026-08-17**: clustering verdict = **fused-similarity exact
HDBSCAN\*†own-impl** (pairwise → Prim MST → condensed tree → EOM +
cluster_selection_epsilon) over d_fused = d_cos × φ(typed-edge strength),
fixed-point, (weight,id,id) tie-breaks — RNG-free, exact at session scale
(ms–s recompute; no incremental machinery justified <10⁵ items), ONE
structure serves five consumers (soft membership→bridges, GLOSH→outliers,
FLASC flares→frontier, DBSCAN\* slices); approximate_predict placement
between debounced recomputes; **MONIC overlap-matching for lineage**
(evolutionary clustering REJECTED — smuggles path-dependent state; cluster
fresh, then match); Leiden = seeded cross-check alternative #2 (Louvain
rejected: 25% badly-connected/16% disconnected defect; UMAP rejected:
stochastic + thread races; streaming variants rejected: lossy
order-dependent). KEY INSIGHT: contradicts edges are ATTRACTION for topic
clustering (same subject); stance/faction = separate signed-graph question
(frustrated-edge counting linear+exact; SPONGE only above derived density).
Labeling: deterministic c-TF-IDF machine label + LLM curator name at
promotion gate (LLM labels beat NPMI/C_v which are receipted-broken), name
= ledger claim bound to MONIC lineage. Stages: KM maturity models =
receipted vapor; citation-dynamics prior art (Ke sleeping-beauty B
coefficient, parameter-free) → continuous scores, quantile bands, ratchet
promotions, EWMA two-threshold hysteresis w/ derived gap (NIST/Nagios).
PoI: Kleinberg batched burst DP (deterministic Viterbi; ln decomposes to
per-recompute constants via own fixed-point ln — libm transcendentals
receipted non-deterministic in Rust), exact Brandes + k-core + quantile
Guimerà-Amaral roles, inverted sleeping-beauty brittleness, FLASC frontier.
Implementation: i8-quantized embeddings + integer similarity (bit-exact),
Q32.32, content-hash IDs, composite-key sorts, brute-force top-k (Faiss's
own guidance at this scale), no ANN ever. Thin-evidence list on file (11
items, incl. brittleness construction = ours not literature). **Track B
LANDED 2026-08-17 — the antigenic field is REPLACED**: verdict = **two-field
seed-set PPR** — corruption = PPR from contradiction/pathogen seeds
(Anti-TrustRank, which BEAT TrustRank per unit labeling at every recall
level) + immunity = PPR from validation seeds (TrustRank), both over one
composite reversed-provenance kernel (derivation edges heavy ⊕ co-derivation
siblings [Guha's 0.4 co-citation receipt + clone receipts] ⊕ semantic-kNN
over pinned embeddings small ⊕ agent-authorship smaller/longer), α≈0.85,
out-degree splitting; infection q(v)=max(0, c−i); superposition = per-
pathogen attribution + exact cure subtraction; ACL forward push + O(1)
amortized incremental (Zhang-Lofgren-Goel) — unifies with existing PPR
machinery, ZERO learned components (learned pathogen head unearned: AIS/
negative-selection receipted underperforming simple baselines — Stibor).
**contradicts edges are ONE-STEP ONLY** (Guha: transitive distrust
semantically broken; one-step won at 81-scheme scale); derivation chains
carry steep geometric decay — CALIBRATION ANCHORS from retraction studies:
hop-1 heavy (93.6–96% of post-retraction citations unaware, 3 studies),
hop-2 content ≈ absent (use induces direct edges — van der Vet full-network
case), semantic spillover ~10× weaker (Azoulay 5–10% lasting decline),
author channel ~7%/yr to 4 hops (Lu), cure conditioned on invalidation
PROVENANCE (self-report penalty vanishes entirely — Lu). **Fiedler-drop
outbreak detection was WRONG**: licensed statistic = s = C_field·λ₁(W_corr)
vs 1 (Wang SRDS'03 + Prakash G2-threshold theorem, 25+ models); fixed-seed
power iteration, Weyl skip-gate; Priebe scan statistics for localized
attribution; DeltaCon for drift; quarantine interventions ranked by λ₁
eigendrop. **ATMS hard channel** (de Kleer): sole-support closure of a
collapsed-S item = hard-OUT deterministically; else graded retrieval
demotion (1−q)^γ, continuous internally, discretized only at action edges
w/ hysteresis (Guha: rounding step 'of significant importance'). Clone-
defect receipts (Juergens ICSE'09: 52% clone groups inconsistent, ~half of
unintentional = faults) ground graded-not-hard sibling suspicion. Thin:
graded-vs-hard retrieval A/B absent; hop-2 decay = the number to re-measure
from own harness data. **Track C LANDED 2026-08-17**: (a) **L-V REJECTED**
— unidentifiable (n(n+1) params vs tens of ticks; Remien; Van den Bulte
bias), descriptive-not-predictive across language/market/meme domains
(Abrams-Strogatz concedes bilinguals exist; Prochazka-Vogl abandoned ODEs
with fine data; winner-take-all emerges from budget+reinforcement alone —
Weng/Gleeson/Tria), internally broken (cosine α is SYMMETRIC under an
asymmetry claim — MacArthur-Levins 1967 is the asymmetric form; endogenous
K_i voids the regime taxonomy; reframed near-duplicates sit on the α·α≈1
knife edge; ODE extinction contradicts never-delete doctrine; Connell 1980
miscited — it's the SKEPTIC's paper, barnacles = Connell 1961).
REPLACEMENT: asymmetric ML-overlap as evidence + activity-share crossover
w/ derived hysteresis + dwell (HPA anti-flap) + supersedes edges/regime
events w/ bi-temporal cooling + co-activation as mutualism/bridge
protection. (b) **CSD KILLED as a trigger** — wrong tipping class (our
shifts are exogenous N/R-tipping where theory says no warning: Ashwin,
Hastings-Wysham, Ditlevsen-Johnsen), wrong statistic (AC×variance product
= exactly what D&J prove invalid), no data (needs 10²–10³ stationary
points; we have tens, nonstationary by construction), measured field
record 9–13% TP / ~50% FP (Burthe 126 datasets; Gsell best-monitored
lakes; Wilkat 105 seizures: nothing). Alternative = CUSUM-class w/
ARL-derived thresholds on mechanism-specific signals (contradiction mass,
correction rates, share crossover) — the Branch-14 discipline reused.
(c) **CONSERVATION INVARIANT ADOPTED** — it IS input-to-state stability
(Sontag) / conservation-of-packets (Jacobson 1988: fixed the 1986
congestion collapse, superposition-stable — THE deployed receipt);
adaptations: conversion rates FITTED never the High/Med/Low grid,
token-bucket semantics at the single influence-minting chokepoint (RFC
2697), hierarchical budgets (global + per-cluster τ_min floors), stated as
ISS storage-function obligation + property-fuzzed CI assertion beside F21;
provenance honesty: per-place bounds are literature (Brueckner/MMAS),
the GLOBAL ledger is our trivial corollary. (d) **CLIMATE: intent adopted,
plumbing replaced** — paced-debt stays primary (autovacuum precedent),
windows DERIVED from rate-ladder scales never wall-clock hour/week
(session lifetime!), robust order statistics (BBR max/min not means), PI
integrator + dead-band + stabilization window (Go GC pacer: proportional-
only provably can't kill error; Hollot PI-AQM), superlinear compensation
for the closed digest→activity→reinforcement loop (BCM stability
condition), Fourier seasonality dropped v1. ECOLOGY.md fact-check
corrections on file (Connell, α asymmetry, unsourced coral-CSD claim,
hand constants). ALL THREE TRACKS LANDED — final reconciliation map
presented for ruling.

**Consensus re-analysis dossier LANDED (2026-08-17, for the Branch-20 etcd
challenge)** — every challenged failure mode classified by layer: (a)
etcd-server/boltdb/watch, (b) etcd-raft-library, (c) single-group-topology.
FINDING: the famous record is overwhelmingly (a)+(c) — v3.5 silent data
inconsistency = server apply-loop watermark race (consistent index persisted
before entry effects; official postmortem: corruption detection experimental
+ off, functional tests "unmaintained, flaky"; the class decisions (2)+(5)
exist to make structurally impossible); boltdb 8GB ceiling/mmap/blocking
defrag/freelist O(n) (Alibaba rewrote it → 100GB) = backend; k8s stale-reads
(#59848)/LIST OOM (KEP-3157)/OpenAI Events-split = watch layer + one-keyspace
topology; 5–7 voter + single-group ceiling = topology the direction already
rejects. The (b) record is real, short, enumerable: apply-time conf-change
liveness hole #12359 (closed STALE — countermeasures = conf-commit metadata
on votes, no direct voter demotion), PreVote stuck-states #8243/#8501 (fixed),
ReadIndex/learner #10589, probe stalls #13418, transfer-bypasses-PreVote
carve-out; protocol-level: Ongaro single-server-change guard,
PreVote+CheckQuorum joint requirement w/ asymmetric-omission residual
(Decentralized Thoughts + Cloudflare/HAOC'21). META-SCALE TABLE: every
property the scaled systems share and etcd lacks (multi-group: Spanner ~1000
groups/node since 2012, CRDB hundreds of thousands; liveness amortized above
the group: CRDB store-liveness/fortification SIGMOD'26, TiKV hibernation
retrofit w/ #10017 as the retrofit-bug receipt; storage decoupled: Delos
loglets/raft-engine/pebble; reconfiguration-as-data: Delos VirtualLog;
epoch-fenced writers: ZippyDB/LogDevice/Chubby) is already in the direction
or now amendable. AsyncStorageWrites (the adopted interface shape) was
authored BY CockroachDB (PR #14627). Exemplar options graded: cockroachdb/
raft fork (active, TLA+-backed fortification work, Go), tikv/raft-rs (Rust
portability proof, pre-AsyncStorageWrites, joint-consensus long experimental),
from-scratch-to-dissertation (forfeits decade of (b) fixes unless checklist
= conformance suite), VSR/TigerBeetle (Jepsen-clean core but single-group,
Zig; its real export = VOPR/FDB deterministic simulation posture). CANDIDATE
AMENDMENTS: 2a re-name exemplar "CRDB-lineage dialect"; 2b (b)-record +
protocol checklist as executable conformance suite; 3-addendum explicit
conf-change activation semantics + #12359 countermeasures; 5a upgrade gate
to deterministic whole-cluster simulation (FDB ~1 trillion CPU-hours;
TigerBeetle VOPR; mutually reinforcing with the pure-core IO-as-data shape).
Full dossier with ~35 primary sources in-conversation; re-presentation =
the pending exchange.

**Cross-region receipts verification LANDED (2026-08-17, the CONSENSUS §7
rider)** — A Physalia CONFIRMED verbatim (P(Av|Ai) placement, same-side-of-
partition, blast radius; precision note: intra-AZ system, region-level is our
extrapolation of the same argument); B Chubby CONFIRMED exact (global cell =
mirrored ACLs/refs/directory, "five replicas... widely-separated," 250ms
antipodes vs <1ms local — the meta-tree precedent verbatim); C Spanner
CONFIRMED (F1 leader re-placement quote; witness replicas in OSDI'12 §2.2
itself; placement driver = minutes cadence; honest caveat: Spanner IS the
sync-WAN counterexample pole); D async pole CONFIRMED (S3 CRR async, RTC =
15-min SLA — quantifies exposure_window; DynamoDB MREC async/LWW default
with opt-in MRSC nuance; f4 §5.2 XOR-across-regions of sealed immutable
volumes = the exact pattern; Tectonic datacenter-scoped); E non-failover
CONFIRMED on Borg ("A job runs in just one cell") + K8s (replacement-not-
migration, region loss out of cluster scope) + F1 (Shard Manager/actor
practice THIN). F FlexiRaft **CORRECTED — rejection survives, reason wrong**:
enforced commit/election quorum intersection makes region failure
UNAVAILABILITY not loss ("(data loss)" appears only for the violated-
intersection hypothetical); correct two-branch argument = (1) fencing
authority unavailable exactly when most needed, (2) permanent destruction ⇒
forced reconfiguration abandons committed tail ⇒ monotonicity break as
operator consequence; and only DYNAMIC mode is rejected — static
multi-region FlexiRaft is the same species as the meta tree's own groups.
G scoping-law precedents CONFIRMED (Clark fate-sharing verbatim, Chubby
lock-delay + sequencers, K8s cluster-scoped Leases, Dynamo surfaced-
conflicts vs global-tables-LWW anti-pattern, CRDB region-survival pricing);
zombie-region safety argument **CORRECTED — three holes**: (H1) pre-
partition materialization lease = safety-by-waiting not construction (root
re-grant must wait lease expiry + derived clock-drift margin; Chubby
lock-delay precedent); (H2) fencing protects only token-checking
chokepoints — externalization channels (git push, external APIs) must be
landing-class fenced chokepoints or safety covers archive state only;
(H3) fate-sharing covers death not resurrection — need explicit rejoin
protocol (dead-declaration = root-quorum + terminal region epoch; heal =
rejoin under NEW epoch; zombie unlanded work = fork branches only, never
continuations). §7 REOPENED per the rider; six-amendment set presented
for verdict.

**Bulk-transport dossier LANDED (2026-08-17, the PROTOCOL class→transport
exchange)** — four workstreams, primary receipts. Receiver-driven transports
(Homa/NDP/pHost/Aeolus): TCP indictment is real but scoped to SHORT-message
tail latency (Homa P99 7–83× better) — at large messages Homa/Linux loses
2:1 to TCP+TSO in its own paper (10.0 vs 20.3 Gbps @500KB; "software
congestion" binding; headers mimic TCP to steal TSO); receiver credits DO
bound incast by construction (ToR ≤ overcommit×RTTbytes; ExpressPass
near-zero buffer) with the first-RTT-unscheduled residue (Aeolus: one
scheduled drop = 100× FCT); ZERO production deployments — hyperscaler
TCP-escapes are hardware-coupled (Azure 65% RoCEv2; Google Snap→Falcon HW).
QUIC: RFC9002 mandates loss-detection machinery not CC (Cubic default in
every stack); HOL wins real on lossy paths (YouTube rebuffers −18%) but
INVERTED on fast clean links (WWW'24: up to 45.2% slower, gap grows w/
bandwidth); UDP throughput parity needs GSO/sendmmsg batching (Fastly 196
vs 466 Mbps pre-optimization); stacks = 5–8yr multi-MB efforts; iroh (our
closest relative) runs BLAKE3 verified streams over QUIC and built its own
QUIC (noq) rather than raw UDP. Storage census: TCP-parallel is
near-universal (S3 CRT saturates 100Gbps via parallel connections; HDFS/
Ceph/MinIO/GridFTP; Meta QUIC = edge only); shipped UDP bulk = WAN niche
(Aspera FASP, delay-based receiver-fed control). Incast/CC: collapse =
RTO_min 200ms artifact (Vasudevan; DCTCP hard floor); Swift = production
proof a host-side owned CC works at Google scale (O(10k) incasts,
pacing-below-cwnd=1 ≈ our credit grants); WAN bar = Cubic-class (BBR bulk
win ≈1%). Reconciliation math: 16 KiB group = 12 datagrams ⇒ (1−p)^12
group-loss amplification (11.4% incomplete @1% loss; 12× retransmit
amplification at group-granular recovery); UDP bulk envelope overhead 7.6%
vs 0.46% TCP-framed; QUIC option collides w/ Guardian AAD-cleartext
policing + HKDF key plane; laptop degenerate penalizes every UDP option
(loopback MTU nit: §1.1's 1500 anchor must become per-path); SIM honesty:
kernel TCP outside SIM — class-6 nemesis coverage tests above TCP, noted.
Four architectures priced (TCP-parallel / Homa-shaped intra-DC / full UDP /
sans-IO QUIC); per-work-class matrix grounded (ordered rows: semantics +
census both say TCP; contested = intra-DC bulk + WAN replication; media
playback-streaming = the one RFC9221-shaped unreliable-datagram fit, edge).
Dossier register updates (2026-08-17, user-driven): Tectonic transport = TCP
**user-attested** (public papers silent; no primary URL exists) — census
hardened: every named production blob plane now sits on TCP by primary
source or attestation, hyperscaler escapes being infra-coupled custom
transports. Falcon disambiguation PENDING user confirmation (dossier's
Falcon = Google's 2023 hardware transport, UDP/IP-encapsulated per unfetched
OCP slides; CrowdStrike Falcon sensor = TLS/TCP telemetry agent, different
product — its heartbeat-vs-report split independently corroborates our
class-0-UDP (lost heartbeat is never retransmitted; the next supersedes) vs
class-3-TCP design). Transport verdict (A1–A7-revised per-row hybrid)
awaiting user ruling.
**Per-system transport determinations LANDED (2026-08-17, dossier addendum)**
— 13 systems ruled, all resolving to FOUR shared mechanisms (TCP frames;
UDP control datagrams; owned granted-flight UDP bulk; TCP-k-parallel WAN
bulk — a fifth would be an owned surface with no receipt). DETERMINED:
registry = TCP frames + delta streams, blobs delegate; harness = split by
signal class (directed TCP / telemetry UDP-superseding); agent↔agent
consults = TCP (Homa's 100× is µs-RPC, our floor is the LLM turn);
agent↔system = per-use split incl. **same-node pairs = no wire at all**
(mailbox; anti-mode-creep); secrets = TCP structurally NEVER UDP
(amplification/reflection — RFC 9000 §8.1's 3× machinery vs TCP handshake
by construction; stale-epoch dies at connect); object tier = THE split:
placement/consensus unchanged, **intra-DC chunk movement (landing, repair,
EC reconstruction, scrub, cache-fill) = owned granted-flight UDP bulk**
(incast-shaped by construction: N→1 repair, k-of-n EC; zero unscheduled
bytes; riders = batching + leaf-granular recovery + jumbo-where-offered +
Swift delay term in grant pacing), **WAN async replication = TCP-k kernel
Cubic**; serving plane = node-local by design, peer cache-fill JOINS the
UDP bulk plane (agent blocked on FUSE_READ = the latency-critical bulk
instance; hedge = second grant); KG/vector = queries TCP, generations =
bulk plane, no bespoke paths; forest = mailbox/gossip-datagrams (lost
emission ≡ slightly faster decay)/TCP retrieval/bulk archive; Designer
media = TRANSFER's own §3/§4 seam — addressed uploads = bulk flights,
**unaddressed ingest parts STAY TCP** (offset==watermark is
ordered-by-meaning; moving it = owning ordering for traffic the spec made
sequential); ledger/delta = TCP closed. TWO CONDITIONALS, triggers named:
roaming-client QUIC-shaped carriage (iff mobile attach ships as product);
Aspera-class delay-based WAN UDP (iff measured cross-region goodput on
lossy high-BDP paths becomes binding). Net: class 6 splits by LEG not
wholesale. Awaiting user ruling on the consolidated A1–A7 set.
**Archetype determination LANDED (2026-08-17, dossier final form,
user-steered)** — supersedes the per-system table as the normative shape:
**systems never pick sockets — every message kind declares exactly one
traffic archetype (R1–R8); the archetype, not the subsystem, determines
carriage at the PROTOCOL chokepoint; an unclassified kind fails boot**
(chokepoint-coverage-at-boot discipline applied to transport). R1
supersession signals = UDP never-retransmitted-never-deduped; R2 idempotent
fenced control (votes, fencing, credit grants, missing-set requests) = UDP
full-envelope + replay window; R3 ordered gap-free logs (AppendEntries,
delta streams, narration, turn streams) = TCP frames; R4 directed
request/response = TCP default + the lawful escape (fits-one-datagram ∧
idempotent ∧ latency-critical ∧ **never_secret** — protocol-checked, not
caller vibe); R5 intra-DC content bulk = owned receiver-credit UDP flights
(conditions: batching parity, leaf-granular recovery, jumbo-aware envelope,
loopback first-light gate); **R6 WAN bulk = the SAME owned UDP plane +
Cubic-class CC + DPLPMTUD with TCP as STRUCTURAL FALLBACK** (Aspera
promoted to determination; fallback = robustness requirement per
SMB-over-QUIC's middlebox record — CHANGED from the prior addendum's
TCP-k-primary); R7 user edge over public internet = ADOPTED QUIC-class
stack at the tool/user plane (outside hecate-wire — no doctrine breach);
R8 loss-tolerant playback = RFC 9221-shaped datagrams. Raft = R2 votes +
R3 log + R5 snapshots. Secrets = R4 TCP-only, escape structurally banned.
Consults = R3/R4 strictly (resolution not idempotent from the parked
issuer's view). Net: two transports + one adopted edge stack, eight rules,
every system derived. Consolidated amendment set awaiting user verdict.
**TRANSPORT RE-RATIFICATION (2026-08-17, user-directed in the research
thread; GAPS.md D-10 is the decision record)** — SUPERSEDES the archetype
R1–R8 entry's TCP-frame assignments above: **QUIC-over-UDP replaces TCP
frames as the primary reliable carriage for every ordered/directed/bulk
class** (turn streams, delta streams, consults, claims, directed commands,
secrets issuance, registry ops, all content transfer incl. cross-region);
the existing stateless bare-UDP datagram plane (PROTOCOL §1.1) remains as
the separate lightweight control plane (consensus votes/membership/fencing
probes/liveness/telemetry/gossip — Raft rides it; protocol-sound: Raft is
loss-tolerant by design, AppendEntries idempotent + leader-retried). The
user is protocol-wise an agent like any other — no separate edge stack.
Rationale anchor: the workload is bursty/concurrent/low-bandwidth-exposed
(agent swarms, laptops, multi-region) — the regime where the QUIC receipts
bind and the TCP storage-census receipts (fat clean stable links) do not;
the intra-DC fat-link penalty (WWW'24) is held as gate D-10(c), not
argued away. FIVE BLOCKING SUB-DECISIONS (D-10 a–e): (a) TLS 1.3 vs
per-pod HKDF + AAD-cleartext Guardian routing (composes with D-7); (b)
owned QUIC-class vs adopted sans-IO state machine; (c) batching/ACK
throughput work as acceptance gates; (d) TCP fallback for UDP-hostile
networks; (e) the spec-amendment enumeration (TRANSFER §3/§8, PROTOCOL
§1.2/§3/§4, FAULTS §3, WIRE_FORMAT). **PROTOCOL.md whole-spec acceptance
now sequences BEHIND D-10(a)/(b)** — they reshape §1/§2; audit amendments
A1–A6 remain valid and pending (A4's D-7 reconciliation composes with
D-10a).
Rider (same thread): the user caught and the dossier owned an
incumbency-smuggling error — SMB-over-QUIC's TCP-first posture is
Microsoft's *migration burden* (port-445 installed base), not engineering
judgment, and transferring it to the user↔agent row inverted the rubric
(on lossy/NAT/migrating last-mile paths QUIC is where the receipts bind
hardest; TCP is the option lacking a justifying receipt there). The
fallback question lives ONCE, in D-10(d), settled on UDP-blocking-rate
evidence — never as a default posture anywhere.
**D-11/D-12 settlement proposals PRESENTED (2026-08-17, in the research
thread; verdicts pending there)** — D-11 cross-node attach: green's
immutability does the work (no coherence protocol exists because nothing
mutable crosses nodes) — three mechanics only: chain-head subscription as
a named PROTOCOL §4 delta-stream subject (QUIC ordered), content-by-hash
through the existing SERVING §6 tiers (QUIC bulk; DAX is per-node physics),
pin+re-bind unchanged (location-independent version pinning); write
direction = seal locally, increment ref travels as directed message, merge
serializer stays single-owner colocated; FS16–FS18; laptop = in-process
collapse. D-12 distributed forest: four-flow composition under FOREST §5's
ratified isolation law — ingest already converges at the colocation unit
(no new machinery), the ONE new verb pair = forest_query/forest_digest
(QUIC directed; turn-path protected by PLACEMENT not verb — colocation law,
F23 structural), replication = deliberately none (derived state,
re-derivation is the availability story; Raft touches nothing),
cross-session/region knowledge = archived registry artifacts over the
durable plane, never live remote field queries; F22–F24. HONEST FLAG
carried: a live global forest would reopen FOREST §5's isolation law —
the proposal settles mechanics WITHIN the ratified law. On acceptance the
research thread writes SERVING §6 / FOREST §5 / PROTOCOL §3–§4 /
OBJECT_TIER cross-refs and closes GAPS D-11/D-12.
D-11/D-12 proposals REFINED in-thread (v2, 2026-08-17; verdicts still
pending there): D-11 — green has no retention floor so RESYNC_REQUIRED is
structurally unreachable for chain subscription (replay-forward always
possible); torn versions unobservable (chain append atomic); "node-local
by design" survives for work-volume WALs — the shared-volume claim was
never about them; spec home = SERVING §6b rider + SESSIONS §2 cross-ref;
law sentence: attach = subscription + cache-fill + pinning, no coherence
machinery may exist because none is needed. D-12 — F10's input clock
(identical state under arbitrary arrival permutation) absorbs cross-node
jitter + shed telemetry with zero new design; F13 kept STRUCTURALLY via
digest-PUSH (per-pod QUIC stream → local cache; assembly reads cache only,
zero network at assembly time); explicit retrieval = agent tool invocation
outside F13 by definition (one clarifying sentence makes it law not lore);
forest needs no Raft/replication/cross-region protocol — total order from
ledger, durability from the planes it rides. Only genuinely new wire
object across both settlements = the green-chain subscription record.
**D-10(a) key-model dossier LANDED (2026-08-17)** — RFC 9000 §7 makes the
handshake VERSION-PLUGGABLE by normative text ("a different QUIC version
could indicate that a different cryptographic handshake protocol");
TLS↔QUIC seam is narrow (secret+AEAD+KDF in → packet protection out —
exactly our HKDF mint's shape); private version + private initial salt
sanctioned (RFC 9001 §5.2; quinn-noise reserved 0xf0f0f2f0). On-wire
visibility under QUIC shrinks to RFC 8999 invariants (DCID/SCID/version) —
cleartext-AAD policing does not survive. Four key models: (1) external-PSK
TLS (RFC 8446/9257/9258 — most faithful to summon-mint, BUT rustls has NO
external-PSK support, issue #174 open since 2018 → C-backed TLS or fork;
zero shipped external-PSK QUIC found); (2) RPK TLS RFC 7250 (works TODAY
on rustls ≥0.23.16 + stock quinn; iroh v1.0 production precedent; mint
type becomes keypairs); (3) Noise-class owned handshake (nQUIC blueprint:
Noise IK in CRYPTO frames, no semantic transport changes, inherits
Tamarin/ProVerif/CryptoVerif analyses, ~1K-LoC implementations vs
OpenSSL's 703K/165 CVEs; three quinn crypto::Session existence proofs —
owned handshake does NOT force owned QUIC); (4) bespoke QUIC-Crypto-style
(dominated by 3; gQUIC's own retirement is the precedent). Guardian axis:
key-sharing/passive-decrypt = precedent-free + NSA-TLSI-cautioned
(rejected); MASQUE = anti-goal; host-terminates ≈ warden-at-endpoint
CONVERGE in our topology — pods egress only via host virtio, the host IS
an endpoint, sees frames pre-encryption; cleartext AAD was compensating
for a passive-middlebox assumption the architecture never had. D-10(b)
facts: quinn-proto = sans-IO, "fully deterministic," Instant-injected
(SIM-fit), crypto-pluggable, no C; quiche = BoringSSL-bound not pluggable;
s2n-quic = tokio-native docs; neqo = NSS + server experimental. iroh
trajectory = the own-it precedent (adopt quinn → fork → standalone noq
only when TRANSPORT semantics diverged, never for crypto). Settlement
exchange presented.
**Forest-diet survey LANDED (2026-08-17, research thread; D-12 exchange
evolved there, verdicts pending)** — Sylk's critical lesson: the rich
forest diet (full claims-delta lifecycle, fabric observations,
consume/resolve reinforcement) was DESIGNED AND IMPLEMENTED BUT NEVER
WIRED in production (no ClaimsDeltaSubscriber set; MountFabricContextObserver
zero callers; harvester = logging no-op, receipts at cmd/tui.go:938,
core/forest/service.go:268, fabric_install.go:41) — shipped forest ate
only content indexing + explicit outcomes. Hecate fix = doctrinal:
**forest input streams enumerated in FOREST.md; boot FAILS if a mandatory
stream has no live subscription** (chokepoint-coverage-at-boot applied to
intake; dark stream = startup failure). Unified event inventory: Tier 1
field deposits (order-independent fold, eager push) = claim/testament/
artifact/validation lifecycles (validation idempotency-by-source-key
discipline ported), consult resolutions, tool/LLM outcomes, precedent-
flagged narration, consumption reinforcement, the three-way retrieval-label
taxonomy (explicit/counterfactual/implicit-negative + ε-greedy — "the
best-designed part of Sylk's forest", the GLM training signal), user
interactions, warden telemetry; Hecate-only: MERGE verdicts (conflict
windows = structural contradiction deposits, AcceptIdentical = independent
convergence), Arbiter findings, rank snapshots, lineage events (landed =
strongest utility label), Guardian refusals, scheduler/autoscaling climate
carriers. Tier 2 exactly-once actions = claims machinery only (promotion→
curation, outbreak→review, remediation via Architect, advisory publication,
cluster naming, operator commands) — field suggests, claims decide. Tier 3
exclusions carried w/ Sylk receipts (atomic telemetry; dual-source facts —
ledger wins; SIR/SEIR; unflagged narration). NOTE: the thread's D-12
mechanism EVOLVED beyond the v2 single-instance proposal → per-pod
replicas + keyed OpSet fold + eager-push/anti-entropy + claims-for-unique-
actions (CALM framing); supersession pending user verdict in-thread
alongside the diet section and the still-open D-11 green-attach proposal.
**D-10(a) DIRECTION CHOSEN (2026-08-17; NOT settled — user paused the over-claim: "did that *actually* ratify anything?"; implementation mechanics owed and presented for correction)** — user direction: "warden → quic endpoint
<-> quic endpoint <- warden. If we need to for virtio to accomplish this,
then we do it." Full settled form in GAPS.md D-10(a): Noise-IKpsk2 owned
handshake (verified suite, not BLAKE3 in-handshake), private QUIC
version+salt, one summon-mint root w/ labeled per-plane derivations +
atomic epoch rotation, IK replay rule + Retry as law, closed 0-RTT list,
derived rekey thresholds w/ key-phase-vs-re-handshake split; TOPOLOGY LAW:
pod frames cross virtio/vsock in the clear → warden rules pre-effect at
the boundary with zero key material → host QUIC endpoint seals; QUIC
endpoints at hosts + user terminals only; a pod's peer is always its host;
virtio-layer work authorized (libkrun fork owned). D-7 resolves into this.
The maximal-audit corners that produced the final form: termination
topology (per-pod QUIC rejected as redundant-with-physics), key-hierarchy
unification, 0-RTT replay policy, AEAD limits split, Noise-suite proof
fidelity, IK-vs-XK argued. NEXT EXCHANGE: D-10(b) adopt-vs-own the
transport state machine (research banked in the (a) dossier).
**D-10(a) mechanics-verification dossier LANDED (2026-08-18)** — every
mechanism CONFIRMED on primary sources: egress ring ≈ vhost-net TX path
(VMM reads guest RAM by construction — OASIS virtio 1.2 descriptor
guest-physical addresses; vhost VHOST_SET_MEM_TABLE; libkrun
GuestMemoryMmap + MMIO BusDevice trait, 8 in-tree devices incl. virtio-fs
as complexity precedent; virtio-wl = shipped-unstandardized-device
precedent); double-fetch class + copy-once mitigation (Bochspwn; Wang
USENIX'17 90 double-fetches; CVE-2015-8550/XSA-155 — COMPILER-introduced
second fetch, arbitrary code exec, RING_COPY_REQUEST as canonical fix;
CVE-2016-9381, CVE-2024-3446); HKDF per-context derivation standard (RFC
5869, SP 800-108 KDK, TLS 1.3 schedule, SigV4); KDC failure-mode analysis
favors us (golden-ticket = KDC gaining authority it didn't have; our
broker host already maps the pod's RAM — zero marginal authority; clock
skew deleted by counter epochs); sealed-payload passthrough = SRTP (RFC
3711 payload-e2e/header-auth) + IPsec AH (RFC 4302 auth-only) + MASQUE
forwarded mode (explicit double-encryption avoidance; its security
considerations = our bulk-lane guard checklist); GMAC = NIST SP 800-38D
standardized auth-only GCM, 0.64→0.16 cpb (Gueron), nonce reuse =
Joux forbidden attack = unlimited forgery (THE crypto landmine); guest-side
validation = TDX Linux guest hardening ("all virtio input untrusted",
split-virtqueues-no-indirect audited config) + VIA ACSAC'21 50 bugs in 22
drivers; perf: AES-GCM 4-10+ GB/s/core, HKDF ~µs amortized, EVENT_IDX
kick suppression in-spec, memcpy bound derived-THIN. THIN: C3 broker
deployed-precedent (2025 arXiv + patents only — spec carries the
first-principles argument). SEVEN spec obligations: compiler-proof
copy-once (read_volatile/copy_nonoverlapping, never &T into guest memory,
length-fetch-once), GMAC nonces = monotone packet-number-bound +
crash-safe-new-key-on-restart + NIST rotation, counter epochs not
wall-clock, broker argument in-spec, bulk-exemption guard
(name-verify-before-use + envelope truncation/reorder detection),
split-queues-no-indirect + purpose-built guest parser, seal-off-event-loop
+ EVENT_IDX batching. WIRE_SECURITY.md presented in-message.

**WIRE_SECURITY.md ACCEPTED + WRITTEN (2026-08-18)** — D-10(a) fully
closed: the presented mechanics spec accepted verbatim ("Accepted.") and
written to docs/specs/WIRE_SECURITY.md with all seven dossier obligations
as law (compiler-proof copy-once + lint, GMAC nonce law, counter epochs,
in-spec broker argument, bulk-exemption guard, split-queues + purpose-built
guest parser, seal-off-event-loop). NEXT: D-10(b) adopt-vs-own transport
state machine (research banked); then (c)/(d)/(e); then PROTOCOL.md
whole-spec re-presentation with A1–A6 + the D-10 amendments folded.
**D-10(b) SETTLED (2026-08-18, "accepted.")** — owned `hecate-quic`: pure
core, RFC 9000/9002 dialect-as-exemplar, executable conformance (9002
pseudocode as reference tests, field bug-record as named regressions,
interop scenarios adapted, loss-recovery fuzz THROUGH the transport in
cluster-SIM — a first for any QUIC impl); scope = archetype subset, no
TLS/h3/interop; quinn-proto/quiche = reading references never deps.
Rejected: adopt (fails no-panic law, lint wall — Bytes=Arc in hot path,
IO-as-data shape, conformance obligation), fork (dominated middle, iroh→
noq receipt). Risk to ledger: loss-recovery subtlety, mitigated
consensus-core-style. D-10(c) folds in as hecate-quic ratchet gates.
**D-10(c)/(d)/(e) SETTLED (2026-08-18)** — (c) folded into hecate-quic
ratchet gates; (d) user verbatim: "no fallback. Period. QUIC + UDP over
TCP utilizing the standard(s) we just designed" — TCP deleted from the
mesh entirely, no tunnel, no tripwire (architect's telemetry+contingency
recommendation overruled, recorded); provider-egress h2/1.1 unaffected
(external plane); (e) accepted — PROTOCOL.md re-presentation is the
execution vehicle. **D-10 IS FULLY SETTLED.** PROTOCOL.md amended spec
presented in-message next.
**PROTOCOL.md ACCEPTED + REWRITTEN (2026-08-18, "accepted.")** — Branch 3
SETTLED. The D-10(e) execution: full rewrite — two planes over UDP, NO TCP
in the mesh (P14 structural); §1.1 HEADER-ENCRYPTED control datagrams (the
user's in-exchange revision: the AAD-cleartext posture was a fossil of
deleted on-path policing — cleartext shrinks to the key-finding prologue
{ver, key_hint, len}; full envelope encrypted+authenticated; enforcement
order gains key-lookup-before-crypto drop; "cleartext is only what is
needed to find the key" = cross-plane law, criterion 14); hecate-quic
session plane w/ four frame classes; archetype-determines-carriage +
metadata-completeness as §3 law; credit clauses implemented natively in
the owned transport (one flow-control law); A1–A6 folded (minting
authorities, HLC liveness-only, no-panic P7, cluster-SIM); P1–P19,
criteria 1–14. SAME-COMMIT RIDERS: LEDGER §7.3 rewritten (D-7 CLOSED),
ADR-0002 corrected, SIBYL grants→Branch 25 (D-8 CLOSED), TRANSFER §3/§4
carriage wording, FAULTS §3 owned-recovery note. Owed-verdict queue now:
MERGE, VFS, PODS, AGENTS_RUNTIME, RANK, SCHEDULER (+C-6 label fix),
OBJECT_TIER whole-spec, FOREST (D-4), VECTOR_INDEX (D-9).
**MERGE.md acceptance exchange IN PROGRESS (2026-08-18)** — user rejected
the four-amendment summary as hand-waving; each amendment now worked at
D-10 rigor, one at a time. **A1 SETTLED ("accepted.") in CORRECTED form**:
the first draft's region-group grant was a REAL FLAW (second authority
that can disagree with session-group leadership = wedge state that exists
only because the mechanism was added; mis-applied epoch-scoping — the
smallest domain containing every legal serializer holder is the SESSION
group). Maximal form = **self-fencing through the log**: a new serializer
instance's first act = committing SerializerOpen{generation} through the
session group — the commit IS the leadership proof AND the fence
(supersedes all prior generations as quorum-committed state; no side
channel can disagree because it is the authoritative state); batches carry
(term, generation), refused at the state machine on mismatch (two-integer
compare, zero crypto); liveness = existing leader fortification +
supervisor restart (Chubby-lease draft machinery DELETED — grant protocol,
keepalives, fenced registry all gone); refs-not-content law (CAS writes
unfenced-safe, only the log/refs carry authority); failure matrix all rows
terminate in ONE authority; ZooKeeper-epoch-open pedigree; CONSENSUS §6
roster records this as the writer's mechanism (meta-tree-lease shape
remains for writers lacking a colocated group). Tests M13a–f incl. the
single-authority property + open-marker lineage replay-derivability.
NEXT: A2 (increment content carriage) at same depth.
**Merge-path throughput receipts LANDED (2026-08-18)** — BLAKE3 0.49
cpb/core ≈ 6.1 GB/s @3GHz (paper Fig.3, c5.metal AVX-512; threads level
off >16 on memory bandwidth); memcmp/memcpy ~15 GB/s/core DRAM (Lemire
Ice Lake), 50–200 GB/s cache-resident (Agner port throughput — THIN
assembled, no single canonical bench); FastCDC ~2.1 GB/s/core (ATC'16
Table 6 cycles, i7-4770 — 10.3× Rabin); borsh/postcard decode 0.2–1.6
GB/s class (rust_serialization_benchmark EPYC 9V74 — mesh 1.61/1.15 GB/s,
log ~0.5/0.4); fixed-stride cast-and-validate precedent CONFIRMED
(Cap'n Proto no-decode, FlatBuffers 0s-vs-220s decode bench, Arrow O(1)
fixed-width + 64B/AVX-512 alignment, LMDB mapped pages — THIN on LMDB
refetch). Key demonstration: a 10k-op doc DECODED at borsh-class rates =
0.4–1.3 ms (breaks the sub-ms bar); CAST at memcmp rates = ~20 µs — the
fixed layer is load-bearing, now receipted. Deleted seal-hash pass worth
~0.33 ms per 2MB increment (BLAKE3 receipt). A2 final presentation next.
**GOVERNING FRAME RECORDED (2026-08-18, user)**: "kubernetes-like
abstractions *with the underlying advantages of the scheduler,
Eden/Tectonic FS's, distributed knowledge graph and forest machinery,
etc." — crystallized as the law: **Kubernetes sets the abstraction bar;
our substrates are the mechanism — never the reverse.** Deliver K8s-proved
ergonomics (declare-don't-place, mount-anywhere, identity-not-location,
reconcile-to-desired) implemented by strictly-stronger native machinery,
zero K8s componentry imported. Correspondence table drawn (volume→
immutable manifests over two planes w/ coherence/locking/snapshot/dedup
wins; scheduler→deterministic optimism + content locality; controllers→
summon-as-claim + ratio autoscalers; service→participant UIDs; etcd→meta
tree; kubelet/CNI/CSI→host runtime+warden+native protocol+store, no
plugin seams; namespaces→sessions w/ VM isolation; CRDs→registry kinds;
plus KG/forest as first-class platform services K8s has no analogue for).
Volume verdict reframed: the dossier's mechanism must CLEAR THE PV BAR
(mount-anywhere ergonomics) while exploiting substrate advantages; the
mutable work volume flagged as the one candidate needing its own
treatment outside the immutable story. Frame governs: MERGE §0 picture,
single-surface law (to become spec text — currently folklore across five
specs), Branch 17 (presentation plane), Branch 33/34, walking skeleton.
Volume/SMR receipts dossier still in flight.
**Volume-model + SMR receipts dossier LANDED (2026-08-18)** — A:
read-through local cache WINS decisively for immutable content-addressed
volumes: K8s PV access modes are per-node ATTACH constraints for the
mutable case (CSI = detach/reattach choreography), while K8s's own
immutable case (container images) is pull-by-digest to local store,
IfNotPresent, cache-forever — our side; EdenFS CONFIRMED on primary text
as lazy local projection ("lazily fetching file data… only for portions
actually used") with the exact layering kernel-VFS-cache → in-memory LRU
→ local RocksDB store → network; AFS/NFS/Ceph coherence machinery exists
ONLY because files mutate (caps/callbacks/close-to-open); GFS no-cache =
streaming-workload rationale, opposite of a coding pod (cite-and-dismiss);
Nix/OSTree = substitute-from-any-peer-verify-by-hash; caveat: cold-miss
latency real (EdenFS admits it) → manifest-driven prefetch of hot sets.
B: warm follower apply = DEFINITIONAL Raft (§5.3 verbatim); failover =
promotion ≈ election timeout (etcd 100ms/1000ms defaults; graceful
transfer sub-timeout via TimeoutNow); epoch-in-the-log fencing = FOUR
production precedents (Raft term, BookKeeper fence op, Kafka KIP-101
leader epoch, Zab epoch) — SerializerOpen now receipted; verify-on-apply
CORRECTED: shipped shape = deterministic apply (replicas recompute
transitions — definitional SMR) + PERIODIC cross-replica hash comparison
w/ fatal-loud divergence (etcd CORRUPT ALARM; CRDB SHA-512 checker kills
divergent node) — per-entry semantic validation exceeds precedent.
Hecate elegance: cross-replica check = compare green-head manifest hashes
per log index — O(1) continuous, free (state IS a hash) vs CRDB's
expensive snapshot SHA-512. Consolidated re-presentation next.
**MERGE ARC WRITTEN TO THE CORPUS (2026-08-18, user directive: "you NEED
to make sure this is written in hecate's documentation… NUMEROUS documents
get the merge systems, the session-wide VFS volume, the per-pod mechanics
WRONG… sessions being one-node-only BLATANTLY wrong")** — MERGE.md fully
rewritten and ACCEPTED (submission-transaction verdict "That matches"):
§0 human picture w/ diagrams (per-machine anatomy, RSM+baton, one-edit
walk), A1 self-fencing w/ four precedents, two-pass verdict, A2 descriptor
increments + fixed-layer ops docs + composed-net-ops law, §5 apply/place/
replicate (OT14-for-green: version blobs placed to session-group members
+acked BEFORE the record commits; warm appliers; free continuous
green-head hash comparison, divergence fatal-loud), §6 green-as-volume
(attachment model), §7 the submission transaction (sequence + failure
table; Arbiter explicitly NOT in the submit path), M13–M17 test families,
13 criteria. SERVING.md: §0 single-surface law added (no API names a
machine; sessions span nodes; EdenFS four-tier read order adopted;
work-volume=RWO carve-out) + §4 placed-before-referenced for green.
VFS.md: §3b volume lifecycle (claims → attachments → access-mode table;
RWX does not exist). CONTEXT.md: Session glossary corrected ("A session
spans machines"), Colocation unit + Attachment entries added.
SUMMONING.md: truth-plane clause corrected (one node "for locality, not
for existence"; failover is promotion). MERGE exchange CLOSED; A3/A4
folded (laptop degenerate = §11; carriage = §7's lanes).
**A1–A4 re-audit dossier LANDED (2026-08-18)** — WS1: TiKV/KRaft/
Multi-Paxos FUSE application writer with consensus leader; CRDB is the
regret case (separately-fenced in-group writer → "leader-leaseholder
splits," indefinite-outage variant → Leader Leases/fortification spent a
protocol change UNIFYING them, 85% lease-CPU reduction); separate epochs
shipped ONLY for writers outside the consensus group (Kafka producers,
BookKeeper clients); NO shipped system fences a replica-resident writer
with an epoch separate from its own group's term. WS2: etcd server-side
forwarding vs CRDB/TiKV client resolver-cache both shipped; retry
pathologies documented (NotLeaseholder storms #23543, redirect ping-pong
#22837); strongest variant = TiKV piggyback (NACK carries current leader).
WS3: input-logging + determinism = canonical line (Schneider, Calvin,
TigerBeetle — divergence DETECTION comes from it); output-logging (Zab
deltas, Aurora redo, Kafka) = apply-without-recompute but replicates a
wrong verdict verbatim; hybrid both-in-record has NO precedent (THIN);
literature posture for µs-cheap pure deciders: inputs authoritative,
recompute at apply, logged outputs = cross-check whose mismatch is fatal.
WS4: reservation-bearing scheduling classes for commit-critical
replication = shipped (Ceph mClock client/subop vs recovery classes;
Scylla service levels); rate-caps-on-bulk = the documented failure (Kafka
KIP-73 throttled ISR catch-up → KIP-542; HDFS balancer caps); classify by
PURPOSE (needed-for-quorum vs opportunistic). etcd N=1 = same code path,
quorum=1, self-ack; the fragile transition is GROWING 1→2 (feeds Branch
38's laptop-to-fleet growth path). Re-audits presented one at a time, A1
first.
**A1 RE-AUDIT SETTLED ("Accepted.", 2026-08-18)** — the settled baton
design OVERTURNED by the fusion receipts: MERGE §2 rewritten — **the
proposer is a role of the session-group Raft leader; the term is the only
fence; SerializerOpen and the generation are DELETED** (succession = the
Ongaro term-opening no-op; promotion = election/transfer; intra-process
races killed by runtime ownership, not distributed fencing;
leadership-follows-the-unit now load-bearing spec text). Rejected-
alternative record = CRDB pre-fortification leaseholder (the split class),
in-spec. M13a–f re-targeted to term semantics + the transfer-back bound;
criterion 7 = grep-proof no second fence. One concept, one message, one
promotion step, one failure class deleted. NEXT: A2 re-audit
(submission topology + record content).
**A2 RE-AUDIT SETTLED ("accepted.", 2026-08-18)** — two corrections
applied to MERGE.md: (1) §5 — **inputs authoritative, appliers recompute
the full two-pass verdict from placed content** (deterministic apply, the
input-logging canon); recorded verdict/manifest-hash = cross-checks only,
mismatch fatal at the index — the output-poison hole (proposer lies
replicated verbatim) made unrepresentable BY the placed-before-referenced
rule (appliers hold the bytes); the trust-the-fence/attested-results
variants deleted. (2) §7 — submission = resolver-cached direct-to-leader
w/ piggyback NACK (TiKV shape), single-flight resolver refresh + directory
fallback as named storm guards (CRDB #23543/#22837 as receipts);
etcd-forwarding = rejected alternative. M15e (lying proposer) + M17b
(resolver storm) added. Unchanged: descriptors, fixed layer, composed net
ops, dedup identity, GC roots. NEXT: A3 (one-line confirmation) + A4
(placement QoS class) exchange.
**A3 + A4 SETTLED ("Agreed and accepted.", 2026-08-18) — A-SERIES RE-AUDIT
COMPLETE.** A3: MERGE §11 stands, receipted (etcd N=1 = same code path,
quorum=1); the fragile 1→2 growth transition named and routed to Branch
38. A4: **quorum-critical transfer** = sixth archetype in PROTOCOL §3;
membership BY PURPOSE never volume (green placement pushes + consensus
catch-up for quorum-needed members; KIP-73 = the named negative);
mClock-shape reservation/weight/limit natively in hecate-quic (D-10(b)
obligation); derived reservation formula; starvation-pair + catch-up
membership tests. **ELEVATED TO SYSTEM LAW (user verbatim): "different
types of traffic for different work should NOT block one another with the
scheduler, and our scheduler needs to be smart enough to know the
difference"** — the traffic non-interference law, written into PROTOCOL
§3; disk-IO/CPU instantiations owed to OBJECT_TIER/RUNTIME as a named
rider. All four A-items now maximal under the final architecture:
A1 fused (term-only), A2 inputs-authoritative + piggyback topology,
A3 receipted, A4 classed. Queue resumes: VFS whole-spec audit next.
**Structural non-interference guarantee ADDED (2026-08-18, user directive
verbatim: "a 2GB upload CANNOT possibly block other work, control frames,
etc.")** — the non-interference law strengthened from policy (reservations)
to CONSTRUCTION: invariant = no class's latency bound contains any term
dependent on another class's object size or queue depth; enforced per
shared resource by partition (per-class queues/credit pools/virtqueue
pairs/arena budgets — interference unrepresentable) or quantum bound
(frame cap: worst-case cross-class occupancy = one packet, invariant in
object size); bulk payloads already do ZERO host crypto (Lane-A
passthrough) + envelope-only inspection; store disk-IO instantiation =
the owed OBJECT_TIER/RUNTIME rider with this invariant as its acceptance
bar (per-class IO queues, Scylla shape); permanent test = the 2GB walk:
p99 latency curves of every other class FLAT across an upload-size sweep
— object size appearing in any curve is a structural failure, not
degradation. Written into PROTOCOL §3.
**Scale walk strengthened (2026-08-18, user: "We need to survive
multi-petabyte walks")** — the independence test renamed and re-scoped:
sweep spans MB→TB in real CI tiers + PB-class in the deterministic
cluster-SIM (simulated bytes free; a PB walk costs seeds not days — the
SIM's reason to exist); flat curves required in latency AND memory. Three
PB-only failure modes named into the walk: rekey-in-flight (AEAD
invocation limits crossed mid-transfer ⇒ hop-key rotation without pause
or cross-class perturbation), duration-invariance (multi-day transfers
survive leadership/epoch/node churn by missing-set resume — the TRANSFER
scoping theorem asserted at PB duration under nemeses), fleet-aggregate
effects (per-node reservations don't compose alone: incast bounded by
receiver-driven credits at fan-in; a transfer's own generated maintenance
— staging leases, GC, scrub — is opportunistic by the purpose rule, so a
transfer cannot promote its own cleanup into anyone's critical path).
**VFS audit receipts LANDED (2026-08-18)** — all three CONFIRMED:
(1) per-class memory budgets w/ typed refusal = shipped practice at three
levels (Seastar static per-shard partitioning + bad_alloc; Scylla
reader-permits — "1 count + 128K memory resource on admission," kill-limit
throws typed; cgroups v2 memory.min hard protection); nuance recorded:
Scylla's intra-shard subsystem budgets are ELASTIC controller targets, the
hard walls are shard boundary + permits — both points in the space named.
(2) infinite attr/entry caching for immutable layers = the
libfuse-RECOMMENDED shape verbatim ("if attributes only change as a
result of requests that come through the kernel, this should be set to a
very large value") + EdenFS ships it ("Eden returns an infinite expiry"
+ explicit invalidation only) + virtiofsd cache=always — our
per-attachment pinned-validity model IS the documented practice.
(3) terminal→fleet ingestion = git haves/wants (the exact
upload-only-what-the-server-lacks negotiation, primary text) + Sapling
Commit Cloud (auto-upload on creation, hash-addressed) + CitC (server-side
workspace materialization over the content store; noted: CitC's backend IS
the cloud — a different point, recorded). VFS amended audit presented.
**Heterogeneous placement item ADDED to the SCHEDULER whole-spec exchange
(2026-08-18, user)** — a mechanism to steer specific work to specific node
types/regions over heterogeneous compute/storage; the K8s taints analogy
offered explicitly AS A PROMPT NOT A DESIGN ("Don't take this
recommendation as is — research the maximally correct, robust, performant,
efficient means"). Research dispatched: K8s taints/tolerations/affinity/
topology-spread semantics + documented pain; Borg constraints (hard/soft);
Twine entitlements + host profiles (machines RESHAPED per workload);
Firmament min-cost-flow; Paragon/Quasar classification-based heterogeneity
scheduling; device/GPU scheduling practice; interaction with our existing
machinery (summon claims as the requirements carrier, content-locality
scoring, Guardian admission, region colocation law). Exchange follows the
dossier; VFS item-5's memory-wall half is unaffected (node-local classes).
**Heterogeneous-placement dossier LANDED (2026-08-18)** — the four
mechanisms answer four DIFFERENT questions: attribute matching = "which
machines CAN run declared work" (irreducible base; universal; costs =
declaration quality — Quasar's Twitter receipt: <20% utilization vs 80%
reservations, 70% of workloads over-declare up to 10× — sprawl, and the
opaque-integer ceiling that forced K8s's DRA; Slurm's typed GRES
gpu:a100:2 = the cheap fix, type INSIDE the accounted resource);
repulsion (taints) = the one question matching can't answer: "how does a
NODE protect itself from work that declared NOTHING" (authored node-side,
defaults closed; K8s docs: dedicated capacity needs taint+affinity+
admission-webhook TOGETHER — the ergonomics tax; Nomad independently
rediscovered the gap and built node pools); profile pools (Twine) =
"how FEW machine shapes can the fleet have" — entitlements as abstract
quota dynamically bound to machines + HOST PROFILES reshaping machines on
pool rebind (kernel/sysctl/storage/NIC; 11% web-tier throughput from
tuning — NOT '11% picky jobs', that Borg citation doesn't exist, the
constraint-cost source is Sharma SoCC'11; segregation costs 20-30% more
machines per Borg §5.2; twshared 15%→56% of fleet); performance-model
placement (Paragon/Quasar) = "which feasible machine is BEST, measured
not declared" — the biggest numbers in the space (91% vs 3-7% QoS; 62%
vs 15% utilization) but native form = online SGD classifiers, fights
determinism; the extraction = EPOCH-FROZEN data-derived coefficients fed
to the deterministic scorer. Locality = a scoring family we have (graded
ladder w/ fixed score-discounts replacing wall-clock delay-scheduling
waits — its preconditions don't hold for us; Dragonfly/Kraken = the
move-bytes-not-work boundary, locality weight derived from measured
transfer cost). Convergent stack across all surveyed end-states:
pools → hard feasibility (requirements + repulsion, pure predicates) →
deterministic scoring → quota-at-admission → gang. Determinism red flags:
online classifiers + NoExecute eviction (⇒ drain-not-kill only).
Predicate-cost mitigation — CORRECTED on reconciliation (2026-08-18):
SCHEDULER.md §5 already ratifies the STRICTER law ("Score every candidate
in the shard — no sampling… injects banned nondeterminism; its benefit
inverts when feasibility is scarce, kubernetes#108606"; AC-2 = no sampling
code exists, architecture test) — and heterogeneity STRENGTHENS it
(feasible sets shrink ⇒ sampling's benefit inverts further). The Borg/K8s
sampling receipts = why THEY sampled at their scale, never a mechanism
available here; Hecate-legal mitigation = equivalence classes +
content-keyed memoization only (§5's bundle-hash/constraint-set/
state-version keying). Also: the "11% picky jobs" correction had no
target — no Hecate doc ever cited it; all existing Borg citations
verified sound. Exchange presented, now with the sampling clause struck
and one added amendment: SCHEDULER §6's "exact on homogeneous nodes" fit
claim becomes exact-PER-CLASS once node classes exist.
**Heterogeneous-placement verdicts (2026-08-18, user)** — Item 1 node
classes: RESHAPING ACCEPTED ("that cost is fine") — registry-declared
classes as identical-machine equivalence keys (unclassified node fails
boot — chokepoint-coverage law), dynamic class membership + class→purpose
binding as versioned meta-group state (Twine entitlement shape), and a
host-profile actuator applying per-class kernel/sysctl/storage/VMM
settings on rebind (Twine Sidekick; fenced, Branch-32-integrated —
profile-apply is a mini node-join; convergence states live in the
inventory map). Item 2 repulsion: per-class-only REJECTED as incomplete —
per-node repulsion is "an extremely valuable escape hatch"; investigation
directed for the maximally correct marriage of both axes; marriage design
presented in-message — class axis = registry-declared repel (design
intent, workload-shaped), node axis = fenced inventory-map dispositions
ONLY (operator cordon/drain = auto-disposed but epoch-bumped map
proposals, never free-floating taints; K8s receipt verified: production
per-node taints are control-plane-authored from conditions — "the
Kubernetes control plane automatically creates taints that match the
conditions affecting the node" — with cordon as the operator hatch:
"prevents the scheduler from placing new pods onto that Node but does
not affect existing Pods"; structural note: item 1's accepted reshaping
REQUIRES the node axis — a mid-rebind machine must repel work via map
state). Marriage ACCEPTED 2026-08-18 ("accepted"): class axis
registry-authored; node axis = map-disposition-only, auto-disposed
operator cordon as the immediate escape hatch (fenced, epoch-bumped,
reason-carrying — never a free-floating taint); closed state vocabulary
{cordoned, draining, rebinding, commissioning} with per-plane
repair-suppression scopes (noout class) owed to Branch 32; no NoExecute
anywhere — state changes emit rebalancer consent moves; interaction rows
named for the amendment (cordon vs in-flight gang, draining session-core,
commissioning = coefficient-campaign claims, laptop loud-refusal). Item 3 typed resources: ACCEPTED; vocabulary
derivation pass added to the tree as D-13 (GAPS §2), sequenced
immediately before the SCHEDULER amendment presentation. Item 4
performance coefficients: ACCEPTED — slot-now-identity-matrix, activation
gated on the first commissioning baseline (fit-before-influence, the
FOREST AC-4 pattern).
**Heterogeneous-placement amendment ACCEPTED 2026-08-18 ("accepted.")** —
D-13 pass executed first as sequenced (v1 vocabulary {cores, mem,
storage_cap(nvme), storage_write_bw(nvme)}; write-bw dual-reader call —
admission accounts, OT13 servo enforces; repair/scrub IOPS not minted;
accelerator slot reserved unminted; D-13 CLOSED in GAPS). SCHEDULER.md
amended in-file: §1 node classes (registry equivalence key, meta-group
membership, Branch-32 host-profile actuator), §2 intake gains map-state
transitions + coefficient epochs, §5a typed vector + two-axis repulsion
(three pure predicates; label change from presentation: coefficients
section landed as §5b, not §5c — no gap minted), §5b epoch-frozen
coefficients (identity until commissioning epoch 1), §6 typed-budget
coherence clause, SCH16–21, AC-9/10, header status line. GAPS inventory
row updated (SCH1–21, AC 10). The heterogeneous-placement item of the
SCHEDULER whole-spec exchange is SETTLED.
**Branch 28 OPENED — research dossiers LANDED (2026-08-18)**, three
workstreams, primary sources verified. Detection: entropy-only = high
recall/catastrophic precision (truffleHog v2's 4.5/3.0 thresholds carried
ALL its detections yet missed ~70–75% of secrets — Meli NDSS'19);
distinct-signature regexes + lookaround anchoring + statistical filters
(entropy-deviation >3σ, word/sequence filters) = 99.29% candidate
validity, 89.10% of found secrets sensitive (Meli); shipped-tool trade
stark — Gitleaks 88% recall/46% precision vs GitHub 75% precision (ESEM
2023 Basak); GitHub scale receipts: 39M secrets leaked 2024, ~90% of
GitHub's own internal alerts closed non-valid (the FP-poison anchor);
live verification (trufflehog ~800 provider probes) is the only
FP-killer but = outbound API call CARRYING the credential —
never inline; Vault audit = the fail-closed chokepoint pattern
(HMAC-SHA256 instead of value + "Vault refuses to service the
corresponding API request" if no audit device can log). Storage: Vault
barrier/seal/Shamir/auto-unseal, dynamic-secrets leases + prefix TREE
revocation ("vault lease revoke -prefix aws/"), rotate-vs-rekey
distinction, response wrapping (single-use cubbyhole, malfeasance
detection); age (per-file CSPRNG file key, recipient stanzas, no
config); sops (encrypt values not keys, MAC under data key, key groups +
Shamir); per-OS keychains verified (Keychain AES-256-GCM two-key,
DPAPI logon-credential scoping, Secret Service session collections,
kernel keyrings unswappable); secret zero = platform-identity
attestation (Vault AWS/K8s auth "AWS is treated as a Trusted Third
Party"; SPIFFE workload API "does not require that a calling workload
have any knowledge of its own identity"). Injection: universal
convergence on references-in-specs + materialize-at-trusted-boundary
into RAM-backed files (K8s secret volumes ARE tmpfs by doc; Vault
injector shared MEMORY volume, app never Vault-aware; systemd
credentials non-swappable + not propagated down process tree; 1Password
op:// = secrets-as-references product pattern; BuildKit secret mounts
never in layers); env vars = documented anti-pattern (Docker: "available
to all processes… printed in logs"; OWASP: "not recommended"); rotation
= re-render in place at 2/3 lease (Vault agent), K8s env vars need
restart (the rotation gap); NIST 800-63B: event-driven not calendar
("SHALL NOT require… change periodically… SHALL force… if compromised");
access-as-audited-event (Vault audit devices, CloudTrail GetSecretValue).
Design exchange follows.
**Placement exchange NOW WORKED IN THE RESEARCH THREAD (2026-08-18)** —
the thread verified the tree (Branch 28 secrets + Branch 35 hosting
confirmed on-tree; GAPS §3 staleness re Branch 35 fixed this commit),
committed the SCHEDULER §6 exact-per-class scoping (6f50e8b, verified
coherent with the reconciliation line), and presented FIVE RULINGS to the
user there: (1) node classes — recognition vs Twine-style RESHAPING
(host-profile actuator on class rebind; interacts w/ Branch 32 bring-up);
(2) repulsion granularity — per-class (recommended) vs per-node;
(3) authorize the PODS-derived typed-resource vocabulary pass (the
consumed⇒typed-resource / matched⇒attribute discriminator as law);
(4) performance coefficients — slot-now-activate-at-first-baseline
(FOREST AC-4's fit-before-influence pattern; correctness-neutral,
utilization-bearing); (5) **Branch 39 charter proposed — observability
plane + mesh/pod telemetry integration** (the substrate ~10 specs'
ratchet gates presuppose; collection at existing chokepoints only;
telemetry = supersession class; bounded cardinality derived; content-free
law; operator query surface; non-scope = HEALTH judgment/Branch 30
declaration/Branch 14 math; research-first OTel-as-pattern, Monarch,
Gorilla). Orchestrator standing off SCHEDULER while that thread drafts;
VFS amend-and-accept remains open in the main line.
**Placement four-item presentation DELIVERED in the research thread
(2026-08-18; Branch 39 chartered there, 4f05dbb — verified coherent)** —
each mechanism walked against the concrete class-a/b/c fleet: (1) classes
as the identical-machine equivalence key restoring §6 exactness + SCH8
memoization (class joins the plan-shape key); dynamic membership via
meta-group events (Twine entitlement receipt; Borg's 20-30% segregation
tax); OPEN RULING: recognition vs reshaping actuator. (2) Repulsion:
the Monday-morning GPU-starvation walk (matching working-as-specified IS
the failure); per-class repel + derivable tolerations (consuming a
protected typed resource implies admittance) + Guardian as the stamp
point; per-node repel REJECTED as a second authority competing with
Branch 30's inventory map; drain-never-kill. (3) Typed resources: the
budget/placement-drift walk (32 fungible "gpus", 12 free, all wrong
model — admission passes, placement parks forever; the documented DRA
retrofit); the law = (kind, type, quantity) with the "can two pods
exhaust it?" discriminator; OPEN RULING: authorize the PODS/OBJECT_TIER/
SERVING/VECTOR_INDEX/Br-23 vocabulary derivation pass (v1 read: cores/
mem/storage_cap/storage_bw, accelerator slot unminted). (4) Coefficients:
the slow-serializer walk (locality-blind 30% forever); epoch-frozen
matrix as ordinary evaluation-log input; OPEN RULING: confirm
slot-now-identity-matrix + activate-at-first-baseline (FOREST AC-4
pattern). Four rulings + Branch-39 scope pending with the user in that
thread; amendment text to be presented in-message there before any write.
**Two-axis repulsion marriage PRESENTED in the research thread
(2026-08-18; repo coherent through 79fa956 — reshaping/typed-resources/
coefficients verdicts recorded there, D-13 vocabulary pass chartered)** —
the key structural finding: **accepting reshaping made the node axis
mandatory** (a machine mid-profile-apply must repel all work — class-only
can't represent it); the free-floating K8s taint rejected on dual-
authority + lifecycle-less sprawl; the receipt = K8s ITSELF converged to
machine-authored condition-taints + cordon-as-the-human-residue with
exactly our consent-move semantics. The marriage: class axis =
registry-authored repel (design intent); node axis = CLOSED disposition
vocabulary of the fenced inventory map ONLY (cordoned/draining/rebinding/
commissioning; repair-suppression flags owed to Branch 32); operator
cordon = auto-disposed proposal to the map (immediate hatch, but fenced +
epoch-bumped + reasoned — the forgotten-taint failure structurally gone);
feasibility = class_admit ∧ map_admit, two pure predicates over logged
inputs; commissioning benchmarks = the coefficient campaign (items 1/2/4
close into one loop). Ruling pending in-thread; SCHEDULER §5/§6 amendment
to be drafted there after D-13.
**D-13 EXECUTED + SCHEDULER amendment PRESENTED in the research thread
(2026-08-18)** — the derivation pass minted exactly four kinds from real
consumers (cores, mem — PODS §2 + Branch 38's measured microVM overhead;
storage_cap(nvme) — Branch 37/OBJECT_TIER §7; storage_write_bw(nvme) —
OT13's endurance budget, admission-accounts/servo-enforces, one
derivation two readers); repair/scrub IOPS NOT minted (fleet-plane
pacing, no admission consumer); CPU-gen/ISA/region confirmed
matched-only; accelerator slot reserved-unminted (zero consumers in the
tree — minting follows a consumer). The full §1/§2/§5a/§5c/§6 amendment
text + SCH16–21 + criteria 9–10 presented in-message there; awaiting the
user's word to write. Orchestrator remains off SCHEDULER.md.
**Branch 28 five-decision design exchange PRESENTED in the research
thread (2026-08-18; dossiers landed as ccfff5b, verified coherent)** —
the standout structural moves: (a) the TWO-CLASS detector split — a
per-session KNOWN-VALUE INDEX (keyed HMACs of every value the vault
itself materialized: exact, zero-FP/FN for front-door secrets — a
detector class no scanner in the literature can have) + versioned
pattern-rule epochs inline (the §5b coefficient-epoch pattern applied to
scan rules), with live verification probes DISQUALIFIED inline (they
exfiltrate the candidate as their detection step — nondeterministic,
networked, on the seal hot path) and confined to Guardian staging/async
rule-fitness; (b) per-surface dispositions tuned so the cheap error is
the likely one (redact-and-reference w/ HMAC placeholders on durable
surfaces; push-protection-style block at seal w/ bypass as USER-authority
claim; pasted secrets auto-offered into the vault — leakage becomes
provisioning); (c) vault = own barrier on the durable plane under the
D-3 hierarchy, HMAC-ADDRESSED OUTSIDE THE CAS (secret dedup = a
confirmation-of-possession oracle — the one content class where dedup is
an attack), secret-zero deleted by summon-identity (SPIFFE
attestation-by-birth ≈ our summon pipeline; meta group as the trusted
third party), OS keychain = laptop unseal ROOT only; (d) injection =
secret:// refs + warden-bound RAM-only UNWITNESSED mount (the scratch
contract reused — secret bytes never cross FUSE_WRITE witnessing), env
vars banned STRUCTURALLY, rotation = targeted invalidation (the green
re-bind primitive); (e) event-driven leases (NIST 800-63B kills calendar
rotation), handoff = re-materialize under the new key_epoch (secrets
never in the brief), audit-as-claims fail-closed. Cross-tree: provider
gateway named MANDATORY chokepoint for the known-value scan (one more
forcing function on the unbranched gateway gap). Five rulings pending
in-thread; SECRETS.md draft to follow acceptance there.
Branch 28 rider (in-thread, 2026-08-18): the user's Postgres challenge
produced the TWO-POPULATION taxonomy for SECRETS.md's opening
definitions — (1) WORKLOAD secrets (property of the user's project;
Hecate stores/references/injects/detects/audits but never consumes; user
= granting authority; session/project scope; the seal boundary's
concern) vs (2) SYSTEM secrets (Hecate's own material — enrollment
identities, pod roots, transport/flow keys, vault KEKs, provider
credentials at the gateway; owners mostly exist already in
WIRE_SECURITY/D-3; vault holds the residue; identity plane = authority).
Structural rule: agent-visible secret:// resolves ONLY within the
workload population — system names are outside the namespace (not
denied; nonexistent). Five rulings still pending in-thread.
Branch 28 maximal forms PRESENTED in-thread (2026-08-18, on the user's
no-menus demand): detection = scan-before-CDC on the whole emission
stream (boundary-straddling secrets invisible per-chunk), Aho-Corasick
known-value automaton over ALL standard encodings (raw/base64/hex/URL/
JSON-escape — one O(n) pass), RE2-class linear engines only (no
backtracking DoS on the seal path), verifier-fed per-rule precision
ratchet, and the DX law: every "no" ships its pre-minted fix (span +
ready secret:// ref), FPs killed permanently via fingerprint-scoped
user-authority allowlist claims. Dispositions = boot-registered per
surface (unregistered emission surface FAILS STARTUP — chokepoint law on
emissions), redaction-in-chat IS the capture flow, block-at-seal carries
the one-action auto-fix. Injection = ONE resolver, THREE triggers
(boot-resolve loud-fail / bind-resolve at attachment prefetch /
JIT-resolve via agent-invoked request_secret) — bind IS JIT run by the
attachment step; JIT ungranted ⇒ turn PARKS into a grant claim in the
user's pane (grant-once/session/standing; denial typed, never a hang);
delivery = flow-key sealed, response-wrapped single-consumption
(interception DETECTABLE); registration atomic with materialization (no
scanner-blind window); revoked values keep HMAC shadows in the detection
index (bounded, derived). Lifecycle = leases ARE claims (drain law
force-revokes at handoff custody post), event-driven rotation only,
revocation cascade with a named completeness test, compromise of
workload creds ⇒ rotation-required claim to the user (system creds
rotate immediately), audit total + fail-closed. SECRETS.md draft next
in-thread on acceptance.
Branch 28 self-examination vs the tree (in-thread, 2026-08-18) — two REAL
conflicts found in its own design and resolved: (1) the JIT delivery step
violated the ratified ingress model (guests hold flow receive keys; a
warden unsealing payload = host payload-crypto, illegal) — resolved
CLEANER: the secrets lane is **warden-terminated by classification** (the
mount IS the endpoint; vault seals to the warden's lane key; guest access
= FUSE reads only; boot-classifier row `secrets_issuance →
warden-terminated, sealed, single-use, TTL`); (2) audit-as-claims cannot
hold for the SYSTEM population at boot (no session ledger exists) —
per-population audit devices: workload = session-ledger claims
(fail-closed as designed); system = durable operational log (Branch 39's
substrate) w/ boot-fails-loudly — **Branch 39 now on Branch 28's critical
path**. Self-correction: envelopes (fresh-CSPRNG-key sealed, unique
ciphertext by construction) ARE ordinary CAS content — the dedup oracle
runs through plaintext-derived addressing only; the VAULT INDEX is the
non-CAS mutable authority. Meta-scale design: three-way state split —
envelopes = async-everywhere on the durable plane (staleness of
ciphertext harmless); authority = small strongly-consistent state on the
EXISTING consensus tree by scope (session/user-home-region/root — no new
groups); **grant-epoch fencing at the warden mount-write makes
replication staleness harmless at the EFFECT** (externalization-fencing
law verbatim; stronger than Vault Enterprise's read-consistency race —
their model flagged for a receipts pass before citing); revocation = one
consensus epoch bump + invalidation fan-out, lease-shadow margin bounds
in-flight; **crypto-erase under async replication = the punchline: erase
the scope key at the authority, every envelope copy everywhere including
mid-flight becomes garbage — deletion consistency reduces to the small
state**; region rejoin protocol applies unchanged (dead-region grant
epochs fence-fail after rejoin). No global hot state; laptop = same code.
SECRETS.md full draft pending the user's word in-thread.
**Branch 28 META-SCALE REPLICATION REOPENED FOR RESEARCH (2026-08-18,
user: "investigate the meta-scale secrets replication… MAXIMALLY correct,
robust, performant, efficient, no-corners-cut").** The design-thread's §B
replication argument (envelope=async-CAS / authority=strong-consistent-
by-scope / epoch-fence-at-the-mount-write / crypto-erase-reduction /
region-rejoin) was derived from ratified laws + ONE flagged receipt
(Vault Enterprise), never grounded. Two parallel research passes
dispatched: (1) shipped KMS/secret-manager replication+consistency
behavior + crypto-erasure formalism; (2) the authorization-consistency
theory the design implicitly claims (Zanzibar zookies, Macaroons,
capability revocation, effect-vs-read consistency, short-lived-credential
school). Verdict question for both: does the presented design hold as
maximal, or is there a stronger pattern? SECRETS.md draft HELD pending
these dossiers.

**META-SCALE SECRETS REPLICATION — KMS/SHIPPED-SYSTEM DOSSIER LANDED
(2026-08-18)**; the authz-theory half is being RE-RUN on the service model
per user direction, so the SECRETS §B verdict is HELD for synthesis. KMS
findings (all primary-sourced): the 5-element design is at-or-above the
shipped state of the art. Envelopes-async-CAS = every shipped system
replicates ciphertext + separates authority (KMS MRK replicates key
material but NOT policy/grants; Secrets Manager primary→replica; Azure KV
async); the lone CP counterexample (GCP Secret Manager "replication is a
synchronous process", writes FAIL on regional outage) exists ONLY because
its read IS the effect with no downstream fence — our effect-fence is what
makes async safe. Authority-on-consensus = GCP Cloud KMS verbatim
("consensus always required among datacenters storing key material… for
cryptographic operations consensus is not required"). Effect-fence =
CONFIRMED as the Zanzibar-zookie / KMS-grant-token / Vault-X-Vault-Index
pattern, and OUR variant fences BOTH directions (grant-side like
KMS-grant-tokens/Vault-SSCT AND supersession-side like Zanzibar's
content-change check) where each shipped system fences only one. TWO
CORRECTIONS to fold into SECRETS.md: (1) **the fence has its own freshness
contract** — a materialization may proceed only when the warden's view of
the scope epoch is PROVEN current (live authority lease / bounded-staleness
consensus read); else DENY. Partition posture: never Azure's read-only-
failover inversion (effects proceed but epoch bumps can't) — fail
materialization CLOSED. (2) **crypto-erase = committed intent, NOT
completion**: the scope key is replicated in every group member's log +
snapshots + backups (NIST 800-88r2 + ISO 27040: "all copies of the target
keys must be sanitized"; AWS deletes replica-keys-first, 7-30d window,
"clusters from backups might contain deleted key material"). Fix =
store scope keys ONLY WRAPPED under an erasable root KEK so log history
holds only ciphertext (the KEK-cascade NIST r2 blesses); erase state =
committed→quiesced→complete (holder-purge ack loop for unwrapped RAM
copies) not boolean; pending-deletion window for high-blast user/root
scopes. (3) keep short TTLs on grants + short-lived/rotatable materialized
secrets — the fence does NOT subsume expiry (backstop for missed
invalidations + state-GC; ALTS/K8s/Chubby all keep both).
**META-SCALE SECRETS REPLICATION §B SETTLED ("accepted", 2026-08-18)** —
both dossiers (theory + shipped-KMS) synthesized; the 5-element design is
CONFIRMED maximal (Zanzibar-zookie / KMS-grant-token / Chubby-sequencer /
Kleppmann-fence class; ours fences BOTH grant + supersession at the effect,
which no shipped system does). THREE amendments accepted, to fold into
SECRETS.md §B: (1) the fence's own freshness contract — materialize only
when the warden's scope-epoch view is PROVEN current (pushed invalidations,
ALTS-local-CRL shape; revocation done-when-fences-ack); a warden with a
stale feed / lapsed lease fails materialization CLOSED; partition posture =
NEVER Azure's read-only-failover inversion (effects stop, not revocation).
(2) crypto-erase = committed→quiesced→complete, NOT one op: scope keys
stored ONLY WRAPPED under an erasable root KEK (log/snapshot/backup hold
ciphertext only — the NIST-800-88r2 KEK-cascade); quiesce = holder-purge
ack loop for unwrapped RAM copies; pending-deletion window for user/root
scopes. (3) expiry stays (fence ≠ subsume — SPIFFE/ALTS/K8s/Chubby all
keep both; backstop + state-GC); epoch folded into the Biscuit caveat so
token+authority can't diverge; epoch floor covers the COMPOSED decision
(single-authority chokepoint gives new-enemy safety free). Scale arithmetic
intact (envelopes on the exabyte plane; authority small on the existing
consensus tree by scope; no global hot state; ≥128-bit-AEAD invariant).
SECRETS.md now UNBLOCKED — presented in-message (grant section IAM-pending,
Branch 44).
**SECRETS.md verdict HELD (2026-08-18) — the user's namespace probe caught
real corners in the presented draft**: (1) NO tenancy/namespace model — the
draft**AUTHZ-THEORY RE-RUN + IAM DOSSIER LANDED (2026-08-18; service model;
all-primary receipts — Zanzibar/Chubby/Anderson/Macaroons/Cedar/NIST
PDFs read directly)** — Synthesis A CONFIRMS the §B settlement verbatim:
effect-fence maximal (enforce-at-CHECK collapses into enforce-at-EFFECT
only when check+effect are atomic; detachable effects — locks, secrets,
egress, commits — REQUIRE the resource-side floor; Kleppmann/Chubby/
CWE-367); stale-reads-safe iff complete-mediation + monotonic-floor-at-
effect + systematic-invalidation-with-expiry-backstop; fence-freshness
contract = ALTS local-CRL shape (CRL-not-expiry as source of truth —
Google's own clock-skew rationale ≡ our epochs-not-wall-clock law);
crypto-erase completion = max(replica-destruction acks, lease-shadow
margin), declared not assumed. IAM Synthesis B: ReBAC graph = universal
substrate (Zanzibar: hundreds of services, one model; roles = concentric
relations) BUT every production ReBAC bolts on a condition mechanism
(OpenFGA Conditions, SpiceDB CEL caveats, Cedar when) — graph+typed-
conditions is the real shape; Cedar = the only surveyed language meeting
the determinism/verification bar (total, side-effect-free, order-
indifferent, default-deny + forbid-overrides, typed-never-errors,
SMT-analyzable sound+complete, Lean-modeled, Rust, 28-80× faster than
FGA/Rego) w/ ONE divergence required: skip-on-error → typed fail-closed;
AWS evaluation ALGEBRA adopted regardless of language (deny-overrides +
union-grants + intersection-boundaries + intersection-session — maps 1:1
to hard-blocks/grants/SafetyPolicy/scope-down); STS role mechanics
(intersection-only scope-down; SourceIdentity-persists ≡ caused**IAM + AUTHZ-THEORY DOSSIER LANDED (2026-08-18, service-model re-run) —
grounds Branch 44 and re-confirms secrets §B with verbatim primary
receipts.** AUTHZ THEORY: effect-fence CONFIRMED maximal in exact form —
"a monotone version floor checked by the resource at the moment of the
effect closes the check-to-effect window no read-side discipline can
close" (Kleppmann verbatim "cannot fix by a check just before writing" +
"storage server must take an active role"; Chubby sequencer "recipient
server is expected to test... reject"; CWE-367). Enforce-at-CHECK
(Zanzibar) = special case of enforce-at-EFFECT when check+effect atomic
(zookie stored atomically with content version); detaches for locks/
secrets/egress/disk ⇒ effect is the general primitive. Stale reads safe
IFF: complete mediation (Anderson "always invoked") + monotone floor at
the effect (zookie/sequencer/epoch) + systematic invalidation w/ expiry
backstop (Saltzer-Schroeder "remembered results must be systematically
updated"; §1.12 REFUTED fence-subsumes-expiry — SPIFFE/ALTS/K8s/Chubby/
Macaroons/Biscuit ALL keep both; ALTS names CRL not expiry the source of
truth). Vault-Enterprise read-consistency (X-Vault-Index/412) = the weaker
placement, receipted. Both secrets §B corrections re-grounded: fence
freshness contract (ALTS local-CRL push + measured lag + fail-closed;
K8s TokenReview honors deletion only "60s or more" after — even authority
checks carry a bound); crypto-erase completion (NIST 800-88: complete only
when "all copies of the keys are sanitized" — authority replicas + escrow
+ live lease-shadow RAM copies; completion_time = max(replica-acks,
lease-shadow margin)). IAM MODEL (Branch 44): ReBAC relationship graph =
universal substrate (Zanzibar: hundreds of services one model; roles =
concentric relations; RBAC subsumed, ABAC subsumed ONLY w/ attached
condition mechanism — OpenFGA Conditions/SpiceDB CEL caveats/Cedar `when`,
EVERY production ReBAC adds one). Cedar = the policy language matching our
bar (total, side-effect-free, order-indifferent, default-deny +
forbid-overrides, typed-never-errors, SMT sound+complete, Lean-modeled,
RUST-native, DRT; 28-80× faster than OpenFGA/Rego; ONE divergence:
skip-on-error → make typed fail-closed for us). Rego REJECTED for
seed-replay (eval-time http.send/time.now_ns). AWS evaluation ALGEBRA
stolen regardless: deny-overrides + union-grants + intersection-boundaries
+ intersection-session-scope → maps 1:1 to SafetyPolicy(boundary)/
grants(session)/hard-blocks(deny). Role mechanics = STS transposed:
assume = session identity w/ INTERSECTION (never union) of role+session
policy; chaining carries provenance (SourceIdentity ≙ caused_by) + hard
duration cap (anti-laundering); confused-deputy avoided by-construction
(Biscuit third-party blocks / Macaroon contextual confinement). PDP/PEP
(NIST 800-207): PDP = decision service on consensus tree (decides+logs);
PEPs ALREADY EXIST (warden/Guardian/merge-gate/boot-classifier); decision
= f(request, policy-epoch, graph-snapshot) — the §5b/SCH19/zookie pattern.
UNIFICATION MAP (the mandate): Rank = domain authority relations + event
modulation @ ledger-Refuse PEP; SafetyPolicy = user boundary fragment
(intersection/caps-never-grants); Guardian = PEP + escalate-disposition
judge (HOLD stays agentic); Biscuit = portable attenuable revocation-id
serialization of a plane decision; **claim affordances = the plane READING
THE LEDGER-AS-GRAPH (axis-2 dependency = Zanzibar reachability literally;
the ledger already IS the ReBAC substrate)** [CORRECTED 2026-08-18, user:
the ledger is a fact SOURCE the PDP may read for work-scoped attributes —
"the ledger is NOT for role/permissions control plane work"; the
relationship/authority store is the IAM plane's OWN — Branch 44 second
correction]. CANNOT fold (flagged):
work-quality judgment, sensor tighten-only (composes as DENY layer,
Istio DENY-before-ALLOW), user supremacy. Agent↔agent governance = mesh
pattern on existing rails (SPIFFE-by-birth mint, policy names principals
not addresses, PEP = warden + FlowKeyGrant as the natural default-deny
moment — a flow key issues only when the plane edge exists at current
epoch). Repo governance (Br 35) = lineage resource policies + CODEOWNERS-
as-path-relations + required validations @ land PEP. Universal-plane
precedent: NO ONE runs literally one plane for all (Google runs ≥3);
leak points ALWAYS = dynamic context / resource-native last-inch /
judgment — but Hecate's domains already share one ledger, one identity
mint, one consensus tree, one PEP doctrine, so the historical forcing
conditions don't all apply. Branch 44 model exchange owed after the
namespace dossier (Branch 28 upstream interlock).

**VAULT-NAMESPACE DOSSIER LANDED (2026-08-18)** — Branch 28 unblocked;
amended SECRETS.md presented in-thread. Verdicts: (1) tenancy
discriminator — first-class namespaces exist iff tenants need their OWN
auth/identity/admin plane (Vault namespace = "mini-Vault": own auth
methods, identity store, policies, tokens; COST receipts: ~3500/~7000
namespace cap bounded by the serialized mount table, ~160/~220 depth at
40 bytes/path element; Azure reached the same endpoint by
vault-instance-per-tenant proliferation). Read isolation alone required
first-class NOWHERE (GCP = hierarchy-node policy attach + inheritance;
K8s+HNC = view-tenancy w/ delegated subnamespace creation; AWS = flat +
naming convention, with the ARN-entropy delete/recreate pathology).
(2) "NO cross-namespace visibility" phrasing CORRECTED by dossier:
Vault's real model = isolated by default + administrator-controlled
sharing + parent→child reference + privileged root. (3) Engines: mount =
router + storage barrier (UUID data root, "impossible for an enabled
secrets engine to access other data"); dynamic secrets = behavior-with-
state needing an addressable owner; even revocation is prefix-addressed
(`lease revoke -prefix aws/`); mount TABLE = serialized-state scale
liability; PKI unbounded-issuance receipts (50k–100k problem, 500k+
cluster impact; no_store + tidy remedies). (4) Policy anchor: unanimous
across Vault/AWS/GCP/Cedar/Zanzibar — policy names the STABLE LOGICAL
IDENTITY (path/ARN/node/entity/relation), never content or version.
(5) Corner a: automaton rebuild is ms-class linear (TruffleHog AC receipts
2x avg/3.58x single-target; Meyer IPL-1985 incremental-insert retains
complexities); the defect was keying rebuild to the SCAN EVENT instead of
the pattern-set version; automaton is secret-bearing ⇒ sealed residency;
GitHub minted-format receipts (prefix+checksum ⇒ 0.5% FP + offline
validation). (6) Corner b: per-materialization quorum read = NO-PRECEDENT
at any surveyed scale; receipted maximal = epoch-floor local monotonic
check (zookie shape) + sealed-grant mint-race bridging (KMS grant token,
≤~5min propagation envelope) + push-invalidation with TTL backstop (Vault
agent eviction); the revocation bound must be STATED. (7) Corner c:
index-pins-as-GC-roots (AWS staging labels) + derived version-count bound
(precedents 10/KV-v2, 100/ASM) + age floor (precedent 24h; ours DERIVED =
max lease TTL + freshness window T — the fence⇄GC closure) + unpin ≠
destroy + background tidy only (PKI). THIN: Azure per-vault throttling;
dynamic-delete-AC per-op bounds (paywalled).

**LEDGER/IAM SEPARATION — SECOND USER CORRECTION APPLIED (2026-08-18)**
(verbatim in Branch 44 entry). Swept into the amended Branch 28
presentation: §6 leases = vault-plane lifecycle state (NOT ledger claims;
the residual-lease force-revoke at custody transfer is a vault rule on
the handoff event); §6 audit = secrets-plane audit streams for BOTH
populations on the Branch-39 substrate (NEVER claims; the ledger records
work, not access records); §7 park-to-grant CLAIM stands (it drives a
user decision — that IS work) while the granted authority object lands in
the IAM plane's own store. Research-index "ledger IS the ReBAC substrate"
line annotated-corrected in place.

**IAM MECHANICS RESEARCH RELAUNCHED (2026-08-18, user: "try launching
the agent again")** — prior agent stopped mid-flight; fresh dispatch on
the service model covering: Zanzibar serving+storage internals (tuple
schema, changelog, aclserver cache/hedging, Leopard, Watch, config
rollout), SpiceDB (datastore/MVCC revisions, migration SQL, dispatch
hash-ring, ZedTokens, consistency modes), OpenFGA (immutable model IDs,
check resolution), AWS IAM/STS internals (evaluation algebra, AssumeRole/
chaining mechanics, per-service regionalized evaluation) + AVP, Cedar
paper + cedar-policy crate API + slicing + skip-on-error baseline, Vault
ACL/policy-store internals, compile-and-distribute precedents (OPA
bundles, Istio/Envoy xDS RBAC, K8s RBAC colocated authorizer, GCP IAM
propagation numbers, SPIFFE/SPIRE), synthesis WITHOUT recommendation.
Corrected charter framing (own store, never the ledger) baked into the
brief. Branch 44 design exchange follows its landing.

**IAM BUILD-MECHANICS DOSSIER LANDED (2026-08-18, relaunched agent)** —
grounds Branch 44 implementation. ZERO NO-PRECEDENT findings: every
needed mechanism has production precedent. Highlights (full dossier in
session transcript; verbatim receipts on file):
- **Zanzibar storage**: per-namespace Spanner DBs; tuple PK (shard ID,
  object ID, relation, user, commit timestamp) = MVCC in-row; changelog
  written in the SAME transaction (randomly sharded) feeding Watch;
  namespace configs = config + changelog tables, servers
  load-all-then-tail. Serving: fan-out from any server, consistent-hash
  delegation w/ BOTH-side caching, quantized eval timestamps ("one or
  ten seconds") respecting zookie floors, per-server lock table
  (anti-stampede), hedging, concurrent boolean-tree eval w/ cancel.
  Leopard: (T,s,e) set-container skip-lists; offline snapshot layer +
  Watch-fed incremental layer merged at query. Numbers: 1,500+
  namespaces / hundreds of apps; 2T+ tuples ~100TB; 10M+ qps; Check
  p50/95/99/99.9 = 3/11/20/93ms; 99.999%+ over 3yr; 200M cache
  lookups/s.
- **SpiceDB (buildable exemplar; actual migration SQL captured)**:
  relation_tuple rows carry created/deleted transaction (alive at R iff
  created≤R<deleted; delete = logical sentinel), later xid8+pg_snapshot;
  caveats (name + JSONB context) + expiration TIMESTAMPTZ on tuples;
  schema stored chunked + content-hashed per revision. Revisions:
  PG = xid8+snapshot w/ quantized-selection SQL; CRDB = HLC. **ZedToken
  = datastore-ID + revision + SCHEMA HASH — the only surveyed token
  fencing data AND schema at once** (also detects wrong-datastore
  tokens). Consistency modes verbatim (minimize_latency /
  at_least_as_fresh / at_exact_snapshot / fully_consistent; 5s default
  quantization). Dispatch: per-node consistent hash ring (no consensus;
  endpoint-watch membership), subproblem cache keys include eval
  timestamp, singleflight w/ traversal bloom filter. Preconditioned
  transactional writes (MUST_MATCH/MUST_NOT_MATCH); ImportBulk (one
  txn)/ExportBulk (resumable); Watch = {relationship updates, schema
  updates, CHECKPOINTS} — checkpoints ARE the applied-epoch signal our
  wardens need.
- **OpenFGA contrast**: tuples current-state-only (no MVCC) + separate
  changelog; models = IMMUTABLE ULID snapshots (pin
  authorization_model_id); NO zookie ("considering a similar feature")
  ⇒ receipted INSUFFICIENT alone for our fencing law. **Contextual
  tuples ("treated as if they were actual stored tuples during the
  evaluation of that request"; context takes precedence) = the exact
  precedent for our work-facts-as-request-context-only law.** Stored
  per-model assertions (test cases as data).
- **AWS IAM/STS**: full enforcement-code order verbatim (deny-first →
  RCP ∧ SCP ∧ (resource ∨ identity) ∧ boundary ∧ session; union for
  same-account identity+resource). **Receipted precedence hole: a
  resource policy naming the SESSION principal bypasses boundary/
  session implicit denies** — Hecate must decide this deliberately.
  AssumeRole: 900s–12h, default 1h; **chaining hard-caps at 1h
  regardless of role max**; session policy = intersection (≤2048 chars,
  ≤10 ARNs); tags ≤50 w/ transitive persistence, colliding inherited
  tag FAILS the assume; SourceIdentity set-once, immutable across
  chains, permission-gated both sides, in CloudTrail; ExternalId
  "controlled by [the deputy], not its customers". IAM eventual
  consistency verbatim + "do not include IAM changes in critical
  high-availability code paths"; authorization >400M calls/s (2021).
  AVP: IsAuthorized{PARC + entity slice} → {decision,
  determiningPolicies, errors incl. "does not exist in the slice"};
  Batch ≤30 shared-slice ≤100+100; templates w/ ?principal/?resource +
  RETROACTIVE propagation.
- **Cedar**: decision procedure verbatim (any forbid-true ⇒ Deny; else
  any permit-true ⇒ Allow; else Deny). **Skip-on-error baseline
  verbatim ("the policy does not factor into the authorization
  response; it is skipped") + their own safety argument against blanket
  deny-on-error — the erroring-FORBID-silently-stops-forbidding case is
  exactly what our typed per-effect fail-closed disposition fixes**
  (error-in-permit already fail-closed; error-in-forbid must fail the
  DECISION closed). Crate: Authorizer::is_authorized(Request, PolicySet,
  Entities) → Response{Decision, Diagnostics}; Schema/Validator;
  partial-eval behind `tpe`/`partial-eval` (PartialRequest/TpeResponse/
  EntityLoader) — the natural basis for compiling per-warden RESIDUAL
  policies; Apache-2.0. Validation sound for "most, not all errors" ⇒
  disposition load-bearing. Lean model + nightly DRT ~100M tests;
  cedar-policy-symcc property verification w/ counterexamples.
  Closed-world slice evaluation: the PDP does NO I/O mid-decision.
- **Vault internals (source-read)**: ACL = policies COMPILED to radix
  trees (exact/prefix/segment-wildcard) + capability bitmap at
  token-use; most-specific-wins w/ deny-at-equal-specificity enforced
  IN THE MATCHER (CVE-fix comment captured); policies in barrier, LRU
  2Q cache (1024); tokens carry policy NAMES, LATE-BOUND to content at
  eval (edits bite live tokens — the inverse of AWS's issuance-frozen
  sessions); perf replicas: policies async-replicate, tokens/leases
  deliberately cluster-local.
- **Compile-and-distribute shapes (all receipted)**: xDS full-snapshot
  push w/ version+nonce ACK/NACK + last-valid-config-on-NACK +
  make-before-break ordering; OPA signed gzip bundles w/ etag/304,
  delta bundles (JSON Patch), roots-scoped ownership, last-known-good +
  status API on activation failure, **decision logs stamped with
  bundles[_].revision** (epoch-stamped decisions) + masking hook; K8s =
  colocated-no-distribution (etcd objects ARE the store; chain
  short-circuit; additive-only, no deny rules; **Node authorizer =
  per-node principal w/ graph-computed perms — the warden-identity
  precedent**); GCP propagation "Typically 2 minutes, potentially 7
  minutes or longer" (groups: hours); SPIFFE/SPIRE attestation →
  selector-mapped registration → short-lived SVIDs.
- **Synthesis (no recommendation)**: store-versioning trichotomy
  (MVCC-interval / commit-ts+changelog / immutable-model+current-state)
  — only MVCC-with-schema-hash-in-token fences both planes; management
  verb union captured; PDP laws: compile-before-evaluate, closed-world
  slices, (subproblem, quantized-snapshot) memoization under the zookie
  floor, Leopard escape for deep nesting, decisions carry determining
  policies + epoch; **warden pipeline composite = OPA-style signed/
  revisioned/roots-scoped artifacts + xDS-style ACK/NACK/last-known-good
  + Watch-checkpoint epochs (each element receipted; the composite is
  ours)**. Revocation trichotomy: AWS short-TTL-no-revoke / Vault
  instant-late-binding / SPIFFE rotation — our push-invalidation + TTL
  backstop ≙ Vault-style late-bound grants + SPIFFE-style short
  sessions.
- Caveats: agent's WebSearch budget was exhausted ⇒ AWS-internal
  replication topology beyond official docs = NO-RECEIPT; THIN:
  Zanzibar staged config rollout, SpiceDB Leopard-equivalent, OpenFGA
  check internals, Cedar bench numbers/index structures, K8s
  aggregation verbatim, GCP inheritance verbatim, SPIRE rotation.
Branch 44 design exchange: OWED — sequenced AFTER the tenancy/blend
exchange (scale dossier in flight), since scope/tenancy shape the
authority store's sharding and the management surface's attachment
points.

**CLARIFICATION (user pause, 2026-08-18): SQL is NOT a design input.**
The build-mechanics dossier quoted SpiceDB/OpenFGA migration SQL because
that is where those systems state their data model most precisely —
evidence NOTATION, not a storage recommendation. Hecate's IAM authority
store rides Hecate's own substrate like every other authority: its own
consensus group(s), hecate-wire records, WAL/snapshot machinery, RSM
in-memory indexes, large immutable artifacts (schema/policy text,
compiled bundles) as CAS objects referenced by authoritative records.
Transposition recorded: their DB-borrowed revision domains
(xid8/pg_snapshot/HLC) ⇒ our group log position/epoch IS the revision
(no foreign MVCC bridge); their same-transaction changelog ⇒ our log IS
the changelog (Watch/distribute tail it); MVCC interval rows ⇒ records
carrying (created_pos, deleted_pos), alive at R iff created ≤ R <
deleted; ZedToken(datastore-id, revision, schema-hash) ⇒
(group-id, applied-position, schema-hash) — the same SHAPE as the
secrets-grant fence accepted in SECRETS §8.1, which covers secrets
grants ONLY. No IAM token, store, group, watch/checkpoint stream, or
distribution machinery exists or is designed at any status — Branch 44
designs and builds all of it from nothing. NEW Branch 44 exchange item: the point-in-time read window (how
long old revisions stay queryable) needs a derived GC bound on our
substrate — Postgres/Spanner gave the exemplars that for free.

**TENANCY-AT-SCALE DOSSIER LANDED (2026-08-18)** — the blend question
ANSWERED with receipts: AWS Organizations (flat immutable 12-digit
accounts, ARN self-routing, OUs = pure relations, ≤5 levels/2000 OUs,
depth-capped SCP walk, "All policy limits are hard limits", move =
reparent-only), GCP CRM (project ID "permanent"; move keeps ID + data +
direct grants, ONLY the inherited overlay recomputes; folders ≤10
deep/≤300 per parent), HNC (parent pointer = CR row in the child;
inheritance = eager copy-down) — the blend is SHIPPED three ways, and
HashiCorp's own guidance concedes it ("The entire list of namespaces
must fit into a single storage entry" / "Use namespaces sparingly" /
recommends ACL templating + an external onboarding layer over shared
mounts). Failure anatomies: single-serialized-artifact (Vault entry;
ZK-era Kafka controller O(partitions) reload, KIP-500; etcd 2GiB-default
keyspace binding K8s at 10^4 namespaces/1.5×10^5 objects) vs
sharded-rows-under-hierarchical-addressing (Zanzibar 1,500 configs vs
2T tuples sharded by object ID; Spanner/F1 >100M single-fragment
customer directories, 100–1000 Paxos groups per server, movedir =
background copy + atomic metadata flip; CRDB meta1/meta2 2^36 ranges,
512MiB/2500qps split thresholds, quiescence "not ticked... no
MsgHeartbeat" from source; AWS "millions of customers"; Colossus
metadata→BigTable "100x over the largest GFS clusters"; Twine 1M
machines sharded-by-job behind a single-pane proxy; KRaft
metadata-as-log w/ deltas+snapshots "even... millions of partitions").
Depth bounds are DESIGN constants everywhere (AWS ≤5, GCP ≤10, K8s
flat; Vault's ~160–220 = residual byte budget — the outlier).
Single-Raft-group envelope: ~10^2–10^3 sustained write qps / 100s of
MiB before the receipted answers kick in: split-under-addressing (CRDB),
bucket-move (Spanner movedir), or incremental consumption (KRaft).
THIN: Kafka 2M-partition seconds, Tectonic ~10-tenant figure, Twine
entitlement internals, CRDB per-node range cap, absolute AWS/GCP counts.
Feeds IAM.md §2, SECRETS §1b, and a CONSENSUS.md region-directory
amendment (splittable directory keyspace + meta addressing + lazy
descriptor repair).

**BRANCH 44 FULL ARCHITECTURE PRESENTED (2026-08-18)** — user command
(verbatim intents): "architect IAM for this entire system from ground
up. Maximally correct, no gaps, no compromises"; includes "the decision
tree, policy evaluation logic, request/action/etc. intercept logic for
each system"; "needs to work at *Meta scale*, cross region"; "*also*
needs to work locally on laptop *just as well*". IAM.md presented
in-message: object model; blend tenancy; own-store mechanics (never the
ledger); capability taxonomy under a compile_to_pep existence law
(generalizing SKILLS_API's compile_to_warden); typed-fail-closed
decision tree; compile-and-distribute; per-system intercept logic for
every plane; agent↔agent governance; assignment/assumption/chaining;
egress + repo governance; management surface + audit; cross-region
scale walk + laptop degenerate; test matrix; acceptance criteria.
Verdict owed. Write-to-disk only on accept.

**BRANCH 44 GRILL ROUND 1 (2026-08-18, user)** — four challenges: (1)
in-pod vs boundary-only intermediation ("isolated enough trust me bro"
vs "everything checked, UX miserable"); (2) knowledge systems missing +
claims board governance must be GRANULAR (see/execute/write ×
claims/testaments/artifacts/validations/deltas; hijack threat named) +
sessions-as-enforcement-layer ("think in layers"); (3) scope/tenancy
recommendation convicted as an ESCAPE HATCH — maximal answer demanded;
(4) IAM must be "*near physically impossible*" for agents to
manipulate. AMENDMENTS PRESENTED IN-THREAD: (1) boundary-complete
enforcement law — the pod boundary IS the complete effect surface
(VFS server-side, lanes warden-terminated, egress gatewayed, claims
through the core): IAM evaluates at boundary events (attach/load/
grant/edge), compiled residuals enforce per-IO at constant time,
in-guest computation is FREE, sensor observes tighten-only; (2)
six-layer model L0 metal → L1 session envelope (cross-session =
resolution-layer NONEXISTENCE, one door: brokered Grant) → L2
structural walls → L3 boundary caps → L4 policy → L5 judgment; granular
ledger matrix w/ metadata-vs-content split, typed artifact reads,
receipt-holder-only testify/activate (structural), double-entry edge
checks; ANTI-HIJACK laws H1–H5 incl. NO-AUTHORITY-TRANSFER (executor
acts with own authority ∩ attached scoped Grant, never issuer's) +
core-stamped unforgeable provenance; DERIVED-DATA-INHERITS-MOST-
RESTRICTIVE-SOURCE-SCOPE law (kills read-via-index laundering; forest/
vector ingestion = registered emission surfaces); knowledge governance
(contribution permits, provenance-weighted trust, source-scope
visibility); (3) scope subsystem upgraded to maximal: visibility =
chain ∪ grants at RESOLUTION (no exists-vs-denied oracle — D-3
reasoning), delegated-admin containment + non-interference invariant
(partition-keyspace structural), epoch-atomic reparent (wholly-old or
wholly-new chain, never mixed; cross-region reparent → CONSENSUS §7
externalization fence), scope lifecycle (create/freeze/archive/dispose)
+ derived quota attachment; escape-hatch framing RETRACTED (warrant =
AWS-Orgs/GCP/F1 receipts; Vault guidance demoted to failure anatomy);
(4) tamperproof triad (Anderson): T1 host-side-only plane (zero IAM
code in guests), T2 management-endpoint NONEXISTENCE on pod lanes, T3
type-level unbindability (iam/node_plane actions schema-marked
principal_kinds:[user,system_service]; agent bindings unrepresentable),
T4 record-signature-verified-at-APPLY on every replica (compromised
node or LEADER cannot mint authority), T5 signed artifacts, T6 node
blast radius = resident sessions only (no quorum, no keys), T7
high-blast mutations carry user-approval obligations, T8 probe =
sensor high-signal → hard block + quarantine. Tests IAM25–36 + criteria
15–20 added. Verdict owed.

**BRANCH 44 DILIGENCE ROUND (2026-08-18, user) — round-1 amendments
DEMOTED to proposals pending diligence.** User convictions, all accepted:
"solved the holes without doing diligence"; "no research backing, no
concrete details"; "no analysis of our existing designs to determine
conflicts"; "no comprehensive list of actions, principals, resources,
roles examples, policy examples"; "no practical mechanics of how we
replicate and distribute, what protocols we use — this simply just
magically exists?"; "How does it work with our storage types? What
networking does it use? Do we cache? How? How do we store audits,
access, storage of policies?"; "At Meta AND laptop scale to be clear."

REQUIREMENTS REGISTER for the IAM re-presentation (all mandatory):
R1 receipts on every claim (external security-receipts dossier IN
FLIGHT: Anderson triad, Saltzer-Schroeder, Firecracker/gVisor/virtiofs/
seccomp boundary receipts, Goguen-Meseguer noninterference, Denning
lattice, Flume DIFC, SELinux MAC/DAC, GitHub 404-privacy, Kafka/NATS
granular ACLs, Hardy confused deputy, ocap no-ambient-authority, OWASP
LLM01/excessive-agency, K8s ResourceQuota/lifecycle/NodeRestriction/
system:-prefixes, GCP/AWS lifecycle windows + liens, TUF thresholds,
Google BSRS multi-party authorization, seL4 proofs, Ed25519 verify
costs, CT append-only). R2 corpus conflict register (FOUR agents IN
FLIGHT covering all 25 specs + 5 architecture docs + CONTEXT.md +
secrets presentation; conflict categories CONTRADICTION/DOUBLE-SPEC/
GAP/HOT-PATH-COST/VOCABULARY w/ verbatim both-side quotes; plus
extraction of the exact existing machinery IAM must ride). R3 complete
enumerations: every principal (all system services named), every
resource type, every action (closed lists, no abbreviation), worked
ROLE definitions per office + system roles, POLICY examples as concrete
dialect text. R4 replication/distribution mechanics: record kinds,
log-stream integration per WAL consensus-substrate clause, message
flows, artifact transport (CAS-hash + pointer-record over named
PROTOCOL archetypes), compiler service placement per RUNTIME task
laws. R5 storage integration: where policy text/bindings/sessions/
grants/artifacts/audit live across consensus logs, CAS arena/pack
tiers, durable plane — named per storage type. R6 networking: which
planes/lanes/archetypes carry store↔compiler↔PEP traffic; identity +
sealing per WIRE_SECURITY lane classes. R7 caching: what caches exist
(residual artifacts, decision memoization, context slices), cache keys
(subproblem × epoch — Zanzibar quantization shape), invalidation =
epoch bump; what is deliberately NOT cached. R8 audit/access-record
storage: stream classes, encodings, retention, fail-closed
dispositions, per population. R9 decision tree + per-system intercepts
(round-1 text; must survive R1/R2 reconciliation). R10 EVERY mechanism
shown at laptop N=1 AND Meta cross-region (both scale walks, no
modes). R11 tamperproof T1–T8 (pending R1 receipts). Vocabulary risk
already self-flagged for R2: draft "Session" (assumed-role) collides
with CONTEXT.md "Session" (isolation unit) — rename owed (likely
"Assumption" or "AssumedIdentity").

Re-presentation assembles when all five agents land. Nothing asserted
before evidence; round-1 text stands only as proposal input.

**BRANCH 44 — ALL FIVE DILIGENCE AGENTS LANDED (2026-08-18).** Tally:
6 BLOCKERS, ~45 MAJORS, ~30 MINORS, plus the external receipts pass
(ALL CONFIRMED verbatim — Anderson triad, Saltzer-Schroeder incl. the
cached-result-invalidation clause, Firecracker 24-syscall/40+-device/
125ms/150-vm-s, gVisor Sentry, virtio-fs host daemon, seccomp 29-106ns,
K8s authz-at-apiserver, Goguen-Meseguer noninterference, Denning ⊕=LUB,
Flume label propagation, SELinux MAC-over-DAC, GitHub 404-not-403,
Kafka AclOperation enum, NATS deny-beats-allow, Hardy confused-deputy +
capability cure, ocap Property-D no-ambient-authority, OWASP LLM01 +
LLM06 "implement authorization in downstream systems", K8s ResourceQuota
403-at-admission / Active-Terminating / system:-reserved / NodeRestriction,
GCP DELETE_REQUESTED-30day + liens, AWS 90-day post-closure, TUF
thresholds/rollback/delegation + "root of trust must not rely on
external PKI", Google BSRS MPA + blast-radius compartments, seL4
functional-correctness + conf/int/avail theorems + timing-channel
caveat, Ed25519 273364-cyc/114µs verify → batch 56µs / dalek 25-40µs /
25-70k-per-s-core, CT append-only+monitors). Full dossiers cached in
$JOBTMP; conflict registers saved (agentA_register.md etc).

BLOCKERS + resolutions: (B-i) "Session"(assumed-role) vs glossary
Session → RENAME object to **Mandate**. (B-ii) H3 "agents cannot mint
user-plane claims" outlaws the Sibyl → reword to IMPERSONATION ban:
kind is a core-stamped record FIELD (not a wire branch); agents mint
claims AS agent-kind; Sibyl mints user-plane claims as itself (fine).
(B-iii) CAS policy-text has no GC root (OT9/§7 collects it) → IAM
records are the GC roots for their referenced blobs (index-as-authority,
the vault-envelope pattern). (B-iv) draft rewrote sensor
hold-and-escalate → un-overridable DENY → REVERT: sensor stays
tighten-only + escalate (narrows the compiled residual; NOT a decide()
step). (B-v C-1/F-2) freshness window T stalls session-local NEW
effects vs region-partition-Masked (CN13) → decisions serve from the
PEP's last-valid compiled artifact under last-known-good; T governs
REVOCATION propagation only, never decision liveness; root-feed silence
never blocks a session-path decision. (B-vi C-2) watch checkpoints =
banned per-group heartbeats (CN2) → NO periodic checkpoints; use the
existing demand-driven ordered-log subscribe/cursor/RESYNC (PROTOCOL
§4); revocation is a pushed supersession record (event-driven); freshness
= artifact carries an epoch-derived validity horizon (SPIFFE short-SVID
shape), refreshed pre-expiry only for pods holding a LIVE artifact —
idle groups push nothing.

MAJOR clusters + resolutions: (1) ledger read-granularity vs total-
within-session + delta-self-sufficiency (B2/C2) → read authorization
moves to a NEW named PEP, the **ledger serving edge** (per-pod,
host-side, where the warden already is): core stays identity-blind and
emits the whole byte-identical stream; the serving edge filters per
recipient via delta-subscription classes + traverse filtering compiled
from the residual; default within-session posture stays broad
(coordination substrate preserved), read-restriction is an optional
tightening for sensitive claim classes — the user's granular read EXISTS
without redacting deltas or filtering the core. WRITE/EXECUTE
(issue/testify/activate/evaluate) are refuse-set extensions (standing
only). (2) permit matrix vs "no enforcement layer atop claims" (C3) →
IAM decides STANDING (may this principal issue this KIND at all); claims
keep WORK-ORDER + SCOPE authority (unchanged); amend LEDGER.md to name
the split. (3) office→Role double-store (H1) → role-pack bindings DERIVE
at summon from the registry's AgentRole office binding (registry owns
agent→office; IAM owns office→capabilities; bindings are compilation
output, not a 2nd writable store). (4) rank pack (D1/D2) → COMPILED
PROJECTION of RANK.md's single source, freshness-exempt (core-local
inputs), one refuse-set member; RANK owns content (K1-K8 preserved).
(5) caused_by (C1) → principal-carried parentage VERIFIED against
core-known turn context at commit (keeps turn-mint, adds anti-forgery).
(6) validations (C4) → issuer-OWNED, multi-CONTRIBUTED (Guardian
validators enter w/ contributed_by). (7) confer rule (H3-agents) →
PassRole semantics (confer-permit), NOT hold-the-cap-yourself; Guide
summons write-pods holding only a confer-permit. (8) consult/challenge
(H2) → universal in shipped packs; clarification exempt from the permit
layer (structural, matches K3). (9) Archivalist cross-session archive
(H4) → archive at USER scope; same-user cross-session recall is up-chain
scope visibility, NOT a cross-fence reach; "one door" = cross-USER only.
(10) attach_artifact absent (H6) → add to family. (11) materialization
gate (E1) → add user-validation/review gate to the 7.7 conjunction.
(12) store-as-4th-home (PLATFORM) → NOT a 4th home; partitions ON the
existing root/region/session groups (zero new homes). (13) lineage
authority root-scoped (C-3) → SEPARATE the two trees: scope LADDER
(inheritance) = root→org→user→project→session (≤5; lineage=fork tree off
project, not a rung); failure-domain tree (authority placement/epoch) =
node<AZ<region; each scope's records placed by holder-containment
(lineage+root = root group; user/org = home-region; session = session
group). Answers Org placement (B1): Org is the rung between root and
user; laptop-degenerate collapses it. (14) Byzantine (F-1/C-7/T4) →
WRITE the FAULTS §1/§3 amendment admitting a SCOPED compromised-host
adversary FOR THE AUTHORITY PLANE (justified by the user's "near
physically impossible… escaped or otherwise"); apply-time Ed25519
signature verify (receipts: ~25-40µs/verify dalek, 25-70k/s/core) +
SIGNED snapshots (fixes C-7 install bypass). (15) splittable keyspace
(C-4) + cross-region reparent (C-5) → genuinely new consensus machinery;
THIN-flag + defer to a CONSENSUS amendment exchange; interim: 10^7 scope
rows fit one region group's storage envelope; reparent = rare admin op
via landing-class externalization fence + 2-phase record. (16)
mgmt-service/compilers unclassified writers (C-6) → classify: mgmt
service = lease+fence writer w/ named per-scope epoch; compilers =
CAS-first (artifacts content-addressed, no consensus write). (17)
FOREST contribute vs no-emission (D1) → contribute() targets ONLY
knowledge-graph/documents organs (Br 22/23), NEVER the Forest field.
(18) derived-scope vs governed lift (D2/E2) → add the governed-scope-lift
clause (promotion→archive=user scope; publication→published scope;
landing→lineage scope); forest is session-fenced by design (matches).
(19) knowledge plane no PEP (D3) → the field/index serving edge is a
named PEP (same resolution as the ledger serving edge). (20) vector
per-item scope vs hot-index-ban (E1) → scope granularity = generation
lineage (corpus selection), never per-vector predicate. (21) registry
cross-scope grant vs publication-only (B3) → registry resources are
grant-ineligible cross-scope; publication stays the only road. (22)
staging authority (B5) → fail-closed conjunction (REGISTRY owns
content-bound approval; IAM owns standing). (23) merge approve (MERGE) →
governing field is disk_write_mode; "Architect joins" stays MERGE's, not
minted in the IAM catalog. (24) evict vs SCH17 → REMOVE evict;
scale-down = disposal via existing lifecycle. (25) egress revocation →
keep SUMMONING §4 sever-existing; IAM composes, never weakens.

LANGUAGE-LAW amendments (update-all-sites-together): Session→Mandate;
Boundary-object→**Ceiling** (frees "boundary" for the pod perimeter);
refusal stays reserved for STRUCTURAL — forbid/ceiling denials on agent
tool calls surface as inform/yield (tightens the draft, honors
CONTEXT); Principal = Participant-viewed-by-authority (1:1 map stated;
wire never branches on kind — kind is a read field); "work lease" →
"the governing claim's deadline"; CONTEXT Warden/Affordance/SafetyPolicy
definitions amended in the SAME change as IAM.md.

Full reconciled re-presentation PRESENTED in-thread (R1-R11 satisfied:
receipts inline, conflict register w/ resolutions, complete
enumerations + worked roles/policies, replication/storage/networking/
caching/audit mechanics on named existing machinery, decision tree +
per-system intercepts, laptop+Meta scale walks, tamperproof w/ receipts).
Verdict owed; on accept, IAM.md + the companion amendments land in one
change.

**BRANCH 44 — STORAGE-SUBSTRATE QUESTION (user, 2026-08-18): "IAM
records ride as WAL entry payloads on top of *what database*? How are
they queryable? Updateable? Deleteable? Again, more research."** Real
gap: "WAL payload" = durability/replication, NOT query/update/delete.
CORPUS FINDING (grep-verified): Hecate has NO database, by design —
(a) OBJECT_TIER §2 EXPLICITLY REJECTED an LSM/mutable-keyed on-disk
engine with receipts ("LSM (ShardStore) earns its complexity only for
mutable keys and heat-driven re-placement — paid with soft-updates
dependency DAGs and an institutional formal-methods [burden]"); pack
store = append-only immutable content-addressed, in-RAM
`blake3→(volume,offset,len)` index, rebuild-by-scan. (b) LEDGER_CORE
holds mutable state as IN-MEMORY ARENAS; its relations arena =
`{from:Handle,to:Handle,rel:Relation}` + per-node in/out edge lists +
secondary index, queried by bounded `traverse(node,filter,depth)` —
i.e. ALREADY a ReBAC tuple/edge store, log-backed, snapshot-persisted.
(c) WAL owns "only the floor API"; each logical-log client materializes
+ checkpoints its own applied state. PROPOSED IAM ANSWER (grounding in
flight): IAM applied state = the log-backed in-memory edge-arena pattern
(update = superseding MVCC-interval record; delete = tombstone record;
query = traverse over edge indexes), snapshot-persisted to the content
tier, SHARDED by scope so each group's arena is RAM-bounded; cross-fleet
WhoCan = offline denormalized index (Leopard/SpiceDB-Materialize shape),
eventually-consistent read-optimization never authority. RESEARCH
DISPATCHED (service model): log-vs-state-machine-store separation
(etcd/bbolt, CRDB/Pebble, TiKV/RocksDB), MVCC/query/update/delete/PITR
mechanics in LSM+B-tree, the in-memory-authoritative+log+snapshot
alternative (Redis AOF+RDB, VoltDB/H-Store command-log, RamCloud
log-structured-memory), ReBAC edge-store shape (Zanzibar-on-Spanner as
the honest CHALLENGE — 2T tuples/100TB does NOT fit RAM → they chose a
DB; Leopard in-memory index as the counter; TAO cache-over-store),
scaling envelope + sharding + cross-shard denormalized index. Full IAM
re-presentation HELD until this dossier lands; the storage-substrate
answer folds into the store section (§3) with receipts. Note: this also
retro-grounds the WAL-payload extraction from the substrate reconciler
(IAM records as entry payloads = the DURABILITY leg; the arena is the
QUERY leg).

**BRANCH 44 — ARENA-REUSE OVERRULED (user, 2026-08-18): "That doesn't
even make any sense. Clearly we need some sort of organized storage
designed for extreme availability, low latency, and global scale."** The
"reuse the ledger's in-memory edge arena" framing is REJECTED and
recorded as the architect's error: the ledger arena is a bounded
per-session working-set RSM; a fleet-wide authority plane (roles/
bindings/grants across users/orgs/regions) is a purpose-built GLOBAL
storage problem. CORRECTED PREMISE: the IAM plane gets a first-class,
organized, globally-distributed storage subsystem designed for extreme
availability + low-latency reads everywhere + MVCC + global scale.
CONSISTENCY NOTE (not a corpus violation): OBJECT_TIER's LSM rejection
is SCOPED to immutable content and its own words name the carve-out —
"LSM earns its complexity only for mutable keys and heat-driven
re-placement"; mutable-keyed authority records ARE that workload, so a
purpose-built mutable-keyed MVCC engine for IAM is the case the
rejection names, not one it forbids. SHAPE (grounding in flight, Zanzibar
is the existence proof of all three requirements at once — 10M+ QPS,
p95<10ms, 99.999%/3yr, 2T tuples globally distributed): reference
architecture = [authoritative writes: per-scope consensus groups] +
[state engine: OWNED mutable-keyed MVCC — B-tree(bbolt-shape) vs
LSM(Pebble-shape) argued] + [global read-locality: local replicas
serving bounded-staleness reads under a freshness/epoch floor, NO
cross-region RTT on the decision path] + [reachability: denormalized
index, Leopard shape] + [availability: partition-survivable local
serving]. Running storage research (a39974...) REFRAMED toward this
(global HA/low-latency/scale distribution model as the headline; owned
B-tree-vs-LSM engine choice; DynamoDB-global-tables / Spanner-read-
replicas / AWS-IAM-global-replication read-locality receipts). Full IAM
re-presentation STILL HELD; the store section (§3) becomes a real
distributed-storage design, not arena-reuse.

**BRANCH 44 — IAM STORAGE SUBSYSTEM, CONCRETE DESIGN PRESENTED (2026-08-18,
answering "what subsystem? how does it sit on existing filesystems? what
replication? mechanics + internal structure?").** The store = an OWNED
log-structured MVCC keyed engine (LSM-family) assembled from existing
Hecate primitives, NOT a new filesystem and NOT the ledger arena. Key
insight: LSM sorted-runs ARE content-addressed pack blobs; LSM compaction
IS the existing copy-forward pack compaction; the memtable IS the arena;
the WAL IS the consensus log; replication IS consensus(log)+content-plane
(blobs). Structure: IAMRecord{key:(scope,kind,id), revision:LogPos,
body:Live(hecate-wire)|Tombstone}; sorted (key, revision desc). LEVELS:
L0 memtable (in-RAM arena, fed by applied consensus records) → L1..Ln
immutable sorted runs = pack-volume blobs {records, bloom, min/max key,
min/max rev} on NVMe tier by BLAKE3; a manifest (consensus-tracked) names
current run-hashes = store root at a revision. WRITE: mutation →
hecate-wire IAMRecord → consensus append (owning scope's Raft group) →
quorum-ack (durable) → apply to memtable (queryable). FLUSH: memtable ≥
derived-threshold → immutable run → pack blob → manifest add via consensus
record → WAL checkpoint floor advances. READ(key ≤ R): memtable then runs
newest-first w/ bloom+key-range+min-rev skip; Tombstone⇒absent — BUT hot
path = compiled residual at the PEP (store read is COMPILE-time, off the
decision path — why LSM point-read cost is not the hot path). COMPACT:
existing copy-forward merge → drop superseded+below-GC-floor + tombstones
→ new run → manifest swap → retire inputs (pack GC). GC floor =
max(grant TTL, mandate TTL)+freshness T+audit margin (derived).
REACHABILITY (WhoCan/WhatCan) = separate in-RAM denormalized reverse
index (Leopard (T,s,e) set-containers/skip-lists, offline+incremental,
log-fed) — eventually consistent read-optimization, NEVER authority.
REPLICATION dual: (a) consensus log via Raft across the scope group's
replicas (quorum, ordering, authoritative); (b) run blobs by hash via the
content plane (TRANSFER chunks-travel-by-hash, self-verifying, resumable,
ordering-free). Replica bootstrap = fetch manifest@floor → fetch run
hashes via content plane → tail log from floor (= WAL snapshot+tail /
CONSENSUS §5 snapshot-via-transfer-plane). GLOBAL READ-LOCALITY: each
region hosts replicas for scopes it serves (epoch-scope placement:
session→session group, user/org→home-region, root/lineage→root); PEP
reads LOCAL at rev ≥ epoch floor (bounded staleness, no cross-region RTT);
writes commit on the scope's owning group (region-local for user/session).
AVAILABILITY: region partition ⇒ local replica serves reads under last
floor (Masked, satisfies FAULTS); writes to away-scopes wait; node loss ⇒
group re-replicates from quorum + refetch runs by hash. TAMPERPROOF T4:
each IAMRecord + manifest carries mgmt-service Ed25519 sig, verified at
apply on EVERY replica AND at run-load AND on snapshot install (fixes C-7
bypass); ~25-40µs/verify (dalek), off hot path. Engine choice B-tree vs
LSM: LSM wins on STRUCTURAL grounds (composes append-only immutable pack
tier + copy-forward compaction; B-tree needs a new mutable-page format
that fights the substrate) AND access-pattern (hot path is the compiled
residual, not the store, so LSM point-read cost is off-critical-path);
quantitative confirmation lands with the running storage dossier
(a39974...). Laptop degenerate = same engine, failure-domain tree
collapsed to 1 node, 1 replica, zero modes. Presented in-thread; folds
into IAM store §3.

**BRANCH 44 — IAM STORAGE MAXIMALITY CHECK (user: "maximal? no
shortcuts? conflicts?").** Architect declined to certify prematurely.
Two diligence items IN FLIGHT before certification: (a) engine-choice
dossier a39974... (B-tree vs LSM w/ numbers + global HA/latency/scale
distribution receipts); (b) NEW storage-corpus reconciler abfd6b...
checking the concrete LSM-on-pack-tier design vs OBJECT_TIER/WAL/
CONSENSUS/TRANSFER/VFS/FAULTS/RUNTIME/PROTOCOL (the prior 4-agent
reconciliation checked the ARENA-framing draft, NOT this LSM design).
Architect's own thin-spot list surfaced (recorded in
$JOBTMP/iam_storage_design.md KNOWN-OPEN): (1) "compaction generalizes"
was a SHORTCUT — pack copy-forward is OBJECT-granular, LSM merge is
RECORD-granular NEW logic; (2) large-run CDC-chunking vs coherent
merge-reads + bloom-over-logical-run unverified; (3) reachability index
has NO memory budget/scope-partition (unbounded-growth risk); (4) local
NVMe I/O contention compaction-vs-session-hot-path unpriced
(non-interference law is network-only); (5) per-node LSM proliferation
vs CN2 idle-zero-cost + RUNTIME task tracking; (6) manifest-churn as
consensus records (log bloat?); (7) content-plane GC + run-retirement
wiring (IAM manifest as mark-from-roots root); (8) PITR-below-floor
typed failure. Design file written for reconciliation. Certify-or-revise
when both agents land; then storage §3 folds into the full IAM
re-presentation. NOT asserting maximal until diligence returns.

**BRANCH 44 — ENGINE-CHOICE DOSSIER LANDED (2026-08-18, a39974...).**
DECISIVE FINDING (NO-PRECEDENT, searched): "a production, globally
distributed authorization plane whose AUTHORITATIVE store is an
in-memory arena/heap with only log+snapshot durability" — NONE EXISTS.
Every surveyed authz/identity plane (Zanzibar, SpiceDB deployments,
AWS IAM, KMS, TAO-as-authz, Vault) puts authority in a REPLICATED
ON-DISK DB/engine and uses in-memory structures STRICTLY as derived
caches/indexes; the only in-memory authz datastore (SpiceDB memdb) is
documented non-HA/ephemeral/dev-only. This is the strongest possible
corroboration of the user's arena-reuse OVERRULE. Universal architecture
fact CONFIRMED: every consensus record store separates (a) append-only
ordered LOG + (b) mutable-keyed sorted queryable ENGINE the log applies
into + (c) applied-index watermark; reads from (b), never scanning (a).
etcd = Raft-WAL + bbolt-B+tree + consistent_index (its OWN RBAC lives as
authRoles/authUsers buckets — authz-in-consensus-B+tree is a boring
working precedent); CRDB = per-range-Raft-log + Pebble-LSM ("storage
layer commits writes from the Raft log"); TiKV = two RocksDB (raftdb +
kvdb); Spanner = Paxos-log + "B-tree-like files + WAL" on Colossus,
reads "at any replica sufficiently up-to-date". MVCC universally =
version-rows keyed by revision/timestamp (etcd (rev,sub,type); CRDB/TiKV
HLC-suffixed; Zanzibar PK (shard,object,relation,user,commit-ts) — the
IAM record shape LITERALLY); delete = tombstone + async reclaim
(compaction/defrag); PITR = read within GC window, explicit horizon
error beyond ("required revision has been compacted") — a documented
contract everywhere, NOT a gap. REFERENCE ARCHITECTURE confirmed leg-by-
leg with receipts: [1] per-scope consensus groups, geographically TIGHT
quorums (Zanzibar 5 voters ≤25ms apart; one global group anti-receipted
by etcd 50s election ceiling) + changelog dual-write same-txn; [2] owned
mutable-keyed MVCC engine; [3] global read-locality = FULL replication +
non-voting local replicas serving BOUNDED-STALENESS reads under a
freshness token (zookie: "at-least-as-fresh"; Safe-requests 2 orders >
Recent, "vast majority of checks locally"; Spanner ≥10-15s local-serve;
KMS "all authorization information... available on all regional hosts");
[4] reachability = denormalized in-memory Leopard set-index ((T,s,e)
skip-lists, RAM-served, offline-built + Watch-fed; <1ms p99; commercial
twin AuthZed Materialize) — the DERIVED layer where the ledger's
snapshot+log-replay competence legitimately lives; [5] availability =
partition-survivable LOCAL serving, NO cross-region RTT on the decision
path (KMS 99.999%, DynamoDB-global-tables 99.999%, Zanzibar 99.999%/3yr
absorbing 10s Spanner leader re-elect in the Recent threshold). Numbers:
Zanzibar 2T tuples/100TB/10M+ QPS/p95<10ms/p50~3ms/>10k servers/30+
locations; IAM 400M+ auth-calls/s. B-TREE vs LSM DISCRIMINATOR
(receipted, bbolt's own guidance): read-heavy/range-scan → B-tree;
>10K random-writes/s → LSM. IAM is read-DOMINATED (Zanzibar 25K writes/s
vs 12.2M reads/s, 3 orders) w/ small per-scope shards → by ACCESS
PATTERN the B-tree's simplicity "wins ground"; BUT Hecate-specific
SUBSTRATE FIT cuts for LSM (pack tier is append-only-immutable =
SSTable disk model; a B-tree needs a mutable-page format fighting the
substrate, or a COW-B-tree = still a mutable-root page store, not
content-addressed blobs). ENGINE CHOICE NOT YET CALLED — it hinges on
whether the pack tier CLEANLY HOSTS SORTED RUNS (thin-spots #1
object-vs-record-granular compaction, #2 large-run chunking) = exactly
what the running storage-corpus reconciler (abfd6b...) determines. If
pack-tier composition holds → LSM substrate-fit decisive; if not → both
engines need a new on-disk format and read-dominated-small-shard tips
toward B-tree. Certification + storage §3 + engine decision wait on the
reconciler. THIN in dossier: Vault-secondary-partition semantics,
Spanner t-safe internals, DynamoDB ms-phrasing, RAMCloud-2009-not-2015,
Neo4j exact source-of-truth phrasing, TiKV MVCC key encoding depth.

**BRANCH 44 — STORAGE-CORPUS RECONCILER LANDED (2026-08-18, abfd6b...) —
the last gate.** Verdict: skeleton composes real machinery, but NOT
maximal as sketched. THREE claimed-reuses corrected: (A PARTIAL) a run
is NOT a single pack blob — it's a content-addressed MANIFEST-OF-CHUNKS
(ContentRef root over CDC chunks); full-run merge-scan NOT broken
(manifest order preserves byte order); bloom+min/max go in the store-root
for zero-fetch skip, bloom in the run's header chunk via ranged_get.
(B REFUTED — my thin-spot #1 CONFIRMED) pack copy-forward is
chunk-granular GC reclaim "never for updates"; record-merge is ENTIRELY
NEW logic; BUT OBJECT_TIER §2's LSM-rejection criterion ENDORSES this
use ("LSM earns its complexity only for mutable keys… keeps bulk bytes
outside the tree") — cite §2 as SUPPORT, stop claiming merge-reuse.
(C PARTIAL) "new WAL kind:u8" is wrong layer — IAMRecord = a hecate-wire
SCHEMA kind inside raft ENTRIES; and the store-root manifest should BE
the group's CHECKPOINT (WAL §6 floor API), not an ever-appending swap
stream — resolves the churn concern. CONFIRMED-fits: (D) content-plane
run fetch + batch_exists-dedup + snapshot+tail bootstrap; (Task3-4)
epoch-scope placement (session→session grp / user-org→region / root-
lineage→root) CONFIRMED against CONSENSUS §6 holder-containment (caveat:
a globally-mobile principal's holders force root scope). (E PARTIAL) IAM
manifest is a legit added mark-from-roots root but OBJECT_TIER §7's root
list must be AMENDED (update-all-sites); dedup interacts CORRECTLY
(shared chunks stay live); "become garbage" was loose. 
TWO BLOCKERS: (C1) FAULTS obligation-matrix cells for {IAM store,
compaction, reachability index} × every fault class are boot-validated
CI and currently ABSENT — must author them (mitigant: FAULTS §2
dispositions already classify the artifacts — run chunks=re-fetch-by-hash,
manifest=rebuild-from-quorum/N=1-refuse-loudly, index=discard-and-
re-derive); my region-partition cell mis-stated (reads Masked but
writes-to-away-scopes = Degraded, split cell). (C2) runs must NOT be a
second on-disk format — "exactly one on-disk store format exists… a
second of any is unrepresentable"; a run is a LOGICAL content object
(hecate-wire sorted records + index block + bloom) CDC-chunked into pack
chunks — internal structure is CONTENT, on-disk format stays the pack
volume; stated as a literal .sst it's a BLOCKER.
THREE DOCTRINE TENSIONS: (C4) CONSENSUS §3 "ReadIndex only, v1. Lease
reads do not exist" vs bounded-staleness local reads → for session/user
scopes the owning group IS region-local so ReadIndex is region-local (no
WAN, satisfies "no cross-region RTT" w/o a new mode); root/lineage lean
on the compiled-residual escape (store read at COMPILE time, off the
decision path); any genuine local-read optimization = a CONSENSUS
amendment, never a flag. (C5) CN2 no-per-group-timer vs time-derived GC
floor → node-level amortized sweep or event-driven advance, never a
per-group timer. (C6) no-unbounded-growth vs reachability index →
derived budget (copy OBJECT_TIER §2 index-RAM formula items×per-item-cost
vs node RAM + escape hatch) + scope partition + eviction (safe: it's
derived, evictable, NEVER authority). MINORS: C7 "manifest" vocab
collision (rename store-root → "IAM root"/"level set"); C9 revision=LogPos
is PER-SCOPE not global (PITR at rev≤R is per-group; revision must be the
committed/applied index, not raw append pos); C10 Ed25519 "management
service" custody/rotation belongs in Branch 25 key hierarchy + RUNTIME §4
FFI-lint allowlist, verify-at-apply is apply-path CPU (~25-40µs) off the
read path; C11 arena/index/checkpoint overloads; C12 memtable-apply must
advance applied watermark in the SAME txn (CONSENSUS §2); C13 derive
bloom-FP/flush-threshold/T/audit-margin/part_floor at definition sites
(zero literals); C14 the compiled-residual hot-path claim is IAM-domain,
unverifiable vs storage specs, C4's severity depends on it.

**ENGINE CHOICE RESOLVED → LSM (owned, over the pack tier).** The B-tree
vs LSM fork is settled NOT on access-pattern (which mildly favored
B-tree: read-dominated small shards) but on the ONE-ON-DISK-FORMAT LAW
(C2): a mutable-page B-tree is a SECOND on-disk format = "unrepresentable";
an LSM's immutable sorted runs CDC-chunk into the EXISTING pack format as
content; OBJECT_TIER §2 explicitly ENDORSES an LSM-consumer over the
immutable pack tier; and the compiled-residual model puts store reads at
COMPILE time so the LSM's weaker point-read is off the hot path — its one
disadvantage neutralized. LSM wins because it's the only engine that
composes Hecate's substrate without violating the one-format law.

STORAGE §3 now GROUNDED + CORRECTED; all research in (5 reconcilers +
engine dossier + storage-corpus reconciler). Ready to assemble the full
IAM re-presentation (R1-R11) on the user's word.

**BRANCH 44 — ACCEPTED + IAM.md WRITTEN (2026-08-18, user: "accepted!").**
docs/specs/IAM.md written whole (§0 separation law, §0b six layers, §1
seven objects incl. Mandate rename, §2 blend tenancy + scope ladder vs
failure-domain tree, §3 owned LSM store grounded+corrected, §4 full
taxonomy w/ compile_to_pep existence law, §5 decision tree, §6
compile-and-distribute + caching, §7 per-system intercepts, §7b ledger
matrix + anti-hijack H1-H5 + derived-data law, §8 boundary-complete, §9
assignment/assumption/chaining, §10 worked roles/policies, §11 storage/
net/cache/audit, §12 tamperproof T1-T8, §13 mgmt surface, §14 scale
walks, §15 IAM1-36 + IAMS1-6, §16 acceptance 1-16, §17 companion
amendments). Verdict: ACCEPTED whole after 6 diligence dossiers (5 corpus
reconcilers + engine + storage-corpus) resolved 6 blockers + ~45 majors.
Branch 44 status: SPEC-WRITTEN. REMAINING = the §17 companion amendments
(update-all-sites-together, one change) + the deferred splittable-
keyspace/cross-region-reparent rider (own exchange, GAPS.md). SECRETS.md
still owed (its §4/§7 rewrite to reference IAM lands when SECRETS.md is
written).

**BRANCH 44 — §17 COMPANION AMENDMENTS LANDED (2026-08-18).** All
update-all-sites-together edits committed across three batches: CONTEXT
glossary (authority plane/Principal/Ceiling/Mandate/Grant + Affordance/
Warden/SafetyPolicy), OBJECT_TIER §7 IAM roots, FAULTS §1/§3 scoped
authority-plane adversary + §5 three-subsystem cells + F8 + AC-1 note,
PODS §6 residual compile-source, LEDGER inv.9 standing/work-order split +
ledger serving edge, RANK §1 pack-as-projection, REGISTRY Scope-as-
projection + AgentRole/Role split, CONSENSUS §3 region-local ReadIndex
note, FOREST §5b governed scope-lifts + emission-surface + provenance
stamps, VECTOR_INDEX §5 generation-lineage scope granularity + manifest
stamp. GAPS.md updated: IAM.md added to component inventory (ACCEPTED),
moved out of §3 undesigned, D-14 opened (splittable-keyspace + cross-
region-reparent rider), SECRETS §4/§7 rewrite deferred to Branch 28.
DEFERRED (each owed its own exchange, NOT done): D-14 consensus
machinery; SECRETS.md write. Branch 44 = SPEC-WRITTEN + reconciled.

**C-7 STATUS-LINE AUTHORITY — RESOLVED for the foundation set (2026-08-18).**
Authority rule now law (recorded in GAPS.md C-7): the spec file's `Status:`
header is the SINGLE source of truth for acceptance; it reads `ACCEPTED
<date>` only on an explicit dated whole-spec verdict (verdict quote in the
header); GAPS §1 mirrors it; **this GRILLING "SETTLED" table denotes
DIRECTION-settled (a design direction chosen), strictly weaker than
spec-accepted — never read as acceptance.** Verified by direct header read:
foundation set headers were ACCEPTED all along (RUNTIME/WAL "amend and
accept" 08-17; PROTOCOL "accepted." 08-18) — the C-7 "conflict" was a STALE
LEDGER (GAPS inventory unsynced), now fixed; MERGE same drift, synced.
Genuinely header-presented and CORRECT (awaiting explicit whole-spec
verdicts, not a status fix): VFS, PODS, AGENTS_RUNTIME, RANK, SCHEDULER.

**BRANCH 14 / SCORE SERVICE + SCRIBE-COMMS — DESIGN PRESENTED, SENT TO
RESEARCH (2026-08-19).** HANDOFF spec (Branch 14) presented in-thread
(five tiers: gathering/weighing/storage/trigger+CUSUM/execution +
Guardian SPRT+fresh-context-probe + commissioning + 16-Sylk-lessons
tests). §3 storage challenged by user → surfaced that the SCORE SERVICE
is referenced across the corpus (RANK §4, PLATFORM §6, LEDGER_CORE §2c,
HEALTH, FOREST, AGENTS) but its ARCHITECTURE (placement/distribution/
communication) is UNDESIGNED — a dangling-reference gap. Also raised:
agent↔Scribe communication is undefined (protocol/data/does-it-go-
through-the-warden). PRESENTED design (HELD pending research):
- Score service = deterministic harness TASK (not pod/agent/external/
  separate-process), one per session group, IN the colocation unit
  (next to field service); computes per-(agent,domain) score as a pure
  function of ordered inputs (ledger deltas + event-carried Scribe
  signal snapshots), pushes score snapshots into LEDGER_CORE local
  state (§2c, no synchronous query); re-derivable, checkpointed,
  consensus-backed via the session group (NOT peer-to-peer, NOT global,
  NOT external, region-local).
- Agent↔Scribe = OBSERVE-not-send (the monitored cannot feed/manipulate
  its monitor — PLATFORM §6 rationale); no primary-guest→Scribe channel;
  Scribe consumes host-side chokepoint streams (warden verdicts via
  health plane + sensor + ledger deltas + gateway usage); does NOT get
  raw LLM transcripts (robustness); carriage = PROTOCOL delta/ordered
  streams over the Scribe pod's host lanes, session-group-local.
USER OVERRULE/CONSTRAINTS (2026-08-19): (1) MUST be research-backed —
learn from Sylk Scribe/score patterns+faults + external SIDECAR patterns
(user cited SoloIO's in-process gateway vs Istio sidecar + "significant
latency benefits"; the per-pod-sidecar tax the industry left). (2) MUST
research telemetry/observability/monitoring at META SCALE translating
DOWN to laptop w/o eating resources (max correct/robust/performant/
efficient, no modes). (3) ISOLATION CONSTRAINT: injecting the Scribe
(a second agent) into the primary's microVM breaks isolation/boundaries
— rules OUT naive co-residence; sharpens toward isolated-pod vs
per-node-shared (ztunnel-shape) vs split (cheap-per-node collector +
expensive-per-identity narrator, the Ambient L4/L7 split). THREE
research agents IN FLIGHT: Sylk Scribe/score internals (a007b0bf...);
external sidecar-placement patterns w/ numbers (a7ffa4ec...); telemetry
Meta-scale→laptop pipeline (dispatched). "Scribe = own microVM pod"
DEFAULT now UNDER CHALLENGE (it's the Istio per-pod-sidecar pattern the
industry moved off). Design re-presents on all three landing.

**CO-RESIDENCE NOT EVICTED (user correction, 2026-08-19):** "*Is*
co-residence out though? Or are you just prematurely evicting it... This
is literally what research is for — can we co-locate processes and
effectively isolate them." Architect's "co-residence is out" RETRACTED as
premature. Co-location-with-isolation is now a FIRST-CLASS researched
option. THREAT-MODEL is the crux (established as the research axis):
isolation vs a merely-FAULTY/degrading primary (easy — process
isolation) vs a COMPROMISED/adversarial primary (hard — needs a boundary
a guest-kernel compromise can't cross). KEY INTERNAL PRECEDENT: Hecate
ALREADY runs a co-located in-guest observer — the SENSOR — explicitly
semi-trusted ("a guest-kernel exploit defeats the sensor; the warden and
VM boundary still hold", PODS §6). So the corpus already licenses an
in-guest observer at a defined (semi-trusted) tier; the open question is
whether a co-resident Scribe rides that same tier or needs warden-class
tamper-proofing. FOURTH research agent dispatched (a2bec1a9...):
co-located process/VM isolation mechanisms + strength per threat model
(intra-guest namespaces/seccomp/Landlock/cgroups; gVisor/WASM
intra-guest second boundary; same-node separate microVMs + vsock;
K8s-multi-container-pod precedent; confidential-computing-is-VM-not-
process; starvation isolation via cgroups). Placement decision now spans
FIVE candidates: same-VM-separate-processes, same-VM-monitor-behind-
gVisor/WASM, same-node-separate-microVMs+vsock, host-side warden-class,
own-remote-pod. FOUR agents now in flight (Sylk, sidecar-placement,
telemetry, co-location-isolation). Design re-presents on all landing.

**TELEMETRY META-SCALE→LAPTOP DOSSIER LANDED (2026-08-19, a87cce1a;
resumed after a machine-sleep interruption).** 100% primary-source
(WebSearch exhausted ⇒ all direct PDF/doc fetches). THE LAW (no
small-mode/big-mode): "autonomous-local-first — each node runs ONE code
path: collect into an in-memory hot ring, sample+aggregate AT the point
of collection so cost tracks RETAINED SIGNAL not raw volume, federate
upward only when an upward exists. N=1 is a zone of one running the
identical binary; N=many is the same leaves + a global query plane on
top." (literal Monarch zone/global architecture + Prometheus
single-node-autonomous property.) RECEIPTS: Gorilla (in-memory
write-through cache, 26h hot window answers 85% of reads <1ms,
delta-of-delta+XOR = 1.37 B/point/12×, 96% timestamps→1 bit, buffer ≤64kB
before flush = tolerated loss; 2B series in 1.3TB/20 machines). Monarch
(in-memory ON PURPOSE to avoid circular dependency on monitored storage;
LIGHT compression on hot tier, TS-sharing ~10:1; collection-aggregation
36:1 [≤1e6:1] on 1 CPU core = 25% CPU vs query-based; PUSH beat PULL —
stated lesson; zone-autonomous, 95% queries answered in-zone; fingerprint
1.3 B). Dapper (sampling NECESSARY + aggressive-sampling-doesn't-lose-
signal "if a pattern surfaces once it surfaces thousands of times";
1/1024 default, 0.01% high-traffic, ADAPTIVE RATE-BASED so low-traffic
auto-raises/high-traffic auto-lowers; span 176-204ns, daemon <0.3% core,
<0.01% net, out-of-band local-log→pull). Scuba (in-memory memory-bound,
sample_rate column COMPENSATED in aggregates, 30d/100GB expire-at-ingest,
drop-leaves-past-10ms + warn-if-<99.5%). OTel (agent=stateless
batch/compress/ship pushes DOWN; gateway=stateful; SINGLE-WRITER
convergence required for per-identity aggregation — trace assembly/dedup/
per-name rollup). Prometheus (1-2 B/sample, single-node-autonomous
"rely on it when other infra is broken", local-first + optional
remote_write; NOT for 100%-accuracy billing = the lossy-tolerant trade).
GWP (2-D sampling machines×events ⇒ <0.01% aggregate overhead, capped
"<a few percent" — overhead bounded INDEPENDENT of fleet size). Cardinality
= the multiplicative cost bomb (never key series on unbounded identities).
DESIGN IMPLICATIONS (validate the sketched score/Scribe): (1) score
service = the single-writer convergence point per session group (OTel
principle) — confirms colocation-unit placement; (2) Scribe AGGREGATES+
SAMPLES at source, pushes SNAPSHOTS not raw (Monarch push + Dapper
adaptive-sample + event-carried-snapshot pattern) — bounded cost; (3)
NEVER block a claim on a telemetry write (Monarch circular-dependency +
Gorilla tolerated-loss) — confirms "scores are harness state, nothing
touches the ledger" + async-by-default; (4) per-node in-memory hot ring
w/ Gorilla-style light streaming compression + bounded retention for
operational signal, durable tier separate/lossy-tolerant; (5)
telemetry/signal plane ≠ ledger (hot-ring-vs-cold-store split); the
single pane is a FEDERATION layer over autonomous nodes, not a 2nd
pipeline (matches D-single-pane). NO-PRECEDENT flagged: "% infra on
observability" (unsourced), eBPF/Hubble specific overhead (GWP
substituted). THREE agents still out: Sylk (a007b0bf, resumed),
sidecar-placement (a7ffa4ec), co-location-isolation (a2bec1a9).

**SYLK SCRIBE + SCORE-SERVICE DOSSIER LANDED (2026-08-19, a007b0bf,
resumed post-sleep).** file:line-grounded forensic read. CONFIRMED
findings: SCRIBE = in-process goroutine set (-feed + -periodic) co-located
in the parent's AgentPod, ONE PER PARENT TYPE, on the parent's shared
GoroutineScope — NOT isolated (scribe.go:315-323, agent_pod.go:794-832).
Agent→Scribe comms = DUAL: (1) PUSH via bounded LOSSY Go channel (feedCh
cap 32, drops oldest on overflow — parent controls fill-rate AND content
= a starvation/manipulation surface), carrying RAW TURN TRANSCRIPTS; (2)
OBSERVE via activity-fabric subscription (typed activities). Both live in
prod, both hit processFeed, NO DEDUP — the fabric path was "documented as
REPLACING push" but push never removed (SCRIBE_FABRIC Phase-10 cleanup
never ran) = the same ghost-class as the perf-handoff eviction. Scribe is
a continuity CARRIER not a handoff initiator (no trigger logic in the
package). SCORE SERVICE = the core/handoff GP stack: per-agent-INSTANCE
GP in a HandoffBridge (in-process) + process-global HandoffSupervisor
(profileLearner keyed agentID+model) + ServiceRegistry. Scoped
per-(agentType,model) process-global — NO per-session, NO per-domain, NO
rank/bindingness (Hecate-NEW, no Sylk antecedent). CONFIRMED FAULTS: (1)
SPLIT-BRAIN — THREE profile copies: b.profile (NEVER updated),
profileLearner (updated every turn + real outcomes), blender (synced from
the STALE b.profile); the learned threshold NEVER reaches the decision
(exact "learner updates / controller reads stale" fault predicted). (2)
Score NOT outcome-grounded — quality = turn TELEMETRY (tool-success
ratio/stop-reason/cache), not validated work outcomes; conflates
well-formed-turn w/ competent-work. (3) OBSERVER==OBSERVED — every agent
RECORDS ITS OWN turns (the telemetry that scores it), Scribe scores itself
(scribe/tool_loop.go:201) — universal self-scoring. (4) Dead branches:
cost-opt trigger dead (EstimatedCostPerToken never set), controller
UpdateAfterHandoff/UpdateWithoutHandoff zero non-test callers. (5)
Magic-number thresholds (violates Sylk's own derive-from-data rule).
Wall-clock in batch triggers (non-deterministic segmentation). THE
TRANSFERABLE DATUM (W3c): Sylk's co-residence LEAKED the narrator/narrated
boundary — parent both FEEDS and can STARVE its Scribe (lossy shared
channel) AND every agent SELF-SCORES on shared machinery; in-process made
it cheap to bolt a 2nd ingest path without removing the 1st. Sylk's
recommendation: "push the boundary to per-node/host-side; score service =
single authority reading ONE ordered stream, never self-reported."
ARCHITECT NUANCE (for the design): Sylk conflated PLACEMENT (co-resident)
with COMMS (fed) — the ROOT faults are COMMS/AUTHORITY faults
(feed+self-score), fixable INDEPENDENT of placement. Placement
(co-resident vs per-node vs pod) and comms (observe-not-feed) are
ORTHOGONAL; Sylk did co-resident AND fed AND self-scored. Hecate mandates
(from Sylk, regardless of placement): OBSERVE-not-feed; score = SINGLE
AUTHORITY reading the ordered stream; score = OUTCOME-grounded (validated
verdicts) not turn-shape; SEPARATE fast-detection (CUSUM per-instance)
from slow-reputation (per-(agent,domain) durable) — two signals two
lifetimes; ONE authoritative state object (learned copy == decision
copy); no decision axis w/o a wired input; derive constants; remove-Y-when-
X-replaces-it same change. So co-residence is NOT ruled out by Sylk IF
observe-not-feed + single-authority-outcome-score hold — pending the
isolation research (can a co-resident process be prevented from
feeding/starving its monitor). Reusable Sylk mechanism: hierarchical blend
(instance→agent-model→model→global priors) IF wired so learned==read.
Decoys noted: forest scoring.go (build-tagged, uncompiled, retrieval not
agents), guardian domain_reputation (web-URL, unrelated). Isolation agent
(a2bec1a9) resumed post-sleep; sidecar-placement (a7ffa4ec) still out.

**CO-LOCATION-ISOLATION DOSSIER LANDED (2026-08-19, a2bec1a9, resumed
post-sleep).** DECISIVE, primary-source. THE DIVIDING LINE = the
primary's KERNEL. Two bars held apart: Bar A (FAULTY/degrading primary,
userspace) vs Bar B (COMPROMISED, guest-kernel/ring-0 primary). Every
intra-guest mechanism (UID sep, PID/mount/IPC namespaces, seccomp,
capabilities, Landlock incl. IPC-scoping-to-domain, Yama
ptrace_scope=3, cgroup v2 memory.min "won't be reclaimed under any
conditions" + cpu.weight) is enforced BY THE SHARED GUEST KERNEL: FULLY
effective vs Bar A, COMPLETELY VOID vs Bar B (GKE Sandbox verbatim: "A
flaw in... the host kernel could allow a process running within a
container to 'escape' the container and affect the node's kernel").
Confidential computing does NOT move the line (SEV-SNP/TDX unit = the
whole GUEST vs the HOST; does NOT partition two processes in one guest —
tempting wrong answer CLOSED). DECISION MATRIX (5 placements): (1)
same-VM separate processes = ✅BarA ❌BarB, cheapest/lowest-latency —
"the naive assumption 'co-residence breaks isolation' is FALSE at Bar
A"; (2) same-VM primary-behind-gVisor/WASM = ✅BarA ⚠️until-Sentry-escape
(shifts trust anchor off shared kernel), syscall-bound cost; (3)
same-node SEPARATE microVMs + warden-brokered vsock = ✅BarA ✅BarB,
<5MiB+~125ms/VM, host-mediated AF_UNIX↔AF_VSOCK bypasses network stack
(direct precedent for warden brokering); (4) host-side warden-class =
✅BarA ✅BarB STRONGEST (the literal "warden+VM boundary still hold"),
cheapest per-agent, collects across the VM boundary; (5) remote pod =
✅✅ but network hop. VERDICT ON HECATE'S SENSOR PRECEDENT: it LICENSES a
co-resident Scribe at EXACTLY the sensor's trust tier and NO HIGHER — a
row-1 co-resident Scribe occupies the identical position (strong vs
faulty, defeated by a guest-kernel exploit, warden+VM boundary the
backstop), NO new trust assumption. A TAMPER-PROOF (warden-class) Scribe
CANNOT be co-RESIDENT (NO-PRECEDENT: a co-resident monitor tamper-proof
vs a kernel-compromised primary is an architectural IMPOSSIBILITY by the
kernel-line limit) — it must be co-LOCATED-in-its-own-VM+vsock (row 3) or
host-side (row 4). THIN (WebSearch exhausted): namespace/seccomp exact
overhead, gVisor exact %, vsock-vs-loopback latency delta (all
qualitative claims CONFIRMED). 
SYNTHESIS ACROSS ALL 4 DOSSIERS (converging): the SECURITY-CRITICAL
signal COLLECTION is ALREADY host-side (warden/sensor/health plane —
Bar B, tamper-proof, EXISTS) = the "ztunnel/per-node cheap always-on"
tier. The Scribe = the EXPENSIVE SEMANTIC INTERPRETATION (LLM narration
+ scoring signals) CONSUMING those already-tamper-proof-collected
signals = the "waypoint/per-identity expensive" tier — its placement is
FREED from the security-critical requirement (it's not the collector),
so it can be co-resident (row 1, sensor-tier) OR own-pod, chosen on
cost/latency. This IS the Ambient L4-per-node/L7-per-identity split.
Combined w/ Sylk (observe-not-feed + single-authority-outcome-score,
placement⊥comms) + telemetry (autonomous-local-first no-modes,
aggregate-at-source push-snapshots, single-writer convergence,
telemetry≠ledger). KEY USER RULING owed: the Scribe's threat model —
Bar A (perf-monitoring of faulty agents; co-resident row-1 suffices,
sensor-tier) vs Bar B (must survive adversarial/compromised agents
evading monitoring; needs row-3 own-VM+vsock or row-4 host-side). Note:
if the Scribe is observe-not-feed (inputs = host-side chokepoints the
primary doesn't control), co-residence risk reduces PURELY to a Bar-B
primary reading/tampering the Scribe's MEMORY — the security-critical
collection is already host-side regardless. Awaiting the 4th dossier
(sidecar-placement a7ffa4ec — Istio/Ambient/Solo receipts corroborating
the split) before presenting the full synthesized design + the threat-
model ruling.

**SIDECAR-PLACEMENT DOSSIER LANDED (2026-08-19, a7ffa4ec).** Numbers:
per-pod sidecar = 0.20 vCPU + 60 MB EACH (historical 0.35/40), +1.7ms
P90 two-proxy round trip, sized-to-worst-case→over-provisioned, LINEAR
in N (100 agents ≈ 6GB+20vCPU just for observers). Istio AMBIENT
correction = split by COST × CARDINALITY: cheap per-NODE ztunnel (0.06
vCPU/12 MB, no L7, "significantly leaner", single instance/node,
identity-scoped keys "requests for identities not running on the node
are rejected") + expensive per-IDENTITY waypoint ("shared between apps
in same namespace/SA", "only where needed", autoscalable pods). ~50×
memory gap for the always-on layer = "the entire reason the industry
moved". KEP-753 native sidecars = proof co-located-sidecar lifecycle/
restart pain was real enough K8s added an API. W5 tamper counterweight
(Buoyant): a sidecar "runs in the SAME SECURITY CONTEXT of the
application instance" — a FEATURE for a data-plane proxy, a LIABILITY
for a monitor that must not be tamperable; per-node shared proxy =
noisy-neighbor + blast-radius + shared-key attack vector (mitigated by
identity-scoping cross-node, not co-tenant). eBPF can't do L7/semantic
work. THIN (JS-blogs/Wayback-blocked/WebSearch-exhausted): Solo exact
latency #, ambient-vs-sidecar latency delta, Dapr/Cilium/OTel numbers.

**ALL FOUR DOSSIERS IN — DESIGN CONVERGED + PRESENTED (2026-08-19).**
The four agree on ONE architecture. KEY REALIZATION: Hecate ALREADY HAS
the cheap-always-on-security-critical collection tier, and it's ALREADY
Bar-B tamper-proof — it's the WARDEN (host-side) + SENSOR (in-guest) +
health plane. That IS the ztunnel-equivalent; not built anew. So the
"Scribe" is TWO+ jobs wearing one name, split by cost×cardinality×
trust: (1) COLLECTION = existing host-side warden/sensor/health plane
(Bar B, exists); (2) FAST DETECTION + score-signal compute = cheap,
always-on, DETERMINISTIC, in the COLOCATION UNIT single-writer (score
service + CUSUM), consuming the signal stream, NOT per-agent-pod, Bar B
host-side; (3) SEMANTIC NARRATION = the Scribe's EXPENSIVE LLM part,
per-identity ON-DEMAND/bursty (waypoint shape), a SEPARATE process
(observe-not-feed, never co-resident-fed), consuming host-side streams,
licensed at SENSOR TIER (Bar A) because the WARDEN is the Bar-B security
backstop (same logic that licenses the sensor) + the score service is
outcome-grounded (reads ledger) so spoofed Scribe signals have bounded
authority + a Bar-B agent is a Guardian/warden hard-block SECURITY event
not a perf-handoff concern. RESULT: the Scribe is NOT a per-agent
always-on sidecar microVM (rejected: sidecar tax linear-in-N +
lifecycle coupling + same-security-context tamper liability). THREAT-
MODEL RULING RESOLVED BY EVIDENCE (not left to user): Bar A / sensor-
tier for the narrator suffices because collection is already Bar-B
host-side. Score service = single-writer authority per session group in
colocation unit, outcome-grounded, push snapshots to RANK check (all 4
dossiers concur). Design presented in-thread for verdict.

**SCRIBE DECOMPOSITION REJECTED — AGENTIC COORDINATOR (user, 2026-08-19,
verbatim):** "the purpose of the scribe agent is to serve as an
intelligent, interactive narrator... Reducing the system in this way
violates the agentic nature of hecate. The Scribe serves as a
*coordinator* of these systems, not 'three in a trenchcoat'. It's
agentically enabled observability." ARCHITECT ERROR: mapped dumb-proxy
sidecar research (Ambient ztunnel/waypoint = L4/L7 BYTE proxies) onto an
INTELLIGENT AGENT, dissolving it into a mechanical pipeline — the exact
anti-agentic reduction Hecate forbids. CORRECTION: the Scribe is a
FIRST-CLASS AGENT (intelligent interactive narrator + COORDINATOR of the
observability systems). The mechanical systems (collection, detection,
scoring) EXIST as SUBSTRATE the Scribe agent coordinates — NOT what the
Scribe IS. GROUNDING = Hecate's canonical mechanism+judgment pattern:
warden (deterministic host-side mechanism) : Guardian (agentic judgment)
:: {host-side collection + deterministic CUSUM detection + outcome-
grounded score service} : SCRIBE (agentic coordinator). The 4-dossier
research STANDS but applies to the SUBSTRATE (cheap host-side collection
Bar-B; deterministic detection/score in colocation unit single-writer;
telemetry aggregate-at-source/sample laws; observe-not-feed; signal-
source≠score-authority; outcome-grounded). The SCRIBE sits atop as the
agent: intelligent narration, interactive history-serving (peers consult
it, it reasons what to surface), coordinates collection (consumes
host-side signals, observe-not-feed), reads the deterministic detection/
score signals and applies AGENTIC JUDGMENT (requests performance handoff
with evidence+context; Guardian approves — CONTEXT.md model preserved),
is the score service's signal SOURCE but NOT the score authority (Sylk
separation). PLACEMENT: the Scribe is its OWN agent/microVM (one-agent-
per-microVM, first-class, ISOLATED — not co-resident, not dissolved).
EFFICIENCY = substrate does the cheap always-on mechanical work + the
Scribe applies intelligence AGENTICALLY/on-demand (scale-to-zero when
primary quiet, AUTOSCALING), NOT from making it stateless/pooled.
Memory: feedback_dont_dissolve_agents_into_substrate. Re-presented
in-thread with the corrected agentic frame.

**SCRIBE = CO-LOCATED PROCESS, MECHANICS RESEARCH (user, 2026-08-19).**
User: prose w/ "zero practical application"; "scale to zero" is
INCOHERENT (a monitor attached to a RUNNING agent can't scale to zero).
VOCABULARY RULE: NOT a "sidecar" (mesh baggage) — a **CO-LOCATED
PROCESS**. Confirmed direction: the Scribe is a first-class agent
running as a co-located, mutually-isolated PROCESS inside the primary's
microVM (Kata Containers = the production precedent: a whole K8s pod =
multiple isolated processes in ONE microVM via kata-agent guest init +
per-process namespaces/cgroups). BIDIRECTIONAL non-tampering is
co-equal: primary-must-not-tamper-Scribe is AS important as
Scribe-must-not-tamper-primary — PEER isolation, not a privileged
watcher. SCALE-TO-ZERO RETRACTED → honest model: the Scribe process is
RESIDENT (blocked on its host-side input stream, ~0 CPU idle, cost = its
RSS); MODEL INFERENCE is on-demand/bursty (narrate/judge on events), not
per-turn. CONCRETE-MECHANICS RESEARCH dispatched (ad03bcc9, expanded):
W1 libkrun actual process/guest model (does the fork support a
multi-process guest w/ init/supervisor, or is that fork work?); W2 Kata
multi-container-in-one-VM precedent (kata-agent spawn + per-container
ns/cgroup isolation, ttRPC/vsock); W3 guest-init supervisor pattern; W4
CONCRETE isolation flags (clone/unshare NEWNS/NEWPID/NEWIPC/NEWUSER,
cgroup v2 memory.min/cpu.weight + delegation, separate UID + yama
ptrace_scope, seccomp/Landlock — actual flags/paths); W5 native-sidecar
spawn ordering (KEP-753); W6 resident-idle footprint (kills
scale-to-zero); W8 MUTUAL/symmetric isolation (both processes protected
from each other; each own cgroup floor the other can't rewrite unless
guest-root); W9 process lifecycle + failure/RESTART within the microVM
(guest-init PID1 reaping/restart; Scribe crash→restart w/ primary
running; primary crash→Scribe observes+reports+torn down; ordering);
W10 lifecycle COUPLING (how the Scribe polls/watches the primary's
liveness from within the guest — pidfd_open(2) race-free death
notification, /proc, cgroup.events — NOT a primary-controlled channel);
W11 TRIPWIRES (seccomp RET_TRAP/audit, Landlock denials, cgroup OOM =
attempted-boundary-violation is itself a detectable event surfaced to
the host warden). Mechanics-grounded design presents when it lands. NO
more architecture prose w/o the concrete spawn/isolation/lifecycle
mechanics + examples.

**CO-LOCATED COMPANION LOOP — ACCEPTED w/ EXCEPTIONAL-DOCUMENTATION
MANDATE (user, 2026-08-19): "I accept that tradeoff as a part of
colocation, however we need to make sure it is exceptionally well
documented."** DECISION LOCKED: the Scribe is a co-located COMPANION
AGENT LOOP = an ownership subtree in the primary's SINGLE hecate-rt
runtime (NOT two runtimes, NOT two OS processes), sharing the N-shard
thread pool; the Scribe subtree is light (observer + on-demand
inference, mostly parked). ISOLATION = the runtime's OWN discipline
(RUNTIME §1 single-owner arenas + Rust ownership = no cross-subtree
memory; §4 per-subtree budget = no starvation; §4b no-panic = a fault
is a typed error not a crash; cancellation = hung task bounded) →
Bar-A (faulty-agent) MUTUAL/symmetric isolation. TRADEOFF ACCEPTED:
loses userspace-CODE-EXEC isolation of the Scribe (a code-exec-
compromised primary owns the shared process incl. the Scribe subtree);
BACKSTOP = the host-side WARDEN (Bar B, boundary-crossing observation,
tamper-proof) + Guardian hard-block (a code-exec compromise is a
SECURITY event, not a perf-narration concern) + the Scribe is ADVISORY
(score service is outcome-grounded host-side, bounded authority). COMMS
= each subtree its own vsock flow identity (PODS §3); Scribe observes
host-side streams over ITS vsock (observe-not-feed); NO intra-runtime
primary→Scribe channel. EXCEPTIONAL-DOCUMENTATION BAR (what the spec
MUST contain, first-class not footnote): (1) explicit THREAT MODEL
section — Bar A defended (faulty/degrading: memory/starvation/fault/
ptrace all held by runtime discipline) vs code-exec-compromise NOT
defended in-runtime + exactly what catches it (warden Bar-B + Guardian
hard-block); (2) isolation-mechanism × vector table (memory→Rust
ownership; starvation→per-subtree budget; fault→no-panic; signal/ptrace
→ n/a same process, so the code-exec limit) w/ the tier each holds/
breaks at; (3) the "what breaks & what catches it" chain, spelled out;
(4) the ALTERNATIVE CONSIDERED (two OS processes = adds code-exec
isolation at ~2× runtime cost / N+1 threads w/ right-sized Scribe) + WHY
the shared-runtime tradeoff was chosen (efficiency + warden backstop +
advisory role); (5) the derivation/reasoning chain so a future reader
sees the DELIBERATE choice; (6) tests asserting Bar-A mutual isolation
holds (neither subtree touches/starves/crashes the other) AND a
code-exec test showing the warden catches the tradeoff boundary.
COROLLARY AMENDMENTS: RUNTIME.md + PODS.md gain the co-located-companion
-loop concept (PODS §3 init spawns the runtime hosting BOTH loops);
AGENTS_RUNTIME.md "Scribe feed after every turn" (§1/§5/crit) REMOVED
(the Sylk push anti-pattern) → observe-not-feed. Mechanics research
(ad03bcc9) still in flight — its lifecycle/restart/tripwire/failure
findings now reframe to the RUNTIME level (ownership-tree teardown, task
supervision, budget tripwires) + ground the documentation + provide the
OS-process alternative for completeness. Spec written (w/ exceptional
tradeoff documentation) after the research lands + the score-service/
Scribe-comms design is finalized.

**CO-RESIDENT MECHANICS DOSSIER LANDED (2026-08-19, ad03bcc9).** Primary
-source, concrete flags/syscalls/API. KEY: libkrun boots its OWN init
(PID1, built-in) that runs EXACTLY ONE workload + reboots the VM on that
workload's exit (verbatim exec.rs fork→waitpid(main)→set_exit_code→
reboot(RB_AUTOBOOT); the `_=>continue` arm reaps arbitrary children).
Two co-located WORKLOADS = NO-PRECEDENT in libkrun = fork work. Natively
PROVIDED: guest PID1 reaping, host→guest vsock (krun_add_vsock_port, ONE
device/multi-port) + virtio-console multiport (/dev/vportNpM),
per-workload uid (krun_setuid), shutdown eventfd. Kata = the production
precedent for N-isolated-processes-in-one-microVM (one VM=one sandbox=
whole pod; kata-agent=the in-guest supervisor; per-container ns+cgroups
created INSIDE the guest; PR_SET_CHILD_SUBREAPER + waitpid(-1,WNOHANG|
__WALL)). Concrete isolation (W4/W8): unshare(CLONE_NEWNS|NEWIPC|NEWUSER
|NEWPID); cgroup v2 delegation + memory.min (hard, "won't be reclaimed
under any conditions") + cpu.weight; distinct non-root UIDs + Yama
ptrace_scope=2/3; PR_SET_NO_NEW_PRIVS→seccomp + Landlock (self-restrict,
un-removable). HONEST LIMIT: cgroup protects siblings from each other but
GUEST-ROOT owns the hierarchy → design = supervisor=guest-root owns the
tree, BOTH peers = distinct non-root UIDs in delegated sub-cgroups.
Liveness (W10): pidfd_open(2) race-free (EPOLLIN=zombie/EPOLLHUP=reaped),
supervisor opens pidfd on primary + hands read-only fd to observer
(never needs primary's cooperation); cgroup.events populated;
PR_SET_PDEATHSIG. Tripwires (W11): seccomp RET_TRAP(SIGSYS)/RET_LOG
(auditd)/RET_USER_NOTIF(live→warden) on ptrace/cross-boundary; Landlock
EACCES; memory.events/oom_kill — every attempted violation is an
OBSERVABLE event surfaced to the warden. Footprint (W6): resident-idle =
blocked in epoll_wait (state S) ≈ 0 CPU + RSS; inference = separate
bursty spike (kills scale-to-zero). Restart-on-exit INSIDE one guest =
NO-PRECEDENT (K8s restarts above the VM) = fork work. THIN: <5MiB
overhead #, small-model inference RSS, "KEP-753" label.

**RECONCILIATION w/ the ACCEPTED shared-runtime decision:** the research
is about TWO OS PROCESSES; the user accepted TWO OWNERSHIP SUBTREES in
ONE hecate-rt. These map cleanly: (1) the SHARED-RUNTIME model FITS
libkrun's one-workload model NATIVELY — the ONE workload libkrun execs
IS the hecate-rt runtime, which hosts both loops as subtrees + is itself
the supervisor of its subtrees & tool-child-processes; NO separate guest
supervisor fork work needed (whereas the two-process alternative WOULD
need the Kata-style supervisor). So shared-runtime is BOTH more efficient
AND simpler-to-build — research REINFORCES the choice. (2) The
mechanics dossier GROUNDS THE ALTERNATIVE-CONSIDERED for the exceptional
documentation (two OS processes: exact ns/cgroup/uid/seccomp/Landlock/
pidfd/tripwire flags + Kata precedent) — precisely the "alternative
considered + why not chosen" the doc bar requires. (3) REAL CONSTRAINT
surfaced for the shared-runtime model: TOOL/CODE EXECUTIONS must run as
OS-ISOLATED CHILD PROCESSES (the W4 flags: distinct uid/cgroup/seccomp/
Landlock), NOT inside the hecate-rt process — else arbitrary
agent-generated code (a coding agent runs code!) could reach the shared
runtime's memory incl. the Scribe subtree, breaking Bar-A. This is the
concrete requirement that makes the shared-runtime Bar-A isolation
actually hold; likely implied by VFS §6 (tools execute in-guest) + the
warden, but the tool-child-process ISOLATION must be stated explicitly.
(4) Comms/liveness/tripwire primitives (vsock/virtio-console for
observe-not-feed host-side input; pidfd for the Scribe watching the
primary's liveness; seccomp-RET_USER_NOTIF→warden tripwires) apply to
the shared-runtime model too (the Scribe subtree's host-input vsock; the
tool-child pidfd/tripwires). ALL RESEARCH IN (Sylk+telemetry+isolation+
sidecar+mechanics). Design fully grounded; ready to write (companion
loop + score service + agent↔Scribe + exceptional tradeoff doc + the
tool-child-isolation constraint) on the user's go.

**STRONGER ASYNC-TASK ISOLATION — "GREEN PROCESS" FRONTIER (user,
2026-08-19): "is there a way we can better isolate those async tasks? At
a system level — run like async tasks, but have some of the isolation of
OS processes, tracing, monitorability."** The canonical model = green
process / strongly-isolated actor: schedules like an async task, isolated/
monitorable like a process. FOUR AXES: (1) memory isolation stronger than
language ownership (survives bugs/native code); (2) preemption + resource
metering (a runaway task can't monopolize; per-task CPU/mem caps); (3)
fault isolation; (4) per-task tracing/monitorability (process_info-grade).
hecate-rt ALREADY has the actor skeleton: single-owner arenas ≈ isolated
heaps; per-task budget ≈ reductions; no-panic ≈ fault isolation; the
question = how far to push it to process-grade. RESEARCH DISPATCHED
(a9105719): W1 BEAM/Erlang (isolated per-process heaps + per-process GC;
PREEMPTIVE reduction-counting scheduling ~2000 reductions; let-it-crash
fault isolation; process_info/observer/trace per-process introspection;
µs creation, millions/node) = the 40-yr proof of all four axes end-to-
end; W2 WASM/Wasmtime instances (linear-memory isolation surviving
arbitrary compiled code; FUEL deterministic metering; EPOCH interruption
= forcible preemption; ResourceLimiter/StoreLimits per-instance caps;
async_support so it SCHEDULES as an async task; WASI capability
deny-by-default) = the modern in-process mechanism giving process-grade
memory+preemption+capability+resource isolation while scheduling async;
W3 Intel MPK/pkeys hardware intra-process memory isolation (pkey_mprotect/
WRPKRU, per-thread page-group access w/o syscall; ERIM <1%-overhead,
Hodor) = near-zero-cost hardware memory isolation between tasks (+ honest
PKRU-attack limits); W4 SFI + RLBox (type-driven in-process sandbox
boundary, Rust-adjacent) = software-only alternative; W5 tokio-console/
console-subscriber (per-task poll/busy/idle/scheduled/waker/state =
"top for async tasks") + tracing spans = the monitorability axis; W6
runtime preemption beyond cooperative yield (Tokio auto-coop budget; Go
signal-based async preemption at safepoints) = bounding a non-yielding
task. W7 synthesis = decision matrix (6 mechanisms × 4 axes + overhead +
composes-with-actor-runtime), mapping each onto hecate-rt's existing
model + what each ADDS. Grounds whether the two agent loops get WASM-
instance / MPK / reduction-style-preemption / console-grade-tracing
upgrades over today's ownership+budget+no-panic. Presents decision matrix
on landing.

**GREEN-PROCESS FRONTIER — TWO AXIS SHARPENINGS (user, 2026-08-19):**
(1) "no-panic as fault isolation is STILL weak — processes do unexpected
things." CORRECT: no-panic/catch_unwind covers only the EXPECTED fault
path (recoverable panics, panic=unwind). PROCESS-FATAL faults it does
NOT contain in a shared process: abort (panic=abort/double-panic/
alloc-fail-abort), stack overflow→SIGSEGV, OOM, hang/livelock/deadlock
(only PREEMPTION contains — ties to axis 2), FFI/unsafe UB/native crash.
Real fault isolation of the UNEXPECTED needs a SANDBOX (WASM: OOB/
stack-overflow/unreachable→traps caught by host, contained to the
instance; fuel/epoch bound infinite loops; StoreLimits bound growth —
host-call residual) or an OS PROCESS (contains all, at process cost).
MPK contains NONE of the fault-fatal (memory access control ≠ fault
containment). Even BEAM's honest hole: a bad native NIF crashes the VM →
native/arbitrary code MUST be at arm's length (child process — Hecate's
tools-as-child-processes). Addendum sent: fault TAXONOMY (a-f) ×
mechanism containment table. (2) "purely relying on tokio for
monitorability is weak — how do we determine what the process is doing?
Resource usage?" CORRECT: tokio-console = SCHEDULER-level only (poll/
busy/idle/waker/state), NOT actual compute/memory/syscalls/semantics.
Process-grade needs FOUR LAYERS: L1 EXACT per-task accounting (WASM fuel
= instructions executed + linear-mem size = exact bytes + host-calls =
every I/O at the boundary; or BEAM process_info reductions+heap+
current_function+msg_queue_len+status; hecate-rt today = only arena-byte
budget); L2 SEMANTIC (tracing spans = what operation); L3 KERNEL/
MECHANICAL (eBPF — syscalls, on-CPU + OFF-CPU "what's it blocked on",
page faults, I/O — the deep view tokio can't give); L4 RESOURCE ENVELOPE
(cgroup cpu.stat/memory.current/io.stat). Addendum sent: four-layer
monitorability × mechanism table. THE THROUGH-LINE emerging (to be
priced, not asserted): WASM instances score high on ALL THREE axes
SIMULTANEOUSLY — memory isolation (surviving arbitrary code → could
CLOSE the §3 code-exec tradeoff), fault containment (traps + fuel +
limits, host-call residual), AND monitorability (fuel/linear-mem = exact
resource accounting, host-calls = observable I/O). The decision matrix
must weigh this against the WASM boundary cost (model/tool calls become
host calls; whether the agent loop itself should be a WASM instance vs
tools-only). Research (a9105719) covers all + both addenda.

**GREEN-PROCESS FRONTIER — LATENCY/SCALE-COST SHARPENING (user,
2026-08-19): "hesitant to just jump to WASM — laptop might support it,
Meta scale the latency will KILL."** CORRECT instinct, sharpened: WASM's
per-call boundary cost kills FINE-GRAINED workloads but is NEGLIGIBLE for
the COARSE await-heavy agent loop (model ~100s-ms, tool child ~seconds,
vs µs boundary). The REAL Meta-scale WASM tax is INSTANTIATION/compile +
LINEAR-MEM DENSITY across N instances (mitigable by pooling-allocator/
pre-instantiation/AOT — to be quantified). KEY: WASM is NOT the only path
— cheaper non-WASM mechanisms hit most axes at NEAR-ZERO per-call cost:
MPK/pkeys (WRPKRU ~tens-of-cycles, no syscall/boundary, ERIM <1% — memory
isolation surviving... actually only access-control not code-exec, but
near-free); runtime preemption (reduction-count/signal — bound a hung
task ~free); supervision + POD-DEATH RECONSTRUCTION (process-fatal faults
uncatchable in-process contained at the POD level — pod dies, warden
detects, successor reconstructs from durable claims, AGENTS_RUNTIME R3);
eBPF + runtime accounting (deep monitorability, kernel-side, zero app
boundary). Addendum sent: matrix gains {per-call/hot-path, instantiation,
memory-density@N} cost columns × the isolation/fault/monitorability axes.
THE HONEST SPECTRUM the matrix must lay bare: cheap-strong-on-3-axes
(MPK + runtime-preemption + eBPF + supervision — but NO arbitrary-code
fault containment) → WASM (ADDS arbitrary-code containment at an
instantiation/density tax, per-call-negligible-for-coarse-loops). Choose
per the both-scales-no-modes law. Research (a9105719) now covers
mechanisms × axes × cost = the full priced decision matrix. Presents on
landing; NO jumping to WASM.

**GREEN-PROCESS ISOLATION DOSSIER LANDED (2026-08-19, a9105719).**
Full priced matrix, primary-source. hecate-rt today = "BEAM MINUS THE
RUNTIME": single-owner arenas ≈ isolated heaps, per-task budget ≈
reductions, no-panic ≈ EXPECTED-fault-only. FOUR GAPS (receipted): (i)
memory isolation COMPILE-TIME ONLY, fails under native/unsafe (FFI=UB);
(ii) no-panic NECESSARY-NOT-SUFFICIENT — catch_unwind catches only
unwind-panic; abort/double-panic/stack-overflow→SIGSEGV/OOM-abort/FFI-UB
all PROCESS-FATAL (kill BOTH loops); (iii) cooperative budget CAN'T
preempt a non-yielding loop{}; (iv) monitorability L2-only. MECHANISMS:
BEAM = the end-to-end proof (isolated heaps + reduction preempt CONTEXT_REDS=4000
+ process_info + supervised restart; 233 words/proc, 2^20/node; but NIF
crash kills whole VM → native at arm's length). WASM/Wasmtime = strongest
IN-PROCESS container surviving arbitrary compiled code: fuel (1 unit/instr
= EXACT compute meter, get_fuel) + epoch interruption (forcible preempt,
~10% cost, non-deterministic wall-clock) + StoreLimits + traps
(stack-overflow/OOB/div0/unreachable→trap CAUGHT BY HOST, host survives,
2 sequential traps same Store) + WASI capabilities; call_async IS a Future
(schedules as async task). Cost NOT per-call (negligible for coarse
await-heavy loops; ~thin trampoline, compute 45-55% browser/1.2-1.8×
bounds-check) — real tax = instantiation + linear-mem density, AMORTIZED:
pooling 2ms→5µs (400×), CoW → RSS ≈ dirtied pages (few KB), 4GiB guard =
VIRTUAL address space not RAM. Residual: HOST-FUNCTION bug = native = fatal;
host-side OOM untracked. MPK/pkeys = hardware memory isolation ~11-260/26/
23.3 cycles, <1% (ERIM), 90-98% native (Hodor) — but DATA-ACCESS ONLY,
contains NO fault class (segfault still kills), NOT SECURE ALONE (PKU
Pitfalls: 10/10 exploits bypass; hardening → 40% throughput loss).
SFI/RLBox = type-safe tainted<T> compile-error boundary, 4%/0.22µs
crossing/1.6MB/sandbox, backend swappable (Wasm/SFI/proc). OS process/
microVM = contains ALL faults, 125ms/5MiB. FAULT TAXONOMY (a panic/b abort/
c stack-overflow/d OOM/e hang/f FFI-UB): catch_unwind=a-unwind-only; WASM=
a-e ✅ (f: guest✅/host-fn-fatal); MPK=none; BEAM=a-e ✅ (f fatal); OS=all.
4-LAYER MONITORABILITY: L1 exact (WASM fuel+data_size / BEAM process_info)
+ L2 semantic (tracing/tokio-console = scheduler-level poll/busy/idle/state,
NOT cycles/bytes) + L3 eBPF (on/OFF-CPU why-blocked, syscalls; per pinned
shard-thread 1:1) + L4 cgroup (usage_usec/memory.current/peak exact).
THE HONEST SPECTRUM: [cheap stack] MPK + runtime-preemption + eBPF/cgroup/
tokio-console + supervision+pod-reconstruction = memory-iso + preempt +
process-grade-monitor at ~0 per-call/instantiation/density — but NO
arbitrary-code fault containment (segfault/abort/FFI kills both loops →
pod dies → reconstruct). → [WASM] ADDS arbitrary-code memory-safety +
trap fault-containment + epoch forcible-preempt + exact fuel-metering,
schedules-as-async, at amortizable instantiation+density. → [OS process]
full containment, coarse/per-invocation only (tool children). THIN: WASM
host-call ns#, Cranelift compile-time#, BEAM µs-creation#. Priced matrix
presented in-thread for the isolation decision.

**WASM COST NUMBERS UNDER-SOURCED — USER CAUGHT IT (2026-08-19): "Where
do those numbers even come from? Did you back them with actual research
into WASM overhead? The case where Prisma spent years ripping out WASM
due to performance costs?"** ARCHITECT OWNS IT: the WASM cost figures
were WEAKLY sourced — 45-55% = Jangda "Not So Fast" (BROWSER engines
V8/SpiderMonkey, NOT Wasmtime; the dossier itself flagged Wasmtime-native
= NO-PRECEDENT); "1-10% heavy math" = echoed from the USER's own prior
message; the DATA-TRANSFER cost (the dominant term) = MY qualitative
reasoning w/ ZERO production evidence. Presented firmer than warranted.
PRISMA is the decisive production evidence I lacked: built the query
engine in Rust, shipped native-binary + WASM, spent YEARS fighting the
JS↔engine SERIALIZATION/data-transfer boundary cost + bundle-size +
cold-start, now REMOVING the Rust/WASM engine for a native TypeScript
query compiler FOR PERFORMANCE. A production WASM-rip-out > academic
microbenchmarks, and it points exactly at the data-marshalling boundary
cost I hand-waved (the Prisma problem = boundary cost dominates
data-moving workloads). REAL RESEARCH DISPATCHED (a0a499ff): W1 Prisma
full story (why remove Rust/WASM; the specific costs — serialization/
bundle/cold-start/memory; the native-engine before/after numbers); W2
other production WASM overhead/removal reports + honest counter-cases
(Figma win, Shopify Functions limits, edge cold-start); W3 the
data-marshalling/boundary-transfer cost RIGOROUSLY (lifting/lowering,
copy-into-linear-memory, host-call ns, why compute-bound-cheap vs
data-moving-expensive); W4 rigorous Wasmtime-SPECIFIC overhead (Sightglass,
bounds-check, AOT-vs-JIT — confirm/refute the NO-PRECEDENT); W5 synthesis
for the AGENT-LOOP workload (coordination + data-moving: is WASM a
Prisma-class trap? can the data plane stay host-side w/ WASM holding only
handles, or does data still get lifted/lowered?). Brutally-honest verdict
owed. Prior isolation matrix STANDS on the isolation/fault/monitorability
axes + the cross-platform finding (MPK disqualified = x86-only mode; WASM
uniform cross-platform; eBPF/cgroups in-guest-Linux uniform) — only the
WASM COST leg is being re-grounded. Decision on gap-(ii)/§3 HELD until
the real WASM-cost evidence lands.

**WASM OVERHEAD — PRODUCTION EVIDENCE LANDED (2026-08-19, a0a499ff).**
THE RULE: WASM taxes BYTES CROSSING THE BOUNDARY, not instructions inside
it. PRISMA (verbatim, raw HTML): removing Rust/WASM query engine because
"the cost of serializing data between Rust and TypeScript is very high
[and] negates any benefit gained"; penalty SCALES WITH DATA — findMany
25k records 185ms→55ms (3.4×), large m2m 1539ms→136ms (11×), "minimal"
on small queries; bundle 14MB→1.6MB→148KB; WASM prod failures (#28012
Cloudflare "Invalid array buffer length", #16805 "Out of memory: wasm
memory" 32 comments). CRUCIAL: Prisma's NEW arch IS the mitigation —
WASM compiler emits SQL (tiny/compute), JS driver executes+receives bulk
rows (data never re-crosses WASM). ZAPLIB (rewrote-in-WASM-then-
abandoned): compute win only "5% faster"/"2× some of the time, not 10×"
— WASM compute speedup is SMALL + RARE (so isolation, not speed, is the
only reason to WASM a coordination loop). FIGMA 3× (but COMPUTE-bound
rendering). SHOPIFY Functions hard caps (128kB in/20kB out = platform
bounding boundary transfer). Wasmtime bounds-check 1.2-1.8× is ELIDED by
default on 64-bit (4GiB guard + page-fault traps) — NOT a Hecate cost.
NO clean Wasmtime-vs-native % exists (Sightglass explicitly refuses the
comparison) — NO-PRECEDENT CONFIRMED. Per-call host-call ns = THIN (not
published; direct call not syscall, small; data-copy is the term that
matters). Cold-start/bundle = Prisma's EDGE pain, does NOT transfer —
Hecate = long-lived POOLED instances (Wasmtime pooling allocator + CoW +
AOT + InstancePre = 5µs instantiation; Lucet <50µs). MITIGATION clean +
expressible: component-model `resource` = host-owned handle, guest holds
opaque i32, bulk data never enters linear memory (= Prisma's new arch).
Residual honest: whenever the guest must READ bytes to decide, THAT slice
copies in → design loop to read MINIMUM (decisions on metadata/handles,
not full payloads); same-language Rust↔Rust avoids Prisma's JS
(de)serialization. VERDICT: agent loop NOT a Prisma trap CONDITIONALLY —
ONLY if bulk data plane (context/token-stream/tool-I/O) stays HOST-SIDE
behind handles; if data crosses, it IS the Prisma wall. ARCHITECT READ:
compute win nil (Zaplib) → isolation is the ONLY WASM benefit; data cost
real+controllable-but-a-design-constraint for a content-reasoning loop;
cheap-stack (ownership+preemption+in-guest-eBPF/cgroups+pod-reconstruction,
FREE + cross-platform + Bar-A + pod-level recovery) is the better DEFAULT.
RECOMMENDATION: accept §3 Bar-A + cheap-stack; do NOT WASM the loops (nil
compute win + real data cost + design constraint don't beat
pod-reconstruction); reserve WASM (if anywhere) for BOUNDED-COMPUTE tool
execution (a separate decision, Shopify-Functions-shaped). gap-(ii)/§3
decision now RE-OPENED for the user with the real evidence.

**WASM CLOSURE + COMPANION-LOOP DESIGN CONFIRMED & ACCEPTED (user,
2026-08-19): the Scribe-observes-→-bytes-cross-boundary point settled it
("confirmed and accepted").** LOCKED: agent loops (primary + Scribe) are
NATIVE RUST co-located ownership subtrees, NOT WASM (data-centric
workload = the Prisma trap continuously; Scribe = purest case, all it
does is read observations, no handle-mitigation possible for an observer).
Baseline isolation = cheap cross-platform stack: Rust ownership (Bar-A) +
runtime-counting preemption + in-guest eBPF/cgroups + supervision/
pod-death-reconstruction. §3 code-exec tradeoff = accepted-as-documented
(warden Bar-B backstop). Tools = isolated child processes (OS iso, no
boundary tax — coding tools are data-heavy too). WASM's role in Hecate ≈
none (correct for the workload). MPK also out (x86-only = a mode). The
multi-exchange green-process/isolation/WASM arc RESOLVES to: native Rust
+ cheap stack, no WASM. Feeds MONITORING.md (companion loop + substrate +
score) + the RUNTIME/PODS/AGENTS_RUNTIME amendments.

**RETURN TO HANDOFF WORK (Branch 14 / D-5, 2026-08-19).** The HANDOFF
spec was PRESENTED earlier (five tiers: gathering/weighing/storage/
trigger-CUSUM/execution + Guardian-SPRT+fresh-context-probe +
commissioning + HO1-16 Sylk-lesson tests) but BLOCKED on §3 (detector
state placement — "where does it live"). The detour RESOLVED §3 and
produced the MONITORING plane. RECONCILIATION (what the detour settled
for HANDOFF): §3 detector CUSUM state = colocation-unit DETECTION
SUBSTRATE (deterministic, single-writer, checkpointed, re-derivable —
NOT pod/Scribe RAM; kills the Sylk split-brain + PODS-§7 discard
problem); §1 collectors = the MONITORING host-side collection substrate
(warden/sensor/ledger/gateway), consumed observe-not-feed; the Scribe =
co-located companion loop = the AGENTIC handoff INITIATOR (reads the
deterministic detection signal + applies judgment to REQUEST a
performance handoff → Guardian adjudicates §5); the SCORE service (slow
reputation, Rank) = SEPARATE colocation-unit substrate from the FAST
CUSUM detector (two signals, two lifetimes — Sylk fault #9). Detection
math (risk-adjusted CUSUM/Steiner, h=ln(ARL0), ARL0=T/δ, K-of-N),
adjudication (SPRT+fresh-context-probe), execution (brief/claims/drain/
re-bind under bumped epoch), commissioning (FIR/fleet-priors) = STAND as
presented. NEXT: finalize HANDOFF w/ corrected §3 + MONITORING
reconciliation; write MONITORING.md + HANDOFF.md as two specs (MONITORING
= the plane/machinery; HANDOFF = detection-math + execution consumer).

**HANDOFF DETECTION — DISCRIMINATOR-INFORMS-AGENT (user, 2026-08-19):
"we need *some sort of non-agentic discriminator like CUSUM that can help
inform the scribe*."** Architect OVER-CORRECTED (swung CUSUM-decides →
no-CUSUM); user set the balance point. RESOLUTION = the warden:Guardian
pattern applied to degradation: a DETERMINISTIC CUSUM-class DISCRIMINATOR
INFORMS the Scribe's agentic judgment; the Scribe DECIDES. Dissolves the
architect's objection: "CUSUM needs a meaningful per-turn quality metric"
was an objection to CUSUM-AS-DECISION; as an INFORMING discriminator it
accumulates EVIDENCE over observable signals (state-action recurrence /
outcome-grade deltas / behavioral), risk-adjusted, graded + trajectory —
the SCRIBE supplies the MEANING (real degradation vs hard task vs
legitimate retry). WHY it earns its place: binary tripwire = too crude
(no gradation/trajectory/risk-adj); per-turn agentic judgment = too
expensive (model call every turn). The discriminator = cheap +
deterministic + always-on + graded + REPLAYABLE (testable, unlike a
per-turn model judgment) middle that hands the Scribe rich input so it
spends intelligence only when warranted. BONUS: because it only INFORMS
two agentic filters (Scribe judgment → Guardian fresh-context probe) it
can be tuned SENSITIVE (flag early/generously; false spikes filtered by
Scribe+Guardian) — catches MORE real degradation than a conservative
auto-trigger. CORRECTED HANDOFF: §4 = the DISCRIMINATOR (colocation-unit
substrate, risk-adjusted CUSUM or K-of-N over per-channel CUSUMs for
dead/noisy-channel robustness, graded+trajectory, δ-budget = ATTENTION
HINT not auto-fire, deterministic/single-writer/checkpointed); §5 = the
Scribe's AGENTIC JUDGMENT consuming the discriminator + observation +
context → requests handoff w/ reasoning + discriminator evidence; then
Guardian adjudicates (fresh-context probe). Score (Rank) = separate slow
agentic-verdict aggregate (RANK §4), unchanged. Context handoff =
deterministic threshold, unchanged. The full CUSUM/risk-adj/K-of-N/
derived-threshold research is EXACTLY RIGHT for the discriminator ROLE.
Fold into HANDOFF.md; write MONITORING.md + HANDOFF.md.

**HANDOFF — IT'S ALSO A METRICS PROBLEM (user, 2026-08-19): "So it is
*also* a metrics problem, and we need to examine that."** CORRECT + the
load-bearing piece: the discriminator is only as good as its inputs, and
SYLK'S REAL FAILURE WAS METRICS not math (2/3 channels zero-producer,
surviving signal 97% constant-1.0, "quality"=tool-success-ratio =
conflates WELL-FORMED turn w/ COMPETENT work). A perfect CUSUM over
garbage metrics discriminates noise. HARD CONSTRAINT: the discriminator
is NON-AGENTIC → metrics must be (a) observable DETERMINISTICALLY from
Hecate's substrate (ledger deltas / warden verdicts / sensor / gateway;
NO model call, NO logprobs-Anthropic-API-doesn't-expose), (b) actually
CORRELATED with degradation (not crude proxies), (c) robust vs Sylk
modes (dead producers, constant channels, well-formed-vs-competent
conflation). METRICS RESEARCH DISPATCHED (a9a3ea7b): W1 LLM-agent
failure taxonomies + observable signatures (MAST freqs, OpenHands/
SWE-agent failure modes); W2 state-action recurrence/looping (best-
evidenced, exact measurement method + correlation#); W3 outcome signals
(validation-failure streak, self-correction/revert/corrective-churn,
lagging-vs-leading); W4 behavioral (tool-error/malformed/retry-storm/
stop-reason — WHY tool-success-ratio fails, what non-conflating looks
like); W5 progress/goal-drift (IS progress non-agentically measurable at
all, or does it require judgment→Scribe?); W6 metric-design principles
as REQUIREMENTS (observability/variance/non-conflation/risk-adjustment/
robustness, each tied to a Sylk failure); W7 synthesis = candidate
metric set for the discriminator (each: measures-what / evidence+# /
non-agentic-extraction-from-Hecate-observables / leading-vs-lagging /
avoids-Sylk-trap), + the honest line between non-agentically-measurable
(→discriminator) vs judgment-requiring (→Scribe). This settles the
discriminator's INPUTS. HANDOFF §1 (gathering) + §4 (discriminator)
finalize on this landing; MONITORING.md + HANDOFF.md write after.

**HANDOFF METRICS DOSSIER LANDED (2026-08-19, a9a3ea7b).** Backbone =
MAST ("Why Do Multi-Agent LLM Systems Fail?", Cemri 2025, 150 traces,
κ=0.88, 14 failure modes). THE PROOF the user was right (Sylk = metrics
failure): MAST Appendix J shows the metric class Sylk chose (tool/
verification WELL-FORMEDNESS) appears JUST AS OFTEN in SUCCESSFUL runs —
verification failures FM-3.2/3.3 present in successes (3.3: 20-25% both
success+fail) → CANNOT discriminate. Empirical proof "well-formed ≠
competent" (corroborated: BFCL AST≠executable; τ-bench well-formed but
pass^8<25%). Looping (FM-1.3) = #1 observable signal (15.7%) BUT
near-ubiquitous (96-99% of traces) → measure EXCESS/RATE/STREAK not
presence (= the Sylk 97%-constant pathology; CUSUM integrates the rate).
No single mode >15.7%, categories near-orthogonal (corr 0.17-0.32) →
multi-signal VECTOR CUSUM mandatory. THE METRIC SET (evidence-ranked,
non-agentic, from Hecate observables): M1 state-action recurrence/looping
(ledger; leading; FM-1.3 15.7%; excess/streak not binary); M2 outcome-
failure accumulation = validation-fail-streak + rejected-increment
(ledger verdicts; lagging/high-precision; MAST Appendix J "higher # of
failures signal higher final-failure chance" = the canonical CUSUM
input); M3 non-termination signature = turns w/o terminal ledger event
(ledger+gateway; leading; FM-1.5 12.4% "almost exclusively in failed
runs" = fatal+observable); M4 context-pressure/truncation (gateway
tokens+stop-reasons; Chroma context-rot + Lost-in-Conversation 39%-drop-
"do-not-recover"; a NORMALIZER/risk-multiplier); M5 malformed/denied-call
rate = the NON-CONFLATING behavioral metric (warden verdicts, SEPARATE
from competence; BFCL/τ-bench); M6 unforced-self-revert churn POLARITY-
CONDITIONED (revert WITHOUT preceding failed verdict = bad, Huang self-
correct-degrades; revert AFTER verdict = healthy red-green, Reflexion
91v80 — condition on the external trigger to avoid penalizing TDD); M7
refusal/error stop-reason (gateway; discrete ALARM not continuous
channel); M8 task-difficulty BASELINE normalizer (input-size + historical
pass-rate; MAST base-rates 41-87%, Anthropic "token usage explains 80%
of variance") = the risk-adjustment. METRIC-DESIGN REQUIREMENTS (each
tied to a Sylk failure + source): (a) observability = live producer per
channel or fail boot; (b) variance = counts/streaks/excess NEVER a
saturating ratio; (c) non-conflation = warden-well-formed axis SEPARATE
from Inspector/Arbiter-competent axis; (d) risk-adjustment vs difficulty;
(e) robustness = vector CUSUM not scalar. THE HONEST SPLIT: discriminator
(non-agentic) measures the observable SHAPE of degradation (M1-M7 risk-adj
M8); the SCRIBE (agentic) supplies MEANING — "unnecessary"? on-goal?
PROGRESS-toward-goal = NO-PRECEDENT for non-agentic measurement = the
Scribe's job (proxies only: looping M1 + context M3). FINALIZES HANDOFF
§1 (gathering = M1-M8) + §4 (discriminator = vector risk-adjusted CUSUM
over M1-M7 normalized by M8) + validates discriminator-informs-Scribe
(shape vs meaning). THIN: BFCL/AgentBench no per-model %; MAST Table 7
small-n magnitudes (direction robust); OpenHands 4/3/3/6 + LangGraph-25
UNREACHABLE (repo moved) — load-bearing loop evidence CONFIRMED (MAST
15.7% + pause_turn=10). MONITORING.md + HANDOFF.md write on the metric-set
verdict.

**HANDOFF DETECTION → SRE-GRADE OBSERVABILITY REFRAME (user, 2026-08-19,
5 precise points).** Metrics dossier fell short — didn't deliver (a) the
comprehensive metric suite, (b) performance-curve-grounded detector math,
(c) a SUITE (not monolithic CUSUM), (d) SRE alerting. USER'S SRE ANALOGY
(adopted wholesale): (1) METRICS = Datadog-style + well-targeted-LLM-EVAL
numeric assessments (intent-adherence, error-rate=exhaustion, failed-
validations, repetitiveness, misalignment) — measure PRECISELY/RUTHLESSLY/
COMPREHENSIVELY (note: includes LLM-EVAL numeric scores, NOT just
deterministic — corrects architect's over-restriction). (2) DETECTION =
LEARNED + DETERMINISTIC, grounded in the WELL-ESTABLISHED LLM/agent
PERFORMANCE CURVES (sudden intent-shift, long-running sessions,
context) — RESEARCH the curves, then derive the math FROM them. (3) NOT
monolithic — a SUITE of detectors, each w/ the appropriate learning-
curve/formula for its phenomenon as related to LLM perf curves. (4) On
trip, the DETECTOR provides SRE context: frequency, timing, duration,
severity — the AGENT NEVER derives these itself. (5) The SCRIBE = a
seasoned SRE: examines alerts/tripwires, acts via RUNBOOKS (skills+tools).
Corrects architect's earlier missteps (over-restricted metrics to
deterministic; proposed one vector-CUSUM). TWO RESEARCH PASSES: (A,
a4d24e5e) comprehensive METRIC CATALOG — LLM-obs platforms (Datadog LLM
Obs, Arize, LangSmith, OTel GenAI semconv, Langfuse) + LLM-EVAL metrics
(RAGAS/DeepEval/G-Eval/LLM-as-judge intent-adherence + reliability
caveats) + agent metrics (tool-correctness, trajectory, pass^k) →
deterministic-vs-eval catalog mapped to the 5 named factors; (B,
a491f37e) PERFORMANCE CURVES (context-rot/lost-in-middle/lost-in-multi-
turn-39%-non-recovery/turn-count curve SHAPES + functional forms) +
DETECTOR SUITE MATH (CUSUM/risk-adj-CUSUM/Page-Hinkley/EWMA/BOCPD/GLR/
ADWIN/DDM-EDDM/SPRT/regression-residual → mapped per-phenomenon) +
LEARNED-yet-DETERMINISTIC recipe (fit-to-curve/baseline, DPCL, ARL0=T/δ,
replay-safe; Sylk anti-pattern = fitted-but-never-read) + SRE ALERTING
(Google SRE book, SLO multi-window multi-burn-rate severity math, alert
enrichment freq/timing/duration/severity fields, runbook model). Present
when both land; then finalize HANDOFF (metric suite + detector suite +
alert schema + Scribe-as-SRE-runbooks) + MONITORING.md. Design NOT
written until the SRE-grade detection is grounded.

**CONTAINERS-IN-MICROVM RESEARCH DISPATCHED, FANNED OUT (user,
2026-08-19).** User: the earlier Scribe-isolation research was
INCOMPLETE — the missing angle is running *containers* within one
microVM (isolation of primary+Scribe, startup/runtime cost,
communication avenues); and (mid-flight correction) the pass warranted
MULTIPLE agents per cited aspect, not one. The accepted shared-runtime-
subtree design STANDS but gets RE-PRESENTED against the container
option when the lanes land. FOUR LANES in flight: (1) OCI runtime-spec
mechanics + runtime layer (crun/youki/runc; libcrun + youki-libcontainer
as EMBEDDABLE Rust crates; startup/memory/process-model COST numbers) —
narrowed from the original single agent; (2) Kata in-guest mechanics
DEEP (kata-agent CreateContainer flow, rustjail structure = the exact
shape hecate-init would take) + guest prep (cgroup2/dev) + container
rootfs on a RO virtio-fs projection (overlayfs/bind-manifest-subtree) +
LIBKRUN FEASIBILITY (containers-inside-a-krun-guest: works-today vs
fork work); (3) ISOLATION DELTA — honest: containers = the SAME kernel
primitives (strength delta vs raw processes = zero; Bar-B unchanged),
but two containers = two OS PROCESSES so the process-fatal fault classes
(abort/SIGSEGV/OOM/FFI) become PER-LOOP contained instead of killing
both — i.e. potentially converts the accepted §3 documented-gap into
per-loop containment; plus declarative-config/tooling/lifecycle deltas;
(4) COMMUNICATION avenues — pod sharing model, unix-socket-via-shared-
mount, shared-IPC, fd-passing, and the DECISIVE one: container→HOST
vsock (is AF_VSOCK namespaced? per-PORT separation so the Scribe
container gets its host stream the primary can't touch —
device-cgroup/seccomp + host-side warden enforcement), host-mediated-
only pattern as the observe-not-feed fit. ALSO: the two SRE detection
passes (metric catalog; perf-curves+detector-math+SRE-alerting) were
killed and RE-DISPATCHED fresh. Six agents in flight total. On landing:
present containers-vs-accepted-design + the SRE detection design.

**CONTAINERS LANE 1 LANDED (2026-08-19): OCI spec + runtime layer +
COSTS.** CONFIRMED: a container = a DECLARATIVE JSON encoding of exactly
the primitives the raw-process design hand-wires ("uses various kernel
features like namespaces, cgroups, capabilities, LSM, and filesystem
jails"; youki docs: "a container is just another process in Linux, which
has control groups, namespaces, pivot_root and other mechanisms applied
to it"). config.json vocabulary captured verbatim: 8 namespace types
incl. path-JOIN semantics (the K8s-pod sharing trick is first-class);
cgroup resources incl. device-allowlist + raw cgroup2 `unified`
passthrough; full seccomp (incl. SCMP_ACT_NOTIFY listenerPath); 5
capability sets + noNewPrivileges; rlimits; idmapped mounts
(MOUNT_ATTR_IDMAP — projecting one VFS subtree into two containers under
different uid maps); maskedPaths/readonlyPaths. Lifecycle: 4 states, 13
steps, CREATE/START SPLIT (stage everything privileged in create,
inspect, then fire — load-bearing for a supervisor), 6 hook kinds. runc
SPEC.md gives the exact choreography (unshare → mounts → devices →
cgroup-join-BEFORE-init-runs via FD-3 sync pipe → pivot_root →
caps/seccomp → exec) + default 15-cap set; seccomp profile = the
ENGINE's job (hecate-init owns its own profile). COSTS (measured/
published): crun 100×/bin/true = 16.9ms/container vs runc 33.4ms
(-49.4%); youki hyperfine full create+start+delete cycle = 47.3ms crun /
111.5ms youki / 224.6ms runc (UPPER bounds — 3 sudo process spawns per
cycle; embedded/library-call spawn latency = NO-PRECEDENT, unpublished);
a crun container runs under a 512KB cgroup limit where runc fails at
4MB; binaries runc 10.9MiB / crun 3.4 (2.0 no-systemd) / youki 7.8MiB
musl-static. PROCESS MODEL: create/start detaches — ZERO resident
runtime processes; monitor duty (subreaper/stdio/exit-record) = conmon
per-container, conmon-rs POD-LEVEL (Rust), or ABSORBED INTO hecate-init
when embedded. EMBEDDING: runc = Go /proc/self/exe re-exec, NOT usable
from Rust; libcrun = real C API (load_from_memory/create/start/kill/
update/pause/exec); **youki libcontainer = Rust crate 0.7.0 ("Library
for container control", 116k downloads, musl-static + v2-only feature
builds, Executor override, double-fork topology) with PRODUCTION
EMBEDDERS: runwasi (containerd's wasm shim) + rk8s — runwasi = the exact
architectural precedent for hecate-init embedding container-spawn
in-process (zero extra process census).** Lane price tag: tens-of-ms
once per container at pod start, ~0 steady-state processes, 2-8MiB code
bite — buys spec'd lifecycle/hooks/live-update/freeze/exec/stats +
conformance suite over a hand-maintained choreography; buys ZERO new
kernel primitives (isolation delta = sibling lane's verdict). Scratch
source cache left for siblings. 3 container lanes + 2 SRE passes still
in flight; containers-vs-accepted-design presents when the set lands.

**CONTAINERS LANE 3 LANDED (2026-08-19): ISOLATION DELTA.** THE HONEST
CORE: (1) container isolation = LITERALLY the same kernel primitives
(namespaces/cgroups/seccomp; NIST 800-190 "multiple apps share the same
OS kernel instance"; gVisor "container escape is possible with a single
vulnerability") → strength delta vs hand-wired raw processes = ZERO;
Bar-B unchanged (the microVM stays the real code-exec boundary). (2) THE
REAL GAIN — vs the ACCEPTED shared-runtime model — comes from the
PROCESS boundary: fault classes (b) abort / (c) stack-overflow / (d)
OOM-within-budget / (f) FFI-crash convert from "process-fatal → BOTH
loops die → pod reconstruct" (the accepted §3 gap) to "ONE container's
process dies → peer keeps running → supervisor restarts it." Kernel-
verbatim OOM boundary: "If the OOM killer is invoked in a cgroup, it's
NOT going to kill any tasks outside of this cgroup" + memory.min floor +
pids.max; fatal signals terminate THE PROCESS (signal(7)); separate
address spaces (fork(2)). CAVEAT: guest-GLOBAL OOM uncontained if
budgets oversubscribe guest RAM (sizing invariant derived from the pod
budget); (a) panic already contained in-process; (e) hang needs liveness
detection in ALL models. (3) What the container LAYER adds over raw
processes achieving the same conversion: ONE frozen declarative
config.json per peer (immutable after create — auditable, diffable
symmetry; NIST "eliminates the need to manually create all the necessary
configurations"), spec lifecycle grammar w/ cleanup guarantees
(create/start/kill/delete; delete "MUST delete the resources that were
created during the create step... resources not created by this
container MUST NOT be deleted"), standardized state/stats/hooks/exit
observation (runc events --stats; cgroup.events populated + memory.events
oom_kill = kernel-PUSHED exit/OOM notification for the Scribe), sidecar
precedent verbatim ("restarted without affecting the main application
container"). (4) LIMITS: OCI surface is a SUBSET of the raw toolbox —
NO Landlock, NO Yama ptrace_scope (zero spec hits; still hand-wired);
NO container-native mechanism strengthens cannot-starve/blind/spoof
(NO-PRECEDENT); restart POLICY + health checks = ENGINE-layer not OCI
(in-guest supervisor still writes the loop; conmon = the exit-capture
precedent). VERDICT SHAPE (for the re-presentation when all lanes land):
containers-in-guest ≈ raw-processes + declarative-config + standard
lifecycle/observability — the QUESTION becomes shared-runtime (accepted;
§3 gap documented) vs process-per-loop (gap converted to per-loop
containment; cost = lane-1's tens-of-ms + supervisor work; feasibility =
lane-2 pending). 2 container lanes (Kata/libkrun feasibility, comms) +
2 SRE passes still out.

**CONTAINERS LANE 4 LANDED (2026-08-19): COMMUNICATION AVENUES.** THE
DECISIVE FINDING (how the Scribe's host stream stays untouchable): (1)
device cgroups CANNOT keep the primary off vsock — socket(AF_VSOCK) is a
plain socket(2) call needing NO device node (/dev/vsock exists only for
the CID ioctl, vsock(7)); OCI device lists gate device NODES only. (2)
NAMESPACES cannot either — AF_VSOCK is GLOBAL per-kernel ≤6.19 (no
netns.vsock at v6.18/v6.19 tags); Linux 7.0 adds netns modes BUT
verbatim "Any vsocks within the same network namespace are always
reachable, regardless of the mode" + g2h_fallback=1 default (per-netns
0644 sysctl — writable back by netns-root unless /proc/sys RO). (3) The
enforcement IS SECCOMP on socket(2) domain — OCI arg-filtering
(index/value/op) + SHIPPED PRECEDENT: containerd's DEFAULT profile
"Allow socket(2) for all address families except AF_VSOCK and AF_ALG"
(three range rules → fall through to ActErrno); 32-bit socketcall caveat
noted (moot for x86_64/aarch64). THE THREE-LAYER ANSWER (each receipted,
no single point of failure): [host wiring] warden owns port↔UDS mappings
fixed at VM build (krun_add_vsock_port/2 verbatim; Firecracker: unwired
port ⇒ VIRTIO_VSOCK_OP_RST; guest cannot create/re-target mappings) +
[who may dial] seccomp AF_VSOCK denial on the primary (inherited by its
tool-children wholesale) + [how the Scribe holds it] init-connects-then-
passes via SCM_RIGHTS socketpair (runc console-socket precedent: "the
only process with a copy... is whoever read the fd" — NO guest-visible
name to squat) or CAP_NET_BIND_SERVICE privileged port <1024. KATA
PRECEDENT: agent owns vsock (fixed ports 1024 ctl/1025 logs/1026
debug = per-stream port separation); workload-direct-vsock =
NO-PRECEDENT; Kata ships disable_guest_seccomp=TRUE by default (their
threat model = whole-guest-one-unit; Hecate's intra-guest adversary
means Hecate must apply what Kata skips). AVENUE TABLE: localhost/
shared-netns = WEAK (port squat, unauthenticated 127.0.0.1, shared
/proc/net + firewall, CAP_NET_ADMIN rewrite); UDS-in-shared-mount =
strongest general-purpose (fs perms + SO_PEERCRED auth; dir-write peer
can squat path); shm = memory-speed/WORST integrity (disqualifying for
observer); FIFO = dominated (64KiB backpressure starvation); SOCKETPAIR-
FD-PASSING = strongest capability-shaped (unnamed, unsquattable,
possession=capability); vsock CID-1 loopback = a SIDE DOOR the same
seccomp denial closes. HOST-MEDIATED-ONLY = ideal for observe-not-feed
(no shared channel exists to tamper/starve; the broker round-trip lands
only on flows the law already forbids; K8s stdio-redirect + Kata
everything-through-agent precedents). Tool-children: socketpair-fd or
scoped UDS mount (Scribe outside the share). 1 container lane
(Kata/libkrun feasibility) + 2 SRE passes still out; containers
re-presentation on set completion.

**SRE PASS A LANDED (2026-08-19): THE COMPREHENSIVE METRIC CATALOG.**
43 metrics, ~90% CONFIRMED, two classes exactly per the user's frame.
CANONICAL VOCABULARY = OTel GenAI semconv (12 standard metrics w/
advised buckets: token.usage, operation.duration, TTFT, time-per-output-
chunk/token, invoke_agent.duration, invoke_agent.inference_calls +
.tool_calls histograms [1,2,4..128], execute_tool.duration, workflow
duration; error.type conditionally-required on failure; finish_reasons;
span vocab incl. `plan`; cache_read/creation token split) — the
deterministic substrate Hecate instruments natively. CLASS A —
DETERMINISTIC (27 metrics, 100% of traffic, FREE/CHEAP): A1 errors/tool
health (tool error rate per-tool, consecutive-same-tool-failure
run-length, schema-violation count [OpenAI ModelBehaviorError
precedent], API error rate by type, retry rate, validation.failure_count
— Hecate claim-validations slot natively); A2 loop/repetition (seq-rep-n
[Welleck], distinct-1/2 [Li], action.recurrence_rate (exact
tool+args repeats), turns-vs-budget [LangGraph recursion_limit=1000 /
MaxTurnsExceeded precedents], calls-per-invocation histograms,
embedding self-similarity + refusal-template similarity [LangKit,
CHEAP]); A3 latency histograms; A4 tokens/context/cost
(context.fill_ratio = leading exhaustion gauge ["token usage explains
80% of variance"], cache split, COST-PER-SUCCESSFUL-TASK not per-call
[Arize: "a cheap run that fails and gets retried is the expensive
one"]); A5 stop-reason distribution (end_turn/max_tokens/pause_turn/
refusal/context-exceeded mix-shift = countable degradation surface) +
refusal/empty rate; A6 reliability probes (pass^k = E[(c choose k)/(n
choose k)] [τ-bench; pass^8<25% vs pass^1 61%], pass@k ceiling,
UNRELIABILITY U₁₀⁹⁰ = p90−p10 + aptitude A⁹⁰ [Lost-in-Conversation:
aptitude −16% but unreliability +112%], self-consistency agreement,
trajectory match strict/unordered/subset/superset [agentevals],
tool-correctness ratio, path convergence = optimal/average length,
end-state reward r_action×r_output [τ-bench; = Hecate claim terminal
states]). CLASS B — LLM-EVAL JUDGE (16, sampled, 0-1 + reasoning,
threshold-gated): intent/instruction adherence (Prompt Alignment =
followed/total), goal completeness (resolved/identified intentions;
Datadog >50%-unresolved⇒incomplete precedent), ACTION ADVANCEMENT
per-turn progress (the stall detector: advancement→0 while turns climb
[Galileo]), task completion (trace AlignmentScore), step efficiency,
tool selection/argument/response-handling judges, faithfulness =
supported/total claims + hallucination = contradicted/total contexts,
topic adherence P/R/F1, role adherence, KNOWLEDGE RETENTION =
turns-without-attrition/total (THE repeat-asks metric [DeepEval]), user
friction ("corrections, retries, frustration in follow-ups" [Phoenix]),
safety set, G-Eval custom rubrics (auto-steps, token-prob-weighted
score; Spearman 0.514), judge-of-judge calibration. JUDGE CAVEATS
(primary numbers): position bias swap-consistency GPT-4 65%/GPT-3.5
46%/Claude-v1 24%; verbosity attack 8.7% vs 91.3%; self-preference
correlates w/ self-recognition → RULES: single-call 0-1 rubric
(Anthropic prod: "single LLM call... 0.0-1.0... most consistent"),
never fixed-order pairwise, length-normalize, judge ≠ judged family;
agreement ceiling ≈ human-human 81-85%. FIVE-FACTOR MAPPING delivered
(intent/error-exhaustion/failed-validations/repetitiveness/misalignment
× deterministic-vs-judge). TIERS: T1 = tool-errors+retries, validation
failures, tokens/context, stop-reasons, turns/calls, latency, pass^k +
U₁₀⁹⁰ canaries (the two with published degradation numbers); T2 =
goal/intent judges, tool judges, repetition stats, step efficiency,
knowledge retention, friction; T3 = faithfulness, topic/role, safety,
convergence, plan, calibration. "Exhaustion" as a named metric =
NO-PRECEDENT (Hecate names a composite the industry measures piecewise).
FINALIZES HANDOFF §1 (gathering = this catalog, tiered). Remaining: SRE
pass B (curves+detector-math+alerting) + container lane 2 (feasibility).

**CONTAINERS LANE 2 LANDED (2026-08-19): KATA MECHANICS + LIBKRUN
FEASIBILITY — the set of four is COMPLETE.** THE LOAD-BEARING FINDING:
**libkrunfw (6.12.91) ships a container-capable kernel config TODAY**,
both arches — NAMESPACES/PID/NET/USER/UTS/IPC/TIME_NS, full CGROUPS
(MEMCG/PIDS/DEVICE/FREEZER/BPF), SECCOMP_FILTER, OVERLAY_FS +
TMPFS_XATTR (overlay-on-tmpfs works), DEVTMPFS, VETH/TUN/NFTABLES,
VSOCK/VIRTIO_FS/FUSE_DAX all =y. NOT set: **CONFIG_SECURITY → NO LSM in
the guest — NO LANDLOCK, no SELinux/AppArmor** (cross-lane correction:
the raw-process toolbox's Landlock leg is UNAVAILABLE on the stock
libkrunfw kernel; a fork-config flip if wanted); no OVERLAY_FS_
REDIRECT_DIR/METACOPY (EXDEV-on-lower-rename, tolerated); kernel carries
libkrun's ~30-patch out-of-tree queue (TSI etc.) = THE recurring fork
cost across kernel bumps. LIBKRUN 2.0 = the init seam is SUPPORTED:
init split into libkrun_init.so, krun_fs_add_overlay_file injects any
init binary as a virtual inode ("no rootfs modification needed");
teardown-on-workload-exit is PURE INIT POLICY (exec.rs receipted:
waitpid(main)→set_exit_code(ioctl 0x7602)→reboot); krun_add_virtiofs3
gives RO root + DAX first-class. KATA MECHANICS (pinned-commit source):
do_create_container 11-step pipeline; Start = exec-FIFO one-byte kick
(create/start split runc-style); persistent sandbox IPC/UTS ns via
bind-mount to /var/run/sandbox-ns (pid ns can't persist —
first-container-as-infra pattern); storage = driver registry →
baremount; bundle = bind rootfs under /run/kata-containers/<cid>;
RUSTJAIL = re-exec-self-with-"init"-subcommand (one static binary =
supervisor + container-init scaffold; spec/process/state/cgroup-mgr as
JSON over sync pipes; pidns-unshare-then-fork; userns uid_map handshake;
pivot_root exact runc dance; seccomp-before-capdrop ordering;
parent-applies-cgroups; ≈7k lines REDUCIBLE for Hecate's 2-container/
no-userns/no-hooks/no-systemd case — kata itself forces cgroupfs when
agent-is-init). GUEST PREP: kata INIT_ROOTFS_MOUNTS checklist ≈ what
libkrun stock init ALREADY mounts (incl. cgroup2); delta = nsdelegate +
/dev/pts/ptmx symlink + /run tmpfs + per-container cgroup subtrees;
manifest projection needs only empty dev/proc/sys/run mountpoint dirs
(libkrun synthesizes as virtual dirs). ROOTFS RECIPE: lowerdir = RO
manifest SUBTREE of the projection (same virtio-fs device, host-side RO)
+ upper/work = GUEST TMPFS + kernel overlayfs → bind → pivot;
ANTI-RECIPE receipted: upper on host-shared virtio-fs BREAKS
(muvm #199: trusted.overlay xattr EPERM + rename EACCES on FUSE).
PRECEDENT LEDGER: containers inside a libkrun-VMM VM = CONFIRMED
production (podman machine on macOS) BUT boots EFI/distro-kernel — does
NOT exercise libkrunfw-kernel+minimal-init; crun's krun handler =
inverse direction; **containers spawned INSIDE a libkrunfw-kernel guest
by a custom PID 1 = NO-PRECEDENT — every ingredient individually
receipted (kernel config + init seam + rustjail/vminitd/kata-agent as
3 independent architecture precedents) but Hecate would be FIRST to
assemble it**; muvm #199 = the one recorded similar attempt, stalled on
guest-prep gaps Hecate's design avoids (tmpfs upper, no rootless, no
pasta/tun). hecate-init build sketch: contract +her spawn-container verb;
embedded rustjail-pattern spawner; W3 prep delta; W4 rootfs recipe.
CONSOLIDATED CONTAINERS-VS-ACCEPTED RE-PRESENTATION assembled in-thread
(four lanes complete). Remaining agent: SRE pass B only.

**SRE PASS B LANDED (2026-08-19): PERFORMANCE CURVES + DETECTOR SUITE +
ALERT DISCIPLINE — all research complete.** CURVES (W1): context-length =
monotone-in-trend NON-UNIFORM decline, slope conditioned on
needle-similarity + distractors (Chroma 18-model; NoLiMa "11 of 13 below
50% of baseline at 32K"; GPT-4o 99.3→69.7) — NO universal closed form ⇒
a LEARNED per-(agent,task-class) reference curve; position = U-SHAPE
(Liu: 75.8/53.8/63.2, middle can undercut closed-book 56.1) ⇒ a
COVARIATE for risk adjustment, not an alarm; intent-shift/multi-turn =
CHANGEPOINT not ramp (−39% step; aptitude −16% vs unreliability +112% —
the dominant signal is VARIANCE EXPLOSION) + ABSORBING ("get lost and do
not recover"); long-horizon = METR LOGISTIC-in-log-task-duration (50%
time horizon; ~100% <4min vs <10% >4hr; doubling ~7mo) + τ-bench pass^k
combinatorial decay + Vending-Bench MELTDOWN regimes "rarely recover",
UNCORRELATED with context fill (⇒ detect regime onset, not smooth
decay); Viering-Loog caution: "no universal model" ⇒ fit a small
candidate family per phenomenon, select by held-out fit. DETECTOR SUITE
(W2, 10 detectors, all online + deterministic-given-frozen-params, each
w/ formula + false-alarm characterization): CUSUM (S=max(0,S+x−μ−k),
k=δσ/2, h≈4-5σ or b=|log α|, Lorden/Moustakides minimax-optimal,
ARL0=1/FAR); RA-CUSUM (STEINER FORMULA VERBATIM: exp(R_t)=exp(YΔ)·
(1+e^{Xβ})/(1+e^{Δ+Xβ}) — per-agent charts, ARL0=10000 precedent);
Page-Hinkley (mean drift); EWMA (λ 0.2-0.3, gradual drift); BOCPD
(run-length posterior = ONSET-TIME evidence; NO frequentist FA guarantee
— never the sole alarm authority; at defaults doesn't beat baselines);
GLR-CUSUM (unknown shift size — the intent-shift fit); ADWIN
(variance-aware ε_cut, FP≤δ/step + FN bounds THEOREMS, window cut ⇒
DURATION estimate, O(log W)); DDM/EDDM (built for "learner's error rate
rose": p+s vs p_min+2s/3s = 95%/99%); SPRT (A=(1−β)/α, B=β/(1−α), true
errors α′≤α/(1−β), ~50% fewer obs — the ADJUDICATION step);
learned-curve+residual-band (regression-adjusted charts = standard SPC;
Gandy-Kvaløy residual CUSUM/EWMA verbatim). PHENOMENON→DETECTOR MAP:
context-rot → fitted-curve residual EWMA/CUSUM; position/difficulty →
risk-adjustment covariates; intent-shift → GLR-CUSUM + DISPERSION-CUSUM
(variance!) + BOCPD onset; derailment/loops → Page-Hinkley/ADWIN;
reliability decay → DDM/EDDM + RA-CUSUM w/ difficulty model; confirmation
→ SPRT. LEARNED+DETERMINISTIC RECIPE (W3): fit→FREEZE as versioned
logged artifact→detector READS it (pure function of metrics-log +
artifact-version = replayable bit-for-bit)→thresholds DERIVED from
false-alarm budget (b=|log α|; ARL0=T/δ; SPRT A/B; ADWIN/DDM δ) +
BOOTSTRAP-CALIBRATED for estimation error (Gandy-Kvaløy: "guarantee with
high probability that the in-control ARL is not below a specified
value"; naive 4.1→adjusted 5.5 example); GP posterior mean/var =
closed-form deterministic predictor; conformal bands when
model-skeptical; refit out-of-band bumping artifact version. THE SYLK
LAW: "if deleting the fitted artifact would not change any alert, the
design is wrong." SRE ALERTING (W4): every page actionable; alert
fatigue discipline; BURN-RATE math (burn = how fast budget consumed;
14.4×/1h page, 6×/6h page, 1×/3d ticket; 1000× ⇒ 43min exhaustion;
short-window 1/12 reset refinement; precision/recall/detection-time/
reset-time = the 4 axes); for/keep_firing_for anti-flap; Datadog anomaly
bands (rolling-quantile/SARIMA/decomposition); Alertmanager structured
fields (Status/StartsAt/EndsAt/Fingerprint/Labels/Annotations/
GeneratorURL) + grouping/dedup/INHIBITION ⇒ 1:1 alert/incident;
runbooks ("playbooks... explain the severity and impact... include
debugging suggestions and possible actions"; folkloric 3×-MTTR figure
NOT FOUND — do not cite). ALERT SCHEMA delivered: {phenomenon,
fingerprint, status, severity(burn-rate-graded), frequency(error-ratio/
burn/budget-consumed), onset(StartsAt + changepoint-estimate from
BOCPD-MAP/ADWIN-cut/CUSUM-last-zero), duration(pending/firing/ends),
trajectory(statistic/threshold/time-to-exhaustion), evidence(residuals/
curve-ref/params/FA-budget), runbook_ref} — ALL deterministic; the
Scribe receives enriched incidents and NEVER computes these; its
intelligence = WHICH runbook action. NO-PRECEDENT flagged honestly:
universal context-length law; per-(agent,task-class) curve-fitting +
residual charts FOR LLM AGENTS; agent-loop probability curve;
burn-rate severity on QUALITY budgets — all novel compositions of
CONFIRMED parts. FINALIZES HANDOFF §4 (detector suite replaces the
single CUSUM) + §5 (alert schema + Scribe-as-SRE) — both presentations
(containers + SRE detection) now assembled in-thread; ALL agents
complete; awaiting user verdicts.

**INTRA-VM CHANNEL + SCRIBE THREAD MODEL — USER REFINEMENT (2026-08-19).**
Two directives on the MONITORING presentation: (1) the Scribe RECORDS A
RUNNING HISTORY of its colocated primary; its SECONDARY thread should
largely exist only for OUTBOUND reach-out (Archivalist/external) — the
main loop consumes the history stream; (2) "we *should be able to
identify communication and networking internal to the microVM for comms
between the two OCI containers*" — a DESIGNED, IDENTIFIED, CLASSIFIED
intra-VM channel is REQUIRED. HONEST REVISION this forces on observe-not-
feed (named, not buried): the presented design routed ALL Scribe input
guest→host→guest, taxing the highest-rate flow (colocated history) with
VMM hops. RESOLUTION = the AUTHORITY/ENRICHMENT split: authority signals
(warden verdicts, ledger deltas, gateway) STAY host-side tamper-proof —
detection/scoring reads ONLY those; the HISTORY/narration stream flows
INTRA-VM primary→Scribe over a designed channel whose safety shape is:
emitter NEVER blocks (non-blocking, overflow=counted drop — the kernel
observability channel shape: BPF ringbuf/perf-buffer/ftrace all do
exactly this), seqnum+drop-counter gap detection cross-checked against
host streams (silence/tamper is itself a detectable signal the primary
can't hide because warden/ledger streams don't lie), protection
asymmetry (writer-RW/reader-RO or kernel-mediated), supervisor-created
fd-passed (no name to squat), and the channel is a FIRST-CLASS
CLASSIFIED lane in the transport registry (identity via
SO_PEERCRED/SO_PEERPIDFD/fd-provenance; metering/rate-enforcement
hooks; honest note: intra-guest traffic is invisible to the VMM unless
exported — in-guest sensor/cgroup stats are the host visibility path).
Primary LYING in its own history = bounded (enrichment only; authority
is host-side) — the Sylk distinction preserved: Sylk's fault was
feed-as-SOLE-input + self-score; this is emit-as-enrichment + host-side
authority. THREE RESEARCH LANES DISPATCHED: (1) mechanisms+NUMBERS
(a2ad7636: UDS stream/seqpacket vs pipes/splice vs shm+eventfd-doorbell
vs TCP-lo/shared-netns vs veth-pair/separate-netns vs vsock-CID_LOCAL —
latency/throughput/syscalls-per-msg/copies/backpressure table); (2)
one-way tamper-bounded stream DESIGN (a2c7ce1a: BPF-ringbuf/perf
data_head-data_tail/PERF_RECORD_LOST/ftrace-overwrite-vs-drop
semantics; LMAX single-writer+sequence; seqlock; memfd_create sealing
esp. F_SEAL_FUTURE_WRITE writer-keeps-RW/new-maps-RO asymmetry —
VERIFY; journald suppressed-N + K8s stdout + Vector when_full=
block-vs-drop_newest precedents; the layered-trust untrusted-producer/
trusted-control-plane cross-check pattern); (3) identity/observability/
classification + THREAD MODEL (a9e1a810: SO_PEERPIDFD, sock_diag/
UNIX_DIAG, tc-on-veth rate enforcement, memcg sock accounting,
boot-classification tuples per channel type; epoll-ET/io_uring
SINGLE_ISSUER+DEFER_TASKRUN+multishot-recv single-thread ingestion;
tokio current-thread + outbound-only side pool = the reactor shape
grounding "secondary thread only for outbound"). On landing: the channel
design + thread model fold into MONITORING §2/§4 and re-present.

**HISTORY-STREAM PURPOSE CONFIRMED (user, 2026-08-19): "the purpose of
the scribe ingesting and observing primary agent actions is to help keep
history for handoff, etc."** Pins the intra-VM stream's consumer
purposes: (1) HANDOFF BRIEF assembly — the Scribe's running window IS
the source of the Scribe brief that resume-by-reconstruction consumes
(AGENTS_RUNTIME R3: successor reconstructs from claims graph + Scribe
brief at watermark); (2) history SERVING (peers consult the Scribe for
its primary's recent activity; Archivalist beyond the window); (3)
narration. All ENRICHMENT/CONTINUITY — never detection authority
(the split holds). DESIGN CONSEQUENCES: (a) the Scribe's outbound
thread's primary duty = periodic history/narration FLUSH to the
Archivalist (the durability path — R3's "no in-memory state is
load-bearing across instances" preserved: durable continuity = claims
graph + archived narration; the live window is a quality enhancer, not
a durability dependency); (b) CONTAINER-DESIGN BENEFIT now explicit:
because the Scribe is a separate container, its live history window
SURVIVES the primary's death — on a primary crash or performance
handoff the Scribe assembles a rich brief from the intact window
(vs pod-death = archive+claims reconstruction only); (c) window sizing
+ flush cadence = derived constants (window from handoff-brief needs —
turns-to-reconstruct; cadence from window size × loss tolerance).
Folds into MONITORING §4/§7 + HANDOFF §8 on re-present when the three
channel lanes land.

**CONTEXT-ECONOMY RATIONALE CONFIRMED (user, 2026-08-19): the Scribe's
history-keeping "effectively ensures the primary agent doesn't waste
context annotating and keeping track of its own history on top of doing
work."** Elevated to a design LAW with two consequences: (1) THE
DIVISION-OF-LABOR LAW — the primary spends context on WORK ONLY; it
carries ZERO history-keeping duties: no self-annotation instructions in
its prompts, no history-summarization turns, no narration obligations.
The Scribe spends ITS context on history/narration. Grounded in the
curves already on file: context-rot degrades performance with length;
"token usage by itself explains 80% of the variance"; context exhaustion
= the dominant handoff cause — so every self-annotation token costs
3× (tokens + accelerated rot + earlier context handoff); offloading =
a performance intervention, not a convenience. (2) THE MECHANICAL
REALIZATION — for the offload to cost the primary ~ZERO tokens, the
history stream is emitted BY THE PRIMARY'S RUNTIME (hecate-rt
instrumentation at turn boundaries/tool dispatch/claim posts —
structured activity events as a SIDE EFFECT of doing work, below the
model), NEVER by the model writing annotations. The channel's emitter is
runtime code, not model output — which also strengthens the
tamper-bounding (runtime-emitted events are code-shaped, not
prompt-injectable prose; the model can't be socially-engineered into
corrupting a stream it doesn't write). TESTABLE: the primary's prompt
assembly contains zero history-keeping instructions (grep-proof); the
primary's token spend carries zero narration overhead (measured);
history capture continues when the model is mid-inference (it's
runtime-level). Folds into MONITORING §4 (emitter = runtime
instrumentation) + §7 (division of labor) + the CONTEXT.md Scribe
definition annotation on re-present.

**CHANNEL LANE 3 LANDED (2026-08-19): IDENTITY/OBSERVABILITY/METERING +
SCRIBE THREAD MODEL.** IDENTITY: SO_PEERCRED (kernel-attested, at
connect/socketpair time — stale-PID race noted) → **SO_PEERPIDFD (Linux
6.5) = the race-free modern primitive** ("allows programmers not to care
about PID reuse"; -ENODATA fail-closed; NOT yet in man pages — receipted
from kernel source + 6.5 changelog; guest-kernel ≥6.5 = a boot-check
item; libkrunfw is 6.12 ✓); SCM_CREDENTIALS kernel-checked per-message
(forgery needs CAP_SYS_ADMIN/SETUID/SETGID — de-capped containers can't
spoof); **fd-provenance = possession-is-identity** (capsicum "makes file
descriptors into capabilities"; supervisor-minted channel = no name, no
connect race, endpoints exhaustively known at boot = ideal for the
transport registry; socketpair keeps SO_PEERCRED/PIDFD for audit,
pipes/memfds don't); veth = interface-is-identity (supervisor-assigned,
non-forgeable-from-inside); vsock-loopback intra-guest = WEAKEST (both
ends CID 1, identity = port only, no peer-cred equivalent =
NO-PRECEDENT) → vsock stays guest↔host only. OBSERVABILITY/METERING:
`ss -xmpe` alone = full audit tuple (path+inode+uid+pid+queue depths+
drop counter); sock_diag/UNIX_DIAG programmatic (PEER inode = pairwise
topology!, RQLEN, SK_MEMINFO array); bcc undump/sofdsnoop kprobe
patterns (even SCM_RIGHTS handoffs eBPF-auditable); **BPF_CGROUP_UNIX_*
attach types = per-CONTAINER interception of UDS connect/sendmsg — the
runtime tripwire that makes the boot-classification law enforceable
after boot** (connect to an unregistered path = caught); veth = the ONLY
kernel-enforced rate cap (tc-tbf/police) + ABI-stable byte counters.
ACCOUNTING ASYMMETRY (registrable attribute per transport): pipe pages
= memcg-charged to the WRITER (__GFP_ACCOUNT receipted); shm =
indeterministic sharer-charging (pin by pre-faulting); **UDS buffers =
NOT memcg-charged at all** (af_unix.c negative-searched) → cap via
SO_SNDBUF/RCVBUF + meter via UNIX_DIAG. HONEST HOST-VISIBILITY LAW:
intra-guest traffic is INVISIBLE to the VMM unless exported — the
warden's window = an in-guest sensor shipping derived telemetry over a
registered vsock flow; provenance-class the metrics ("as reported by
guest sensor" vs host-observed). THREAD MODEL (kernel-enforced!):
io_uring IORING_SETUP_SINGLE_ISSUER (-EEXIST on violators = a KERNEL
assertion of the one-thread invariant) + DEFER_TASKRUN (completion
batching; "reduce request latency by 50%" in-kernel receipt) + multishot
recv w/ provided buffers (one submission → stream of CQEs); eventfd
doorbell epoll-integrable + cheaper than a pipe; tokio current-thread +
spawn_blocking (cap max_blocking_threads to outbound-channel count, not
default-512) = the packaged reactor-with-side-pool; capacity: Redis
single-thread ≈180k req/s unpipelined / >1.5M batched vs agent-history
O(10²-10³)/s = 2-4 orders headroom → INGESTION NEVER NEEDS THREAD #2;
secondary lane = outbound-only, justified exactly when outbound involves
blocking libs or vsock backpressure. Registry tuples per channel type
delivered (fd-pair/UDS-mount/shm+doorbell/veth/vsock). 2 lanes still
out: mechanisms+numbers (a2ad7636), one-way stream design (a2c7ce1a).

**CHANNEL LANE 2 LANDED (2026-08-19): ONE-WAY STREAM DESIGN.** Kernel
precedent convergence — FOUR independent kernel observability channels
(BPF ringbuf / perf / ftrace / relay) all obey one law: THE PRODUCER
NEVER BLOCKS; consumer lag = counted/detectable loss, never stall. BPF
ringbuf: "if there is no more space left in ring buffer, reservation
fails, no blocking"; reserve/commit split w/ busy+discard header bits;
epoll doorbell w/ SELF-PACING ("send a notification … only if consumer
has already caught up"); double-mapped data area for contiguous
wraparound; NO kernel drop counter (producer counts own failed reserves
— convention). **kernel/bpf/ringbuf.c enforces OUR constraint in
shipped code**: consumer may write ONLY its consumer_pos page (mmap
handler: "allow writable mapping for the consumer_pos only", EPERM
otherwise). perf: data_head/data_tail protocol; **overwrite-vs-consume
selected by the CONSUMER'S MAPPING PROTECTION** (RO map = flight
recorder; PROT_WRITE data_tail = kernel won't overwrite unread);
PERF_RECORD_LOST = in-band counted loss record (loss discovered by
READING the stream). ftrace: overwrite vs producer/consumer modes;
"a writer can preempt a reader, but a reader cannot preempt a writer";
reader-page SWAP = reader never contends on live pages. relay: "data
will be lost in either case; the only difference is whether data is
lost from the beginning or the end of a buffer" — THE both-ways-lossy
law, verbatim. Userspace: LMAX Disruptor claim/commit/batch-catch-up
sequencing (single-producer = zero contention) BUT its full-buffer
policy = producer WAITS — replaced by the kernel-observability policy
for our shape. Thompson single-writer principle: every cursor has
exactly one writer, cross-visibility read-only. seqlock even/odd
read-retry for aux stats blocks (no writer starvation). **memfd
asymmetry VERIFIED verbatim**: F_SEAL_FUTURE_WRITE = "one process can
create a memory buffer that it can continue to modify while sharing
that buffer on a 'read-only' basis with other processes" (writer keeps
prior RW maps; new writable maps + write(2) ⇒ EPERM); ALSO the fd-MODE
route: O_RDONLY fd ⇒ EACCES on any PROT_WRITE MAP_SHARED (mmap(2)) —
no ordering constraint AND survives writer respawn (FUTURE_WRITE would
block a respawned writer's map ⇒ fd-mode chosen for Hecate);
F_SEAL_SHRINK|GROW|SEAL kills the shrink-SIGBUS attack + locks
geometry. Log precedents: LTTng = fullest userspace statement ("LTTng
privileges performance over integrity"; instrumented app writes shm
rings, colocated consumer daemon reads; discard mode saves lost-count
INTO the trace; overwrite mode stamps PER-SUB-BUFFER seqnums since 2.8
— the flight-recorder torn-read answer); journald: datagram-per-entry
+ SEALED-memfd large entries (the untrusted-peer rationale applied in
production) + counted suppression ("Suppressed %i messages" +
N_DROPPED= machine field; count carried on next permitted message);
K8s/CRI: emission inside, collection authority outside; Vector names
block vs drop_newest and reserves drop for telemetry-grade data.
TAMPER LIMITS (Garfinkel&Rosenblum NDSS'03 VMI): isolated observer
"continue[s] observing and reporting with integrity even if the host
has been corrupted"; compromised in-domain reporter "may even start to
report misleading data" ⇒ SILENCE/GAPS mechanically detectable (seqnum
discontinuity + counter deltas + stream-instance id + host
cross-check); LIES not detectable from inside ⇒ the intra-VM stream is
ENRICHMENT class, authority reads host-side streams — our
classification law, now source-grounded. Dossier delivered two
candidates: A = memfd ring + eventfd doorbell (BPF-ringbuf shape, 0
syscalls/copies hot path, overwrite variant per perf's rule); B =
socketpair SEQPACKET MSG_DONTWAIT (journald shape, kernel-mediated
total isolation, 1 syscall+copy/event, clean EOF; no overwrite mode).

**CHANNEL LANE 1 LANDED (2026-08-19): TRANSPORT MECHANISMS + MEASURED
COSTS.** Three measured tiers, same-box ping-pong (ipc-bench,
i5-4590S): shm/mmap 4.7–5.3M msg/s (~0.2µs RTT) ≫ pipes 162k / UDS
130k (~6.2–7.7µs) > TCP-lo 70k (~14.2µs) — **shm = 36–41× UDS message
rate**, payload-size-independent (iceoryx "without a single copy";
rigtorp SPSC 112M ops/s; LMAX mean 52ns). UDS-vs-TCP corroborated ×3:
Redis "around 50% more throughput" (edge ERODES under pipelining),
Percona 33–35% + p99 12× at saturation. Pipes: 64KiB default / 1MiB
unprivileged cap (F_SETPIPE_SZ); vmsplice zero-copy is PRODUCER-side
only ("in the opposite direction, it actually just copies");
Cloudflare splice reality-check: CPU-bound below line rate, still 2
syscalls/chunk. SOCK_SEQPACKET = boundaries+order+connection (unix(7)
verbatim); STREAM amortizes (one recv drains many; io_uring multishot
→ measured 2.00→1.01 syscalls/op at depth, SYSTOR'22) vs SEQPACKET
hard 1 syscall/msg + MSG_TRUNC truncation risk. SO_SNDBUF default =
A FORMULA IN KERNEL SOURCE (SK_WMEM_DEFAULT = 256 × SKB_TRUESIZE(256)
≈ 212992) — constants-from-anchors precedent in the kernel itself;
AF_UNIX dgram qlen default = 10 (shallow). Networking tier DOMINATED:
veth+bridge = 18–30% bulk loss + ~10× MPI latency (INFOCOM'18: "Good
performance can be attained by sharing the same network namespace
while security is enforced by using isolated namespaces"); vsock
CID_LOCAL = ZERO published loopback numbers (NO-PRECEDENT) + netns-
blind pre-7.0 + weakest identity ⇒ stays guest↔host only (lane-3
concurrence). **vhost-user = THE industrial precedent for our shape**:
shm data plane + eventfd kick/call fds passed as ancillary data —
every DPDK/virtio userspace backend runs on it; K8s pods bless
cross-container shm. libkrunfw guest config VERIFIED both arches:
UNIX/MEMFD/EVENTFD/FUTEX/SHMEM/VSOCK+LOOPBACK/VETH/IO_URING/EPOLL all
=y — nothing excluded. SQPOLL pathology receipted (13 KIOPS / 8ms
median when core-starved; "more cores than drives" demanded) ⇒ NOT for
the Scribe; multishot + DEFER_TASKRUN is the shape. Syscall floor:
mode switch ~50–100ns; blocked-consumer wakeup = context-switch-class
1.1–4.5µs regardless of transport — why every blocking transport lands
in the same RTT class and only shm+polling escapes it.

**CHANNEL COMPOSED (2026-08-19) + BOTH SPECS RE-PRESENTED IN FULL.**
The composition (three lanes converge): **supervisor-minted memfd
flight-recorder ring + eventfd doorbell** — hecate-init mints ring
memfd + cursor memfd + eventfd BEFORE spawning either container,
passes fds at spawn (fd-provenance = possession-is-identity; no name,
no connect race; registry endpoints fixed at VM build). SPLIT-CURSOR
fd-MODE asymmetry (each memfd exactly one writer, kernel-refereed):
ring = primary O_RDWR / Scribe O_RDONLY; cursor = Scribe O_RDWR /
primary O_RDONLY; both sealed SHRINK|GROW|SEAL (geometry locked,
shrink-SIGBUS dead); NO FUTURE_WRITE (blocks respawned writer;
fd-mode already does the work). Primary PRE-FAULTS the ring ⇒ pages
memcg-charged to the primary deterministically — THE OBSERVED PAYS FOR
ITS OWN BLACK BOX. Protocol: LTTng-style SUB-BUFFERED OVERWRITE
(flight recorder) — producer never blocks/never drops NEW; full ring
reclaims OLDEST unconsumed sub-buffer + counts it; chosen FOR THE
PURPOSE (handoff brief needs the NEWEST window; wedged-Scribe losses
land on oldest unpersisted — relay both-ways-lossy law, we pick the
end that serves handoff); per-sub-buffer seqnum/commit stamps give the
torn-read answer (copy-out then re-validate stamp; changed ⇒ discard
+ count — seqlock discipline at sub-buffer granularity, LTTng-shipped
15yr); record = 8B header (len+commit+discard bits) + monotone seqnum
per stream-instance id (journald model: respawn = new id ≠ gap);
carries STRUCTURED ACTIVITY EVENTS ONLY (bounded metadata records —
turn boundaries, tool dispatch digests, claim posts, stop reasons,
usage), never transcripts/raw tool output; doorbell self-paced (elide
when consumer behind); doorbell misuse = self-DoS ≡ silence class.
Sizing = formulas (sub-buffer ≥ max record × batch factor; ring =
max event rate × worst-case drain interval incl. Scribe restart
backoff ceiling). CHANNEL SURVIVES BOTH DEATHS (the decisive argument,
not the 36–41× throughput — irrelevant at O(10²–10³)/s): supervisor
holds fds; Scribe respawn re-maps + resumes from its OWN cursor
byte-exact; primary death ⇒ Scribe drains tail to final producer_pos ⇒
death report carries the final-actions window; teardown gated on flush
(pipeline lifecycle law). Candidate B (socketpair) REJECTED for the
stream: kernel queue dies with the socket on Scribe restart (channel
state lost), UDS buffers memcg-UNcharged (accounting hole), no
flight-recorder mode; B's shape retained nowhere intra-VM (no
primary↔Scribe control channel exists at all — supervisor owns
lifecycle). Thread model folded: ingestion = ONE thread
(SINGLE_ISSUER kernel-asserted, multishot poll on eventfd,
DEFER_TASKRUN; 2–4 orders headroom); secondary = outbound-only
spawn_blocking capped to outbound-channel count. Design survives
EITHER §2 ruling: under Design B (shared runtime) protocol identical,
enforcement degenerates kernel-fd-modes → compile-time ownership.
MONITORING re-presented w/ §4 REVISED (authority/enrichment split +
context-economy law replace "no primary→Scribe channel of any kind" —
the runtime-emitted one-way history ring is the sole primary-side
channel, model-unreachable, enrichment-class) + NEW §5 (the channel) +
renumber + MON14–20 + criteria; HANDOFF §3/§8 updated (window
transit/persistence split; brief includes drained tail on death).
AWAITING: §2 ruling (A vs B) + accept/amend on both full specs.

**BRANCH OPENED (2026-08-19): WARDEN/SENSOR INTERIOR COVERAGE + THE
CONDUCT SIGNAL PATH** (user directive, two demands, children of §2/§5):
(1) warden/sensor must be designed to handle INTERNAL microVM traffic
(the two-container interior); (2) the Scribe must work with BOTH warden
AND sensor — metrics from both feed detection; a malicious/misaligned
agent trips both regularly ⇒ handoff path. CORPUS GROUND TRUTH read:
PODS §6 (warden = host-side pre-effect on the device surface; "in-guest
actions are ungated as calls" — sound for ONE workload, predates the
two-container interior; sensor = guest-kernel eBPF, fixed image-hashed
programs, tighten-only, silence-is-a-signal, streams to the warden over
its own vsock channel; T13–T17); HEALTH (pod-pressure signal already
sources warden+sensor; content-free H8; AbsenceIs::Degraded for sensor;
no-authority H4); IAM §7.3 (warden compile-source ratified; sensor = a
DENY layer above the evaluator, never a decide() step); IAM §6
(compile-and-distribute per-PEP residuals). FOUR TENSIONS/GAPS NAMED:
(T1) PODS §1 "one microVM running one agent" — predates primary+Scribe;
definitional amendment owed. (T2) PODS §3 init contract is EXHAUSTIVE
(five duties; "an init that can do more fails review") vs the
two-container extension (spawner + channel minting) AND the
newly-found hole: the sensor's kernel programs cannot speak vsock —
SOMETHING userspace must drain BPF rings into the sensor channel, and
no component owns that duty (init? a dedicated supervisor-plane
exporter?). (T3) kernel-config conflict: PODS §6 requires eBPF/LSM
"compiled into our kernel image" vs containers-dossier receipt (stock
libkrunfw: CONFIG_SECURITY unset, no LSM) — AND self-flag: MONITORING
§5.8's BPF_CGROUP_UNIX_* tripwires assumed CONFIG_CGROUP_BPF, never
verified in stock config; the fork-flip list must be enumerated
DAX-style ("fork work, tracked — not waived"). (T4) detection stack has
NO conduct phenomenon: HANDOFF §1 consumes warden verdicts as
work-quality only; warden security verdicts (deny/hold/escalate rates,
class mix) + sensor telemetry (syscall-class aggregates, tripwire
firings, interior denials) absent as detector inputs; no §4 row for
repeated-enforcement-tripping; interior denials (seccomp
RET_ERRNO = silent!) currently surface NOWHERE. WORKING HYPOTHESIS
(pending receipts): NO second warden — warden stays the single
authority; IAM §6 compile-and-distribute extends ONE MORE HOP into the
guest (interior enforcement = warden-compiled kernel residuals —
seccomp/BPF/cgroup profiles — installed by hecate-init BEFORE either
workload runs; install-then-exec ordering = Bar-A trustworthy); interior
observation = the sensor extended with per-container attribution
(cgroup-id-keyed) + denial-event classes, drained by a supervisor-plane
exporter; conduct phenomenon enters HANDOFF §1/§4 with rare-event
detectors (Poisson/Bernoulli/TBE CUSUM) under the same δ budget;
line drawn: pattern ⇒ Scribe-runbook ⇒ handoff; confirmed hostility ⇒
Guardian hard-block (never mere handoff); every tripped op was ALREADY
denied pre-effect — detection adds the ACTOR response, enforcement owns
the ACT. THREE LANES DISPATCHED: (a) interior enforcement observability
(seccomp denial observation routes RET_LOG/USER_NOTIF + TOCTOU caveat,
BPF LSM, cgroup-BPF attach mechanics + landing versions, cgroup v2
event surfaces memory.events/pids.events/cpu.stat/PSI + poll semantics,
libkrunfw stock-config verification of the full BPF/tracing/audit/PSI
flag set both arches ⇒ fork-flip list, Falco/Tetragon/Kata-agent-policy
/gVisor exporter-placement precedents, interior tripwire event-class
enumeration); (b) VMM-side visibility (KVM binary stats fd + exit-mix
inference, host-observed truth via VMM-process cgroup/schedstat/RSS,
Firecracker per-device metrics taxonomy, libkrun.h API scan for any
stats surface — expected NONE ⇒ fork-roadmap receipt, virtio-balloon
guest-stats trust wording, CloudWatch hypervisor-vs-guest-agent split,
lie-detector table guest-claim ↔ host-proxy); (c) conduct detection
math (Axelsson base-rate fallacy, Lucas Poisson CUSUM, Gan/Vardeman-Ray
TBE/exponential CUSUM, Bernoulli CUSUM, g-charts, integer-ARL
discreteness caveats, Forrest sense-of-self + Wagner-Soto mimicry
caveat, Ye EWMA-on-audit, Falco/GuardDuty/EDR pattern⇒quarantine
response precedent, Anthropic agentic-misalignment + Apollo scheming
measured rates as base-rate priors, benign-trip rates). On landing:
design the interior coverage + conduct path, fold into MONITORING
(§3/§5/§6 + new §) + HANDOFF (§1 metric family + §4 phenomenon row +
§6 runbook line + §7 Guardian line) + PODS §1/§3/§6 amendments +
re-present. All three §2-ruling-agnostic.

**BRANCH OPENED THEN PARKED (2026-08-19): THE RESPONSE AUTHORITY CHAIN
— UNDESIGNED, requirements recorded.** User directive (verbatim-close):
warden/sensor must be able to reach an EXTERNAL agent that can
restart/block/cordon/etc. a malignant VM — the Guardian takes informed
action, BUT "this side of functionality ultimately needs to respect
human, end-user configuration and specifications": users set the
runbook parameters; the Guardian respects and automates them, adjusting
for deployment shape/scale/environment like an experienced SRE. Worked
requirements given: user block-list of processes / external resources ⇒
must clearly respect; user max-vCPU threshold per pod ⇒ maintain and
enforce with discretion; user policy "pods running well-known malignant
processes are cordoned and isolated, NOT killed" ⇒ respected (the
malignant-process DATA sourcing = commissioned research). Refinements
(same exchange): Guardian also provides sensible defaults
(environment/scale-relevant) for inexperienced users, with proper APIs
always exposed for professionals to specify exactly; the user may also
specify KILL outright, or "AUTO" (= Guardian discretion). STATUS: NONE
of this machinery is defined, designed, or researched (user correction
recorded: "We haven't defined any of this machinery or researched it
yet" — I overstated by presenting authoring semantics as adopted; the
explicit/unset-derived-default/auto three-state framing is a CANDIDATE
to test against receipts, nothing more). SEQUENCING (user): "we need to
round out the Scribe/observability/handoff work first" — this branch
PARKS until that arc completes. Lane D research (response-verb
mechanics: cgroup.freeze/KVM-freeze caveats/clock-jump, cpu.max live
adjust + steal time, K8s cordon naming, IR memory-forensics receipt for
the documented-non-goal; user-parameter precedent: GuardDuty user
threat lists, K8s LimitRange defaults, Gatekeeper template-vs-parameter,
Falco overrides, systemd resource directives→cgroup/BPF; threat-intel
sourcing: STIX/TAXII/MISP, abuse.ch, OSV MAL- entries, NSRL known-good,
Falco miner/reverse-shell rules, GuardDuty CryptoCurrency findings,
MITRE T1496 layering) is IN FLIGHT and lands onto this parked record.
Two observations logged for the future design, status = untested
hypotheses: cordon=sever+freeze+keep-resident is compatible with PODS
crit-10 (no guest-memory persistence — the resident pod is the
forensic artifact); PODS §1 fixed-at-summon vs live ceilings resolves
host-side (VMM is a host process; its host cgroup is the
throttle/freeze point; guest sees steal time, never topology change).
NEXT (user): re-present the Scribe/observability/handoff planning
documents (MONITORING + HANDOFF as last presented, §5 channel
included), work from there; the three in-flight arc lanes (interior
observability / VMM visibility / conduct math) fold in on landing.

**CONDITIONAL ACCEPTANCE (2026-08-19): MONITORING + HANDOFF.** Both
documents re-presented in full with the four confirmed gaps carried as
explicit pending-amendment markers (MONITORING crit-14 / HANDOFF
crit-13: amendments land BEFORE files are written). User verdict:
"let's wait for the research regarding the warden/sensor metrics to
return, incorporate that, and then this is accepted." = ACCEPTED
conditional on incorporating the three arc lanes (interior enforcement
observability af03…, VMM-side visibility a09c…, conduct detection math
a7a8…). On landing: record each dossier, compose the interior-coverage
+ conduct-family design, present the incorporated sections in-message,
then write docs/specs/MONITORING.md + docs/specs/HANDOFF.md + the
corpus amendments (MONITORING crit-15 list incl. PODS §1/§3/§6) in one
change; update GAPS (closes D-5/Branch 14) + this tree. FLAG STILL
OPEN: the §2 ruling (Design A containers-per-loop [recommended] vs
Design B shared-runtime) — the accepted document cannot carry "THE
OPEN RULING" to disk; needs the user's explicit call at incorporation.
Parked separately: response-authority branch + its lane D (adbe…).

**§2 RULED + BOTH SPECS ACCEPTED (2026-08-19).** User, three points
verbatim-close: (1) "Containers-per-loop -> I assume this means the
containers in microvm" — CONFIRMED, meaning fixed: one libkrun microVM
per primary agent; inside it one OCI container PER AGENT LOOP (primary
loop + Scribe loop = two containers per pod), spawned/supervised by
hecate-init as PID 1; "loop" = agent loop, never per-turn. (2)
"accepted" = the §2 ruling: **DESIGN A — CONTAINERS-PER-LOOP —
ACCEPTED**, superseding the previously-accepted shared-runtime model
(Design B kept in the spec as the documented alternative + §5.9
degeneration note); the NO-PRECEDENT assembly (hecate-init container
spawner on the libkrunfw-lineage kernel) is now in-scope build work,
carried as spec text with its caveats (no-LSM baseline, OOM sizing
invariant, upper-never-on-virtiofs). (3) "accepted" = MONITORING +
HANDOFF acceptance re-affirmed; the incorporation condition stands
(three warden/sensor lanes fold in before files are written; MONITORING
crit-14 / HANDOFF crit-13). At write time the §2 section converts from
"OPEN RULING" to "RULED: Design A (2026-08-19)" with B as the recorded
alternative; corpus amendments include the previously-documented
shared-runtime tradeoff revision (the crit-15 "if Design A" item).
REMAINING before write: the three arc lanes land → dossiers recorded →
interior-coverage + conduct designs composed → incorporated sections
presented → both files + amendments in one change → GAPS closes
D-5/Branch 14.

**SCOPE DIRECTIVE (2026-08-19, user): FULL CORPUS RECONCILIATION.**
"you will need to update NUMEROUS other docs - our microvm docs, how we
summon, etc. This means you'll need to examine each relevant doc after
determining the relevant docs, modify the design to incorporate these
changes, and re-present for acceptance after conflict and gap
analysis." = the IAM-reconciler diligence pattern applied to this
acceptance. Corpus enumerated from the tree: 26 specs (docs/specs/) + 5
architecture docs (AGENTS, LEDGER, PLATFORM, SKILLS, SUMMONING) +
CONTEXT.md + 5 ADRs + GAPS.md. Reconcilers dispatched over the whole
corpus (5 lanes by affinity: pods/lifecycle, runtime/agents,
protocol/security/health, planes/knowledge/ledger, root docs) against a
written statement of the accepted design; each returns per-doc
CONFLICT (verbatim+line+proposed amendment) / GAP / NO-CHANGE (explicit
clean list) + pending-amendment interaction sites. Re-present after
conflict+gap analysis; acceptance precedes any file write.

**ARC LANE B LANDED (2026-08-19): VMM-SIDE VISIBILITY (host-observed
truth).** KVM_GET_STATS_FD (api.rst 4.133) = a PRODUCTION telemetry
surface by design (commit fdc09ddd: "lightweight… lock-free solution
for user space telemetry applications… pulling frequency could be as
high as a few times per second"; "reading workload can be handed over
to other unprivileged process" — warden-side collector needs no
privilege once it holds the fd). Stat inventory receipted:
halt_exits/halt_wait_ns/blocking + exits/io_exits/mmio_exits/
hypercalls/insn_emulation… (kvm_types.h + x86.c descriptor array).
Idle-vs-spin inference grounded (halt-polling.rst: idle guests cede via
HLT): claimed-idle + no halt exits + full vCPU thread runtime =
SPINNING. Backend symmetry: WHP WHvGetVirtualProcessorCounters
(HaltInstructions + TotalRuntime100ns + intercept/event/APIC counter
structs verbatim) ≅ KVM; HVF has NO counters API (grep-receipted from
shipped SDK header) BUT every exit is delivered synchronously in
hv_vcpu_exit_t ⇒ the fork self-counts (Firecracker's own model). HOST
TRUTH SURFACES: /proc/<pid>/schedstat (cpu-time/runqueue-wait/
timeslices), VMM-cgroup cpu.stat usage_usec = unfakeable guest burn,
smaps_rollup/RssAnon = true faulted footprint, steal-time MSR ("time in
which this vCPU did not run… idle will not be reported as steal") =
host-manufactured truth the guest reads — starvation claims verifiable
from BOTH sides host-owned = the cleanest lie-detector row.
FIRECRACKER = THE minimal-VMM metrics precedent: formal per-device
metric families (vcpu/vsock/net/block/…); vsock metrics complete
(rx/tx_bytes/packets, conns_added/killed, queue events); vsock.md
verbatim: guest connect to a port with no host listener ⇒ VMM-authored
RST — every attempt COUNTABLE per port; net tx_spoofed_mac_count = the
existing precedent for "the VMM counts guest lies at the device
boundary". CloudHypervisor /vm.counters; QEMU query-stats re-exports
the KVM stats fd. virtio-fs: spec-verbatim the DEVICE (=VMM) "acts as
the FUSE file system daemon" ⇒ the whole op stream is host-owned
pre-effect by construction; but NO existing virtio-fs daemon exposes a
formal op-metrics API (virtiofsd = log-only; NO-PRECEDENT — fork is
first-party). **libkrun: ZERO stats/metrics/counter functions in the
entire public API** (include/libkrun.h fully enumerated; runtime
signals = shutdown eventfd + pause/resume only) — the gap receipted
precisely; fork adds Firecracker-shaped device counters + stats-fd
collector, DAX-style tracked fork work. RECONCILIATION PRECEDENT:
virtio-balloon = guest stats OPTIONAL ("driver chooses which ones to
supply") + QEMU host-stamped last-update ("a buggy guest can't
influence its value") = THE micro-pattern: host-authoritative ENVELOPE
(freshness/liveness) around guest-authoritative CONTENT — exactly the
provenance discipline for sensor reports. Industry codifies the
visibility split: AWS CPUUtilization = hypervisor-level (guest tools
"can show a different percentage"), memory metrics REQUIRE the in-guest
agent (GCP verbatim same). Cross-view validation = the NAMED principle
(GhostBuster coined cross-view diff; Lycosid verbatim trusted-view/
untrusted-view + statistical inference to trade time for accuracy;
Antfarm: VMM infers guest process activity implicitly, 2.5% worst-case
overhead; LibVMI production tooling) — THIN as a continuous
telemetry-reconciliation standard (scattered practice, no named
standard; composed for Hecate as design). LIE-DETECTOR TABLE delivered,
7 rows [R]/[C]-tagged: idle/spin (host-authoritative), memory
(split-authority: host owns footprint+freshness, guest owns semantics),
hidden-process (cross-view, trusted-view-authoritative), stream
liveness (device counters self-refute under-reporting), actor
attribution (guest-authoritative-WITH-HOST-VETO via boundary signature
— capability-set physics), starvation (host-manufactured, cleanest),
boundary probing (host-authoritative: the guest cannot suppress the
host's count of its own refused attempts). 2 arc lanes still out:
interior observability (af03…), conduct math (a7a8…).

**ARC LANE A LANDED (2026-08-19): INTERIOR ENFORCEMENT OBSERVABILITY.**
SECCOMP DENIALS: RET_ERRNO is SILENT by design (VINDICATES gap 1 — no
log, no counter); the kernel keeps NO per-process/per-cgroup seccomp
denial counter anywhere (proc_pid_status has only mode+filter-count;
cgroup-v2.rst grep seccomp=0 — NO-PRECEDENT). Three routes to COUNT a
denial: (a) SECCOMP_RET_USER_NOTIF listener fd — deny-only (never
FLAG_CONTINUE, never deref target memory) has NO TOCTOU window (the
man page's "can not be used to implement a security policy" applies to
CONTINUE, not to deny+count), supervisor-death ⇒ ENOSYS fail-closed;
cost HIGH (target sleeps + cross-process round trip per event) ⇒ only
if denials rare-by-design. (b) RET_ERRNO + SECCOMP_FILTER_FLAG_LOG +
actions_logged + CONFIG_AUDIT(SYSCALL) ⇒ audit record; no auditd ⇒
ratelimited pr_notice type=1326 in kernel log (LOSSY as a counter).
(c) cgroup-BPF (below). RET_LOG is log-AND-EXECUTE (cannot be the deny
primitive). BPF LSM: observe-and-deny in one hook ("Return an -EPERM or
write information to the perf events buffer"); needs CONFIG_SECURITY +
BPF_LSM + BPF_EVENTS→FTRACE chain (all fork flips). **BPF_CGROUP_UNIX_*
landed in 6.7** (uapi diff 6.6=0/6.7=5; commit 859051dd); libkrunfw =
6.12.91 ⇒ source present; **CONFIG_CGROUP_BPF=y on STOCK BOTH ARCHES**
(+ BPF=y + BPF_SYSCALL=y) ⇒ **my MONITORING §5.8 tripwire assumption is
VINDICATED — cgroup-attached UNIX connect/sendmsg interception works on
stock**, program returns 0 ⇒ caller EPERM (kernel/bpf/cgroup.c), emits
ringbuf record + bpf_get_current_cgroup_id (base helper, no tracing
config) = per-container attribution for free. BUT BPF_JIT is OFF stock
(interpreter only — a perf fork-flip). CGROUP v2 EVENT SURFACES (the
per-container interior metrics, mostly FREE + KERNEL-PUSHED via
poll/inotify on file-modified): memory.events{low,high,max,oom,
oom_kill,oom_group_kill,sock_throttled}(+.local), pids.events{max},
cgroup.events{populated,frozen} — all pushed; cpu.stat{nr_throttled,
throttled_usec} POLLED-only; PSI cpu/memory/io.pressure = kernel-
evaluated trigger fds (poll/epoll, ≤1/window). **CONFIG ASYMMETRY (the
fork must harmonize): x86_64 has AUDIT+SECURITY but NO PSI; aarch64 has
PSI-on-by-default but NO AUDIT and NO CONFIG_SECURITY AT ALL (no LSM
layer whatsoever).** FORK-FLIP LIST (explicit, DAX-style tracked): (1)
BPF_JIT=y both; (2) SECURITY+SECURITYFS=y aarch64; (3) BPF_LSM stack
both (drags BPF_EVENTS→FTRACE/KPROBE_EVENTS, + lsm=…,bpf boot/CONFIG_
LSM); (4) DEBUG_INFO_BTF=y both (CO-RE/LSM attach — THIN on kernel-doc,
CONFIRMED by Falco/Tetragon requiring BTF); (5) PSI=y x86_64; (6)
AUDIT+AUDITSYSCALL=y aarch64 IF the seccomp-audit route is chosen; (7)
optional KPROBES, IKCONFIG(+_PROC for in-guest /proc/config.gz kernel
attestation); (8) raw-syscall tracepoint telemetry needs #3's chain.
On stock TODAY (no flips): seccomp+unotify, full cgroup-event surface
(minus PSI-on-x86), cgroup-BPF UNIX interception+ringbuf+cgroup-id.
Fork-flip unlocks: BPF LSM hooks (ptrace_access_check=cross-container
ptrace/proc-mem-read; task_kill=cross-container signal; bprm_check/
file_open=exec+sensitive-open — hot, must in-kernel-filter), raw-
syscall-rate telemetry. EXPORTER PLACEMENT (settles gap 2): in EVERY
shipped system (Falco DaemonSet, Tetragon agent, gVisor unsandboxed
sidecar, Kata) the kernel-telemetry drainer is a DEDICATED SUPERVISED
process — **PID 1 as BPF-ring drainer = NO-PRECEDENT**; nearest is
kata-agent-as-init which drains its own ttRPC/policy, NOT kernel rings.
bpf_link PINNING (bpffs) is the tool that lets ENFORCEMENT survive the
drainer's death (default fd-owned links detach on owner exit) ⇒ the
shipped pattern is "PIN enforcement, SUPERVISE the drainer" — so
interior enforcement (seccomp/BPF/cgroup residuals) is installed+pinned
by hecate-init pre-spawn, and a DEDICATED in-guest sensor-exporter
process (supervised by hecate-init, NOT init itself) drains the rings
to the sensor vsock channel. Ringbuf drainer-death = records persist
until ring fills, then reserve fails/no blocking (drops counted, never
blocks the workload). KATA AGENT POLICY = the "policy compiled OUTSIDE,
installed at spawn (rootfs or base64 pod-creation annotation), enforced
INSIDE by the agent" precedent — VINDICATES the warden-compiled-
residual hypothesis (IAM §6 compile-and-distribute extends one hop into
the guest). Event-class table delivered (12 rows, each surface +
push/poll + cost + stock-vs-flip).

**ARC LANE C LANDED (2026-08-19): CONDUCT DETECTION MATH.** Axelsson
base-rate fallacy (TISSEC 2000, PDF-verbatim): "the false alarm rate is
the limiting factor"; at P(I)=2e-5 "the factor governing the detection
rate … is completely dominated by the factor … governing the false
alarm rate" — and he DERIVES the requirement from a human alarm budget
("the SSO, being only human, can only react to a relatively low number
of alarms"; "100 false alarms per day … met by a false alarm rate of
1e-5") = the EXACT δ→threshold / ARL₀=T/δ shape Hecate already uses,
now source-licensed for conduct streams: at conduct base rates, δ (not
detection power) is what makes an alarm mean anything. PER-STREAM
STATISTIC ASSIGNMENT (composed, premises receipted): (1) warden policy
denials = per-op OPPORTUNITY stream ⇒ **risk-adjusted Bernoulli CUSUM**
(Reynolds&Stoumbos 1999: per-item Bernoulli CUSUM "detect changes in p
substantially faster than … grouping items into samples"; binned charts
useless at low rates — Szarka&Woodall) with the **Steiner risk weight**
(Biostatistics 2000: standard CUSUM "may signal as a result of changes
in the referral pattern … rather than … a change in the actual …
performance" — replace patient→op, referral-pattern→task-mix = the
Hecate confounder verbatim); (2) tripwire firings / escalations = sparse
timed events (often zero/session) ⇒ **TBE exponential CUSUM** on
inter-arrival times (Gan 1994 / Vardeman&Ray 1985 "controlling the
intensity of a Poisson process"; = geometric ops-between-trips CUSUM,
same statistic by R&S equivalence) or **Poisson CUSUM** (Lucas 1985,
k-from-two-means + FIR) for window-aggregated counts; (3) sensor
behavioral aggregates ⇒ **EWMA intensity** (Ye 2002/2003 EWMA on
audit-event intensity — feeds the EXISTING residual-EWMA stack, no new
mechanism). δ ON DISCRETE STREAMS: threshold via Markov-chain/Monte-
Carlo run-length (Brook&Evans; JSS 70(10) verbatim "chose a value of 2
for h so that the probability of a false alarm within the 56 timepoints
… is less than 0.1") = a BOUND statement at the achieved discrete h
(exact-equality designs exist only at sparse points — Rossi 1999);
report achieved P alongside δ. FIR head-starts on REPLACEMENT/fresh
agents (Lucas/White&Keats) — a successor that resumes tripping is
caught fast (mirrors handoff FIR-seeding). SEVERITY: separate CATEGORY
(interior-boundary vs egress vs scope — different base rates, benign-
trip likelihoods, risk weights) from RATE; per-category charts (or one
categoricalCUSUM) with category-specific k/R; egress-category carries
higher out-of-control odds than scope-category; NEVER collapse to one
trip counter (hands benign noise to the hostile threshold). THE
REPLACEMENT LINE (production-standard, receipted): warden already
denied every op pre-effect ⇒ NO damage question ⇒ the detector alarm is
purely ACTOR-level ("pattern no longer consistent with learned in-
control profile ⇒ replace/escalate"). MDE attack-disruption states the
split verbatim: incident-level action "differs from … blocking based on
a single indicator of compromise"; GuardDuty "terminate … and replace
it with a new instance"; Falco-Talon ships terminate/cordon/drain/
networkpolicy actionners; MDE holds "99% or higher [precision] based on
real production data" + audit-mode-before-release + all-actions-undoable
= exactly the observe-mode-first + reversibility discipline. CONVERSELY
a SINGLE confirmed-hostile act = Guardian HARD-BLOCK (enforcement, not
detection — routing it through a CUSUM only adds latency + a false-
negative channel; Wagner&Soto mimicry: pattern detectors are EVADABLE
so the hard line must NOT depend on them). BASE RATES (priors for the
learned layer): measurable + nonzero but swing orders of magnitude with
framing (Anthropic agentic-misalignment 96/96/80/79% blackmail under
adversarial framing vs 55.1% "real" vs 6.5% "eval"; Apollo scheming
0–15%/model/action; METR o3 reward-hacking 1–2% of task attempts) ⇒
universal thresholds statistically INCOHERENT ⇒ learned per-(agent-type,
task-class) λ₀/p₀ + Steiner weighting, MANDATORY. Benign boundary-brush
is real (o1-preview Docker-API "benign … systems administration"
reward-hack; Claude Code sandboxing "84% fewer permission prompts" =
how often benign work brushes boundaries) ⇒ the risk weight is
load-bearing, not decorative. ALL THREE ARC LANES NOW LANDED. Corpus
reconcilers (5 lanes) still in flight.

**LANE D LANDED (2026-08-19): RESPONSE VERBS + USER-PARAMETER PRECEDENT
+ THREAT-INTEL SOURCING — lands onto the PARKED response-authority
branch (NO design work now; user sequencing: rounds out Scribe/
observability/handoff first).** RESPONSE VERBS (each cgroup/kernel-
receipted, reversibility-classed): FREEZE = write 1 to the pod-VMM
cgroup's `cgroup.freeze`; completion signaled via cgroup.events
"frozen"; v2 freezer = jobctl-stop-like, NOT observable from inside
(v1 doc design intent: kernel freezer "prevent[s] the freeze/unfreeze
cycle from becoming visible"; SIGSTOP/CONT ARE visible ⇒ freezer is
strictly better), frozen tasks still KILLABLE + ptrace-inspectable
(read registers) = evidence preservation WITHOUT execution or memory
persistence; CAVEAT — freezing the VMM cgroup pauses vCPU threads
without KVM's knowledge ⇒ kvmclock jump + spurious guest soft-lockup
on thaw UNLESS the fork issues KVM_KVMCLOCK_CTRL per vCPU pre-freeze
(sets the pvclock "paused" bit the guest watchdog checks — api.rst
§4.70 + timekeeping.rst §4.6 receipted; the composite is THIN/
fork-work). THROTTLE = live writes to cpu.max/memory.high(soft-reclaim,
never-OOM)/io.max on the running VMM cgroup — enact-on-write, bite
within one CFS period (~100ms); memory.high doc literally briefs the
warden ("an external process monitors the limited cgroup"); guest sees
only STEAL TIME, topology unchanged (resolves the PODS §1
fixed-at-summon tension exactly as hypothesized). SEVER = warden
refuses new flows at the egress gate (NetworkPolicy egress-isolation +
AWS isolation-SG precedent — CAVEAT: AWS "existing tracked connections
won't be terminated… only future traffic" ⇒ Hecate must NAME whether
SEVER kills established flows; the per-flow gate CAN, unlike an SG).
CORDON = SEVER + FREEZE + keep-resident; naming precedent kubectl
cordon "Mark node as unschedulable" (≠ kill; uncordon reverses);
Hecate cordon also = scheduler stops routing new work/claims while
resident-for-inspection (cordon=no-new-work vs drain=evacuate = two
knobs). RESTART = teardown + fresh summon from the content-addressed
manifest rootfs (return to a VERIFIED state — stronger than K8s
image-by-reference restart). KILL = `cgroup.kill` (SIGKILL whole
subtree, fork-race-safe) — two grades in precedent, both need names:
evict (graceful, respects in-flight commit — honors the
pipeline-lifecycle-vs-disk-commit law) vs fail (immediate, 0-grace).
INTERIOR-BLOCK = update the user-parameter objects so the NEXT
admission/exec/flow decision differs (ResourceQuota "changes… will not
affect already created resources" = prospective-by-default; explicit
verbs above do retro-application). SNAPSHOT-FOR-FORENSICS = DELIBERATELY
NOT offered for guest memory (PODS crit-10): practice captures memory
FIRST (RFC 3227 order-of-volatility; AWS "PRIOR TO isolation/shutdown")
— Hecate substitutes FREEZE-and-hold (inspectable-not-running) + the
COMPLETE host-side per-flow effect record (RFC 3227's "remote logging"
class, complete because the warden gates every crossing) + admission-
time content hashes (disk-evidence equivalent). USER-PARAMETER
SUPREMACY (the "human sets policy, automation executes within"
precedent set): GuardDuty user threat/trusted lists = THE exact shape
("stop generating findings from your trusted sources and generate
findings for known malicious sources from your threat lists"; TRUSTED
BEATS THREAT on collision = user-suppression precedence; formats incl.
SHA-256 + STIX; bounded slots 1 trusted/6 threat; edit ⇒ re-activate,
≤15min propagation — the disclosed-bound pattern); K8s LimitRange/
ResourceQuota (user ceilings, platform-enforced, prospective);
ValidatingAdmissionPolicy triad (policy-logic / paramKind / binding) +
Gatekeeper ConstraintTemplate(logic+schema)-vs-Constraint(instance) =
the TEMPLATE-VS-PARAMETER split, formalized; Falco override
append/replace + author-bounded exceptions ("the author of the rule
defines what construes a valid exception"; upstream ships NO exceptions
= adopter fills tuples); SRE SLOs→alert rules + quantified overload
goals ("paging events per shift < 2") + Rundeck runbook-automation
("self-service access to the processes"); systemd resource-control =
config lines compiling to kernel enforcement (CPUQuota=→cpu.max,
MemoryHigh=main/MemoryMax=last-line, IPAddressDeny=→cgroup-BPF firewall
with allow-over-deny ordering) = the "user directive → compiled
residual" precedent in a shipped init. THREE PARAMETER-AUTHORING STATES
(candidate from prior exchange, now precedent-backed): EXPLICIT
(binding) / UNSET (platform-derived default — constants-from-anchors) /
AUTO (delegated verb choice); Guardian discretion = choose among
USER-PERMITTED verbs + timing, NEVER invent a verb (ASR "only when
initiated by you… or when automated remediation has been enabled";
MDE actions all-undoable + audit-mode-first = observe-mode-first +
reversibility). THREAT-INTEL SOURCING: STIX 2.1 indicator (pattern
lang, SHA-256 example verbatim) + TAXII 2.1 transport (collections,
`added_after` delta cursor, HTTP-Basic-over-TLS-1.2-MUST, 0-RTT
forbidden; NO content-signing in the spec = NO-PRECEDENT) / MISP core
format alt; feeds: abuse.ch family (MalwareBazaar hashes / ThreatFox
IOCs / URLhaus / SSLBL cert+JA3 — free Auth-Key, hourly/daily batches;
CC0 NO LONGER asserted on current pages), OSV MAL- malicious-packages
(Apache-2.0, the coding-agent-specific supply-chain vector) + GitHub
Advisory type:malware + npm-placeholder/PyPI-quarantine, Spamhaus DROP
(IP ranges, daily, SBL-removal auto-propagates = FP governance), NSRL
= known-TRACEABLE not known-good (includes hacking tools — allowlist
caveat), Team Cymru MHR (free known-bad hash lookup) vs VirusTotal
public (500/day + "must not be used in commercial products" = legally
excluded from the product). MATCHING LAYERS (MITRE T1496 + Falco
verbatim honesty): NAME/cmdline "can generally be bypassed quite
easily" (cheap first layer, not the control) < HASH (admission-time
over the content-addressed rootfs manifest — image binaries hash-known
BEFORE boot; tmpfs-built/downloaded binaries = the only exec-time
hash-unknown class) < DESTINATION/behavior (mining-pool ports/domains,
SSLBL JA3, Stratum cmdline, fd-dup-to-socket reverse shell) at the
egress boundary Hecate already gates per-flow = the layer that survives
renames. Falco→Talon ships terminate/cordon/drain/networkpolicy
actionners = the response-verb set as deployed code; GuardDuty
CryptoCurrency findings (BitcoinTool.B vs .B!DNS = flow-vs-DNS naming).
STATUS: recorded on the parked branch; design deferred to after the
Scribe/observability/handoff arc writes. Response-verb table +
parameter-object families (block-lists / ceilings / phenomenon→action
maps / feed-subscriptions, template-vs-parameter) + intel-ingestion
shape all delivered as composed synthesis for that future design.

**RECONCILER R1 LANDED (2026-08-19): PODS/LIFECYCLE set (PODS,
SUMMONING, AUTOSCALING, VFS, TRANSFER, SERVING, PLATFORM).** Totals
15 CONFLICT / 38 GAP / 8 PENDING-SITE / 0 STALE-REF / 2 OPEN-QUESTION /
1 NO-CHANGE. TRANSFER = clean (transport-only, anatomy-agnostic).
Epicenter PODS: 8 conflicts — §1 pod-def "running one agent" (→ primary
+ Scribe, 2 containers, N+1 census, one-way ring, no shared netns/vol);
§3 init "exhaustive five-duty" contract must be RE-STATED still-
exhaustive (duty 3 "the agent runtime process" singular wrong — add
mint-channel-then-spawn-two, install warden-compiled residuals
pre-spawn, scribe-first start, supervise-both, tail-drain-hold,
flush-gated teardown); §3 "Two vsock channels" WRONG COUNT (control +
agent + Scribe-flow + sensor, all guest↔host); §3 trust-posture
conflates Bar A/B (container interior contains at Bar A; only Bar B
owns init's space); §6 "in-guest actions ungated as calls" needs the
two-workload qualification (residuals gate in-kernel, zero round-trip);
§7 crash bullet ("Scribe drives replacement") WRONG when the VM itself
dies — Scribe dies with it ⇒ colocation-unit checkpointed substrate +
health plane drive replacement, successor brief = last flushed window;
crit-2 pins the superseded five-duty count. New tests T20–T24 (Scribe
respawn/tail-drain/channel-tamper/interior-residuals/census). VFS:
6 gaps (two container rootfs subtrees as RO lowerdirs; upper-on-tmpfs-
never-virtiofs law per container; work volume mounts PRIMARY container
ONLY — Scribe attachment-free by law; V12 intra-pod isolation test).
SERVING: container-upper writes never reach the machine (tmpfs) —
strengthens AC-1. PLATFORM: §4 "cannot outright block" NOW WRONG
(Guardian CAN deny — fresh-probe fail ⇒ task-hard ⇒ deny); §6 "derived
on demand" contradicts the pushed single-writer architecture (RANK/
LEDGER_CORE already document the push — PLATFORM the lone laggard);
§5 consumers row hands Guardian continuous conduct analysis (→ detection
substrate analyzes, Scribe judges, Guardian adjudicates). **TWO
LOAD-BEARING OPEN-QUESTIONS (need user ruling; several amendment texts
depend on them):** OQ1 — do pooled/snapshot GENERIC VMs pre-stage the
two containers, or create-at-assignment? current text implies create-
at-assignment (pools "generic", bundle "attaches at assignment");
options (a) both created+started at assignment [T7 trivially clean;
spawn cost inside the "ms" assignment budget], (b) pre-create at
pool-fill identity-free + start at assignment [faster ready; T7 scan +
snapshot-genericity proof + reseed-before-container-start must extend to
container FS], (c) hybrid: Scribe (role-independent) pre-created,
primary at assignment. OQ2 — the primary's "agent" channel under the
new seccomp socket(AF_VSOCK)⇒EPERM: (a) stays vsock, fd PRE-CONNECTED by
init + passed at spawn (EPERM blocks only NEW socket() creation, not an
inherited fd — the Scribe pattern), or (b) agent traffic is
virtio-net-ONLY per SUMMONING §63/§83 and the PODS agent-vsock row is
superseded — this surfaces a PRE-EXISTING PODS↔SUMMONING disagreement
(PODS calls agent-channel vsock; SUMMONING says claims/MCP ride the
virtual network) that the seccomp rule forces to a decision.

**RECONCILER R5 LANDED (2026-08-19): ROOT/ADR/GAPS set (CONTEXT, ADR
0001–0005, GAPS).** CONTEXT: 3 CONFLICT (Pod def; Scribe def = retire
"sidecar"/"monitors performance"/keep "requests" perf-handoff; colo-
unit service list += score service + detection substrate), + 6 NEW
GLOSSARY ENTRIES owed (History channel, Runtime emitter [names the §4c
law's subject so per-turn language can't regrow], hecate-init,
Detection substrate, Score service, Provenance class) + 2 candidates
(drained, Runbook); office-naming OQ ("sidecar narrator" → "companion
narrator"?, recommend rename). **ADR RECOMMENDATION (adopt): AMEND
ADR-0001 Consequences** (same fork decision, GROWN scope — hecate-init
replaces libkrun init via 2.0 seam + embeds spawner; guest-kernel
config fork-owned; VMM grows first-party stats surface, upstream exports
ZERO; dated-amendment house style per ADR-0005) + **WRITE NEW ADR-0006
"Two-container pod interior / one OCI container per agent loop"** —
passes all three ADR tests (hard-to-reverse: reshapes init contract/
channel supervision/lifecycle ordering/census/Σmemory.max admission/
interior seccomp+cgroup; surprising: SUPERSEDES accepted Design B +
revises the corpus-wide "VM boundary is the only inter-agent isolation"
reading — two agents share a guest at Bar A; real tradeoff: Design B
lower-overhead/weaker-attribution is a live tombstoned alternative);
ADR-0006 becomes the citation target for CONTEXT Pod + ADR-0001
amendment. ADR-0001 also: "OS sandboxes kept only as degraded mode" NOW
FALSE (seccomp/cgroup/ns are interior default at Bar A) — scope to
"world-facing boundary only in degraded mode; interior compartment-
alization is default"; STALE-REF "virtio-fs workspace"→"volumes"
(C-5c sweep missed this ADR). ADR-0002/0003/0005 = NO-CHANGE (0002 has
a PRE-EXISTING out-of-scope TCP-headline staleness, D-10 territory, not
ours). ADR-0004 "single binary" = GAP not conflict: literally true
(whole VM in one HOST process; guest hecate-init+2×hecate-rt are guest-
kernel, not host) but AMBIGUOUS — scope the claim host-side; 2 OQs
(init binary identity: one-binary-argv0 / separate / --init-mode-of-rt;
guest-image distribution embedded-in-binary vs side-shipped). GAPS
(two-phase per its own C-7 header-authority rule): PHASE-1-NOW — D-5 row
CONFLICT (says "spec is what remains owed" → ACCEPTED-2026-08-19
conditional-on-§11, closes-on-write); Branch 39 (observability plane)
supplied → moves out of undesigned on write (Branch-44 pattern; residual
= §11b exporter + Branch 17 dashboards); NEW rows: pending-amendments
tracker (§11a–e, all block write), parked response-authority-branch
charter row, companion-amendments block; §8 libkrun-fork row expand
(+init-seam +fork-owned-kernel-config +stats-surface); provider-gateway
"fold into Branch 14" option EXPIRED (accepted w/o absorbing it; design
DEPENDS on gateway for provider-authoritative context accounting); §0
"nine ACCEPTED" already-stale→count-free. PHASE-2-AT-WRITE — add
MONITORING/HANDOFF §1 inventory rows (C-7: no row without header),
header counts 20→22 specs +ADR-0006, §9 step-5 strike D-5, C-10 += 
ADR-0006 candidate. **DESIGN-B SHARED-RUNTIME TRADEOFF TEXT LOCATED
(statement §12 dangling item RESOLVED): it lives in GRILLING.md itself
(~3767–3838, 4257–4361, 5013–5035), NOT in any spec — so the "revise
Design B tradeoff" companion amendment = the not-yet-written MONITORING
spec CARRIES it as the tombstoned alternative + §5.9 degeneration, no
existing-spec edit.** §4c-BANNED PER-TURN LANGUAGE LOCATED:
AGENTS_RUNTIME.md:127 "Scribe feed emitted after every turn; narration
flush is part of drain." (acceptance criterion 5) — in the still-out
runtime/agents reconciler's set (a041). R1+R5 done; 3 reconcilers still
out: runtime/agents (a041), protocol/security/health (a4cda), planes/
ledger/knowledge (a773).

**RECONCILER R2 LANDED (2026-08-19): RUNTIME/AGENTS set (RUNTIME,
AGENTS_RUNTIME, AGENTS, REGISTRY, SKILLS_API, SKILLS, SESSIONS).**
RUNTIME = 0 conflict (placement-agnostic; Design-B text NOT here) but
GAP: shard-count "N from available cores" would give 2N in a two-process
guest ⇒ each hecate-rt's shard count is bundle-declared w/ derivation
(primary N-from-cores; Scribe clamped to 1 = single-ingestion-thread
design), census N+1 not 2N. AGENTS_RUNTIME = 5 CONFLICT incl. **the
corpus's ONLY literal "Scribe feed emitted after every turn"
(AGENTS_RUNTIME:127, acceptance criterion 5)** → runtime-emits-below-
model + teardown-gates-on-Scribe-flush; also :4-7 (singular in-guest
process + "Scribe feed" duty + "single shard" — all wrong: 2 hecate-rt
processes, history EMITTER not feed, primary N shards); :95-96
"flush narration" at drain (primary has no narration/no Scribe path);
:21-23 "one pod's mind" (a pod now = two minds); :48-50 TS/Py exec
in-pod CONTRADICTS accepted SKILLS_API no-interpreter law; §6 handoff
seq missing 4 statement-§7 elements (drained force-close, key_epoch
re-bind, suppressed-testament-flush-at-resume, FIR-seed+tier-escalate).
AGENTS = 6 CONFLICT (pod anatomy+comms-exclusivity; Guardian "cannot
outright block" → CAN deny; perf-handoff mis-classed as soft-gate →
adjudication w/ deny; Scribe "monitors performance" → detection
substrate analyzes/Scribe judges; score "derived on demand" → pushed
single-writer; "sidecar" ×3 lines 5/32/311 → "companion"). **GLOSSARY-
WINS PRECEDENCE HAZARD (AGENTS:17-18 "glossary wins"): CONTEXT.md must
change in the SAME commit or the wrong Scribe/Guardian text stays
authoritative** (update-all-sites law). REGISTRY = 0 conflict; VERDICT:
warden/sensor correctly have NO AgentRole entries + must NOT gain them
(structural mechanism, not agents); GAPs: AgentRole needs scaling+
placement class (Scribe declares structural-1:1-companion so resolution
knows a primary's summon also resolves its companion); two-bundle pods
(primary + Scribe bundles, per-container warden residuals); runbooks =
ordinary Skill-kind home; "handoff re-resolves, nothing else" protected
(Scribe respawn-in-place ≠ handoff, re-creates from frozen bundle no
resolution). SKILLS.md = 2 CONFLICT (§4 executes TS/Py in-pod
CONTRADICTS accepted SKILLS_API — a PRE-EXISTING SKILLS↔SKILLS_API
conflict my change surfaces; Scribe capability parenthetical "anything
beyond narration" → += history serving + runbook skills). SKILLS_API =
clean, runbooks fit the declared-skill model exactly. SESSIONS: "session
group" = per-session consensus group (CONSENSUS:16) ⇒ "colocation unit
per session group" parses cleanly; GAP: detection substrate + score
service need home in the colo-unit service list; NO-CHANGE on handoff-
custody axis. NEW OQs: (R2-OQ-a) where does the blocking rustls PROVIDER
POOL live under Design A? (a) host-side at the gateway chokepoint,
in-guest speaks hecate-wire over pre-connected fds [in-guest thread
claim dies] / (b) pre-connected egress fds keep TLS in-guest per
container — TIES TO R1-OQ2 (agent channel transport); (R2-OQ-b) who owns
the scaling-class enum: PODS table (today) or AgentRole descriptor
(canonical, doctrine favors one owner); (R2-OQ-c) fleet priors are
CROSS-session but the colo-unit is per-session — home = (a) versioned
logged artifacts in object-tier/registry referenced at boot / (b) a
meta-group service that publishes them; (R2-OQ-d) score-service pointer
target = PLATFORM §6 (let it absorb) or the new spec file directly.
DESIGN-B TEXT CONFIRMED at GRILLING.md:3736-3763 ONLY (needs
supersession marker; new home = PODS §1).

**RECONCILER R4 LANDED (2026-08-19): PLANES/LEDGER/KNOWLEDGE set
(LEDGER_CORE, LEDGER, RANK, SCHEDULER, CONSENSUS, MERGE, OBJECT_TIER,
WAL, FOREST, SIBYL, VECTOR_INDEX).** 3 CONFLICT / 14 GAP / 1 PENDING /
3 STALE-REF / 4 OQ / 4 NO-CHANGE (MERGE-substantive, WAL, SIBYL,
VECTOR_INDEX). **KEY GAP (task-mandated check): `drained` is ABSENT
from the canonical claim-status vocabulary (LEDGER §3: generated→…→
satisfied|validation_*), exists ONLY as a signal REASON (LEDGER:375
"drained|revoked|expired|superseded"); the handoff force-close law
(statement §7) REQUIRES it as a TERMINAL STATE** → add to LEDGER §3
diagram + LEDGER_CORE L1 sweep TOGETHER (cross-cutting-identifier law:
closed delta-action enum + IsTerminal affordance predicate + action↔
delta bijection all change in ONE commit). RANK = 2 CONFLICT: "nothing
touches the ledger" (RANK:70-71) + AC-4 now LITERALLY contradict the
push architecture (every core input is WAL-logged) → "writes no ledger
OBJECTS; its sole ledger-directed output = the modulation snapshot
pushed as an ordinary logged core input"; "Scribe triggers handoffs on
the same data" (RANK:56-59) stale → detection substrate detects, Scribe
judges, Guardian adjudicates; + GAP: RANK carries NO score-architecture
pointer → add MONITORING §6. **LEDGER STALE-REF (load-bearing ordering):
§8 "Outbox for projections" (LEDGER:335-338) was SUPERSEDED by
LEDGER_CORE's ACCEPTED no-outbox decision ("the log IS the outbox") —
must fix BEFORE adding the Scribe as a delta consumer, else the new
subscription inherits a DELETED mechanism** (a pre-existing internal
inconsistency my change surfaces; "narration intake" in that line also
predates the Scribe→Archivalist flush). LEDGER_CORE GAPs: Scribe = named
per-primary delta consumer (cursor-consumes its primary's claims/
testaments/verdicts onto its vsock flow — authority stream, never the
ring); score-service home pointer; accumulator suppressed across handoff
(no duplicate testimony). SCHEDULER GAPs: colo-unit membership += score
service + detection substrate (enter §6 gang-admission whole-unit fit);
two-container pod admission (requirement vector sums both containers +
init; Σ memory.max + init ≤ guest RAM enforced); boot/health validation
pair wording (both containers up IN ORDER, Scribe first). CONSENSUS GAP:
**the score service is a NEW named single-writer — UNCLASSIFIED today,
it FAILS the boot roster by CONSENSUS's own chokepoint law
(CONSENSUS:226-229 "an unclassified writer fails startup")** → classify
region-scope epoch, add to the Branch-27 audit list (+ detection-
substrate checkpoint writer). MERGE = NO-CHANGE substantive + minor
STALE-REF: "─ring─►" arrow (MERGE:292) collides w/ the newly-minted
"history ring" → relabel "host channel". OBJECT_TIER = 3 OQ: (R4-OQ-a)
home for fitted baseline artifacts ("versioned logged artifacts") —
durable-plane class list names none; options (a) new "monitoring
baselines" generation-shaped class / (b) registry content / (c) archives
[wrong: live inputs not cooled proof]; (R4-OQ-b) home for checkpointed
detector-suite state — same species as FOREST field checkpoint
(host-local, never replicated), both unhomed; options (a) node-local
pack cache-role never-GC-root re-derivable / (b) declared outside the
hierarchy like the mutable side — ONE ruling covers both; (R4-OQ-c)
teardown-gate archival rung for Scribe window flush + trajectory —
rung 2 sealed (node-local, dies w/ node) vs 3 placed (survives node —
death-handoff argues this) vs 4 referenced. FOREST = 1 CONFLICT: rank
inputs — FOREST computes prevalence/specificity/trust as FIELD
AGGREGATES + pushes to score service (FOREST:180-184), but statement §6
says the score service computes reputation from (ledger deltas + Scribe
snapshots) as ONE authoritative copy ⇒ field-computed factors = a
SECOND authoritative computation → field aggregates ADVISORY, score
service alone computes; OQ rider: OR amend the statement's stream
enumeration to admit field snapshots as a 3rd logged input class
(statement-side ruling; FOREST is PROVISIONALLY-DIRECTED so statement
controls today) + STALE-REF FOREST:220-222 "Branch 14 owns detection"
→ "MONITORING/HANDOFF (accepted) owns detection". WAL/SIBYL/
VECTOR_INDEX = NO-CHANGE verified. 4 of 5 reconcilers in; LAST OUT =
protocol/security/health (a4cda: PROTOCOL vsock-channel-model [critical
for R1-OQ2], WIRE_SECURITY two-identity keys, FAULTS, IAM Scribe-
principal/§7.12, HEALTH §3-triggers).

**RECONCILER R3 LANDED (2026-08-19): PROTOCOL/SECURITY/HEALTH set
(PROTOCOL, WIRE_FORMAT, WIRE_SECURITY, FAULTS, IAM, HEALTH). ALL 5
RECONCILERS NOW IN.** WIRE_FORMAT = NO-CHANGE (identity-free codec;
inline-vs-reference law fits content-free evidence bundles exactly).
**THE CENTRAL CROSS-CUTTING FINDING — IDENTITY GRANULARITY: the wire/
fault/authority corpus keys trust to the POD as the finest speaker, but
the design puts 2 agent principals + init + sensor in one pod and
observe-not-feed requires a compromised primary CANNOT forge as its
Scribe at Bar A. Fix = per-WORKLOAD flow keys + per-container fd custody
UNDER the one pod summon-mint root, and it MUST land together across 5
sites (PROTOCOL §2, WIRE_SECURITY §2/§3/§6, FAULTS §1, IAM §1/§6) —
fixing one alone recreates the two-drifting-impls failure.** PROTOCOL:
CONFLICT §2 "compromised pod speaks only as itself" (pod-granular) →
per-loop/init/sensor fd+key custody; GAPs: no class/archetype rows for
Scribe streams (authority-in class-6, alerts class-3 never-shed,
handoff-request/death-report class-3, Archivalist-flush bulk) / sensor
channel / alert stream; single-path guest-egress parenthetical (staging
ring is now PRIMARY-container-only; Scribe/sensor/init use own vsock
flows); OQ: envelope src_pod/dst_pod is pod-granular ⇒ (a) keep + carry
loop in flow-layer (32-bit channel-id in nonce + registry flow_identity
gains loop dim) NO envelope change [cheaper] / (b) version-bump envelope
to src_pod,src_loop,dst_pod,dst_loop [attribution survives flow-table
loss]. WIRE_SECURITY: CONFLICT §3 "recv_root installed IN THE GUEST"
(guest-global) → per-workload recv roots installed ONLY into each loop's
container (primary can't derive Scribe's receive keys); GAPs: flow-key
derivation + FlowKeyRequest/Grant need loop_id endpoint dimension;
staging-ring ownership is primary-container-only (fencing "src must
equal owning WORKLOAD = primary loop"); Scribe inbound vsock = a 2nd
guest receive path (same purpose-built-parser law + own enforcement-
point class); boot-classifier table += Scribe-flow + confirm sensor row;
key_epoch rule should NAME handoff. **VERIFIED CONSISTENT: key_epoch
semantics otherwise sound (predecessor frames die at both checks today;
PROTOCOL:103 + IAM:255-257 agree).** FAULTS: CONFLICT §1 Byzantine
out-of-scope "per-pod keys, lie only as itself" → per-workload flow keys
(primary can't lie as its Scribe at Bar A; Bar B collapses interior but
still speaks only as that pod, contained host-side); GAPs: the two-bar
adversary model is UNRECORDED and FAULTS is the fault-model authority
(add Bar A=degradation=HANDOFF's domain, Bar B=no Byzantine consensus
traffic); nemesis vocabulary needs pod-interior classes (container-exit
each ordering, ring-overrun, doorbell-stall); obligation-matrix rows for
history channel / Scribe lifecycle / init spawner (ring loss = in-
protocol typed gap records, NEVER a rebuild-from-quorum/authority
disposition — it's a non-authority enrichment surface). IAM: CONFLICT §6
"per-POD warden profiles (principal fixed)" → per-WORKLOAD residuals
(one per loop principal; primary and Scribe hold different authority;
IAM14 too); GAPs: **the Scribe MUST hold its OWN Principal** (first-class
agent, "its primary only" scoping needs a distinct principal) and needs
NO Mandate (runs under birth bindings); agent_pod→agent-LOOP (2
agent_pod principals per microVM, distinct UIDs, shared attestation +
init spawn-provenance); §7.4 summon pre-validates BOTH principals'
bindings (scribe office pack binds observability.read_stream for its
primary + claim subscribe + egress for reach-out + Archivalist
contribute); §7.12 read-set enumerated; §8 the ring named as the
non-IAM instance (fd-provenance, physics not policy). **VERIFIED (task-
mandated): NO IAM text gives the ring an IAM entry; §7.3 compile-source
+ sensor-tighten-only match the statement exactly; §7.12 "Scribe: its
primary only" matches verbatim.** HEALTH: 2 CONFLICT — §1 Token-progress
/turn-quality/context-fit sourced from "agent runtime" (guest) but §4b
says detection reads ONLY host-side ⇒ RE-SOURCE to gateway (host-
observed, provider-authoritative); those turn/stop/usage events are
exactly what rides the ring (enrichment, never a detector input) → add
a PROVENANCE column (host-observed|guest-reported), detection restricted
to host-observed, divergence-itself-a-signal (cross-view); §3 evidence
bundle "plus its narrative of intent drift" CONTRADICTS content-free H8
+ HEALTH's own "narrative belongs to Scribes" → reference (UID/hash) to
a narration artifact, never inline; GAPs: detection substrate + alert
stream absent from §2 consumer list; single-evidence-request = the
fresh-context probe (H3); per-container liveness; score-service inputs
refined; STALE-REFs: §1 "Branch 14 owns context-fit" (landed — point at
handoff spec, and it did NOT "slot in without changing shape") + header
"RANK score consumption" (architecture now supplied); OQ: does the
enriched-alert stream ride the health plane (a: signal class, reserved
never-shed group, AbsenceIs::Unknown) or its OWN class-3 directed stream
(b: detection→Scribe, reword H5 to permit it as the plane's one derived
output) — (b) matches delivery-class semantics better. RECONCILIATION
COMPLETE: 5 lanes, ~34 conflicts / ~65 gaps / ~20 pending-sites across
the corpus; 4 NO-CHANGE docs (TRANSFER, WIRE_FORMAT, WAL, SIBYL,
VECTOR_INDEX + MERGE-substantive). NEXT: consolidate + resolve OQs w/
recommendations + present for acceptance, then write MONITORING.md +
HANDOFF.md + ADR-0006 + all corpus amendments + GAPS in ONE change.

**USER RULINGS ON THE 3 LOAD-BEARING OQs (2026-08-19):** (1)
provider-egress/agent-channel placement = host-side gateway chokepoint
→ **ACCEPTED** ("Good"; resolves the PODS↔SUMMONING vsock-vs-virtnet
disagreement in SUMMONING's favor; primary has no netns + AF_VSOCK
EPERM; rustls TLS pool host-side at the gateway; in-guest speaks
hecate-wire over pre-connected fds; claims ride the staging ring;
PODS §3 agent-vsock row superseded; vsock = control + Scribe-flow +
sensor). (2) warm-pool container timing = **OVERRULED my
create-at-assignment** → the user wants images CACHED/kept-ready/
minimal/near-instant-INCLUDING-LOADING, PRE-LOADING agent OCI
containers pre-summon (they're role-keyed + IDENTITY-FREE ⇒
pre-loadable without breaking the generic-pool proof; DAX shared-map
one-host-copy-per-node, Scribe image = maximal dedup); user instinct:
(a) internal hecate agents ship EXTREMELY-LIGHTWEIGHT CUSTOM containers
+ ability to install additional tools at runtime; (b) each default
agent ships a MINIMAL TOOLS MANIFEST of what its work needs — and
this became **a NEW TREE ITEM (see below).** (3) Forest vs score
service = **CORRECTED (category error in the reconciler AND my
resolution): they are ENTIRELY DIFFERENT MECHANISMS FOR DIFFERENT
PURPOSES — the FOREST facilitates AMBIENT LEARNING; the SCORE SERVICE
facilitates AUTHORITY in challenge/consult and red/green feedback.**
NOT one drifting concept to consolidate. Fix = DECOUPLE: the Forest
does NOT feed the authority score (FOREST:180-184 "Rank inputs …
pushed to the score service" is the actual error — remove the
coupling); the score service computes authority INDEPENDENTLY from
ledger outcome deltas (challenges upheld, consults, red/green pass
rates) + Scribe snapshots (statement §6 already correct); the
Forest's aggregates drive its OWN advisory ambient-learning influence.
The shared prevalence/specificity/trust VOCABULARY is a domain-model
term collision (same 3 words, 2 mechanisms) → disambiguate in the
CONTEXT glossary (they name different things: field-ambient vs
authority). "fix root asymmetry" applies to the VOCABULARY, not the
mechanisms (which stay separate).

**BRANCH OPENED (2026-08-19): OCI HANDLING SUBSYSTEM (private-registry-
level) — new tree item, its own spec owed.** Directive (user, verbatim-
close): "add an item to our tree to define oci handling with respect to
our registry, underlying filesystem storage the registry uses (the
Tectonic FS), OCI image replication, hashing, authorization,
compatibility, etc. This should function at the level of a private
docker registry. Pin the image-pre-loading as a part of this tree
item." GROUNDING (corpus checked): "Tectonic FS" = the OBJECT_TIER
durable-plane chunk store (OBJECT_TIER IS Hecate's Tectonic-modeled FS,
FAST'21 lineage). TODAY: OCI is only a borrowed PATTERN — REGISTRY:171
"the registry hosts nothing; the resolver pins" (git/OCI refs → digests,
content lives elsewhere by hash — VFS §6, OBJECT_TIER Venti/OCI
any-copy-valid-by-hash). THE GAP: Hecate cannot natively HOST/SERVE/
REPLICATE OCI images — it pins external refs. This branch elevates OCI
to a FIRST-CLASS SUBSYSTEM functioning as a private docker registry:
scope = (i) OCI Distribution-Spec + Image-Spec handling (manifest/
config/layer blobs, push/pull/discovery) over (ii) the Tectonic FS
(OBJECT_TIER) as content-addressable blob storage — OCI sha256 digests
reconciled with Hecate chunk hashing; (iii) OCI image REPLICATION
(OBJECT_TIER copyset/popularity-mirror mechanisms; the Scribe image =
maximal-dedup replicated-everywhere case); (iv) AUTHORIZATION (IAM §7.9
publish/stage_approve extended to OCI push/pull/stage — who may push/
pull/serve images); (v) COMPATIBILITY (OCI-compliant so standard base
images + tooling interoperate — agents pull standard bases + install
tools); (vi) **IMAGE PRE-LOADING PINNED HERE**: pre-load/cache agent
OCI containers pre-summon, DAX-shared, near-instant spin-up INCLUDING
loading; minimal custom per-role images + per-role minimal tools
manifest + runtime tool-install (warden-gated egress + hash-screened —
ties to the parked response-authority lane-D threat-intel: runtime-
built/pulled binaries = the exec-time hash-match residue class). TOUCHES
on write: REGISTRY (§4b materialization, the "hosts nothing"→"hosts OCI
images" shift), OBJECT_TIER (OCI blobs as a durable-plane content class),
VFS (container rootfs subtrees, DAX), PODS (§2/§4 warm-tier pre-load,
§4b pull path), IAM §7.9 (OCI push/pull/stage authz). RELATION TO THE
MONITORING/HANDOFF WRITE: the container-loading/pre-staging design
belongs to THIS branch; the reconciliation write references it as
PINNED (PODS §4 warm-tier + VFS container-subtree wording point at the
OCI branch for pre-loading mechanics). RESEARCH OWED (dispatch on
user go): OCI Distribution/Image specs; private-registry impls
(Distribution/Harbor/zot) + CAS storage; near-instant OCI loading
(nydus/RAFS, stargz/eStargz, SOCI, overlaybd/DADI — measured cold-start)
+ DAX rootfs; pre-fetch/pre-warm (k8s image-puller, Kata pre-load);
minimal images (distroless/wolfi/apko/melange) + tool-manifest precedent
(apko lists, nix closures, devcontainer features); reconciliation with
the content-addressed manifest-projection rootfs Hecate already runs.
STATUS: tree item ADDED; design + research deferred to user direction;
image-pre-loading pinned to it (unblocks the MONITORING/HANDOFF write
via a pinned reference).

**RIGOR CHECK ACCEPTED (2026-08-20):** the 8 lower-stakes OQ
resolutions accepted after the maximally-correct/robust/performant/
efficient pass; 4 TIGHTENED (recorded for the write): (a) fitted
baselines = new CONTENT CLASS reusing the generation MACHINERY (not a
new mechanism; small ⇒ replicated-everywhere cache-role like the
routing artifact; atomic ref-flip gives the delete-artifact-changes-
alerts law free); (b) detector checkpoints host-local/re-derivable BUT
re-derivability REQUIRES detector INPUTS durably logged (logged
authority stream — ledger deltas already WAL-durable; warden verdicts +
gateway usage must be logged inputs) — the lossy telemetry hot ring is
DASHBOARDS-ONLY, never a detection input (hard correctness constraint);
(c) teardown gate = rung-2 sealed (fast/always); brief-critical window
places to rung-3 ASYNC best-effort — the ring-tail brief is ENRICHMENT,
the AUTHORITATIVE successor input is the claims graph, so simultaneous-
node-death degrades gracefully (never force rung-3 into the gate);
(f) scaling-class enum AgentRole-canonical + PODS-table-projection PLUS
a BOOT GATE (every role declares a scaling class or startup fails — no
default guess, chokepoint-coverage doctrine). HELD as-stated: (d) alert
stream own class-3 never-shed + H5 collection-vs-derived-output reword;
(e) envelope keeps src_pod/dst_pod, loop in the flow layer (per-workload
key IS the non-forgeable loop id; no version bump); (g) one guest binary
argv-dispatch (rustjail pattern; PID1 established by VMM, rt can't
re-exec as init); (h) HEALTH re-source to gateway host-observed +
provenance column + tool-signal split (detector tool signal =
warden-observed dispatches; ring tool digests = narration only). Office
= "companion narrator". NET: set stands; 2 refinements SHRANK the
design (b input-durability replaces ring-as-source; c rung-2 not rung-3).
**MONITORING/HANDOFF WRITE STAGED (resolutions accepted, ready) — NOT
executed; user is continuing to expand the tree (below); write folds in
the system-observability refinement first to avoid MONITORING §6 churn.**

**BRANCH OPENED (2026-08-20): SYSTEM OBSERVABILITY — telemetry / OTel /
logging across ALL systems.** Directive (user): "continue to refine
observability - we need to define telemetry gathering, examine
open-telemetry compatability and use, log monitoring and logging across
all systems, etc." SCOPE DISTINCTION (load-bearing): the just-finished
MONITORING/HANDOFF stack is AGENT observability (the Scribe's domain —
degradation/conduct detection over authority signals). THIS branch is
SYSTEM observability — metrics/traces/logs across EVERY Hecate subsystem
(harness services: Guide/Guardian/Archivalist/Arbiter/Inspector; storage
OBJECT_TIER/WAL; consensus; merge; VMM/pods; registry; IAM; OCI). It
GENERALIZES + DEEPENS MONITORING §6 (which designed only the agent-
envelope telemetry pipeline: per-node hot ring, Gorilla compression,
aggregate-at-source, bounded cardinality) into a system-wide plane, and
likely spawns a companion spec (TELEMETRY.md / LOGGING.md /
OBSERVABILITY.md — TBD). CORPUS STATE: OTel appears NOWHERE in the
written specs (the OTel-GenAI-convention metric-vocabulary refs live
only in the un-written MONITORING/HANDOFF drafts) ⇒ this branch decides
Hecate's OTel posture from scratch. THE LOAD-BEARING DECISION: **OTel
adoption DEPTH** — (i) full OTel (SDK instrumentation + OTLP export +
collector — max interop w/ users' Datadog/Grafana/Jaeger, big dep) /
(ii) OTel-COMPATIBLE-native (Hecate-native efficient in-process
collection per MONITORING §6 + OTLP export + semantic conventions —
interop WITHOUT the SDK dep, preserves efficient native collection) /
(iii) conventions-only (OTel vocabulary, native everything else —
minimal, ~where MONITORING is today). My prior (untested, needs
receipts): (ii) — Hecate's from-scratch/no-heavy-dep posture (own
protocol, own chunk store, no SQL) + the "single laptop, don't eat
resources" constraint argue AGAINST the OTel SDK's per-call overhead,
but OTLP-export-for-interop is high-value at Meta scale (users have
existing observability stacks). CHILD DECISIONS the branch spawns:
telemetry gathering across all subsystems (metrics + traces + logs from
each; extends §6 collection beyond agents); LOGGING architecture
(structured-log standard, levels, per-node→federated pipeline,
retention, correlation w/ traces/metrics via exemplars); LOG MONITORING
(log-based signals — do they feed the detection substrate or stay a
separate operational plane?); the RELATIONSHIP to HEALTH's "one signal
stream" + the detection substrate (agent-detection vs system-operational
— one plane or two?); the efficiency/overhead budget (sampling,
cardinality, laptop degenerate). RESEARCH DISPATCHED (2 lanes): OTel
data-model/OTLP/collector/adoption-tradeoffs; system-wide telemetry+
tracing+logging at scale + log monitoring. Write of MONITORING/HANDOFF
now WAITS on this branch settling (shared §6 telemetry surface).

**SYSTEM-OBSERVABILITY RESEARCH — interrupted then resumed (2026-08-20).**
First dispatch (a3e9bf5a OTel; aa9e08f75a syslog — the latter self-fanned
into W2/W3/W4/W5 sub-agents) ALL FAILED on a session usage limit (reset
12:20am America/Chicago) before composing dossiers — but left strong
receipts in scratch: otel_lane/ = proto_README.md + otlp_spec.md +
docs_listing.json; syslog_lane/ = FULL Dapper paper (dapper.txt 83KB),
FULL Scuba VLDB paper (scuba.txt 70KB), crown_jewels.md (confirmed
quotes: tracing/slog/RFC5424/SRE-workbook/Scuba). RESUMED post-reset
with 2 lanes (a68d41da OTel; a973c132 syslog), each told to build on the
retained downloads + fetch only gaps + NOT fan out (avoid multiplying
session budget). Awaiting.

**SYSLOG LANE LANDED (2026-08-20): SYSTEM TELEMETRY + TRACING + LOGGING
+ CORRELATION + COST.** Findings map ~1:1 onto Hecate's EXISTING
patterns (strong design signal). W1 TRACING: Dapper — un-sampled
tracing is UNAFFORDABLE; **1/1024 head sampling within experimental
error** (Table 2: 1/1→+16.3% latency, 1/16→+2.12%, 1/1024→−0.20%);
ADAPTIVE-BY-TARGET-RATE ("parameterized not by uniform probability but
by a desired rate of sampled traces per unit time… low traffic
auto-increases, high traffic lowers… actual probability recorded with
the trace") = EXACTLY Hecate's existing adaptive-rate agent sampling,
now receipted for tracing; out-of-band collection (in-band would
perturb app net dynamics). Canopy (Meta, 1.3B traces/day): "Evaluating
interactive queries over raw traces is computationally infeasible" ⇒
AGGREGATE-AT-SOURCE (extract features → Scuba/Hive), per-tenant TOKEN
BUCKET (5 traces/s default), probability|rate, LEVEL-OF-DETAIL knob.
Jaeger: HEAD-vs-TAIL is THE explicit decision (tail = "runtime overhead
… record and export ALL traces" + backend memory). Tempo: NO INDEX,
trace-id lookup, object storage — "orders of magnitude more trace data
for the same cost" (the cold-tier argument). W2 STRUCTURED LOGGING:
Rust **`tracing` crate** = the fit (structured event-based; "span =
period, event = moment"; typed data; async/tokio rationale: interleaved
task logs need spans — DIRECTLY fits Hecate's task-native runtime);
slog (KV type-preserving JSON); RFC 5424 STRUCTURED-DATA + enumerated
severity 0-7; journald KV fields + PRIORITY + TRUSTED underscore-fields
(provenance, matches Hecate's validation-provenance discipline);
Honeycomb wide-events/high-cardinality. W3 STORAGE: **Loki = "does NOT
index the contents of the logs, but only indexes metadata … as labels"
(THE canonical cost statement)**; LogDevice (append-only, TRIM-by-
retention = hot-ring eviction analog, decouple ordering-from-storage via
sequencer for write-availability); **Scuba (VLDB'13) = the at-Meta-scale
PROOF of Hecate's per-node in-memory hot ring**: all-in-memory,
sampled (1-in-100 to 1-in-1M), >6× compression, "MEMORY not cpu is the
scarce resource", + FAN-IN AGGREGATION TREE (Root→Intermediate
fanout-5→Leaf, partial aggregates propagate up, avg→sum+count for
end-compute, sub-second queries) = THE MISSING CROSS-NODE PIECE for
Hecate's aggregate-at-source; Scribe (sample at emission edge); Vector
(bounded buffers, backpressure, EXPLICIT block-vs-drop — Hecate must
pick deliberately per no-drops/no-unbounded-growth rules). W4
LOG-MONITORING: Google Cloud logs-based-metrics + Loki LogQL
(rate/count_over_time) → logs BECOME metrics feeding the SAME alerting
plane (empirical answer: log-derived signals CAN feed the same
detection machinery); BUT SRE-book discipline: "spend much more effort
on catching SYMPTOMS than causes", 4 golden signals (latency/traffic/
errors/saturation), white-box-vs-black-box, "alert rules as simple,
predictable, reliable as possible" (matches Hecate doctrine #10
no-string-matched-roll-ups). W5 CORRELATION: one propagated trace_id +
exemplars (metric→trace) + Loki derived-fields (log→trace regex) +
Honeycomb single-wide-event; MTTR% THIN. W6 LAPTOP/OVERHEAD: Dapper
measured — daemon 0.3% of one core, 0.01% network, 426 B/span avg,
**9 ns un-sampled fast-path (thread-local lookup)** = what makes
instrument-EVERYTHING-record-a-FRACTION affordable; Prometheus —
single-node local storage is the DEFAULT (N=1 is NOT a special mode),
1-2 B/sample, cost = retention×rate×bytes-per-sample (FORMULA FROM
PHYSICAL ANCHORS — matches Hecate no-magic-numbers). W7 SYNTHESIS — 5
axes, receipts both poles, NO pick: (1) unify-wide-event (Honeycomb;
correlation free, one record type) vs separate-planes-bridged-by-ids
(Prometheus+Tempo+Loki; each individually cheapest per signal); (2)
storage tiering = hot-in-memory (Scuba) + cold-metadata-indexed
(Loki/Tempo) + append-log spine (LogDevice) — extends Hecate's hot ring;
(3) **sampling + bounded cardinality = THE cost control at BOTH scales**
(instrument everything, record a fraction, aggregate at source, record
the sample rate to correct aggregates — Hecate's existing agent
discipline generalizes VERBATIM to all subsystems); (4) log-monitoring
feeds same substrate (symptom-level golden-signal detectors) vs separate
operational plane — OPEN; (5) correlation = one id + two link
affordances. 1 lane still out: OTel depth (a68d41da).

**OTEL LANE LANDED (2026-08-20): DECISIVE.** HEADLINE: OTel splits into
3 INDEPENDENTLY-ADOPTABLE LAYERS; the interop value lives in the CHEAP
layers (OTLP wire + conventions), ALL the cost/risk lives in the SDK +
Collector. W1 DATA MODEL: trace-id 16B / span-id 8B (native-mintable);
metrics sum/gauge/histogram/exp-histogram, DELTA temporality "enables
sampling and supports shifting the cost of cardinality OUTSIDE the
process" (+ SINGLE-WRITER requirement = matches Hecate discipline);
**logs WRAP not replace — a "Logs Bridge API" for appenders over
existing logging** (LogRecord carries trace_id/span_id = log→trace
correlation); exemplars = metric→trace (trace_id/span_id in metric
points); resource = shared attrs = correlation third leg. **W2
(LOAD-BEARING) — CRUX ANSWERED YES: OTLP is a STABLE, SELF-CONTAINED
wire format a NATIVE (non-SDK) emitter targets directly** — proto
"consumed as GIT submodules or copied and built directly"; parties
defined by ROLE not SDK ("sending side of telemetry collectors" ⇒ a
native Rust emitter IS an OTLP Client); stability = no field/number/
name changes, additive-only, NO version numbers (Protobuf schema
evolution); gRPC :4317 / HTTP :4318; partial-success + retry tables +
throttle/backpressure + size limits (64MiB req/4MiB resp rec); dup-data
"deliberate right tradeoff for telemetry" (relevant to at-most-once).
W3 COLLECTOR: receiver→processor→exporter, one-codebase agent+gateway,
FULL-TEARDOWN-on-reload, SYNC COUPLED fan-out (blocking caution);
testbed CI cost 10k spans/s OTLP-gRPC = 20% core / 100MiB (attr-size
sensitive: 100attrs×50B ⇒ 120% core) — **the Collector DUPLICATES
Hecate's own per-node collection; needed ONLY to speak OTLP to
arbitrary backends.** W4 (LOAD-BEARING) SDK OVERHEAD: Rust SDK Traces
still BETA (Metrics/Logs Stable); logs = bridge API, **maintainers
recommend the `tracing` crate** (CONVERGES with syslog lane); per-op
(NoOp, all-cores): logs 27M/s enabled vs 1.4B/s disabled = **~50× gap**
(cost is BUILDING the record ⇒ cheap enabled-check must gate hot paths);
metrics counter 1.65M/s @1000-time-series (**cardinality is where cost
concentrates**); traces 5.2M/s; prod "removed-OTel" anecdotes THIN
(search budget exhausted) but first-party SDK numbers are stronger. W5
CONVENTIONS: YAML spec you FOLLOW NATIVELY (no SDK); **gen_ai.* =
Development-grade, JUST MOVED to a dedicated repo (churning) but has
EXACTLY the multi-agent-coding-harness vocabulary**: usage.input/output/
reasoning.output/cache_read/cache_write tokens, execute_tool.duration,
invoke_agent.duration, invoke_workflow.duration, TTFT, time_per_output_
token; provider files (anthropic.md, mcp.md); following natively (PIN a
version) insulates from churn. W6: lineage OpenTracing+OpenCensus merger
(OpenCensus = Google Census/Dapper heritage), CNCF, "NOT a backend
itself"; OTLP-as-ingestion adopted by Prometheus (native OTLP receiver),
Datadog Agent, AWS ADOT, Grafana — NO SDK needed to feed them;
Meta/Google-internal-vs-OTel NO-PRECEDENT this run. W7 THE ASYMMETRY
(verbatim): "the interop benefit of OTel is almost entirely capturable
at Depth A/B, while essentially all of the overhead, maturity risk, and
dependency cost lives in Depth C. The SDK is not a prerequisite for OTLP
compatibility; it is one (heavyweight, partly-Beta) implementation of
it." 3 DEPTHS: A conventions-only (zero dep) / **B native-collection +
OTLP-export + conventions (low bounded dep, MAXIMAL interop, serialize-
at-export-boundary-only, fits own-the-hot-path posture)** / C full SDK+
Collector (highest dep, Beta traces, duplicates per-node collection).
BOTH LANES IN — consolidating + presenting the branch design w/ the
Depth-B recommendation.

**CLARIFICATION (user caught, 2026-08-20): the upstream OTel Collector
is a GO service** (the testbed cost numbers are from Go files) — cited
only as a PROPERTY of Depth C, never something Hecate builds. Its
Go-ness is one MORE reason Depth C is wrong for a Rust system: adopting
it = bolting a foreign-runtime service (own process/supervision/
lifecycle) onto Hecate that DUPLICATES the native per-node collection.
**Depth B (recommended) has NO Collector and NOTHING Go: native Rust
per-node collection (already built for agent metrics) does receive/
aggregate/sample; a RUST OTLP ENCODER (vendored proto submodule,
Protobuf message-building, no SDK) speaks OTLP at the export boundary.**
Any future collector-like fan-in/routing = built in Rust (we already
have the design: the Scuba-shape cross-node fan-in aggregation tree).
The plane stays Rust end-to-end. (Note: OTel Rust SDK exists and IS
Rust, but it's the OTHER half of Depth C — Beta traces + per-record
overhead; Depth B skips it too.)

**USER CHALLENGE (2026-08-20): "Why not build our own collector? We
don't fear complexity." — CORRECT; I under-sold it.** The real decision
was NEVER collector-vs-no-collector; it's ADOPT-THE-GO-COLLECTOR
(Depth C) vs BUILD-OUR-OWN-NATIVE-RUST-COLLECTOR. What I called "native
per-node collection" IS a collector — I mis-framed "collector" as the
Go artifact to avoid. FIRST-PRINCIPLES ANSWER: **build our own** (call
it what it is: a first-class Hecate telemetry collector). REFRAMED
DESIGN — the Hecate collector = a native Rust telemetry PIPELINE
(receivers → processors → exporters, the OTel Collector's SHAPE as
precedent) in TWO TIERS: per-node AGENT tier (the in-memory hot ring)
+ cross-node GATEWAY/fan-in tier (the Scuba-shape aggregation tree),
speaking OTLP at BOTH EDGES (OTLP-IN + OTLP-OUT). RECEIVERS: native
`tracing`/metric/log emission from every subsystem + **OTLP-IN from the
instrumented workloads Hecate RUNS** (agent tool subprocesses, MCP
servers, user code — they emit OTLP; we ingest it). PROCESSORS:
aggregate-at-source, head+TAIL sampling (tail needs complete-trace
buffering at the fan-in tier — a collector-only capability), bounded-
cardinality enforcement, resource enrichment, trace-id correlation
stitching, + TWO HECATE-NATIVE processors the Go Collector CANNOT do:
**provenance-classing** (OTLP-in from a workload = guest-reported,
never authoritative for detection; Hecate-emitted subsystem telemetry =
host-observed) and **content-free-law enforcement** (HEALTH's no-
work-content/no-ledger-content rule, structural at ingest). EXPORTERS:
OTLP-OUT (interop — Prometheus/Datadog/ADOT/Grafana ingest directly) +
internal fan-out to the detection substrate / score service /
dashboards / durable spine (WAL + object-tier), ALL off ONE pipeline
(no duplication). WHY OWN IT (beyond doctrine): a thin OTLP encoder
CAN'T ingest workload telemetry, can't provenance-class at ingest,
can't tail-sample (no fan-in buffer), can't be the single pipeline
feeding both interop-export AND internal detection — the moment you
want fan-in + tail-sampling + OTLP-in + multi-exporter you HAVE a
collector, so own it. RIGOR (maximally-correct/robust/performant/
efficient): correct (provenance + content-free structural at ingest;
one authoritative pipeline); robust (no foreign runtime; Hecate
supervision/scheduling; backpressure under no-drops/no-unbounded-growth
rules; we design the fan-out, avoiding the Go Collector's documented
sync-coupled-fan-out blocking hazard); performant (native Rust, no
per-record SDK cost, 9ns enabled-check gate, tail-sampling at the right
tier); efficient (one pipeline, N exporters; reuses the hot ring +
fan-in tree + storage tiers already designed). This is Depth B done
MAXIMALLY (= "own-collector"): STILL no SDK, STILL no Go — OTel
Collector = pipeline-shape precedent, OTLP+conventions = the wire
contract (in AND out), the implementation is ours. The companion
"telemetry substrate" spec IS this collector spec. SCOPED to Hecate's
needs (not OTel's 100+ receivers/exporters): the receivers/processors/
exporters Hecate actually needs, extensible.

**DECISION FINALIZED (2026-08-20, user): PORT THE GO OTEL COLLECTOR TO
RUST + ADAPT to our needs/protocols.** Definitive method — not "build
inspired by the shape" but PORT the actual OTel Collector (Go,
Apache-2.0 ⇒ permissive, clean to derive) to Rust and adapt. WHAT WE
PORT (the core, NOT the 100+ contrib components): the pipeline framework
(receiver/processor/exporter abstractions + service wiring), the OTLP
receiver + OTLP exporter, the batch + tail-sampling processors. WHAT WE
ADAPT: config/wiring → Hecate's model (AgentRole/registry-shaped, not
raw YAML); internal transport → hecate-wire + warden-gated vsock;
external edges → standard OTLP (in AND out). WHAT WE ADD (Hecate-native
components atop the ported framework): receivers = native `tracing`/
metric/log emission from every subsystem + OTLP-IN from instrumented
workloads over warden-gated vsock; processors = provenance-classing
(guest-reported vs host-observed) + content-free-law enforcement +
aggregate-at-source + adaptive-rate + the Scuba cross-node fan-in tree;
exporters = OTLP-OUT (interop) + internal fan-out to detection substrate
/ score service / dashboards / WAL+object-tier. WHAT WE FIX during the
port (the Go Collector's DOCUMENTED faults, under Hecate rules): the
SYNC-COUPLED fan-out blocking hazard → our fan-out under no-drops/
no-unbounded-growth + explicit block-vs-drop; the FULL-TEARDOWN-on-
config-reload → hot reconfiguration. TWO TIERS (ported topology): agent
= per-node host-side (the hot ring; tamper-proof host collection) +
gateway = placed region-local service (the fan-in tree, colocation-unit-
adjacent). RUNTIME SUPPORTS IT (user, 2026-08-20: "our microvm + OCI
runtime certainly has the ability to support it"): OTLP-IN from the
workloads Hecate RUNS rides the EXISTING pod channel infra (registered
vsock flow, warden-terminated, provenance-classed guest-reported — like
the sensor channel); the collector hosts on Hecate's own runtime
(agent tier host-side; gateway tier as a placed service, or dogfooded in
a pod) — so a std OTel-instrumented workload (user code / tool subproc /
MCP server) running in a Hecate pod gets its OTLP telemetry ingested,
provenance-classed, correlated. This SUPERSEDES the A/B/C depth framing:
the answer is "own a Rust collector PORTED from the OTel one," which is
neither adopt-the-Go-Collector (C) nor thin-encoder (my under-sold B) —
still NO SDK, still NO Go in Hecate; the ported Rust collector IS the
OTLP client/server. NEW TREE ITEM: the Hecate Collector spec (= the
telemetry substrate MONITORING §6 + the system-operational plane both
consume). STILL OWED: the two-planes ruling (system log/telemetry-
monitoring feeds the detection substrate vs a separate operational
plane — my rec: two planes, one shared collector pipeline + correlation
spine).

**PROCESS CORRECTION (user, 2026-08-20): "Rather than just saying crisp
and settled, you should do actual research and design the solution with
respect to ALL of our existing specs and architecture."** I over-
declared "settled" on a DIRECTION without the diligence the discipline
requires (the IAM "zero actual research / no analysis of existing
designs for conflicts" lesson, repeated). The port-to-Rust direction is
chosen; the DESIGN is owed = (a) research WHAT the OTel Collector
actually is internally (the parts that must be ported), (b) DESIGN the
Hecate Collector reconciled against EVERY existing spec (integration
points + conflicts + gaps, IAM-reconciler pattern), backed by receipts.
3 LANES DISPATCHED: L1 OTel Collector CORE architecture (pdata data
model ptrace/pmetric/plog + mutability/copy; Service/pipeline graph +
connectors + shared-receiver fan-out semantics; Component/Factory/
registry model + extensions; confmap/config resolution); L2 OTel
Collector LOAD-BEARING subsystems (exporterhelper queued-retry +
sending-queue memory-vs-PERSISTENT + storage-extension backing = the
reliability/durability core; batch; memory_limiter backpressure;
tail_sampling buffer+policies+decision-cache+memory-cost; filter/
transform/attributes enrich-redact family; self-telemetry); L3 CORPUS
INTEGRATION MAP (read ALL relevant specs, produce per-spec integration/
conflict/gap for a native Hecate Collector — OBJECT_TIER cold-telemetry
class + persistent-queue backing on Tectonic FS; WAL durable spine +
is-the-collector-a-logical-log-client; PROTOCOL/WIRE_FORMAT/WIRE_SECURITY
internal transport + OTLP-in flow class/keys/provenance; PODS host-side
agent tier + OTLP-in vsock + gateway hosting; SCHEDULER gateway
placement + colo-unit membership; CONSENSUS single-writer classification
of the gateway aggregator; IAM telemetry authz + provenance-class
governance + §7.12; HEALTH one-signal-stream relationship + two-planes +
content-free law; MONITORING/HANDOFF agent-detection consumer + §6
refactor + detector-input-durability; REGISTRY component/factory
registration + config-as-registry-content; SESSIONS per-session vs
system-wide; OCI dogfooding; RUNTIME/AGENTS_RUNTIME tracing-instrument
the runtime). On landing: SYNTHESIZE the designed Hecate Collector spec
(architect's job) + present reconciled-against-corpus for acceptance.
MONITORING/HANDOFF write still staged behind this.

**TWO DIRECTIVES (user, 2026-08-20) — shape the design:** (1)
**TWO-PLANES RULING SETTLED (separate, with one crossing):** "The otel/
telemetry pipeline is to be separate of the monitoring and health plane
by and large excepting that all health and monitoring events, processes,
and services (i.e. the warden, the sensor, all of it) needs to be
instrumented." ⇒ the Collector (telemetry) is SEPARATE from the
monitoring/health plane (detection reads its OWN authority signals, NOT
telemetry); the ONE crossing = the monitoring/health machinery is itself
a SUBJECT OF INSTRUMENTATION (warden, sensor, detection substrate, health
service, score service, Scribe — ALL emit telemetry into the Collector).
KEY MODEL: a component emits into BOTH planes with different outputs —
warden VERDICT (deny/allow) = monitoring-plane authority signal; warden
PERFORMANCE (decision latency/throughput/CPU) = telemetry into the
Collector. Same component, two planes, no blur. (Supersedes my "two
planes over ONE shared pipeline" rec — they're SEPARATE pipelines; the
link is instrument-the-monitoring-plane, not share-the-collection.) (2)
**MAXIMAL COLLECTION: "We collect absolutely as much of everything.
Period."** ⇒ TOTAL instrumentation, nothing un-instrumented. RIGOR
(reconcile w/ "sampling is the cost control" — different STAGES, not a
contradiction): collect-everything at EMISSION (9ns un-sampled fast path
⇒ affordable at source) + aggregate LOSSLESSLY over the FULL stream
(counts/histograms preserve the whole signal as raw events age out) +
cost discipline moves to RETENTION TIERING + raw-event TAIL-SAMPLING
(keep aggregates over 100%, tail-sample which raw traces survive as
exemplars — Scuba ingests millions/sec bounded by memory + expire-at-
ingest-rate). The durability core (exporterhelper PERSISTENT QUEUE) must
hold under that volume. RESEARCH LANES ADJUSTED for both: L2 adds the
maximal-collection-vs-affordability reconciliation (aggregate-over-all
lossless + tier/tail-sample the raw; persistent-queue durability under
high volume); L3 adds the two-planes-separate constraint (map how
warden/sensor/detection/health/score emit BOTH authority-to-monitoring
AND telemetry-to-Collector; the Collector instruments the monitoring
plane but stays separate).

**+2 MORE DIRECTIVES (user, 2026-08-20):** (3) "And you need to research
and design that" — the MAXIMAL-COLLECTION model is RESEARCH+DESIGN, not
a gloss (the collect-everything + lossless-aggregate-over-all + tier/
tail-sample-raw + persistent-queue-durability model must be grounded in
receipts AND fully designed). (4) "You also need to design the 'single
laptop' case. And research that as well." — the N=1 DEGENERATE of the
WHOLE telemetry/Collector system is first-class RESEARCH+DESIGN: the
two-tier collector (per-node agent + cross-node gateway) → ONE
in-process pipeline at N=1 by DERIVED PARAMETERS not modes (PODS
scale-doctrine); local storage on the object-tier/WAL laptop-degenerate;
the same collect-everything model bounded by LAPTOP memory (Scuba
memory-bound + expire-at-ingest-rate; Prometheus single-node-is-the-
default; the un-sampled-fast-path keeps instrument-everything cheap even
at N=1); zero modes. LANES SCOPED to cover all four: L1 += the OTel
single-binary/embedded/in-process/agent-only shape (the N=1 runtime
form); L2 += maximal-collection reconciliation (research+design) + N=1
storage/retention/memory-bound; L3 += N=1 no-modes corpus consistency
(how PODS/OBJECT_TIER/WAL/HEALTH handle laptop-degenerate — the
Collector must follow the same derived-parameter-not-mode discipline).

**+2 MORE DIRECTIVES + EXPANDED TO 4 LANES (user, 2026-08-20).**
(5) "You need to research the WORK REQUIRED to adapt the otel collector,
you need to research via OUR SPECS and other decisions what is required
to INSTRUMENT, you need to actually research all of this." (6) "distill
it into a coherent, actionable, explicit, HYPER-DETAILED actionable plan
at the granularity and detail we have clearly come to expect given our
other specs" + "Your research and design must produce the maximally
correct, robust, performant, efficient, COMPATIBLE, COMPREHENSIVE (both
system coverage/breadth AND detail) design." ⇒ DELIVERABLE BAR = a
spec-grade Hecate Collector design at IAM.md/PODS.md granularity
(sections + mechanics + worked examples + test matrix + acceptance
criteria + corpus amendments), maximally correct/robust/performant/
efficient/compatible/comprehensive. 4 LANES DISPATCHED (all no-fan-out):
**A (af9bc69)** OTel Collector CORE + PORT WORK — pdata data model
(the crux to port), Service/pipeline graph + sync-coupled-fan-out
hazard, Component/Factory/registry, confmap config, connectors/
extensions, embedded/single-binary/in-process (N=1 runtime shape), +
THE PORT EFFORT (core-vs-contrib inventory, Rust-collector prior art,
Go→Rust translation: goroutines→tokio / interfaces→traits / reflection-
factory→explicit-registration). **B (ab36703)** RELIABILITY subsystems
+ MAXIMAL-COLLECTION + N=1 — exporterhelper queued-retry + sending-queue
memory-vs-PERSISTENT (the durability core), batch, memory_limiter
backpressure, tail_sampling (buffer/policies/decision-cache/mem-bound),
filter/transform/attributes; the collect-everything-affordably model
(lossless-aggregate-over-all + tier + tail-sample-raw; Scuba/Prometheus/
exp-histogram receipts); N=1 resource story (memory-bound + formula-
from-anchors + 9ns-fast-path). **C (a10a751)** INSTRUMENTATION SURFACE
from OUR SPECS — read ALL 26 specs + 5 arch docs, enumerate per-
subsystem spans/metrics/logs + the two-planes split (monitoring-
authority-signal vs telemetry) for warden/sensor/pods/runtime/scheduler/
consensus/object-tier/wal/merge/ledger/iam/registry/serving/vfs/forest/
rank/health/sessions/vector/agents/gateway/oci/collector-self/detection.
**D (a8552f0)** CORPUS INTEGRATION MAP + N=1 no-modes + two-planes-
separate — per-spec integration/conflict/gap on OBJECT_TIER/WAL/PROTOCOL
/WIRE/PODS/SCHEDULER/CONSENSUS/IAM/HEALTH/MONITORING/REGISTRY/SESSIONS/
AUTOSCALING; the N=1 derived-parameter-not-mode consistency; the
separate-plane-but-instrument-the-monitoring-plane placement. On ALL
FOUR landing: synthesize the hyper-detailed Hecate Collector spec
(architect's job), present reconciled-against-corpus for acceptance,
THEN it joins the staged MONITORING/HANDOFF write.

**COLLECTOR LANE B LANDED (2026-08-20): RELIABILITY + MAXIMAL-COLLECTION
+ N=1.** W1 EXPORTERHELPER (the reliability core to port): sender chain
outer→inner = Queue→ObsReport→Retry→Timeout→pusher — **the queue is the
durability boundary; retry/timeout run CONSUMER-side, so a crash
mid-retry loses nothing the persistent queue holds.** Sending queue:
num_consumers 10, queue_size 1000, block_on_overflow false(drop)/
true(block); batching ABSORBED into the queue (min_size 8192,
flush_timeout 200ms); retry 5s→30s cap, max_elapsed 300s, ×1.5, per-try
timeout 5s. **PERSISTENT QUEUE = WAL-LIKE**: monotonic read/write index
+ separate DISPATCHED-ITEMS set; crash recovery re-enqueues dispatched-
but-unacked (`retrieveAndEnqueueNotDispatchedReqs`, "picked up again
after restart") ⇒ the in-flight set turns AT-MOST-ONCE into
AT-LEAST-ONCE across restart; bbolt-backed (filestorage) → maps onto
Hecate's WAL/OBJECT_TIER for the durable queue. W2 batch: size(8192)+
timeout(200ms) dual trigger, after memory_limiter. W3 MEMORY_LIMITER
(the no-unbounded-growth primitive): soft = limit−spike; refuse-at-soft
+ force-GC-above-hard; upstream backpressure; FIRST in pipeline; "data
PERMANENTLY LOST if the preceding component doesn't retry" ⇒ MUST pair
w/ persistent queue. W4 TAIL_SAMPLING: complete-trace buffering, "all
spans MUST be received by the SAME collector instance" = the hard
FAN-IN constraint (needs trace-aware load-balancing in front — can't
trivially sub-shard); policies latency/status/probabilistic/
rate_limiting/composite/ottl/…; decision_wait 30s, num_traces 50k
in-mem, decision_cache LRU for released-trace verdicts (straggler-span
trick); filter/transform/attributes = **the content-free model**
(attributes:hash SHA1, transform:replace_pattern redaction, filter:drop)
→ Hecate's provenance-class + content-free processors. **W5 MAXIMAL
COLLECTION (grounded): maximal ≠ keep-everything-raw-forever; maximal =
(total instrumentation @emission, 9ns un-sampled fast path — Dapper)
+ (LOSSY-BUT-BOUNDED-ERROR aggregates over 100% — exp-histogram "high
dynamic range, small relative error"; Prometheus native-histogram ~8×;
spanmetrics R.E.D over ALL spans; O(buckets) mem over O(events))
+ (TIERED retention — Scuba memory-bound/expire-at-ingest-rate/
subsample-the-aging-tail/cold-object-store; Tempo object-store RF1)
+ (tail-sample which RAW traces survive as EXEMPLARS addressable from
metrics via trace_id).** THE COMPOSITION (flagged composed, primitives
confirmed): metric-deriving connector AHEAD of the sampler ⇒ metrics
computed over 100%, sampler picks retained raw exemplars; "never
conflate OBSERVED with RETAINED-RAW" (Scuba's raw-count + adjusted-count
is the same trick). **W6 N=1: same formulas, cluster terms = 1, NO lite
mode.** Prometheus disk = retention × ingest_rate × bytes_per_sample
(1-2 B/sample), single-node-by-DEFAULT, WAL crash-safe; Scuba
memory-bound + expire-at-ingest = the laptop bound; Dapper daemon <0.3%
core + lowest-sched-priority + 426 B/span, cost tracks RETAINED not
OBSERVED ⇒ 9ns fast path keeps instrument-everything true at N=1;
N=1-is-degenerate = COMPOSED (the 3 formulas are node-count-free). 3
lanes still out: A (core+port), C (instrumentation surface), D (corpus
integration).

**COLLECTOR LANE C LANDED (2026-08-20): INSTRUMENTATION SURFACE (all 32
docs read, exhaustive per-subsystem inventory — the BREADTH piece).**
HEADLINE SPLIT: the corpus ALREADY emits a rich, mostly-BOUNDED signal
set (constants-from-data + counted-drops + five-outcome-accounting +
ratcheted floors are pervasive design law) ⇒ the Collector's job is
**~70% OBSERVATION/CONSOLIDATION of already-named signals + ~30% NEW
performance instrumentation** (CPU/mem, LLM-call spans, provider detail,
distributed trace context, self-telemetry). TWO PLANES ARE CLEAN
PER-COMPONENT: AUTHORITY signals (verdicts/deltas/validations — already
owned by ledger/health, the Collector OBSERVES not re-authors) vs
TELEMETRY (performance: latency/throughput/errors/saturation/CPU/mem —
the new mandate). CROSS-CUTTING LAWS the Collector inherits: (i)
**CARDINALITY = THE CONTENT-FREE LAW** (HEALTH H8 + WIRE_FORMAT §3c):
labels are BOUNDED closed hecate-wire enums ONLY (node/shard/office(10)/
participant_kind(4)/principal_kind(5)/delivery_class(0-6)/archetype(6)/
drop_reason(8)/verdict/disposition/fault_class(16)/storage_class/…);
FORBIDDEN as labels (⚠️ span-attr/exemplar ONLY): claim_uid/testament_
uid/request_id/session_uid/pod_uid/agent_uid/path/symbol/chunk_hash/
content_hash/flow_key/HLC/manifest_hash/green_version (IAM19 + H6/T10:
bounded by NODE count never POD count); the Collector enforces this on
ITS OWN labels by type-walk; `collector.cardinality.series` = its most
important self-signal. (ii) **TIMING READS Driver::now()→Tick** (SIM-
deterministic; RUNTIME bans std Instant/SystemTime in core crates; T1);
wall-clock telemetry-only, never a correctness path. (iii) runs on
hecate-rt (single-owner tasks, bounded queues, no-panic). **TWO HARD
ARCHITECTURAL GAPS (🔩 must be minted):** (1) **TELEMETRY CARRIAGE is
UNDESIGNED** — no spec assigns spans/metrics/logs a delivery class or
traffic archetype; health rides UDP gossip "under the datagram budget"
(HEALTH §2/PODS §3/PROTOCOL §1.1 class-1) which CANNOT carry heavy
telemetry; needs its OWN opportunistic-class operational-log lane
(PROTOCOL §1.2 hecate-quic or bulk-adjacent) that respects the
non-interference law (telemetry = opportunistic-by-purpose, NEVER enters
another class's critical path) — and PROTOCOL P19 FAILS BOOT on an
unclassified kind, so it MUST be minted. (2) **NO trace/span-id in the
envelope** — PROTOCOL §1.1 envelope has request_id + caused_by + HLC but
NO trace_id/span_id; distributed traces reconstruct from caused_by
parentage (the causal spine, stamped where the turn is minted) +
request_id + HLC, OR add an append-only span-context field (WIRE_FORMAT
§5 additive). OTHER NEW HOOKS: per-task CPU/mem meters (arenas give mem,
no CPU-time meter — read Driver::now()); provider-gateway detail surface
(token accounting required but per-provider latency/error/token/429/
failover histograms + LLM-call spans provider/model/stage/effort/TTFT/
stop-reason/cache-hit = the single highest-value new trace for cost/
latency attribution); `panic.aborts` counter (RUNTIME §4b requires
"counted, root-caused" but names none); the Collector's own self-
telemetry. REUSE LIST (10, don't duplicate): health's 6 signals +
freshness + AbsenceIs; five-outcome accounting (ONE shared instrument
across PODS/SCHEDULER/TRANSFER/AUTOSCALING); drop taxonomy (8 closed);
fault dispositions (Masked/Degraded/Refused × 16, boot-validated);
ratcheted latency floors (warden µs/shard/placement/WAL/merge/serve/
seal/loopback — all already declared); named saturation gauges (warden
hold-queue/frontier-lag/retirement-debt/monitor-closure/NVMe-endurance/
warm-pool/per-office-queues = the autoscaling signals); scaling+quality
signals (speculation-accuracy/memoization/locality/recall@k/dedup/
scrub/Forest-value-gate); named ALARMS (stuck-cursor ×3/summon-budget-
miss/closure-breach/merge-divergence-fatal/sensor-silence/warden-frozen/
signal-staleness); idle-cost ratchet (CN2/IAMS3 — prove ~zero); the
NON-INTERFERENCE SCALE-WALK (per-class latency AND memory FLAT MB→PB,
PROTOCOL §3 = the single richest telemetry surface). BOTTOM LINE: ~70%
observe/consolidate + ~30% new instrument; the 2 hard gaps = carriage +
trace-context; the FAULTS failure×obligation matrix (16 classes ×
disposition) = the natural top-level Collector dashboard. 2 lanes still
out: A (core+port), D (corpus integration).

**COLLECTOR LANE D LANDED (2026-08-20): CORPUS INTEGRATION MAP (18
specs + GRILLING accepted-design read; per-spec integration/conflict/gap
+ N=1 + two-planes placement — the RECONCILIATION piece).** MOSTLY
REUSE, few new mechanisms. **RECONCILES Lane C's "carriage gap": Lane C
overstated "undesigned" — PROTOCOL:113 ALREADY classes telemetry as
"1 Observation (SHEDDABLE)" and PROTOCOL:23-29 says the bare-UDP control
plane carries "class-1 telemetry" (loss absorbed by supersession, never
retransmitted) — so LIGHT telemetry/federation carriage EXISTS as law;
never-shed = classes 0/3/5 (claims shed NEVER, telemetry sheds FIRST).
What's genuinely NEW: HEAVY telemetry (bulk spans/metrics/logs + cold
archival) rides OPPORTUNISTIC BULK (PROTOCOL:132-135 "durable-plane
archival replication") under the non-interference law (CANNOT block
control/claims), and the OTLP-IN lane — both need transport-registry
classification (WIRE_SECURITY:146-153, else boot fails).** INTEGRATION
DECISIONS (per spec): OBJECT_TIER — hot ring = MUTABLE-SIDE node-local
(not in tier hierarchy; enters tier at SEAL); persistent-queue backing
= the STAGING ROLE (lease-reclaimed, scan-recoverable, not-yet-addressed
append buffer — near-exact fit, REUSE); cache-role for hot query; GAP =
NEW COLD-TELEMETRY DURABLE CLASS (class-at-root, boot-validated OT11,
**TTL-retention-governed NOT liveness-rooted** — unlike every current GC
root); EC cold tail applies. WAL — the queue REUSES WAL's durability
PRIMITIVES (derived-ω always-full, typed-retryable-never-block
backpressure, floor-API reclaim) but is NOT a ledger-WAL logical-log
client (content-never-in-WAL; telemetry = bulk content → OWN store on
WAL primitives, OFF the consensus commit path — avoids the MONARCH
circular-dependency: monitoring can't depend on the storage it
monitors); Branch-25 encrypt-at-rest flag named. PROTOCOL/WIRE — OTLP-IN
= registered warden-terminated vsock lane (like the SENSOR channel),
per-workload flow-key ⇒ guest-reported provenance STRUCTURALLY;
CONFLICT→content-free PROCESSOR (OTLP unbounded attrs/log-bodies vs
WIRE_FORMAT:117-127 inline-vs-reference law ⇒ ContentRef or reject/
bound, counted). PODS — agent tier ALREADY EXISTS IN EMBRYO (PODS:68-71
node rollup, T10 node-count-bound — the Collector FORMALIZES it as the
hot ring); warden+sensor = instrumentation SUBJECTS (two outputs). 
SCHEDULER — gateway IS a scheduled service, region-local, colo-unit-
ADJACENT (NOT a member); GAP = name the gateway placed-service class,
agent tier is host-infra-not-a-summon. CONSENSUS — **the Collector is
WRITER-LESS (append-only, any-copy, sharded single-OWNER not fenced) ⇒
does NOT enter the single-writer roster — EXACTLY what separates it from
the monitoring-plane single-writers (score service + detection-checkpoint
writer) that DO get region-scope-epoch classified**; GAP = still
explicitly classify the durable writers (CAS-first ref-flip for the
manifest; single-owner non-fenced queue) for chokepoint-coverage.
IAM — **`observability` resource type ALREADY EXISTS** (read_stream/
read_health/trace, PEP=health serving edge); §7.12 Scribe-its-primary-
only; ingestion = registered emission surface (provenance = contributor-
identity+epoch, influence advisory = the structural bar on guest-
reported ever being a detector input); OTLP-in authz via
peer_channel.send(telemetry_lane) warden-enforced per-frame (keeps
telemetry OFF the authority-object model); **IAM audit RIDES the
Collector** (IAM:434 "Branch-39 substrate: session stream / operational
stream" — the Collector is the SINK for IAM decision audit, two-stream
shape owed). HEALTH — H5 NOT violated (Collector ≠ a health subsystem);
the load-bearing re-source CONFIRMED (turn/stop/usage → provider gateway
host-observed + PROVENANCE column host-observed|guest-reported +
divergence-as-tamper-signal); content-free processor reconciles OTLP.
MONITORING/HANDOFF — **SEPARATION VERIFIED STRUCTURALLY (3 guarantees):
(1) provenance-class processor marks OTLP-in guest-reported "never
authoritative for detection" at ingest; (2) detection's DURABLE inputs
BYPASS the Collector entirely (WAL-logged ledger deltas + host-side
warden verdicts + provider-gateway host-observed usage read directly);
(3) the host-observed/guest-reported DIVERGENCE is itself a cross-view
tamper signal.** REGISTRY — ported factories → registry DESCRIPTORS;
config-as-DocValue (canonical closed-schema, replaces YAML); Guardian
staging for custom components. SESSIONS — collection NODE/REGION-scoped,
identity PER-SESSION; colo-unit: detection+score ARE members, Collector
agent-tier is NOT, gateway is ADJACENT; CONFLICT→serving-edge isolation
(collection node-SHARED, reads session-ISOLATED — the ledger metadata/
content-split pattern, IAM §7b). AUTOSCALING — agent tier structural-
per-node; gateway load-driven (signal = ingest-rate/fan-in-depth,
latency only via target-derivation); overload = SHED not block (class-1
sheddable) ⇒ maximal-collection bounded by retention-tiering+tail-sample
NOT producer-backpressure. N=1 NO-MODES: doctrine cited verbatim across
PODS(derived-param-never-mode)/OBJECT_TIER(§10 both-planes-collapse,
class-labels-inert)/WAL(ω→1, no-local-shortcut)/CONSENSUS(§8 1-voter ≡
N-voter, no-branch)/HEALTH + the telemetry law itself ("N=1 is a zone of
one running the identical binary"); THE COLLAPSE = two tiers → ONE
in-process pipeline (fan-in fan-out is a DERIVED-CARDINALITY parameter
reaching ZERO-upward at N=1, like hedged-reads→no-ops / warm-pool→~zero
/ cross-region→inert), durable spine = object-tier/WAL laptop-degenerate,
memory-bound collect-everything (9ns fast path), same encoder/processors/
schema, permanent N=1≡fleet CI gate. OWED (GAP register, 10 items): cold-
telemetry class; queue=WAL-primitives/staging-role-reuse-not-logical-log;
transport-registry classify 3 telemetry lanes; CONSENSUS classify the
durable writers (writer-less hot path stated); IAM emit-authz decision +
the audit-sink two-stream shape; HEALTH re-source amendment; content-free
processor exact rules; serving-edge session isolation; REGISTRY Collector
kinds + DocValue config; AUTOSCALING gateway scaling class; N=1 CI gate.
1 lane still out: A (OTel core + port work).

**COLLECTOR LANE A LANDED (2026-08-20): OTel CORE + PORT WORK — ALL 4
LANES NOW IN.** DECISIVE FINDING: **there is an OFFICIAL Rust OTel
pipeline engine — `otel-arrow` OTAP Dataflow Engine ("our new Rust
OpenTelemetry code base, a pipeline engine" w/ built-in OTAP+OTLP
receivers/exporters + batching/fanout/failover/retry/routing; crate
layout MIRRORS the collector: engine/core-nodes/contrib-nodes/pdata/
config/controller/channel) — the REFERENCE DESIGN + possible dependency**;
+ `rotel` (independent Rust collector, tokio, OTLP in/out) proves
viability; opentelemetry-rust = client instrumentation NOT a collector
(source of Rust OTLP proto types only). CORE DISTRO = **~12 REAL
components** (2 recv otlp/nop, 3 proc batch/memlimit/queuebatch, 4 exp
otlp/otlphttp/debug/nop, 1 conn forward, 2 ext memlimit/zpages) + the
framework; contrib ~240 = NOT the port target. W1 pdata = the in-mem
model every component operates on, a WRAPPER over OTLP proto structs
(keeps `orig` ptr); 3 ownership rules (no cross-instance aliasing;
explicit MoveTo/CopyTo; consume-then-forget = "after return, undefined
behavior to access"); MutatesData capability flag (default read-only) —
**Rust makes these COMPILER-ENFORCED (move=MoveTo, &mut/&=MutatesData)**;
OTAP chose a DUAL rep (OTLP bytes OR Arrow RecordBatch) for columnar
throughput. W2 graph = real DAG (gonum+topo-sort): recv→capabilitiesNode
→procs→fanOutNode→exps; shared recv/exp = ONE instance + fan-out;
**SYNC-COUPLED-FAN-OUT HAZARD VERIFIED IN CODE** (fanout = synchronous
sequential in-caller `for tc: ConsumeTraces` loop ⇒ a slow downstream
BLOCKS the receiver + backpressures every sharing pipeline); build =
topo then reverse (downstream-first); Start = reverse-topo (receivers
LAST), Shutdown = forward-topo (drain upstream first); Service IS the
component.Host. W3 component = {Start,Shutdown} + 5 kinds + StabilityLevel
ladder; ID=type+name; sealed Factory (functional opts WithTraces/Metrics/
Logs); `otelcol.Factories` flat registry (errors on dup); NO reflection
— explicit registration. W4 config = 5 component-maps + service block;
Config=any; confmap Provider/Converter/Resolver (env/file/http/https/
yaml). W5 connectors = pipeline-to-pipeline bridges (both exp+recv; the
ONLY cycle source → explicit cycle detection); extensions = lifecycle-
outside-pipelines (ordered start/reverse shutdown); STORAGE EXTENSION =
keyed byte-store backing the persistent queue (GetClient→Get/Set/Delete/
Batch, survives restart). **W6 THE PORT (grounded in OTAP): PORT the
valuable/correct pieces ~as-is — pdata (prost-proto-wrapper, discipline
compiler-enforced), graph builder (petgraph, keep capabilities/fanout
virtual nodes + connector dual-role + cycle detection), lifecycle
ordering (VERBATIM), factory/registry shape (traits + explicit
registration), confmap Provider/Converter/Resolver (over serde);
REPLACE the ONE weakness — the synchronous blocking fanout call-chain —
with OTAP-style BOUNDED ASYNC CHANNELS + explicit backpressure +
Ack/Nack/Config/TimerTick/Shutdown control messages. THE CRUCIAL
NON-OBVIOUS Go→Rust LESSON (OTAP-grounded): Go goroutines are ALWAYS
Send (work-stealing); naive port forces Send+Sync+'static on EVERYTHING
incl. pdata (painful/slow) ⇒ OTAP's model = THREAD-PER-CORE + !Send
LOCAL tasks + spawn_local (preferred), escalating to Send "shared
adapters" ONLY at true integration boundaries (e.g. Tonic receivers) —
"one single-threaded async runtime per assigned core, no work-stealing
in the hot data path, bounded channels not unbounded buffering." This
maps PERFECTLY onto hecate-rt (single-owner sharded tasks, bounded
channels, no cross-shard sharing).** STRONGLY consider otel-arrow/
otap-dataflow as prior-art-or-dependency vs re-deriving the async engine.
ALL 4 LANES IN ⇒ NOW SYNTHESIZE THE FULL SPEC-GRADE HECATE COLLECTOR
DESIGN (IAM/PODS granularity) + present in-message before write.

**COLLECTOR SPEC PRESENTED (2026-08-20) THEN PULLED BACK — USER AUDIT
FOUND 4 REAL GAPS + "lacks actual mechanics."** Full COLLECTOR.md spec
presented in-message (§0 shape/two-planes/two-tiers, §1 port-ledger,
§2 pdata→Rust compiler-enforced, §3 async-channel exec replacing sync
fanout, §4 component/factory/config, §5 two tiers, §6 OTLP in/out, §7
provenance-class + content-free processors, §8 durable spine, §9 maximal
collection, §10 trace-context, §11 carriage, §12 two-plane separation,
§13 placement/scaling/authz, §14 N=1, §15 instrumentation surface, §16
scale walks, §17 test matrix CO1-15, §18 acceptance, §19 corpus
amendments). USER AUDIT (verbatim-close): (1) **"we have NO queue
primitive… we lack cache primitives. We need to design a queue and cache
equivalent. Add these to the tree, they are next to design."** — the
design LEANED on "persistent queue" (OTel-internal) + "cache role"
(OBJECT_TIER-internal pack-volume policy, NOT a general primitive) as if
they were Hecate primitives; they are NOT. QUEUE + CACHE = NEW TREE
ITEMS, Collector dependencies, design-next. (2) "does this match Meta
scale? Do you need more research?" — HONEST AUDIT: shape holds (Scuba
proves the pattern) but 5 THIN SPOTS lack mechanics: gateway fan-in tree
is a SKETCH (no topology/sharding/rebalancing); aggregate cardinality at
scale unaddressed; tail-sampling-at-scale hand-waved (trace-aware
routing + num_traces×size×decision_wait memory at 1.3B traces/day);
cold-telemetry petabyte capacity model absent; NO query plane designed.
YES more research. (3) "account for distributed AND multi-region. Do you
need more research?" — YES; "region-local + federate upward" was a
HAND-WAVE; Monarch (Google planet-scale, zonal-autonomy + global query)
is THE precedent, undesigned. (4) "How should we handle sharding,
replication, durability?" — the cross-cutting MECHANIC that was missing;
Hecate HAS substrate (OBJECT_TIER copyset+EC, WAL Raft, SERVING HRW) to
reuse EXCEPT where telemetry's LOSSY-TOLERANCE differs from ledger
zero-loss. (5) "Should each session have its own collector?" — MY
ANALYSIS (to validate via research): NO — collection = INFRASTRUCTURE
(node agent + region gateway; node-rollup bounded by node-count not
session-count, PODS T10; sessions spread across nodes); session =
scope/read-isolation dimension at the SERVING EDGE (collection
node-shared, reads session-isolated — IAM metadata/content split); the
MONITORING plane (detection+score) IS per-session (colo-unit) but that's
the SEPARATE authority plane. (6) **"solid design but it lacks actual
mechanics"** = the core critique; the corrective = design the real
mechanics (sharding/replication/durability, the tree topology,
cardinality mgmt, tail-sampling routing, cold capacity, query plane,
multi-region federation) grounded in research. COLLECTOR SPEC STATUS =
PRESENTED-BUT-BLOCKED pending: queue+cache primitives designed +
Meta-scale/multi-region mechanics researched+designed + per-session
ruling. Core architecture (ported OTel, two planes, provenance/
content-free processors, N=1, the async-channel fix) STANDS; the gaps
are mechanics + primitives + federation. 3 RESEARCH LANES DISPATCHED
(each → mechanics + Hecate-design-rec): SCALE MECHANICS (a381c17c —
Monarch zonal/global + target-sharding + query tree, Cortex/Mimir/Thanos
ingester-RF/consistent-hash-ring/object-store-flush, tail-sampling
loadbalancing-exporter trace-ID routing, telemetry durability-tiers
lossy-tolerance, multi-region autonomy + the per-tenant-vs-shared
scoping answer); QUEUE PRIMITIVE (a3715779 — Kafka log-as-queue
partitions/ISR/offsets, SQS visibility-timeout/redelivery/DLQ,
exporterhelper persistent-queue crash-recovery, sharding/replication/
tunable-durability, on WAL/object-tier substrate); CACHE PRIMITIVE
(a6a3fa67 — W-TinyLFU admission + eviction, ARC/SIEVE/CLOCK, sharding,
sizing-from-anchors, reconcile OBJECT_TIER cache-role). On landing:
design QUEUE + CACHE specs, re-audit + design the Collector's Meta-scale/
multi-region MECHANICS, settle per-session, re-present all three.
TWO NEW TREE ITEMS: QUEUE primitive, CACHE primitive.

**LAPTOP-USECASE REMINDER (user, 2026-08-20): "Don't forget to also
research the laptop usecase (i.e. 'run on anyone's laptop')."** Stronger
than N=1-as-formula: the ZERO-EXTERNAL-DEPENDENCY, EMBEDDED, in-process,
minimal-footprint degenerate — NO separate collector process, NO
external object-store/Kafka/Redis/broker/cache-server, single-binary,
"just works" on a dev machine, SAME code path as fleet by DERIVED
PARAMETERS (no mode). Pushed as a required dossier section into ALL 3
running lanes via SendMessage (queued for next tool round): scale
(a381c17c — Prometheus-single-node-default / Mimir monolithic mode /
Grafana Agent embedded / the minimal single-binary story); queue
(a3715779 — embedded durable queue: exporterhelper-persistent-queue is
embedded single-file, sled/bbolt/SQLite-as-queue, Redpanda-single-node,
no broker); cache (a6a3fa67 — in-process bounded cache: Caffeine/**moka**
the Rust Caffeine-port as candidate dep, W-TinyLFU as a LIBRARY not a
server). Each must add a "run-on-anyone's-laptop (zero-dep/embedded)"
section + Hecate rec. FIRST-CLASS design constraint on all three
(queue/cache/collector), shaping the PRIMITIVES (embeddable, no external
service) not just their sizing.

**USER SHARPENED THE 2 PRIMITIVES (2026-08-20):** "cache/pub-sub
equivalent (think ValKey, but matches our global Meta scale AND local
laptop)" + "at-least-once message delivery (think SQS, but Meta scale
AND laptop)." ⇒ CACHE item is actually **CACHE + PUB-SUB (ValKey-
equivalent)** — KV cache + publish/subscribe in one, ephemeral
at-most-once pub-sub (invalidation/live-fanout/ephemeral coord) DISTINCT
from the durable queue; QUEUE item is **at-least-once message delivery
(SQS-equivalent)** — durable, visibility-timeout/redelivery/DLQ. Both
Meta-scale (Valkey Cluster 16384-slot sharding+replication / SQS) +
laptop (embedded moka+in-proc-bus / embedded durable log). Cache lane
(a6a3fa67) extended via SendMessage to add the pub-sub half (Redis/
Valkey pub-sub + sharded SSUBSCRIBE + cluster mechanics + moka; Streams
as the straddle; recommend one-family-vs-two). Queue lane already
SQS-targeted. Redis STREAMS informs the queue (at-least-once consumer
groups).

**SCALE-MECHANICS LANE LANDED (2026-08-20): MONARCH-GROUNDED, DECISIVE —
supplies the missing mechanics + SETTLES per-session.** (Completed
before the laptop SendMessage delivered ⇒ laptop addendum from
a381c17c PENDING.) **MONARCH (Google planet-scale in-mem TSDB, VLDB'20)
= THE precedent, validates Hecate at nearly every point:** zonal
(regional) AUTONOMY + global query/config planes = Hecate's autonomous-
local-first law VERBATIM ("local monitoring in regional zones combined
with global management and querying"; a zone "can work continuously
during transient outages of other zones, global components, and
underlying storage"); CAP = trades consistency for availability ("drops
delayed writes and returns partial data"); LOW-DEPENDENCY in-memory to
avoid "a potentially dangerous circular dependency" on monitored storage
(the Monarch trap, receipted). INGESTION = 2-level divide-conquer
(ingestion routers regionalize by LOCATION field → leaf routers
distribute by RANGE ASSIGNER); leaves = in-mem store + **BEST-EFFORT
recovery logs (NO ack-wait, async-replicated ×3 clusters)**. SHARDING =
TARGET-based (series keyed by monitored entity; location→zone;
**lexicographic target RANGES** = shard unit; Slicer-style range
assigner splits/merges/moves w/ recovery-log-mediated zero-loss handoff;
replicas across failure domains, 1-3 user-tunable). COLLECTION
AGGREGATION at ingest = cardinality collapse (36:1 typical, 1e6:1
extreme). QUERY = 3-level tree (root mixer→zone mixers→leaves) + **Field
Hints Index (Bloom-like) prunes fanout −99.5% zone / −80% root** +
PUSHDOWN (95% of standing queries complete ZONE-LEVEL) + streaming
scatter-gather w/ token flow-control + ZONE PRUNING (drop unresponsive
zone past soft deadline, return partial + notify) + hedged reads. SCALE:
38 zones, 950B series, 750TB mem, 2.2TB/s, 6M QPS, 144k leaves. SHARDED-
TSDB (Cortex/Mimir/Thanos/VM): consistent-hash RING + RF=3 + quorum
⌊N/2⌋+1 + WAL-replay-on-restart + flush-to-object-store-every-2h;
handoff-on-death = DEPRECATED (converged on RF+WAL); Thanos global-view
querier federates + dedups via replica-label; VM SHARED-NOTHING
(vmstorage nodes don't know each other); compactor DOWNSAMPLES (raw/5m/
1h) for fast long-range + per-resolution retention. TAIL-SAMPLING:
loadbalancing-exporter routes by trace-ID consistent-hash so all spans
→ one instance; 2-tier (agents→LB→tail); num_traces=50k circular buffer
× decision_wait=30s = the memory wall; Canopy (1.3B traces/day) shards
by TraceID (shared-nothing tailers), ingestion-time FEATURE AGGREGATION
not raw-query ("computationally infeasible"), completion via triggers+
timeouts, head-sample via distributed token-bucket (global+per-tenant).
**DURABILITY/LOSS RULE (receipted across ALL): hot tier = in-memory,
node-local or RF-replicated, BEST-EFFORT, loss-accepted-on-node-death;
cold tier = flushed/compacted immutable blocks in durable object store =
system-of-record, async off-hot-path. Replication/EC on COLD; hot trades
durability for latency/cost. TELEMETRY HOT WRITES MUST NOT WAIT ON RAFT/
derived-ω durable-ack — that reintroduces the MTTD cost Monarch rejects
⇒ the Collector's hot tier RELAXES Hecate's ledger-grade WAL to a LOSSY
model (the key divergence from the zero-loss ledger).** MULTI-REGION =
regional collection + global query federation; regions autonomous (work
if global down); prune unresponsive regions. **PER-SESSION SCOPING —
DEFINITIVE ANSWER, REFUTED: NO planet-scale telemetry system runs
per-tenant/per-session collectors; ALWAYS shared collection + query-time
isolation** (Monarch shared-service + per-user cgroups + memory-accounting
+ cancel-on-overuse; Cortex X-Scope-OrgID over shared ingesters; VM
accountID:projectID "data for all tenants evenly spread"; Canopy
per-tenant token-bucket on shared tailers). CONFIRMS my per-session
analysis: session = a LABEL on shared hot-ring + cold-blocks + serving-
edge isolated reads + per-session resource caps + optional shuffle-
sharding — NEVER a per-session collector. HECATE SYNTHESIS (W6, maps
cleanly): (1) gateway sharding = target/lexicographic-range for metrics
+ trace-ID-HRW for traces + collection-aggregation; (2) replication =
hot RF 2-3 in-region node-local-LOSSY quorum-ack (NOT Raft) + cold
OBJECT_TIER copyset+EC for flushed blocks; (3) durability 3-tier (hot
in-mem best-effort / warm node-local-WAL-derived-ω-for-loss / cold
replicated-EC + downsample); (4) query = root→region→node scatter-gather
fanout-5 + FHI-Bloom-prune + pushdown + region-local-ReadIndex reuse +
single-flight + hedged + region-prune + COMPLETENESS MARKER (non-
negotiable for a lossy plane); (5) multi-region = regional autonomy +
global federation on root/region Raft groups, no-synchronous-WAN-on-hot-
path; (6) per-session REFUTED → shared + serving-edge isolation. 2 lanes
still out: queue (a3715779), cache+pubsub (a6a3fa67); + laptop addendum
from a381c17c pending.

**SCALE LANE LAPTOP ADDENDUM LANDED (2026-08-20, a381c17c resumed):
"run on anyone's laptop" is RECEIPTED as the same-binary-config-derived
degenerate, NOT a stripped embedded build.** Prometheus = single-node
standalone IS the DEFAULT ("single server nodes are autonomous… no
reliance on distributed storage… rely on it when other parts of your
infra are broken"). **Mimir `-target=all` = THE no-mode single-binary
story: identical binary runs the whole write+read+store pipeline in one
process on a laptop AND fans out to a microservices fleet — only the
`-target` config differs** ("N=1 is a zone of one running the identical
binary" made literal). Prometheus Agent mode = SAME CODE forward-only,
"upward" (remote-write) is an INTERFACE engaged only when a target
exists ("same scraping APIs, same semantics, same configuration");
storage-integration is "a set of interfaces" not a rewrite. VictoriaMetrics
= "single small executable without external dependencies", single
`-storageDataPath` dir, memory-bound (7× less RAM). Scuba = memory-bound
derived eviction. NO-PRECEDENT for per-session/per-tenant PROCESSES on a
laptop — universally ONE in-process pipeline holding everything, memory-
bound, with upward/replication/object-store edges ABSENT when targets
absent. HECATE LAPTOP DESIGN (W6.7): the degenerate = IDENTICAL fleet
binary, config-derived wiring, distributed edges absent-because-targets-
absent — the HRW ring has ONE member (self) so routing is identity + no
separate collector process; upward set empty → standalone; OBJECT_TIER
cold blocks → local pack volume / single dir (copyset/EC → 1 local copy
by derived RF=1); **RF, region-count, fanout all DERIVE to 1 FROM RING
CARDINALITY — a derived parameter NOT a mode flag** (the Hecate-specific
framing, ingredients receipted); memory-bound derived eviction; same
query tree (root=region=node=self, pushdown/FHI no-ops but code path
IDENTICAL). THESIS (for the spec): "planet-scale telemetry is NOT a
distributed ledger — it is autonomous regional in-memory collection
(lossy hot tier, unreplicated) + best-effort node-local WAL + durable
cold EC blocks, region-local-first scatter-gather w/ Bloom fanout
pruning, sharded by target-key/trace-ID, tenant-isolated by label+quota
NOT dedicated pipelines, collapsing to one memory-bound in-process
binary on a laptop by driving RF/region/fanout→1 from ring cardinality.
Reuse OBJECT_TIER cold / SERVING-HRW rings / CONSENSUS region-local
ReadIndex — but DO NOT put the ledger's Raft-synchronous WAL on the
telemetry HOT path (the single most important reconciliation)." SCALE
LANE NOW COMPLETE (both extremes). STANDING REQUIREMENT (user,
2026-08-20): "enforce MAXIMAL COMPLIANCE with + IDENTIFY CONFLICTS with
existing specs; maximally correct/robust/performant/efficient; no fear
of complexity, NO shortcuts" — pushed into the 3 running primitive lanes
(queue/cache+pubsub/fanout) as a required "corpus compliance + conflicts"
section; the THOROUGH per-primitive corpus-reconciliation (Lane-D-style,
reconciler agents reading the actual specs) is the diligence pass owed
before each primitive spec is finalized. 4th PRIMITIVE ADDED: FAN-OUT
(SNS-equivalent, a9bd127b dispatched) — durable topic fan-out to many,
filtering, the SNS→SQS pattern; factoring question = own-primitive vs
router+queue+pubsub composition. PRIMITIVE FAMILY NOW: CACHE+PUBSUB
(ValKey), QUEUE (SQS at-least-once), FAN-OUT (SNS), all Meta-scale +
laptop. 3 lanes out: queue, cache+pubsub, fanout.
