# writing-clear-tech-docs — recommended changes

**Date:** 2026-08-05
**Status:** Applied 2026-08-10. All five changes landed in `skills/revise-for-clarity/SKILL.md` (the skill
was renamed from `writing-clear-tech-docs` in the same change). The cross-reference below is the one item
still open: the baseline-reset clause was applied here and the sibling copy in Big Cartel's private
`tech-docs` plugin has not been updated, so the two rules now disagree until that side lands.
**Source:** Retrospective on five drafts of a Rails design RFC (Big Cartel admin, variants editor).
The author's verdict on the drafts: v2 and v3 were "incredibly hard to follow," and v3 "seemed to follow
the mechanics of writing-clear-tech-docs but not its spirit/intent of understandability."
Restructuring as an RFC through a separate templating skill produced v4, which was "much clearer"; v5
"took it up another level."

Five changes. The first is the important one; the rest are supporting.

---

## The measurement that drives all of this

| | v2 | v3 | v4 | v5 |
|---|---|---|---|---|
| Words | 7,084 | 3,976 | 4,988 | 7,582 |
| Headings (H2 + H3) | 37 | 10 | 33 | 33 |
| H3 subsections | 30 | **0** | 24 | 24 |
| Paragraphs opening with a bolded lead-in | — | **30** | — | — |
| Inline `[VERIFIED]`-style tags | — | 13 | 0 | 0 |
| Reader verdict | hard to follow | hard to follow | much clearer | clearest |

**v3 is the shortest of the four and the hardest to follow. v5 is the longest and the clearest.**
Length was never the variable that mattered, and the skill's most prominent numeric target was
optimizing it.

v3 was produced under full, good-faith compliance with all four passes. It has a genuine SCQA opening,
claims for every heading, active voice, given-before-new chains, and concrete examples. It is still
unreadable. That combination is what needs explaining, and the explanation is structural.

---

## Change 1: headings need a slot *and* a claim, and the current red flag forbids the form that works

**Location:** Pass 1, "Headings as claims, not topic labels," plus the matching entry in "Red Flags."

### The problem

The skill frames claim-versus-label as a binary and picks claim. The red flag enforces it hard:

> Headings are topic labels, not claims. **Any heading that could appear in a document on a different
> topic (e.g., "Problem," "Architecture," "Migration Plan," "Risks") is a topic label — rewrite as a
> claim.**

In a document type with conventional slots, this is actively harmful. "Risks" and "Alternatives
considered" are not lazy topic labels; they are the *slots a reader navigates by*. An RFC reader looking
for what could go wrong scans for "Risks." Rewriting that heading into a pure claim removes the only
handle they have.

v3 complied fully, and its ten H2s are all claims. The consequence is that a reader cannot locate
anything. Two examples from the actual document:

- `## 4. Four more passes through the design, and the third one changes the UI`
- `## 10. Start here`

Nothing in that heading set tells a reader where the risks live, where the open questions live, or what
is being asked of them. The document became unnavigable *because* it obeyed the rule.

### What worked instead

The compound form, slot first and claim second:

- `## Risks and security: renaming a choice destroys a sibling's variants today, and no constraint can catch it`
- `## Rollout plan: harden the write path, extend the dirty mechanism, swap the plan object invisibly, then flag the grid`
- `## Alternatives considered` with each H3 opening `### Rejected: <alternative>, because <reason>`

The slot gives navigation. The claim gives the skim layer its argument. Both, not either.

### Proposed edit

Replace the binary with the compound, and scope the red flag:

> **Headings carry a slot and a claim.** Where the document type has conventional sections (an RFC's
> Risks, Alternatives, Rollout, Open questions; a postmortem's Timeline, Impact), name the slot, then
> state the section's conclusion after a colon: "Risks: renaming a choice destroys a sibling's variants
> today, and no constraint can catch it." The slot is how a reader navigates; the claim is how the skim
> layer carries the argument. Where the document has no conventional structure, the claim alone is right.
>
> A bare slot name with no claim is the failure this rule exists to prevent. **A document whose headings
> are all claims and no slots is the opposite failure, and it is worse:** the reader cannot predict where
> anything lives, so they must read linearly to find the one section they came for.

And in Red Flags, replace the current entry with:

> Headings are bare topic labels with no claim attached — **or**, in a document type with conventional
> sections, claims with the slot name stripped out, leaving the reader nothing to navigate by.

---

## Change 2: say that the passes improve hierarchy and never choose it

**Location:** new preamble to Pass 1.

This is the direct answer to "followed the mechanics but not the spirit." Every pass in this skill is a
**relative operator**: it improves whatever structure it is handed. Not one of them chooses the
structure. Run all four passes, at full compliance, over a document organized by the areas the author
happened to investigate, and the output is a well-written investigation report. That is exactly what v3
is, and it is why compliance and understandability came apart.

What fixed it was an *absolute* structure keyed to the reader's decision, supplied by an RFC template:
Context, Proposed design, Alternatives considered, Risks, Rollout, Open questions, Estimate, Gotchas.
The reordering alone accounted for most of the gain from v3 to v4, at roughly equal word count.

Proposed preamble:

> **Choose the structure before you improve it.** These passes are relative: each one improves whatever
> organization you hand it, and none of them chooses that organization. A document organized around the
> author's investigation — one section per area explored, in the order it was explored — will pass every
> check below and still be hard to follow, because the reader is navigating someone else's research
> process instead of their own decision.
>
> So before Pass 1, ask what the reader has to decide and what the document type's conventional sections
> are. If the type has a settled structure (RFC, ADR, postmortem, PRD), adopt it wholesale and *then*
> run these passes inside it. Two tells that a draft is organized around the investigation rather than
> the decision: section numbering that goes three levels deep, and a section describing what changed
> since the last draft.

---

## Change 3: add a red flag for hierarchy replaced by typography

**Location:** Red Flags, and a note under Pass 2.

v3 has **zero** H3 subsections and **thirty** paragraphs each opening with a bolded sentence. Bold has
one level, so thirty of them at identical visual weight is a flat list wearing an argument's clothes.
The reader gets no signal about which paragraph is load-bearing and which is an aside — the skill's own
"treating all information as equally important" failure, reached *through* its guidance, because BLUF
applied at paragraph granularity across a whole document makes everything a headline.

Proposed red flag:

> Every paragraph in a section opens with a bolded lead-in, and the section has no subsections. Bold has
> one level; hierarchy needs more than one. This is BLUF applied at the wrong granularity — promote the
> real divisions to subheadings and let most paragraphs start unbolded.

Worth noting for whoever applies this: the existing **3-5 rule** already half-caught v3, which had ten
sibling H2s. Sequential numbering (`## 1.` through `## 10.`) disguised the violation by making the set
look organized. A note under the 3-5 rule that numbering is not grouping would help.

---

## Change 4: qualify the 30% cut target

**Location:** Pass 3, "Cut 30% of word count."

The target is right for a bloated draft and wrong as a standing objective, and it is the most prominent
number in the skill, so it gets treated as the primary success metric. In this session the most
compressed draft was the least understandable one, and the clearest was the longest.

Proposed addition:

> **Cutting is for prose that repeats, hedges, or narrates. It is not a fix for bad structure, and it
> cannot compensate for the absence of one.** A draft organized around the wrong spine gets *worse* as
> it compresses, because compression removes the redundancy that was helping the reader recover. If a
> draft is hard to follow and you cannot find 30% to cut, re-run Pass 1 before cutting anything: the
> problem is the pyramid, not the word count.

This does not conflict with the subtraction invariant, which governs *revisions* of an already-structured
document. Worth making that boundary explicit, since the two rules currently read as the same rule.

---

## Change 5: extend the revision-narration ban to analysis narration

**Location:** "Revise → Apply Targeted Passes," the "Never narrate the revision inside the document"
bullet.

The existing rule covers diffs, concessions, and "as noted in v2." v3 obeyed it and then committed the
same sin one level up: it narrated the *analysis* process instead of the revision process.

- A heading naming how many passes the author made through the design (`## 4. Four more passes through
  the design, and the third one changes the UI`)
- A closing `## 10. Start here`
- A "Verification convention" block in the front matter, plus 13 inline `[VERIFIED]` / `[UNMEASURED]`
  tags scattered through the prose

All of it is the author's working state leaking onto the page. The reader does not care how many passes
were made; they care what is true. v5 has zero inline tags — verification moved to an evidence appendix,
where a reader who wants it can find it and everyone else is not reading around it.

Proposed edit:

> Never narrate your own process inside the document — the revision process *or* the analysis process.
> Diffs, concessions, and "as noted in v2" are the obvious form. The subtler form: headings that count
> the author's passes through the problem, closing sections that tell the reader where to start, and
> per-claim verification tags inline in the prose. Verification status belongs in an evidence appendix,
> one entry per claim, so the reader meets the prose and the proof separately.

---

## Cross-reference

The subtraction invariant in "Revise → Apply Targeted Passes" (the "more than 5% longer than the draft it
replaces" rule) needs a baseline-reset clause for the case where an independent review invalidates a
load-bearing claim and the recommendation is re-derived rather than patched. The same rule is duplicated
in a separate templating skill, and the full argument plus proposed wording is filed there:
`claude-marketplace/docs/plans/2026-08-05-tech-docs-skill-recommendations.md`, change 2. Apply both or
neither, or they will disagree.
