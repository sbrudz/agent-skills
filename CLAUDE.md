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

## Development Notes

### Background agent notifications can be silently dropped

When running tests or work via background subagents, completion notifications are unreliable — agents may finish but never notify. If a test appears hung for more than a few minutes, check the output file directly (`ls -la /tmp/<expected-output-file>`) rather than waiting. The file existing means the agent completed silently.

**But the file existing does not mean it is finished.** Agents rewrite their output several times; one run went 1400 → 1353 → 1288 words after the file first appeared. Measuring too early inverts conclusions. Prefer the completion notification, and when you must poll, check staleness numerically:

```bash
python3 -c "import time,os;print(time.time()-os.path.getmtime('FILE'))"
```

Do **not** use `find -newermt` for this. It is a GNU extension; this machine's `find` is `bfs`, which errors on it, and `$(...)` swallows the error into an empty string that reads as "stable" — so every check passes instantly and silently. Verify a measurement instrument before trusting a null result from it.

### Verify subagent self-reported metrics independently

Subagents routinely misreport quantitative metrics about their own output (word counts, percentage reductions, file sizes). When a subagent claims "reduced by 55%," verify with `wc -w` or equivalent. Subagent self-reports are directional at best — never trust the specific numbers without independent verification.

The converse also happens: a self-report can be right while your own number is wrong because you measured mid-write. When your figure contradicts the agent's, re-measure after settling before concluding the agent misreported.

### A stated numeric limit becomes a spending target

Any threshold a skill states will be read as a budget to consume. Told that "more than 5% longer is failure," a run landed at +4.9% and justified it as "at the ceiling the methodology allows" — having hit the same quality score at −0.6% one iteration earlier. When a rule needs a number for checkability, name the real target separately and deny the budget reading outright ("X is a boundary for detecting failure, not an allowance to spend").

### Read tool calls, not tokens, to tell whether a rule is being followed

Token counts do not indicate effort spent on compliance. Across twelve benchmark runs, Sonnet used *more* tokens than Opus in every single arm while applying fewer of the skill's rules. The informative signal was tool calls: as rules accumulated, Opus went 26 → 56 while Sonnet sat flat at 15–28, applying one rule cluster per run and alternating which. More rules answered with more prose instead of more verification means the rules are being read, not run.

### Checklists must demand actions, not assertions

A model that stops once its changes hang together will mark an assertion-style checklist complete without looking. "Check that the example is one real instance" gets a yes; "name the instance in one noun phrase, then list every property you attributed to it that the instance lacks" produces an artifact that cannot be faked. Converting a checklist from assertions to actions with written outputs moved Sonnet's tool calls 26 → 36 and got both rule clusters applied in one run for the first time. Pay for such a section by moving existing checks into it rather than restating them.

## Adding or Removing Skills

When a skill is added, removed, or significantly changed:

1. **Update README.md immediately** — add/update/remove the skill's row in the Available Skills table before committing the skill itself (or in the same commit).
2. **Test across models when creating or significantly revising a skill.** Sonnet and Opus have different natural tendencies (e.g., Opus has a stronger "add detail" instinct during revision). A skill that works for one model may fail for the other. Run RED-GREEN-REFACTOR cycles on both models before finalizing.

### Pre-release checklist

Before bumping versions, ensure:

1. **README.md is up to date.** If skills were added, removed, or significantly changed, update the README to reflect the current skill inventory and descriptions.

### Release workflow

After the pre-release checklist passes, bump versions, then:

1. Commit the version bump: `git commit -m "chore: bump version to X.Y.Z"`
2. Create a git tag: `git tag vX.Y.Z`
3. Push the commit and tag: `git push && git push --tags`
4. Create a GitHub release with descriptive notes:

```bash
gh release create vX.Y.Z --notes "$(cat <<'EOF'
## New Skill / Changes

- **skill-name** — One-sentence description of what the skill does and its key features.

Any additional context (e.g., companion skill updates, CLAUDE.md changes).

**Full Changelog**: https://github.com/sbrudz/agent-skills/compare/vPREVIOUS...vX.Y.Z
EOF
)"
```

Do NOT use `--generate-notes` — it produces empty output when commits go directly to main without PRs. Always write release notes that describe what was added or changed in user-facing terms.

### What NOT to version

SKILL.md versions (inside individual skill directories) are independent and manually managed. Do not bump them as part of this process.
