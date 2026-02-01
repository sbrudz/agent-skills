# TypeScript-Specific Setup

Additional steps when the project uses TypeScript.

## ESLint packages

For non-framework projects (no Expo/Next.js), add `typescript-eslint` to the ESLint packages:

```
npm install --save-dev typescript-eslint
```

Framework configs like `eslint-config-expo` and `eslint-config-next` already include TypeScript rules.

## Type definitions

Install type definitions for the test runner so `tsc --noEmit` passes on test files:

| Runner | Package |
|--------|---------|
| Jest | `@types/jest` |
| Mocha | `@types/mocha` |

Vitest ships its own types — no extra package needed.

## CI: add type checking

Add `npx tsc --noEmit` as a CI step between `format:check` and the test runner.

## lint-staged: file extensions

Use `*.{ts,tsx}` patterns for lint-staged instead of `*.{js,jsx}`:

```json
{
  "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{js,json,md}": ["prettier --write"]
}
```

For mixed JS/TS codebases, combine: `"*.{js,jsx,ts,tsx}"`.

## Common lint fixes

After running `eslint --fix`, these TypeScript-specific errors typically require manual fixes:

- **Empty interfaces**: Convert `interface Foo extends Bar {}` to `type Foo = Bar`
- **Discriminated union narrowing in tests**: When removing `if` guards to satisfy `jest/no-conditional-expect`, TypeScript loses type narrowing. Fix with `Extract`:
  ```ts
  expect(result.status).toBe('ok');
  const ok = result as Extract<typeof result, { status: 'ok' }>;
  expect(ok.value).toBe(42);
  ```
- **Unused type imports**: Remove type-only imports that aren't referenced in runtime code
