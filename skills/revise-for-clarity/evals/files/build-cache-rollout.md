# Remote build cache for the monorepo CI

**Verification convention:** claims marked [VERIFIED] were reproduced locally against commit
`a3f91c2`. Claims marked [UNMEASURED] come from the vendor's documentation or from reasoning
about the code, and nobody has run them.

CI takes 34 minutes on a clean checkout and 31 minutes on a warm one, because almost nothing is
reused between runs. Every merge to main rebuilds all 240 packages from source, and the queue
backs up for 20 minutes each afternoon when the team lands work before standup. How do we cut
merge-queue latency without rewriting the build system? We should adopt a remote build cache
keyed on content hashes, land it behind a flag, and turn it on for the six slowest packages
first.

## 1. Content hashing is the only key derivation that survives a dependency bump

**A cache key built from the git SHA invalidates everything on every commit**, which buys
nothing, so the key has to come from content. We hash each package's source files, its resolved
dependency versions, and the compiler flags, then use that digest as the lookup key. [VERIFIED]
A one-line change to a leaf package now invalidates 3 of 240 packages instead of all of them.

**Timestamps in generated files break the hash.** Four packages embed a build date into a
generated constants file, so their digest changes on every run even when nothing else does. We
strip the date at hash time and leave the generated file alone. [VERIFIED]

**Symlinks in the vendor directory hash by target, not by path.** This one cost a day to find.
The vendored protobuf toolchain is a symlink into a versioned directory, so hashing the path
produced a stable digest across genuine toolchain upgrades, and the cache served stale objects.
We resolve symlinks before hashing. [VERIFIED]

## 2. Object storage beats a dedicated cache server for our read pattern

**Our reads are cold and wide rather than hot and narrow**, so an in-memory cache server wins
nothing. Each CI run reads 240 objects once and never again, and the working set across a day is
roughly 40 GB. Object storage with a CDN in front of it serves that pattern at a tenth of the
cost of a provisioned cache tier. [UNMEASURED]

**We rejected a self-hosted cache server** because it needs an on-call rotation we do not have,
and a cache outage would block every merge rather than slow it. Object storage degrades to a
cache miss, which is the current behavior.

**We rejected the CI vendor's built-in cache** because it caps entries at 500 MB and six of our
packages exceed that on their own. [VERIFIED]

## 3. Compression choice trades CPU against transfer, and zstd wins at level 3

**Transfer dominates at our object sizes.** The median cached object is 12 MB and the p99 is
180 MB, so the compression ratio matters more than the compression time. zstd at level 3 gets
2.9x on our objects and costs 40 ms per object, against gzip's 2.4x at 90 ms. [VERIFIED]

**Level 9 is not worth it.** It buys another 8% ratio for 6x the CPU, and the CPU comes out of
the same runners we are trying to free up. [VERIFIED]

## 4. Four more passes through the design, and the third one changes the storage layout

**The first pass assumed one object per package.** That produced 240 round trips per run, and at
80 ms of latency each the sequential case cost 19 seconds before any transfer.

**The second pass batched the manifest fetch**, so one request returns all 240 digests and the
runner fetches only the misses. On a warm run that is 3 to 8 objects.

**The third pass changed the layout, and this is the one that matters.** We had been storing
objects under a per-package prefix, which meant the manifest and the objects lived in different
key spaces and could disagree after a partial upload. We now write objects first and the
manifest last, so a manifest entry is only ever published for an object that already exists.
A partially uploaded run leaves orphan objects, which the lifecycle rule reaps after 14 days.

**The fourth pass added a negative cache** for digests known to be absent, so a package that
never caches (the four with nondeterministic output) does not pay a lookup on every run.

## 5. A poisoned cache entry is worse than a slow build, and only the digest protects us

**Nothing authenticates a cache object beyond its digest.** Anyone who can write to the bucket
can serve arbitrary build output to every subsequent CI run, and that output goes straight into
release artifacts. The write credential is scoped to CI and rotated quarterly. [VERIFIED]

**We verify the digest on read.** A downloaded object is hashed before it is unpacked, and a
mismatch is treated as a miss rather than an error, so a corrupted entry degrades to a rebuild.
[VERIFIED]

**A malicious PR cannot poison the shared cache**, because pull-request runs read the cache and
never write it. Only post-merge runs on main hold the write credential. [VERIFIED]

## 6. The flaky-test suite interacts badly with caching, and we cannot fix that here

**Eleven tests fail intermittently and pass on retry.** A cached test result hides the flake
rather than surfacing it, so a package whose tests were cached green stays green until its
digest changes, which can be weeks. That trades signal for speed.

**We are excluding test results from the cache** and caching only compilation output. This gives
up roughly a third of the available time saving. [UNMEASURED] Fixing the flakes is tracked
separately and is a larger piece of work than this one.

## 7. Here is a merge landing on a warm cache

A developer merges a one-line change to `packages/currency-format`, a leaf package with two
dependents. The runner computes digests for all 240 packages and fetches the manifest in one
request. It finds 237 hits and 3 misses: `currency-format` itself and its two dependents. It
downloads 237 objects in parallel across 16 connections, taking 42 seconds, unpacks them,
verifies each digest, and rebuilds only the 3 missing packages, taking 90 seconds. Total wall
clock is 2 minutes 40 seconds against the current 31 minutes. [UNMEASURED, projected from the
per-object timings above]

## 8. Cost lands slightly below the runner time it replaces

**Storage and egress run about $310 a month** at 40 GB of working set, a 14-day lifecycle, and
roughly 2,100 runs a month. [UNMEASURED] **The runner time it replaces is about $380 a month**
at the current merge volume. The margin is thin enough that a 3x growth in run volume makes
this cost-neutral rather than a saving, so the justification is latency and not spend.

## 9. Turning it on for everything at once would hide a correctness bug behind a speedup

**We are enabling it per package behind a flag**, starting with the six slowest, which together
account for 40% of build time. Each package gets a week of shadow mode where the runner builds
from source, fetches the cached object anyway, and compares the two outputs byte for byte. A
mismatch logs and does not fail. [UNMEASURED] Only after a clean week does the package start
serving from cache.

**Rolling back is a flag flip per package** and leaves the objects in place, so re-enabling does
not re-warm from scratch.

## 10. Start here

Read section 1 for the key derivation, then section 4 for the storage layout, then section 9 for
the rollout. Sections 5 and 6 are the ones to push back on. The open questions are whether the
14-day lifecycle is long enough for packages that change monthly, whether we should cache test
results once the flakes are fixed, and who owns the bucket credential rotation after the first
quarter.
