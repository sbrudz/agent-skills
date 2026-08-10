---
name: revise-for-clarity
description: Revise existing prose to be shorter and clearer: a design doc, RFC, ADR, proposal, PR or ticket description, status update, email, or any passage carrying an argument. Use ONLY on text that already exists, and ONLY when the user explicitly invokes this skill. Triggers on "revise this for clarity", "make this shorter and clearer", "tighten this up", "edit this down", "this is dense and hard to follow". Never invoke it automatically while drafting, and never use it to write something new from notes: it requires a file, a section, or a pasted passage as input.
---

# Revise for Clarity

## Overview

Writing succeeds when the reader takes away the key insight, the reasoning, and how the evidence supports it. It does not succeed by recording every fact. Good writing communicates more by saying less.

**Core principle: revise by subtraction and restructuring, never by addition.** Structural framing (BLUF sentences, level-of-detail signals, SCQA openings) replaces existing content instead of adding to it. If you added a framing sentence and cut nothing, the piece got worse.

## What This Needs

**Input:** text that already exists — a file path, a named section, or a pasted passage. **Output:** the revised text, plus the numbers from the final checklist.

**HALT — no draft supplied.** If the request names no file and pastes no text, stop and ask which text to revise. Never draft something new in order to revise it. Gathering information, analyzing tradeoffs, and deciding what to say all precede this skill.

**Do not use for:** reference documentation, where completeness outranks persuasion; templates and formatting; or a piece whose facts are still unsettled.

## Before Pass 1 — Choose the Spine

**The passes improve a structure. Not one of them chooses it.** Each is a relative operator: hand it any organization and it makes that organization better. Run all four at full compliance over a piece organized around the author's investigation — one section per area explored, in the order explored — and you get a well-written investigation report that is still hard to follow, because the reader is navigating someone else's research process instead of their own decision. This is the one place full compliance and understandability come apart, and compressing such a draft makes it worse.

So first name what the reader has to decide, then pick the spine serving that decision:

- **If the genre has settled sections** — an RFC's Context, Proposal, Alternatives, Risks, Rollout, Open questions; a postmortem's Timeline and Impact — adopt them wholesale and run the passes inside them. Do not invent a structure where one is conventional.
- **If it does not** (a message, an update, an email), the spine is the reader's question, and the answer goes first.

Two tells that a draft follows the investigation rather than the decision: numbering three levels deep, and a section describing what changed since the last draft.

## The Four Passes

Work in passes. Each has one lens. Do not try to do everything at once.

### Pass 1 — Structure: Build the Pyramid

**Goal:** A reader skimming only headings and first sentences gets the whole argument.

- **BLUF (Bottom Line Up Front):** Every section opens with its conclusion. Never lead with background or preamble.
- **SCQA opening:** The first paragraph runs Situation → Complication → Question → Answer, in at most 4 sentences. *"We serve 10k requests/min (S). Traffic doubles every quarter and the architecture stops at 50k (C). How do we reach 200k without a rewrite in six months? (Q) Shard by tenant and add a read-replica layer (A)."*
- **Governing ideas:** One per section. Two means split the section.
- **Headings carry a slot and a claim.** Where the genre has conventional sections, name the slot, then state that section's conclusion after a colon: "Risks: renaming a choice destroys a sibling's variants today, and no constraint catches it." The slot is how a reader navigates; the claim is how the skim layer carries the argument. Where there is no conventional structure, the claim alone is right. A bare slot with no claim is the failure this rule exists to prevent. **All claims and no slots is the opposite failure, and it is worse:** the reader cannot predict where anything lives, so they read linearly to find the one section they came for. A claim resting on a pointer is a slot label in disguise: "Decisions 5 and 6 pull in opposite directions" is grammatically a claim and gives the reader nothing to evaluate.
- **The 3-5 rule:** No level has more than 5 sibling sections. More means grouping them under a higher-level governing idea. **Numbering is not grouping** — `## 1.` through `## 10.` looks organized and is still ten siblings. **A genre's settled slot set is exempt,** because the reader navigates by it: an RFC's six or seven conventional sections plus its appendices stay flat at the top level, and you group inside them.
- **Concrete walkthrough (non-negotiable):** Walk one concrete scenario through the system before generalizing. A design doc with zero concrete examples is incomplete. Place it early, after the SCQA opening or at the start of the design section. "Here is a request during dual-write. It lands on the old database first..." Three rules govern how it is built:
  - **One real instance, never a union of categories.** Rebuild it from scratch rather than editing the draft's example sentence: a composite survives light editing, because every clause in it is individually true. **A generic subject is the tell.** If it opens on "a file," "a user," or "a product," you have not named an instance yet. Name the type first ("a budget spreadsheet," not "a file"), then run the property test: for each property the walkthrough attributes to it, ask whether that one type actually has it. A spreadsheet has no transcoded preview; a t-shirt has no download link. Every "no" moves out to its own two-sentence case — same operation, different kind of thing, one consequence each — and you close by stating the coverage: "no single file carries all three; every file carries a row." A reader who spots the contradiction stops trusting the rest.
  - **The walkthrough's spine is whatever the piece is arguing.** If it exists to show that two paths behave differently, its first two sentences state both. Narrating one path in full and disposing of the other in a closing line ("the web app does none of this") puts the actual subject where readers skim. Test: delete the last paragraph. If the subject was in it, restructure the walkthrough rather than expanding that line.
  - **Give it the budget the argument needs.** Three to five sentences is the floor, not a ceiling. When the walkthrough *is* the evidence for the central claim, no other section should be longer, and you pay for it by cutting elsewhere. **Exempt from cuts is not exempt from rewriting:** this protects the walkthrough's word budget, never its existing sentences. Carrying a bad example forward because it is "the load-bearing example" is the most common misreading. Rebuild it, then fund it out of other sections, so the piece lands at or below its previous length even when the walkthrough triples.

**Check:** Can a busy reader get the argument from headings plus first sentences alone?

### Pass 2 — Hierarchy: Set Levels of Detail

**Goal:** The reader always knows what level of detail they are at and why.

- **Signal the level near the top of each section:** "This section stays at the level of deployable units and how they communicate."
- **One level per section.** Do not mix system-wide description with component internals in the same paragraph.
- **Nest details under their claim.** Implementation details, edge cases, and alternatives live in subsections or bullets under the governing idea they support.
- **MECE sections:** same-level sections do not overlap and leave no gaps.
- **Hierarchy needs structure, not typography.** Bold has one level, so a section of ten paragraphs each opening with a bolded lead-in is a flat list wearing an argument's clothes, and the reader gets no signal about which paragraph is load-bearing. That is BLUF applied at the wrong granularity: promote the real divisions to subheadings and let most paragraphs start unbolded.

**Check:** Pick a random paragraph. Can you name its level of detail? Should it be at a different one?

### Pass 3 — Clarity: Make Every Sentence Earn Its Place

**Goal:** The reader never has to re-read a sentence to understand it.

- **Given-before-new:** Each sentence opens with what the reader already knows and puts the new information at the end, so the new becomes given for the next sentence.
- **Active voice:** "Component A calls Component B," not "Component B is called by Component A."
- **One idea per paragraph.** Topic sentence first, support after. A second point means a new paragraph.
- **Concrete before abstract.** Anchor every abstraction with an instance before generalizing.
- **Cut clutter, keep bounds.** Hedging ("it should be noted that," "generally," "in most cases"), redundant pairs ("full and complete"), and intensifiers ("very," "really," "basically") all go. A bound is different: deleting it changes what the sentence claims, so it stays. "Where a combination survives the edit, keep its row" describes what the code already does, while the crisper "preserve the row through structural edits" promises a capability that does not exist. Before cutting a qualifier, check whether the sentence is still true without it; if it is not, the tighter version is a false claim. **Modal verbs marking state are bounds.** Cutting `would` from "the shim would double-write for one release" produces a sentence asserting that it double-writes today: crisper and false. `will`, `would`, and `does` are exempt from this cut. `should` is not, because it marks no state at all — pick one of the three.
- **Cut 30% of word count.** This is the target for a bloated first draft, not a standing objective. **Cutting is for prose that repeats, hedges, or narrates. It does not fix bad structure and cannot compensate for the absence of one.** A draft on the wrong spine gets worse as it compresses, because compression strips the redundancy that was helping the reader recover. If a draft is hard to follow and you cannot find 30% to cut, re-run Pass 1 before cutting anything: the problem is the spine, not the word count. The subtraction invariant under Revise is a separate rule governing an already-structured piece, where the bar is parity rather than a percentage.

**Check:** Read a paragraph aloud. Does it flow? If it sounds like a textbook, rewrite it.

### Pass 4 — Reader Calibration: Kill the Curse of Knowledge

**Goal:** Someone reading cold follows the argument and understands why the decisions were made, without opening anything else.

- **State the reader's knowledge before this pass:** "The reader knows X and Y. The reader does NOT know A or B." Then read the piece as that reader.
- **Every decision has a why and a why-not.** "We chose Postgres because... We rejected Mongo because..." A decision without rejected alternatives is a fact, not an argument.
- **Define before use, then replace every load-bearing pointer with its claim.** Jargon, acronyms, and system names get defined on first use, and so do the labels standing in for ideas: decision numbers, document names, milestone and track names, ticket ids, review bodies, and people's names (give the role). A label is a lookup key you hold and the reader does not. Sort each into two kinds. *Navigational* pointers send the reader away for detail they do not need here ("the sizing lives in the design doc") and are fine. *Load-bearing* pointers are links in the argument: if the reader cannot resolve one, the reasoning breaks. Rewrite the sentence around the substance and delete the label. If the substance will not fit in a clause, either it belongs in this piece or the argument resting on it does not.
- **The deletion test — the only way to pass the rule above.** Delete the label from your rewritten sentence. If it still reads and still makes its point, the substance is in the prose. If deleting it breaks the sentence, you appended a gloss instead of replacing the pointer, and the reader still holds a lookup key. These fail: "Decision 12 (Redis evicts under memory pressure) blocks this" and "the concerns in Decision 12, which are about Redis eviction." This passes: "Redis evicts keys under memory pressure and silently logs users out, which is why the admin console stayed on the database." **A person's name is a pointer too, and the easiest to leave bare:** "Wei flagged this in review" says nothing about why the flag carries weight, while "the engineer who owns the attribution model flagged this" does, and survives deleting the name. **Resolving pointers must not grow the piece** — annotating adds words and leaves the labels standing, while replacing spends those words on substance and pays for them out of the prose the labels stood in for.
- **Say which state every claim describes.** The reader must be able to tell, sentence by sentence, whether a passage describes what runs now or what you are proposing. Every downstream judgment depends on it, and there are four states, not two:

  | State | Covers | Reads as |
  |---|---|---|
  | **Was** | behavior that no longer runs anywhere | past tense, dated, and never alone: paired with what runs now instead |
  | **Today** | what production does right now | present tense |
  | **Available, not live** | code that exists and no user reaches: behind an off flag, merged and undeployed, unmerged | present tense plus its gate, in the same sentence |
  | **Proposed** | what this piece asks for | `will` for the recommendation, `would` for alternatives and hypotheticals |

  A section mixing `will` and `would` for the same mechanism has not decided what it recommends. **The heading does not carry tense** — `## Current state` and `## Proposed design` leak, because every sentence asserting behavior gets quoted, skimmed, or moved out from under its heading. The walkthrough, the risk list, and the background section are where that leak is routine. Full procedure, the six-step tense audit, and the anti-pattern list: `references/temporal-clarity.md`.
- **Verify the claims the argument rests on, and distrust the tidy ones.** Some sentences scope the argument: "that case is already excluded," "only three remain," "the objection and the remaining scope land on exactly the same edits." Everything downstream depends on them, so check each against the source, not against your memory of it. Symmetry is the signal to check hardest: the compression target and the claim-heading rule both reward a confident assertion over an accurate qualified one, so an argument resolving into a neat coincidence is as likely to mean you wrote past a gap as found one. **"Already excluded," "already handled," and "out of scope per X" are the highest-risk form** — quote X and check that it says what you need. **Apply it as a binary test: write down, in one sentence, the single behavior the clause preserves.** If you cannot do that without picking between two options, the clause names no behavior, is not an exemption, and whatever it appeared to exclude is still in scope. That the divergence is long-standing, deliberate, or covered by a passing test is irrelevant here: those facts explain why it exists, and a divergence the clause cannot choose between is what voids it. Do not substitute the easier question "is this gap in scope?" Where you cannot tell which reading was intended, say so as an open question and state what the answer decides. When one turns out wrong, delete the conclusion it supported rather than footnoting it, and follow the correction through the scope list, the alternatives, and the risks. **Bound the underlying fact instead of deleting it.** "Checkout got 240 ms faster the week writes went on" keeps what was measured; cutting the number throws away a true finding along with the false claim built on it. A correction parked in an appendix has not been applied, and a rhetorical high point resting on a false premise is the most expensive sentence in the piece.
- **The "so what" test:** for each paragraph, "why should the reader care?" No answer means cut it.
- **One path through.** A reader goes start to finish without jumping around. Forward references signal structural problems.

**Check:** Would someone who joined the team yesterday follow this? Someone on another team?

## Revise → Apply Targeted Passes

When incorporating feedback after sharing the piece:

- **Restructure, do not append.** New information replaces or reshapes existing sections. It does not get tacked onto the end.
- **After every change, re-run the pass that governs what changed.** New rationale means Pass 4. New section means Passes 1 and 2. Rewritten paragraph means Pass 3.
- **Growth is legitimate only when you can name what it bought** — which case, which risk, which open question. "The argument needed it" with nothing named is how bloat gets waved through. **Naming the purchase licenses the words, not the growth:** even a justified new case gets paid for out of the existing prose, and a revision ending more than 5% longer than the draft it replaces has stopped cutting, however well it accounts for what it added. **That 5% detects failure and is not an allowance to spend.** A revision landing just under it read a limit as a budget and stopped Pass 3 early; the target is parity or shorter. **Correct first, then cut** — never hold a word count by leaving a false argument standing.
- **Reset the baseline when the conclusion is re-derived rather than patched.** If review invalidates a load-bearing claim and the recommendation has to be rebuilt instead of amended, the prior draft is no longer the thing you are revising, so measuring against it means nothing. Say the baseline reset, name the new one, and apply the invariant from there. This is the only exemption, and re-deriving a conclusion you merely dislike does not qualify.
- **Never narrate your own process inside the piece — the revision process or the analysis process.** Diffs, concessions, "as noted in v2," and what changed since the last draft go in your message to the reviewer, because the piece is read cold by people who never saw the earlier version. The subtler form: headings counting your passes through the problem, closing sections telling the reader where to start, and per-claim verification tags inline in the prose. Verification status belongs in an evidence appendix, one entry per claim, so the reader meets the prose and the proof separately. Moving all of that out is usually the first 100 words of the cut that funds legitimate growth.

## Polish → Pass 3 Only

Final line-level pass: given-new chains, active voice, clutter cuts. No structural changes. Read the whole thing aloud.

## Quick Reference

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| "Wall of text" | No pyramid, no hierarchy | Pass 1: BLUF, governing ideas |
| "It's short and still hard to follow" | Wrong spine; compression stripped the recovery cues | Choose the spine, then re-run the passes inside it |
| "I can't find where the risks are" | Headings are all claims with the slots stripped out | Pass 1: slot first, claim after the colon |
| "Can't tell what's important," or every paragraph is bolded | No levels of detail; hierarchy carried by typography | Pass 2: signal the level, promote real divisions to subheadings |
| "Sentences are hard to parse" | Given-new violated, passive voice | Pass 3: reorder, active voice |
| "Too long, nothing to cut" | Curse of Knowledge | Pass 3: cut 30%. If the spine is wrong, Pass 1 first |
| "That example couldn't exist" | Walkthrough built as a union of categories | Pass 1: one instance; each other category its own short case |
| "The walkthrough buries the point" | The comparison the piece is about arrives last | Pass 1: put the contested behavior in the first two sentences |
| "Is this shipped or proposed?" | State unmarked, or carried by the heading | Pass 4: mark every behavioral sentence was/today/available/proposed |
| "This claim is doing a lot of work" | Scoping claim asserted from memory, not checked | Pass 4: verify against the source; delete what rested on it |
| "I'd need three other docs open" | Labels standing in for ideas the reader lacks | Pass 4: replace each load-bearing pointer with its claim |

## Common Mistakes

- **Improving a structure instead of choosing one.** Every pass here is a relative operator. A piece organized around the author's investigation passes all four checks, stays unreadable, and gets worse as it compresses.
- **Rewriting conventional slot names into pure claims.** "Risks" and "Alternatives considered" are the handles a reader navigates by. Stripping them to satisfy the claim rule leaves nothing to navigate.
- **Leading with context instead of the conclusion.** The reader needs to know where you are going before they care how you got there.
- **Writing for your current self instead of a future stranger.** The person joining in six months has zero context.
- **Defending instead of arguing.** Listing reasons your approach is right, without the alternatives you rejected. The latter persuades more.
- **Trading a true bounded claim for a crisp false one.** The 30% target and the claim-heading rule both reward assertion. Neither licenses promising a capability that does not exist, asserting a scope you did not check, or dropping the modal that marked something as proposed.
- **Naming an idea instead of stating it.** "Decision 5 and decision 6 conflict" reads as an argument to the author and as a lookup task to everyone else. Cutting word count by turning claims into labels makes a piece shorter and less understandable at once.

## Red Flags — Stop and Rewrite

- The piece got longer after a revision pass
- You cannot state the single key insight in one sentence
- Headings are bare topic labels with no claim attached — **or**, in a genre with conventional sections, claims with the slot name stripped out, leaving the reader nothing to navigate by
- Every paragraph in a section opens with a bolded lead-in and the section has no subsections
- A section has more than 5 immediate subsections, sequential numbering included and a genre's conventional slot set excepted
- A paragraph takes more than 4 sentences to make its point
- A sentence asserting system behavior that you cannot place in one of the four states by reading it alone
- "The reader will figure it out" — you have Curse of Knowledge
- You cannot find a single concrete walkthrough anywhere
- Elegance treated as evidence: the neater the convergence, the likelier you wrote past a gap

**Any of these: identify which pass was skipped, redo that pass.**

## Before Declaring a Revision Done

Run all seven. Each is an action producing something you write down, not a question you answer yes to. A revision that satisfies these from memory has not done them, and stopping because the changes so far hang together is the failure this list exists to catch.

1. **Name the spine in one sentence** — the decision the reader is making, and the sections in the order that serves it. If that order matches the order you investigated in, reorder before doing anything else.
2. **Name the walkthrough's instance in one noun phrase** ("a budget spreadsheet," not "a file"). Then list every property the walkthrough attributes to it and mark each one that instance does not have. A non-empty mark list means Pass 1 is unfinished: move those properties out to their own cases.
3. **Quote the walkthrough's first two sentences.** If the piece contrasts two behaviors and both do not appear in what you just quoted, restructure the walkthrough.
4. **Write the word count of every section.** If the walkthrough carries the central claim and any section is longer, cut that section.
5. **List every sentence that scopes the argument** — "already excluded," "already handled," "only N remain," "covers exactly the same." For each, quote the text it rests on and write the single rule or behavior that text names. Any one you cannot write down is a correction to make, and the correction runs through the scope list, the alternatives, and the risks.
6. **List every label and cross-reference** — decision numbers, document names, milestone and track names, ticket ids, review bodies, people's names — and mark each navigational or load-bearing. Replace each load-bearing one with its substance, then re-read that sentence with the label deleted. A piece that needs three other documents open is not finished, however short and well-structured it is.
7. **Write three numbers, then four.** From the tense audit in `references/temporal-clarity.md`: sentences you could not place in a state, future markers sitting in current-state sections, and undated or unpaired past-tense claims. All three go to zero. Then: words before and after, surviving labels before and after. Both must fall. Words down with labels flat means you compressed claims into shorthand; labels down with words up means you glossed instead of replacing. If words rose, name what the growth bought, then cut to parity.
