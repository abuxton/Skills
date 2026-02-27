---
name: writing-skills
description: 'Author high-quality agent skills following the agentskills.io specification, with correct frontmatter, workflow structure, and reference assets.'
---

# Writing Agent Skills

Create well-structured agent skill files (`SKILL.md`) that comply with the [agentskills.io specification](https://agentskills.io/specification) and are ready for distribution.

## Role

You are an expert in agent skill authoring, the agentskills.io specification, and AI-assisted developer tooling. You understand how coding agents discover and apply skills, and you know how to write clear, actionable instructions that agents follow consistently.

- Follow the agentskills.io SKILL.md specification exactly
- Write skills that are scoped, actionable, and unambiguous
- Include meaningful frontmatter, a clear role section, and a step-by-step workflow
- Bundle reference assets alongside the skill when they add value

## Skill File Structure

Every skill lives in its own directory under `skills/`:

```text
skills/
└── <skill-name>/
    ├── SKILL.md          # Required — main skill instruction file
    └── references/       # Optional — supporting reference assets
        └── *.md
```

### SKILL.md Frontmatter

```yaml
---
name: <skill-name>
description: '<One sentence describing what the skill does.>'
---
```

- `name`: kebab-case identifier matching the directory name
- `description`: concise, action-oriented sentence starting with a verb

### SKILL.md Body Sections

| Section | Purpose |
| ------- | ------- |
| `# <Title>` | Human-readable skill title |
| `## Role` | The agent's persona and guiding principles for this skill |
| `## Workflow` | Numbered steps the agent follows, in order |
| `## Notes` | (Optional) Edge cases, caveats, and tips |

## Workflow

1. **Define the skill scope** — Identify one discrete task the skill should perform. Skills should be focused; avoid combining unrelated concerns in a single skill.

2. **Name the skill** — Choose a kebab-case name that describes the task (e.g., `shields-badges`, `publishing-npm`, `openapi-linting`). Create the directory `skills/<skill-name>/`.

3. **Write the frontmatter** — Open `SKILL.md` with the YAML frontmatter block containing `name` and `description`.

4. **Write the Role section** — Describe the agent's persona, what it knows, and the guiding principles it applies. Use bullet points for key capabilities.

5. **Write the Workflow section** — Break the task into numbered steps. Each step should:
   - Begin with a bold action label (e.g., **Discover context**)
   - Describe what to examine, decide, or produce
   - Reference any supporting assets in `references/` where relevant

6. **Add reference assets** — If the workflow requires lookup tables, templates, or examples that are too large to inline, place them in `references/` as markdown files and reference them from the workflow.

7. **Write a Notes section** (if needed) — Document edge cases, constraints, or tips that do not fit naturally in the workflow steps.

8. **Validate the skill** — Check:
   - Frontmatter is valid YAML and matches the directory name
   - All referenced files in `references/` exist
   - The workflow is unambiguous and complete enough for an agent to follow without additional context
   - The skill does not duplicate an existing skill in the `skills/` directory

9. **Update the README and AGENTS.md** — Add the new skill to the `## Available Skills` table in both `README.md` and `AGENTS.md`:

   ```markdown
   | [<skill-name>](skills/<skill-name>/SKILL.md) | <description> |
   ```

## Notes

- Keep skills small and focused. A skill that does one thing well is more reusable than a broad skill that does many things.
- Avoid hardcoding project-specific values (paths, usernames, repository names). Skills should be portable across projects.
- Reference assets should be in markdown format so agents can read them directly without external tools.
- Skills are discovered by agents from `skills/*/SKILL.md`; ensure the directory name matches the `name` frontmatter field.
