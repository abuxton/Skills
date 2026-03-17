---
name: do-nothing-scripting
description: 'Derive a do-nothing script from an asciinema .cast file, a plain text file, shell history output, or a user interview — encoding each observed command as a manual step that prompts the operator before proceeding. Preferred implementation uses the danslimmon/donothing Go library; a bash template is also maintained for environments without Go.'
---

# Do-Nothing Scripting

Inspired by [Dan Slimmon's do-nothing scripting pattern](https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation/), this skill converts a command sequence — from any source — into a **do-nothing script**: a runnable procedure that walks an operator through each step manually, while making each step trivially replaceable with real automation later.

The **preferred implementation** uses the [`danslimmon/donothing`](https://github.com/danslimmon/donothing) Go library, which provides a structured framework for building do-nothing procedures with built-in support for step automation, typed inputs/outputs, and Markdown documentation generation. A bash template (`references/do_nothing_template.sh`) is maintained as an alternative for environments without Go.

## Role

You are an expert in automation strategy, Go programming, shell scripting, and the do-nothing scripting pattern. You understand:

- How to use the [`danslimmon/donothing`](https://github.com/danslimmon/donothing) Go library to author structured procedures
- How to read asciinema v3 `.cast` files and extract the sequence of commands a user ran
- How to parse plain text files and shell history output to extract command lists
- How to interview a user to elicit the steps of a manual procedure
- How to identify logical groupings of commands into named steps
- How to write idiomatic Go and safe bash following modern best practices
- How to structure a do-nothing script so each step can be independently automated over time
- How to surface context variables (usernames, paths, URLs) that a step depends on
- How to pass typed outputs from one step as inputs to the next using the Go library

## Implementation Approaches

> **Preferred: Go (`danslimmon/donothing`)**  
> Use the Go library whenever Go is available. It provides a type-safe, structured framework with built-in input/output passing between steps, automatic step sequencing, and Markdown documentation generation via `--print`. See `references/do_nothing_template.go` for a ready-to-use starting point.

> **Alternative: Bash**  
> Use the bash template when Go is not available in the target environment, or when the audience is more comfortable with shell scripts. See `references/do_nothing_template.sh`. The bash approach has no external dependencies and runs anywhere with a POSIX-compatible shell.

### Go library quick-start

```bash
# Initialise a new Go module (if needed)
go mod init example.com/your-procedure

# Add the donothing dependency
go get github.com/danslimmon/donothing

# Copy the template as a starting point
cp skills/do-nothing-scripting/references/do_nothing_template.go ./do_nothing.go

# Run interactively
go run do_nothing.go

# Print the procedure as Markdown documentation
go run do_nothing.go --print
```

Key Go library concepts:

| Concept | API | Purpose |
| ------- | --- | ------- |
| Procedure | `donothing.NewProcedure()` | Container for all steps |
| Short description | `pcd.Short("...")` | One-line summary shown at the top |
| Long description | `pcd.Long("...")` | Markdown prose shown when procedure starts |
| Add step | `pcd.AddStep(func(step *donothing.Step) {...})` | Register a step by passing a configuration closure |
| Step name | `step.Name("camelCaseName")` | Machine-readable identifier (camelCase by convention) |
| Step title | `step.Short("Human readable name")` | Section heading shown to the operator |
| Step instructions | `step.Long("...")` | Markdown instructions; reference outputs with `@@OutputName@@` |
| Declare output | `step.OutputString("Name", "description")` | Prompts the operator for a value; available to later steps as input |
| Declare input | `step.InputString("Name", required)` | Marks that this step consumes the named output from a prior step |
| Validate | `pcd.Check()` | Returns a list of problems with the procedure definition |
| Run procedure | `pcd.Execute()` | Interactive run; returns `error` |
| Print docs | `pcd.Render(os.Stdout)` | Emit Markdown documentation to any `io.Writer`; returns `error` |

## Input Modes

This skill accepts four input modes. Choose the mode that matches what the user provides:

| Mode | When to use | Example |
| ---- | ----------- | ------- |
| **cast** | An asciinema `.cast` recording exists | `./tmp/deploy.cast` |
| **text** | A plain text file lists the commands, one per line | `./tmp/steps.txt` |
| **history** | The user wants to derive a script from recent shell history | `history 20 > /tmp/history.txt` |
| **interview** | No input file is available; gather steps interactively | _(ask the user)_ |

## Do-Nothing Scripting Principles

A do-nothing script:

- **Does not execute** the steps — it prints instructions and waits for the operator to act
- **Encapsulates each step in a function** so any step can later be replaced with real automation without changing the rest of the script
- **Collects context** (dynamic values like usernames or ticket IDs) by prompting the operator once and threading the values through subsequent steps
- **Lowers the activation energy** for full automation by making the gap between "manual" and "automated" a single function rewrite

## Workflow

1. **Determine the input source** — Ask the user which input mode applies if it is not already clear:
   - **cast**: `"Do you have an asciinema .cast file? If so, what is the path?"`
   - **text**: `"Do you have a text file listing the commands? If so, what is the path?"`
   - **history**: `"Would you like to use your recent shell history? Run: history <N> > /tmp/history.txt"`
   - **interview**: `"I don't see an input file. Let's build the script together — what is the first step in your procedure?"`
     Continue asking `"What is the next step?"` until the user says there are no more steps. Record each step description as a command line in `/tmp/<name>_steps.txt`, then proceed as for the **text** mode.

2. **Extract the command list** — Use `references/extract_commands.py` to pull the command sequence.
   The script auto-detects the format, or you can override with `--format=`:

   ```bash
   # auto-detect (cast, history, or text)
   python3 skills/do-nothing-scripting/references/extract_commands.py ./tmp/<name>.cast

   # explicit formats
   python3 skills/do-nothing-scripting/references/extract_commands.py --format=cast    ./tmp/<name>.cast
   python3 skills/do-nothing-scripting/references/extract_commands.py --format=history ./tmp/history.txt
   python3 skills/do-nothing-scripting/references/extract_commands.py --format=text    ./tmp/steps.txt
   ```

   The script prints each detected command prefixed with its sequence number. Review the output and discard noise (shell prompts, `clear`, incidental `cd` calls that are part of navigation rather than procedure).

   **Capturing history directly:**
   ```bash
   history 20 > /tmp/history.txt
   python3 skills/do-nothing-scripting/references/extract_commands.py --format=history /tmp/history.txt
   ```

3. **Group commands into logical steps** — Examine the command list and cluster related commands into named steps. Good step names are verb phrases that describe what a human does, not what the computer does:
   - `create_feature_branch` (not `git_checkout`)
   - `update_config_file` (not `sed`)
   - `wait_for_pipeline` (not `watch`)

   Aim for 1–5 commands per step. A step that is a single trivially-automatable command is fine and desirable.

4. **Identify context variables** — Note any values that will differ between runs: usernames, branch names, ticket IDs, environment names, file paths. These become context variables, collected once in `main()` and passed to step functions.

5. **Write the do-nothing script** — Choose the implementation approach based on the environment:

   **Go (preferred)** — Use `references/do_nothing_template.go` as the starting point. Rules:
   - One `pcd.AddStep(func(step *donothing.Step) {...})` call per logical step
   - Give each step a `step.Name("camelCaseName")` and `step.Short("Human readable name")`
   - For manual steps, add a `step.Long(...)` with Markdown instructions
   - Use `@@OutputName@@` in `Long()` text to embed the value of a named output from a prior step
   - For values that flow between steps, declare `step.OutputString("Name", "description")` on the producing step and `step.InputString("Name", true)` on each consuming step
   - The operator will be prompted to supply each output value at runtime; earlier outputs are shown in later steps' instructions automatically
   - To automate a step: implement the logic as a Go function, call it in `main()` directly (outside the procedure), and remove the corresponding `AddStep` block
   - Call `pcd.Check()` before executing to validate the procedure definition
   - End `main()` with `pcd.Execute()` for interactive use, or `pcd.Render(os.Stdout)` when the `--print` flag is passed; handle the returned `error`
   - Write the file to `./tmp/<name>_do_nothing.go`

   **Bash (alternative)** — Use `references/do_nothing_template.sh` as the starting point. Rules:
   - Shebang: `#!/usr/bin/env bash`
   - Safety flags: `set -euo pipefail` immediately after the shebang
   - One function per step, named `step_<snake_case_name>()`
   - Each function prints a heading (`echo "==> Step N: <Human readable name>"`), prints each sub-command the operator must run (indented), and calls `wait_for_enter` at the end
   - A `wait_for_enter()` utility function using `read -rp`
   - A `collect_context()` function that prompts for all context variables
   - A `main()` function that calls `collect_context` then each step in order, finishing with `echo "✓ Done."`
   - `main "$@"` as the last line of the file
   - Write the file to `./tmp/<name>_do_nothing.sh`

6. **Annotate automation potential**:
   - **Go**: Add a `// TODO: automate` comment above any `AddStep` call whose `Long()` body is a single deterministic command.
   - **Bash**: Add an inline `# TODO: automate` comment on functions whose body is a single deterministic command.
   This signals which steps are lowest-effort to convert from manual to automated.

7. **Write and verify the output file**:

   For Go:
   ```bash
   go run ./tmp/<name>_do_nothing.go
   ```
   Fix any compile errors before presenting the result.

   For Bash — make it executable and validate:
   ```bash
   chmod +x ./tmp/<name>_do_nothing.sh
   bash -n ./tmp/<name>_do_nothing.sh
   ```
   Fix any syntax errors reported before presenting the result.

8. **Present a summary** — Show the operator:
   - The path to the generated script and the implementation approach used
   - The list of steps and their automation potential
   - A note on which context variables are required at runtime
   - For Go: remind the operator to run `go mod init example.com/your-procedure` and `go get github.com/danslimmon/donothing` if they have not already

## Notes

- **Implementation choice**: Default to the Go (`danslimmon/donothing`) implementation unless the user explicitly requests bash or Go is not available. The Go library provides better structure, typed inputs/outputs between steps, and built-in Markdown generation.
- **Go module setup**: The first time a user adopts the Go approach in a new directory, remind them to run `go mod init example.com/your-procedure` and `go get github.com/danslimmon/donothing` before running or compiling the script.
- **Gradual automation in Go**: To automate a step, implement the logic as a Go function and call it directly in `main()` before `pcd.Execute()`. Remove the corresponding `AddStep` block so the procedure no longer prompts the operator for that step. Each step is isolated, so automating one step never requires changing any other. Once all steps are replaced with Go code, the procedure becomes a fully automated tool.
- **Markdown generation**: Running with `--print` calls `pcd.Render(os.Stdout)`, which emits the full procedure as Markdown — useful for runbooks or documentation. Step `Long()` content is rendered as prose. Output names referenced with `@@OutputName@@` are rendered with their names and descriptions.
- **Format auto-detection**: `extract_commands.py` inspects the first line for a JSON header (cast), checks whether the majority of lines match `  N  command` (history), and falls back to plain-text otherwise. Use `--format=` to override when auto-detection is incorrect.
- If the cast file contains only `"o"` (output) events and no `"i"` (input) events, `extract_commands.py` falls back to parsing command prompts from the output stream. Results may be less accurate; review carefully.
- **Text file format**: Lines beginning with `#` are treated as comments and skipped. Blank lines are ignored.
- **History format**: Accepts the output of `history` (bash/zsh), which prefixes each line with a sequence number: `  N  command`.
- Do-nothing scripts are **not** meant to be run in CI or automation pipelines — they are operator guides. Do not add flags or logic that suppress the interactive prompts.
- When a step involves waiting for an external system (a build, a deploy, a human approval), represent it as a `wait_for_enter` pause (bash) or a manual `step.Long()` with no automation yet added (Go) — do not attempt to poll or sleep.
- Manual steps (those with only `Long()` and no automation code) should remain pure operator guides: no side effects, no file writes, no network calls. The only action they take is printing instructions and waiting.
- Prefer `printf` over `echo` for portable output when the string may contain escape sequences; use `echo` for simple prose lines (bash approach).
