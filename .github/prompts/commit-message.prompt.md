# Conventional Commit Message Generator

Generate a conventional commit message for the staged changes.

## Changes to Commit

[DESCRIBE YOUR CHANGES OR PASTE THE `git diff --staged` OUTPUT]

## Conventional Commit Format

```
<type>(<scope>): <short summary>

[optional body — explain WHY, not WHAT]

[optional footer(s)]
```

### Types

| Type       | When to use                                          |
|------------|------------------------------------------------------|
| `feat`     | New feature for the user                             |
| `fix`      | Bug fix for the user                                 |
| `docs`     | Documentation changes only                          |
| `style`    | Formatting, whitespace (no logic change)            |
| `refactor` | Code restructuring (no feature or fix)              |
| `perf`     | Performance improvement                              |
| `test`     | Adding or updating tests                             |
| `build`    | Build system or dependency changes                   |
| `ci`       | CI/CD configuration changes                         |
| `chore`    | Maintenance tasks (no production code change)       |
| `revert`   | Reverts a previous commit                           |

### Scope Examples

Common scopes for this repository:
- `pre-commit` — pre-commit hook configuration
- `ci` — GitHub Actions workflows
- `devcontainer` — dev container configuration
- `docs` — documentation
- `api` — API specification or implementation
- `deps` — dependency updates

### Rules

- Summary line: 72 characters max, imperative mood ("add" not "added")
- Body lines: 100 characters max
- Reference issues in footer: `Fixes #123` or `Closes #123`
- Breaking changes: add `!` after type/scope or `BREAKING CHANGE:` footer

### Examples

```
feat(api): add pagination to resource list endpoint

Adds cursor-based pagination to GET /resources to handle large result
sets efficiently. Clients pass a `cursor` query parameter to fetch
the next page.

Closes #42
```

```
ci(pre-commit): update hook versions to latest

- pre-commit-hooks: v4.3.0 → v4.5.0
- markdownlint-cli: v0.32.2 → v0.39.0
- Add markdown-link-check hook
```

```
fix(auth)!: require explicit token expiry in JWT payload

BREAKING CHANGE: tokens without an `exp` claim are now rejected.
Update all token issuers to include an expiry.
```
