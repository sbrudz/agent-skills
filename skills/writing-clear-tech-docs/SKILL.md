---
name: writing-clear-tech-docs
description: Use when creating, revising, or refining software design documents, RFCs, architecture decision records, or other technical prose intended to be read and understood by fellow engineers. Also use when a technical document is accurate but dense, hard to follow, buries key insights in detail, reads like a list of facts rather than an argument, or got longer after a revision pass.
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
- **Headings as claims, not topic labels:** "We will use Postgres, not Mongo" not "Database Choice."
- **The 3-5 rule:** No level has more than 5 sibling sections. More? Group under a higher-level governing idea.
- **Concrete scenario (non-negotiable):** Pick one concrete scenario and walk through it in 3-5 sentences before generalizing. This is not optional — a design doc with zero concrete examples is incomplete. Place this walkthrough early, typically after the SCQA opening or at the start of the architecture section. "Here is a request during dual-write. The write lands on the old database first..."

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
- **Active voice:** "Component A calls Component B" not "Component B is called by Component A."
- **One idea per paragraph:** Topic sentence first, supporting details follow. Second point? New paragraph.
- **Concrete before abstract:** Anchor every abstract concept with a concrete example before generalizing. "Consider a user uploading a profile photo. The image pipeline..." then explain the general case.
- **Cut 30% of word count:** Target for every revision pass. Structural framing (zoom signals, BLUF sentences, headings) must be paid for by cutting existing prose — not added on top. If you can't find cuts, you have Curse of Knowledge.

**Check:** Read a paragraph aloud. Natural flow? If it sounds like a textbook, rewrite.

### Refine → Pass 4: Reader Calibration (Kill the Curse of Knowledge)

**Goal:** Someone reading cold follows the argument and understands why decisions were made.

- **State the reader's knowledge explicitly before this pass:** "The reader knows X, Y. The reader does NOT know A, B." Read the document as that reader.
- **Every decision has a "why" and a "why not":** "We chose Postgres because... We rejected Mongo because..." A decision without rejected alternatives is a fact, not an argument.
- **Define before use:** Jargon, acronyms, system names. "Obvious" to you is not obvious to a new team member.
- **The "so what" test:** For each paragraph: "So what? Why should the reader care?" No answer? Cut it.
- **One path through:** A reader should read start to finish without jumping around. Forward references signal structural problems.

**Check:** Would someone who joined the team yesterday understand this? Someone in another team?

### Revise → Apply Targeted Passes

When incorporating external feedback after sharing the document:

- **Restructure, don't append.** New information replaces or reshapes existing sections; it doesn't get tacked onto the end.
- **After every change, re-run the pass that governs what changed.** New rationale? Re-run Pass 4. New section? Re-run Pass 1 and 2. Rewritten paragraph? Pass 3.
- **If the document grew, re-run Pass 3 (clarity) over the whole thing.** Feedback incorporation is the #1 source of bloat.

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
| Document got longer after revision | Added detail instead of restructuring | Re-run relevant pass. Revise by subtraction. |
| "I'll just add a paragraph to address that feedback" | Appending instead of restructuring | Pass 1: Where does this belong in the pyramid? |

## Common Mistakes

- **Adding detail during revision instead of rewriting.** "This needs more explanation" usually means the existing sentences are poorly structured. Rewrite them — don't add more.
- **Leading with context instead of conclusion.** The reader needs to know where you're going before they care about how you got there.
- **Treating all information as equally important.** Six H2 sections with equal word count = no hierarchy.
- **Writing for your current self instead of a future stranger.** The engineer joining in 6 months has zero context.
- **Defending instead of arguing.** Listing reasons your approach is correct, without presenting alternatives you rejected. The latter is more persuasive.

## Red Flags — Stop and Rewrite

- The document got longer after a revision pass
- You can't state the single key insight in one sentence
- Headings are topic labels, not claims. **Any heading that could appear in a document on a different topic (e.g., "Problem," "Architecture," "Migration Plan," "Risks") is a topic label — rewrite as a claim.**
- A section has more than 5 immediate subsections
- A paragraph takes more than 4 sentences to make its point
- "The reader will figure it out" — you have Curse of Knowledge
- You can't find a single concrete walkthrough anywhere in the document
- **Word-count check:** Before declaring a revision complete, compare word count to the previous version. If it didn't shrink, you added scaffolding instead of replacing content. Go back and cut.

**Any of these: identify which pass was skipped, redo that pass.**
