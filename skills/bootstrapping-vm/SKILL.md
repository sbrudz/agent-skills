---
name: bootstrapping-vm
description: Use when starting a new VM session, when the user says bootstrap or set up this VM, or when both the superpowers plugin and GitHub access are missing.
compatibility: Requires a Linux VM with root access, internet connectivity, and Claude Code CLI.
metadata:
  author: sbrudz
  version: "1.3"
---

# Bootstrapping a VM

Sets up a fresh Linux VM for development with Claude Code. Runs two skills in sequence:

1. Install the obra/superpowers plugin collection
2. Configure git and GitHub credentials

## Progress checklist

Copy and track progress:

```
- [ ] Install superpowers
- [ ] Configure GitHub credentials
- [ ] Confirm VM is ready for development
- [ ] Prompt user to restart Claude Code (if superpowers was newly installed)
```

## Step 1: Install superpowers

Follow the [installing-superpowers](../installing-superpowers/SKILL.md) skill.

Note whether superpowers was newly installed or already present. Continue to Step 2 either way — GitHub credential setup does not depend on superpowers.

## Step 2: Configure GitHub credentials

Follow the [configuring-github-credentials](../configuring-github-credentials/SKILL.md) skill.

This step is interactive — it will prompt the user for their GitHub username, guide them through authentication, and set up SSH keys.

## Step 3: Confirm readiness

Verify the VM is ready for development:

```bash
echo "=== Superpowers ===" && test -d ~/.claude/plugins/cache/superpowers-marketplace && echo "OK" || echo "MISSING"
echo "=== GitHub CLI ===" && gh auth status 2>&1 | head -5
echo "=== SSH ===" && ssh -T git@github.com 2>&1 | head -1
echo "=== Git config ===" && git config --global user.name && git config --global user.email
```

If all checks pass, report the status to the user.

If superpowers was newly installed in Step 1, tell the user:

> All setup is complete. Please restart Claude Code so the superpowers plugin takes effect. After restarting, superpowers skills will be available.

If superpowers was already installed, no restart is needed.
