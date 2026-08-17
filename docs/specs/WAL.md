# SPEC: the ledger WAL — logical logs over derived-ω physical streams

Status: presented for acceptance (grilling Branch 2). Ratified direction: per-session
**logical logs** (one sequencer each — replay, watermark, and monotone-cut invariants
untouched) multiplexed over **ω physical WAL streams** (durability only, never an
ordering authority), CRDB/TiKV-lineage; **one durability policy: always-full**,
naturally batched, pipelined. References: TiKV raft-engine (writer group, purge),
Pebble/etcd WAL discipline, TigerBeetle batching, fsync research on file
(GRILLING.md).

## 1. Model

- **Logical log** = per-session ordered record stream, `log_seq` strictly monotonic,
  written only by that session's sequencer task (the ledger core; under replication,
  the Raft leader — locally a 1-replica group whose append self-acks through the
  same call path).
- **Physical stream** = an append-only segment chain on disk. Records from many
  logical logs interleave, each tagged `(log_id, log_seq)`. A stream has exactly one
  writer task (single-owner, per §Runtime); "multi-writer" is the MPSC front-end.
- Artifact **content never enters the WAL** — content-addressed blob store; the log
  carries references. Log records stay small; flush batches stay dense.

## 2. Derived-ω topology (constants from data)

At boot, measure the device: k flushes on a preallocated probe file → `flush_p50`,
plus per-stream submission overhead `submit_cost` (measured, not assumed).
Choose ω ∈ {1..N_shards} maximizing the closed-form throughput model:

```
throughput(ω) = ω × batch_size(ω) / (flush_p50 + submit_cost)
where batch_size(ω) = expected arrivals during one flush at rate λ/ω (natural batching)
```

— cheap flush (PLP NVMe, µs-scale) drives ω → N_shards (parallelism dominates);
expensive flush (consumer NVMe ms-scale, macOS F_FULLFSYNC 17–24ms) drives ω → 1
(batch amortization dominates). λ starts from the arrival-rate prior recorded on
last run (first boot: model evaluated at the measured probe rate) and ω is
re-derived per boot, never hand-set. The derivation and its inputs are logged.

Session→stream assignment: stable hash of session id over ω; a session's records
never split across streams within an epoch (recovery locality; migration §6).

## 3. Record and segment format

- **Segments**: fixed-size, preallocated and zero-filled at creation (file length
  never changes → `fdatasync` suffices on Linux; no metadata journal churn).
  Segment size derived from measured write bandwidth × target rotation interval.
- **Records**: 8-byte aligned; header
  `{len: u32, crc: u32, log_id: u64, log_seq: u64, stream_seq: u64, kind: u8, ver: u8}`
  then payload, zero-padded to alignment. `crc` is CRC32C **chained** — computed over
  (prev record's crc ‖ header-sans-crc ‖ payload) — so a valid-looking stale record
  in a recycled segment can never be accepted (ghost-record defense).
- **Recovery** per stream: sequential scan, verify chain, **checksum-truncate** at
  first invalid record — with etcd's torn-vs-corrupt discrimination: examine the
  failed region in 512-byte-aligned sectors; all-zero sectors ⇒ torn write (truncate;
  only unacked records lost — safe), any non-zero garbage ⇒ latent corruption ⇒
  typed hard error naming stream/offset; refuse to start. **No doublewrite** —
  append-only logs never overwrite acked bytes, so page-store machinery is waste.

## 4. Commit path

- Producers send `Append{log_id, records, ack}` over a bounded MPSC to the stream's
  writer task. **Natural batching, no timers**: everything that queues while a flush
  is in flight rides the next write+flush (etcd model). `commit_many` pipelines a
  producer's burst as one message; entries are individually acked (a pipeline, not a
  transaction).
- Durability primitive per platform, one policy — **always-full**:
  Linux `fdatasync` on preallocated segments via **io_uring linked SQE
  (write→fdatasync)**; macOS `F_FULLFSYNC` (`File::sync_all`); Windows
  `FlushFileBuffers`. Ack is sent only after the durable return. Accepted cost on
  ledger: ack p50 ≈ one flush (µs on PLP, ~0.5–5ms consumer NVMe, 17–24ms macOS) —
  invisible against seconds-scale agent turns; nothing latency-sensitive awaits a
  flush.
- Backpressure: full producer queue ⇒ typed retryable error with derived retry hint,
  counted — never blocking the producer's shard, never unbounded growth.

## 5. Replication hook

The sequencer appends through the consensus-group API in every mode. Locally the
group has one replica and the leader's durable-append self-acks; distributed, the
same call path runs 3-replica Raft with pipelined appends (leader = sequencer). The
physical stream stores the group's log entries below consensus. No local-only commit
shortcut exists.

## 6. GC and migration

- Reclaim is watermark-driven per logical log (snapshot floor + retention). Segments
  free when all resident records are below their logs' floors; long-lived stragglers
  are **rewritten forward** (raft-engine purge model) rather than pinning old
  segments.
- Session migration (colocation-unit move): snapshot at a sequence + tail export of
  `(log_id ≥ floor)` records; the receiving node opens the logical log at the same
  `log_seq` — physical stream identity is never exposed above the WAL API.

## 7. Simulation

The stream writer runs on hecate-rt; in SIM the disk is a simulated device with the
fault matrix (torn write at arbitrary byte, reordered completions, EIO, ENOSPC,
power-cut). WAL invariant oracles run under the same seeds as everything else.

## 8. Test cases (failure each catches)

| # | Test | Catches |
|---|---|---|
| W1 | Power-cut fuzz: cut at every byte offset across a commit batch (SIM disk); recover; assert acked prefix intact, unacked cleanly truncated | torn-write mishandling; the acked-loss class |
| W2 | Torn-vs-corrupt: zeroed tail sectors ⇒ truncate + start; non-zero garbage ⇒ typed refusal naming offset | silently replaying corrupt state |
| W3 | Recycled-segment ghost: stale chain-valid-looking records rejected by chained CRC | ghost records resurrecting old state |
| W4 | Interleave replay: N logical logs on one stream; two recoveries byte-identical; per-log order preserved | cross-log ordering leak; nondeterministic recovery |
| W5 | ω-derivation: same measured inputs ⇒ same ω; model-vs-measured throughput within 20% on CI hardware | topology derivation drift; model fantasy |
| W6 | Ack-durability property: any commit acked before a SIM power-cut survives recovery, across full seed sweep | the only unforgivable WAL bug |
| W7 | Backpressure: saturated queue ⇒ typed retryable + counter increments; memory bounded under sustained overload | unbounded growth; silent drops |
| W8 | Migration: snapshot+tail export then re-open on a fresh node; log_seq continuity and content identity preserved | migration losing or reordering a log |

## 9. Acceptance criteria

1. **Zero acked-commit loss** under the SIM power-cut sweep (W1/W6) — CI-gated on
   every merge, permanently.
2. Recovery never scans beyond the segment index + last checkpoint; recovery
   throughput ≥ 0.5 × measured sequential-read bandwidth of the device.
3. Throughput floors phrased against measured device numbers (constants-from-data),
   ratcheted from first CI baseline: sustained durable commits/s ≥ 0.8 × the ω-model
   prediction for that hardware; macOS ack p50 ≤ 1.5 × measured F_FULLFSYNC latency
   under load.
4. One durability policy in the tree: no barrier tier, no checkpoint tier, no
   config knob that weakens the ack contract.
5. Every constant (segment size, probe count, queue bounds, ω) derives from measured
   anchors with the derivation at the definition site.
6. Determinism: same (seed, trace) ⇒ byte-identical stream files in SIM.
7. The consensus-group append path is the only commit path, at every replica count.
