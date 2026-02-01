# Node.js / TypeScript

## Contents

- Linter (ESLint)
- Formatter (Prettier)
- Pre-commit hook (Husky + lint-staged)
- CI workflow
- TypeScript-specific additions

## Linter: ESLint

Install ESLint 9 with the appropriate framework config and `eslint-config-prettier`:

| Framework | Config package |
|-----------|---------------|
| Expo / React Native | `eslint-config-expo` |
| Next.js | `eslint-config-next` |
| React (Vite, CRA) | `@eslint/js` + `eslint-plugin-react` + `eslint-plugin-react-hooks` |
| Node.js (no framework) | `@eslint/js` |

For TypeScript without a framework config that includes TS rules, also add `typescript-eslint`.

If Jest is the test runner, add `eslint-plugin-jest`.

Create `eslint.config.js` using flat config format. Spread the framework config, add `eslint-config-prettier` last, add an `ignores` block for `node_modules/`, `dist/`, `coverage/`, and config files.

Add scripts to `package.json`:

```json
"lint": "eslint .",
"lint:fix": "eslint . --fix"
```

Run `lint:fix`, then manually resolve remaining errors.

## Formatter: Prettier

Install `prettier`. Create `.prettierrc` by inferring style from existing code (quote style, trailing commas, semicolons, line width, indentation). Create `.prettierignore` for build output, `node_modules/`, and lockfiles.

Add scripts:

```json
"format": "prettier --write \"src/**/*.{js,jsx,ts,tsx}\" \"*.{js,json}\"",
"format:check": "prettier --check \"src/**/*.{js,jsx,ts,tsx}\" \"*.{js,json}\""
```

Adjust glob patterns to match the project's source directories and file extensions.

Run `format` to apply to all source files.

## Pre-commit hook: Husky + lint-staged

```
npm install --save-dev husky lint-staged
npx husky init
```

Replace `.husky/pre-commit` contents with `npx lint-staged`.

Create `.lintstagedrc.json`. Map source extensions to `eslint --fix` + `prettier --write`, and config/doc files to `prettier --write` only:

```json
{
  "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{json,md}": ["prettier --write"]
}
```

Narrow extensions to match the project (JS-only, TS-only, or both).

## CI workflow

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

Adapt: use `yarn`/`pnpm` if that's the project's package manager. Adjust the test command to match the runner.

## TypeScript additions

These apply only when the project uses TypeScript.

**Type definitions for test runner**: Install `@types/jest` (or `@types/mocha`). Vitest ships its own types.

**Type checking in CI**: Add `npx tsc --noEmit` as a step between `format:check` and `test`.

**Common TS-specific lint fixes**:
- Convert empty interfaces (`interface Foo extends Bar {}`) to type aliases (`type Foo = Bar`)
- After making `expect` calls unconditional (for `jest/no-conditional-expect`), restore type narrowing with `Extract`:
  ```ts
  expect(result.status).toBe('ok');
  const ok = result as Extract<typeof result, { status: 'ok' }>;
  ```
- Remove unused type-only imports
