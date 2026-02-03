---
name: functional-core-imperative-shell
description: Use when reviewing code that mixes business logic with I/O, database calls, or side effects, or when tests require extensive mocking to verify logic
---

# Functional Core, Imperative Shell — Code Review Checklist

Detect code that tangles business logic with side effects. The fix is always the same: **push decisions into pure functions (the core), confine I/O to a thin orchestration layer (the shell).**

## The Litmus Test

**Can you test this function's business logic without mocking anything?**

If the answer is no, the function mixes core and shell. Every mock in a test is evidence of a missing boundary.

## When to Use

During code review on any codebase. Language-agnostic.

Apply as an additional pass after the standard review. Flag violations as Important.

## 1. Impure Business Logic

Business logic functions that perform I/O. The most common violation.

**Flag when a function both:**
- Makes a decision (branching, validation, calculation, transformation)
- AND performs I/O (database query, API call, file read/write, network request)

**Signals:**
- Function validates input, then queries a database, then calculates based on the result — all in one body
- Calculation depends on a value fetched mid-function (e.g., fetching a discount rule then applying it)
- Function determines what action to take AND executes that action

**The pattern:** The shell gathers inputs (I/O), passes them to the core (pure), then acts on the result (I/O).

```
// BAD: decision + I/O tangled
function processOrder(orderId) {
  order = db.getOrder(orderId)              // I/O
  if (order.total > 100)                    // decision
    db.applyDiscount(orderId, order.total * 0.1)  // I/O
}

// GOOD: separated
function calculateDiscount(order) {         // pure core
  if (order.total > 100) return order.total * 0.1
  return 0
}
// shell: order = db.get() → discount = calculateDiscount(order) → db.apply(discount)
```

## 2. Fat Shells

The shell should be a flat sequence: **gather → decide → act**. No branching, no transformation.

**Flag when the shell contains:**
- `if`/`else` or `switch` that determines behavior (not just dispatching on a core return value)
- Data transformation, mapping, or filtering
- Validation logic
- Multiple sequential decisions interleaved with I/O (read → decide → write → read → decide → write)

**Dispatching is OK:** `if (result.notify) sendEmail()` is fine — the shell executes the core's decision. Flag when the shell *makes* the decision.

## 3. Hidden Side Effects in the Core

Functions that look pure but aren't. Subtle — easy to miss in review.

**Flag these in any function that should be pure:**

| Hidden side effect | Why it breaks purity | Fix |
|---|---|---|
| Logging (`logger.info`, `console.log`) | I/O operation | Return diagnostic data; let the shell log |
| Current time (`new Date()`, `Date.now()`) | Non-deterministic input | Accept timestamp as parameter |
| Randomness (`Math.random()`, `uuid()`) | Non-deterministic input | Accept seed/value as parameter |
| Environment variables (`process.env`) | Implicit external input | Accept as parameter |
| Global/module-level mutable state | Shared state mutation | Return new values; let the shell persist |
| Throwing exceptions for control flow | Forces caller into try/catch | Return result/error values |

**The test:** Given the same arguments, does this function always return the same result with no observable effect on the outside world?

## Severity Guide

- **Impure business logic** (Section 1): Important — core architectural issue, causes mock-heavy tests and tangled concerns
- **Fat shell** (Section 2): Important when the shell contains non-trivial logic; Minor for simple dispatch branching
- **Hidden side effects** (Section 3): Important for non-determinism (`Date`, `random`) and mutable state; Minor for logging in small functions
