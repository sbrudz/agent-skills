---
name: boy-scout-rule
description: Use during the REFACTOR phase of TDD red-green-refactor and during code quality review to identify and apply incremental refactoring improvements to touched code and its immediate neighbors
---

# Boy Scout Rule — Leave the Code Cleaner Than You Found It

Concrete refactoring checklist for the TDD REFACTOR phase and code quality review. Replaces vague "clean up" guidance with specific patterns to look for.

## Scope

**Refactor: touched code + immediate neighbors.**

- **Touched code:** Anything you wrote or modified in this task.
- **Immediate neighbors:** Functions your code calls, functions that call your code, types your code uses. If your changes made adjacent code harder to read or revealed existing mess, clean it up.
- **Out of scope:** Code you only read for context. Refactoring that would require new tests beyond the task's scope — note it as a follow-up task instead.

**The guardrail:** If a refactoring would show up as an unrelated change in a code review diff, it's out of scope.

## TDD Refactor Checklist

Run through after tests go green. Check your code and its immediate neighbors.

### Structural clarity

- **Extract function** — Any code block doing a distinct thing that you have to read to understand? Name it.
- **Reduce nesting** — More than 2 levels of indentation? Use early returns, guard clauses, or extract the inner logic.
- **Simplify conditionals** — Complex boolean expression? Extract to a named variable or function (`isEligibleForDiscount` instead of `total > 100 && !isTrial && coupon.active`).
- **Rename for clarity** — Do names describe *what*, not *how*? Would a new team member understand without reading the implementation?

### Structural design

- **Consolidate duplication** — Did you write something similar to existing code? Three similar implementations = extract the common pattern. Two might be coincidence.
- **Right-size functions** — Does any function do more than one thing? Split by responsibility. If you can't describe what it does without "and," it's too big.
- **Flatten data flow** — Is data passed through intermediaries that don't use it? Restructure to reduce pass-through.

## Code Review Refactor Checklist

Apply during code quality review (`superpowers:code-reviewer`). The reviewer has the full diff and can spot cross-cutting patterns.

### Cross-cutting patterns

- **Emerging abstractions** — Did multiple tasks create similar code? Three similar implementations is the signal to consolidate.
- **Inconsistent patterns** — Does the new code handle something differently from existing code nearby? Pick one pattern and make them consistent.
- **Growing modules** — Did this task push a file past the point where it's easy to navigate? Flag for splitting.
- **Leaky abstractions** — Does the caller need to know implementation details to use this code correctly? Tighten the interface.

### Companion skill checks

- If code mixes business logic with I/O → apply `functional-core-imperative-shell` checklist
- If code is React (`.tsx`/`.jsx`) → apply `react-best-practices` Section 1 (component responsibility)

### What NOT to flag as refactoring

- Formatting/whitespace changes — that's the linter's job
- Renaming across the whole codebase when only one file was touched
- Refactoring that would require its own unrelated tests — note as a follow-up task
