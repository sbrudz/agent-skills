---
name: domain-driven-design
description: Use when planning features that involve business logic or domain modeling, and during code review to check naming consistency and module boundary violations — applies strategic DDD patterns
---

# Domain-Driven Design — Name Things Right, Draw Boundaries Well

Strategic DDD patterns for planning and code review. Focuses on ubiquitous language (naming), bounded contexts (boundaries), and context mapping (how modules relate).

## Scope Gate

Does this feature involve business logic or domain concepts? If purely UI, infrastructure, or DevOps with no domain modeling → skip.

## During Planning: Ubiquitous Language

Before technical questions, establish the language the code will use.

- **What are the key domain concepts?** Name them. One name per concept everywhere — code, UI, docs.
- **Do these names already exist in the codebase?** Use them. Don't introduce synonyms ("order" in one module, "purchase" in another).
- **Would a domain expert recognize these names?** `fulfillOrder` over `processOrderData`. If you have to explain what a "Handler" does, the name is technical, not domain-driven.
- **Does the same term mean different things in different parts of the system?** That's a bounded context boundary signal.

**Existing codebases:** Don't define the whole language upfront. Survey names in the modules you're touching, pick the best existing name for each concept, use it consistently in new code. Don't rename outside touched code — same guardrail as `boy-scout-rule`.

## During Planning: Bounded Contexts

**Signals of separate contexts:**
- Same word, different meaning. "Account" in billing (balance) vs. identity (permissions) — two models sharing a name.
- Different rates of change. Pricing changes weekly; user profiles change yearly. Coupling them means one breaks the other.
- Different ownership. Different teams making independent decisions about different parts.

**Identify during planning:**
- What contexts does this feature touch? Most features live in one context and talk to others.
- What crosses the boundary? Data crossing a context boundary should be translated at the boundary, not passed as internal types. Don't import another module's domain types directly — define what your context needs and map at the edge.
- Which context owns this concept? If "Order" exists in both Fulfillment and Billing, each has its own Order model with only the fields it needs.

**Context mapping:** When a feature spans contexts, name the relationship. Which is upstream (provides data), which is downstream (consumes)? Does one conform to the other's model, or translate at the boundary?

**ADR interaction:** Bounded context boundaries are decisions `architecture-decision-records` should capture — they affect multiple components and are hard to reverse.

## During Code Review

**Naming checklist:**
- Do new names follow the established ubiquitous language?
- Are there generic names hiding domain meaning? `Manager`, `Handler`, `Processor`, `Service`, `Data`, `Info` — the real domain concept probably hasn't been named yet.
- Do functions describe domain operations? `approveClaim` over `updateClaimStatus`.

**Boundary checklist:**
- Does new code reach across module boundaries to access internals?
- Are domain types shared across contexts? Each context should own its representation.
- Is translation happening at boundaries? Data crossing contexts should be mapped, not passed through as the sender's types.

## Related Skills

**During planning:**
- `architecture-decision-records` — bounded context boundaries warrant ADRs
- `ux-design-principles` — ubiquitous language should flow through to UI labels

**During implementation:**
- `functional-core-imperative-shell` — the functional core IS the domain model. DDD structures what goes in the core; FCIS keeps it pure

**During refactoring:**
- `boy-scout-rule` — "rename for clarity" becomes "rename to match ubiquitous language"
