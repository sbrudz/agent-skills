---
name: configuring-github-credentials
description: Use when setting up a new Linux VM for development, when git or gh commands fail with authentication errors, when SSH to github.com is not configured, or when the user asks to configure GitHub access.
compatibility: Requires a Linux VM with root access and internet connectivity.
metadata:
  author: sbrudz
  version: "1.2"
---

# Configuring GitHub Credentials

Sets up git, GitHub CLI, SSH keys, and git configuration on a Linux VM.

## Progress checklist

Copy and track progress:

```
- [ ] Install git and GitHub CLI
- [ ] Prompt user for GitHub username
- [ ] Authenticate to GitHub CLI
- [ ] Verify GitHub CLI connectivity
- [ ] Generate SSH key
- [ ] Configure SSH for GitHub
- [ ] Upload SSH public key to GitHub
- [ ] Verify SSH connectivity
- [ ] Configure git globals
- [ ] Set up project repository
```

## Step 1: Install git and GitHub CLI

Detect the Linux distribution and install packages with the native package manager. See [references/package-managers.md](references/package-managers.md) for distro-specific commands.

```bash
. /etc/os-release && echo "Distro: $ID"
```

Check if `git` and `gh` are already installed before attempting installation:

```bash
command -v git && echo "git: installed" || echo "git: missing"
command -v gh && echo "gh: installed" || echo "gh: missing"
```

Install only what is missing, using the commands from the package manager reference for the detected distro.

## Step 2: Prompt for GitHub username

Ask the user which GitHub account to use. Recommend using an account with limited permissions (not a personal account with org admin access) since the credentials will live on the VM.

**Important:** Wait for the user's response before proceeding.

## Step 3: Authenticate to GitHub CLI

**Primary method — Device flow (OAuth):**

**Important:** This command must be run as a background task so the output streams properly. Running it inline with `2>&1` will not display the URL and code.

```bash
# Run in background — do NOT run inline
gh auth login --hostname github.com --git-protocol ssh --web --scopes admin:public_key
```

The `--scopes admin:public_key` flag is required so that Step 7 (`gh ssh-key add`) has permission to upload SSH keys. Without it, the default OAuth scopes will not include this and you will need to re-authenticate.

Use `run_in_background: true` when calling the Bash tool. Then read the output to find the one-time code and URL. Present both to the user clearly:

> Open this URL in any browser: https://github.com/login/device
> Enter this code: XXXX-XXXX

Wait for the user to confirm they completed the browser flow.

**Fallback — Personal access token:**

If the device flow fails or the user prefers a token:

1. Ask the user to create a PAT at https://github.com/settings/tokens with the scopes: `repo`, `read:org`, `admin:public_key`
2. Ask the user to provide the token
3. Authenticate:

```bash
echo "<TOKEN>" | gh auth login --hostname github.com --git-protocol ssh --with-token
```

## Step 4: Verify GitHub CLI connectivity

```bash
gh auth status
```

Confirm the output shows the expected username and authentication method. If it fails, return to Step 3.

## Step 5: Generate SSH key

Generate an ed25519 key specifically for GitHub:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/github_ed25519 -N "" -C "ai-agent-vm"
```

Set correct permissions:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/github_ed25519
chmod 644 ~/.ssh/github_ed25519.pub
```

If `~/.ssh/github_ed25519` already exists, ask the user whether to overwrite or reuse the existing key.

## Step 6: Configure SSH for GitHub

Add a host entry to `~/.ssh/config` (create the file if needed):

```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_ed25519
    IdentitiesOnly yes
```

Set permissions on the config file:

```bash
chmod 600 ~/.ssh/config
```

If `~/.ssh/config` already has a `github.com` entry, ask the user before modifying it.

## Step 7: Upload SSH public key to GitHub

```bash
gh ssh-key add ~/.ssh/github_ed25519.pub --title "ai-agent-vm-$(hostname)-$(date +%Y%m%d)"
```

The title includes the hostname and date for easy identification in GitHub settings.

## Step 8: Verify SSH connectivity

```bash
ssh -T git@github.com -o StrictHostKeyChecking=accept-new
```

Expected output: `Hi <username>! You've successfully authenticated...`

If this fails, review Steps 5-7 for issues.

## Step 9: Configure git globals

Check if `user.name` and `user.email` are already set:

```bash
git config --global user.name || echo "NOT SET"
git config --global user.email || echo "NOT SET"
```

If not set, ask the user what name and email to use for git commits. The git commit identity may differ from the GitHub account username (e.g., a dedicated CI/bot identity). Suggest the GitHub noreply email format as a default:

```bash
git config --global user.name "<name>"
git config --global user.email "<name>@users.noreply.github.com"
```

Verify the configuration was applied:

```bash
git config --global user.name && git config --global user.email
```

## Step 10: Set up project repository

Ask the user which repository to use for their work. Options:

1. **Clone an existing repo** — ask for the repo name (e.g., `owner/repo-name`):
   ```bash
   gh repo clone <owner/repo-name>
   ```

2. **Create a new repo** — ask for the desired name and visibility:
   ```bash
   gh repo create <name> --private --clone
   ```

All source code should be committed to this repo and pushed to GitHub.
