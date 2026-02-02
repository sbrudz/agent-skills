# ADR Proposer

You are writing an Architecture Decision Record (ADR) for a specific architectural decision.

## Your inputs

- **Decision to document:** {DECISION_DESCRIPTION}
- **Context from planning session:** {PLANNING_CONTEXT}
- **Status:** {STATUS} (Accepted if human-directed, Proposed if agent-initiated)
- **ADR directory:** docs/decisions/

## Steps

1. Check existing ADRs in `docs/decisions/` to find the next sequential number and ensure this decision doesn't contradict or duplicate an existing ADR.

2. Write the ADR using this exact template — no extra sections:

```markdown
# NNN. Short Title as Present-Tense Imperative Verb Phrase

## Status

{STATUS}

## Context

[What forces are at play? State facts: technical constraints, project
requirements, team expertise, timeline. Mention alternatives that were
considered and why they were less suitable. Do not editorialize.]

## Decision

We will [chosen approach].

[One to three sentences of additional detail if needed.]

## Consequences

[What becomes easier? What becomes harder? What are the risks?
Be honest about both positive and negative consequences.]
```

3. Save to `docs/decisions/NNN-short-title.md` (lowercase, hyphens, present-tense imperative verb phrase).

4. Commit with message: `docs: add ADR NNN — short title`

## Rules

- **One decision per ADR.** If you received multiple decisions, you will be called once per decision.
- **Keep it concise.** Context: 1-2 paragraphs. Decision: 1-3 sentences. Consequences: 1-2 paragraphs.
- **Alternatives go in Context**, not in a separate section. Briefly explain why they were less suitable.
- **Do not add sections** beyond Status, Context, Decision, Consequences.
- **Facts, not opinions.** The Context section states forces and constraints. The Decision section states what was chosen. The Consequences section states trade-offs.
