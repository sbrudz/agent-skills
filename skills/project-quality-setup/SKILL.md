---
name: project-quality-setup
description: Configures ESLint, Prettier, Husky with lint-staged, and GitHub Actions CI for Node.js projects. Detects the tech stack (Expo, Next.js, React, Node) and adapts accordingly. Triggers after project scaffolding, before implementation begins, or when a project lacks linting/formatting configuration.
compatibility: Designed for Claude Code (or similar products). Requires Node.js.
metadata:
  author: sbrudz
  version: "2.0"
---

# Project Quality Setup

Configure linting, formatting, git hooks, and CI **before** writing implementation code.

## When to trigger

- After scaffolding a new project
- Before starting implementation on a project without lint/format config
- When the user asks to set up code quality tooling

## Progress checklist

Copy and track progress:

```
- [ ] Detect tech stack
- [ ] ESLint: install, configure, fix issues
- [ ] Prettier: install, configure, format files
- [ ] Husky + lint-staged: install, configure hooks
- [ ] GitHub Actions CI: create workflow
- [ ] Verify all checks pass
```

## Step 1: Detect the tech stack

Read `package.json` and project config files. Determine:

- **Framework**: Expo/React Native, Next.js, React, Node.js
- **Language**: TypeScript or JavaScript
- **Test runner**: Jest, Vitest, or other
- **Package manager**: npm, yarn, or pnpm

**If TypeScript is detected**, read [references/typescript.md](references/typescript.md) for additional steps that apply throughout this workflow.

## Step 2: ESLint

Install ESLint 9 with the appropriate framework config and `eslint-config-prettier`:

| Stack | Config package |
|-------|---------------|
| Expo/React Native | `eslint-config-expo` |
| Next.js | `eslint-config-next` |
| React (Vite/CRA) | `@eslint/js` + `eslint-plugin-react` + `eslint-plugin-react-hooks` |
| Node.js | `@eslint/js` |

If Jest is the test runner, also add `eslint-plugin-jest`.

Create `eslint.config.js` using flat config format. Spread the framework config, add `eslint-config-prettier` last, and add an `ignores` entry for `node_modules/`, `dist/`, `coverage/`, and config files.

Add scripts: `"lint": "eslint ."` and `"lint:fix": "eslint . --fix"`.

Run `lint:fix`, then manually resolve remaining errors. Common fixes:
- Remove unused variables or prefix with `_`
- Escape special characters in JSX (`&apos;`, `&quot;`)
- Restructure conditional `expect` calls in tests to be unconditional

## Step 3: Prettier

Install `prettier`. Create `.prettierrc` by inferring style from existing code (quote style, trailing commas, semicolons, line width, indentation). Create `.prettierignore` for build artifacts and lockfiles.

Add scripts: `"format": "prettier --write ..."` and `"format:check": "prettier --check ..."` with glob patterns matching the project's source directories.

Run `format` to apply consistent formatting to all source files.

## Step 4: Husky + lint-staged

```
npm install --save-dev husky lint-staged
npx husky init
```

Replace `.husky/pre-commit` contents with `npx lint-staged`.

Create `.lintstagedrc.json` mapping source file extensions to `eslint --fix` + `prettier --write`, and config/doc files to `prettier --write` only. Match the file extensions to the project's language (`.js`/`.jsx` for JavaScript, `.ts`/`.tsx` for TypeScript, or both).

## Step 5: GitHub Actions CI

Create `.github/workflows/ci.yml`:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check
      - run: npm test
```

Adapt: use `yarn`/`pnpm` if that's the project's package manager. Add `npx tsc --noEmit` for TypeScript projects. Adjust the test command to match the project's runner.

## Step 6: Verify

Run each and confirm exit code 0:

1. `npm run lint`
2. `npm run format:check`
3. Test suite passes
4. Make a test commit to confirm the pre-commit hook runs lint-staged
