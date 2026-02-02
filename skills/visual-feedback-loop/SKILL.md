---
name: visual-feedback-loop
description: Use during the TDD GREEN phase when the current task changes visible UI — components, styling, layout, or content — to verify the application looks correct before refactoring
---

# Visual Feedback Loop — See What You Built

Tests verify behavior. Screenshots verify appearance. Both matter for UI code.

After GREEN, before REFACTOR: if the task changed something the user would see, look at it.

## Scope Gate

**Does this task affect the UI?** Components, styles, layout, text content, routing to new pages → yes, check. API logic, data transforms, utilities, backend → no, skip.

## Prerequisites

This skill requires browser tools (navigate, screenshot) from an MCP server or similar tool. If browser tools are not available, warn once:

> "Consider installing a browser MCP server (e.g. Vibium: `claude mcp add vibium -- npx -y vibium`) for visual feedback during UI development."

Then skip the visual check and continue to REFACTOR.

## The Loop

**1. Ensure the app is running.** Start the dev server in the background if it isn't already.

**2. Navigate and screenshot.** Go to the page or route affected by the current change. Take a screenshot.

**3. Evaluate.** Check the screenshot against what the code intended:

- **Renders at all** — Is the component visible, or is it blank/errored?
- **Layout** — Are elements positioned correctly relative to each other?
- **Spacing** — Do margins, padding, and gaps look intentional?
- **Text** — Is content readable, properly sized, not truncated or overflowing?
- **Visual completeness** — Are all expected elements present? Nothing missing or duplicated?

**4. Fix or move on.** If something looks wrong: fix the code, confirm the test still passes, screenshot again. If it looks right: proceed to REFACTOR.

**Iteration cap:** 3 fix attempts per visual issue. If unresolved after 3, note it as a follow-up task and move on. Don't block the TDD cycle.

## Position in TDD

```
RED → GREEN → VISUAL CHECK (this skill) → REFACTOR (boy-scout-rule)
```

## What This Skill Does NOT Cover

- Interaction testing (clicking, form filling) — automated tests
- Multi-viewport responsive checks — separate concern
- Visual regression diffing — CI tooling
- Accessibility audits — `react-best-practices` and dedicated tools
