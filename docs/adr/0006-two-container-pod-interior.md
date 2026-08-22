# Two-container pod interior — one OCI container per agent loop

Accepted 2026-08-22 (the MONITORING/HANDOFF design, accepted 2026-08-19; specs
accepted 2026-08-22). A pod is one microVM running **two OCI containers**: the
primary agent's loop in one, its Scribe companion's loop in the other, spawned and
supervised by `hecate-init` (PID 1, embedded spawner — rustjail pattern, reduced:
two fixed containers, no userns maps, no hooks, cgroupfs driver). This supersedes
the previously accepted shared-runtime placement (Design B: the Scribe as a task
inside the primary's runtime) and revises the corpus-wide reading that the VM
boundary is the only inter-agent isolation — **two agents share a guest at Bar A**,
compartmentalized by kernel mechanisms (per-container mount+PID namespaces, cgroup
bounds, seccomp profiles, pinned residuals), with exactly one inter-loop channel
(the one-way history ring).

## Why

- **Observe-not-feed needs a boundary, not a convention**: with two processes in
  two containers, the ring's direction is kernel-enforced fd permissions and the
  Scribe is unreachable from any primary surface — Design B could only promise
  this in code review.
- **Attribution**: per-container cgroup identity makes interior denials, resource
  use, and behavioral telemetry attributable to the loop that caused them —
  Design B blended both loops into one accounting.
- **Blast containment at Bar A**: a faulty primary cannot corrupt the Scribe's
  memory, starve its scheduler share (cgroup floors), or forge its flow identity
  (per-workload keys).

## Consequences

Reshapes the init contract (mint-then-spawn-two, scribe-first, tail-drain hold,
flush-gated teardown — PODS §3), the channel inventory (four vsock flows +
the memfd ring), the census (N+1 threads), admission (Σ memory.max + init ≤ guest
RAM), and the interior enforcement/observation model (pinned residuals +
per-container denial export). Guest-global OOM is uncontained unless the admission
bound holds. The assembly has no direct industry precedent (Hecate first); the
stock guest kernel lacks an LSM until the fork-flip list lands.

## The tradeoff, honestly

Design B (shared runtime) is lower-overhead — no second container, no channel
mint, no admission split — and remains the tombstoned alternative. It was
rejected because its weaker attribution and convention-grade isolation put the
comms laws (the plane's cardinal rules) on discipline instead of physics.
Reversal cost is high: the init contract, channel custody, lifecycle ordering,
census, admission arithmetic, and interior policy all encode the two-container
shape — which is exactly why this is an ADR.
