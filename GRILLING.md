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
| `docs/specs/VFS.md` | one BLAKE3 CDC chunk store, manifests as layers, four volume roles (work volume/green/tools/scratch — scratch added by SERVING.md), virtio-fs serving, tool plane + 3 Guardian gates, content-addressed distribution |
| `docs/specs/PODS.md` | microVM pods, manifest-projection rootfs + DAX day-one all platforms, hecate-init 5 duties, warden+sensor (§6), warm tiers + reseed-on-resume, autoscaling classes (§4b; Architect=serialized-judgment), NO work-bearing memory ever persisted |
| `docs/specs/AGENTS_RUNTIME.md` | serial turn/instance, park-on-consult AND long tools, hold-teardown at human latency, brief+claims handoff (volume re-binds; no transcript), warden-topology skills, R-series |
| `docs/specs/RANK.md` | domain enums, derived bindingness, override-refuse as sole enforcement, score service (prevalence/specificity/trust, demote-only, observe-first). A1–A5 applied to LEDGER.md (single vocab; closed enums+bijection; retirement=custody transfer to Archivalist archive, anti-tombstonic; deadlines as replay inputs; layered scope map) |
| `docs/specs/SCHEDULER.md` | sharded deterministic evaluation-log spine; **deterministic optimism** (parallel intent-aware speculative planners, logged outputs, serial pure applier); content-keyed memoization + snapshot-page/chunk locality scoring; gang-at-admission; Borg bands, hard limits; §9b request lifecycle (amendment=supersession-with-reuse; disposition-retry partials; issuer judges sufficiency) |
| `docs/specs/SIBYL.md` | the 10th agent (name user-ratified): workstream judgment above sessions, lineage-partitioned instances (never global), judgment/machinery split, experiment-as-claim-tree, content-blind, grant brokering (Biscuit), user-plane ledger. AGENTS.md + glossary landed |
| `docs/specs/SERVING.md` | the serving machine (Branch 21, ACCEPTED 2026-08-16): two-representation law (per-pod log-structured overlay = journal + extent index; manifests-over-CAS everywhere else), ack=witness (group commit before reply, no fsck — recovery is replay), seal at increments (writeback drain → op-log derivation → CDC/BLAKE3 → CAS), green = manifest chain (extends never writes, EROFS structural, all-DAX shared pages, pin+re-bind), inode law (volume,path-entry stable per volume lifetime, serializable for handoff), digest-xattr honesty, weighted-HRW topology (chunk-groups + exception table, state-follows-compute, R_eff loud degenerate), mapping engine splice\|managed per platform, own FUSE-over-virtio layer on hecate-rt in the libkrun fork, scratch volume role. Riders landed: VFS.md (4th role + op-log clause), ADR-0005 amendment (one law: no auto-resolution anywhere; dispositions by author liveness), CONTEXT.md (Landing, Conflict value, Witness, Seal) |
| `docs/specs/SESSIONS.md` | ACCEPTED 2026-08-16 (verdict held for Branch 21, unblocked by SERVING.md): lineage first-class + single-holder fenced materialization lease; session = template-stamped isolation unit, per-session pods, home session hosts Sibyl; §3 physical contract = SERVING.md's machine; fork = O(manifest) + skeleton; three-layer landing engine (manifest prune → eg-walker replay as detector-only → jj conflict algebra, resolution-is-a-change); composition = declared-order pairwise, disjoint-or-verdict-clean + re-verification; resolver proposers version-pinned, validated, never silent; conflict deposits per-template; user review first-class (materialization = prompt + zero unresolved conflicts); 6-stage evaluation funnel with measured lifts (dedup/differential/hybrid/committee; composition-by-regeneration PDR; critic-gated early stopping); lifecycle fast-forward states; GC licensed by continuous exfiltration; scale-down floors ratcheted. Riders executed with SERVING.md commit |
| `docs/specs/LEDGER_CORE.md` | ACCEPTED 2026-08-16 (sub-decisions a/b/c; amended under maximal audit): single-owner core per session (ceiling priced + CI-measured), writer disjointness as struct layout, apply-on-ack with **effective-state checks** (arenas ⊕ pending, closes the pipelined-affordance/update-on-terminal race, L13 CI gate), per-parked-scope monitors + oracle fuzz (global SCC rejected as less verifiable; closure memory budgeted L15), no outbox — log+cursor projectors (typed RESYNC), event-carried score snapshots (bounded staleness priced), three-layer exactly-once stated (cursor + dedup window + content identity), retirement as PACED custody transfer (debt-driven interleave, never idle-work, L14), panics = evidence (catch_unwind → failure testament), L3 replay normalizes derived caches |
| `docs/specs/AUTOSCALING.md` | ACCEPTED 2026-08-16 (sub-decisions i ratio-law-only, ii scale-to-zero; amended under maximal audit): two instantiations (session + node) of one deterministic ratio target-tracking controller; signals restricted to LOAD-PROPORTIONAL classes (latency budgets enter via Little's-law target derivation, never as controller signals — architecture test); silence fails closed (freshness bound → hold + alarm, A11 gate); τ from ratcheted commissioning baseline, never continuously adaptive; asymmetric response + AIMD clamps + in-flight accounting; drain = graceful, parked scopes transfer via brief+claims handoff (A5 resume equivalence); scale-up through Guardian admission front door; work-driven roles get advisories to the Guide only (A8 structural); two loops at derived-apart cadences (A9 anti-resonance); decisions=logs, ledger=summon/teardown claims only, targets=config |
| `docs/specs/REGISTRY.md` v2 | ACCEPTED 2026-08-16 (amended under maximal audit, exact implementations): RawObject envelope, per-kind codecs the only typed boundary; **universal canonical encoding** — compiled kinds hecate-wire, schema-registered kinds via compiled `DocValue` type (i128 ints no floats, BTreeMap sorted-unique keys, dialect-proof hashing G11; closed schema subset, unknown keywords reject; append-only schema versions); three-state upsert (unchanged = zero writes); intent/observation split with resolvedSource carve-out; bundles = Merkle fingerprint + dependency snapshot + `resolved_at_revision`; **tenancy = scope-in-key** (Shipped\|Org\|User leading key component, authority in typed handles, publication = Guardian staging transition, G13 gate); **revision-floor reads** (session watch cursor as floor, serve_at_floor wait-or-forward, never stale, G14); storage = 6-op semantic contract (CAS put/get, ref-CAS sole mutation + unbypassable events, ordered scan, label index, forward/reverse ref index, event log) file-backed ≡ replicated (G10); external resumable watch (RESYNC discipline); Guardian staging = inventory-from-bytes content-bound approvals; no semantic search (pgvector fossil), no runtime authority, loud one-way doors |
| `docs/specs/SKILLS_API.md` | ACCEPTED 2026-08-16 (amended; USER CORRECTION captured: **TS/Python are authoring bindings, never runtimes** — no interpreter in any microVM): one Rust derive → five artifacts (wire codecs, MCP projection, skill:// resource, registry doc, dispatch glue — no second interpreter); bindings = registry-wide typed authoring SDKs generated from kind descriptors, output = canonical DocValue documents only, submitted via apply + Guardian staging; declared-skill invocation = COMPOSITION not code (closed DispatchTarget: Facade w/ pure field-mapping template \| ToolExec via provisioned Recipe — logic forbidden, static total verification at staging); arbitrary behavior enters only as provisioned tools through the tool plane; capabilities = closed harness-versioned bitset w/ compile_to_warden(), derived-not-trusted from dispatch targets (S9); built-ins stateless between invocations (lint); omission-is-absence surfaces, S6 count budgets; S1/S5/S6/S8 permanent (S8 = no-execution structural) |
| Architecture set | `docs/architecture/{AGENTS,SUMMONING,LEDGER,SKILLS,PLATFORM}.md`, `CONTEXT.md`, ADRs 0001–0005 — amended throughout this session (open roster/offices, Arbiter, summon-as-claim, retirement, work volume, ten agents) |

## ON THE TABLE (drafted + shown; awaiting acceptance — settle ONE at a time)

1. `docs/specs/HEALTH.md` — one plane (Sylk ran four); no authority.
2. `docs/specs/FOREST.md` — Z-set field engine, ACT-R/FSRS/MMAS/Parunak/PPR
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
- **Walking skeleton** — final branch; re-presents against completed tree
  (P0 wire → P1 runtime → P2 spine → P3 pod leg → P4 first agent → P5 first
  merged change; now must thread Sibyl/home-session/lineage into first light;
  each rung carries fault-matrix cells).
- Small owed: full "Guide summons" language sweep (key sites corrected; grep
  pass owed); ADR candidates (sessions/lineage+landing engine; deterministic
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
