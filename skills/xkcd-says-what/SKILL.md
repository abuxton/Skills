---
name: xkcd-says-what
description: 'Fetch a matching XKCD comic and generate validated Markdown or HTML embed output for docs or terminal use.'
license: MIT
metadata:
  author: abuxton
  version: "1.0"
  type: utility
  mode: application+generative
  maturity_score: 18
---

# XKCD Says What: Fetch and Embed XKCD Comics

You help users find one relevant XKCD comic and turn it into something immediately usable in a document or terminal. Your role is to resolve the comic request, validate the result, and generate clean Markdown or HTML output without dragging in complex dependencies.

## Core Principle

**Return one validated comic with a clear selection rationale, and reject fancy extras that need heavyweight tooling.**

## Quick Reference

Use this skill when the user wants to:

- fetch the latest XKCD comic
- fetch a random XKCD comic via `https://c.xkcd.com/random/comic/`
- find a likely comic from a short search term or natural-language description
- insert the comic into `README.md` or another Markdown file
- print valid HTML anchor or image markup to the terminal

Default behavior:

- if no target document is supplied, update `README.md`
- if the user asks for HTML, print HTML to the terminal instead of editing a file unless they explicitly request both
- if the user asks for ASCII art, reject it unless it can be done with a small shell or Python helper and no special libraries or terminal clients

## Workflow

1. **Classify the request** — Determine whether the user wants `latest`, `random`, a numeric comic id, a direct XKCD URL, or an archive-based match from a phrase or description. Also determine the requested output mode: Markdown edit, terminal HTML, or both.

2. **Resolve one comic** — Use `scripts/fetch_xkcd.py` to retrieve the comic metadata and output snippets:
   - `latest` should use `https://xkcd.com/info.0.json`
   - `random` should resolve through `https://c.xkcd.com/random/comic/`
   - search and natural-language lookup should parse `https://xkcd.com/archive/` and choose the nearest title match conservatively
   - if the match is approximate, say so clearly

3. **Validate the result** — Confirm that the comic page URL and image URL resolve with HTTP `200` before editing a document or presenting the HTML snippet. If validation fails, surface the failure explicitly instead of pretending the embed worked.

4. **Generate the requested output** — Use the returned snippets to produce one of:
   - Markdown image syntax
   - linked Markdown image syntax
   - HTML anchor markup
   - HTML image markup

5. **Edit the target document when needed** — If the user wants the comic embedded in Markdown:
   - update the explicit target file when provided
   - otherwise update `README.md`
   - verify the inserted link or embed text is present in the file after editing

6. **Handle ASCII requests conservatively** — Do not promise ASCII rendering by default. Reject it unless a relatively simple shell or Python script with only standard tooling can do the job. In this skill, ASCII output is intentionally rejected because rendering arbitrary PNG images reliably requires image-decoding or terminal-rendering dependencies that are outside the allowed simplicity bar.

7. **Report the outcome** — Summarize which comic was selected, why it was selected, what output was produced, what file was changed if any, and what validation succeeded.

## Available Tools

### `scripts/fetch_xkcd.py`

Resolve a comic request, emit reusable snippets, and optionally validate the page and image URLs.

```bash
python3 skills/xkcd-says-what/scripts/fetch_xkcd.py latest --format json --validate
python3 skills/xkcd-says-what/scripts/fetch_xkcd.py random --format markdown-linked
python3 skills/xkcd-says-what/scripts/fetch_xkcd.py "subduction ocean crust" --format html-anchor --validate
python3 skills/xkcd-says-what/scripts/fetch_xkcd.py https://xkcd.com/2057/ --format html-image
```

Prefer `--format json` when the agent needs both the metadata and the ready-to-use snippets.

## Example Interaction

**User:** "Add a random XKCD comic to the README and also show me the HTML anchor."

**Your approach:**

1. Run `python3 skills/xkcd-says-what/scripts/fetch_xkcd.py random --format json --validate`
2. Use the returned linked Markdown image snippet to update `README.md`
3. Print the returned HTML anchor snippet in the terminal
4. Confirm that the README now contains the comic link and that both validated URLs returned HTTP `200`

## Anti-Patterns

### The Transcript Fantasy

**Problem:** Pretending archive search covers comic transcripts, alt text, or semantic understanding far beyond the archive title list.

**Fix:** Be explicit that archive-based search is title-driven and approximate. If confidence is low, say so.

### The Broken Embed

**Problem:** Inserting Markdown or HTML before checking whether the comic page and image URL actually resolve.

**Fix:** Validate first, then edit the file or print the snippet.

### The ASCII Rabbit Hole

**Problem:** Pulling in Pillow, ImageMagick, `chafa`, or other special clients just to force an ASCII output mode.

**Fix:** Reject ASCII rendering under this skill's constraints and explain that the feature exceeds the allowed complexity budget.

## Reasoning Requirements

### Standard Reasoning

- Classifying the request as latest, random, direct id, URL, or archive search
- Interpreting script output and selecting the correct snippet type
- Deciding whether to edit a file or print terminal output

### Extended Reasoning

Use extended reasoning for:

- ambiguous natural-language descriptions with several plausible archive matches
- requests that combine file edits, terminal output, and validation requirements
- deciding whether a low-confidence archive match is acceptable or should be surfaced as uncertain

## Execution Strategy

### Sequential

- classify the request before fetching
- fetch before validating
- validate before editing a target document

### Parallelizable

- page URL validation and image URL validation can run concurrently
- if needed, multiple candidate archive scores can be compared independently before choosing one result

### Subagent Candidates

| Task | Agent Type | When to Spawn |
|------|------------|---------------|
| Repository doc update | general-purpose | When the embed needs to be inserted into multiple docs |
| Codebase exploration | explore | When the correct target Markdown file is unclear |

## Context Management

### Approximate Token Footprint

- **Skill base:** ~2k tokens
- **With script usage examples:** ~3k tokens
- **With live fetched comic metadata:** ~4k tokens

### Context Optimization

- Load `scripts/fetch_xkcd.py` only when the request needs exact arguments or output formats
- Prefer the JSON output mode when one fetch needs to drive several outputs
- Do not paste fetched HTML into chat unless debugging matching logic

## What You Do NOT Do

- You do not scrape more of xkcd.com than needed for one comic selection
- You do not claim ASCII support under the current simplicity constraint
- You do not rehost comic images; use XKCD's existing page and image URLs
- You do not silently downgrade validation failures into success

## Integration Graph

### Inbound (From Other Skills)

| Source Skill | Source State | Leads to State |
|--------------|--------------|----------------|
| writing-skills | Workflow Step 6: Add reference assets | XSW1: Need a runnable helper for repeatable comic lookup |

### Outbound (To Other Skills)

| This State | Leads to Skill | Target State |
|------------|----------------|--------------|
| XSW4: Need a polished Markdown destination after embedding | shields-badges | README polish after comic insertion |

### Complementary Skills

| Skill | Relationship |
|-------|--------------|
| writing-skills | Similar authoring conventions for maintaining the skill itself |
| do-nothing-scripting | Useful fallback when the user wants a manual script outline instead of immediate automation |
| shields-badges | Helps refine README presentation after the comic embed is added |

## Notes

- XKCD exposes reliable per-comic JSON at `https://xkcd.com/<num>/info.0.json` and the latest comic at `https://xkcd.com/info.0.json`.
- The archive page is good enough for lightweight title matching, but it is not a transcript search index.
- XKCD comics are licensed for sharing under Randall Munroe's published license terms; preserve attribution context by linking back to the comic page and avoid implying commercial reuse rights.
