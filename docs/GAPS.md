# The Gap Ledger — Branch 29 (authoritative, kept current)

Status: first full pass executed 2026-08-17 (direct read of every file in the
repo: CONTEXT.md, README.md, 5 architecture docs, 5 ADRs, 20 specs, GRILLING.md
complete). Rubric per the branch charter: research on file? spec exists? test
matrix? acceptance criteria? laptop degenerate stated? open decisions named?
Classification: `undesigned | designed-unspecced | specced-untested |
decision-open | drift (owed-and-forgotten)`. **A stale gap ledger is itself a
gap**: every branch acceptance, spec verdict, or tripwire firing updates this
file in the same change.

## 0. The one global fact

**No code exists.** The repo is docs-only (zero Cargo.toml, zero .rs). Every
spec below — including the nine ACCEPTED ones — is therefore
**specced-untested**: every "permanent CI gate" is an obligation, not a fact.
The walking skeleton has not started. This is the known, accepted state
("first light is far behind the wheel count"), recorded here so the ledger's
other classes are read against it.

## 1. Component inventory

| Spec | Status (header) | Tests | AC | Laptop degenerate |
|---|---|---|---|---|
| RUNTIME.md | presented (Br 1) | T1–T8 | 7 | implicit (shard formula) |
| WAL.md | presented (Br 2) | W1–W8 | 7 | implicit (1-replica group) |
| PROTOCOL.md | ACCEPTED 2026-08-18 | P1–P19 | 14 | yes (per-path MTU, P18) |
| MERGE.md | presented (Br 4) | M1–M12 | 9 | not stated |
| VFS.md | presented (Br 5) | V1–V11 | 8 | not stated |
| PODS.md | presented (Br 6) | T1–T19 | 13 | yes (formula-derived) |
| AGENTS_RUNTIME.md | presented (Br 7) | R1–R11 | 6 | not stated |
| RANK.md | presented (Exch 8) | K1–K8 | 5 | not stated |
| SCHEDULER.md | presented (§9b + heterogeneity amendment accepted inline) | SCH1–21 | 10 | yes (shard=1, SCH9 + SCH21) |
| FOREST.md | presented + PROVISIONALLY DIRECTED ×2 | F1–F21 (no F20) | 6+4b | §5b "local", not named laptop |
| SERVING.md | ACCEPTED 2026-08-16 | FS1–FS15 | 10 | yes (§6, AC-9) |
| SESSIONS.md | ACCEPTED 2026-08-16 | SES1–SES13 | 8 | yes (§9, SES11) |
| LEDGER_CORE.md | ACCEPTED 2026-08-16 | L1–L15 | 6+1b | n/a (WAL owns) |
| AUTOSCALING.md | ACCEPTED 2026-08-16 | A1–A11 | 5+1b | yes (AC-5) |
| REGISTRY.md | ACCEPTED 2026-08-16 | G1–G14 | prose | yes (§4, §5b) |
| SKILLS_API.md | ACCEPTED 2026-08-16 | S1–S9 | prose | not stated |
| HEALTH.md | ACCEPTED 2026-08-16 | H1–H8 | prose | not stated |
| SIBYL.md | ACCEPTED 2026-08-16 | WV1–WV10 | 6 | scale-to-zero only |
| OBJECT_TIER.md | presented (Br 24) | OT1–OT15 | 8 | yes (§10, OT15) |
| VECTOR_INDEX.md | accepted-in-session 2026-08-17 (see D-9) | VX1–VX12 | 6 | yes (§6, VX12) |

Architecture set (AGENTS/LEDGER/PLATFORM/SKILLS/SUMMONING + CONTEXT + ADRs
0001–0005): law-level, no test matrices by design.

## 2. Decision-open (blocking decisions, named owners)

- **D-1 Consensus (Branch 20) — the widest dependency in the tree.**
  Direction **RATIFIED 2026-08-17** after the user's etcd challenge was
  answered by the layer-classification dossier (every challenged failure
  mode traced to etcd-server/boltdb/watch, etcd-raft-library, or
  single-group-topology; the library record short and enumerable; Meta-scale
  practice table). Ratified form = the five decisions + four amendments:
  (2a) "CRDB-lineage dialect" exemplar naming, (2b) bug-record-as-
  conformance-suite, (3-addendum) explicit conf-change activation semantics
  + #12359 countermeasures, (5a) deterministic whole-cluster simulation
  gate. **CLOSED 2026-08-17**: `CONSENSUS.md` + `FAULTS.md` accepted and
  written with three in-exchange delta sets (split-brain assembly + the
  fabric-is-liveness-only law; actor-architecture position; cross-region —
  failure-domain tree, meta tree, epoch-scoping law, async content-only
  cross-region durability, FlexiRaft rejected for the meta plane).
  **Rider closed 2026-08-17**: the cross-region verification dossier landed
  (A–E confirmed on primary text; F+G corrected), §7 was reopened per the
  rider and re-settled with the accepted six-amendment set (FlexiRaft
  two-branch rewrite, lease-shadow law, externalization-fencing law, region
  rejoin protocol, async-pole honesty, receipts strengthening; CN15/CN16 +
  F7a–d). Branch 27 narrows to the §6 writer-roster audit at build time. Consumed by: WAL §5 (the only commit
  path "at every replica count"), SERVING §6 inventory map, SCHEDULER §1 meta
  group, REGISTRY §5 replicated revision (which dangles a reference to the
  nonexistent `CONSENSUS.md`), OBJECT_TIER §4 placement map, LEDGER_CORE §2
  append API. Branch 27 (leader-election revisit) deliberately re-derives part
  of its scope — settle together.
- **D-2 `WIRE_FORMAT.md` — CLOSED 2026-08-17.** `WIRE_FORMAT.md` +
  `TRANSFER.md` accepted and written ("accepted for the sake of output");
  PROTOCOL §6's process gate is satisfied, PROTOCOL §4 carries the
  flow-control amendments, OBJECT_TIER §2 gains the staging pack role.
  Branch 26 (multi-modal media) narrows to content **policy** only:
  class-assignment, content-type verification, EXIF hygiene, parser
  sandboxing, the per-class chunk-policy table, media descriptor documents —
  it inherits a settled transport.
- **D-3 Encryption × dedup — CLOSED 2026-08-17** ("approved."): OBJECT_TIER
  §9 settled — scope-salted convergent encryption validated against the
  full attack literature, four hardenings as law (256-bit random salt +
  BLAKE3 keyed mode; write-closed global domain + possession-proof IDs;
  chunk-size hygiene w/ the eprint 2025/558 caveat; crypto-erase hierarchy
  killing derivability), RCE split recorded as tripwire option, DupLESS +
  no-dedup rejected with receipts, OT16–OT19 added, AC-6 lifted (gate now
  practical: hardenings implemented + tests green). Branch 25 inherits the
  wrap structure; Branch 28 sits above, untouched.
- **D-4 FOREST whole-spec verdict.** Retention + retrieval hybrids
  PROVISIONALLY DIRECTED; full acceptance gated on reconciliation against
  ECOLOGY/EMERGENT_FOREST/EMERGENT_AGENCY — **files that live in the Sylk
  repo, not this one** (import or pin them, or the gate is unauditable here).
- **D-5 Branch 14 (handoff detection math).** HEALTH.md carves out context-fit
  accounting + threshold derivation for it by name; AGENTS_RUNTIME triggers
  and the Scribe's central duty rest on it. Research LANDED ×2 (GRILLING
  reports section: Sylk post-mortem — 0 performance handoffs in 9,780 WAL
  observations over 3 months; detection-literature verdict = risk-adjusted
  CUSUM). **The spec is what remains owed** — the five-tier pipeline exists
  only in a research report.
- **D-6 Branch 22 graph side.** Vector side spec'd (VECTOR_INDEX.md); the
  Glean-lineage stacked-DB exchanges remain open; FOREST symbol marks are
  "absent until then." Includes the OPEN vorpal instance-model decision
  (embedded-lib vs session worker vs KG-service pod) and the upstream patch
  list (Manifest::from_entries, content-source hook, xxh3 I3, scoped-interner
  R1, knob parameterization).
- **D-7 — CLOSED 2026-08-18**: LEDGER.md §7.3 rewritten (PSK/mTLS text
  deleted; defers to PROTOCOL.md + WIRE_SECURITY.md), ADR-0002 corrected —
  in the PROTOCOL acceptance commit. Branch 25 keeps rotation cadence,
  at-rest encryption, padding/traffic-shaping, grants.
- **D-8 — CLOSED 2026-08-18**: home assigned = Branch 25 (grants are
  authn/authz material, not envelope machinery); SIBYL's citation corrected
  in the PROTOCOL acceptance commit.
- **D-9 VECTOR_INDEX.md status confirmation.** The design was approved
  in-message and the spec written on "do it" — but standing rule 2 (specs
  shown in-message before file write) was not literally followed for the
  formatted spec. The header says ACCEPTED; the user should confirm or demote
  to presented. (OBJECT_TIER.md correctly says presented.)
- **D-10 Transport re-ratification: QUIC+UDP primary, bare-UDP control plane
  — ACCEPTED 2026-08-17 ("D-10(a)-(e) accepted" — user, in-session), sub-items
  (a)–(e) ratified as the reconciliation work plan.** Direction:
  QUIC-over-UDP replaces TCP frames as the primary reliable carriage for every
  ordered/directed/bulk class (turn streams, delta streams, consults, claims,
  directed commands, secrets issuance, registry ops, content transfer —
  upload/download/repair/replication, cross-region included); the existing
  stateless UDP datagram protocol remains as the *separate* lightweight plane
  for consensus votes/membership/fencing probes/liveness/telemetry/gossip
  (Raft = UDP; placement map/membership = UDP). The user is protocol-wise an
  agent like any other — no separate edge stack. Open reconciliations, each a
  blocking sub-decision: (a) **CLOSED 2026-08-18** — settled ("accepted.") after a
  six-round grilling arc, mechanics verified (dossier on file), and
  **`docs/specs/WIRE_SECURITY.md` written** (staging device, copy-once
  invariant, flow keys, hop classes, guest path, boot classifier,
  P-a1..P-a5 plan) (per-pod-QUIC → host-terminated → in-guest-seal
  three-leg → seal-once lanes → warden-seals-what-it-inspected →
  ingress-tamper audit → generalized five-layer default). The settled form:
  **Handshake**: Noise-IKpsk2 owned handshake in QUIC CRYPTO frames (nQUIC
  blueprint; spec-named verified suite — 25519/AESGCM-256/SHA-256-or-BLAKE2s,
  NOT BLAKE3 in-handshake for proof fidelity; one-hash law governs content
  identity only); private QUIC version + private Initial salt (RFC 9000 §7
  sanctioned); IK message-1 replay rule + QUIC Retry/address-validation as
  law; 0-RTT = closed list of replay-safe frame kinds; derived AEAD rekey
  thresholds from RFC 9001 formulas; key-phase update (routine) vs full
  re-handshake (identity/handoff) never conflated. **Keys**: one summon-mint
  root per pod, HKDF-labeled derivations (control-plane envelope, flow keys),
  key_epoch bump at handoff rotates all atomically; per-flow end-to-end keys
  brokered by hosts as minting authorities; SENDING GUESTS HOLD NO TRANSPORT
  KEYS. **The seal-once pipeline (1 payload seal + 1 payload unseal, the
  physical floor; hosts do payload-integrity only, never payload
  encryption)**: guest posts frame plaintext to a staging ring in its own
  RAM → WARDEN reads it in place (VMM page access, full plaintext, zero
  crypto, pre-seal) → verdict → **the warden seals those exact bytes**
  (TOCTOU/approve-then-swap structurally impossible; a rooted guest has no
  path to any wire except the warden's own seal — no egress stamp needed)
  → our private QUIC version carries sealed payloads WITHOUT re-encryption
  (sealed-payload frame class) → intermediate hosts route/admit on
  hop-authenticated cleartext AAD → destination guest holds the flow
  receive key and unseals. **The metadata-completeness law**: every warden
  verdict anywhere is decidable from typed envelope metadata alone (opaque/
  encrypted payloads are the norm — content-free doctrine applied to
  enforcement); payload plaintext may tighten (sensor discipline) but never
  be required; escalation decrypt = minting authority's deliberate LOGGED
  act, never fast-path (NSA-TLSI class stays excluded). **The five-layer
  default, ALL connections both stacks** (user: "make this robustness the
  default for *all* of our quic + udp connections"): (1) every hop
  authenticated by its strongest mechanism — session AEAD/MAC on wire hops,
  structural channel identity on virtio/in-process, equivalence stated as
  law; (2) end-to-end flow authenticity wherever an end exists, tag = final
  authority; (3) EVERY acceptance point (host parsers, guest unseal points,
  terminal clients, bare-UDP datagram parsers) is a parser-resident
  enforcement point running the §1.3 order with categorized counters;
  (4) replay discipline at both layers (hop packet numbers/nonces + per-flow
  endpoint windows); (5) per-lane payload integrity derived from recovery
  story — claims payloads under the hop MAC (transport retransmit preserved,
  GHASH-only), bulk exempt (name-verify + missing-set IS the recovery),
  supersession datagrams neither. **Boot classifier**: every socket/session/
  stream-class/flow classified against the stack at boot; unclassified
  transport path fails startup (chokepoint-coverage law applied to transport
  security). Ingress-tamper audit closed: on-path envelope forgery/
  decryption-DoS die at hop MAC before admission logic; admitted-vs-sealed
  divergence = typed alarm. Traffic-analysis (sizes/timing under encrypted
  payloads) = named Branch 25 rider (padding/shaping). Virtio work
  authorized (staging ring + doorbell in the libkrun fork). External-egress
  caveat: guest-held TLS policed at destination/policy level as accepted.
  Rejected along the arc, receipts on file: external-PSK TLS (rustls gap),
  RPK TLS (drags the TLS machine), bespoke non-Noise handshake (gQUIC's own
  retirement), per-pod QUIC endpoints (redundant with virtio physics THEN
  superseded by in-guest→warden-seal evolution), three-leg per-hop AEAD
  (deleted: cost made structurally absent), egress-stamp variant (TOCTOU),
  unauthenticated-envelope ingress (the audit's hole). D-7 resolves into
  this settlement (LEDGER §7.3/ADR-0002 corrections ride the PROTOCOL
  amendment). Test matrix: forgery/replay/decryption-DoS/corruption-per-
  lane/divergence suites run against EVERY endpoint class under cluster-SIM
  nemeses; coverage-matrix boot check permanent; one-seal-one-unseal
  structural audit; pre-seal inspection ordering instrumented; escalation-
  decrypt audit trail zero-on-fast-path;
  (b) **SETTLED 2026-08-18 ("accepted.")**: **owned `hecate-quic`** — pure
  core written to the RFC 9000/9002 dialect as exemplar (the consensus-core
  2a/2b pattern verbatim: dialect named, quinn-proto/quiche = reference
  implementations for READING, exemplars never dependencies); scope = the
  archetype subset only (streams, loss recovery, Cubic-class CC + pacing,
  dual-level flow control, datagrams, connection migration, WIRE_SECURITY
  keying hooks — no TLS, no h3, no public-QUIC interop); conformance suite
  = RFC 9002 pseudocode as executable reference tests + quinn/quiche/mvfst
  documented-bug checklist as named regressions + interop-runner scenario
  shapes adapted to the private version + loss-recovery property fuzz
  THROUGH the transport under cluster-SIM nemeses. Adoption rejected on
  law-compliance (no-panic, lint wall/Bytes-Arc in hot path, IO-as-data,
  conformance obligation) + the packet-layer divergence voiding adopted
  maturity exactly where we change it (sealed-payload class, GMAC lanes,
  Noise handshake); fork-quinn = dominated middle (iroh/noq trajectory as
  receipt). Ledger: loss-recovery/CC subtlety = the one genuine risk,
  mitigated by pseudocode-as-tests + seed-replayable SIM (the owned-
  consensus-core posture); wheel count +1 acknowledged; (c) **SETTLED-BY-CONSTRUCTION 2026-08-18**: the batching/ACK-frequency
  items are `hecate-quic`'s own ratchet gates (P-a4); (d) **SETTLED
  2026-08-18 (user, verbatim): "no fallback. Period. QUIC + UDP over TCP
  utilizing the standard(s) we just designed."** — TCP exists NOWHERE in
  the mesh: no tunnel, no tripwire contingency (my telemetry+contingency
  recommendation overruled — recorded per discipline); the terminal edge
  is QUIC/UDP like every other participant; RUNTIME §5's provider-egress
  h2/1.1 is unaffected (external APIs are their wire, not our mesh);
  (e) **ACCEPTED 2026-08-18 ("fine")** — executes as the PROTOCOL.md
  whole-spec re-presentation (A1–A6 + the D-10 rewrite: TCP stack deleted,
  two-plane UDP carriage, WIRE_SECURITY key model, archetype/lane
  classification + boot classifier, TRANSFER/FAULTS/WIRE_FORMAT
  cross-amendments, D-7/D-8 reconciliations same-commit). Rationale anchor: the workload is bursty/concurrent/low-bandwidth-
  exposed (agent swarms, laptops, multi-region) — the regime where the QUIC
  receipts (HOL independence under loss, connection migration, multiplexed
  streams, edge-measured wins) bind, and the TCP storage-census receipts
  (fat clean stable links) do not.
- **D-11 Cross-node attach to the post-merge shared VFS volume — undesigned
  (user-flagged 2026-08-17: "have we even discussed the mechanics — we
  haven't").** SERVING.md/VFS.md treat work-volume journals as node-local;
  nothing specifies how pods on *different nodes* attach to a shared
  post-merge volume: attach protocol, single-writer vs multi-reader fencing,
  cache coherence vs sealed-manifest snapshotting, transport carriage (bulk
  chunk fill = QUIC streams per D-10; invalidation/lease control = which
  class?), laptop degenerate. Needs a branch and a spec home (SERVING.md
  rider or its own); settle before the serving plane is implemented.
- **D-12 The distributed forest substrate — undesigned, research directed
  (user-corrected 2026-08-17: the forest is an external computational-biology
  and ML-driven substrate that IS distributed; a first "nobody queries a
  remote forest" settlement attempt was rejected as an invented falsehood).**
  User-sketched candidate: the field runs as a process **within every agent
  pod of a session**; changes propagate among nodes via gossip and/or Raft;
  the priced downside is convergence lag (a session's pods' forests take time
  to become consistent). Directed research before settlement: **peer-to-peer
  machine learning** (gossip/decentralized learning, convergence guarantees)
  and **consensus** (what, if anything, in the forest needs agreement vs
  eventual convergence); **federated learning** added 2026-08-17, with the
  stated preference (same date) to **eschew centralized coordination** — most
  FL requires a coordinating server, so FL receipts serve as the priced
  counter-case (what coordination buys) and as transferable aggregation math,
  never the candidate architecture; decentralized candidates (gossip
  learning, D-PSGD-class, stigmergy-native propagation) are the primary
  class, and session membership/fencing already provides the membership
  substrate gossip needs. Design tensions to resolve against receipts:
  per-pod replication vs FOREST.md's single field service + F10 determinism
  (note: the Z-set weight algebra is commutative and the input clock
  `(HLC64, stream_id, stream_seq)` already defines a total order — delta
  dissemination with order-independent apply may give deterministic
  convergence without consensus; hypothesis, untested); which forest events
  (promotion? curation?) need authority vs propagation; carriage per D-10
  (gossip = bare-UDP plane, ordered delta exchange = QUIC); cross-region
  posture; laptop degenerate (one pod = trivially consistent). Settle with
  FOREST.md's pending whole-spec verdict (D-4).

- **D-13 Resource-kind vocabulary derivation pass — CLOSED 2026-08-18.**
  Pass executed (PODS, OBJECT_TIER, SERVING, VECTOR_INDEX, Branch 23/34
  charters swept); v1 vocabulary minted and written into SCHEDULER §5a:
  `cores`, `mem` (PODS §2 role profiles + Branch 38(b) microVM overhead),
  `storage_cap(nvme)` (Branch 37 summon budget charge + OBJECT_TIER
  capacity formulas), `storage_write_bw(nvme)` (OBJECT_TIER endurance
  budget — dual-reader: admission accounts, OT13 servo enforces).
  Boundary calls recorded: repair/scrub IOPS NOT minted (fleet-plane
  pacing, no summon-time consumer); accelerator kind structurally
  provided for, UNMINTED until a Hecate-hardware consumer exists (none in
  tree — agents use provider-side models; forest/vector are CPU/SIMD).
  Matched-only attributes confirmed: cpu_gen/ISA, region, plane role.
  Discriminator law ("can two pods exhaust it?") + no-label-beside-counter
  now SCHEDULER §5a text, enforced by AC-9/SCH18.

## 3. Undesigned (open branches, charter only)

15 steering · 17 remote client/terminal (the entire presentation plane —
no spec anywhere) · 18 continuity/conversation · 23 document DB ·
25 wire security · 26 multi-modal media · 27 leader-election revisit ·
28 secrets · 30 fleet fault detection/recovery · 31 replica handling ·
35 git-compatible code hosting · 36 attachment lifecycle mechanics ·
37 volume provisioning (both planes) ·
39 observability plane + mesh/pod telemetry integration ·
32-WIDENED node provisioning + abstraction expansion · 38 the laptop
collapse (whole-system scale-down map + no-modes validation + degenerate
sweep of the inventory's not-stated column) ·
32 node lifecycle · walking skeleton (final).

**Unbranched gap found by this pass**: the **provider gateway** — LLM request
shaping, streaming, retry/backoff, rate limits, provider errors, failover
mechanics. PLATFORM §2/§3 state the law (one ModelConfig authority; failover
semantics) and RUNTIME §5 gives it a thread pool, but no branch or spec owns
the machinery. Every agent turn crosses it. Recommend: new branch, or fold
into Branch 14's execution half.

## 4. Drift (owed-and-forgotten) — corrected or to-correct

Corrected in the same change as this ledger's first pass (mechanical
doc-sync, no design content):

- **C-1 Fabric vocabulary** (ratified: the fabric plane is deleted; "shared
  façades" replaces "fabric façades"): AGENTS.md §3.8 ("and the fabric") + §4,
  SKILLS.md §5 + §6 heading, SKILLS_API.md §3 — swept.
- **C-2 RANK.md §2** "one synchronous query to the score service" contradicted
  ACCEPTED LEDGER_CORE sub-decision (c) (event-carried snapshots; "no
  synchronous query escapes the core") — aligned to snapshots.
- **C-3 ADR-0002 stale pointer** ("specification lives in LEDGER.md §7") —
  now points at PROTOCOL.md; LEDGER.md §7.3 annotated that PROTOCOL.md §2 is
  the ratified key model pending Branch 25.
- **C-4 AGENTS.md** "The nine agents in this document" vs the ten-agent
  roster — corrected to ten.
- **C-5 VFS.md §7** "registry (open branch)" — REGISTRY.md has been ACCEPTED;
  reference updated.
- **C-5a CONTEXT.md L3** "hosts a fixed roster of agents" vs the ratified open
  roster (AGENTS.md L3, REGISTRY custom agents) — corrected to open roster.
  Note the authority inversion this fixed: AGENTS.md defers to the glossary
  ("where this document and the glossary disagree, the glossary wins"), so
  the stale glossary line was technically law.
- **C-5b SUMMONING.md admission rule** "the roster is closed; a summon naming
  anything else is refused" vs open roster — corrected to registry-known
  (shipped or Guardian-staged custom).
- **C-5c Retired-"workspace" sweep** (SESSIONS.md AC-2 grep gate, standing
  rule 7): live design-vocabulary uses swept in AGENTS.md (×3), SUMMONING.md
  (×4), SKILLS.md (×2), and SESSIONS.md §3 itself ("Session workspace
  state"). Code identifiers (`Capabilities::WORKSPACE_RW`) and Sylk
  historical mentions left as-is.
- **C-5d GRILLING bookkeeping**: VECTOR_INDEX.md added to the SETTLED table
  (it was recorded only inside Branch 22); OBJECT_TIER.md added to ON THE
  TABLE (it was recorded only inside Branch 24); Branch 21's stale trailing
  "Next: (b) overlay representation" pointer annotated as history.

Remaining drift, needs a decision or a sweep (not mechanically safe):

- **C-6 Branch-label collision**: SERVING.md and SCHEDULER.md both claim
  "grilling Branch 21." History knows which is which; the labels should be
  disambiguated once in GRILLING.md.
- **C-7 Status-line authority**: GRILLING's SETTLED table lists RUNTIME, WAL,
  PROTOCOL, MERGE, VFS, PODS, AGENTS_RUNTIME, RANK, SCHEDULER as settled while
  their file headers still read "presented for acceptance." One authority must
  win; recommend updating headers upon explicit acceptance verdicts, and until
  then reading the table as direction-settled rather than spec-accepted.
- **C-8 Test-ID hygiene**: RUNTIME and PODS both use T-prefixed IDs (T1–T8 vs
  T1–T19); FOREST skips F20 and keeps F12–F14 in prose; PODS T18/19 and
  SCHEDULER SCH13–15 live outside their matrices. Cosmetic until cross-spec
  citations ambiguate; fold into the next touch of each file.
- **C-9 "Work plan on file" phrasing**: GRILLING says "Work plan W1–W7 on
  file" (vector) and "S1–S8 on file" (object tier) — the plans' substance is
  baked into the two specs, but no standalone plan artifact exists in the
  repo; the phrasing should not imply one.
- **C-10 ADR hygiene**: the five ADRs carry no Status/Date headers; four
  offered ADRs remain unwritten (sessions/lineage+landing engine,
  deterministic optimism, forest, open roster/offices) — and this pass adds
  two candidates: the two-planes object-tier verdict and
  TS/Python-as-bindings-never-runtimes, both user-corrected one-way doors
  currently recorded only in GRILLING/spec prose.

## 5. Residual magic-number surface (against the derivation doctrine)

- WAL.md acceptance factors: recovery ≥ **0.5×** device read bandwidth,
  throughput ≥ **0.8×** model, macOS ack ≤ **1.5×** measured, model-vs-measured
  within **20%** — multipliers over measured anchors whose own values carry no
  derivation.
- The shared "**>10%** regression fails CI" bar (RUNTIME, MERGE, PODS,
  SCHEDULER) — one hand constant repeated four times.
- RUNTIME.md provisional ≥1M cycles / ≤1µs p99 — explicitly flagged
  provisional-pending-baseline (compliant, listed for completeness).
- SERVING.md `reclaim_headroom(20 ranges)` — the weakest derivation in that
  file by its own framing.
- FOREST.md PPR α = 0.15 — flagged canonical-start + re-fit milestone
  (compliant, listed).

Disposition: each either gains a derivation at its definition site or is
explicitly ratified as a shape constant; the ledger tracks them until then.

## 6. Fit-before-influence milestones (cannot activate without data campaigns)

- FOREST AC-4: co-fit of both retention halves from Hecate's own event
  stream — observe-mode is mandatory until it exists.
- VECTOR_INDEX §7/AC-3: lineage-scale recall/latency fit precedes any recall
  claim; SOAR-variant gate (VX11) rides the same harness.
- Every ratcheted floor and commissioning-derived τ across the corpus assumes
  a **first CI baseline** that requires running code (see §0).

## 7. Armed tripwires (metrics must exist from day one)

ADR-0005/MERGE: p99 intervening-deltas-per-merge reopens eg-walker; MERGE:
rebase-livelock rescoping; SERVING §3: overlay index-rebuild vs pod-resume
budget reopens the checkpoint decision; VECTOR_INDEX §5: predicate-selectivity
reopens filtering; PODS §4b: Architect consult latency ⇒ record-replicas;
PODS §2/AC-4: WHP/HVF DAX is in-scope fork work, tracked.

## 8. External dependencies and port hazards

- **libkrun fork**: three-platform DAX + splice (WHP the risk cell) — unbuilt,
  day-one required by PODS AC-4 / SERVING §7.
- **vorpal upstream patches** (Branch 22 list): 4 commits incl. xxh3 identity
  (I3) + scoped interner R1; process-wide interner is the named multi-session
  hazard until landed.
- **Sylk port hazards** (component survey, on file): BeamSearchBBQ never
  traverses the graph it builds; deterministic RNG machinery exists unused
  while live paths use unseeded rand; maintenance signals trigger nothing;
  IVF WAL unwired in one of two places. The VECTOR_INDEX build (W1) must
  treat the Sylk code as architecture-reference only — none of these can
  survive the port.
- **FOREST reconciliation corpus** outside this repo (D-4).

## 9. Blocking order toward the walking skeleton

1. ~~**D-2 WIRE_FORMAT.md**~~ CLOSED 2026-08-17 (`WIRE_FORMAT.md` +
   `TRANSFER.md` accepted; P0 wire unblocked by process rule) →
2. ~~**D-1 CONSENSUS.md + FAULTS.md**~~ CLOSED 2026-08-17 (specs accepted
   and written; §7 receipts-verification rider open; Branch 27 → roster
   audit) →
3. Accept-or-amend the presented foundation set (RUNTIME, WAL, PROTOCOL —
   C-7's status authority) →
4. First code: runtime + SIM + wire (P0/P1), turning §0 from fact into
   history and §5/§6's baselines into numbers →
5. D-5 (Branch 14), ~~D-3~~ (closed — §9 hardenings must be *implemented* +
   OT16–OT19 green per the practical gate), Branch 25 — before agents run
   against real providers with real content →
6. Everything else per the branch tree; this ledger re-audits at each rung.
