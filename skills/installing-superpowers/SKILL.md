---
name: installing-superpowers
description: Use when starting a new Claude Code session, when the user mentions superpowers or obra, or when another skill depends on the superpowers plugin collection being available.
compatibility: Requires Claude Code CLI with plugin support.
metadata:
  author: sbrudz
  version: "1.2"
---

# Installing Superpowers

Ensures the [obra/superpowers](https://github.com/obra/superpowers) plugin collection is installed in Claude Code.

## Progress checklist

Copy and track progress:

```
- [ ] Check if superpowers is already installed
- [ ] Install superpowers if missing
- [ ] Verify installation succeeded
- [ ] Prompt user to restart Claude Code (if newly installed)
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

## Step 4: Restart Claude Code

The superpowers plugin will not be active until Claude Code is restarted. Tell the user:

> Superpowers has been installed. Please restart Claude Code for the plugin to take effect. After restarting, you can continue with the next step (e.g., configuring GitHub credentials).

**Do not continue with tasks that depend on superpowers skills being available.** The current session will not have access to them.
