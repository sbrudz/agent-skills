---
name: git-commit-message
description: Use when about to write a git commit message, before running git commit — applies when staged changes are ready and a message needs to be drafted
---

# Git Commit Message

A commit message is not a description of what changed — the diff already shows that. It's a record of *why* the change was made: the problem it solved, the constraint it respected, the decision it encoded. This skill guides writing messages that are useful months later to a reader with no context.

## Step 1 — Detect Repo Convention (do this first)

Run `git log --oneline -20` and scan the subject lines.

- If ≥50% use `type:` or `type(scope):` prefixes → **conventional commits mode**
- If the repo has no commits yet → **conventional commits mode** (new repo default)
- Otherwise → **match existing style**: extract the dominant pattern from recent commits (ticket prefixes, sentence case, imperative phrases, etc.) and replicate it

**Do not default to conventional commits if the repo uses a different style.**

## Step 2 — Hygiene Check (flag before drafting)

Scan the staged diff for multiple unrelated concerns:

- Different logical areas changed together (e.g., bug fix + dependency bump + formatting)?
- Does describing the change require "and"?

If yes → flag it: *"These look like separate logical changes — consider splitting into multiple commits."* Then **still draft the message** for the combined change. The hygiene flag is advisory — do not block or wait for a response before producing the commit message.

When drafting a combined message: subject covers the most significant change; body lists the remaining changes with a one-line reason each.

## Step 3 — Draft the Subject Line

- **Imperative mood**: completes "If applied, this commit will ___"
  - ✓ `Add null check for emailVerifiedAt in auth middleware`
  - ✗ `Added null check` / `Adding null check`
- **50 chars target, 72 hard limit** — longer subjects get truncated in `git log` and GitHub
- **No trailing period**
- **No vague words without concrete detail**: avoid *fix, update, change, improve, misc* as the entire subject — always follow them with what specifically
  - ✓ `Fix off-by-one error in pagination that skipped last item`
  - ✗ `Fix pagination bug`
- **No "and"** — if you need it, split the commit

## Step 4 — Write the Body (required for non-trivial changes)

The body answers the question: *"Why did this change need to exist?"*

For any change involving a decision, trade-off, or non-obvious fix, answer these:

1. **What was wrong before?** What problem, gap, or constraint triggered this change?
2. **Why this approach?** If alternatives existed, why this one?
3. **Anything the reader needs to know?** Side effects, follow-ups, related issues?

**The body is optional only for purely mechanical changes** (version bumps, generated file updates, whitespace-only fixes).

**The diff already shows *what* changed. Do not restate it.**

```
# BAD — restates the diff
fix: add null check for emailVerifiedAt in auth middleware

Prevent null pointer by checking if emailVerifiedAt exists before
calling toISOString().

# GOOD — explains why it was a problem
fix: guard against null emailVerifiedAt crashing login flow

Unverified users have a null emailVerifiedAt. The auth middleware was
calling .toISOString() on it unconditionally, crashing the login
request with a TypeError. This only affects users who registered but
never confirmed their email.
```

Separate subject from body with a blank line. Wrap body lines at 72 chars.

## Pre-Finalization Checklist

Before committing:

- [ ] Subject follows detected repo convention
- [ ] Subject is imperative mood
- [ ] Subject is ≤72 chars (≤50 preferred)
- [ ] Subject has no trailing period
- [ ] Subject has no vague words without concrete detail
- [ ] Subject has no "and" (or hygiene flag was addressed)
- [ ] Body is present for any non-trivial change
- [ ] Body explains *why*, not *what* — could someone understand the reasoning without reading the diff?
- [ ] Body lines wrap at 72 chars

## Common Mistakes

| Mistake | Fix |
|---|---|
| Body restates the diff | Ask: "Does this say anything the diff doesn't?" If not, replace with *why* |
| Defaulting to conventional commits in a non-CC repo | Run `git log --oneline -20` first, always |
| Vague subject (`fix bug`, `update files`) | Name the specific thing that changed and what happened to it |
| Combining unrelated changes | Flag hygiene issue before drafting; suggest splitting |
| Writing body for a version bump | Body optional for mechanical changes with no decision involved |
