---
name: ux-prototyping
description: Use after designing a UI feature when the design involves novel interactions, complex multi-step flows, or layouts where visual balance matters — to build a throwaway HTML prototype for user validation before implementation
---

# UX Prototyping — Validate Before You Build

After design, before implementation: build a quick throwaway prototype to validate the design visually with the user. Catches layout and hierarchy problems before they become production code.

## Threshold Gate

After the design phase completes and the design doc is written, check — does any of the following apply?

- Novel interaction pattern the user hasn't seen before
- Complex multi-step flow (wizard, onboarding, multi-page form)
- Layout where visual balance and hierarchy are central to success
- The user expressed uncertainty about how the design will look or feel

If yes → suggest prototyping. If none apply → proceed to implementation. The user can always request or decline a prototype.

```
Design (ux-design-principles) → PROTOTYPE (this skill) → Plan → Implement
```

## The Loop

**1. Build a throwaway HTML file.** Single `.html` file with inline CSS. No framework, no build step, no JavaScript unless essential. Use placeholder content, approximate colors, rough layout. Speed over quality — this is not production code.

**2. Screenshot and show the user.** Open the file in the browser with available browser tools. Take a screenshot and present it. Explain what you're showing and what feedback you need: "Here's the rough layout for step 2. Does this hierarchy feel right?"

**3. Iterate on feedback.** User responds in natural language. Update the HTML, re-screenshot, present again. Change one or two things per iteration, not a full redesign.

**4. Converge or go back.** When the user is satisfied:
- Capture key design decisions in the design document
- Save screenshots of the accepted prototype to `docs/plans/` alongside the design doc
- Delete the HTML file — nothing carries into production code

If the user isn't satisfied after several iterations, the requirements need more design work, not more prototyping. Go back to `ux-design-principles`.

## What the Prototype Should Capture

- Layout and spatial relationships
- Visual hierarchy (what stands out)
- Flow structure (what comes first, second, third)

## What the Prototype Should NOT Capture

- Final styling (exact colors, fonts, pixel-perfect spacing)
- Real data or API integration
- Interactive behavior beyond basic structure
- Design system components — that's implementation work

## Related Skills

- **Prerequisite:** `ux-design-principles` (design thinking must precede prototyping)
- **Next:** implementation planning → `visual-feedback-loop` (verify the production implementation matches the approved prototype)
