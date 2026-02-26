# Gitflow Branch and Commit Helper

Help me follow the Gitflow branching strategy for this change.

## Context

Describe the change you want to make:

[DESCRIBE YOUR CHANGE HERE]

## What I need

Based on the description above, suggest:

1. **Branch name** — following the pattern:
   - `feature/<short-description>` for new features
   - `fix/<short-description>` or `bugfix/<short-description>` for bug fixes
   - `hotfix/<short-description>` for urgent production fixes
   - `release/<version>` for release preparation
   - `docs/<short-description>` for documentation-only changes
   - `chore/<short-description>` for maintenance tasks

2. **Source branch** — whether to branch from `develop` (features, fixes) or `main` (hotfixes)

3. **Commit messages** — conventional commit format for the planned changes:
   ```
   <type>(<scope>): <short summary>
   ```

4. **PR description template** — a concise PR description including:
   - What changed and why
   - How to test
   - Related issues

5. **Merge targets** — which branches to merge back into when done

## Gitflow Quick Reference

| Branch type | Source    | Merge into            |
|-------------|-----------|----------------------|
| feature     | develop   | develop               |
| bugfix      | develop   | develop               |
| release     | develop   | main + develop        |
| hotfix      | main      | main + develop        |
