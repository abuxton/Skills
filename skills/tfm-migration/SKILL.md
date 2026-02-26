---
name: tfm-migration
description: 'Run a stepped TFE/TFC migration using the tfm CLI. Guides the user through each phase of the migration, requesting confirmation at every action.'
---

# TFM Migration Skill

Guide the user through a complete Terraform Enterprise (TFE) or Terraform Cloud (TFC) migration using the [`tfm`](https://github.com/hashicorp-services/tfm) CLI. Each phase is a discrete step that requires explicit user confirmation before proceeding.

## Role

You are an expert in HashiCorp Terraform migrations. You understand the `tfm` CLI, its configuration file format, and the end-to-end workflow for migrating workspaces, state, variable sets, and VCS connections between TFE and TFC organisations.

- Always read and validate the `tfm` configuration file before executing any migration commands
- Pause and request user input between every phase
- Surface any errors or warnings from `tfm` output to the user before proceeding
- Never run destructive operations (delete, lock, VCS disconnect) without explicit user confirmation
- Prefer the `--autoapprove` flag only when the user has explicitly opted in

## Prerequisites

Before starting, confirm the following are in place:

1. `tfm` binary is installed and available in `$PATH` (`tfm -v` should print the version)
2. A valid `tfm` config file exists at `~/.tfm.hcl` or at a path the user will specify with `--config`
3. The user holds an **Owner token** for both the source and destination organisations
4. Network access to both the source TFE/TFC hostname and the destination TFE/TFC hostname

## Migration Phases

The migration is divided into the following ordered phases. Use the sub-skills listed below to execute each phase. **Pause and ask the user to confirm before starting the next phase.**

| Phase | Sub-skill | Description |
| ----- | --------- | ----------- |
| 1 | [tfm-migration-setup](../tfm-migration-setup/SKILL.md) | Validate the `tfm` config file and verify connectivity to source and destination |
| 2 | [tfm-migration-copy-workspaces](../tfm-migration-copy-workspaces/SKILL.md) | Copy workspace definitions from source to destination |
| 3 | [tfm-migration-copy-state](../tfm-migration-copy-state/SKILL.md) | Copy Terraform state from source workspaces to destination workspaces |
| 4 | [tfm-migration-copy-varsets](../tfm-migration-copy-varsets/SKILL.md) | Copy variable sets from source to destination |
| 5 | [tfm-migration-finalize](../tfm-migration-finalize/SKILL.md) | Lock source workspaces, remove VCS connections on source, and verify the migration |

## Workflow

### Step 0 — Identify migration scope

Ask the user:

1. What is the **migration type**?
   - TFE → TFC
   - TFC → TFE
   - TFC org → TFC org
   - TFE server → TFE server (consolidation)
2. What is the **path to the `tfm` config file**? (default: `~/.tfm.hcl`)
3. Should specific workspaces be migrated, or **all workspaces** in the source organisation?

Record the answers and pass them as context to each sub-skill.

### Step 1 — Setup and validation

Invoke the **tfm-migration-setup** sub-skill. Do not proceed until it reports success.

### Step 2 — Copy workspaces

Invoke the **tfm-migration-copy-workspaces** sub-skill.

After completion, display the list of workspaces that were created in the destination and ask:
> "All workspaces have been copied. Are you ready to proceed to state migration? (yes/no)"

### Step 3 — Copy state

Invoke the **tfm-migration-copy-state** sub-skill.

After completion, ask:
> "State migration is complete. Would you like to copy variable sets next? (yes/no)"

### Step 4 — Copy variable sets

Invoke the **tfm-migration-copy-varsets** sub-skill.

After completion, ask:
> "Variable sets have been copied. Are you ready to finalise the migration? This will lock source workspaces and optionally remove their VCS connections. (yes/no)"

### Step 5 — Finalise

Invoke the **tfm-migration-finalize** sub-skill.

After completion, display a migration summary and ask the user to verify their destination organisation manually before decommissioning the source.

## Error Handling

- If any `tfm` command exits with a non-zero status, display the full output to the user and **stop**.
- Do not attempt automatic retries on authentication errors or 403/401 responses.
- For rate-limit or transient errors, offer to retry after a short pause.

## Reference

See `references/tfm-config-reference.md` for a full list of supported configuration file parameters and environment variable equivalents.
