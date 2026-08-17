# SPEC: hecate-rt — the sharded deterministic async runtime

Status: presented for acceptance (grilling Branch 1). Direction ratified: async
everywhere on our own runtime; deterministic by construction; zero refcounting.
References: actix-web's shard model (pinned current-thread workers, `!Send` tasks, no
work stealing), TigerBeetle/FDB determinism discipline, hyperscale's
admission-before-task-creation, S2/Polar Signals leak reports as the anti-checklist.

## 1. Shape

- **N shards**, N derived from available cores (config-clampable). One pinned OS
  thread per shard, each running a single-threaded executor: FIFO ready queue,
  hierarchical timer wheel, per-shard driver handle.
- **Tasks are `!Send`-capable and never migrate.** Spawn targets a shard; placement is
  explicit (caller names the shard or uses the placement policy); there is no work
  stealing and no load-balancing migration. State lives in plain owned types.
- **Cross-shard communication is move-only** over bounded SPSC/MPSC channels. No type
  containing `Arc`/`Rc` crosses (or exists — §4).
- **Every stateful component is one task** owning its state, fed by its mailbox:
  ledger core, claims-graph monitor, merge serializer, protocol endpoint, WAL stream
  writer, VMM controller. Effects leave as messages or as returned effect values.

## 2. The driver seam

```rust
pub trait Driver {
    fn now(&self) -> Tick;                                  // monotonic; virtual in SIM
    fn rng(&mut self) -> u64;                               // seeded in SIM, OS entropy in REAL
    fn submit(&mut self, op: IoOp, waker: TaskRef) -> IoId; // completion-shaped API
    fn timer(&mut self, at: Tick, waker: TaskRef) -> TimerId;
}
```

- The API is **completion-shaped** on all platforms (an op is submitted and completes),
  so io_uring is the native fit and readiness backends emulate completion.
- **REAL drivers, day one — no deferred work, no silent fallback:**
  - Linux: **io_uring** primary, with linked SQE support (write→fsync chains).
    Minimum kernel version declared in one place and probed at boot; below it the
    binary fails loudly naming the requirement. No epoll fallback.
  - macOS: kqueue (readiness) under the completion API. Disk ops via the blocking
    pool (kqueue does not signal regular-file readiness usefully).
  - Windows: IoRing where present, IOCP otherwise; minimum Windows version declared
    alongside the WHP requirement.
- **SIM driver**: virtual clock (time advances only by simulator decision), seeded
  PRNG, simulated transports/disk with a fault matrix (drop, delay, partition,
  reorder, duplicate, corrupt, torn write, ENOSPC, EIO, power-cut at arbitrary byte),
  and seeded cross-shard delivery order. Component code is identical under REAL and
  SIM; the driver is the only substitution point.

## 3. Determinism contract

- Per-shard scheduling is FIFO and single-threaded; in SIM, cross-shard delivery and
  timer firing order derive from the seed. Two SIM runs with identical (seed, input
  trace) are **bit-identical** in all outputs (WAL bytes, delta order, frame order).
- **Banned in all core crates, enforced by workspace lint (CI-fatal):**
  `std::time::{Instant, SystemTime}`, `std::thread::spawn`, `rand`/`getrandom`
  direct use, `tokio`/`async-std`/foreign runtimes, unbounded channel types, and
  **std `HashMap`/`HashSet` in component state** (DoS-randomized iteration order is a
  determinism leak — S2's receipt); deterministic-iteration maps only.
- The blocking pool (provider HTTP, file fallbacks) exists only at edges; results
  re-enter shards as messages. In SIM, blocking-pool dependencies are simulated
  components.

## 4. Memory doctrine — zero refcounting

- **`Arc` and `Rc` are denied workspace-wide** (lint). The only exceptions are named
  FFI edge modules (libkrun bindings, platform APIs) in a PR-reviewed allowlist.
- Intra-component references are **generational handles** (`u32` index + `u32`
  generation) into owner-managed arenas. A stale handle is a **typed error**, never a
  silent hit; generation checks are mandatory on every dereference.
- Shared-immutable fan-out (one payload referenced by N in-flight consumers) uses
  **explicit acquire/release counts stored as data in the owning arena** — visible in
  replay, single-threaded, auditable. Never a smart pointer.
- Buffers transfer by move; within a shard, loans (`&[u8]`) are fine; across shards,
  ownership moves or an owner-mediated handle is sent.

## 5. Provider egress

Blocking rustls HTTP/1.1 client on a dedicated thread pool (LLM streams: long-lived,
low-count; SSE supported). No async-ecosystem HTTP dependency anywhere in the tree.

## 6. Test cases (failure each catches)

| # | Test | Catches |
|---|---|---|
| T1 | Bit-reproducibility: same (seed, trace) twice → byte-identical WAL, delta sequence, frame order | any nondeterminism leak: stray clock, map iteration, racy wake |
| T2 | Planted-bug exploration: a test component with a deliberate ordering bug must be found within N seeds | a sim harness that runs but doesn't explore (hyperscale's never-executed replay guard, as a test) |
| T3 | Lint wall red: `Arc`/`Rc`/std-time/`thread::spawn`/rand/tokio/std-HashMap/unbounded channel anywhere outside allowlist → CI failure | doctrine decay |
| T4 | Reactor conformance (echo, timers, timeouts, partial IO, linked write→fsync) green on Linux/macOS/Windows CI | per-platform driver drift — the REAL≠SIM divergence class |
| T5 | No-migration: task state address stable across polls (debug assert) | work stealing reintroduced |
| T6 | Stale-handle: arena slot reuse + old handle → typed generation error, never data | use-after-free-by-index |
| T7 | io_uring linked-SQE vs emulated path produce identical results on shared test corpus | Linux fast path semantically diverging |
| T8 | Boot probe below minimum kernel/OS → loud failure naming requirement | silent degraded mode |

## 7. Acceptance criteria

1. T1 enforced in CI on every merge, permanently.
2. Zero `Arc`/`Rc` outside the reviewed FFI allowlist; zero unbounded queues; zero
   banned APIs — all lint-enforced, CI-fatal.
3. Identical component code under REAL and SIM; driver is the only substitution.
4. Tasks never migrate; cross-shard traffic is move-only over bounded channels.
5. io_uring is the operative Linux driver from the first merge that touches disk or
   network on Linux; no epoll fallback exists in the tree.
6. Performance floors are **ratcheted from first measured baseline** on pinned CI
   hardware (constants-from-data): baseline run establishes shard wake→poll
   throughput and bounded-channel p99 latency; any regression >10% fails CI.
   Provisional expectations pending baseline: ≥1M wake→poll cycles/s/shard;
   channel send→recv p99 ≤ 1µs.
7. Every derived constant (shard count, pool sizes, queue bounds) carries its
   derivation at the definition site; bare tuning literals fail review.
