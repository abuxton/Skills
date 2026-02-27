---
name: do-nothing-scripting
description: 'Derive a do-nothing bash script from an asciinema .cast file, encoding each observed command as a manual step that prompts the operator before proceeding.'
---

# Do-Nothing Scripting from Asciinema

Inspired by [Dan Slimmon's do-nothing scripting pattern](https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation/), this skill converts an asciinema `.cast` recording into a **do-nothing bash script**: a runnable procedure that walks an operator through each step manually, while making each step trivially replaceable with real automation later.

## Role

You are an expert in shell scripting, automation strategy, and the do-nothing scripting pattern. You understand:

- How to read asciinema v3 `.cast` files and extract the sequence of commands a user ran
- How to identify logical groupings of commands into named steps
- How to write idiomatic, safe bash following modern best practices
- How to structure a do-nothing script so each step can be independently automated over time
- How to surface context variables (usernames, paths, URLs) that a step depends on

## Do-Nothing Scripting Principles

A do-nothing script:

- **Does not execute** the steps — it prints instructions and waits for the operator to act
- **Encapsulates each step in a function** so any step can later be replaced with real automation without changing the rest of the script
- **Collects context** (dynamic values like usernames or ticket IDs) by prompting the operator once and threading the values through subsequent steps
- **Lowers the activation energy** for full automation by making the gap between "manual" and "automated" a single function rewrite

## Workflow

1. **Obtain the cast file** — Identify the `.cast` file to analyse. It may be passed directly (e.g. `./tmp/deploy.cast`) or produced by the `asciinema-record` skill. Confirm the file exists before proceeding.

2. **Extract commands from the cast** — Use the helper script `references/extract_commands.py` to pull the command sequence from the cast:
   ```bash
   python3 skills/do-nothing-scripting/references/extract_commands.py ./tmp/<name>.cast
   ```
   The script prints each detected command on its own line, prefixed with its sequence number. Review the output and discard any commands that are noise (shell prompts, `clear`, incidental `cd` calls that are part of navigation rather than procedure).

3. **Group commands into logical steps** — Examine the command list and cluster related commands into named steps. Good step names are verb phrases that describe what a human does, not what the computer does:
   - `create_feature_branch` (not `git_checkout`)
   - `update_config_file` (not `sed`)
   - `wait_for_pipeline` (not `watch`)

   Aim for 1–5 commands per step. A step that is a single trivially-automatable command is fine and desirable.

4. **Identify context variables** — Note any values that will differ between runs: usernames, branch names, ticket IDs, environment names, file paths. These become context variables, collected once in `main()` and passed to step functions.

5. **Write the do-nothing bash script** — Generate the script following the template in `references/do_nothing_template.sh`. Rules:
   - Shebang: `#!/usr/bin/env bash`
   - Safety flags: `set -euo pipefail` immediately after the shebang
   - One function per step, named `step_<snake_case_name>()`
   - Each function:
     - Prints a heading: `echo "==> Step N: <Human readable name>"`
     - Prints each sub-command the operator must run, indented with spaces
     - Calls `wait_for_enter` at the end
   - A `wait_for_enter()` utility function using `read -rp`
   - A `collect_context()` function that prompts for all context variables
   - A `main()` function that calls `collect_context` then each step in order, finishing with `echo "✓ Done."`
   - `main "$@"` as the last line of the file

6. **Annotate automation potential** — Add an inline `# TODO: automate` comment on functions whose body is a single deterministic command. This signals which steps are lowest-effort to convert from manual to automated.

7. **Write the script to `./tmp/<name>_do_nothing.sh`** and make it executable:
   ```bash
   chmod +x ./tmp/<name>_do_nothing.sh
   ```

8. **Validate the script** — Run:
   ```bash
   bash -n ./tmp/<name>_do_nothing.sh
   ```
   Fix any syntax errors reported before presenting the result.

9. **Present a summary** — Show the operator:
   - The path to the generated script
   - The list of steps and their automation potential
   - A note on which context variables are required at runtime

## Notes

- If the cast file contains only `"o"` (output) events and no `"i"` (input) events, `extract_commands.py` falls back to parsing command prompts from the output stream. Results may be less accurate; review carefully.
- Do-nothing scripts are **not** meant to be run in CI or automation pipelines — they are operator guides. Do not add flags or logic that suppress the interactive prompts.
- When a step involves waiting for an external system (a build, a deploy, a human approval), represent it as a `wait_for_enter` pause with clear instructions — do not attempt to poll or sleep.
- Step functions should remain pure: no side effects, no file writes, no network calls. The only action they take is printing and waiting.
- Prefer `printf` over `echo` for portable output when the string may contain escape sequences; use `echo` for simple prose lines.
