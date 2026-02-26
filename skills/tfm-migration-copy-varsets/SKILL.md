---
name: tfm-migration-copy-varsets
description: 'Copy variable sets from a source TFE/TFC organisation to a destination organisation using the tfm CLI, with confirmation at each stage.'
---

# TFM Migration — Copy Variable Sets Sub-skill

Copy variable sets from the source Terraform Enterprise (TFE) or Terraform Cloud (TFC) organisation to the destination organisation using the `tfm` CLI.

## Role

You are an expert in Terraform Cloud/Enterprise variable sets and `tfm` migration. You help users copy variable sets safely, including renaming them at the destination when required.

- Always confirm which variable sets will be copied
- Show `tfm` command output after each step
- Never print variable values to the terminal
- Request confirmation before executing commands

## Prerequisites

- Copy workspaces phase completed successfully
- `CONFIG_PATH` is known from the setup phase

## Workflow

### Step 1 — Confirm variable set scope

Ask the user:
> "Do you want to copy (a) ALL variable sets from the source organisation, or (b) only specific variable sets listed in a `varsets-map` in your config file?"

If (b), confirm that `varsets-map` is present in the config file with entries in the format `"source-varset-name=destination-varset-name"`.

Remind the user:
> "Variable set contents (including sensitive variable values) will be copied from the source to the destination. The source variable sets will not be modified."

Ask:
> "Are you ready to copy variable sets? (yes/no)"

### Step 2 — Copy variable sets

**Option (a) — all variable sets:**

```bash
tfm copy varsets --config "$CONFIG_PATH"
```

**Option (b) — only mapped variable sets (uses `varsets-map` from config):**

```bash
tfm copy varsets --config "$CONFIG_PATH"
```

> Note: `tfm copy varsets` automatically uses the `varsets-map` if it is present in the config file.

Display the full output to the user after the command completes.

### Step 3 — Verify variable sets in destination

Ask:
> "Would you like to list the variable sets now visible in the destination organisation? (yes/no)"

If yes, run:

```bash
tfm list varsets --side destination --config "$CONFIG_PATH"
```

Ask:
> "Do the variable sets in the destination look correct? (yes/no)"

If no, stop and ask the user to investigate before proceeding.

### Step 4 — Summary

Display a summary of what was completed in this phase:

```text
✅ Copy variable sets complete
   Scope:       all / mapped only
   Config file: <CONFIG_PATH>
```

Return control to the parent **tfm-migration** skill to proceed to the finalise phase.

## Error Handling

- If `tfm` exits non-zero, display the full output and stop.
- If the user answers "no" to any confirmation, stop and ask what they would like to do.
- If `varsets-map` contains an empty entry or duplicate, `tfm` will return an error — instruct the user to correct the config file.
