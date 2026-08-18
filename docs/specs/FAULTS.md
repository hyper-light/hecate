# SPEC: the fault model — scope, dispositions, simulation

Status: ACCEPTED 2026-08-17 (decision 5 + amendment 5a of the ratified
Branch-20 direction; accepted with the split-brain and cross-region delta
sets). Governs: the consensus core, WAL, both storage planes, the protocol
layer — every subsystem names its obligations against this one fault
taxonomy. Companion: `CONSENSUS.md`.

## 1. The fault scope (what we defend, stated closed)

**In scope**: crash-recover (kill at any instruction, recover from durable
state); process pause/resume of any duration (the GC/scheduler stand-in —
defeated by fencing, never by timing assumptions); network partition in
every shape (clean splits, majorities-ring, **per-link per-direction
asymmetric omission** — the Cloudflare class — and region-scale partitions);
message loss, duplication, reordering; clock strobe/jump (only telemetry may
notice — no correctness path reads wall-clock); storage faults with
detection (torn writes, misdirected writes, detected corruption,
disk-swap-on-reboot, stalled-device gray failure); **region-scale events**
(WAN partition, correlated loss of a full failure-domain subtree, WAN
latency inflation); **internal-machinery misbehavior of liveness-only
components** (the node-liveness fabric emitting contradictory/stale/withheld
claims — in scope precisely because CONSENSUS §3b's fabric law promises
safety is untouched by it).

**Out of scope, explicitly**: Byzantine participants (the pod/warden
boundary and per-pod keys are the authenticity mechanism — a compromised pod
can lie only as itself and cannot forge consensus traffic); undetected
corruption past the checksum layer (BLAKE3-everywhere makes the undetected
residue the hash-collision probability, stated, not defended further).

## 2. Corruption dispositions (protocol-aware recovery, FAST'18 CTRL)

The one law: **never silent truncation** — truncating a corrupt log region
without protocol awareness can un-commit globally-committed entries.
Dispositions, typed per artifact:

- **Torn tail** (fails its own frame checksum at the recovery frontier):
  discard — it was never acked (the witness discipline makes this safe by
  construction).
- **Detected body corruption** (checksum fails behind the frontier): typed
  disposition by artifact class — consensus log entry ⇒
  **rebuild-from-quorum** (fetch the committed entry from peers; refuse to
  serve until repaired); N=1 or quorum-unavailable ⇒ **refuse loudly**
  (typed, names the entry, operator-surfaced — never guess); content chunk
  ⇒ re-fetch by hash (self-healing; OBJECT_TIER scrub/repair path); derived
  state ⇒ discard and re-derive (always legal; watermark-recovery
  invariant).
- Every disposition is a counted, categorized event; a disposition with no
  signal is a bug.

## 3. The nemesis matrix (the closed fault-injection vocabulary)

`kill` (any instruction) · `pause` (unbounded, resume) · `partition`
(clean, majorities-ring, partial) · `omit` (per-link, per-direction,
probabilistic and total) · `dup/reorder` · `clock` (strobe, jump, skew) ·
`torn-write` · `misdirected-write` · `corrupt` (targeted byte flips, data
and metadata) · `disk-swap` (node reboots with a peer's or stale disk) ·
`disk-stall` (device alive, unbounded latency) · `fabric-fault`
(contradictory/stale/withheld/forged-within-scope support claims) ·
`region-partition` (WAN cut, incl. asymmetric) · `region-loss` (correlated
kill of a full subtree) · `wan-inflate` (WAN latency ×10–100).

Every class has at least one CI scenario; composite scenarios
(pause + partition + clock jump; region-partition + fabric-fault) are
seed-generated, not hand-enumerated. New fault classes enter by amending
this section, never by an ad-hoc test.

## 4. The deterministic whole-cluster simulation (amendment 5a)

- **One simulation, cluster-scoped**: RUNTIME.md's SIM driver extended to
  host N simulated nodes across a simulated failure-domain tree — simulated
  network (the §3 vocabulary as injectable edges, WAN edges with derived
  latency distributions), simulated storage (torn/corrupt/stall
  injectable), logical time. The consensus core's IO-as-data shape
  (CONSENSUS §2) means the cluster runs unmodified inside it — the two
  decisions are one design.
- **Seeded and replayable**: every run is a seed; every failure is a
  seed + step count, replayable to the instruction. A failing seed becomes
  a permanent regression seed.
- **Biased search, BUGGIFY-style**: injection sites carry seed-driven bias
  hooks (prefer the rare branch, the full buffer, the expiring lease, the
  healing partition) — the FDB lesson that unbiased random rarely finds
  the interesting interleavings.
- **Budget as a ratchet, not a number**: simulation CPU-hours per release
  ratchet up from the first CI baseline; the FDB ~trillion-CPU-hour and
  TigerBeetle 24/7-VOPR postures are the reference points; our floor
  derives from fleet size and release cadence at the definition site.
- **The N=1 gate** (CONSENSUS §8): the crash-injection suite runs at N=1
  as a named, separate CI job — the configuration where the v3.5 class
  hides.

## 5. The failure×obligation matrix

The spec's core artifact: rows = §3 fault classes, columns = subsystem
obligations. Each cell is one of **Masked** (no observable effect),
**Degraded** (typed, bounded, surfaced), or **Refused** (loud stop, never
guess) — and each non-trivial cell names its test. The matrix ships in this
document and is **boot-validated for coverage**: every subsystem × fault
class has a stated cell — an uncovered cell fails CI, not review. Headline
rows:

- `pause` ⇒ Masked everywhere by fencing (CN8).
- `disk-stall` ⇒ Degraded via support-lapse election (CN3).
- `corrupt(log body)` ⇒ Degraded via rebuild-from-quorum; Refused at N=1.
- asymmetric `omit` ⇒ Masked for safety, Degraded-bounded for liveness
  (CS8).
- `fabric-fault` ⇒ Masked for safety unconditionally, Degraded for
  election latency only (CN11 — the executable form of the fabric law).
- `region-partition` ⇒ Masked for everything region-local; Degraded for
  the closed root-operation stall list, which may never intersect a
  session path (CN13).
- `region-loss` ⇒ Degraded per the priced loss class: unlanded work within
  the replication lag forfeits; sealed work intact; sessions re-summon
  (CN14).

## 6. Test matrix

| # | Test | Catches |
|---|---|---|
| F1 | Full nemesis × linearizability sweep (CN1's harness) at N=1/3/5 across a multi-region simulated tree, seeds ratcheted | safety under every in-scope fault |
| F2 | Every §2 disposition exercised by targeted corruption injection; zero silent truncations (asserted structurally) | the un-commit class |
| F3 | Replay determinism: any failing seed replays byte-identically | debuggability of everything above |
| F4 | Obligation-matrix coverage check: no subsystem × fault cell unstated | silent scope holes |
| F5 | Byzantine non-goal boundary: a forged-message attempt dies at the key layer, never reaches the core (negative test) | scope confusion |
| F6 | Disk-swap-on-reboot: node with stale/foreign disk is detected (epoch/identity mismatch) and refuses to vote | the FAST'18 disk-swap class |
| F7 | Region-heal fuzz: partition a region (not kill), let both sides run, heal ⇒ safety holds under the full §7 protocol: (a) inside the lease-shadow window the root refuses re-grant/re-summon-with-materialization while the cut side may still legally materialize (CN15's window, exercised from the fault side); (b) after dead-declaration the region epoch is terminal — on heal the region rejoins under a new epoch, no pre-partition epoch resumes authority or renews a lease; (c) zombie sessions' unlanded work ingests as fork branches only, never continuations — overlapping descendants of one lineage node surface as parallel workstreams carrying conflict values; (d) zombie externalization attempts during and after the partition are refused at the fenced egress chokepoints (CN16 from the fault side) | zombie-region resurrection; the lease shadow; un-fenced externalization |

## 7. Acceptance criteria

1. The fault scope is closed: new fault classes enter by amending §1/§3,
   never by an ad-hoc test.
2. Zero code paths truncate a log region without a typed §2 disposition
   (architecture test).
3. Simulation runs in CI from the first consensus commit; the seed corpus
   and CPU-hour floor only ratchet.
4. The obligation matrix is complete and boot-validated (F4 permanent).
5. Every incident-derived scenario (Cloudflare asymmetric partition, v3.5
   watermark race, TiKV #10017, disk-swap, region-heal) exists as a named
   regression seed.
6. The simulated failure-domain tree covers depth one (laptop) through
   multi-region in the same harness; no scenario is laptop-only or
   fleet-only by construction.
