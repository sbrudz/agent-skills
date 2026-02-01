# Package Manager Reference

## Detecting the distro

```bash
if [ -f /etc/os-release ]; then
  . /etc/os-release
  echo "$ID"
fi
```

## Installing packages by distro

| Distro ID | Package manager | Install git | Install gh |
|-----------|----------------|-------------|------------|
| `ubuntu`, `debian` | apt | `apt-get update && apt-get install -y git` | See [GitHub CLI install docs for Debian/Ubuntu](#debianubuntu) |
| `fedora` | dnf | `dnf install -y git` | `dnf install -y gh` |
| `rhel`, `centos`, `rocky`, `almalinux` | dnf/yum | `dnf install -y git` | See [GitHub CLI install docs for RHEL](#rhel) |
| `arch`, `manjaro` | pacman | `pacman -Sy --noconfirm git` | `pacman -Sy --noconfirm github-cli` |
| `opensuse-leap`, `opensuse-tumbleweed`, `sles` | zypper | `zypper install -y git` | `zypper install -y gh` |
| `alpine` | apk | `apk add git` | `apk add github-cli` |

## Debian/Ubuntu

The GitHub CLI requires adding a repository:

```bash
apt-get update && apt-get install -y curl
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
apt-get update && apt-get install -y gh
```

## RHEL

For RHEL-based distros without `gh` in default repos:

```bash
dnf install -y 'dnf-command(config-manager)'
dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
dnf install -y gh
```
