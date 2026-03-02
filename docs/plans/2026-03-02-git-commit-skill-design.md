# Git Commit Message Skill — Design

**Date:** 2026-03-02
**Status:** Approved

## Overview

A skill that guides writing high-quality git commit messages before running `git commit`. The core insight: a commit message is not a description of what changed (the diff shows that) — it's a record of *why* the change was made. This skill helps produce messages that are useful months later, to a reader with no context.

**Skill name:** `git-commit-message`

**Trigger:** Use when about to write or finalize a git commit message — before running `git commit`.

---

## Design: Option C — Principles First, Checklist as Guardrail

### Step 1 — Repo Convention Detection

Before drafting, detect the repo's commit style:

1. Run `git log --oneline -20` and scan subject lines
2. If ≥50% use `type:` or `type(scope):` prefixes → **conventional commits mode**
3. If the repo has no commits yet → **conventional commits mode** (new repo default)
4. Otherwise → **match existing style** (extract the dominant pattern from recent commits)

This step runs once before any drafting.

---

### Step 2 — Core Principle: Why, Not What

Before drafting, ask: *"If someone reads only this commit message in 6 months with no other context, will they understand why this change existed?"*

Three questions to answer in the body for any non-trivial change:
1. What was the problem or gap before this change?
2. What does this commit do about it, and why this approach over alternatives?
3. Are there side effects, constraints, or follow-ups the reader should know?

The body is **not optional** when the change involves a decision, trade-off, or non-obvious fix. It *is* optional for purely mechanical changes (e.g., `chore: bump version to 2.2.0`).

---

### Step 3 — Subject Line Rules

- **Imperative mood**: completes "If applied, this commit will ___"
  - ✓ "Add Redis caching"
  - ✗ "Added Redis caching"
  - ✗ "Adding Redis caching"
- **50 characters target, 72 hard limit** — longer subjects get truncated in `git log`, GitHub, and most tooling
- **No banned vague words** without concrete detail: *fix, update, change, improve, misc, stuff, things, cleanup* — "fix null pointer in user auth" is fine; "fix bug" is not
- **No period at the end**
- **No "and"** — if you need "and", the commit likely covers two logical changes and should be split

---

### Step 4 — Commit Hygiene Check (secondary, non-blocking)

Before finalizing, scan the staged diff:

- If the diff touches **multiple unrelated areas** → flag: *"Consider splitting into separate commits — one per logical change."*
- If the subject contains **"and"** → same flag
- Advisory only — if the user wants to proceed with a combined commit, continue without blocking

---

### Step 5 — Pre-Finalization Checklist

- [ ] Subject is imperative mood
- [ ] Subject is ≤72 chars (≤50 preferred)
- [ ] Subject contains no banned vague words without concrete detail
- [ ] Subject has no trailing period
- [ ] Body is present for any non-trivial change
- [ ] Body explains *why*, not just *what*
- [ ] Body lines wrap at 72 chars
- [ ] Message follows detected repo convention (conventional commits or matched style)
- [ ] No "and" in subject (hygiene flag addressed or acknowledged)

---

## Decisions

- **Format-agnostic by default** — conventional commits applied contextually based on repo detection, not forced universally
- **Why > what** is the primary principle — all other rules serve it
- **Hygiene is advisory** — commit scope issues are flagged but never block message finalization
- **Body is required for non-trivial changes** — "trivial" means purely mechanical with no decision involved
