---
name: project-quality-setup
description: Configures linting, formatting, pre-commit hooks, and CI for a project before implementation begins. Detects the tech stack and applies the appropriate tools. Triggers after scaffolding a new project, when a project lacks quality tooling, or when the user asks to set up linting, formatting, CI, or code quality.
compatibility: Designed for Claude Code (or similar products).
metadata:
  author: sbrudz
  version: "3.0"
---

# Project Quality Setup

Establishes linting, formatting, pre-commit hooks, and CI **before** writing implementation code.

## When to trigger

- After scaffolding a new project
- Before starting implementation on a project without quality tooling
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
