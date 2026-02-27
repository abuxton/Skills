---
name: publishing-npm
description: 'Prepare and publish an npm package that ships agent skills, following the skills-npm convention for skill bundling and distribution.'
---

# npm Publishing for Agent Skills

Configure an npm package to bundle and publish agent skills following the [skills-npm convention](https://github.com/antfu/skills-npm), so consumers can symlink them automatically with `skills-npm`.

## Role

You are an expert in npm package publishing, the agentskills.io specification, and the skills-npm distribution convention. You understand how to structure `package.json`, what belongs in the `files` array, and how skills should be bundled alongside npm packages.

- Configure `package.json` correctly for publishing skills to npm
- Ensure skills are included in the published package via the `files` field
- Follow semantic versioning and provide accurate package metadata
- Guide consumers on how to install and activate the bundled skills

## Workflow

1. **Check the skills directory** — Confirm a `skills/` directory exists at the package root and contains at least one skill subdirectory, each with a `SKILL.md` file:

   ```text
   skills/
   └── <skill-name>/
       └── SKILL.md
   ```

   If skills are missing, create them first using the `writing-skills` skill.

2. **Create or update `package.json`** — Ensure the following fields are present and correct:

   ```json
   {
     "name": "<package-name>",
     "version": "1.0.0",
     "description": "<description>",
     "license": "<SPDX-identifier>",
     "repository": {
       "type": "git",
       "url": "git+https://github.com/<owner>/<repo>.git"
     },
     "homepage": "https://github.com/<owner>/<repo>#readme",
     "bugs": {
       "url": "https://github.com/<owner>/<repo>/issues"
     },
     "keywords": ["skills", "agent-skills", "agentskills"],
     "files": [
       "skills"
     ]
   }
   ```

   - `name`: use a scoped name (`@org/package`) when publishing under an organisation
   - `files`: must include `"skills"` so the skills directory is included in the published tarball
   - `keywords`: include `agent-skills` and `agentskills` to improve discoverability

3. **Update `.gitignore`** — Add the following entries to prevent committing symlinks created by `skills-npm` in consuming projects, and to ignore installed dependencies:

   ```gitignore
   node_modules/
   skills/npm-*
   ```

4. **Verify the publish tarball** — Run a dry-run publish to confirm the `skills/` directory is included:

   ```bash
   npm pack --dry-run
   ```

   Confirm the output lists `skills/<skill-name>/SKILL.md` for each skill.

5. **Update the README** — Add installation and usage instructions for consumers. At minimum, include
   an `## npm` section with:
   - Installation: `npm install <package-name>`
   - Skill symlink: `npx skills-npm`
   - A `"prepare"` script in `package.json` to automate symlinking on install, for example:

     ```json
     {
       "scripts": {
         "prepare": "npx skills-npm"
       }
     }
     ```
6. **Publish the package** — Authenticate with the npm registry and publish:

   ```bash
   npm login
   npm publish --access public
   ```

   For scoped packages, `--access public` is required unless publishing to a private registry.

7. **Verify the published package** — After publishing, confirm the skills are accessible:

   ```bash
   npm pack <package-name> --dry-run
   npx skills-npm
   ```

## Notes

- The `files` field in `package.json` acts as an allowlist. Without `"skills"` in it, the `skills/` directory will not be included in the published tarball even if it exists locally.
- Skills discovered via the `skills-npm` convention are symlinked to `skills/npm-<package-name>-<skill-name>` in the consuming project. The `skills/npm-*` pattern in `.gitignore` prevents these symlinks from being committed.
- If the package is not yet published, consumers can reference it locally using `npm link` or a relative path in `package.json` dependencies.
- Use `npm version patch|minor|major` to bump the version before publishing updates.
- Verify that all skills pass the `writing-skills` checklist before publishing.
