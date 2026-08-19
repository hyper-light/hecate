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
