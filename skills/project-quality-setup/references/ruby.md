# Ruby / Rails

## Contents

- Linter and formatter (RuboCop)
- Pre-commit hook
- CI workflow

## Linter and formatter: RuboCop

RuboCop handles both linting and formatting for Ruby.

Add to `Gemfile` (in the `:development` group):

```ruby
gem 'rubocop', require: false
gem 'rubocop-rails', require: false        # if Rails
gem 'rubocop-rspec', require: false        # if RSpec
gem 'rubocop-performance', require: false  # recommended
```

Run `bundle install`.

Generate a default config:

```bash
bundle exec rubocop --init
```

This creates `.rubocop.yml`. Add the extensions:

```yaml
require:
  - rubocop-rails        # if Rails
  - rubocop-rspec        # if RSpec
  - rubocop-performance

AllCops:
  NewCops: enable
  TargetRubyVersion: 3.2  # match the project's Ruby version
  Exclude:
    - 'db/schema.rb'
    - 'bin/**/*'
    - 'vendor/**/*'
    - 'node_modules/**/*'
```

Run `bundle exec rubocop -a` for safe auto-fixes, then `bundle exec rubocop -A` for all auto-fixes. Resolve remaining issues manually.

## Pre-commit hook

**Option A: Lefthook** (Ruby-friendly, no Python dependency):

```bash
gem install lefthook
lefthook install
```

Create `lefthook.yml`:

```yaml
pre-commit:
  commands:
    rubocop:
      glob: '*.rb'
      run: bundle exec rubocop --force-exclusion {staged_files}
```

**Option B: pre-commit framework** (if Python is available):

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/rubocop/rubocop
    rev: v1.75.2
    hooks:
      - id: rubocop
        args: [--force-exclusion]
```

Run `pre-commit install`.

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
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: .ruby-version
          bundler-cache: true
      - run: bundle exec rubocop
      - run: bundle exec rspec --format progress
```

Adjust: use `rake test` or `bin/rails test` for Minitest projects instead of `rspec`.
