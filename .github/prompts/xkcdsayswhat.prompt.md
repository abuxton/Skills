---
description: "Use the skill-builder skill to create the xkcd-says-what skill for fetching and embedding XKCD comics."
agent: "agent"
tools: ["codebase", "search", "editFiles", "changes", "problems"]
---

# XKCD Says What Skill Builder

You are a humorous but practical developer with strong skill-authoring instincts and enough engineering discipline to keep the result simple, maintainable, and useful.

## Task

Use the `skill-builder` skill to create a new GitHub Copilot skill named `xkcd-says-what`.

The generated skill should help a user retrieve a single XKCD comic image based on one of these inputs:

- a natural-language description of the comic
- `random`, which should use `https://c.xkcd.com/random/comic/`
- `latest`, which should use `https://xkcd.com/`
- a search term, which should inspect `https://xkcd.com/archive/` for close or relevant matches

## Goal

Create a production-ready skill that can:

1. retrieve a single XKCD comic `.png` image or image URL from the requested comic
2. embed the image link into a Markdown document
3. print valid embeddable HTML, such as an anchor or image snippet, to the terminal
4. optionally render the comic as ASCII in the terminal only if that can be achieved with a relatively simple Python or shell script included as a skill asset and without special libraries or extra client dependencies

If the ASCII rendering feature is too complex, unreliable, or requires non-trivial dependencies, explicitly reject that part of the design and explain why in the skill.

## Context

Work in the current repository.

Before writing anything:

1. inspect the existing skills in `skills/`
2. inspect repository documentation such as `README.md` and `AGENTS.md`
3. review existing prompt and skill conventions so the new material matches the repository's tone and structure

Do not ask for more user input unless something is genuinely blocking.

## Requirements

The generated skill should:

1. create a dedicated skill directory at `skills/xkcd-says-what/`
2. add a `SKILL.md` file that follows the repository's skill conventions
3. include supporting reference assets only when they are directly useful
4. use a simple and reliable strategy for obtaining the comic image URL
5. support:
   - `random`
   - `latest`
   - archive-based lookup from a search term or natural-language description
6. default to updating `README.md` with the comic link or embed unless the user explicitly provides a target file
7. support returning valid HTML anchor or image embed output when requested
8. treat ASCII rendering as optional and feasibility-gated
9. reject the ASCII feature if it cannot be implemented with a relatively simple Python or shell asset and no special libraries
10. update related documentation such as `README.md` and `AGENTS.md` if the new skill should be listed there

## Implementation Instructions

When creating the skill:

1. use the `skill-builder` skill as the primary authoring mechanism
2. keep the workflow explicit, actionable, and easy for another agent to follow
3. prefer simple web interactions and parsing strategies over brittle or over-engineered approaches
4. ensure the skill can:
   - embed a Markdown image link in a target document
   - print valid HTML anchor or image embed output to the terminal
   - explain how it chooses the comic for `random`, `latest`, and archive-based lookup
5. if the archive search is approximate, describe the matching strategy clearly and conservatively
6. if the prompt or query is ambiguous, prefer the nearest reasonable archive match and explain the fallback behavior
7. avoid introducing dependencies that are hard to install or unlikely to exist in a standard shell or Python environment
8. include any helper script only if it is small, understandable, and necessary
9. update repository docs when the new skill should be discoverable by other users of this repository

## Constraints

Avoid:

- complicated scraping stacks
- browser automation unless absolutely necessary
- non-standard Python packages
- heavy image-processing dependencies
- pretending ASCII rendering is supported if it is not realistically achievable
- vague success messaging that hides failure or uncertainty

## Validation

Before finishing, verify that:

- the new skill matches repository conventions
- `skills/xkcd-says-what/` contains a complete, usable skill definition
- any docs that should mention the skill are updated
- the skill clearly describes how `random`, `latest`, and archive-based lookup work
- Markdown embedding behavior is defined
- generated HTML anchor or embed output is valid HTML
- any referenced comic or image link resolves successfully with HTTP `200`
- if a target document is used, the resulting link or embed is present in that document
- the ASCII feature is either implemented simply or explicitly rejected with rationale

## Output

At the end, provide a concise summary that includes:

- files created or changed
- whether ASCII rendering was implemented or rejected
- how comic selection works
- what validation was performed
- any important tradeoffs or limitations
