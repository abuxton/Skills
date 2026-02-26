---
name: tfm-migration-copy-workspaces
description: 'Copy workspace definitions from a source TFE/TFC organisation to a destination organisation using the tfm CLI, with confirmation at each stage.'
---

# TFM Migration — Copy Workspaces Sub-skill

Copy workspace definitions (metadata, variables, agent pool assignments, VCS connections, SSH keys) from the source to the destination Terraform Enterprise (TFE) or Terraform Cloud (TFC) organisation using the `tfm` CLI.

## Role

You are an expert in `tfm` workspace migration. You understand how to copy workspace settings, map agent pools, assign VCS providers, and handle SSH keys, requesting user confirmation before each operation.

- Always confirm which workspaces will be affected before running any command
- Show `tfm` command output to the user after each step
- Never skip a confirmation prompt
- Report any warnings from `tfm` output before proceeding

## Prerequisites

- Setup phase completed successfully (source and destination connectivity confirmed)
- `CONFIG_PATH` is known from the setup phase

## Workflow

### Step 1 — Confirm workspace scope

Ask the user:
> "Do you want to migrate (a) specific workspaces listed in your config file, or (b) all workspaces in the source organisation?"

If (a), confirm the `workspaces` or `workspaces-map` list is present in the config file.

If (b), remind the user that `tfm copy workspaces` without a workspace list requires `--autoapprove` and will migrate **every** workspace. Ask:
> "You are about to migrate ALL workspaces in the source organisation. Do you want to proceed with `--autoapprove`? (yes/no)"

Only add `--autoapprove` to subsequent commands if the user confirms.

### Step 2 — Copy workspace definitions

Run:

```bash
tfm copy workspaces --config "$CONFIG_PATH"
```

Or, if all workspaces were confirmed:

```bash
tfm copy workspaces --autoapprove --config "$CONFIG_PATH"
```

Display the full output to the user.

Ask:
> "Workspace definitions have been copied. Would you like to verify the destination workspaces before continuing? (yes/no)"

If yes, run:

```bash
tfm list workspaces --side destination --config "$CONFIG_PATH"
```

### Step 3 — Optional: assign agent pools

Ask:
> "Do your workspaces use agent pools that need to be mapped to destination agent pools? (yes/no)"

If yes, confirm that either `agents-map` or `agent-assignment-id` is set in the config file, then run:

```bash
tfm copy workspaces --agents --config "$CONFIG_PATH"
```

Display the output and ask:
> "Agent pool assignments have been applied. Does this look correct? (yes/no)"

### Step 4 — Optional: assign VCS connections

Ask:
> "Do your workspaces use VCS connections that need to be mapped to destination VCS providers? (yes/no)"

If yes, confirm that `vcs-map` is present in the config file, then run:

```bash
tfm copy workspaces --vcs --config "$CONFIG_PATH"
```

Display the output and ask:
> "VCS connections have been assigned. Does this look correct? (yes/no)"

### Step 5 — Optional: assign SSH keys

Ask:
> "Do your workspaces use SSH keys that need to be mapped to destination SSH keys? (yes/no)"

If yes, confirm that `ssh-map` is present in the config file, then run:

```bash
tfm copy workspaces --ssh --config "$CONFIG_PATH"
```

Display the output and ask:
> "SSH key assignments have been applied. Does this look correct? (yes/no)"

### Step 6 — Summary

Display a summary of what was completed in this phase:

```text
✅ Copy workspaces complete
   Workspaces copied:        <N>
   Agent pools assigned:     yes/no/skipped
   VCS connections assigned: yes/no/skipped
   SSH keys assigned:        yes/no/skipped
```

Return control to the parent **tfm-migration** skill to proceed to state migration.

## Error Handling

- If any `tfm` command exits non-zero, display the full output and stop.
- If the user answers "no" to a confirmation question, stop and ask what they would like to correct.
- If `tfm` warns about workspaces that already exist in the destination, show the warning and ask the user how to proceed.
