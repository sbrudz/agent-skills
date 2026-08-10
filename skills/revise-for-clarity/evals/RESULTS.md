# Eval results

Three changes have been benchmarked against this skill. Newest first. All word and label
counts come from the committed scripts run against **settled** output files, never from a
run's self-report — runs misreport their own numbers in both directions, and reading a file
mid-write produced wrong figures in all three benchmarks. See *Reproducing* for how to avoid it.

Run outputs are not retained (they would ship to every plugin install). Counts are
reproducible by re-running.

---

# Spine, slot-claim headings, temporal state, input contract (2026-08-10)

The change that also renamed the skill from `writing-clear-tech-docs` to `revise-for-clarity`
and generalized it past technical documents. Under test:

- A **Before Pass 1 — Choose the Spine** section: the passes are relative operators that
  improve a structure and never choose one.
- Headings carry a **slot and a claim**, replacing the previous claim-only rule. The old Red
  Flag forbade the form that works.
- Pass 2 gained the **typography** rule (bold has one level).
- Pass 3 scoped the **30% target** to a bloated first draft and exempted **modal verbs as
  bounds** from the hedge cut.
- Pass 4 gained the **four states** (was / today / available-not-live / proposed) with the
  audit in `references/temporal-clarity.md`.
- The Revise section gained a **baseline-reset** clause and extended the narration ban to
  **analysis** narration.
- A new **input contract** with a named HALT: existing text only, explicit invocation only.

**Baseline** = SKILL.md at v2.6.0 (git `7ef8dcb`, 3,751 words, named
`writing-clear-tech-docs`). **Current** = 4,169 words + a 1,814-word reference file.

12 arms: two new fixtures x {baseline, current} x {opus, sonnet}, plus a regression pair and
an input-contract pair on current only. Planted traps are recorded in `files/TRAPS.md`,
written before grading so no rubric was adjusted to fit a result.

## Fixture A — the investigation spine (`files/build-cache-rollout.md`)

1,307 words. Reproduces the profile of a real draft a reader called "incredibly hard to
follow" *while fully complying with every pre-2.7.0 rule*: 10 sequentially numbered
claim-only H2s, zero H3, 21 of 24 paragraphs opening bolded, 16 inline `[VERIFIED]` tags,
0 slot+claim headings. Its walkthrough is deliberately correct, isolating the new rules from
the v2.6.0 walkthrough rules. **The draft is already terse, so a 30% cut is the wrong
operation** and a substantially shorter output is a failure.

| arm | words | Δ | H2/H3 | numbered | slot+claim | inline tags | traps |
|---|---|---|---|---|---|---|---|
| baseline | Opus | 1288 | −1% | 4/9 | 0 | **0** | **15** | 6 / 8 |
| baseline | Sonnet | 1125 | **−14%** | 5/8 | **5** | **1** | **16** | 4 / 8 |
| current | Opus | 1287 | −2% | 6/8 | 0 | 12/14 | 0 | **8 / 8** |
| current | Sonnet | 1323 | +1% | 6/8 | 0 | 5/14 | 0 | **8 / 8** |

Both baselines failed the same two traps: they left 15 and 16 of the 16 verification tags in
the prose, and produced 0 and 1 slot+claim headings, so a reader still cannot locate risks or
alternatives. Baseline Sonnet additionally kept 5 numbered headings and cut 14% from a draft
with nothing to cut. Both current arms produced conventional slot sets — Opus:
`Design:` / `Alternatives considered:` / `Risks` / `Rollout:` / `Open questions` /
`Appendix: evidence` — at parity length.

**Opus reported landing its first pass at +14% and then cutting back below parity, citing the
subtraction invariant.** That is the anti-Goodhart wording from the previous benchmark holding
under a rule set that actively invites growth.

## Fixture B — four states, not two (`files/outbox-delivery-migration.md`)

898 words, almost no pointer labels, every falsifying fact in its own appendix: flag state (A),
the 15th call site (B), measurement provenance (C), dates (D).

| arm | words | Δ | risk state column | appendices kept | traps |
|---|---|---|---|---|---|
| baseline | Opus | 842 | −6% | ✗ `Risk \| Mitigation` | 1 of 4 | 8 / 11 |
| baseline | Sonnet | 720 | **−20%** | ✗ `Risk \| Mitigation` | **0 of 4** | 6 / 11 |
| current | Opus | 890 | −1% | ✓ `Risk \| State \| What to do` | 1 of 4 | **11 / 11** |
| current | Sonnet | 963 | **+7%** | ✓ `Risk \| Status \| Mitigation` | **4 of 4** | 10 / 11 |

Current Opus is the strongest arm in the benchmark. It promoted the buried correcting sentence
into the summary ("nothing drains the table, so the inline call still delivers everything and
the duplicate-send bug is still live"), gated the digest claim in the same sentence, attached
the file path to today's state rather than to proposed behavior, and dated the measurement
("a run on 2026-07-14 cost 14 writes per 200-row batch… the 1.4x once claimed has no basis").

Baseline Sonnet is the clean counter-example on provenance: it kept "the dispatcher costs 14
writes per 200-row batch" as a standing present-tense property, which is the measurement
promoted to a property, exactly.

## Findings worth keeping

1. **The typography rule is not a discriminator.** Both baseline-A arms promoted real divisions
   to subsections unprompted (H3 = 9 and 8). Recommendation 3 codifies behavior that already
   happens rather than fixing a gap. Kept because it is cheap and because fixture B's Sonnet
   arm did go flat (H3 = 0), but it earns no credit here.
2. **The conventional-slot instruction contradicts the 3-5 rule, and the models were right to
   ignore the 3-5 rule.** A standard RFC slot set is 6-8 sections. Three of five current arms
   exceeded 5 top-level siblings (H2 = 6, 6, 7) while correctly adopting the slots. The skill
   sanctions neither outcome. **Fix: exempt a genre's settled slot set from the 3-5 rule
   explicitly.**
3. **Deleting a false claim and scoping it are both passes, and scoping is better.** Both
   baseline-B arms resolved the 240 ms overclaim by deleting it; both current arms kept it and
   bounded it to what was measured. Deletion loses true information, so a trap "passed" by
   deletion should be recorded separately from one passed by correction.
4. **Both baseline-B arms destroyed the evidence appendices** to fund their cuts (1 of 4 and
   0 of 4 surviving), while current-Sonnet preserved all four. The analysis-narration rule
   redirects verification status *into* an appendix, and that is what protects it from the
   compression pass.
5. **The subtraction invariant held on Opus and slipped on Sonnet.** Opus cut back from +14% to
   −2%; Sonnet landed at +7.2% on fixture B and conceded it had only "paid for [it] partly."
   Growth pressure is what the new rules add, and Sonnet is where it leaks.
6. **Sonnet's tool calls broke the flat band.** Across the entire v2.6.0 benchmark Sonnet sat at
   15-28 tool calls regardless of how many rules it was given. Here: 23, 24, 28, 46. The 46 was
   fixture B, the case with the most verification to do. The written-output checklist is
   producing verification work on Sonnet rather than more prose about verification.
7. **The input contract holds on both models.** Given raw notes and "Draft the RFC," both
   halted and quoted the HALT rule back. Neither drafted. Note the limit of this result: the
   skill was supplied directly as the arm's methodology, so this measures whether the contract
   *governs behavior once loaded*, not whether the description prevents auto-triggering. That
   second question needs an installed build.
8. **The regression pair is clean.** On `folder-move-parity.md`, current Opus landed at 1288
   words (−0.1%), matching the v2.6.0 record exactly, with every v2.6.0 behavior intact (union
   walkthrough rebuilt, binary exclusion test fired, 7 labels down to 1) plus new temporal
   marking on risk rows and `would` in Alternatives. Sonnet drifted to +3.5%, within the
   boundary, while catching more (a miscount, a forward reference, an undefined term).

## Known gaps

- **Fixture B is a weak discriminator on Opus.** Baseline Opus caught 8 of 11 traps using only
  the v2.6.0 claim-verification rule plus the appendix evidence. The temporal rules' measured
  value on Opus is the *systematic* framing (a state column, an available-not-live section)
  rather than catching claims Opus would otherwise miss. On Sonnet the gap is real (6 → 10).
- **Trap B8** (phase-anchoring "both paths write to the same table") is ungradable: every arm
  deleted or rewrote the sentence, so no arm was ever tested on it.
- **`should`-as-state-marker (B9) and the unmerged limiter (B10)** were verified on the current
  arms only; the baseline arms restructured those sentences away before the check could apply.

# Walkthrough construction + anti-overpromise (2026-08-04)

Change under test, all in response to review feedback on a real proposal:

- Pass 1's concrete-scenario bullet became three rules: one real instance rather than a union
  of categories, the contested comparison as the walkthrough's spine, and a budget sized to
  the argument instead of capped at 3-5 sentences.
- Pass 3 gained **cut hedges, keep bounds**.
- Pass 4 gained **verify the claims the argument rests on, and distrust the tidy ones**.
- The Revise section gained a named-purchase rule for legitimate growth, a ban on narrating
  the revision inside the document, and a 5% growth ceiling.

**Baseline** = SKILL.md at v2.5.0 (git `2075672`, 127 lines).
Fixture: `files/folder-move-parity.md`, 1289 words, walkthrough 92 words (7% of the doc)
while carrying the central claim. It plants a composite example, a buried comparison, a false
scoping claim whose falsifying evidence sits in its own appendix, an unbounded reword, and a
revision-narration section. **It carries zero external pointer labels, so it isolates this
change from the v2.5.0 pointer rules.**

## Scores

| skill version | model | words | Δ | assertions |
|---|---|---|---|---|
| baseline | Opus | 1051 | −18.5% | 4 / 10 |
| baseline | Sonnet | 1285 | −0.3% | 0 / 10 |
| iter 1 | Opus | 1216 | −5.7% | 8 / 10 |
| iter 1 | Sonnet | 1177 | −8.7% | 2 / 10 |
| iter 2 (+ mechanical triggers, + exclusion test) | Opus | 1285 | −0.3% | **10 / 10** |
| iter 2 | Sonnet | 1471 | **+14%** | 8 / 10 |
| iter 3 (+ 5% ceiling, + pay-for-it-here) | Opus | 1281 | −0.6% | **10 / 10** |
| iter 3 | Sonnet | 1288 | −0.1% | 6 / 10 |
| iter 4 (+ binary exclusion test, + correction precedence) | Opus | 1352 | **+4.9%** | **10 / 10** |
| iter 4 | Sonnet | 1234 | −4.3% | 6 / 10 |
| iter 5 (+ reframed ceiling, + action checklist) | Opus | **1288** | **−0.1%** | **10 / 10** |
| iter 5 | Sonnet | **1289** | **0%** | **~7.5 / 10** |

**Shipped: iter 5.** Opus 4 → 10 and Sonnet 0 → ~7.5, both landing at or below the source
length. Sonnet's residual gaps are one fail (another section outweighs the walkthrough, 197
and 176 words against its 154) and three partials: the client contrast arrives in the
walkthrough's fourth sentence rather than its first two, and its premise correction records
the trash gap as "known, not resolved" instead of moving the move into the disputed set. It
does apply the tidy-convergence rule explicitly and in its own words — *"That fit is too neat
to trust without checking the case the policy waves off."*

**Sonnet oscillates between the two rule clusters; Opus applies both.** Iter 3 Sonnet passed
all five walkthrough assertions and failed all three premise-correction assertions. Iter 4
Sonnet inverted it exactly: it corrected the premise, deleted the symmetry claim, and left the
composite example verbatim with the walkthrough at 86 words against a 202-word sibling. Each
iteration that strengthened one cluster cost the other, at a roughly constant total score.
Opus reached 10/10 on both clusters at iterations 2, 3, and 4.

The effort telemetry rules out the obvious explanation. Sonnet is not under-trying: it spent
more tokens than Opus in every arm. The asymmetry is in tool calls, not tokens.

| arm | Sonnet tokens / calls | Opus tokens / calls |
|---|---|---|
| baseline | 115k / 28 | 89k / 26 |
| iter 1 | 98k / 15 | 91k / 27 |
| iter 2 | 119k / 19 | 111k / 40 |
| iter 3 | 126k / 25 | 101k / 35 |
| iter 4 | 131k / 26 | 104k / 45 |

As rules accumulated, Opus's tool calls climbed 26 → 45 while Sonnet's stayed flat at 25-28.
**Opus answered more rules with more verification; Sonnet answered them with more prose.** The
failure is therefore a stopping criterion, not a capacity limit: Sonnet stops once it holds a
coherent set of changes it can narrate, rather than auditing each rule against the document.
That matches its iter-3 behavior of stating the falsifying fact accurately and then reasoning
to the opposite conclusion — a coherent narrative built over an unaudited rule.

The consequence for skill design: a completion checklist has to demand **actions with written
outputs** ("name the walkthrough's instance type, then list every property attributed to it"),
never assertions ("check that the example is one real instance"). A satisficing run marks an
assertion-style checklist complete without looking. It also means the two clusters are not
competing for a scarce resource, so rebalancing their relative emphasis would not have fixed
this — the one hypothesis the telemetry does eliminate.

**The action checklist confirmed the diagnosis and broke the oscillation.** Iter 5 added the
six-item *Before Declaring a Revision Done* section, and Sonnet's tool calls jumped 26 → 36,
leaving the 15-28 band it had held for five straight arms, while Opus went 45 → 56. Sonnet
applied both clusters in one run for the first time. Read the tool-call count, not the token
count, when judging whether a rule is being run or merely read — tokens rose monotonically
across every arm regardless and told us nothing.

The checklist was paid for structurally rather than added: five completion checks moved out of
Red Flags into it, so the section cost 7 net lines and no rule is stated in two places.

Per-assertion detail, baseline vs the shipped version:

| # | assertion | base Opus | base Sonnet | final Opus |
|---|---|---|---|---|
| 1 | one real instance, not a union of categories | ✗ | ✗ | ✓ |
| 2 | per-type variation split into its own cases | ✗ | ✗ | ✓ |
| 3 | contested comparison leads the walkthrough | ~ | ✗ | ✓ |
| 4 | walkthrough budget grows | ✓ | ✗ | ✓ |
| 5 | no other section outweighs it | ✓ | ✗ | ✓ |
| 6 | catches the false exclusion | ~ | ✗ | ✓ |
| 7 | scope corrected, or raised as an open question | ✗ | ✗ | ✓ |
| 8 | symmetry claim deleted, not footnoted | ✓ | ✗ | ✓ |
| 9 | reword's collision with a deliberate behavior named | ✗ | ✗ | ✓ |
| 10 | revision narration removed | ✓ | ✗ | ✓ |

## Findings worth keeping

1. **"Protect the walkthrough's budget" was read as "do not touch the walkthrough."** Iter 1
   Sonnet reproduced the composite example verbatim and said so in its own report: it
   deliberately left the example alone because the methodology "protects it from budget cuts."
   The rule now says *exempt from cuts is not exempt from rewriting*. A rule that shields a
   section will be read as shielding its sentences unless you say otherwise.
2. **A composite example survives light editing, because every clause in it is individually
   true.** Nothing in the sentence is false; only the conjunction is impossible. That is why
   the rule has to say *rebuild from scratch* and supply a lexical tell — a generic subject
   ("a file," "a user," "a product") — rather than describe the defect and hope it is noticed.
3. **"Verify against the source" is not a check.** All four iter-1 arms read the appendix that
   falsifies the trash-move exclusion; three accepted the exclusion anyway. What worked was
   naming the *form* ("already excluded", "already handled") and the *specific defect*: a
   clause deferring to current behavior exempts nothing when the behavior differs by case,
   because it names no single behavior.
4. **Noticing a contradiction is not applying it.** Baseline Opus found the trash divergence,
   wrote it into its appendix, and left the body's "already excluded" and the two-move scope
   standing. Hence *a correction parked in an appendix has not been applied*, plus the
   instruction to follow the correction through the scope list, alternatives, and risks.
5. **Naming the purchase licensed the growth.** The named-purchase rule alone let iter-2
   Sonnet grow the document 14% with every addition accounted for. Opus hit the same 10/10
   at −0.3%, proving the growth was avoidable, so the rule needed a number, not more prose.
6. **Correctness and length competed on Sonnet, and it paid for one with the other.** Iter 2
   Sonnet corrected the false premise and grew the document 14%. Iter 3, which added only the
   length constraints, hit parity and quietly dropped the correction — and did it in the worst
   possible way: it stated the falsifying fact accurately ("that behavior differs by design")
   and then used it to *support* the exemption ("that gap predates this proposal and stays out
   of scope"), substituting the easier question "is this gap in scope?" for the one the rule
   asks. A rule that can be satisfied by answering an adjacent question needs a binary
   procedure, which is why the exclusion test now reads *write down, in one sentence, the
   single behavior the clause preserves.*
7. **A stated ceiling becomes a spending target.** Told that "more than 5% longer" is failure,
   iter 4 Opus landed at +4.9% and said so plainly: "at the ceiling the methodology allows."
   Iter 3 Opus had scored the same 10/10 at −0.6%. The threshold now names parity as the
   target and 5% as a detector, with the Goodhart failure called out explicitly, because a
   number in a rule will be read as a budget unless it is denied that reading.
8. **Opus passed an iteration before Sonnet, for the second consecutive change.** At iter 2
   Opus was at 10/10 while Sonnet was at 8/10 and growing the document. Shipping on the first
   good Opus result would have shipped a skill that makes Sonnet inflate documents. This is
   the concrete case for CLAUDE.md's cross-model requirement.

Two things the change bought beyond the assertions: Opus began flagging MECE gaps in
enumerations it was not asked about (a move belonging to neither the settled nor the disputed
list), and it started marking bounds as load-bearing in the prose so a later editor would not
cut them as clutter — *"the trash exception is load-bearing, not hedging."*

See `known_weaknesses` on eval 2 in `evals.json` for two limits of this fixture, including
one trap from the source feedback that does not reproduce in this domain.

---

# Pointer-audit addition (2026-08-04)

Change under test: Pass 4 gained a load-bearing-pointer rule, a deletion test, and a
two-number red flag; Pass 1's heading rule was extended to claims built on pointers.

**Baseline** = the pre-edit SKILL.md (git `92f7764`, 121 lines).

## Eval 1 — revise a dense, pointer-heavy draft (the discriminating case)

Source: `files/session-store-notes.md` — 1,073 words, 45 pointer occurrences, 26 external.
"External" excludes references a document defines itself (its own phase list, track table,
enumerated options); see `INTERNAL_KINDS` in `pointer_report.py`. What remains needs an
artifact the reader does not have: `Decision 12/15`, `PLAT-339x`, `the council`,
`the v1 proposal`, `the runbook`, `milestone 3`, `Phoenix migration`, bare `Wei`/`Priya`.

| skill version | model | words | cut | external labels |
|---|---|---|---|---|
| baseline | Opus | 754 | 30% | 13 |
| baseline | Sonnet | 779 | 27% | 20 |
| iter 1 (pointer rule only) | Opus | 881 | 18% | 4 |
| iter 1 (pointer rule only) | Sonnet | 1030 | 4% | 16 |
| iter 2 (+ deletion test, two-number check) | Opus | **753** | **30%** | **3** |
| iter 2 | Sonnet | 944 | 12% | 9 |
| iter 3 (+ explicit person case) | Sonnet | **746** | **30%** | **0** |

The script over-flags by design — it cannot tell a resolved reference from a bare one, so it
prints each sentence for a reader to grade. Graded by hand, iter 2's nine Sonnet survivors
were three genuine failures, all bare names (`Wei flagged this in review`,
`Priya's suggestion`, `Wei owns this`), which is what iter 3 targeted.

**Result: beats baseline on both models.** Full 30% cut retained with the pointer count
collapsed.

Two findings worth keeping:

1. **The first wording made things worse on length.** "Every load-bearing pointer carries
   its claim" reads as *annotate the label* — models glossed pointers in place
   (`Decision 12 (Redis evicts under memory pressure)`), keeping the lookup key and adding
   words. The deletion test is what forces substitution, and substitution is self-funding:
   the substance replaces the prose the label stood in for instead of adding to it.
2. **Opus passed an iteration before Sonnet did.** At iter 2 Opus was at 30%/2 while Sonnet
   was at 12%/7 with three bare names surviving. The bare-people gap was invisible on Opus
   entirely. Stopping at the first good Opus result would have shipped a skill that leaves
   Sonnet under-cutting with unresolved names.

## Eval 0 — audit a doc that passes every pre-existing red flag

Source: `files/search-reindex-proposal.md` — 1,024 words, 35 pointer occurrences, 19
external. Engineered to satisfy every pre-existing check (SCQA opening, five claim headings,
concrete walkthrough, tight prose, why/why-not per decision), so the only thing left to
find is the pointer density.

| skill version | model | verdict | pointer finding |
|---|---|---|---|
| baseline | Opus | not ready | ~12 undefined external references |
| baseline | Sonnet | not ready | 3 references, framed as *citation* gaps; prescribed adding links |
| final | Opus | not ready | ~20 references, ~14 load-bearing; names the consequence (section 1 unevaluable) |
| final | Sonnet | not ready | 4 references **plus the pointer-based heading** |

**Weak discriminator — see `known_weaknesses` in `evals.json`.** Both baselines found the
problem unprompted, so this case does not demonstrate the edit catches an otherwise-missed
flaw. What it does show: the baseline prescribed the wrong repair (add links, which the rule
explicitly rejects) and missed the heading. Regression-check value going forward.

---

# Reproducing

```bash
# 1. snapshot the baseline skill (use the tag the change was made against)
# the skill was named writing-clear-tech-docs at and before v2.6.0
git show v2.5.0:skills/writing-clear-tech-docs/SKILL.md > /tmp/baseline-SKILL.md

# 2. for each eval in evals.json, run 4 configs: {baseline, current} x {opus, sonnet}.
#    Give the subagent the skill file as its ONLY methodology -- tell it explicitly not to
#    invoke any other skill or read any other SKILL.md, or the installed plugin copy of this
#    skill contaminates the baseline arm.

# 3. measure
python3 pointer_report.py --summary <each>/revised.md   # words + external label count
python3 pointer_report.py <each>/revised.md             # sentences, to grade by hand
python3 section_report.py <each>/revised.md             # per-section words, largest first
```

Traps both benchmarks hit, all worth avoiding on the next run:

- **Measure only after the run's completion notification, and verify your wait actually
  waits.** A file can be rewritten several times; one arm went 1400 → 1353 → 1288 words after
  it first appeared. Worse, the shell guard used to wait for stability was
  `find … -newermt '-90 seconds'`, which is a GNU extension: this machine's `find` is `bfs`,
  which errors on it, and `$(…)` swallowed the error into an empty string that read as
  "stable." Every stability check silently passed instantly. Compare mtime numerically
  instead:
  `python3 -c "import time,os;print(time.time()-os.path.getmtime(P))"`.
- **Do not trust a run's self-reported metrics.** One claimed "label count dropped from 9 to
  0" while counting only two of the label classes; seven survived. Another reported 871 words
  for an 881-word file. Note the converse also happened: two self-reports were right and the
  numbers contradicting them were mine, taken mid-write.
- **Verify the baseline arm never read the edited skill.** Grep each transcript for the
  edited file's path before believing a null result.
- **Measure section balance with H3 reported separately.** An H2-only version of
  `section_report.py` scored a false pass for a run that nested an unrelated subsection under
  the walkthrough heading, inflating that H2 to 311 words while the walkthrough itself stayed
  at 87.
