# Skills

[![npm version](https://img.shields.io/npm/v/@abuxton/skills?style=flat)](https://npmjs.com/package/@abuxton/skills)
[![License](https://img.shields.io/github/license/abuxton/Skills)](LICENSE)

Agent skills for GitHub Copilot and other coding agents, built following the
[agentskills.io specification](https://agentskills.io/specification) and
publishable via [skills-npm](https://github.com/antfu/skills-npm).

## Available Skills

| Name | Description |
| ---- | ----------- |
| [shields-badges](skills/shields-badges/SKILL.md) | Analyse a repository to identify its focus and technology stack, then apply appropriate [shields.io](https://shields.io) badges to markdown files. |
| [writing-skills](skills/writing-skills/SKILL.md) | Author high-quality agent skills following the agentskills.io specification, with correct frontmatter, workflow structure, and reference assets. |
| [publishing-npm](skills/publishing-npm/SKILL.md) | Prepare and publish an npm package that ships agent skills, following the skills-npm convention for skill bundling and distribution. |
| [github-gist](skills/github-gist/SKILL.md) | Create, manage, and organize GitHub Gists using the gh and CLI. |
| [asciinema-record](skills/asciinema-record/SKILL.md) | Record a terminal session to a named .cast file using asciinema, trim the recording to marked content, and optionally convert it to a GIF using agg. |
| [do-nothing-scripting](skills/do-nothing-scripting/SKILL.md) | Derive a do-nothing bash script from an asciinema .cast file, encoding each observed command as a manual step that prompts the operator before proceeding. |

## Usage

![npx install ascii](./_assets/asciinema/skills-session.gif)

### Via npx (Recommended)

Install the package and symlink the bundled skills using [npx](https://github.com/antfu/skills-npm):

```bash
npx skills -h
> Usage: skills <command> [options]
...

npx skills install @abuxton/skills

```
### Via npm

Install the package and symlink the bundled skills using [skills-npm](https://github.com/antfu/skills-npm):

```bash

npm install @abuxton/skills
npx skills-npm
```

To symlink skills automatically on every `npm install`, add a `prepare` script to your `package.json`:

```json
{
  "scripts": {
    "prepare": "npx skills-npm"
  }
}
```

`skills-npm` creates symlinks at `skills/npm-<package-name>-<skill-name>` in your project. Add this to your `.gitignore` to avoid committing them:

```gitignore
skills/npm-*
```

### Manually

Copy a skill folder to your local `skills/` directory and reference it in your
Copilot prompts, or let the agent discover it automatically.

Each skill folder contains a `SKILL.md` instruction file and optional bundled
reference assets.

## Contributing

See [AGENTS.md](AGENTS.md) for guidance on writing new skills and publishing them via npm.
