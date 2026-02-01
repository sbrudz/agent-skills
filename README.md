# Agent Skills

Reusable [Agent Skills](https://agentskills.io) for Claude Code and other AI coding assistants.

## Available skills

| Skill | Description |
|-------|-------------|
| [project-quality-setup](skills/project-quality-setup/SKILL.md) | Configures linting, formatting, pre-commit hooks, and CI before implementation begins. Detects the tech stack (Node.js/TypeScript, Go, Ruby, Rust) and applies the appropriate tools. |

## Installation

### Claude Code

Add the skill to your project's `.claude/settings.json`:

```json
{
  "skills": [
    "https://github.com/sbrudz/agent-skills/tree/main/skills/project-quality-setup"
  ]
}
```

Or use the `/install-skill` command in Claude Code and provide the GitHub URL to the skill directory.

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
