# Skill Creator for `.gitattributes`

Use the `skill-creator` skill to create a new GitHub Copilot skill for managing `.gitattributes`.

## Task

Create a new skill that:

- researches `.gitattributes` using the official Git documentation at `https://git-scm.com/docs/gitattributes`
- reviews the community reference repository at `https://github.com/gitattributes/gitattributes`
- creates a skill for generating and maintaining a sensible default `.gitattributes` file for Unix-like development environments
- supports safe capabilities to add attributes, remove attributes, and explain why each supported attribute should be used

The generated skill should produce conservative defaults for `*nix`-based development, especially around line endings and repository hygiene, and should avoid risky or unnecessary attribute rules.

## Context

Work in the current workspace at `${workspaceFolder}`.

Inspect existing skill files and repository conventions before generating anything so the new skill matches the structure, tone, and layout already used in this repository.

Do not require additional user input beyond invocation of this prompt.

## Requirements

The new skill should:

1. Create a dedicated skill directory under `skills/`
2. Add a `SKILL.md` file that follows this repository's skill conventions
3. Include any supporting reference assets only if they are genuinely useful
4. Explain the default `.gitattributes` choices with research-backed rationale
5. Support operations for:
   - creating a sensible default `.gitattributes`
   - adding new attribute rules safely
   - removing existing attribute rules safely
   - preserving user intent where repository-specific rules already exist
6. Prefer Unix-first defaults, especially for line endings and text normalization
7. Avoid destructive edits, unsupported assumptions, or overly aggressive normalization rules

## Research Instructions

Before writing the skill:

1. Review the official Git documentation for `.gitattributes`
2. Review the `gitattributes/gitattributes` repository for practical patterns
3. Inspect this repository's existing skills to learn:
   - expected `SKILL.md` structure
   - naming conventions
   - how workflow steps are written
   - when to include supporting references
4. Synthesize the research into a conservative, practical skill design

## Implementation Instructions

When creating the skill:

1. Choose a clear skill name related to `.gitattributes`
2. Write the skill as if it will be used by engineers maintaining repositories across Unix-like development environments
3. Make the workflow explicit and actionable
4. Include guidance for:
   - when to mark files as text
   - when to use explicit `eol` settings
   - when binary handling is appropriate
   - when not to add a rule
5. Ensure add/remove behavior is safe and does not blindly overwrite repository-specific intent
6. Reuse repository patterns rather than inventing a new format
7. Update related documentation such as `README.md` and `AGENTS.md` if the new skill should be listed there

## Constraints

Avoid:

- risky defaults
- unnecessary attributes
- destructive rewrites of existing `.gitattributes` files
- broad assumptions about all repositories having the same needs
- adding rules without justification
- creating capabilities that are not supported by the research

## Validation

Before finishing, verify that:

- the new skill matches repository conventions
- the skill includes research-backed `.gitattributes` guidance
- Unix-first defaults are sensible and conservative
- add/remove attribute behavior is described safely and clearly
- related docs are updated if needed
- the result is usable without further clarification

## Output

At the end, provide a concise summary that includes:

- files created or changed
- the default `.gitattributes` strategy chosen
- any add/remove capabilities included
- what research informed the skill
- what validation you performed
