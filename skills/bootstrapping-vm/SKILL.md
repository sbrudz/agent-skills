---
name: bootstrapping-vm
description: Bootstraps a Linux VM for development with Claude Code by installing the superpowers plugin collection and configuring GitHub credentials. Triggers at the start of a new VM session, when the user says bootstrap or set up this VM, or when development tools and GitHub access are not yet configured.
compatibility: Requires a Linux VM with root access, internet connectivity, and Claude Code CLI.
metadata:
  author: sbrudz
  version: "1.0"
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
```

## Step 1: Install superpowers

Follow the [installing-superpowers](../installing-superpowers/SKILL.md) skill.

Do not proceed to Step 2 until superpowers installation is verified.

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
