---
name: project-quality-setup
description: Use when a project lacks linting, formatting, pre-commit hooks, or CI. Must be completed before executing any implementation plan (superpowers:executing-plans, superpowers:subagent-driven-development). Also triggers after scaffolding a new project or when the user asks to set up code quality tooling.
compatibility: Works with any AI coding assistant.
metadata:
  author: sbrudz
  version: "3.2"
---

# Project Quality Setup

Establishes linting, formatting, pre-commit hooks, and CI **before** writing implementation code.

## Ordering requirement

**This skill must complete before any feature implementation.** If you are about to use superpowers:executing-plans or superpowers:subagent-driven-development, first check whether the project has:

- A linter configured and passing
- A formatter configured and passing
- A pre-commit hook
- A CI workflow

If any are missing, complete this skill first. Do not implement features on a project without quality gates.

### No tech stack yet?

If the project directory has no tech stack indicators (`package.json`, `go.mod`, `Gemfile`, `Cargo.toml`, etc.), the plan likely includes a scaffolding task (e.g., `npx create-next-app`, `rails new`, `cargo init`).

In this case:

1. Execute **only** the scaffolding task from the plan
2. Stop before executing any feature tasks
3. Run this skill to set up quality tooling on the newly scaffolded project
4. Resume the remaining plan tasks

Do not skip quality setup because the tech stack doesn't exist yet. Defer it until after scaffolding, then complete it before feature work begins.

## When to trigger

- Before executing feature tasks in an implementation plan
- Immediately after scaffolding a new project (before any feature work)
- When the user asks to set up linting, formatting, or CI

## Progress checklist

Copy and track progress:

```
- [ ] Detect tech stack
- [ ] Linter: install, configure, fix existing issues
- [ ] Formatter: install, configure, format all files
- [ ] Pre-commit hook: run linter + formatter on staged files
- [ ] CI workflow: lint, format check, type check (if applicable), tests
- [ ] Verify all checks pass
```

## Step 1: Detect the tech stack

Examine the project root for language and framework indicators (`package.json`, `go.mod`, `Gemfile`, `Cargo.toml`, etc.). Then read the matching reference file for stack-specific tools and configuration:

| Stack | Reference |
|-------|-----------|
| Node.js / TypeScript (Expo, Next.js, React, etc.) | [references/nodejs.md](references/nodejs.md) |
| Go | [references/golang.md](references/golang.md) |
| Ruby / Rails | [references/ruby.md](references/ruby.md) |
| Rust | [references/rust.md](references/rust.md) |

**Follow the reference file for all remaining steps.** The steps below describe the goals each reference file implements.

## Step 2: Linter

Install and configure the ecosystem's standard linter. Add a `lint` command that can be run locally and in CI. Run the auto-fixer, then manually resolve remaining issues.

## Step 3: Formatter

Install and configure the ecosystem's standard formatter. Add a `format` command and a `format:check` command (for CI). Run the formatter on all existing source files.

## Step 4: Pre-commit hook

Configure a pre-commit hook that runs the linter and formatter on staged files. This prevents unformatted or failing code from being committed.

## Step 5: CI workflow

Create a GitHub Actions workflow (`.github/workflows/ci.yml`) triggered on push to `main` and on pull requests. The workflow should:

1. Install dependencies
2. Run the linter
3. Run the format check
4. Run type checking (if the language has a separate type checker)
5. Run the test suite

## Step 6: Verify

Confirm all checks pass locally:

1. Lint command exits 0
2. Format check exits 0
3. Test suite passes
4. A test commit triggers the pre-commit hook
