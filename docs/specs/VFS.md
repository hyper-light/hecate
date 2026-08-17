# SPEC: the VFS — one chunk store, manifest layers, three volume roles, the tool plane

Status: presented for acceptance (grilling Branch 5; directions ratified: 5a
chunk-native unified store, 5b tool plane over it with the third store deleted).
References: Sylk VFS/OT survey and Tool VFS survey on file (GRILLING.md); Nix/Bazel/
OCI content-addressed distribution pattern.

## 1. The store

One content-addressed chunk store per node. Everything on it: base images, green,
pod overlays, Designer volumes, tool blobs, guest images, registry content.

- **Identity**: BLAKE3 — the single hash family, everywhere (chunks, manifests,
  content identity, schema hashes).
- **Chunking**: content-defined (FastCDC-family), boundaries stable under insertion;
  min/avg/max chunk sizes derived from measured device and workload anchors, with
  derivations at the definition sites. Files at or below the minimum are one chunk —
  the common small-source-file case pays one hash and no boundary scan.
- **Placement in memory**: chunk bytes live in our own slab/mmap arena (off-GC-heap
  equivalent; budget-charged). **No disk spill exists.** Exhaustion is a typed
  retryable error plus pressure telemetry to the Guardian — never a hidden write.
  **Reconciliation with the node pack-volume store** (`OBJECT_TIER.md` §2/§5,
  amendment 2026-08-17): the arena and the pack-volume store are the RAM and
  NVMe **tiers of this one store** — movement between them is explicit
  lifecycle (flush-at-seal, fill-on-demand), never spill; "no disk spill"
  means exhaustion is typed at each tier, not that no NVMe tier exists.
  Exactly one on-disk store format exists (the pack volume, cache and origin
  roles alike) — the EdenFS two-overlapping-disk-caches admission is the
  binding counter-receipt.
- **Lifetime**: owner-managed acquire/release counts on generational handles (the
  memory doctrine's shared-immutable mechanism — refcounting as auditable data in the
  owner's state, not smart pointers). A stale handle is a typed error.
- **Concurrency**: hash-sharded across runtime shards by leading hash byte; each
  shard's store partition is a single-owner task. No locks, no cross-shard sharing —
  cross-shard chunk transfer is by handle message.
- **Integrity**: every read is hash-verifiable; corruption is detected at read and is
  a typed hard error naming the chunk — never silently served.

## 2. Manifests and layers

A **manifest** is the content-addressed unit of "a filesystem state": ordered
`path → (chunk list, mode, size)` entries, deterministically encoded (hecate-wire),
hashed like any content.

| Layer | Representation |
|---|---|
| Base image | full manifest, produced at session open (gitignore-filtered scan) |
| Green | a **versioned manifest chain**: each merge produces version N+1 as a delta over N; advanced only by the merge serializer |
| Pod work-volume overlay | delta manifest over its declared green base |
| Designer volume | standalone manifest tree, outside the merge machinery |
| Tool manifests | RO manifests produced by the provisioner (§6) |
| Guest images, registry content | manifests like everything else |

- Snapshot = manifest reference: O(1) to take, O(paths) to materialize a listing,
  zero bytes copied.
- Memory is **O(unique bytes) node-wide**: identical content across pods, sessions,
  layers, and tools deduplicates at the chunk store by construction.
- Deterministic iteration order everywhere a manifest is walked (runtime map rules).

## 3. Volume roles

Four roles, one store beneath them (intentional architecture, ratified;
scratch added by `SERVING.md` acceptance 2026-08-16):

1. **Work volume** — per-pod RW overlay of its assigned work: writes land
   server-side into the overlay's delta manifest; basis leases validated at the
   serving boundary. ("Workspace" is retired from the design vocabulary
   (`SESSIONS.md`); the in-guest mount path may keep any conventional name.)
2. **Green** — the session's versioned, serializer-owned staging truth
   (increment-validated work only; `MERGE.md`). Extended by chain append, never
   written in place; serving instances carry no write path (`SERVING.md` §4).
3. **Tools** — read-only composition of the pod's resolved tool manifests (§6).
4. **Scratch** — pod-local, unwitnessed, unjournaled, unmergeable; mounted at
   template/registry-declared redirect paths (`target/`, `node_modules/`,
   caches) and freed at pod teardown. Exists so the witnessed overlay holds
   source-tree mutations only (`SERVING.md` §2; the EdenFS-redirections /
   CitC-vs-ObjFS split).

The Designer's volumes are work-volume-role in isolation but never enter merge; its
disk path is the Guardian-staged overflow flow with a threshold derived from the
volume's budget.

## 4. Budgets

All derived at boot from physical anchors (system memory, summon allocations):
per-volume budgets from the summon; store arena budget from node memory; charge on
acquire, release on drop, reconciled transactionally with writes (a failed charge
rolls the write back with a typed error). Pressure telemetry streams to the Guardian
— the primary consumer — and to Scribes via the health plane.

## 5. Serving: the guest mount

- Host-side server per pod, speaking virtio-fs to the guest; one mount presenting
  the composed view: work-volume overlay (RW) ⊕ green base (RO) ⊕ tools (RO).
- The serving cut is the path-based namespace interface (stat/list/read/write +
  handle layer) proven in Sylk — now served over virtio-fs instead of in-process
  FUSE. Writes are captured server-side into the overlay; RO layers return
  EROFS-equivalent typed errors on write.
- **Witnessed writes yield per-file op logs**: every captured write is a
  content-bearing journal record (`SERVING.md` §2); at seal, per-file edit ops
  are derived from successive witnessed versions by a pure, version-pinned
  deriver — the landing engine's replay input (`SESSIONS.md` §5 layer 2). The
  derivation runs off the hot path; same inputs ⇒ same ops, always.
- Range reads and streaming are first-class (no whole-file `Vec<u8>` transfers as
  the only verb — the Sylk §4.4 portability list, closed).
- **Merge–splice seam** (`MERGE.md` §1): accepted ops rewrite only the chunks their
  mapped ranges touch — re-chunk the affected region, splice the manifest, bump the
  green version. The merge engine operates on logical byte streams; chunking is
  storage; neither leaks into the other.
- Cache coherence: manifest versions are the invalidation unit; the server advertises
  attr/entry validity derived from layer volatility (RO layers cache long; overlay
  entries invalidate on own-writes only; green base invalidates on version advance).

## 6. The tool plane (no third store)

- **Tool = manifest + provenance** over the unified store. The Tool VFS's store is
  deleted; its *governance* survives whole:
  - **Provisioner service**: ecosystem plugins parse install intents; recipes are
    content (content-addressed, deterministic `RecipeID → ManifestID` under the
    determinism profile); builds run in deny-first sandbox pods; lockfile witnesses
    are per-session state, no silent upgrades.
  - **Three Guardian gates**, wired, not prose: provision (full transitive closure +
    provenance inventory before any fetch), sandbox capability
    (APPROVED_WITH_CAVEATS downgrade supported), disk fallback (consented,
    hash-pinned, permanently tagged).
  - Hash mismatch on any fetch ⇒ refusal + durable violation event. Verification is
    every-fetch, intrinsic to content addressing.
- **Three tiers**: base toolchains in role guest images (pinned at summon);
  provisioned tooling as RO tool manifests (this plane); work-volume-local artifacts
  (a project's `node_modules`) as ordinary overlay writes — deduplicated anyway.
- Tools execute **in-guest** against the pod's own mounts. There is no shared
  execution service; sharing is storage- and governance-level only.

## 7. Distribution and migration

- **Chunks travel by hash** (the Nix/Bazel/OCI pattern): a node missing content
  cache-fills from a peer or origin and verifies intrinsically. Immutable +
  self-verifying = the easy distribution problem; no ordering or consensus applies
  to chunks.
- **Session migration** (colocation-unit move): transfer manifest refs + lazy chunk
  fetch on demand; the WAL side is snapshot + tail export (`WAL.md` §6). State
  transfer cost is O(manifest) up front, O(touched bytes) over time.
- The **registry** (`REGISTRY.md`, accepted) rides the same store: its kinds are
  content-addressed documents; Guardian staging inventories content, never trusts
  manifests' self-description.

## 8. Test matrix (failure each catches)

| # | Test | Catches |
|---|---|---|
| V1 | Chunking determinism: same content ⇒ same chunk set and hashes, across platforms and runs | platform-divergent identity — cache poisoning by accident |
| V2 | Refcount balance fuzz: random acquire/release/GC interleavings ⇒ zero orphan chunks, zero premature frees (generational handle checks) | leaks; use-after-free-by-index |
| V3 | Isolation: pod A's server can never resolve pod B's overlay content, by construction test over the composed namespaces | cross-pod bleed |
| V4 | Dedup effectiveness: N pods with overlapping trees ⇒ store bytes ≈ unique bytes (ratcheted bound) | O(pods × bytes) regression |
| V5 | Budget: exhaustion ⇒ typed retryable + rollback of the failing write + pressure telemetry; memory bounded under sustained overload | hidden growth; silent refusal |
| V6 | Serving conformance: POSIX-subset syscall corpus (open/read/write/rename/stat/readdir/mmap-read) green through a real guest on Linux/macOS/Windows hosts | virtio serving drift; the REAL≠SIM class |
| V7 | RO enforcement: writes to green-base and tool paths from the guest ⇒ typed EROFS-equivalent; overlay writes land server-side with lease validation | write-authority leaks |
| V8 | Corruption: flipped chunk bytes ⇒ read fails typed, names the chunk; never served | silent corruption |
| V9 | Provisioner gates: unapproved source, hash mismatch, ungated build each refused with durable violation events; APPROVED_WITH_CAVEATS actually downgrades the sandbox config | half-wired governance (the Sylk substrate fate) |
| V10 | Migration: manifest-ref transfer + lazy fill reproduces byte-identical trees on the receiving node | migration divergence |
| V11 | Snapshot cost: manifest snapshot is O(1)/O(paths), measured, never O(bytes) | accidental deep copies |

## 9. Acceptance criteria

1. **One store**: no second content store exists anywhere in the tree (architecture
   test — the Sylk two-stores-two-hashes fault is unrepresentable); BLAKE3 is the
   only content hash.
2. Memory is O(unique bytes): V4's ratcheted dedup bound holds in CI.
3. No disk-spill path exists in the store or overlays; exhaustion is typed and
   counted.
4. Every guest-visible byte is hash-verifiable; V8 gates every merge.
5. Serving conformance (V6) green on all three platforms before any agent work runs
   on that platform.
6. All three Guardian gates wired end-to-end with refusal tests (V9) before the
   provisioner accepts its first real recipe — capabilities ship wired or not at all.
7. Leases validated at the serving boundary; correctness never depends on them
   (`MERGE.md` owns conflict truth).
8. Budgets, chunk parameters, cache validities: derived, with derivations at
   definition sites; ratcheted perf floors (serve latency p99, chunking throughput)
   from first CI baseline.
