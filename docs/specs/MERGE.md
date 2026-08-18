# SPEC: the merge engine — canonical rebase, deterministic verdict, distributed staging volume

Status: ACCEPTED 2026-08-18 (whole-spec rewrite through the grilling arc;
A1 re-audited and FUSED same day — proposer = session-group leader, term
is the only fence, generation/SerializerOpen deleted; descriptor increments +
fixed-layer ops documents (A2, corrected twice under maximal audit),
replicated-state-machine merge service, green version replication, the
volume-object model, and the submission transaction — all receipted; dossiers
in GRILLING.md). References: OT correctness research; Raft §5.3 (follower
apply); ZooKeeper/Zab epochs, Kafka KIP-101, BookKeeper fencing (fence-in-log
precedents); K8s image-by-digest + EdenFS lazy projection (volume model);
FastCDC/BLAKE3/memcmp/decode throughput receipts; Sylk merge fault family.

## 0. How it works — the human picture

**Every machine in the fleet looks the same:**

```
┌─ machine (any node) ────────────────────────────┐
│  host process                                   │
│  ├─ blob store (RAM + local disk)               │
│  │    immutable blobs, each named by its hash.  │
│  │    Never edited, only added. On a miss, the  │
│  │    store PULLS the blob by name from any     │
│  │    machine that has it, verifies, keeps it.  │
│  ├─ file server (the EdenFS role)               │
│  │    projects volumes to THIS machine's pods,  │
│  │    served from the local store + pull-on-miss│
│  └─ pods (VMs) — agents live here               │
└─────────────────────────────────────────────────┘
```

**Two rules govern all data movement**: bytes move machine-to-machine only
as *pull-these-named-blobs* transfers, verified on arrival; everything else
is tiny notes (refs, ~100 bytes). Machines appear in no API — pods, volumes,
and services are addressed by identity; placement is the scheduler's private
concern (the single-surface law, SERVING §0).

**Green — the session's shared staging volume — demystified**: green is the
session-wide copy-on-write VFS volume where merged work stages before the
Arbiter-gated disk commit (Sylk's global session VFS, matured). It is *not a
disk anywhere*: it is a numbered series of **tables of contents**
(manifests). Version 43 is a small document naming blobs; it shares every
unchanged blob with version 42 by name — that structural sharing *is* the
copy-on-write. Any pod on any node attaches to any version (§6); readers
attach to immutable versions; **no mount writes green — its writer is the
log** (§2).

**The merge service is a replicated state machine whose proposer is its leader:**

```
        the replicated merge log (session group: 3 machines, identical copies)
        ┌──────────┬──────────┬──────────┐
        │  B: copy │  D: copy │  E: copy │
        └────▲─────┴────▲─────┴────▲─────┘
             │ appends   │ applies  │ applies
        ┌────┴─────┐ ┌───┴────┐ ┌───┴────┐
        │ LEADER = │ │follower│ │follower│   ← merge service, 3 instances
        │ PROPOSER │ │ (warm) │ │ (warm) │
        └──────────┘ └────────┘ └────────┘
```

All three instances apply every committed merge record (that is what a Raft
state machine *is* — paper §5.3). **The proposer is a role of the session
group's Raft leader** — deciding verdicts and advancing the version number
is what leadership of this group means; there is no separate writer role
and no separate fence. If the leader's node dies, a follower wins the
election (log-current by Raft's own restriction) and *is thereby* the new
proposer — no replay, because it was never behind; and it already holds
the bytes (§5).

**One edit, three machines, walked** (pod on A edits `main.rs`; session home
= B; reader pod on C):

```
 A (worker)                B (home)                    C (reader)
 1. pod saves file
 2. A's host seals it: new
    blobs c1,c3 → A's OWN
    store + a small change
    description
         │ 3. note (~100 B): "merge desc=D,
         │    result=M, base=green v42"
         ├────────────────────►
         ◄──"send D,c1,c3"─────┤ 4. B pulls the new bytes BY NAME
         ├──── ~24 KB ────────►     (unchanged blobs never move)
         │                  5. conflict check (byte ranges vs
         │                     merges since v42)
         │                  6. B builds ToC v43; PLACES v43's new
         │                     blobs on D and E; awaits acks (§5)
         │                  7. appends "v43 = ToC #abc" to the log;
         │                     D and E apply; head hashes compared
         │                          │ 8. note: "green is now v43"
         │                          ├──────────────────────►
         │                          ◄──"send c1,c3"─────────┤ 9. C pulls only what
         │                          ├──── ~24 KB ──────────►    it lacks, by name
         │                          │                     10. pod on C re-attaches
         │                          │                         to v43, reads locally
```

Nobody wrote to a shared disk; there isn't one. The 24 KB of genuinely new
bytes crossed the network at seal-pull and reader-pull; everything else was
notes. The formal sections below are details of this picture.

## 1. Model

Per session: one **merge service**, run as a replicated state machine on the
session group's member nodes (§0 diagram). Inputs are **increments** —
constant-size descriptor messages (never bytes; §4):

```rust
Increment {
  claim: ClaimRef,                 // the work this increment belongs to
  base: GreenVersion,              // declared, never inferred
  post_state: ManifestRef,         // the sealed final volume state (in the store)
  ops_doc: ContentRef,             // the derived op-description document (in the store)
}
```

Pipeline per increment, inside the proposer, deterministic end to end:

```
dedup:   increment identity = hash(claim, base, post_state, ops_doc);
         seen-in-log ⇒ ack-without-reapply (retries always safe)
fetch:   pull ops_doc (+ ranges as needed) by name — outside the pure core
map:     position-map ops through canonical deltas (base..head]
verdict: two pure passes (§3)
apply:   splice accepted ops into a new manifest (chunk-granular, VFS §5)
place:   push the version's new blobs to the session-group members; await
         acks — on the QUORUM-CRITICAL TRANSFER class (PROTOCOL §3's
         non-interference law), never the opportunistic bulk lane
commit:  merge record {id, verdict, version, manifest_hash, term}
         through the session group — a merge that cannot be recorded never
         applies; a version that is not placed is never referenced
```

## 2. Writer authority — the proposer is the leader

(Re-audited and fused 2026-08-18; the prior generation/`SerializerOpen`
design is deleted — see the rejected-alternative record below.)

- **The merge proposer is a role of the session group's Raft leader.** The
  fence is the **term** — stamped on every merge record, enforced natively
  by Raft (a deposed leader's appends never commit). There is no second
  epoch: no shipped system fences a replica-resident writer with an epoch
  separate from its own group's term, and the fusion receipts are
  unanimous — TiKV's region write role IS its Raft leader; KRaft's active
  controller IS the quorum leader; Multi-Paxos's distinguished proposer IS
  the leader.
- **Succession is leadership**: a new leader's term-opening no-op (the
  Ongaro guard, CONSENSUS §4) is the succession marker; promotion after
  failure = election among log-current followers (election-timeout scale);
  planned handoff = leadership transfer (CS6). Warm followers apply every
  record continuously (§5) and hold the placed bytes, so a new proposer
  starts at the head with content in hand.
- **Placement preference, load-bearing**: session-group leadership is
  fortified at the colocation node (leadership-follows-the-unit); on
  divergence, leadership transfers back within a derived bound — the
  scheduler moves the unit only when the node itself is unhealthy.
- **Intra-process races need no distributed fence**: hecate-rt shards are
  single-threaded and every task's owner holds its handle — a torn-down
  task never runs again (RUNTIME task-lifecycle law). A paused-and-resumed
  *process* is a stale leader; term + fortification + CheckQuorum depose
  it.
- **Content-addressed writes still need no fencing** — a stale instance's
  blob writes are orphans GC sweeps; authority lives entirely in log
  append, which the term governs.
- **Rejected-alternative record**: the prior design — a proposer fenced by
  `SerializerOpen{generation}` markers, free-floating relative to
  leadership — is CockroachDB's pre-fortification leaseholder
  architecture: a separately-fenced in-group writer whose divergence from
  the Raft leader produced the documented "leader-leaseholder splits"
  (indefinite-outage variant), retired by the Leader Leases protocol
  change that merged the roles (85% lease-CPU reduction, seconds-scale
  recovery). We do not rebuild what they spent a protocol change deleting;
  the fortification their fix rests on is already accepted law
  (CONSENSUS §3).

## 3. The verdict — two pure passes

A deterministic function of (canonical history since `base`, mapped
increment, referenced immutable content). Classes: **Accept** (all mapped
ranges disjoint from intervening effect ranges) · **AcceptIdentical**
(same-range concurrent inserts with identical bytes — recognized, not
resolved) · **Conflict** (overlap/containment; edit anchored in a concurrent
delete; same-position differing inserts; rename/rename; create/create
differing).

- **Pass one (pure)**: sweep-line interval overlap on declared ops,
  O((n+m) log(n+m)); emits verdicts plus the list of same-range insert
  overlaps needing identity checks. No diff inference exists anywhere — the
  diff3 pathology family stays structurally unreachable.
- **Fetch (between passes, outside the pure core)**: read the candidate
  source ranges — immutable, content-addressed, typically local.
- **Pass two (pure)**: memcmp results in hand, finish the verdicts.
  Common path: zero content reads. Rare path: one range-compare
  (memory-speed; receipts on file). The always-paid seal-time hashing of an
  earlier draft is deleted.
- Position mapping is one-directional through canonical history and
  composes: `map(a..c) = map(b..c) ∘ map(a..b)` (M4). Leases fast-path,
  never guard.
- Verdict purity is the engine's central theorem — and under the RSM (§5),
  appliers recomputing the verdict at apply *is* deterministic apply, the
  definitional SMR shape.

## 4. Increments and the ops document — descriptors, never bytes

By the time an increment exists, seal already chunked, named, and stored
every changed byte (SERVING §2). Increments therefore carry **no content**:

- **The deriver emits the composed net op set**: witnessed ops compose by
  pure interval algebra (Insert-then-overlapping-Delete cancel and split) —
  the M4 composition law applied intra-increment. Every surviving insert's
  bytes exist in the sealed post-state *by construction*. **Composition of
  declared ops is arithmetic on facts; reconstructing ops by comparing file
  states is the banned diff inference.** The deriver does only the first.
- **The ops document** is content-plane, content-addressed, and uses the
  **fixed-layer discipline** (the second lawful encoding form, per the
  PROTOCOL §1 envelope precedent — `repr(C)`, explicit-endian, compile-time
  asserts, canonical by construction): a hecate-wire header + a flat array
  of 32-byte records `{kind, path_idx, at, len, src_off}`. Receipts: decode
  of compact varint formats measures 0.2–1.6 GB/s; bounds-checked in-place
  cast runs at memory speed — the fixed layer is load-bearing for the §12
  latency budget, and the pattern is Cap'n Proto/FlatBuffers/Arrow/LMDB
  shipped practice.
- No byte-bearing field compiles in any increment type (refs and hashes
  only — the WF8 derive machinery). Message size is invariant in op count
  and content size.
- **Retention**: merge-log-referenced manifests and ops documents are
  OBJECT_TIER §7 GC liveness roots until log truncation (tested, M14e).

## 5. Apply, placement, and version replication

- **Splice**: accepted ops rewrite only the chunks their mapped ranges touch
  (VFS §5 seam); source bytes come from the sealed post-state through the
  store. New chunks + the new manifest land in the proposer's local store.
- **Placed strictly precedes referenced — applied to green** (the OT14
  ladder instantiated here): the merge record referencing manifest `#abc`
  **does not commit until the version's new blobs are replicated to the
  session-group members and acked**. The replica set *is* the session
  group: the nodes holding the log also hold the bytes, so a promoted
  applier has log + applied state + content — failover with zero
  unreachable refs. Cost: one intra-region replication round trip per
  commit (~1–2 ms class, pipelined across increments) — the durability the
  chain requires. The durable-plane copyset placement proceeds
  asynchronously behind this as the archival tier (the ladder's later
  rungs, unchanged).
- **Appliers recompute — inputs are authoritative** (re-audited
  2026-08-18): every session-group member applies each committed record by
  **recomputing the full two-pass verdict from the record's inputs** — the
  refs, whose bytes it holds because placement preceded commit. This is
  deterministic apply, the definitional SMR shape (Schneider, Calvin,
  TigerBeetle — the input-logging canon). The recorded verdict and
  manifest hash are **cross-checks only, never an apply path**: a mismatch
  between an applier's recomputation and the record is fatal-and-loud at
  that index, before any downstream read. Output-logging's poison — a
  wrongly computed output replicating verbatim so every replica agrees on
  the wrong answer — is thereby unrepresentable: a proposer lying about a
  verdict, a memcmp, or a manifest hash trips every applier's own
  recomputation. Records stay small (~100s of bytes of refs + checksums);
  applying stays cheap (µs-class recompute + local reads of placed
  content).
- **Continuous divergence detection, free**: beyond the per-record
  cross-check, replicas compare green-head manifest hashes per log index —
  O(1), because the state IS a hash (versus etcd's periodic CORRUPT ALARM
  and CRDB's 24-hour SHA-512 cycle). All divergence is **fatal-and-loud**
  (alarm + refuse), never silently reconciled — the disposition every
  precedent agrees on.

## 6. Green as a volume — objects, claims, attachments

Green is a **first-class volume object** under the volume lifecycle
(VFS §3b): pods declare volume claims in their summon manifests; at bind the
node's serving layer creates an **attachment** — a per-(pod, volume) object
pinning the version, holding the lease, wiring the warden's scope entries,
running the declared prefetch, and carrying the accounting. Readers attach
to **immutable versions** (the container-image-by-digest sharing pattern —
per-pod instantiation from the local store, never a shared live mount);
version advance is the pod's next re-attach, an explicit lifecycle event.
**No mount writes green**: the writer is the log (§2); "write access" is the
term-holder's role, not a filesystem mode. Cross-node access is the read-through fill of
§0 — mount-anywhere with locality as caching (receipts: K8s images, EdenFS's
own four-tier read path, Nix/OSTree).

## 7. The submission transaction

An agent submitting work is making a network transaction. The sequence,
with its governing settlements:

```
 agent pod P        host A            proposer (B)        session group      frontier→Arbiter
 1. "submit" ─ring─► warden inspects (claim scope), then host-side:
 2.                  SEAL: drain, compose net ops, chunk to A's store
 3.                  ── Increment ~100 B (claims lane, request_id) ──►
 4.                  ◄─ pull ops_doc + new blobs by name (bulk lane) ─  [dedup first]
 5.                                    verdict (two-pass) + splice
 6.                                    ── place new blobs ──► acks (D, E)
 7.                                    ── commit record ────► appliers apply,
                                                              head hashes compared
 8. ◄────────────── Verdict response: Accept{v} | Conflict{windows} ──
                                       └── merge log ──► frontier batches versions,
                                           issues REVIEW CLAIMS via the ledger;
                                           Arbiter pods review asynchronously
```

- **Submission topology (re-audited 2026-08-18)**: resolver-cached direct
  submission to the session-group leader, with the **piggyback rule**: any
  NACK from a non-leader carries the current leader identity and term, so
  one retry suffices (the TiKV shape). Storm guards, named: resolver
  refresh is **single-flight per session** (concurrent submitters share
  one refresh — the CRDB NotLeaseholder-storm class, issue #23543, closed
  by construction); a NACK without leader info falls back to the session
  directory with backoff (the redirect ping-pong class, #22837). Rejected
  alternative: etcd-style server-side forwarding — hides the leader at
  the cost of a permanent extra hop and a silent latency intermediary;
  with the resolver already in the architecture, the piggyback costs
  nothing.
- The agent **parks** on submit (long-op turn shape) and resumes with the
  verdict. **The Arbiter never receives the submission** — it receives
  review claims derived from the merge log; the gate (§9) fires at work-claim
  close, not in this pipe.
- **Failure semantics**: timeout ⇒ resubmit (identity dedup makes retries
  always safe); home-node failover ⇒ the new session-group leader IS the new proposer; the resolver re-points, resubmit lands there, at-most-once holds; submitter dies after
  commit ⇒ the claim's state shows the increment applied — the handoff
  successor resumes from the claim, not a lost ack; source node dies before
  fetch ⇒ typed failure, claim redelivers (the priced seal-to-land loss
  window, OBJECT_TIER §3's formula).
- **Latency**: seal (local) + claims RTT + bulk fetch + placement acks +
  commit + response ≈ single-digit ms intra-region, pipelined; invisible
  under an agent turn. Laptop: identical sequence, in-process, µs.

## 8. Conflict windows and the corrective path

Unchanged in substance: a `Conflict` carries per-path byte windows plus the
refs of the colliding claims — evidence, not markers; presentation in line
runs with optional tree-sitter labels (labeling only, never AST
auto-resolution). Fast path: corrective claim to the authoring Engineer —
rebase against the window, resubmit (a rebased increment has a new identity;
dedup never blocks it). Escalation at derived recurrence thresholds: the
Arbiter adjudicates and authors corrective routing. Rejects are
non-blocking; the proposer never stalls.

## 9. The Arbiter gate flow

Unchanged in substance: the **frontier service** (colocated with the session
home; state fully re-derivable from the merge log) batches contiguous green
versions into review units, issues review claims (at-most-once, lease-expiry
redelivery), and serves hot-context queries to Arbiter replica pods over
directed request/response. The ledger carries only review claims and finding
testaments. Streaming analysis makes the whole-work verdict largely
precomputed; the gate itself is a chokepoint where the verdict's structural
consequence fires — validated ⇒ per-descriptor disk commit unlocks — never
an evaluator.

## 10. Contention control and tripwires

Unchanged: same-scope work serializes above the engine (claim scopes,
`depends_on`, lease ordering); the engine's rejects are the residue. Ledger-
visible tripwires with derived thresholds: sustained rebase-retry rate on a
region ⇒ Arbiter escalation + rescoping; p99 intervening-deltas-per-merge ⇒
reopens the eg-walker branch (ADR-0005) with data in hand.

## 11. Laptop degenerate

One node: the session group is one replica (self-ack), placement is a local
write, every arrow in §7 is an in-process call, attachments project from the
one local store. Same code, same sequence, no modes. Receipt: etcd's own
fault-tolerance table — N=1 is the same Raft code path with quorum = 1; no
special commit path exists. The fragile step is GROWING 1→2 (a two-member
group still tolerates zero failures; member-add's joint quorum is the
delicate transition) — the laptop-to-fleet growth path, owned by Branch 38.

## 12. Test matrix

M1–M12 as before (purity; oracle fuzz; replay equivalence; mapping
composition; AcceptIdentical; apply/record atomicity under power-cut;
deterministic ordering; rename matrix; frontier at-most-once; TLA+ model;
diff3 calibration reported-never-gated; no-LLM/no-IO architecture test —
with M12 restated for the two-pass shape: no IO inside either pure pass).

| # | Test | Catches |
|---|---|---|
| M13a–c | Leadership races: leader kill / pause-resume / transfer / partition-heal fuzz ⇒ stale-term records never commit; single version lineage; no state names a proposer except leadership itself | the Kleppmann class; the CRDB split class made unrepresentable |
| M13d | Writer-roster boot check (CONSENSUS §6): merge proposer registered as leader-fused | unclassified writer |
| M13e | Term check does zero crypto/allocation | fencing as hot-path tax |
| M13f | Leadership-follows-the-unit: fortification preference holds; forced divergence ⇒ transfer-back within a derived bound; proposals pay at most one extra hop meanwhile | silent leadership drift |
| M14a | No byte-bearing field compiles in increment types (trybuild) | inline content returning |
| M14b | Same witnessed stream ⇒ identical ops-doc ContentRef, cross-platform | split-brain derivation |
| M14c | Splice ≡ reference applier (differential) | descriptor path losing bytes |
| M14d | Identical concurrent edits: one range-compare on overlap path, zero content reads on common path (instrumented) | false conflicts; regression of the lazy check |
| M14e | Log-referenced content survives GC until truncation | replay reaching for collected bytes |
| M14f | Increment message size invariant | constant-size erosion |
| M14g | Write-then-revise fuzz: every net `src_off` valid; net-apply ≡ raw replay; composition deterministic | dangling provenance |
| M14h | Merge-path p99 latency ratchet from first-light baseline | sub-ms property decaying |
| M15a | Kill proposer at every point splice→announce ⇒ version fully readable via promotion; chain never dangles | unreachable-head loss |
| M15b | No merge record commits before R placement acks (OT14-for-green, structural) | reference-before-placed |
| M15c | Applier convergence: green-head hashes identical at every index under nemesis; divergence ⇒ fatal-loud | silent split-brain green |
| M15d | Promotion latency ≈ election-timeout scale, no replay on critical path (measured) | cold-failover regression |
| M16a | Attach-denied: undeclared volume claim refused at bind | ambient-mount regression |
| M16b | Version stability: a pod's view never changes without re-attach, fuzzed across concurrent merges | ground shifting under mounts |
| M16c | Re-attach anywhere: kill node, re-summon, attach same version elsewhere, byte-identical | locality masquerading as availability |
| M17 | Submission-transaction fuzz: kill any party at any step ⇒ exactly-once apply, agent resumes with a truthful verdict or claim-driven redelivery | the transaction's failure table |
| M15e | Lying-proposer injection: a corrupted recorded verdict, memcmp result, or manifest hash trips every applier's recomputation at that index, fatal-loud, before any downstream read | output-poison replication — the wrong answer agreed everywhere |
| M17b | Resolver-storm fuzz: leadership churn under concurrent submitters ⇒ bounded retries, no ping-pong, single-flight refresh observed (instrumented) | the CRDB retry-storm class |

## 13. Acceptance criteria

1. M1/M2 permanent (verdict purity; zero false accepts/rejects vs oracle).
2. M6 + M15a/b permanent: apply/record atomic; placed-before-referenced for
   every green version; no crash point yields a dangling head.
3. No silent interleave path; every overlap class terminates in Conflict.
4. No LLM/clock/RNG/IO in either pure pass (lint + M12).
5. Frontier state fully re-derivable; review claims + finding testaments are
   the only ledger objects the review pipeline creates.
6. Conflict windows byte-exact; AST label-only.
7. The proposer is leader-fused in the boot writer roster; no
   generation/epoch state exists for it outside the Raft term (M13d/M13f
   permanent; architecture test: grep-proof no second fence).
8. No content byte rides the claims plane in any merge type; increments are
   constant-size (M14a/M14f permanent).
9. The deriver is composed-net-ops with the never-diff clause as text
   (M14g permanent).
10. Green-head hash comparison runs at every applier continuously;
    divergence is fatal-and-loud (M15c permanent).
11. Volume access is attachment-only: no undeclared claim mounts anything;
    no pod's view changes without a re-attach event (M16a/b permanent).
12. Throughput and latency floors ratcheted from first CI baseline
    (merges/sec; verdict µs p99; merge-path p99 incl. placement; promotion
    latency); regression >10% fails CI.
13. Tripwire metrics emitted from day one; thresholds derived at definition
    sites.
