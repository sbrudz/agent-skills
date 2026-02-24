# Agent Skills

Opinionated [agent skills](https://agentskills.io) that guide AI coding assistants toward software development and UX design best practices. Compatible with Claude Code, Windsurf, Codex, and any tool that supports the [Agent Skills specification](https://agentskills.io/specification).

For VM bootstrapping skills (GitHub credentials, tool installation), see [claude-vm-setup](https://github.com/sbrudz/claude-vm-setup).

## Available skills

| Skill | Description |
|-------|-------------|
| [project-quality-setup](skills/project-quality-setup/SKILL.md) | Configures linting, formatting, pre-commit hooks, and CI before implementation begins. Detects the tech stack (Node.js/TypeScript, Go, Ruby, Rust) and applies the appropriate tools. |
| [react-best-practices](skills/react-best-practices/SKILL.md) | Code review checklist for React: component responsibility splitting, useEffect misuse, React 19 patterns (Suspense, useActionState, React Compiler), behavioral accessibility, and testing practices. Covers judgment calls linters cannot catch. |
| [functional-core-imperative-shell](skills/functional-core-imperative-shell/SKILL.md) | Code review checklist for separating business logic from side effects. Detects impure business logic, fat shells, and hidden side effects (logging, Date.now, mutable state in ostensibly pure functions). Language-agnostic. |
| [architecture-decision-records](skills/architecture-decision-records/SKILL.md) | Captures significant architectural decisions during planning using Michael Nygard's ADR template. Two-subagent workflow: proposer drafts the ADR, reviewer checks quality. Includes threshold gate to prevent ADR bloat. |
| [boy-scout-rule](skills/boy-scout-rule/SKILL.md) | Concrete refactoring checklist for the TDD REFACTOR phase and code quality review. Covers structural clarity (extract function, reduce nesting, simplify conditionals), structural design (consolidate duplication, right-size functions), and cross-cutting patterns. References functional-core-imperative-shell and react-best-practices as companion checks. |
| [visual-feedback-loop](skills/visual-feedback-loop/SKILL.md) | Visual feedback loop for the TDD GREEN phase. Screenshots the running application to verify UI correctness (layout, spacing, text, completeness) before refactoring. Tool-agnostic — works with any browser automation (Puppeteer, Chrome DevTools MCP, etc.). Scoped to UI-affecting tasks only. |
| [ux-design-principles](skills/ux-design-principles/SKILL.md) | User-centered design companion to brainstorming for UI features. Applies Goal-Directed Design (Cooper) and usability principles (Krug) — user goals, context, expectations, progressive disclosure, scanning priority. |
| [ux-visual-evaluation](skills/ux-visual-evaluation/SKILL.md) | Second-pass visual evaluation companion to visual-feedback-loop. Evaluates screenshots for design quality: visual hierarchy, whitespace, spacing consistency, color usage, affordances, system status, and consistency. Draws from Refactoring UI and Nielsen's heuristics. |
| [ux-prototyping](skills/ux-prototyping/SKILL.md) | Throwaway HTML prototyping after brainstorming, before implementation. Threshold gate triggers for novel interactions, complex flows, or visual-balance-critical layouts. Screenshot-based iteration with user, saves accepted prototype screenshots, deletes throwaway code. |
| [domain-driven-design](skills/domain-driven-design/SKILL.md) | Strategic DDD patterns for planning and code review. Ubiquitous language (naming after domain concepts), bounded contexts (module boundaries), and context mapping (how modules relate). Includes code review checklists for naming violations and cross-boundary coupling. |

## Recommended companions

- **[obra/superpowers](https://github.com/obra/superpowers)** — Process-oriented skills for TDD, debugging, brainstorming, and development workflow. Pairs well with the domain and code-quality skills in this collection.

## Installation

### Claude Code

#### Plugin marketplace (all skills)

```
/plugin marketplace add sbrudz/agent-skills
/plugin install agent-skills@sbrudz-skills
```

#### Single skill

Use the `/install-skill` command and provide the GitHub URL to the skill directory:

```
/install-skill https://github.com/sbrudz/agent-skills/tree/main/skills/project-quality-setup
```

### Windsurf

Windsurf loads skills from `SKILL.md` files in specific directories. You can install skills at the workspace level (one project) or globally (all projects).

#### Workspace skills (one project)

From your project root:

```bash
git clone https://github.com/sbrudz/agent-skills.git /tmp/agent-skills
mkdir -p .windsurf/skills
cp -r /tmp/agent-skills/skills/* .windsurf/skills/
rm -rf /tmp/agent-skills
```

#### Global skills (all projects)

```bash
git clone https://github.com/sbrudz/agent-skills.git /tmp/agent-skills
mkdir -p ~/.codeium/windsurf/skills
cp -r /tmp/agent-skills/skills/* ~/.codeium/windsurf/skills/
rm -rf /tmp/agent-skills
```

#### Single skill

To install just one skill (e.g., `project-quality-setup`):

```bash
mkdir -p .windsurf/skills/project-quality-setup
curl -sL https://raw.githubusercontent.com/sbrudz/agent-skills/main/skills/project-quality-setup/SKILL.md \
  -o .windsurf/skills/project-quality-setup/SKILL.md
```

Skills are available in Cascade via `@skill-name` mentions once installed.

### Codex

Codex loads skills from `SKILL.md` files in `.codex/skills/` (repo-level) or `~/.codex/skills/` (user-level).

#### Repo-level skills (one project)

From your project root:

```bash
git clone https://github.com/sbrudz/agent-skills.git /tmp/agent-skills
mkdir -p .codex/skills
cp -r /tmp/agent-skills/skills/* .codex/skills/
rm -rf /tmp/agent-skills
```

#### User-level skills (all projects)

```bash
git clone https://github.com/sbrudz/agent-skills.git /tmp/agent-skills
mkdir -p ~/.codex/skills
cp -r /tmp/agent-skills/skills/* ~/.codex/skills/
rm -rf /tmp/agent-skills
```

#### Single skill

To install just one skill (e.g., `project-quality-setup`):

```bash
mkdir -p .codex/skills/project-quality-setup
curl -sL https://raw.githubusercontent.com/sbrudz/agent-skills/main/skills/project-quality-setup/SKILL.md \
  -o .codex/skills/project-quality-setup/SKILL.md
```

> **Note:** Some skills have supporting files in `references/` subdirectories. When installing single skills, check the skill's `SKILL.md` for references and copy those files too.

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
