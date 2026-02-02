---
name: react-best-practices
description: Use when reviewing React component code during code quality review, when the diff contains .tsx or .jsx files, or when reviewing components that use React hooks, state management, or data fetching patterns
---

# React Best Practices for Code Review

Supplement to the standard code review checklist. Covers judgment calls that linters and static analysis cannot catch.

## When to Use

During code review (`superpowers:code-reviewer`) when the diff contains React code (`.tsx`, `.jsx`, or `.ts` files importing from `"react"`).

Apply these checks **after** the standard code quality review, as an additional pass.

## Review Checklist

Check each section below. Flag violations as Important or Minor per the standard review severity levels.

### 1. Component Responsibility & Size

A component is too large when it mixes concerns, not when it exceeds a line count.

**Flag when a single component does more than one of:**
- Renders UI (view layer)
- Contains business logic (data transformation, validation, calculations)
- Manages complex state interactions (multiple related `useState` + `useEffect`)
- Fetches data

**The fix pattern:**
- **View logic** stays in the component (JSX, conditional rendering, layout)
- **Business logic** moves to pure functions (sorting, filtering, formatting, validation). Pure functions are trivially testable without rendering.
- **Complex state + effects** move to custom hooks (`useOrders`, `useAuth`, `useSettings`). A hook is "complex" when it combines multiple `useState` calls that interact with each other or with `useEffect`.

```tsx
// BAD: all mixed in one component
function Dashboard() {
  const [orders, setOrders] = useState([]);
  const [sorted, setSorted] = useState([]);
  useEffect(() => { fetch(/*...*/) }, []);
  useEffect(() => { setSorted(orders.sort(/*...*/)) }, [orders]);
  const formatPrice = (n: number) => /*...*/;
  return <table>...</table>;
}

// GOOD: separated by responsibility
function Dashboard() {
  const { orders, sort, sortField } = useOrders();  // custom hook: state + fetching
  return <OrdersTable orders={orders} onSort={sort} sortField={sortField} />;
}
// sortOrders(), formatPrice() are pure functions in a utils file
```

### 2. useEffect Misuse

Linters catch missing dependencies. They **cannot** catch unnecessary effects.

**Flag these patterns:**

| Pattern | Fix |
|---|---|
| Effect computes derived state (`useEffect` + `setState` from other state) | Compute during render or `useMemo` |
| Effect resets state when a prop changes | Use `key` on the component instead |
| Chain of effects (A sets state, triggers B, triggers C) | Do the work in one event handler |
| User-driven side effect in `useEffect` instead of event handler | Move to the handler that caused it |
| Effect without cleanup for subscriptions, timers, or fetch | Add cleanup function with `AbortController` |

`useEffect` is ONLY for synchronizing with external systems (subscriptions, timers, DOM manipulation, third-party widgets).

### 3. React Version-Appropriate Patterns

Check `package.json` for the React version. Review for patterns appropriate to that version.

**React 19+ apps should use:**

| Instead of | Use |
|---|---|
| Manual `loading`/`error`/`data` state for fetches | `<Suspense>` boundaries + Server Components for data fetching |
| `onSubmit` + `useState` for form submission state | `useActionState` for form action + state, `useFormStatus` for pending UI |
| `useEffect` to resolve promises | `use()` hook |
| Defensive `React.memo`, `useMemo`, `useCallback` | React Compiler handles memoization automatically. Only add manual memoization when a third-party library requires stable identity, or as an explicit `useEffect` dependency. |

**`useActionState` signature reminder:** `(prevState, formData) => newState` — first arg is previous state, not formData. Imported from `"react"`, not `"react-dom"`.

**`useFormStatus` rule:** Must be called from a child component rendered inside the `<form>`, not in the same component that renders the form.

### 4. Accessibility Beyond Linting

`eslint-plugin-jsx-a11y` catches static markup issues. These behavioral issues require judgment:

**Focus management:**
- Modal/dialog: trap focus inside, return focus to trigger on close
- Route changes in SPAs: announce new page to screen readers
- Form errors: move focus to error summary or first invalid field
- Success/error messages: use `role="alert"` or `aria-live="polite"` so screen readers announce them

**Keyboard navigation:**
- Every interactive element must work with keyboard (Tab, Enter, Space, Escape, Arrow keys)
- `<div onClick>` is never a button — use `<button>` (linter catches some, not all)
- Custom sort controls, dropdowns, tabs need keyboard handlers

**Color:**
- Status indicators (error, success, pending) must not rely on color alone — add icons, text labels, or patterns

### 5. Testing Practices

**Query priority** (most to least preferred):
1. `getByRole` — validates accessibility at the same time
2. `getByLabelText` — best for form fields
3. `getByText` — for non-interactive content
4. `getByTestId` — last resort only

**Interaction:**
- Use `userEvent` (simulates real user behavior: focus, keyboard, hover) not `fireEvent` (dispatches a single DOM event)

**What to test:**
- What the user sees and does — rendered output, interaction results, accessible names
- NOT implementation details — internal state, hook calls, re-render counts, component instance methods

**Mocking:**
- Mock at the **network boundary** with MSW (Mock Service Worker), not by replacing `global.fetch` or mocking component imports
- If you're testing mock behavior instead of real behavior, the test is wrong
