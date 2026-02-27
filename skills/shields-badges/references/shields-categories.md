# Shields.io Badge Categories Reference

A reference guide for common shields.io badge types and their URL formats.

## Badge URL Formats

### Static Badge

```text
https://img.shields.io/badge/<LABEL>-<MESSAGE>-<COLOR>
```

Spaces become `_`, special characters are URL-encoded.

### Dynamic GitHub Badges

| Purpose | URL Pattern |
| ------- | ----------- |
| Workflow/CI status | `https://img.shields.io/github/actions/workflow/status/<USER>/<REPO>/<WORKFLOW_FILE>?branch=<BRANCH>` |
| License | `https://img.shields.io/github/license/<USER>/<REPO>` |
| Latest release | `https://img.shields.io/github/v/release/<USER>/<REPO>` |
| Stars | `https://img.shields.io/github/stars/<USER>/<REPO>` |
| Forks | `https://img.shields.io/github/forks/<USER>/<REPO>` |
| Open issues | `https://img.shields.io/github/issues/<USER>/<REPO>` |
| Open PRs | `https://img.shields.io/github/issues-pr/<USER>/<REPO>` |
| Top language | `https://img.shields.io/github/languages/top/<USER>/<REPO>` |
| Language count | `https://img.shields.io/github/languages/count/<USER>/<REPO>` |
| Repo size | `https://img.shields.io/github/repo-size/<USER>/<REPO>` |
| Last commit | `https://img.shields.io/github/last-commit/<USER>/<REPO>` |
| Contributors | `https://img.shields.io/github/contributors/<USER>/<REPO>` |
| Commit activity | `https://img.shields.io/github/commit-activity/m/<USER>/<REPO>` |

### Package / Registry Badges

| Ecosystem | URL Pattern |
| --------- | ----------- |
| npm version | `https://img.shields.io/npm/v/<PACKAGE>` |
| npm downloads | `https://img.shields.io/npm/dm/<PACKAGE>` |
| PyPI version | `https://img.shields.io/pypi/v/<PACKAGE>` |
| PyPI downloads | `https://img.shields.io/pypi/dm/<PACKAGE>` |
| Go module | `https://img.shields.io/github/go-mod/go-version/<USER>/<REPO>` |
| Gem version | `https://img.shields.io/gem/v/<GEM>` |
| Docker pulls | `https://img.shields.io/docker/pulls/<USER>/<IMAGE>` |
| Docker image size | `https://img.shields.io/docker/image-size/<USER>/<IMAGE>` |
| NuGet version | `https://img.shields.io/nuget/v/<PACKAGE>` |
| Maven Central | `https://img.shields.io/maven-central/v/<GROUP>/<ARTIFACT>` |

### Code Quality Badges

| Purpose | URL Pattern |
| ------- | ----------- |
| Coveralls coverage | `https://img.shields.io/coveralls/github/<USER>/<REPO>` |
| Codecov coverage | `https://img.shields.io/codecov/c/github/<USER>/<REPO>` |
| Code Climate maintainability | `https://img.shields.io/codeclimate/maintainability/<USER>/<REPO>` |
| SonarCloud quality gate | `https://img.shields.io/sonar/quality_gate/<PROJECT>?server=https://sonarcloud.io` |

### Technology / Language Logos

Use `logo=<name>` query parameter to add a logo to any badge. Common logo values:

`github`, `githubcopilot`, `python`, `javascript`, `typescript`, `go`, `rust`, `java`,
`dotnet`, `node.js`, `react`, `vue.js`, `angular`, `docker`, `kubernetes`, `terraform`,
`aws`, `googlecloud`, `azure`, `linux`, `windows`, `apple`, `visualstudiocode`

Example with logo:

```text
https://img.shields.io/badge/Built_with-Python-3776AB?logo=python&logoColor=white
```

### Style Options

Append `?style=<style>` to any badge URL. Available styles:

- `flat` (default)
- `flat-square`
- `plastic`
- `for-the-badge`
- `social`

## Markdown Badge Syntax

```markdown
[![Alt Text](badge-url)](link-url)
```

For non-linked badges:

```markdown
![Alt Text](badge-url)
```

## Badge Placement in README

Place badges immediately after the main title (H1 heading), before any prose description:

```markdown
# My Project

[![Build Status](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml?branch=main)](https://github.com/user/repo/actions)
[![License](https://img.shields.io/github/license/user/repo)](https://github.com/user/repo/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/user/repo)](https://github.com/user/repo/releases)

Project description here...
```

## Common Badge Sets by Repository Focus

### General Open-Source Project

- Build/CI status
- License
- Latest release / version
- Contributors
- Stars / forks (optional)

### Library / Package

- Package registry version
- Package registry downloads
- Build/CI status
- Code coverage
- License

### CLI Tool

- Latest release
- Build/CI status
- Top language
- License

### Container / Docker

- Docker pulls
- Docker image size
- Build/CI status
- License

### Infrastructure / IaC

- Build/CI status
- License
- Last commit
- Repo size

### Documentation Site

- Build/CI status
- Last commit
- License
