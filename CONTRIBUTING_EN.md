# Contributing

🇨🇿 [Česká verze](CONTRIBUTING.md)

Thanks for contributing! This repository contains a **CEZ HDO - Home Assistant custom integration**.

We use a simple workflow suitable for a small team: **`main` is always releasable**, and every change goes through a short-lived branch and a Pull Request (PR).

---

## Table of contents

- [Contributing](#contributing)
  - [Table of contents](#table-of-contents)
  - [Workflow overview](#workflow-overview)
  - [Branch rules](#branch-rules)
    - [Branch naming](#branch-naming)
  - [Commit \& PR title convention](#commit--pr-title-convention)
    - [Format](#format)
    - [Allowed types](#allowed-types)
    - [Examples](#examples)
    - [Recommendations](#recommendations)
  - [Pull Requests](#pull-requests)
    - [PR title](#pr-title)
    - [PR expectations](#pr-expectations)
  - [Merge policy](#merge-policy)
  - [Tagging \& releases](#tagging--releases)
    - [Commands (example)](#commands-example)
  - [Getting help](#getting-help)

---

## Workflow overview

1. (Optional) Create an Issue describing the change.
2. Create a branch from `main` for every change.
3. Commit changes using the message convention below.
4. Open a Pull Request (PR) back to `main`.
5. PR must pass CI and be approved.
6. Merge using **Squash & merge**.
7. **Delete the source branch** after a successful merge.
8. Create a **manual git tag** (when appropriate).

---

## Branch rules

- **`main` is always releasable.**
- Direct pushes to `main` are not allowed (PRs only).
- Create a branch per activity, from `main`.
- Keep branches short-lived and focused.

### Branch naming

Use one of the following prefixes:

- `feature/<short-title>`
- `fix/<short-title>`
- `docs/<short-title>`
- `chore/<short-title>`

If you have an Issue number, you may include it:

- `feature/123-add-new-sensor`
- `fix/87-handle-timeout`

Without an Issue:

- `feature/add-new-sensor`
- `docs/update-readme`

Keep names short, lowercase, words separated by `-`.

---

## Commit & PR title convention

We use a lightweight Conventional Commits style.

### Format

```plain
<type>: <short summary>
```

### Allowed types

- `feat:` – new feature / new functionality
- `fix:` – bug fix
- `docs:` – documentation only
- `chore:` – maintenance / refactor / tooling / formatting
- `test:` – tests only
- `ci:` – CI pipeline changes

### Examples

- `feat: add service to refresh data`
- `fix: handle API timeout during startup`
- `docs: clarify installation steps`
- `chore: reorganize config constants`
- `test: add unit tests for coordinator`

### Recommendations

- Use present tense (“add”, “fix”, “update”).
- Keep it short (ideally under ~70 characters).
- If relevant, reference the issue in the PR description (e.g. `Closes #123`).

---

## Pull Requests

### PR title

PR titles must follow the same convention as commits:

```plain
<type>: <short summary>
```

### PR expectations

- Keep PRs small and reviewable (one logical change).
- CI must pass.
- At least **1 approval** is required before merge.
- If the PR addresses an Issue, reference it in the PR description (e.g. `Closes #123`).

---

## Merge policy

- All merges to `main` go through a PR.
- CI must pass.
- At least **1 approval** is required.
- Merge method is **Squash & merge** (always).
- After merge, **delete the source branch**.

---

## Tagging & releases

Tags are created **manually** and are **immutable** (never moved/rewritten).

- Use semantic versioning: `vMAJOR.MINOR.PATCH` (e.g. `v1.4.2`).
  - **PATCH** for bug fixes
  - **MINOR** for backward-compatible features
  - **MAJOR** for breaking changes

### Commands (example)

Create and push a new tag for the current `main` HEAD:

```bash
git checkout main
git pull

git tag v1.2.3
git push origin v1.2.3
````

---

## Getting help

If you’re unsure about scope, naming, or release/tagging, open a draft PR early and discuss there.
