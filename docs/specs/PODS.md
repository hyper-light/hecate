# SPEC: pods — VMM control, guest boot, and the warm tiers

Status: presented for acceptance (grilling Branch 6; 6a/6b/6c ratified with the
two-ends clauses). References: isolation research and Tool VFS survey on file
(GRILLING.md); krunvm virtio-fs-root pattern; Apple Containerization `vminitd`;
AWS Lambda/SnapStart snapshot density pattern; Nydus/Kata chunk-served images.
Companion: `SUMMONING.md` (lifecycle), `VFS.md` (store/serving), `PROTOCOL.md`
(channels, keys).

Scale doctrine: every laptop-vs-fleet difference in this spec is a **derived
parameter, never a mode**. One formula family sizes pools, cadences, and tiers from
measured anchors at both extremes.

## 1. The pod, physically

A pod is one microVM (forked libkrun family: KVM / HVF / WHP backends, ADR-0001)
running one agent. Its world:

- **vCPU/memory**: fixed at summon, derived from role profile + host capacity;
  resized only via handoff (config reaches live work exclusively through handoff).
- **Devices**: virtio-fs (mounts), virtio-vsock (channels), virtio-net (egress via
  the host user-space network stack — the Guardian chokepoint). Nothing else.
- **Identity**: pod uid, per-pod HKDF keys, fencing identity — all bound at
  **assignment**, never present in pooled or snapshotted state.

## 2. Boot: rootfs is a manifest projection (6a)

- The guest root filesystem is a **read-only manifest projection** served over
  virtio-fs from the unified chunk store (`VFS.md`). A guest image *is* a manifest;
  building one is composing manifests; updating one is publishing a new hash. There
  is no block-image pipeline in the tree.
- Guest-writable paths (`/tmp`, scratch, `$HOME`) are guest-side tmpfs bounded by
  the VM's memory allocation. Nothing writable is served from the root projection.
- Mount set at boot: root projection (RO) + work volume (RW overlay) + green
  base (RO) + tools composition (RO) — per `VFS.md` §5.
- **Scale clauses (required, not optional):**
  - Serving tasks are shard-multiplexed: host-side serving cost scales with *active
    operations*, never with pod count.
  - **DAX / shared-mapping** for RO layers: clean pages of shared content (base
    distro, toolchains) are backed by one host copy across all guests on the node.
    If the VMM fork lacks mature DAX, it is fork-roadmap work, tracked — not waived.
  - Read-path baselines (cold stat storm, compiler file-walk corpus) are ratcheted
    CI floors per platform.

## 3. `hecate-init` (6b)

PID 1 in every guest: a tiny static binary whose version is its image manifest hash.

Contract (exhaustive — init does nothing else):
1. Mount the declared mount set; verify against the bundle manifest.
2. **Reseed on start and on every snapshot resume** (§5): VM-generation bump
   observed → reinject kernel entropy, resync clock, **verify the sensor channel is
   live (§6)**, only then proceed. A pod whose sensor won't come up fails summon
   validation loudly.
3. Spawn the agent runtime process with its bundle; reap children.
4. Report lifecycle events and resource telemetry on the control channel.
5. Execute shutdown/abort orders (graceful drain, then hard stop).

- **Two vsock channels**, both speaking the framed protocol (`PROTOCOL.md`):
  - **control** (harness ↔ init): Control class, admission-reserved; spawn, health,
    shutdown, telemetry.
  - **agent** (agent runtime ↔ claims plane + MCP): per-pod keys, standard envelope.
- **Trust posture**: init runs inside the trust boundary of an untrusted workload. A
  compromised agent owns init's process space; therefore nothing init can send grants
  authority the pod does not already hold — the harness treats every control-channel
  input as hostile (fuzzed as such, P-series tests), and policy lives host-side only
  (device surface, network stack, Guardian). Init is mechanism, never authority.
- **Telemetry rolls up at the node**: the host harness aggregates its own pods'
  liveness/resource telemetry; cross-node health rides the gossip plane piggybacked
  under the MTU budget. Cadence is derived and adaptive. No pod ever heartbeats a
  central control plane directly — fan-in is bounded by node count, not pod count.

## 4. The warm tiers (6c)

Preference order, tier choice and sizes derived per node from measured anchors:

1. **Warm live pool** — booted, *generic* (unassigned) VMs per role class. Pool size
   derives from observed summon arrival rates (Little's-law style, decayed); on a
   laptop the formula correctly yields ~zero and tier 2 dominates — same formula,
   both extremes.
2. **Snapshot-resume** — post-boot, **pre-assignment** snapshots; resume is
   ms-class. Resumed VMs map the snapshot memory file **copy-on-write**, so N clones
   share every clean page of one snapshot — the density mechanism at fleet scale,
   and the zero-idle-memory mechanism on a laptop. Snapshot files are operational
   artifacts (host storage, content-hashed) containing only generic boot state.
   **The snapshot API is structurally pool-tier-only: it refuses assigned pods. An
   assigned (work-bearing) pod's guest memory is never persisted to host storage by
   any mechanism — in-progress work cannot reach disk through the warm tiers.**
3. **Cold boot** — the floor (~100–200ms class), never the steady-state path.
- **Assignment binds identity**: keys, pod uid, volumes, bundle, fencing identity
  attach at assignment; pooled/snapshotted state is provably generic (a pooled VM's
  filesystem and memory contain no session, no key, no uid — tested, T7).
- **Boot storms get the parking discipline**: singleflight per cold target, bounded
  parking with counted shed, one per-flight budget, `budget_exhausted` as a counted
  outcome — a stampede produces backpressure, never a herd of cold boots.
- **Summon-to-ready budget**: derived from measured tier latencies on this host;
  continuously measured; a miss is a health-plane signal (`SUMMONING.md` §11).

## 4b. Autoscaling

Two classes, never blurred: **work-driven summoning is orchestration** (the Guide's
judgment over decomposition — no autoscaler decides how many Engineers a task
deserves); **load-driven replication is autoscaling** — daemon-class agents (Arbiter
replicas vs review-frontier lag) and capacity (pool depth, egress threads) scale
from measured demand: frontier lag, claim-queue depths, arrival rates, admission
sheds, `budget_exhausted` counts.

- **The autoscaler is a deterministic harness service** (system participant):
  derived targets (Little's-law family, hysteresis + decay), acting **only through
  the front door** — its summon requests pass Guardian admission like anyone's,
  which is the anti-runaway property for free. Scale-down drains: complete or park,
  claims redistribute via lease redelivery, teardown fast-forwards. No replica dies
  mid-claim.
- **Pull path = the warm tiers (§4); no registry on the path**: replicas of a role
  share the session's pinned bundle, so scale-up is pool-checkout (or resume, or
  cold boot) plus **assignment binding only** — keys, volume, identity, warden
  policy — milliseconds, with content already local or cache-filling by hash.
- **No rebalancing protocol exists or is needed**: a new replica is another
  consumer of at-most-once claims — work sharing is additive by construction.
- Fleet node acquisition (cloud/k8s environment adapters) is a named boundary
  adapter, outside core.

Per-role scaling classes (custom roles declare theirs in `AgentRole`):

| Role | Class | Primary signal |
|---|---|---|
| Guide | load-driven | intake/consult queue depth, consult latency (per-session at fleet) |
| Archivalist | load-driven | consult queue, retrieval latency, retirement-ingest backlog |
| Guardian | load-driven | **escalation hold-queue latency** — held syscalls block work; low-trust mode multiplies escalations, so SafetyPolicy `trust_mode` is a direct input to Guardian replica targets |
| Inspector | load-driven | review-queue depth (approval artifacts are merge-critical) |
| Arbiter | load-driven | review-frontier lag (§ MERGE.md) |
| Architect | **serialized-judgment** | singleton per session for everything direction-bearing — design direction has no ground truth until decided, so replicated rank-1 authority = forked direction. Parking absorbs consult bursts. Tripwire escape hatch: sustained consult latency ⇒ **record-replicas** (answer only what recorded artifacts settle; forward novel questions to the primary) |
| Engineer, Designer | work-driven | ready-claim backlog is a signal **to the Guide** (orchestration), never to the autoscaler |
| Scribe | structural | 1:1 with instances — coverage can never lag the fleet |
| Warden, sensor | structural | per-pod by construction |
- Tests: T18 — autoscaler storm: demand spike ⇒ targets ramp with hysteresis,
  admission ceilings hold, five-outcome accounting complete, zero mid-claim kills
  on scale-down; T19 — scale-up latency: replica-ready p50 within the assignment
  budget, zero registry reads on the path.

## 5. Snapshot-resume uniqueness (correctness, non-negotiable)

Snapshot clones inherit guest RNG state and clock — the SnapStart-uniqueness hazard.
At fleet scale this is a key-collision factory; it is closed structurally:

- The harness bumps a **VM generation identifier** on every resume; init observes it
  and completes reseed (kernel entropy reinjection, clock resync) **before** the
  agent process starts. No agent code runs on stale entropy, ever.
- Protocol safety is independent of guest entropy by construction: per-pod keys and
  counter nonces mint at assignment, post-resume (`PROTOCOL.md` §2).
- T6 verifies divergence: two clones of one snapshot must produce disjoint entropy
  streams and distinct guest-side randomness immediately after resume.

## 6. The warden and the sensor (per-pod protection)

The Guardian's distributed enforcement, ratified as three levels: mechanism at the
pod (warden), policy in config, judgment in the Guardian agent.

**The warden** — one per pod, **host-side**, a deterministic hecate-rt task on the
pod's device surface. The guest cannot reach it.

- **Inline, pre-effect**: every boundary crossing — virtio-fs op, packet into the
  host network stack, vsock frame — is decided *before it executes*. In-guest
  actions are ungated as calls (the compile-edit-test inner loop runs at native
  speed); every consequence meets a decision at the boundary it crosses.
- **Compiled local policy**, µs decisions, no Guardian round-trip on the fast path.
  Policy compiles from: SafetyPolicy, the role profile, the bundle's declared
  capabilities, and **the pod's active claim scope entries** — writes outside the
  claim's declared scope deny-or-escalate at the filesystem boundary. The claims are
  the authorization, physically.
- **Hold-and-escalate**: an op outside policy is held (guest syscall blocks, derived
  timeout) and escalates as a `guardian_check` claim to the Guardian agent —
  auto-approve under the SafetyPolicy ceiling, user prompt above it, deny with
  reasons. **The verdict compiles back into local policy with provenance** — the
  same op class never re-escalates, and every learned rule traces to the judgment
  that authored it.
- **Fail-closed**: a dead warden is a frozen pod, never an open one.
- Boundaries respected: escalations are claims (proof of work); compiled policy is
  config; the per-decision firehose is logs with categorized counters.

**The sensor** — guest-kernel telemetry (eBPF/LSM hooks compiled into our kernel
image; fixed, preloaded, image-hashed programs — the agent can load nothing).

- Streams early behavioral signals — process exec trees, syscall-class aggregates,
  capability use, file-access patterns — over its own vsock channel to the warden.
- **Tighten-only authority**: sensor signals can narrow the pod's world (flagged
  pods have subsequent crossings preemptively held-and-escalated); nothing the
  sensor says can widen policy. A lied-to sensor grants nothing.
- **Silence is a signal**: sensor tamper indicators or channel silence flip the
  warden to escalate-everything. Killing the sensor locks every door.
- Honest limit, on the record: a guest-kernel exploit defeats the sensor; the warden
  and the VM boundary still hold — that is what the layers are for.

The full stack: **sensor** (early, rich, semi-trusted) → **warden** (authoritative,
pre-effect, tamper-proof) → **Scribe** (semantic narration) → **Guardian** (judgment).

## 7. Lifecycle edges

- **Teardown**: never before work is committed — pod lifecycle is independent of
  disk commit; rejection/correction are not terminal for a pod's volumes. Teardown
  is a fast-forward multi-step operation (idempotent, self-checking steps).
- **Suspend/resume** (idle heavyweights): durable-state-only capture — the guest's
  memory is **discarded, never persisted**; what survives is ledger state, VFS
  manifests, and the bundle. Resume rebuilds the pod from durable state through the
  normal tiers and re-resolves secrets. There is no memory-image suspend.
- **Handoff**: successor pod summons through the same tiers; predecessor keys and
  fencing die at rotation; init executes the drain order.
- **Crash**: init death or VM fault surfaces as a typed lifecycle event on the
  control channel's host side; claims and parked turns survive on the ledger by
  construction; the health plane and Scribe drive replacement.

## 8. Test matrix (failure each catches)

| # | Test | Catches |
|---|---|---|
| T1 | Boot conformance per platform: identical guest image boots and passes the V6 serving corpus on KVM/HVF/WHP | per-backend drift; the platform-cell risk |
| T2 | Hostile init channel fuzz: arbitrary/malformed/replayed control frames from a compromised guest ⇒ typed rejection, no authority gained, host stable | init as an attack surface |
| T3 | Root immutability: guest writes to the root projection ⇒ typed EROFS-class error; tmpfs writes bounded by VM memory | write-authority leaks; unbounded guest memory via tmpfs |
| T4 | Serving-cost scaling: fs-op cost flat as idle pod count grows 10× (active-op scaling, not pod scaling) | O(pods) serving regression |
| T5 | Shared-page density: N resumed clones' resident memory ≈ one snapshot + Σ dirty pages (measured bound, ratcheted) | density mechanism silently broken |
| T6 | Resume uniqueness: two clones of one snapshot diverge in guest entropy immediately; agent process blocked until reseed completes | the SnapStart key-collision class |
| T7 | Generic-pool proof: pooled/snapshotted state contains no identity or work material (scan for keys/uids/session refs/work-volume bytes); the snapshot API refuses an assigned pod (structural) | frozen-identity bug family; in-progress work leaking to disk |
| T8 | Boot-storm sim: summon stampede ⇒ singleflight per target, bounded parking, counted sheds, zero cold-boot herd | thundering herd |
| T9 | Budget signal: induced tier degradation ⇒ summon-to-ready misses emit health-plane signals with tier attribution | silent slowdowns |
| T10 | Telemetry fan-in: pod-count growth leaves control-plane message rate bounded by node count; gossip piggyback stays under the datagram budget | telemetry self-DDoS |
| T11 | Teardown fast-forward: kill/redeliver at every step boundary ⇒ teardown completes exactly once, volumes outlive uncommitted work | double-teardown; premature volume loss |
| T12 | Assignment atomicity: crash between pool-checkout and assignment ⇒ VM returns to pool or dies clean; never a half-identified pod | identity limbo |
| T13 | Warden fail-closed: kill the warden ⇒ pod frozen, zero ops pass; restart resumes from compiled policy | a dead gate swinging open |
| T14 | Claim-scope enforcement: guest writes outside active scope entries ⇒ deny/escalate at the fs boundary; in-scope writes unimpeded | authorization as doctrine instead of physics |
| T15 | Verdict compilation: an escalated-and-approved op class does not re-escalate; every compiled rule carries its authoring verdict's provenance | re-escalation storms; unauditable learned policy |
| T16 | Tighten-only fuzz: arbitrary/hostile sensor input can hold and escalate but can never widen policy or approve anything | sensor as a privilege path |
| T17 | Sensor silence: channel death or tamper indicator ⇒ warden escalates everything; sensor dead at boot ⇒ summon validation fails | tripwire silently removed |

## 9. Acceptance criteria

1. One guest image family, dual-arch, boots on all three backends; T1 gates every
   platform before agent work runs there (inherits VFS V6).
2. Init's contract is exactly §3's five duties — an init that can do more fails
   review; control-channel fuzz (T2) is a permanent CI gate.
3. No block-image pipeline exists in the tree; guest images are manifests; image
   identity is a content hash end to end.
4. DAX/shared-mapping for RO layers operative on **all three backends, day one** —
   where the WHP lineage lacks it, building it is in-scope fork work, not a
   milestone; T5's density bound holds on every platform before agent work runs
   there.
5. Reseed-on-resume is structurally prior to agent start (T6); no configuration can
   disable it.
6. Pool sizes, cadences, tier thresholds, and the summon-to-ready budget are derived
   from measured anchors with derivations at definition sites; the same formulas
   produce laptop and fleet behavior (no mode flags exist).
7. Storm backpressure: T8's five-outcome accounting
   (`served/budget_exhausted/canceled/timeout/error`) with zero uncounted outcomes.
8. All identity binds at assignment; T7 scan is CI-gated.
9. Ratcheted floors: boot/resume/assignment latencies per tier per platform from
   first CI baseline; >10% regression fails.
10. **No mechanism in the tree persists an assigned pod's guest memory to host
    storage** — snapshot API pool-tier-only (T7 structural), suspend is
    durable-state-only, and crash artifacts capture typed diagnostics, never memory
    images of work.
11. Every boundary-crossing path traverses the warden — no fs, network, or vsock
    path exists that bypasses it (architecture test); warden decision latency
    carries ratcheted µs floors; fail-closed verified by T13 permanently.
12. Compiled warden policy is versioned config with per-rule provenance; it is part
    of the SafetyPolicy blast radius (a SafetyPolicy change recompiles predictably).
13. Sensor programs are fixed, preloaded, and image-hashed; tighten-only is
    structural (T16); no dynamic program loading exists.
