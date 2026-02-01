# Go

## Contents

- Linter (golangci-lint)
- Formatter (gofmt / goimports)
- Pre-commit hook
- CI workflow

## Linter: golangci-lint

Install [golangci-lint](https://golangci-lint.run/):

```bash
# Preferred: binary install (not go install, which can have version issues)
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/HEAD/install.sh | sh -s -- -b $(go env GOPATH)/bin
```

Create `.golangci.yml` at the project root. A sensible default:

```yaml
linters:
  enable:
    - errcheck
    - govet
    - staticcheck
    - unused
    - gosimple
    - ineffassign
    - typecheck
```

Adjust linters based on the project's needs. Run `golangci-lint run` and check the enabled linters match what the team expects.

Add a Makefile target or script:

```makefile
lint:
	golangci-lint run ./...
```

Run `golangci-lint run --fix ./...` for auto-fixable issues, then resolve the rest manually.

## Formatter: gofmt / goimports

Go has a built-in formatter (`gofmt`). For import organization, use `goimports`:

```bash
go install golang.org/x/tools/cmd/goimports@latest
```

Add Makefile targets:

```makefile
format:
	goimports -w .

format-check:
	test -z "$$(goimports -l .)"
```

Run `goimports -w .` to format all files.

## Pre-commit hook

Use [pre-commit](https://pre-commit.com/) framework or a simple git hook.

**Option A: pre-commit framework** (if Python is available):

```bash
pip install pre-commit
```

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/golangci/golangci-lint
    rev: v2.1.6
    hooks:
      - id: golangci-lint-full
  - repo: https://github.com/tekwizely/pre-commit-golang
    rev: v1.0.0-rc.1
    hooks:
      - id: go-fmt
```

Run `pre-commit install`.

**Option B: simple shell hook** (no extra dependencies):

Write `.git/hooks/pre-commit`:

```bash
#!/bin/sh
goimports -l . | grep -q . && echo "Run goimports -w ." && exit 1
golangci-lint run ./... || exit 1
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
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
      - uses: golangci/golangci-lint-action@v8
      - name: Check formatting
        run: test -z "$(goimports -l .)"
      - run: go test ./... -race -coverprofile=coverage.out
```
