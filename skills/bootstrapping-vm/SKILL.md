---
name: bootstrapping-vm
description: Use when starting a new VM session, when the user says bootstrap or set up this VM, or when both the superpowers plugin and GitHub access are missing.
compatibility: Requires a Linux VM with root access, internet connectivity, and Claude Code CLI.
metadata:
  author: sbrudz
  version: "1.2"
---

# Bootstrapping a VM

Sets up a fresh Linux VM for development with Claude Code. Runs two skills in sequence:

1. Install the obra/superpowers plugin collection
2. Configure git and GitHub credentials

## Progress checklist

Copy and track progress:

```
- [ ] Install superpowers
- [ ] Restart Claude Code (if superpowers was newly installed)
- [ ] Configure GitHub credentials
- [ ] Confirm VM is ready for development
```

## Step 1: Install superpowers

Follow the [installing-superpowers](../installing-superpowers/SKILL.md) skill.

If superpowers was already installed, proceed to Step 2.

If superpowers was newly installed, it requires a restart to take effect. Tell the user:

> Superpowers has been installed. Please restart Claude Code, then continue bootstrapping by saying "continue setting up this VM" or similar. The next step is configuring GitHub credentials.

**Stop here and wait for the user to restart.** Do not proceed to Step 2 in the current session if superpowers was just installed — the plugin will not be active yet.

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

If all checks pass, the VM is ready. Report the status to the user.
