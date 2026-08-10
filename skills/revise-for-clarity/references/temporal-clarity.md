# Temporal Clarity

Read when the piece describes both how something behaves now and how it would behave after a change: a design doc, RFC, proposal, feature plan, or upgrade plan. Read again once any part of the plan has shipped.

**The failure this prevents:** a reader cannot tell, sentence by sentence, whether a passage describes production or a proposal. A reviewer sizing risk, an implementer picking the piece up six weeks later, and a manager deciding whether the pain is already fixed all read the same sentence and need the same answer from it.

The four states and the `will`/`would` mapping are defined in SKILL.md, Pass 4. This file holds the procedure. Whether a current-state claim is *true* belongs to the claim-verification bullet in Pass 4; this file governs how the piece says which state it is describing.

## Why "available, not live" earns its own state

A flagged-off path is true of the repository and false of what a user experiences. Calling it today's behavior breaks two things at once: the rollback plan, because reverting returns users to a state they have never seen, and the risk list, because a defect described as pre-existing is actually being introduced. Present tense without the gate clause is how that happens, since the sentence is accurate about the code.

- Fails: "the draft engine assigns names on save."
- Passes: "the draft engine assigns names on save, behind a flag that is off in production."

## Past tense: what changed, when, and what it missed

**A past-tense claim is incomplete without the present-tense claim beside it.** "We moved price validation into the model in December 2025" says what happened and nothing about what runs now.

- Fails: "price validation moved into the model in December 2025."
- Passes: "price validation moved into the model in December 2025, and 42 of 43 call sites now use it. The legacy importer still validates in the controller, which is why it accepts prices the model rejects."

**The incomplete migration is the most expensive temporal defect in this genre.** A piece accurate about history and wrong about the present reads as authoritative, and nothing in its structure flags it. State the coverage as a count, name every exception, and say per exception whether it is intentional or residual. A migration you cannot count is a migration you have not verified.

**Date every past-tense claim.** "This used to be synchronous" leaves the reader unable to tell 2019 from last month, and that difference decides whether anyone still remembers why, whether the constraint that forced it still holds, and whether the change is worth mentioning at all. "Recently," "a while ago," and "historically" all fail. Where you cannot date it, say the date is unknown rather than implying recency.

**Past tense is not a way to avoid verifying.** "That was decided earlier," "this was deliberate," and "we already excluded that case" are scoping claims, and past tense makes them feel settled. That a divergence is long-standing and that it was deliberate are both irrelevant to whether the clause names a behavior today.

Three more places past tense is the correct choice:

- **Measurements are events, not properties.** "The importer cost 14 writes when measured on 2026-07-14" is what happened. "The importer costs 14 writes" is a standing claim built on one observation. Put the measurement in the past with its date in the evidence appendix, and the behavior it establishes in the present in the narrative.
- **Approaches already tried are past, not conditional.** `would` marks an option nobody has run. An approach that shipped and was withdrawn takes past tense with its outcome: "a dual-write shim ran for two releases in 2025 and doubled the write cost." That is measured evidence and it outranks a reasoned rejection, so the tense is what tells the reader which one they are reading.
- **Reverted work still exists.** "We shipped the shim in March and reverted it in April" says nothing about whether the code is still in the repository. Say that separately, because dead code is a hazard the next reader inherits.

## Where tense leaks out from under its heading

Four places the leak is routine:

- **The walkthrough.** A trace reads like an observation: "the mutation lands on the direct-save path, which runs model checks and skips the suite." Nothing in it says the skip is what you are proposing. Where the walkthrough narrates proposed behavior, its first sentence says so.
- **The risk list.** Rows mix risks that exist today with risks the change introduces. A reader cannot mitigate what they cannot place. State per row which it is, or split the list.
- **Gotchas.** The same mix at higher cost: an implementer reads a trap the change creates as a trap already in the code, and designs around a problem that does not exist yet.
- **Background, after two edits.** Proposal sentences migrate into the current-state section during editing, because the locally easiest place to add "and we will move this to the new path" is next to the sentence about the old path.

## Evidence attaches to today, never to a proposal

A proposed behavior has nothing to ground, so a citation next to it tells the reader that behavior already exists.

- Passes: "the direct-save path runs model checks only (`app/resolvers/save_direct.rb`), so the suite never fires on it."
- Fails: "the direct-save path will run the full suite (`app/resolvers/save_direct.rb`)."

The second sentence's path is real and its behavior is not, and the pairing is what makes it read as verified. When proposing a change to a file, cite it by naming the change: "the suite call is added to the direct-save path, which today runs model checks only." One citation, one state, one claim.

## Phase-relative claims name their phase

In a phased plan, many statements are true only inside a window. "Both paths write to the same table" holds during phase 2 and is false after phase 3. Unanchored, a reader takes it as the end state, and an implementer builds on a transitional invariant.

- Every claim whose truth ends at a phase boundary names the phase: "through phase 2, both paths write to the same table."
- The end state is stated once, in its own sentence, so the destination is distinguishable from the transitional shape.

## Tense tracks reality, not the draft

Pieces rot temporally as they succeed. Phase 1 ships and the sentences describing it still say `will`, so a piece that now documents production reads as a proposal. Half-shipped is the worst case: the body carries both states with nothing distinguishing them.

On any edit, and always when a status field changes:

- **Re-tense what shipped.** Sentences describing shipped behavior move to present tense in the same edit that records the shipping. This is a rewrite of those sentences, not a note appended near them.
- **Status and body tense agree.** A piece marked Implemented whose body proposes, or marked Draft whose body describes, is one failure with two symptoms. The status field is the cheapest check available.
- **Re-tensing is not growth.** Converting `will` to present tense costs no words and buys the largest correctness gain per word available in an edited piece, so it needs no exemption from the subtraction invariant.
- **Frozen pieces do not re-tense.** An accepted ADR's Decision stays in the tense it was accepted in, and a postmortem's remediation list states per item whether the work has shipped, with a date.

## The tense audit

Run this at Pass 4 and again on every edit. It produces the first three numbers in the final checklist.

1. **Mark every sentence that asserts behavior** with `W` (was), `T` (today), `A` (available, not live), or `P` (proposed). Read each sentence alone, without the heading above it and without the sentence before it. A sentence you cannot mark from itself is the finding, and the fix is rewriting that sentence rather than adding a marker sentence near it.
2. **Split every paragraph carrying more than one mark**, unless it contains an explicit contrast ("today X; after this change Y"). Mixed marks inside one paragraph are how a reader loses the thread mid-passage.
3. **Check every `W` for its date and its pair.** A past-tense claim with no date, or with no present-tense claim beside it stating what runs now, is unfinished. Where the change was a migration, the pair carries a count and names every exception.
4. **Grep the current-state and background sections** for `will`, `we plan`, `once we`, `going to`, and `should`. Every hit is a proposal that leaked into a description of today, or a `should` that names no state.
5. **Grep the design and rollout sections** for `currently`, `today`, `at present`, and `already`. Each hit is either a deliberate contrast, which is good, or a current-state claim stranded where readers expect proposals.
6. **Write three counts:** sentences you could not mark, future markers sitting in current-state sections, and undated or unpaired past-tense claims. All three go to zero before delivering.

## Anti-patterns

- **The present-tense proposal.** A design section in present indicative throughout, so it reads as documentation of a running system. The most common form and the hardest to see, because the prose is otherwise excellent.
- **Flagged-off code called today's behavior.** True of the repository, false of production, and it corrupts the rollback plan and the risk list together.
- **Tense by heading.** Relying on `## Current state` and `## Proposed design` to carry state, so every sentence quoted, skimmed, or moved loses it. These get read by search, not top to bottom.
- **`should` as a state marker.** "The resolver should skip the suite" reads as proposal, requirement, or guess. Three readings, no way to pick.
- **The cited proposal.** A file path attached to behavior that does not exist yet, which makes the proposal read as a verified finding.
- **The unanchored transitional claim.** A dual-write or compatibility shape stated as though permanent, so a later reader builds on an invariant the plan retires.
- **Shipped and still proposing.** A status of Implemented over a body full of `will`.
- **The migration described as done.** Accurate about history, wrong about the present, and invisible, because a reader has no reason to ask whether the change covered everything.
- **Undated past tense.** "This used to be synchronous." Last month and 2019 imply different things about whether the forcing constraint still holds.
- **Past tense as settlement.** "That was decided earlier" standing in for a check.
- **The measurement promoted to a property.** One run reported in the present tense, so a number true on one day reads as a standing characteristic.
- **Re-tensing only the summary.** Updating the opening when a phase ships while the body sections stay in the future, so the skim layer and the body disagree about what exists.
