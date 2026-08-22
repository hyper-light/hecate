# SPEC: MONITORING — the observability plane (Scribe, history channel, telemetry, score, interior warden/sensor, VMM truth)

Status: presented for acceptance 2026-08-20. The design was ACCEPTED 2026-08-19
(GRILLING.md) conditional on folding three in-flight arc lanes (interior
enforcement observability, VMM-side visibility, conduct detection math) and five
corpus reconcilers; those landed and are folded here. Companion to `HANDOFF.md`
(the detection/handoff stack that consumes this plane), `PODS.md` (the
two-container pod anatomy + `hecate-init` + the warden/sensor host contract this
extends), `HEALTH.md` (the content-free signal law + AbsenceIs), `RANK.md` (the
score service supplies its deferred architecture), and `AGENTS_RUNTIME.md`.

## 1. The plane

A pod is **one libkrun microVM per primary agent, running two OCI containers**:
the primary's agent loop in one, its **Scribe** companion agent's loop in the
other (`PODS.md` §1, Design A — containers-per-loop, superseding "one microVM,
one agent"). The Scribe is a **coordinator atop deterministic substrate**
(warden : Guardian ∷ substrate : Scribe) — never a decomposition into a
pipeline. It scales 1:1 with primaries at zero added VMs (it rides the primary's
VM). The plane is governed by three comms laws (§4); its cardinal rule is
**observe-not-feed** — no path from the Scribe back to the primary, and no
model-controlled path from the primary to the Scribe.

## 2. The Scribe (first-class agent)

Per-primary companion: **narrator, history recorder + server, handoff judge**.

- **Inference is event-driven** (alerts, consults, narration-worthy events, a
  derived cadence) — NEVER per-turn-of-the-primary. Resident-idle at ~0 CPU
  (thread census `N+1`, not `2N`), bursty inference.
- **Ingestion is mechanical**: a single thread, kernel-assertable via io_uring
  `SINGLE_ISSUER` + multishot poll on the history doorbell + batch drain.
- **A secondary outbound-only lane** (a `spawn_blocking` pool capped to the
  outbound-channel count) handles Archivalist flush + external reach-out over the
  Scribe's own registered vsock flow.
- The Scribe is **right-sized hecate-rt (1 shard)**; its rootfs is its own RO
  manifest-subtree lower + tmpfs upper; its outbound vsock fd is pre-connected by
  `hecate-init` (SCM_RIGHTS at spawn, no guest-visible name).

## 3. The history channel (intra-VM, one-way, tamper-bounded)

The only inter-loop channel that exists — a **supervisor-minted memfd
flight-recorder ring + eventfd doorbell** (`hecate-init` mints both *before*
spawning and passes the fds into each container's fd table).

- **Split-cursor, kernel-enforced direction**: ring = primary `O_RDWR` / Scribe
  `O_RDONLY`; cursor = Scribe `O_RDWR` / primary `O_RDONLY` (kernel `EACCES` on
  cross-writes). Seals `SHRINK|GROW|SEAL` on both; **not** `F_SEAL_FUTURE_WRITE`
  (would block a respawned writer). The primary pre-faults the ring (deterministic
  memcg charge — *the observed pays for its own black box*).
- **Protocol**: sub-buffered OVERWRITE (flight recorder — newest always present;
  a wedged-Scribe's losses land on the oldest unpersisted); per-sub-buffer
  seqnum/commit stamps; copy-out-then-revalidate torn-read discipline; 8-byte
  record header + monotone seqnum per stream-instance id (id regenerates on
  primary respawn); in-band gap records. The emitter is **zero-syscall,
  zero-blocking on the hot path**, self-paced doorbell.
- **Carries STRUCTURED ACTIVITY EVENTS ONLY** — turn boundaries, tool-dispatch
  digests, claim posts, stop reasons, usage — **never transcripts or raw tool
  output**. Sizing derives from anchors (event-rate ceilings × drain gap incl.
  the restart-backoff ceiling); sub-buffer count ≥ 2.
- **Survives both deaths**: the supervisor holds the fds; the respawned Scribe
  resumes from its cursor; on primary death the Scribe drains the ring tail.
- **Classification: enrichment class** — never a detector, score, or audit input
  (§4b). vsock is guest↔host ONLY (`CID_LOCAL` rejected); no primary↔Scribe
  control channel exists at all.

## 4. The three comms laws

- **(a) Observe-not-feed** — no Scribe→primary path of any kind; no
  model-controlled primary→Scribe path (no tool, no prompt surface reaches the
  ring).
- **(b) Authority/enrichment split** — the Scribe's *authority* inputs are
  **host-side streams over its own vsock flow** (warden verdicts, ledger deltas,
  sensor telemetry, gateway usage) + kernel-pushed liveness (pidfd,
  `cgroup.events`). Detection, scoring, billing, and audit read ONLY these. The
  ring is enrichment / narration / handoff-brief continuity.
- **(c) Context economy** — the primary spends context on work only; history
  events are emitted **by the runtime** (instrumentation at turn boundaries / tool
  dispatch / claim posts, *below the model*) — zero token cost, not
  prompt-injectable, capture continues mid-inference. Any "the agent feeds its
  Scribe after every turn" or "the Scribe reads the primary's transcript" language
  anywhere in the corpus is **wrong** and is removed (`AGENTS_RUNTIME.md`).

## 5. Telemetry pipeline

**Autonomous-local-first**: a per-node in-memory **hot ring** (Gorilla-class
compression, derived retention, lossy-tolerant, **never on a claim path**);
aggregate + adaptive rate-based sampling at source; **bounded-cardinality keys
only**; federate upward only where an upward tier exists (`N=1` = the same
pipeline, no fan-in). Per-loop resource envelopes read from the per-container
cgroup files. `HEALTH.md`'s **content-free law + AbsenceIs semantics** carry
through unchanged (a signal type carrying a raw key/body/channel fails the H8
type-walk at CI). **Execution spans ride this same plane** (`TRACING.md`): host-side
chokepoints emit spans async to the hot ring; guest-interior spans are
runtime-emitted to the history ring and drain via the existing channels — no
tracing-specific channel exists. The collector consumes this plane (`HANDOFF.md`, and the
COLLECTOR spec to follow).

## 6. The score service

A **deterministic harness task in the colocation unit** (one per session group),
**single-writer**. Per-`(agent, domain)` reputation as a **pure function of the
ordered stream** (ledger outcome deltas + Scribe signal snapshots),
**outcome-grounded** — never turn-shape, never self-reported, never the history
ring. Pushed into `LEDGER_CORE.md` local state as **logged inputs** (no
synchronous query; determinism + replay hold). One authoritative copy (learner
copy ≡ decision copy). It is **not a CONSENSUS standing writer** — it pushes
snapshots as inputs, touches nothing on the ledger. `RANK.md` §4 semantics
(prevalence / specificity / trust; demote-only; observe-mode-first) are
unchanged — this supplies only the architecture RANK deferred.

## 7. Warden & sensor — the two-container interior

The `PODS.md` §6 host contract, **extended for the two-workload interior**.

- **Warden** — host-side, per-pod, **pre-effect at every device-boundary
  crossing**, compiled policy (SafetyPolicy + IAM residual + capability atoms +
  claim scopes), hold-and-escalate to Guardian, fail-closed.
- **Sensor** — guest-kernel eBPF, fixed image-hashed programs, tighten-only,
  **silence-is-a-signal**.
- **Interior enforcement** = **warden-compiled kernel residuals installed and
  pinned by `hecate-init` pre-spawn** (the Kata-agent "policy compiled outside,
  installed at spawn, enforced inside" precedent; `IAM.md` §6 compile-and-
  distribute extends one hop into the guest). Enforcement is **pinned**
  (`bpf_link`/bpffs) so it survives the drainer's death — *pin enforcement,
  supervise the drainer*.
- **Interior observation** = the sensor with **per-container attribution** via
  `bpf_get_current_cgroup_id` (a base helper, no tracing config), and a
  **denial-event export** (seccomp denials, cgroup events, tripwire firings —
  formerly silent). A **dedicated in-guest sensor-exporter process** (supervised
  by `hecate-init`, **not init itself** — PID-1-as-drainer has no precedent)
  drains the kernel rings into the sensor vsock channel; on drainer death,
  ringbuf records persist until the ring fills, then reserve fails with counted
  drops, never blocking the workload.
- **Counting a denial**: `RET_ERRNO` is **silent by design** and the kernel keeps
  no per-cgroup seccomp denial counter, so a denial is counted by one of: a
  `SECCOMP_RET_USER_NOTIF` **deny-only** listener (no `FLAG_CONTINUE`, no target
  deref ⇒ no TOCTOU; supervisor death ⇒ `ENOSYS` fail-closed; use only where
  denials are rare-by-design), `RET_ERRNO + FILTER_FLAG_LOG` + audit (lossy as a
  counter), or **cgroup-BPF** (below).
- **Stock vs fork.** On stock libkrunfw (`6.12.91`) today: seccomp + unotify, the
  full cgroup-v2 event surface (`memory.events` / `pids.events` / `cgroup.events`
  kernel-pushed via poll/inotify; `cpu.stat` polled; PSI trigger fds where
  present), and **cgroup-BPF UNIX connect/sendmsg interception** (`CONFIG_CGROUP_
  BPF=y` both arches; program returns 0 ⇒ caller `EPERM`; ringbuf + cgroup-id).
  The **guest-kernel fork-flip list** (DAX-style tracked; harmonizes the arch
  asymmetry — x86_64 has AUDIT+SECURITY but no PSI, aarch64 has PSI but no
  AUDIT/LSM): (1) `BPF_JIT=y` both; (2) `SECURITY`+`SECURITYFS=y` aarch64; (3) the
  `BPF_LSM` stack both (drags `BPF_EVENTS`→FTRACE, `lsm=…,bpf` boot); (4)
  `DEBUG_INFO_BTF=y` both (CO-RE/LSM attach); (5) `PSI=y` x86_64; (6)
  `AUDIT`+`AUDITSYSCALL=y` aarch64 (only if the seccomp-audit route is chosen);
  (7) optional `KPROBES`, `IKCONFIG(_PROC)` (in-guest `/proc/config.gz` kernel
  attestation). The flip unlocks BPF-LSM hooks (cross-container `ptrace_access_
  check` / `task_kill` / `bprm_check` / `file_open`, in-kernel filtered) + raw-
  syscall-rate telemetry.

## 8. VMM-observed truth (the host-observed lie-detector)

libkrun exports **zero** stats today (its public API has no counter/metrics
function); the fork adds **Firecracker-shaped first-party device counters**
(virtio-fs op counts by opcode; vsock per-port flows + RST counts — a guest
connect to a port with no host listener is a VMM-authored RST, *every attempt
countable*; net counters incl. `tx_spoofed_mac`; queue events) plus a
**KVM `GET_STATS_FD`** collector (a production, lock-free, unprivileged-drainable
telemetry surface — `halt_exits` / `halt_wait_ns` / exits / io/mmio / hypercalls
/ insn_emulation), symmetric on WHP (`WHvGetVirtualProcessorCounters`) and
self-counted on HVF (every exit delivered synchronously). **Host-truth surfaces**
the guest cannot fake: `/proc/<pid>/schedstat`, the VMM-cgroup `cpu.stat
usage_usec` (unfakeable guest burn), `smaps_rollup`/`RssAnon` (true faulted
footprint), the steal-time MSR (host-manufactured truth the guest reads).

**Provenance discipline** (the virtio-balloon micro-pattern): a
**host-authoritative envelope** (freshness/liveness) around **guest-authoritative
content**; every metric is provenance-classed `host-observed` vs `guest-reported`.
**Cross-view validation** (guest-reported vs host-observed, *divergence is a
signal*) is a first-class design element. The **lie-detector table** (7 rows):
idle/spin (host-authoritative — claimed-idle + no halt exits + full vCPU runtime
= spinning); memory (split — host owns footprint+freshness, guest owns
semantics); hidden-process (cross-view, trusted-view-authoritative); stream
liveness (device counters self-refute under-reporting); actor attribution
(guest-authoritative **with host veto** via boundary signature — capability-set
physics); starvation (host-manufactured, cleanest); boundary probing
(host-authoritative — the guest cannot suppress the host's count of its own
refused attempts).

## 9. Trust / threat model

**Bar A** (a faulty/degrading primary) vs **Bar B** (a guest-kernel-compromised
primary): every intra-guest mechanism holds at Bar A, none at Bar B; **Bar B is
caught host-side** (warden, host wiring, host-computed score, VMM counters). The
history ring at Bar B is contained by classification (enrichment-only — never an
authority input). Authority = host-side tamper-proof streams; guest-reported data
is provenance-classed and cross-validated (§8).

## 10. Laptop ≡ fleet

`N=1` is the same pipeline — the hot ring federates to itself (no fan-in), the
score service and detection substrate run in the one colocation unit, the two
containers run in the one microVM. Zero modes, everywhere.

## 11. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| MO1 | **Observe-not-feed** (architecture test): no Scribe→primary path and no model-controlled primary→Scribe path exists; the ring is unreachable from any tool/prompt surface | a feedback path; prompt-injection of the black box |
| MO2 | **Authority/enrichment split**: detection/score/billing/audit read only host-side streams; the history ring is never an authority input (typed classification, CI-checked) | a tampered enrichment stream driving a verdict |
| MO3 | **Context economy**: history events are runtime-emitted below the model — zero token cost, capture continues mid-inference (instrumented) | per-turn Scribe feed; transcript reads |
| MO4 | **Channel survives both deaths**: primary respawn resumes writing from a fresh stream-id; Scribe respawn resumes from its cursor; primary death drains the ring tail before teardown | lost black box across a restart; teardown before flush |
| MO5 | **Score is a pure function of the ordered stream** (outcome-grounded, single-writer, logged-input, replay-identical); it holds no CONSENSUS roster entry | self-reported or turn-shape reputation; a synchronous score query |
| MO6 | **Interior attribution + denial export**: every seccomp/BPF/cgroup denial is attributed to its container (cgroup-id) and counted/exported; enforcement is pinned and survives the drainer's death | a silent interior denial; enforcement lost with the drainer |
| MO7 | **Host-observed truth + cross-view**: idle/spin, footprint, starvation, and boundary-probing are decidable host-side; guest-reported vs host-observed divergence surfaces as a signal | a Bar-B guest faking its own telemetry |
| MO8 | **HEALTH content-free**: every monitoring signal is metadata-decidable; a raw key/body/channel in a signal type fails the H8 type-walk | telemetry leaking work content |
| MO9 | **Every constant derived** (ring/sub-buffer sizes, sampling rates, cgroup budgets, false-alarm budgets) from a physical anchor; the fork-flip list is explicit and tracked | magic numbers; an undeclared kernel-config assumption |
| MO10 | `N=1` produces the same pipeline as the fleet (no mode) | mode creep in the observability plane |

## 12. Test matrix (SIM + interior)

| Test | Asserts |
|---|---|
| Death fuzz | MO4 (primary/Scribe death at every point; tail-drain; cursor resume) |
| Comms-law probe | MO1/MO2 (no feedback path; ring not an authority input) |
| Denial-attribution sweep | MO6 (every denial class × container ⇒ counted + attributed; drainer death ⇒ counted drops, workload unblocked) |
| Cross-view lie fuzz | MO7 (injected guest-reported lies vs host-observed truth ⇒ divergence flagged) |
| Score replay | MO5 (byte-identical reputation from the ordered stream) |
| Content-free CI | MO8 (H8 type-walk on every signal type) |
| Laptop parity | MO10 (`N=1` == fleet pipeline) |

## 13. References

Firecracker (per-device metric families; the minimal-VMM precedent); KVM
`GET_STATS_FD` (api.rst 4.133); virtio-balloon host-stamped freshness (the
provenance micro-pattern); Falco / Tetragon / Kata-agent (pin-enforcement /
supervise-drainer; policy-compiled-outside); Ye 2002/2003 (EWMA on audit-event
intensity); GhostBuster / Lycosid / Antfarm / LibVMI (cross-view validation).
Companions: `HANDOFF.md`, `PODS.md`, `HEALTH.md`, `RANK.md`, `AGENTS_RUNTIME.md`.
