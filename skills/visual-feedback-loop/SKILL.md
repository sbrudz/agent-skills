---
name: visual-feedback-loop
description: Use after implementing a UI change or before committing UI changes to visually verify the application looks correct — applies when the current task changes visible UI (components, styling, layout, or content)
---

# Visual Feedback Loop — See What You Built

Tests verify behavior. Screenshots verify appearance. Both matter for UI code.

After implementing a change and tests pass: if the task changed something the user would see, look at it.

## Scope Gate

**Does this task affect the UI?** Components, styles, layout, text content, routing to new pages → yes, check. API logic, data transforms, utilities, backend → no, skip.

## Prerequisites

This skill requires browser tools (navigate, screenshot) from an MCP server or similar tool. If browser tools are not available, warn once:

> "Consider installing a browser automation tool (e.g. Puppeteer, Chrome DevTools MCP server) for visual feedback during UI development."

Then skip the visual check and continue to refactoring.

## The Loop

**1. Ensure the app is running.** Start the dev server in the background if it isn't already.

**2. Navigate and screenshot.** Go to the page or route affected by the current change. Take a screenshot.

**3. Evaluate.** Check the screenshot against what the code intended:

- **Renders at all** — Is the component visible, or is it blank/errored?
- **Layout** — Are elements positioned correctly relative to each other?
- **Spacing** — Do margins, padding, and gaps look intentional?
- **Text** — Is content readable, properly sized, not truncated or overflowing?
- **Visual completeness** — Are all expected elements present? Nothing missing or duplicated?

**4. Fix or move on.** If something looks wrong: fix the code, confirm the test still passes, screenshot again. If it looks right: apply `ux-visual-evaluation` for design quality, then proceed to refactoring.

**Iteration cap:** 3 fix attempts per visual issue. If unresolved after 3, note it as a follow-up task and move on. Don't block the development cycle.

## Position in Development Workflow

```
Implement → Tests Pass → VISUAL CHECK (this skill) → UX EVALUATION (ux-visual-evaluation) → REFACTOR (boy-scout-rule)
```

## What This Skill Does NOT Cover

- Interaction testing (clicking, form filling) — automated tests
- Multi-viewport responsive checks — separate concern
- Visual regression diffing — CI tooling
- Accessibility audits — `react-best-practices` and dedicated tools

## Related Skills

- **Prerequisite:** `ux-design-principles` (design thinking should inform what "correct" looks like)
- **Next:** `ux-visual-evaluation` (design quality evaluation after basic correctness passes) → `boy-scout-rule` (refactoring after visual verification)
