---
name: ux-visual-evaluation
description: Use after visual-feedback-loop confirms basic correctness, or when UI changes are complete and a screenshot is available, to evaluate screenshots for visual design quality — hierarchy, whitespace, affordances, and consistency
---

# UX Visual Evaluation — Does It Look Good and Feel Usable?

Second pass after `visual-feedback-loop` confirms the UI renders correctly. Same screenshot, deeper evaluation. Drawn from Refactoring UI and Nielsen's usability heuristics.

## When to Run

**After visual-feedback-loop:** When visual-feedback-loop's 5-item check passes. Uses the existing screenshot — don't take a new one.

**Independent:** When UI changes are complete and a screenshot is available, even if visual-feedback-loop was not run. Take or request a screenshot, then evaluate.

If the task is non-UI and no screenshot is available → skip.

```
Implement → Tests Pass → basic visual check (visual-feedback-loop) → UX evaluation (this skill) → Refactor
```

## Visual Design Criteria

Evaluate the screenshot for:

- **Visual hierarchy** — Does the most important element stand out? Primary actions: high-contrast solid buttons. Secondary actions: outline or lower contrast. Supporting text: lighter color, not just smaller. If everything looks equally prominent, nothing guides the user's eye.
- **Whitespace** — Generous breathing room? More space between groups than within them. Use whitespace to create separation instead of borders. Too much space is better than too little.
- **Spacing consistency** — Do margins, padding, and gaps follow a consistent scale? Look for one section with tight padding next to another with loose padding. Same-level elements should have the same spacing.
- **Color usage** — Is color strategic, not decorative? Primary actions should have the strongest color. Status indicators (success, error, warning) should use distinct, conventional colors. Text on colored backgrounds needs sufficient contrast.
- **Borders vs. alternatives** — Are borders overused? Prefer background color changes, subtle shadows, or increased whitespace. Borders make interfaces look busy.

## Usability Criteria

- **Affordances** — Do interactive elements look interactive? Buttons should look like buttons, links like links. If you can't tell what's clickable from the screenshot, neither can the user.
- **System status** — Does the UI show where the user is and what's happening? Look for: highlighted nav items, empty state guidance, loading indicators, selected/active states.
- **Consistency** — Does this screen match the rest of the app? Same button styles, heading sizes, spacing patterns. New components should feel like they belong alongside existing ones.

## Iteration

Same as visual-feedback-loop: fix, confirm test passes, re-evaluate. 3-attempt cap per issue — if unresolved, note as follow-up and proceed to refactoring.

## What This Skill Does NOT Cover

- Whether the UI renders correctly — `visual-feedback-loop`
- Design decisions (who is the user, what's their goal) — `ux-design-principles`
- Accessibility audits — `react-best-practices` and dedicated tools

## Related Skills

- **Prerequisite:** `visual-feedback-loop` (basic correctness check before design evaluation), `ux-design-principles` (design rationale informs evaluation criteria)
- **Next:** `boy-scout-rule` (refactoring after visual verification is complete)
