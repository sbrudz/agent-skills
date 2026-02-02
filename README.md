# Agent Skills

Reusable [Agent Skills](https://agentskills.io) for Claude Code and other AI coding assistants.

## Available skills

| Skill | Description |
|-------|-------------|
| [bootstrapping-vm](skills/bootstrapping-vm/SKILL.md) | Bootstraps a Linux VM for development with Claude Code by installing superpowers and configuring GitHub credentials. |
| [installing-superpowers](skills/installing-superpowers/SKILL.md) | Checks if the obra/superpowers plugin collection is installed in Claude Code and installs it if missing. |
| [configuring-github-credentials](skills/configuring-github-credentials/SKILL.md) | Configures a Linux VM with git, GitHub CLI, SSH keys, and GitHub authentication. Distro-aware package installation. |
| [project-quality-setup](skills/project-quality-setup/SKILL.md) | Configures linting, formatting, pre-commit hooks, and CI before implementation begins. Detects the tech stack (Node.js/TypeScript, Go, Ruby, Rust) and applies the appropriate tools. |
| [react-best-practices](skills/react-best-practices/SKILL.md) | Code review checklist for React: component responsibility splitting, useEffect misuse, React 19 patterns (Suspense, useActionState, React Compiler), behavioral accessibility, and testing practices. Covers judgment calls linters cannot catch. |
| [functional-core-imperative-shell](skills/functional-core-imperative-shell/SKILL.md) | Code review checklist for separating business logic from side effects. Detects impure business logic, fat shells, and hidden side effects (logging, Date.now, mutable state in ostensibly pure functions). Language-agnostic. |
| [architecture-decision-records](skills/architecture-decision-records/SKILL.md) | Captures significant architectural decisions during planning using Michael Nygard's ADR template. Two-subagent workflow: proposer drafts the ADR, reviewer checks quality. Includes threshold gate to prevent ADR bloat. |
| [boy-scout-rule](skills/boy-scout-rule/SKILL.md) | Concrete refactoring checklist for the TDD REFACTOR phase and code quality review. Covers structural clarity (extract function, reduce nesting, simplify conditionals), structural design (consolidate duplication, right-size functions), and cross-cutting patterns. References functional-core-imperative-shell and react-best-practices as companion checks. |
| [visual-feedback-loop](skills/visual-feedback-loop/SKILL.md) | Visual feedback loop for the TDD GREEN phase. Screenshots the running application to verify UI correctness (layout, spacing, text, completeness) before refactoring. Tool-agnostic with Vibium recommended. Scoped to UI-affecting tasks only. |
| [ux-design-principles](skills/ux-design-principles/SKILL.md) | User-centered design companion to brainstorming for UI features. Applies Goal-Directed Design (Cooper) and usability principles (Krug) — user goals, context, expectations, progressive disclosure, scanning priority. |
| [ux-visual-evaluation](skills/ux-visual-evaluation/SKILL.md) | Second-pass visual evaluation companion to visual-feedback-loop. Evaluates screenshots for design quality: visual hierarchy, whitespace, spacing consistency, color usage, affordances, system status, and consistency. Draws from Refactoring UI and Nielsen's heuristics. |
| [ux-prototyping](skills/ux-prototyping/SKILL.md) | Throwaway HTML prototyping after brainstorming, before implementation. Threshold gate triggers for novel interactions, complex flows, or visual-balance-critical layouts. Screenshot-based iteration with user, saves accepted prototype screenshots, deletes throwaway code. |
| [domain-driven-design](skills/domain-driven-design/SKILL.md) | Strategic DDD patterns for planning and code review. Ubiquitous language (naming after domain concepts), bounded contexts (module boundaries), and context mapping (how modules relate). Includes code review checklists for naming violations and cross-boundary coupling. |

## Installation

### Claude Code (plugin marketplace)

```
/plugin marketplace add sbrudz/agent-skills
/plugin install agent-skills@sbrudz-skills
```

### Install a single skill

Use the `/install-skill` command in Claude Code and provide the GitHub URL to the skill directory, e.g.:

```
/install-skill https://github.com/sbrudz/agent-skills/tree/main/skills/bootstrapping-vm
```

### Other agents

Any agent that supports the [Agent Skills specification](https://agentskills.io/specification) can use these skills. Point the agent at the `SKILL.md` file in the relevant skill directory.

## Creating new skills

Each skill lives in its own directory under `skills/`:

```
skills/
└── skill-name/
    └── SKILL.md          # Required — frontmatter + instructions
```

See the [Agent Skills specification](https://agentskills.io/specification) for the full format.

## License

MIT
