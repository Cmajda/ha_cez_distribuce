# Copilot Instructions (Repository)

## Commit messages

- Always write commit messages in English.
- Use Conventional Commits prefixes:
  feat:, fix:, docs:, style:, refactor:, perf:, test:, build:, ci:, chore:, revert:
- Use release/version commits as:
  chore(release): <version>
- Use dependency bumps as:
  build(deps): bump <package> to <version>

## Format

<type>(optional-scope): short imperative summary

## Examples

- feat(ui): add Docker version table sorting
- fix(api): handle null response from UniFi endpoint
- docs(readme): update local dev setup
- chore(release): 2.3.1
- build(deps): bump ruff to 0.14.0
