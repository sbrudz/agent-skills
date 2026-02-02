# Agent Skills — Claude Code Instructions

## Commit Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `style`, `perf`, `ci`, `build`

## Semver Versioning

After each push to `main`, bump the version according to these rules:

| Commit type | Version bump |
|---|---|
| `feat:` | Minor (0.0.x → 0.1.0) |
| `fix:`, `refactor:`, `docs:`, `chore:`, `test:`, `style:`, `perf:`, `ci:`, `build:` | Patch (0.0.0 → 0.0.1) |
| `BREAKING CHANGE` footer or `!` after type (e.g. `feat!:`) | Major (0.x.x → 1.0.0) |

When multiple commits are pushed together, the highest-priority bump wins (major > minor > patch).

### Files to update

Bump the version string in **all three** locations — they must stay in sync:

1. `.claude-plugin/plugin.json` → `version`
2. `.claude-plugin/marketplace.json` → `metadata.version`
3. `.claude-plugin/marketplace.json` → `plugins[0].version`

### Release workflow

After bumping versions:

1. Commit the version bump: `git commit -m "chore: bump version to X.Y.Z"`
2. Create a git tag: `git tag vX.Y.Z`
3. Push the commit and tag: `git push && git push --tags`
4. Create a GitHub release: `gh release create vX.Y.Z --generate-notes`

### What NOT to version

SKILL.md versions (inside individual skill directories) are independent and manually managed. Do not bump them as part of this process.
