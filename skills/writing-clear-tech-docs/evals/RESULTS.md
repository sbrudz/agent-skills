# Eval results — pointer-audit addition (2026-08-04)

Change under test: Pass 4 gained a load-bearing-pointer rule, a deletion test, and a
two-number red flag; Pass 1's heading rule was extended to claims built on pointers.

**Baseline** = the pre-edit SKILL.md (git `92f7764`, 121 lines). Run across Opus and Sonnet
per CLAUDE.md's cross-model requirement. All word and label counts below come from
`pointer_report.py --summary` run against the settled output files, never from the runs'
self-reports — several runs misreported their own numbers in both directions, and reading a
file mid-run produced two more wrong figures.

Run outputs were not retained (they would ship to every plugin install). The counts are
reproducible by re-running; see *Reproducing* below.

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

## Reproducing

```bash
# 1. snapshot the baseline skill
git show 92f7764:skills/writing-clear-tech-docs/SKILL.md > /tmp/baseline-SKILL.md

# 2. for each eval in evals.json, run 4 configs: {baseline, current} x {opus, sonnet}.
#    Give the subagent the skill file as its ONLY methodology -- tell it explicitly not to
#    invoke any other skill or read any other SKILL.md, or the installed plugin copy of this
#    skill contaminates the baseline arm.

# 3. measure
python3 pointer_report.py --summary <each>/revised.md   # words + external label count
python3 pointer_report.py <each>/revised.md             # sentences, to grade by hand
```

Three traps this benchmark hit, all worth avoiding on the next run:

- **Do not read an output file while its run is still writing.** An intermediate read
  reported one revision as 1,102 words when it settled at 1,030, inverting a conclusion.
- **Do not trust a run's self-reported metrics.** One claimed "label count dropped from 9 to
  0" while counting only two of the label classes; seven survived. Another reported 871 words
  for an 881-word file.
- **Verify the baseline arm never read the edited skill.** Grep each transcript for the
  edited file's path before believing a null result.
