# Agent Skills

Reusable [Agent Skills](https://agentskills.io) for Claude Code and other AI coding assistants.

## Available skills

| Skill | Description |
|-------|-------------|
| [bootstrapping-vm](skills/bootstrapping-vm/SKILL.md) | Bootstraps a Linux VM for development with Claude Code by installing superpowers and configuring GitHub credentials. |
| [installing-superpowers](skills/installing-superpowers/SKILL.md) | Checks if the obra/superpowers plugin collection is installed in Claude Code and installs it if missing. |
| [configuring-github-credentials](skills/configuring-github-credentials/SKILL.md) | Configures a Linux VM with git, GitHub CLI, SSH keys, and GitHub authentication. Distro-aware package installation. |
| [project-quality-setup](skills/project-quality-setup/SKILL.md) | Configures linting, formatting, pre-commit hooks, and CI before implementation begins. Detects the tech stack (Node.js/TypeScript, Go, Ruby, Rust) and applies the appropriate tools. |

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
