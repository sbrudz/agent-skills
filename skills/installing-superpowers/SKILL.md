---
name: installing-superpowers
description: Checks if the obra/superpowers plugin collection is installed in Claude Code and installs it if missing. Triggers at the start of a new session, when the user asks to install superpowers, or when another skill depends on superpowers being available.
compatibility: Requires Claude Code CLI with plugin support.
metadata:
  author: sbrudz
  version: "1.0"
---

# Installing Superpowers

Ensures the [obra/superpowers](https://github.com/obra/superpowers) plugin collection is installed in Claude Code.

## Progress checklist

Copy and track progress:

```
- [ ] Check if superpowers is already installed
- [ ] Install superpowers if missing
- [ ] Verify installation succeeded
```

## Step 1: Check if superpowers is installed

Check for the directory `~/.claude/plugins/cache/superpowers-marketplace`:

```bash
test -d ~/.claude/plugins/cache/superpowers-marketplace && echo "INSTALLED" || echo "NOT_INSTALLED"
```

If `INSTALLED`, skip to Step 3 (verification).

## Step 2: Install superpowers

Run these two commands in sequence:

```bash
claude plugin marketplace add obra/superpowers-marketplace
```

```bash
claude plugin install superpowers@superpowers-marketplace
```

If either command fails, report the error to the user and stop.

## Step 3: Verify installation

Confirm the plugin directory now exists:

```bash
test -d ~/.claude/plugins/cache/superpowers-marketplace && echo "SUCCESS" || echo "FAILED"
```

If `FAILED`, report the error to the user. Otherwise, installation is complete.
