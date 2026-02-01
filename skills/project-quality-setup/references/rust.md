# Rust

## Contents

- Linter (Clippy)
- Formatter (rustfmt)
- Pre-commit hook
- CI workflow

## Linter: Clippy

Clippy is included with `rustup`. No separate install needed.

Configure via `clippy.toml` at the project root, or add to `Cargo.toml`:

```toml
[lints.clippy]
pedantic = { level = "warn", priority = -1 }
```

Adjust lint groups to the project's strictness preference (`warn` vs `deny`, `pedantic` vs default).

Run:

```bash
cargo clippy -- -D warnings
```

The `-D warnings` flag treats warnings as errors (useful for CI). Fix issues with `cargo clippy --fix`.

## Formatter: rustfmt

rustfmt is included with `rustup`. Configure via `rustfmt.toml` at the project root if the defaults need adjustment:

```toml
edition = "2024"
```

Run:

```bash
# Format all files
cargo fmt

# Check without modifying (for CI)
cargo fmt -- --check
```

## Pre-commit hook

**Option A: pre-commit framework** (if Python is available):

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/doublify/pre-commit-rust
    rev: v1.0
    hooks:
      - id: fmt
      - id: clippy
        args: [--all-targets, --all-features, --, -D, warnings]
```

Run `pre-commit install`.

**Option B: simple shell hook** (no extra dependencies):

Write `.git/hooks/pre-commit`:

```bash
#!/bin/sh
cargo fmt -- --check || { echo "Run cargo fmt"; exit 1; }
cargo clippy -- -D warnings || exit 1
```

Make it executable: `chmod +x .git/hooks/pre-commit`.

## CI workflow

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      - uses: Swatinem/rust-cache@v2
      - run: cargo fmt -- --check
      - run: cargo clippy -- -D warnings
      - run: cargo test
```
