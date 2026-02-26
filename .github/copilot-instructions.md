# GitHub Copilot Instructions

## Project Overview

This is a standard template repository for working projects. It provides baseline tooling,
configuration, and conventions to accelerate new project setup.

## Code Style and Conventions

- Use clear, descriptive names for variables, functions, and files
- Prefer explicit over implicit behaviour
- Follow the principle of least surprise
- Keep functions and methods small and focused (single responsibility)
- Write self-documenting code; add comments only when the intent is not obvious

## Git Workflow (Gitflow)

This repository follows **Gitflow** branching strategy:

- `main` / `master` — production-ready code only; never commit directly
- `develop` — integration branch for features; merge target for feature branches
- `feature/<short-description>` — new features branched from `develop`
- `release/<version>` — release preparation branched from `develop`; merged into `main` and `develop`
- `hotfix/<short-description>` — urgent fixes branched from `main`; merged back into `main` and `develop`
- `fix/<short-description>` or `bugfix/<short-description>` — bug fixes from `develop`

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

Examples:
- `feat(api): add endpoint for user profile`
- `fix(auth): handle token expiry edge case`
- `docs(readme): update installation instructions`
- `ci(pre-commit): update hook versions`

## OpenAPI / OpenSpec Guidelines

When working with OpenAPI specifications:

- Use OpenAPI 3.1.x as the specification version
- Store spec files in `openapi/` or `api/` directories
- File naming: `openapi.yaml` or `<service-name>.openapi.yaml`
- Follow RESTful naming conventions for paths (`/resources`, `/resources/{id}`)
- Define reusable components in `components/` sections (schemas, responses, parameters)
- Always include `description` fields for operations, parameters, and schemas
- Use `$ref` for reusable schemas rather than inline duplication
- Validate specs with [Spectral](https://stoplight.io/open-source/spectral) or [Redocly CLI](https://redocly.com/docs/cli/)

## Infrastructure as Code

- Terraform files follow `terraform fmt` formatting
- Module structure: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`
- Always pin provider versions with `~>` constraints
- Use `terraform validate` and `tflint` before committing

## Testing

- Write tests alongside implementation code
- Name test files consistently with the implementation (e.g., `*_test.go`, `test_*.py`)
- Test edge cases and error paths, not just happy paths

## Security

- Never commit secrets, tokens, API keys, or credentials
- Use environment variables or secrets managers for sensitive values
- Enable `detect-private-key` pre-commit hook
- Review `SECURITY.md` for vulnerability reporting guidelines

## Pull Requests

- Keep PRs small and focused (one concern per PR)
- Include a clear description of the change and its motivation
- Reference related issues with `Fixes #<issue>` or `Relates to #<issue>`
- Ensure all pre-commit hooks pass before requesting review
