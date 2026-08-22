# SPEC: TRACING — execution tracing across every subsystem

Status: presented for acceptance 2026-08-21. Worked in-session (GRILLING.md) against
the tracing research lanes: Dapper (Google TR 2010-1), Canopy (SOSP'17), the OTel
Collector/tail-sampling docs, W3C Trace Context. User direction that shaped this spec:
distributed tracing is required for **everything** — every store, queue, cache, router,
consensus group, pod, and service — and it is **foundational** (its own spec, consumed
by the collector), not a collector feature. Companions: `PROTOCOL.md` (the envelope
carries the context), `MONITORING.md` (spans ride the telemetry plane), `HEALTH.md`
(content-free law), `HANDOFF.md` (detection consumes traces), the COLLECTOR spec to
follow (assembly + storage), `SIBYL` branch (cross-region assembly, deferred).

## 1. Role — the execution story, and the three-id law

A distributed trace is the **execution story of one operation** across the whole
system: a summon crossing gateway → scheduler → consensus admission → pod boot → VFS
mount → warden compile → agent start, with the time spent and the outcome at each hop.
It answers "where did these 8 seconds go" and "which hop failed" — questions no other
plane answers.

It is the third of three correlation planes, and **the three ids never merge**:

| Id | Plane | Answers | Home |
|---|---|---|---|
| `request_id` | transport | which response pairs with which request; dedup | `PROTOCOL.md` §2 envelope |
| `trace_id` / `span_id` | execution | where one operation's time and failures went | this spec (operational plane) |
| `caused_by` | work | which claim caused which claim | the claims ledger (`LEDGER.md` §2/§4) |

**Disjoint by law.** The claims graph is complete, durable, never sampled — it is work
proof. Traces are sampled-for-keep, lossy-tolerant, expiring — they are operational
signal. One id cannot key both: a complete durable trace-graph keyed on `caused_by`
would be a second claims ledger, which `LEDGER` §9.8 bans outright ("no second
authority… no parallel store"), and sampling the shared graph would destroy the proof.
Different altitude too: `caused_by` links claims to claims; spans link infra-ops to
infra-ops *within* one claim's servicing (one claim's execution is dozens of store
reads, cache hits, one provider call).

**Cross-linked by opaque reference, never fused (TR1):** a span may carry a claim UID
as a bounded opaque tag; a claim's system-written lifecycle record carries
**`trace_refs`** — the trace ids of the operations that posted and serviced it
(landed with COLLECTOR acceptance, 2026-08-22; LEDGER §2). An investigator pivots slow-op → claim (an authorized ledger
read) or claim → trace (an authorized operational read). Reference, not identity.

## 2. The trace context on the wire

```rust
/// An ordinary #[derive(Wire)] struct — no codec extension needed (WIRE_FORMAT.md
/// covers derived structs; fixed-width fields, canonical encoding).
struct TraceCtx {
    trace_id: [u8; 16],   // unique per operation; minted at the trace root
    span_id:  [u8; 8],    // the sender's current span — the parent of whatever
                          // the receiver does for this message
    flags:    u8,         // bit 0 = keep (the root's sampling decision, §5);
                          // remaining bits must-be-zero (rejected otherwise)
}
```

- **Placement: inside the encrypted envelope** (`PROTOCOL.md` §1.1), beside
  `src_pod/dst_pod/request_id` — it is not key-finding data, so it never rides the
  cleartext prologue. Encrypted AND authenticated: tamper-evident, invisible on the
  wire, readable by the warden (which already decrypts the envelope to inspect it), so
  warden and sensor emit spans too. ~25 bytes per message; constant, negligible.
- **Total propagation (TR2):** every message carries a `TraceCtx` — the codec rejects
  absence. A message sent while servicing a traced operation carries
  `{that trace_id, the sender's current span_id}`. A message minted outside any traced
  operation (a liveness claim, a background flush) **roots a fresh trace** — there is
  no "untraced" value; the class-aware keep decision (§5) is what makes background
  classes cheap, never an exemption from carrying the context.
- The exemplar is the W3C `traceparent` shape (16-byte trace id, 8-byte parent id,
  flags); exemplar, not dependency — this is hecate-wire, not an HTTP header.

## 3. The span

One chokepoint's timed slice of a trace. **Content-free under `HEALTH` H8** — every
field is a number, a duration, a closed enum, or an opaque id; the type-walk applies
to span types exactly as to every signal type:

| Field | Type | Note |
|---|---|---|
| `trace_id`, `span_id`, `parent_span_id` | opaque ids | the tree structure |
| `chokepoint` | **closed registry enum** | `store.ingest`, `consensus.commit`, `warden.verdict`, `gateway.call`, … — never free text |
| `start`, `end` | monotonic timestamps | duration derives |
| `status` | ok \| typed error class | the closed error taxonomy, never a message string |
| tags | bounded-cardinality only | node id, shard id, size-bucket, principal UID, claim UID — opaque ids and enums; no key, no path, no body |

**Emission is async and below the hot path, always** (the async-by-default law):
host-side chokepoints emit to the node's telemetry hot ring (`MONITORING.md` §5);
guest-interior spans are runtime-emitted below the model to the pod's history ring and
drain via the existing channels — **no new channel exists for tracing**. The traced
operation never blocks on its own span; loss in the lossy ring is tolerated and
**counted** (TR8). Receipts that price this: Dapper measured ~200 ns to create/destroy
a span, 9–40 ns per annotation, 426 bytes per span, its daemon under 0.3% of one core
and trace traffic under 0.01% of network — emission-always is cheap; *keeping* is the
expensive part, which is what §5 bounds.

## 4. The chokepoint-span pattern

The chokepoint law already forces every cross-component access through a named,
boot-validated boundary — board through the board, store through the storage layer,
LLM through the gateway. **Those boundaries are the span points.** One pattern,
applied uniformly:

1. On entry: open a span as the child of the message's incoming `TraceCtx`.
2. Do the work.
3. On exit: close the span (status = the typed outcome), emit async.
4. Anything sent onward carries `{trace_id, this span's id}`.

**The span roster is the chokepoint roster (TR3).** Every subsystem's chokepoint
table — STORE ingest/read/scan/checkpoint, QUEUE post/lease/ack, CACHE get/put/
invalidate, FANOUT route/deliver, CONSENSUS propose/commit, MATERIALIZER epoch/apply,
PODS summon/assign/teardown, VFS/serving ops, MERGE gate ops, IAM decisions, REGISTRY
ops, warden verdicts, gateway calls — is its span roster; registration is validated at
boot exactly as chokepoint coverage already is (an unregistered emitter fails startup,
it does not degrade). On acceptance of this spec, each subsystem spec gains its
one-line "chokepoints emit spans per `TRACING.md` §4" clause in one coordinated sweep
(the update-all-sites law).

## 5. Sampling — class-aware head sampling

**Everything is instrumented; what is *kept* is decided at the root.** The keep
decision is made once, when the trace roots, and propagates in `flags` — so a trace is
kept or dropped **whole** (TR6), never half-assembled.

This is head sampling, and that choice is evidence, not habit: Dapper (default 1/1024,
adaptive to a target kept-rate, 0.01% floor on the hottest services) and Canopy
(1.3 B traces/day, a per-tenant token bucket at trace start) both sample at the head —
the research grep-confirmed **neither planet-scale system tail-samples**; tail
sampling is a collector-era technique whose own docs call it stateful and
resource-intensive, with no hyperscale production precedent. Deciding at the root is
what lets most traces never leave the host — the first fan-in bound.

**The keep decision is class-aware**, keyed on the root chokepoint's class
(config-registered, boot-validated):

- **100%-kept classes** — the operations we can never miss, all bounded-rate by
  construction: summon/teardown, handoff, materialization/landing, merge-gate
  passage, Guardian escalations and verdicts, cross-region operations, and the
  agent-loop turn operations the detection stack watches.
- **Derived-baseline classes** — high-volume micro-ops (a cache get, a queue poll, a
  store read): kept at a rate **derived** from the kept-volume budget ÷ measured class
  volume, adaptive (Dapper's target-rate model). Never a hand-picked percentage.
- **Errors in baseline classes are detected by metrics, localized by traces**: the
  per-chokepoint error/latency envelopes (`MONITORING` §5, `HANDOFF` §2) trip
  detection on 100% of traffic; the kept sample plus the 100% critical classes supply
  the trace when an investigation needs the path. Detection never depends on having
  kept a particular routine trace.
- **Tail sampling is a future opt-in** for a declared low-volume, high-value class —
  gated on a declared workload property like every opt-in in this corpus — never the
  default.

## 6. Assembly, storage, consumers (the seam to the collector)

Kept spans flow with telemetry up the existing pipeline (node ring → federation), and
a kept trace's spans converge for assembly keyed by `trace_id` at the regional tier —
**assembly mechanics, storage tiers, and retention are `COLLECTOR.md` §8's** — the
weighted-HRW assembler, accepted 2026-08-22 (this spec owns emission, propagation,
and the keep decision; the seam is: every kept span carries `trace_id` such that
convergent assembly is possible). A stored trace is one
row keyed by trace id (the Dapper shape), in the operational plane — never the
ledger. Consumers read via IAM's `observability` capability (`trace(target)`):
the detection stack and the SRE-Scribe (localizing a flagged degradation), the
Archivalist (investigation), the user (surfaced through review surfaces). Cross-region
assembly (spans of one operation in several regions) is deferred to the sibyl
branch; v1 assembles region-local.

## 7. Provenance and trust

Spans are provenance-classed like every signal (`MONITORING.md` §8): **host-observed**
spans (warden, VMM device counters, gateway, store, consensus — every device-boundary
crossing is host-visible by construction) are authority-grade; **guest-reported**
spans (the agent runtime's interior detail) are enrichment-grade. At Bar B a
compromised guest can lie only in its own interior spans — the host-observed skeleton
of the same trace stands, and divergence between the two is itself a detection signal
(the lie-detector pattern). Detection reads the authority skeleton; narration and
investigation may use the enrichment detail.

## 8. Laptop degenerate

`N=1`: the regional tier is the node; assembly happens in the one collector; the same
classes, the same derived rates (the budget formula yields laptop numbers from laptop
anchors). No mode.

## 9. Acceptance criteria

| # | Criterion | The failure it catches |
|---|---|---|
| TR1 | **Three-id disjointness**: no shared identity across `request_id`/`trace_id`/`caused_by`; cross-links are opaque references; a durable trace store keyed on `caused_by` is unrepresentable (architecture test) | a second claims ledger; plane fusion |
| TR2 | **Total propagation**: every wire message carries `TraceCtx` (codec-rejected absence); every chokepoint continues the incoming context; system-minted messages root fresh traces | an untraceable hop; an "exempt" message class |
| TR3 | **Boot-validated roster**: span sources ≡ registered chokepoints; an unregistered emitter fails startup; the coverage walk finds no chokepoint without a span | a silent instrumentation gap |
| TR4 | **Zero hot-path cost**: emission is async; traced-op latency at 100% emission is unchanged within the ratcheted floor; no span path blocks the operation | tracing slowing what it traces |
| TR5 | **Content-free**: the H8 type-walk passes over every span type; chokepoint names and statuses are closed registries | work content or free text in a span |
| TR6 | **Whole-trace keep coherence**: the root decision propagates; no mid-trace flip; a kept trace is complete modulo counted loss | half-kept traces; skewed samples |
| TR7 | **Class coverage**: 100%-classes always kept (differential vs oracle); baseline classes within the derived budget, adaptive | a missed handoff trace; budget blow-through |
| TR8 | **Loss honesty**: ring overflow yields counted gaps; an assembled trace with gaps is marked incomplete, never silently whole | fabricated completeness |
| TR9 | **Every constant derived** (keep rates, budgets, class lists at definition sites); zero hand-picked sampling numbers | magic rates |
| TR10 | `N=1` ≡ fleet (no mode) | mode creep |

## 10. Test matrix (SIM)

| Test | Asserts |
|---|---|
| Propagation fuzz | TR2 (every hop, every message class, context present + parented correctly vs a serial oracle) |
| Roster boot check | TR3 (drop one registration ⇒ boot fails; coverage walk) |
| Overhead ratchet | TR4 (100% emission vs tracing-compiled-out, ratcheted delta) |
| Keep-coherence differential | TR6/TR7 (root decisions vs an oracle; 100%-class completeness; baseline within budget) |
| Gap honesty | TR8 (induced ring overflow ⇒ counted gaps, trace marked incomplete) |
| Content-free CI | TR5 (H8 type-walk over span types) |
| Cross-plane pivot | TR1 (span→claim-UID resolves via an authorized ledger read; claim→trace resolves via an authorized operational read; no shared key exists) |
| Laptop parity | TR10 |

## 11. References

Dapper (Google TR dapper-2010-1): head sampling 1/1024 + adaptive target-rate,
out-of-band collection, trace-as-one-row, span cost ~200 ns / 426 B, daemon <0.3%
core. Canopy (SOSP'17): 1.3 B traces/day, token-bucket head sampling at request
entry, TraceID-sharded convergence, feature extraction. W3C Trace Context
(`traceparent`): the 16+8+flags shape (exemplar). OTel sampling docs: head vs tail
definitions; tail's stateful cost and the same-collector convergence constraint.
Companions: `PROTOCOL.md`, `WIRE_FORMAT.md`, `MONITORING.md`, `HEALTH.md`,
`HANDOFF.md`, `LEDGER.md` (§9.8), the COLLECTOR spec to follow.
