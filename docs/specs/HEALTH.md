# SPEC: the health plane — one signal stream, judgment at the edges

Status: presented for acceptance. Direction ratified in `PLATFORM.md` §5: one
consolidated per-agent signal plane replacing Sylk's four disconnected subsystems;
health informs, agents act. References: `PODS.md` (warden/sensor telemetry, node
rollup), `AGENTS_RUNTIME.md` (turn signals), `RANK.md` (score service consumption).

## 1. Signals

Per agent instance, computed from sources that already exist — the plane adds no
probes, it consolidates streams:

| Signal | Source |
|---|---|
| Token progress | agent runtime (streaming LLM loop) |
| Turn quality (stop reason, tool-call coherence, output ratio) | agent runtime |
| Context fit | runtime accounting against the **pinned ModelConfig window** — never a constant |
| Claim coherence (ledger activity consistent with assignment) | frontier/ledger observation |
| Liveness | protocol keepalives + init lifecycle events |
| Pod pressure (memory, fs-op rates, held/escalated ops) | warden + sensor telemetry |

All windows, EWMA weights, and thresholds are **derived** from observed activity
volume and the pinned configuration; every derivation lives at its definition site.

## 2. The node health service

A deterministic harness service per node: consumes the streams above, maintains
per-agent composite state as its own re-derivable state, and **rolls up at the
node** — cross-node health rides the gossip plane piggybacked under the datagram
budget (`PODS.md` §3). Fan-in is bounded by node count, never pod count.

Consumers, each with its own judgment:
- **Scribes** — handoff judgment and narration color for their primary.
- **The score service** (`RANK.md` §4) — outcome-weighted inputs.
- **The Guardian** — conduct analysis and resource response.
- **The Guide** — orchestration visibility (a summon that misses budget, an agent
  that stalls).

The health service itself has **no authority**: it cannot gate, author claims, or
trigger anything. Health is continuous scoring feeding judgment — never a
string-matched phase roll-up, never an enforcement layer.

## 3. Scribe triggers

- **Context handoff**: the derived utilization threshold crossing is sufficient
  cause — Scribe-initiated, unilateral, no evidence bundle required (the number is
  the evidence).
- **Performance handoff**: the Scribe assembles an **evidence bundle** — the signal
  classes that degraded (with windows and baselines), plus its narrative of intent
  drift — and requests via the Guardian, which may soft-gate by requesting more
  evidence exactly once. The bundle's required classes are specified so the
  Guardian can adjudicate from the request alone in the common case.
- New signal classes enter **observe-mode first** (computed, logged, feeding no
  trigger) until their distributions are seen — the standing rollout discipline.

## 4. Tests and acceptance

| # | Test | Catches |
|---|---|---|
| H1 | Signal determinism: identical input streams ⇒ identical composites, in SIM and across platforms | nondeterministic health verdicts |
| H2 | Threshold derivation: swapping the pinned ModelConfig moves context thresholds; no constant exists (the Sylk 100K hardcode is the named regression) | window constants returning |
| H3 | Evidence completeness: a performance-handoff request carries every required signal class; the Guardian's single evidence request is exercised, and a second is structurally impossible | soft-gate becoming a stall loop |
| H4 | No-authority: the health service can gate nothing and author nothing (architecture test) | health becoming enforcement |
| H5 | One plane: no second health/liveness subsystem exists in the tree (architecture test — Sylk ran four) | fragmentation returning |
| H6 | Rollup bounds: control-plane health traffic bounded by node count under 10× pod growth (with `PODS.md` T10) | telemetry self-DDoS |

Acceptance: H1/H4/H5 permanent; all consumers read the one stream; every threshold
derived with its derivation in place; observe-mode gate for any new signal class or
trigger formula.
