---
name: ux-design-principles
description: Use when planning or designing features that involve user-facing UI, or before writing code for any new user-facing feature — pages, components, flows, or interactions — to apply user-centered design thinking before implementation begins
---

# UX Design Principles — Design for Users, Not Features

Companion to feature planning and design for UI features. Injects user-centered thinking into design decisions before any code is written.

## Scope Gate

Is this feature user-facing? Pages, components, flows, interactions → apply. Infrastructure, APIs, data pipelines, backend-only logic → skip.

## During Planning: Ask These First

Before technical questions (stack, architecture, data model), establish the user context. These questions come from Goal-Directed Design (Cooper):

- **Who is the primary user?** Just enough to anchor decisions. "Admin managing a team" and "end user checking status" lead to different interfaces. If multiple user types, which one is this feature primarily for?
- **What is their goal?** Goals are outcomes, not tasks. "Feel confident the deploy is safe" not "click the deploy button." This drives what to surface, hide, and emphasize.
- **What's their context?** Rushed or careful? Frequent or first-time? Mobile or desktop? High-stakes + infrequent = add confirmation. Low-stakes + frequent = minimize clicks.
- **What do they already expect?** Mental models from similar tools. If every competitor puts navigation on the left, putting it on the bottom needs a strong reason.

## During Approach Evaluation: UX Lens

When comparing 2-3 approaches, evaluate each against the user's goal — not just technical trade-offs. The approach that gets the user to their goal with the least confusion wins, even if it's technically simpler. Ask: "Would [user type] trying to [goal] find this confusing?"

## Design Principles to Apply

- **Reduce before you design.** Can the user achieve their goal with fewer steps, fields, or options? What's the simplest version that solves the primary goal? Progressive disclosure: show what's needed now, hide the rest.
- **Structure by scanning priority.** Users scan, they don't read. What does the user need first? What's secondary? What's rare? The primary goal drives the primary content area.
- **Match user expectations.** Favor designs that work like tools the user already knows. Surprising users costs more than surprising developers.
- **Prevent errors, don't just handle them.** Constrain inputs (date picker over text field), set smart defaults, confirm destructive actions. This is a design decision, not an implementation detail.

## In the Design Document

Include a UX rationale section: who the user is, what their goal is, and which principles drove the key design decisions. This gives implementers context for judgment calls during coding.

## What This Skill Does NOT Cover

- Visual design (spacing, color, hierarchy) — `ux-visual-evaluation`
- Accessibility implementation — `react-best-practices`
- Prototyping workflow — `ux-prototyping`

## Related Skills

- **Next (complex UI):** `ux-prototyping` (when design involves novel interactions, complex flows, or visual-balance-critical layouts — prototype before implementing)
- **Next (standard UI):** proceed to implementation → `visual-feedback-loop` (verify the implementation visually)
- **Pairs with:** `domain-driven-design` (ubiquitous language should flow through to UI labels)
