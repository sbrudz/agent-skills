---
name: writing-clear-tech-docs
description: Use when creating, revising, or refining software design documents, RFCs, architecture decision records, or other technical prose intended to be read and understood by fellow engineers. Also use when a technical document is accurate but dense, hard to follow, buries key insights in detail, reads like a list of facts rather than an argument, refers to ideas by label (decision numbers, doc names, ticket ids) instead of stating them, illustrates itself with an example no single real instance could match, or got longer after a revision pass.
---

# Writing Technical Documents

## Overview

A technical document succeeds when a reader understands the key insight, the reasoning, and how evidence supports it — not when every fact is recorded. Good technical writing communicates more by saying less.

**Core principle: Revise by subtraction and restructuring, never by addition.** If a revision made the document longer, it almost certainly made it worse. **Structural framing (BLUF sentences, zoom signals, SCQA openings) must replace existing content, not add to it. The total must shrink.** If you added a zoom-signal sentence but didn't cut a redundant one elsewhere, the document got worse.

## When to Use

- Creating a first draft from analysis notes
- Self-editing before sharing with reviewers
- Incorporating feedback without bloating the document
- A document is factually correct but readers find it dense or hard to follow
- The key insight is buried; everything reads as equally important

**Do NOT use for:** information gathering, tradeoff analysis (precedes writing), API reference docs (completeness over persuasion), templates or formatting (handled separately).

## The Layered Writing Process

Write in passes. Each pass has one lens. Do not try to do everything at once.

### Draft → Pass 1: Structure (Build the Pyramid)

**Goal:** A reader skimming only headings and first sentences understands the full argument.

- **BLUF (Bottom Line Up Front):** Every section opens with its conclusion. Never lead with background or preamble.
- **SCQA opening:** The document's first paragraph: Situation → Complication → Question → Answer. Max 4 sentences. Example: *"We serve 10k requests/min (S). Traffic is doubling every quarter; the current architecture won't scale past 50k (C). How do we handle 200k+ without rewriting 6 months from now? (Q) We will shard by tenant and add a read-replica layer (A)."*
- **Governing ideas:** Each section has exactly one. Need two? Split the section.
- **Headings as claims, not topic labels:** "We will use Postgres, not Mongo" not "Database Choice." A claim built on a pointer is a topic label in disguise: "Decisions 5 and 6 pull in opposite directions" is grammatically a claim but gives the reader nothing to evaluate. State the substance instead: "Making the variants editor create drafts recreates the tangle we sequenced to avoid."
- **The 3-5 rule:** No level has more than 5 sibling sections. More? Group under a higher-level governing idea.
- **Concrete walkthrough (non-negotiable):** Walk one concrete scenario through the system before generalizing. This is not optional — a design doc with zero concrete examples is incomplete. Place it early, typically after the SCQA opening or at the start of the architecture section. "Here is a request during dual-write. The write lands on the old database first..." Three rules govern how it is built:
  - **One real instance, never a union of categories.** Rewrite the walkthrough from scratch instead of editing the draft's example sentence — a composite survives light editing, because every clause in it is individually true. **A generic subject is the tell:** if the walkthrough opens on "a file," "a user," "a product," or "an item," you have not named an instance yet. Name the type in the first sentence ("a budget spreadsheet," not "a file"), then run the property test: take each property the walkthrough attributes to it and ask whether that one type actually has it. A spreadsheet has no transcoded preview; a t-shirt has no digital download link; a plain physical product has no print-on-demand variant id. Every "no" moves out to its own two-sentence case: same operation, different kind of thing, one consequence each. Close by stating the coverage — "no single file carries all three; every file carries a row." An example that fails this test reads as confusing rather than concrete, and a reader who spots the contradiction stops trusting the rest.
  - **The walkthrough's spine is whatever the document is arguing.** If the document exists to show that two paths behave differently, the walkthrough's first two sentences state both. Narrating one path in full and disposing of the other in a closing line — "the web app does none of this," "the other client is unaffected" — is the failure, not the fix: it puts the document's actual subject in the position readers skim. Test: delete the walkthrough's last paragraph. If the subject was in it, you built the walkthrough backwards and the fix is to restructure it, not to expand that last line.
  - **Give it the budget the argument needs.** Three to five sentences is the floor for an illustration, not a ceiling. When the walkthrough *is* the evidence for the central claim, no other section in the document should be longer, and you pay for it by cutting elsewhere. A one-paragraph gesture at a walkthrough that carries the argument is a skipped pass, not a tight one. **Exempt from cuts is not exempt from rewriting.** This rule protects the walkthrough's word budget, never its existing sentences; carrying a bad example forward untouched because it is "the load-bearing example" is the most common way this rule gets misread. Rebuild it, then give the rebuilt version the budget. **Pay for it inside the same revision.** The walkthrough's new words come out of other sections, not out of the total. A revision that doubles the walkthrough and still ends longer overall has stopped doing Pass 3 partway; the document should land at or below its previous length even when the walkthrough triples.

**Check:** Can a busy reader get the argument from headings + first sentences alone?

### Draft → Pass 2: Hierarchy (Set Zoom Levels)

**Goal:** The reader always knows what abstraction level they're at and why they're there.

- **Signal zoom explicitly near the top of each section:** "This section describes the system at the container level — deployable units and their communication."
- **One zoom level per section:** Don't mix system-context description with component internals in the same paragraph.
- **Nest details under their claim:** Implementation details, edge cases, and alternatives live in subsections or bullet lists under the governing idea they support.
- **MECE sections:** Same-level sections are mutually exclusive (no overlap) and collectively exhaustive (no gaps).

**Check:** Pick a random paragraph. Can you identify its zoom level? Should it be at a different level?

### Refine → Pass 3: Clarity (Make Every Sentence Earn Its Place)

**Goal:** A reader never has to re-read a sentence to understand it.

- **Given-before-new:** Each sentence begins with information the reader already knows, then introduces new information at the end. This creates a chain: the new becomes given for the next sentence.
- **Cut clutter:** Delete hedging ("it should be noted that," "generally," "in most cases"), redundant pairs ("full and complete"), and meaningless intensifiers ("very," "really," "basically").
- **Cut hedges, keep bounds.** A hedge softens a claim without changing what it says ("it should be noted that," "generally") and goes. A bound changes what the sentence claims and stays: "where a combination survives the edit, keep its row" describes something the code already does, while the crisper "preserve the row through structural edits" promises soft delete, which does not exist. Before deleting a qualifier, check whether the sentence is still true without it. If it is not, the qualifier was load-bearing and the tighter version is a false claim. Say so in the document when a bound is doing this work, so a later editor does not cut it as clutter.
- **Active voice:** "Component A calls Component B" not "Component B is called by Component A."
- **One idea per paragraph:** Topic sentence first, supporting details follow. Second point? New paragraph.
- **Concrete before abstract:** Anchor every abstract concept with a concrete example before generalizing. "Consider a user uploading a profile photo. The image pipeline..." then explain the general case.
- **Cut 30% of word count:** Target for every revision pass. Structural framing (zoom signals, BLUF sentences, headings) must be paid for by cutting existing prose — not added on top. If you can't find cuts, you have Curse of Knowledge.

**Check:** Read a paragraph aloud. Natural flow? If it sounds like a textbook, rewrite.

### Refine → Pass 4: Reader Calibration (Kill the Curse of Knowledge)

**Goal:** Someone reading cold follows the argument and understands why decisions were made, without opening another document.

- **State the reader's knowledge explicitly before this pass:** "The reader knows X, Y. The reader does NOT know A, B." Read the document as that reader.
- **Every decision has a "why" and a "why not":** "We chose Postgres because... We rejected Mongo because..." A decision without rejected alternatives is a fact, not an argument.
- **Define before use — terms and labels both:** Jargon, acronyms, and system names get defined on first use. So do labels that stand in for ideas: decision numbers ("Decision 5"), document names ("the v4 RFC"), milestone and track names, ticket ids ("GAL-1891"), review bodies ("the council"), artifacts ("the prototype"), and people's names (give the role). A label is a lookup key you hold and the reader does not. "Obvious" to you is not obvious to a new team member.
- **Every load-bearing pointer gets replaced by its claim.** Sort each pointer into one of two kinds. *Navigational* pointers send the reader away for detail they do not need here — "Track A's sizing lives in the design doc" — and are fine. *Load-bearing* pointers are links in the argument: if the reader cannot resolve one, the reasoning breaks. Rewrite the sentence around the substance and delete the label. "Decision 5 conflicts with decision 6" becomes "Sequencing drafts-read before variants was meant to keep a variants rollback clear of unpublished drafts; making the variants editor create those drafts undoes that." If the substance will not fit in a clause, either it belongs in this document or the argument resting on it does not.
- **The deletion test — the only way to pass the rule above.** Delete the label from your rewritten sentence. If the sentence still reads correctly and still makes its point, the substance is in the prose and you are done. If deleting it breaks the sentence, you appended a gloss instead of replacing the pointer, and the reader is still holding a lookup key. Both of these fail the test: "Decision 12 (Redis evicts under memory pressure) blocks this" and "the concerns in Decision 12, which are about Redis eviction". This passes: "Redis evicts keys under memory pressure and silently logs users out, which is why the admin console stayed on the database." **A person's name is a pointer too, and the easiest one to leave bare.** "Wei flagged this in review" tells the reader nothing about why that flag carries weight; "the engineer who owns the attribution model flagged this" does, and survives deleting the name. **Resolving pointers must not grow the document.** Annotating labels adds words while leaving the labels in place; replacing them spends those words on substance and pays for them out of the prose the labels were standing in for. A revision whose word count rose is annotation, not replacement.
- **Verify the claims the argument rests on, and distrust the tidy ones.** Some sentences scope the argument: "that case is already excluded," "only three edits remain," "the objection and the remaining scope land on exactly the same edits." Everything downstream depends on them, so check each against the source rather than against your memory of it. Symmetry is the signal to check hardest — the compression target and the claim-heading rule both reward a confident assertion over an accurate qualified one, so an argument that resolves into a neat coincidence is as likely to mean you smoothed over a gap as found one. **"Already excluded," "already handled," "out of scope per X" are the highest-risk form.** Quote X and check that it says what you need it to say. A clause that defers to current behavior — "keeps today's behavior," "no change from the status quo" — settles nothing when the behavior differs by case. **Apply it as a binary test: write down, in one sentence, the single behavior the clause preserves.** If you cannot do that without picking between two options, the clause names no behavior and is therefore not an exemption, and whatever it appeared to exclude is still in scope. Whether the difference is long-standing, deliberate, or covered by a passing test is irrelevant to this test — those facts explain why the divergence exists, and a divergence the clause cannot choose between is the thing that voids it. Do not substitute the easier question "is this gap in scope?" for the question the test asks. Where you cannot tell which reading was intended, say so as an open question and state what the answer decides. When one of these turns out to be wrong, delete the conclusion it supported rather than footnoting it, and follow the correction through every section that leaned on it — the scope list, the alternatives, the risks. Noticing the contradiction and leaving the body's claim standing is the failure mode to watch for: a correction parked in an appendix has not been applied. A rhetorical high point resting on a false premise is the most expensive sentence in the document.
- **The "so what" test:** For each paragraph: "So what? Why should the reader care?" No answer? Cut it.
- **One path through:** A reader should read start to finish without jumping around. Forward references signal structural problems.

**Check:** Would someone who joined the team yesterday understand this? Someone in another team?

### Revise → Apply Targeted Passes

When incorporating external feedback after sharing the document:

- **Restructure, don't append.** New information replaces or reshapes existing sections; it doesn't get tacked onto the end.
- **After every change, re-run the pass that governs what changed.** New rationale? Re-run Pass 4. New section? Re-run Pass 1 and 2. Rewritten paragraph? Pass 3.
- **If the document grew, re-run Pass 3 (clarity) over the whole thing.** Feedback incorporation is the #1 source of bloat.
- **Growth is legitimate only when you can name what it bought.** Feedback that exposes a wrong premise or an under-served walkthrough can cost real words: a fourth case, a risk row, an open question. That growth is content the argument requires, and the word-count rule does not forbid it. State the purchase explicitly — which case, which risk, which question — because "the argument needed it" with nothing named is how bloat gets waved through. **Naming the purchase licenses the words, not the growth.** Even a fully justified new case gets paid for out of the existing prose: a revision that ends more than 5% longer than the draft it replaces has stopped cutting, however well it can account for what it added. **Correct first, then cut.** Never hold a word count by leaving a false argument standing: make the correction, then pay for it by cutting until the document is no longer than the draft it replaces. **The 5% figure is a boundary for detecting failure, not an allowance to spend.** A revision that lands just under it has read a limit as a budget and stopped Pass 3 early — the target is parity or shorter, and corrections are funded from the prose, not from the ceiling.
- **Never narrate the revision inside the document.** Diffs, concessions, "as noted in v2," and what changed since the last draft belong in your message to the reviewer. The document is read cold by people who never saw the earlier version. Moving that narration out is usually the first 100 words of the cut that pays for legitimate growth.

### Polish → Pass 3 Only

Final line-level pass: given-new chains, active voice, clutter cuts. No structural changes at this stage. Read the entire document aloud (mentally).

## Quick Reference

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| "Wall of text" | No pyramid, no hierarchy | Pass 1: BLUF headings, governing ideas |
| "Can't tell what's important" | Missing zoom levels | Pass 2: Signal abstraction level, nest details |
| "Sentences are hard to parse" | Given-new violated, passive voice | Pass 3: Reorder, active voice |
| "Why did they choose this?" | Missing rationale | Pass 4: Add why/why-not to every decision |
| "Too long, nothing to cut" | Curse of Knowledge | Pass 3: Cut 30%. If you can't, you're not trying |
| "Reads like a textbook" | No concrete examples | Pass 3: Concrete instance before every abstraction |
| "That example couldn't exist" | Walkthrough built as a union of categories | Pass 1: One real instance; each other category its own short case |
| "The walkthrough buries the point" | The comparison the document is about arrives last | Pass 1: Put the contested behavior at the top of the walkthrough |
| "This claim is doing a lot of work" | Scoping claim asserted from memory, not checked | Pass 4: Verify against the source; delete what rested on it |
| "I'd need three other docs open to follow this" | Labels standing in for ideas the reader doesn't have | Pass 4: Replace each load-bearing pointer with its claim |
| Document got longer after revision | Added detail instead of restructuring | Re-run relevant pass. Revise by subtraction. |
| "I'll just add a paragraph to address that feedback" | Appending instead of restructuring | Pass 1: Where does this belong in the pyramid? |

## Common Mistakes

- **Adding detail during revision instead of rewriting.** "This needs more explanation" usually means the existing sentences are poorly structured. Rewrite them — don't add more.
- **Leading with context instead of conclusion.** The reader needs to know where you're going before they care about how you got there.
- **Treating all information as equally important.** Six H2 sections with equal word count = no hierarchy.
- **Writing for your current self instead of a future stranger.** The engineer joining in 6 months has zero context.
- **Defending instead of arguing.** Listing reasons your approach is correct, without presenting alternatives you rejected. The latter is more persuasive.
- **Building the concrete example by union.** Merging every category's worst case into one "seller" or "user" produces something no reader can picture and no instance could be. Concrete means one instance, not the union of all of them.
- **Trading a true bounded claim for a crisp false one.** The 30% target and the claim-heading rule both reward assertion. Neither licenses promising a capability that does not exist, or asserting a scope you did not check.
- **Underfeeding the walkthrough to protect the word budget.** The walkthrough is where words buy the most understanding per word spent. Cutting it to hit a target is cutting the wrong section.
- **Naming an idea instead of stating it.** "Decision 5 and decision 6 conflict" reads as an argument to the author and as a lookup task to everyone else. Compression that leans on the reader's missing context is not compression. Cutting word count by turning claims into labels makes a document shorter and less understandable at the same time.

## Red Flags — Stop and Rewrite

- The document got longer after a revision pass
- You can't state the single key insight in one sentence
- Headings are topic labels, not claims. **Any heading that could appear in a document on a different topic (e.g., "Problem," "Architecture," "Migration Plan," "Risks") is a topic label — rewrite as a claim.**
- A section has more than 5 immediate subsections
- A paragraph takes more than 4 sentences to make its point
- "The reader will figure it out" — you have Curse of Knowledge
- You can't find a single concrete walkthrough anywhere in the document
- Elegance treated as evidence — the neater the convergence, the likelier you wrote past a gap

**Any of these: identify which pass was skipped, redo that pass.**

## Before Declaring a Revision Done

Run all six. Each is an action that produces something you write down, not a question you answer yes to — a revision that satisfies these from memory has not done them. Stopping because the changes so far hang together is the failure this list exists to catch.

1. **Name the walkthrough's instance in one noun phrase** ("a budget spreadsheet", not "a file"). Then list every property the walkthrough attributes to it, and mark each one that instance does not actually have. A non-empty mark list means Pass 1 is unfinished: move those properties out to their own cases.
2. **Quote the walkthrough's first two sentences.** If the document contrasts two behaviors and both do not appear in what you just quoted, restructure the walkthrough.
3. **Write the word count of every section.** If the walkthrough carries the central claim and any section is longer, cut that section.
4. **List every sentence that scopes the argument** — "already excluded", "already handled", "only N remain", "covers exactly the same". For each, quote the text it rests on and write the single rule or behavior that text names. Any one you cannot write down is a correction to make, not a claim to keep, and the correction runs through the scope list, the alternatives, and the risks.
5. **List every label and cross-reference** — decision numbers, doc and RFC names, milestone and track names, ticket ids, section marks, review bodies, people's names — and mark each navigational or load-bearing. Replace each load-bearing one with its substance, then re-read that sentence with the label deleted. A document that needs three other documents open is not finished, however short and well-structured it is.
6. **Write four numbers: words before and after, surviving labels before and after.** Both must fall. Words down with labels flat means you compressed claims into shorthand. Labels down with words up means you glossed instead of replacing. If words rose, name what the growth bought and then cut to parity.
