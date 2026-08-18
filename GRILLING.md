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
