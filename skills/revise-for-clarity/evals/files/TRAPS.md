# Planted traps, per fixture

Written before grading, so a run cannot be graded against a rubric adjusted to fit it.
Every trap here is falsifiable from the fixture's own text — no external knowledge required.

## build-cache-rollout.md — the investigation spine

Baseline profile measured by `structure_report.py`: 1,307 words, H2=10, **H3=0**,
numbered H2=10, slot+claim headings=0/10, bolded lead-ins=21/24 paragraphs, inline tags=16.

Reproduces the profile of the real draft that a reader called "incredibly hard to follow"
while fully complying with every pre-2.7.0 rule. The walkthrough in section 7 is deliberately
*correct* (one real instance, `packages/currency-format`), so this fixture isolates the new
rules from the v2.6.0 walkthrough rules.

| # | Trap | Falsified by |
|---|---|---|
| A1 | Spine is the author's investigation: key derivation, storage, compression, design passes, security, flakes, walkthrough, cost, rollout | Section order tracks what was explored, not what a reader decides |
| A2 | All ten H2s are claims with no slot; a reader cannot locate risks, alternatives, or rollout | Risks live in 5, 6, and 8; alternatives in 2; neither is findable |
| A3 | Zero H3 with 21 bolded lead-ins: hierarchy carried by typography | `structure_report.py` |
| A4 | Sequential numbering disguises ten siblings as organization | `## 1.` through `## 10.` |
| A5 | Analysis narration in a heading: "4. Four more passes through the design" | Counts the author's passes, not what is true |
| A6 | "## 10. Start here" closer, with the open questions buried inside it | Closing section tells the reader where to begin |
| A7 | 16 inline `[VERIFIED]`/`[UNMEASURED]` tags plus a front-matter verification convention | Working state on the page; belongs in an evidence appendix |
| A8 | The draft is already terse, so a 30% cut is the wrong operation | Prose is active, unhedged, one idea per paragraph |

**The discriminating outcome:** a revision that compresses this draft substantially has applied
the most prominent number in the skill and made the document worse. Passing means restructuring
at roughly equal length, or longer.

## outbox-delivery-migration.md — four states, not two

Almost no pointer labels, isolating the temporal rules. Falsifying facts are in appendices
A (flag state), B (call sites), C (measurement provenance), D (dates).

| # | Trap | Falsified by |
|---|---|---|
| B1 | Status says `Implemented (phase 1)`; a whole section is titled "What we will build" | Appendix A: only `outbox_writes` is on |
| B2 | Summary: "removed the duplicate-send class of bug entirely" | Appendix B: `LegacyInvoiceMailer#deliver_now` still sends inline and still carries the risk |
| B3 | Summary credits the design with 240 ms of latency | Appendix C: that is the writes-only delta; no dispatch has run in production |
| B4 | Digest worker described in present tense as today's behavior, with a consequence ("shared rate limiter") drawn from it | Appendix A: digest outbox path sits behind `outbox_dispatch`, off, never run in production |
| B5 | Retry policy and 11-attempt ceiling stated as current behavior | Dispatcher behavior, gated off per Appendix A |
| B6 | Cited proposal: dispatcher behavior in `will` with `app/workers/outbox_dispatcher.rb` attached | The path is real, the behavior is not |
| B7 | "The dispatcher costs 14 writes per batch" as a standing property | Appendix C: one staging run, 2026-07-14 |
| B8 | "Both paths write to the same table" with no phase anchor | Rollout: true in phases 1-2, false after phase 3 |
| B9 | "We should route provider webhooks" — `should` marks no state | Appendix A: `outbox_webhooks` merged, route not mounted |
| B10 | Per-tenant rate limiting: proposed in one sentence, then present tense ("has its rows deferred") | Appendix A: no implementation merged |
| B11 | Risk table mixes risks that exist today with risks the change introduces, unmarked | Row 4 rests on B4, which never runs |
| B12 | "Transactional email used to be synchronous" — undated | Appendix D: written 2019 |
| B13 | The correcting sentence, "the dispatcher is a no-op", sits in the last line of Rollout | It governs how the whole document reads and is placed where readers skim |
| B14 | Summary is past/present while the body proposes: re-tensed only at the top | Skim layer and body disagree about what exists |

**The discriminating outcome:** B4 and B13 together. A revision that keeps the digest worker in
present tense has described flagged-off code as production behavior, which is the failure the
"available, not live" state exists to catch, and it will carry the false rate-limiter risk row
forward with it.
