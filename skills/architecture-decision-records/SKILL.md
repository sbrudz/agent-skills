---
name: architecture-decision-records
description: Use when making architectural decisions during planning or brainstorming sessions, when choosing between technologies, patterns, or system designs that affect multiple components or are hard to reverse
---

# Architecture Decision Records

Capture significant architectural decisions as lightweight documents during planning. Uses Michael Nygard's ADR template with a two-subagent workflow (propose → review).

## When to Use

During `superpowers:brainstorming` or `superpowers:writing-plans`, when architectural decisions are being made. Create ADRs **after** the planning conversation concludes, before transitioning to implementation.

Do NOT interrupt the planning flow to write ADRs. Collect qualifying decisions as they emerge, then batch-create ADRs at the end.

## Threshold Gate

Apply this checklist to each decision. **If 2 or more are yes → write an ADR.**

- [ ] Does it affect multiple components or services?
- [ ] Does it constrain future technical choices?
- [ ] Does it involve choosing between meaningfully different alternatives?
- [ ] Would it be difficult or costly to reverse?

**NOT worth an ADR:** utility library choices, naming conventions, code style, implementation details within a single module, anything already decided by an existing ADR.

The line: **ADRs capture decisions that shape the system's structure, not decisions that shape a single file.**

## Template (Michael Nygard)

Store in `docs/decisions/NNN-short-title.md`. Number sequentially (`001`, `002`, ...). Title uses present-tense imperative verb phrase (e.g., `use-postgres-for-persistence`).

```markdown
# NNN. Short Title as Present-Tense Imperative Verb Phrase

## Status

Proposed | Accepted | Deprecated | Superseded by [NNN]

## Context

What is the issue? What forces are at play? State facts and constraints,
not opinions. Include technical constraints, project requirements, and
team factors.

## Decision

We will [chosen approach].

## Consequences

What becomes easier or harder? Be honest — include both positive and
negative consequences.
```

Keep it to these four sections. Do not add extra sections like "Alternatives Considered" or "Deciders" — alternatives belong in Context, and the git log records who decided.

## Status Rules

- **Human-directed decisions** (the human explicitly chose during the session): Status = `Accepted`. The human already decided; the ADR documents it.
- **Agent-initiated decisions** (the agent made an architectural choice not explicitly discussed with the human): Status = `Proposed`. Surface to human for approval before implementation proceeds.

## Workflow

### 1. Collect decisions during planning

As architectural choices emerge during brainstorming or plan writing, note which ones cross the threshold. Track whether each was human-directed or agent-initiated.

### 2. Dispatch proposer subagent (one per decision)

Use the prompt template in `proposer-prompt.md`. The proposer:
- Checks existing ADRs in `docs/decisions/` to determine the next number and avoid contradictions
- Writes the ADR using the Nygard template
- Sets status per the rules above
- Saves the file and commits

### 3. Dispatch reviewer subagent

Use the prompt template in `reviewer-prompt.md`. The reviewer checks:
- Is the Context factual and complete?
- Is the Decision stated clearly?
- Are Consequences honest (both positive AND negative)?
- Does this actually warrant an ADR (threshold re-check)?
- Does it contradict existing ADRs?

Reports: `Approved` or `Issues` with specific feedback.

### 4. Loop if needed

If the reviewer flags issues, the proposer revises and the reviewer re-reviews.

### 5. Updating existing ADRs

If a later session revisits a decision, don't edit the original. Create a new ADR and set the old one's status to `Superseded by [NNN]`.
