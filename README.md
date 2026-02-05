# Dev Ethos

Opinionated [agent skills](https://agentskills.io) that guide AI coding assistants toward software development and UX design best practices. Compatible with Claude Code, Windsurf, Codex, and any tool that supports the [Agent Skills specification](https://agentskills.io/specification). Designed to complement [obra/superpowers](https://github.com/obra/superpowers).

For VM bootstrapping skills (GitHub credentials, superpowers installation), see [claude-vm-setup](https://github.com/sbrudz/claude-vm-setup).

## Available skills

| Skill | Description |
|-------|-------------|
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

### Claude Code

#### Plugin marketplace (all skills)

```
/plugin marketplace add sbrudz/dev-ethos
/plugin install dev-ethos@sbrudz-skills
```

#### Single skill

Use the `/install-skill` command and provide the GitHub URL to the skill directory:

```
/install-skill https://github.com/sbrudz/dev-ethos/tree/main/skills/project-quality-setup
```

#### Using with Superpowers Workflow Hooks

Dev-ethos skills integrate with [superpowers](https://github.com/obra/superpowers) workflow hooks to automatically trigger at the right points in your development workflow (design, planning, execution, review).

> **Note:** Workflow hooks require superpowers with hooks support. Until this feature is merged upstream, use the fork below.

**1. Install superpowers with hooks support:**

```
/plugin marketplace add git@github.com:sbrudz-ai/superpowers.git#feature/workflow-hooks
/plugin install superpowers@superpowers-dev
```

**2. Install dev-ethos:**

```
/plugin marketplace add sbrudz/dev-ethos
/plugin install dev-ethos@sbrudz-skills
```

**3. Create a workflow hooks configuration file:**

Copy [`workflow-hooks.yaml`](workflow-hooks.yaml) to `.claude/workflow-hooks.yaml` (project-level) or `~/.claude/workflow-hooks.yaml` (global).

Or download directly:

```bash
# Project-level
mkdir -p .claude && curl -sL https://raw.githubusercontent.com/sbrudz/dev-ethos/main/workflow-hooks.yaml -o .claude/workflow-hooks.yaml

# Global
curl -sL https://raw.githubusercontent.com/sbrudz/dev-ethos/main/workflow-hooks.yaml -o ~/.claude/workflow-hooks.yaml
```

**4. Restart Claude Code** to load the new configuration.

For details on hook points, conditions, and modes, see the [superpowers workflow hooks documentation](https://github.com/sbrudz-ai/superpowers/blob/feature/workflow-hooks/hooks/workflow-hooks.md).

### Windsurf

Windsurf loads skills from `SKILL.md` files in specific directories. You can install skills at the workspace level (one project) or globally (all projects).

#### Workspace skills (one project)

From your project root:

```bash
git clone https://github.com/sbrudz/dev-ethos.git /tmp/dev-ethos
mkdir -p .windsurf/skills
cp -r /tmp/dev-ethos/skills/* .windsurf/skills/
rm -rf /tmp/dev-ethos
```

#### Global skills (all projects)

```bash
git clone https://github.com/sbrudz/dev-ethos.git /tmp/dev-ethos
mkdir -p ~/.codeium/windsurf/skills
cp -r /tmp/dev-ethos/skills/* ~/.codeium/windsurf/skills/
rm -rf /tmp/dev-ethos
```

#### Single skill

To install just one skill (e.g., `project-quality-setup`):

```bash
mkdir -p .windsurf/skills/project-quality-setup
curl -sL https://raw.githubusercontent.com/sbrudz/dev-ethos/main/skills/project-quality-setup/SKILL.md \
  -o .windsurf/skills/project-quality-setup/SKILL.md
```

Skills are available in Cascade via `@skill-name` mentions once installed.

### Codex

Codex loads skills from `SKILL.md` files in `.codex/skills/` (repo-level) or `~/.codex/skills/` (user-level).

#### Repo-level skills (one project)

From your project root:

```bash
git clone https://github.com/sbrudz/dev-ethos.git /tmp/dev-ethos
mkdir -p .codex/skills
cp -r /tmp/dev-ethos/skills/* .codex/skills/
rm -rf /tmp/dev-ethos
```

#### User-level skills (all projects)

```bash
git clone https://github.com/sbrudz/dev-ethos.git /tmp/dev-ethos
mkdir -p ~/.codex/skills
cp -r /tmp/dev-ethos/skills/* ~/.codex/skills/
rm -rf /tmp/dev-ethos
```

#### Single skill

To install just one skill (e.g., `project-quality-setup`):

```bash
mkdir -p .codex/skills/project-quality-setup
curl -sL https://raw.githubusercontent.com/sbrudz/dev-ethos/main/skills/project-quality-setup/SKILL.md \
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
