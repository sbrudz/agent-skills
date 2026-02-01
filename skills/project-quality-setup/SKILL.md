---
name: project-quality-setup
description: Set up linting, formatting, git hooks, and CI for a project before starting implementation. Use after scaffolding a new project or when a project lacks ESLint, Prettier, Husky, or CI configuration. Triggers on keywords like "set up linting", "add formatting", "configure CI", "project quality", or when starting a new implementation and no lint/format config exists.
compatibility: Designed for Claude Code (or similar products). Requires Node.js and npm.
metadata:
  author: sbrudz
  version: "1.0"
---

# Project Quality Setup

Set up linting, formatting, git hooks, and CI **before** writing any implementation code. Clean tooling from the start prevents style debt and catches errors early.

## When to trigger

- After scaffolding a new project (e.g., `create-expo-app`, `create-next-app`, `npm init`)
- When starting implementation on a project that lacks lint/format configuration
- When the user asks to set up code quality tooling

## Step 1: Detect the tech stack

Examine `package.json`, framework config files, and project structure to determine:

- **Framework**: Expo/React Native, Next.js, plain React, Node.js, etc.
- **Language**: TypeScript or JavaScript
- **Test runner**: Jest, Vitest, etc.
- **Package manager**: npm, yarn, or pnpm

This determines which ESLint config and plugins to install.

## Step 2: ESLint

### Packages (devDependencies)

| Stack | Packages |
|-------|----------|
| Expo/React Native | `eslint`, `eslint-config-expo`, `eslint-config-prettier` |
| Next.js | `eslint`, `eslint-config-next`, `eslint-config-prettier` |
| React (Vite/CRA) | `eslint`, `eslint-plugin-react`, `eslint-plugin-react-hooks`, `@eslint/js`, `typescript-eslint`, `eslint-config-prettier` |
| Node.js | `eslint`, `@eslint/js`, `typescript-eslint`, `eslint-config-prettier` |

If Jest is the test runner, also add `eslint-plugin-jest`.

### Configuration

Create `eslint.config.js` using **ESLint 9 flat config** format:

```js
// Example for Expo
const expoConfig = require('eslint-config-expo/flat');
const prettierConfig = require('eslint-config-prettier');

module.exports = [
  ...expoConfig,
  prettierConfig,
  {
    ignores: ['node_modules/', 'dist/', 'coverage/', '*.config.js'],
  },
];
```

Add Jest plugin config if applicable:

```js
const jestPlugin = require('eslint-plugin-jest');

// Add to the config array:
{
  files: ['**/*.test.{ts,tsx}', '**/__tests__/**/*.{ts,tsx}'],
  ...jestPlugin.configs['flat/recommended'],
},
```

### Scripts

Add to `package.json`:

```json
"lint": "eslint .",
"lint:fix": "eslint . --fix"
```

### Fix existing issues

Run `npm run lint:fix` then manually resolve remaining errors. Common fixes:

- **Unused variables**: Remove or prefix with `_`
- **Unescaped entities in JSX**: Use `&apos;`, `&quot;`, or curly-brace expressions
- **Conditional expects in tests**: Restructure so `expect` calls are unconditional; use type assertions after runtime assertions for discriminated unions
- **Empty interfaces**: Convert to type aliases

## Step 3: Prettier

### Packages

```
npm install --save-dev prettier
```

### Configuration

Create `.prettierrc`:

```json
{
  "singleQuote": true,
  "trailingComma": "all",
  "semi": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

Adjust to match the project's existing code style if there is one.

Create `.prettierignore`:

```
node_modules/
.expo/
dist/
coverage/
*.lock
```

### Scripts

Add to `package.json`:

```json
"format": "prettier --write \"src/**/*.{ts,tsx}\" \"app/**/*.{ts,tsx}\" \"*.{js,json}\"",
"format:check": "prettier --check \"src/**/*.{ts,tsx}\" \"app/**/*.{ts,tsx}\" \"*.{js,json}\""
```

Adjust glob patterns to match the project's source directories.

### Format all files

Run `npm run format` to apply consistent formatting.

## Step 4: Husky + lint-staged

### Packages

```
npm install --save-dev husky lint-staged
```

### Setup

```
npx husky init
```

This creates `.husky/pre-commit` and adds a `prepare` script to `package.json`.

Replace `.husky/pre-commit` contents with:

```
npx lint-staged
```

Create `.lintstagedrc.json`:

```json
{
  "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{js,json,md}": ["prettier --write"]
}
```

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
      - run: npx tsc --noEmit
      - run: npx jest --ci --coverage
```

Adjust the test command if the project uses a different runner (e.g., `vitest`). Remove `tsc --noEmit` if the project is plain JavaScript.

## Step 6: Install missing type packages

If TypeScript is used, ensure type definitions are installed for the test runner:

```
npm install --save-dev @types/jest
```

## Verification checklist

Run each command and confirm it exits with code 0:

1. `npm run lint` — no lint errors
2. `npm run format:check` — all files formatted
3. `npx tsc --noEmit` — no type errors (TypeScript projects only)
4. `npx jest --ci` — all tests pass
5. Make a test commit to verify the pre-commit hook runs lint-staged
