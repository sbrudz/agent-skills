# Move reindexing off the write path before adding faceted search, not through it

**Written:** 2026-07-14 · **Status:** proposal · **Author:** A. Rivera

The catalog service reindexes synchronously on every write, which costs 40–90ms per save. Faceted
search doubles the index payload, so the current plan lands both changes in one release. Can facets
ship without the queue work? Yes — split the work into four tracks, ship facets against the indexer
that exists today, and let the queue ship separately as the write-latency fix it always was.

**Scope: sequencing only.** Track A's schema and query design live in
[`../search/2026-07-10-facet-design-v3.md`](../search/2026-07-10-facet-design-v3.md). Where the two
disagree, the design doc wins.

---

## 1. Decisions 3 and 7 pull in opposite directions

Decision 3 sequences the queue migration before facets, on the rationale that *"a facet rollback
should never strand half-written index documents."* Decision 7 then makes the facet rollout itself the
thing that expands those documents. Under the combined plan, rolling back facets leaves the cluster
holding expanded documents no query path reads: the exact strand decision 3 exists to prevent, moved
one milestone later.

Two further costs no prior document prices:

- **The v2 RFC's open question 4 measures index lag per write.** Facets change the denominator — each
  save now ships six analyzer passes instead of two, and a single tag edit measured 31 field updates
  against 5. The gate under-measures its own subject.
- **One service would get two indexing models.** Milestone 2 already carves out bulk imports;
  document-versus-document inside one service is a worse seam than the one it replaces.

**What is reopened is the ordering, not the destination.** The queue stays the target end state. Dana
confirmed on 2026-07-11 that she will forego it if that buys a shippable V1, so Track A assumes
synchronous writes.

---

## 2. A facet query is a whole-index intersection, which only the current analyzer can express

Consider a buyer filtering a 400-item catalog by colour *and* size at once. The analyzer takes the
whole filter set, intersects the posting lists in one pass, and returns counts per remaining value —
so the sidebar shows "Blue (12)" without a second round trip. The queue-backed indexer cannot express
that: it writes per-field documents and merges them on read, which computes counts against a partial
view and drifts whenever a merge lags. **The UI's natural unit of work is a whole-index intersection,
and only one of the two indexers has one.**

That is the whole argument for the split. Working backwards from the rest of the mockup reinforces it:
keyword search, sort, and pagination all already exist, and the range filter is the machinery a
server-rendered facet sidebar needs. Genuinely new: count rollups, the empty-facet suppression rule,
and `Hide facet`, the only new domain concept in the mockup.

---

## 3. Four tracks ship independently; only Track A is on the critical path

| Track | Scope | Depends on | Ships |
|---|---|---|---|
| **A** | Faceted search V1: synchronous indexing, server-rendered sidebar, stale-document dialog | nothing queue-side | the buyer-visible feature |
| **B** | Async reindex queue + dual-path harness | nothing | fixes write latency |
| **C** | Milestone 2: bulk import reads the queue | B | imports stop blocking saves |
| **D** | Facet hide / soft delete | A | opt a value out without deleting it |

**Track B is not saved by decoupling — it is freed.** Decision 9 requires the queue for the bulk
importer regardless of where facets land, and v2's own 2026-07-09 amendment says so. So it ships
against the justification that actually holds: 40–90ms added to every save on 180,000 active catalogs,
plus SEARCH-412's estimated 900–2,100 catalogs currently timing out on import.

**Track D is deferred deliberately.** It is the only new column, and it leaks into the sitemap,
the storefront sidebar, two API serializer generations, and the canonical-URL rule. The cost is real
and needs sign-off: per-value exclusion exists today, but **exclusions are not stable** — the next
full reindex regenerates the excluded value.

### Why not build the queue first?

**Building Track B first** was rejected by the council 5–0. The premise it would serve is already
true: the current analyzer computes counts correctly, so facets do not need the queue. Ordering B
first buys 60–100 hours to arrive at the same sidebar.

### The honest cost of deferring: double integration

Both indexing RFCs raise it, and it is the strongest objection here. Track A's query surface is
replaced when Track C converts reads to the queue — eight query endpoints, each needing a new
response shape. Both RFCs price that "Convert" phase at 20–30 hours, against 60–100 hours of queue
work. The trade holds; see the design doc's risk 2 for the corrected accounting.

**Also honest:** the current path is not clean. The council found four liabilities on it, including an
analyzer collision that silently drops counts. The design doc's §4.1 lists them.

---

## 4. Stale documents block the facet sidebar rather than waiting for Track C

**Decided 2026-07-11: this cannot wait for Track C.** A catalog with documents older than its last
write must show a notice and fall back to keyword search until a reindex completes.

**Falling back is cheaper than Track C, not a slice of it.** Track A never needs the merge-on-read
mechanic, and it removes that mechanic's partial-count hazard. Roughly 6–9% of catalogs carry stale
documents at any moment — on the order of 12,000, the same order as SEARCH-412's timeout count.

---

## 5. Track A can start once Dana and Priya settle three questions

| Question | Owner |
|---|---|
| Is the V1 unstable-exclusion limitation acceptable while Track D is deferred? (§3) | Dana, Priya |
| Count rounding above 1,000; is the sidebar order configurable? | Priya |
| Which of the two indexing RFCs is live? Track C inherits this; Track A does not. | eng lead |

Write the analyzer-collision spec first. It settles the highest-severity open question on the path
Track A depends on. Four production measurements are still outstanding; the design doc's §13 lists
them.
