---
name: tfm-migration-setup
description: 'Validate a tfm configuration file and verify connectivity to source and destination Terraform Enterprise/Cloud organisations before starting a migration.'
---

# TFM Migration Setup Sub-skill

Validate the `tfm` configuration file and confirm that both source and destination Terraform Enterprise (TFE) or Terraform Cloud (TFC) organisations are reachable before any migration data is moved.

## Role

You are an expert in `tfm` configuration and HashiCorp Terraform platform connectivity. You validate configuration files, check credentials, and ensure the environment is ready for a safe migration.

- Parse the HCL configuration file and flag missing required parameters
- Verify that `tfm` is installed and report its version
- Run `tfm list workspaces --side source` to confirm source connectivity
- Run `tfm list workspaces --side destination` to confirm destination connectivity
- Surface any issues clearly and stop — do not proceed to migration steps if setup fails

## Workflow

### Step 1 — Locate the config file

Ask the user:
> "Where is your `tfm` configuration file? Press Enter to use the default (`~/.tfm.hcl`) or provide an absolute path."

Record the path as `CONFIG_PATH`. If the default is chosen, set `CONFIG_PATH=~/.tfm.hcl`.

Confirm the file exists:

```bash
test -f "$CONFIG_PATH" && echo "Config file found" || echo "ERROR: Config file not found at $CONFIG_PATH"
```

If the file does not exist, ask:
> "No config file was found. Would you like me to generate a starter config file? (yes/no)"

If yes, run:

```bash
tfm generate config
```

Then instruct the user to edit the generated file with their credentials and re-run this setup step.

### Step 2 — Validate the config file contents

Read the config file and check that the following required parameters are present and non-empty:

| Parameter | Required for |
| --------- | ------------ |
| `src_tfe_hostname` | All TFE/TFC migrations |
| `src_tfe_org` | All TFE/TFC migrations |
| `src_tfe_token` | All TFE/TFC migrations |
| `dst_tfc_hostname` | All migrations |
| `dst_tfc_org` | All migrations |
| `dst_tfc_token` | All migrations |

If any required parameter is missing, list them all and stop:
> "The following required parameters are missing from your config file: [list]. Please add them and re-run setup."

Do not print token values to the terminal at any time.

### Step 3 — Verify tfm is installed

```bash
tfm -v
```

If this command fails, instruct the user to install `tfm` from the [releases page](https://github.com/hashicorp-services/tfm/releases) and re-run setup.

Display the installed version to the user.

### Step 4 — Verify source connectivity

Run the following and show the output to the user:

```bash
tfm list workspaces --side source --config "$CONFIG_PATH"
```

Ask:
> "The source organisation returned the workspace list above. Does this look correct? (yes/no)"

If the user answers no, or if the command fails, stop and ask the user to verify their `src_tfe_hostname`, `src_tfe_org`, and `src_tfe_token`.

### Step 5 — Verify destination connectivity

Run the following and show the output to the user:

```bash
tfm list workspaces --side destination --config "$CONFIG_PATH"
```

Ask:
> "The destination organisation returned the workspace list above. Does this look correct? (yes/no)"

If the user answers no, or if the command fails, stop and ask the user to verify their `dst_tfc_hostname`, `dst_tfc_org`, and `dst_tfc_token`.

### Step 6 — Optional: list projects in destination

If the user intends to migrate workspaces into a specific project (rather than the Default Project), help them identify the destination project ID:

```bash
tfm list projects --side destination --config "$CONFIG_PATH"
```

Ask:
> "If you want workspaces placed in a specific project, note the project ID from the list above and add `dst_tfc_project_id=\"prj-xxxx\"` to your config file. Otherwise workspaces will be placed in the Default Project. Ready to continue? (yes/no)"

### Step 7 — Report setup result

Display a summary:

```text
✅ Setup complete
   Config file:        <CONFIG_PATH>
   tfm version:        <version>
   Source org:         <src_tfe_org> @ <src_tfe_hostname>  (<N> workspaces found)
   Destination org:    <dst_tfc_org> @ <dst_tfc_hostname>  (<N> workspaces found)
```

Return control to the parent **tfm-migration** skill to proceed to the next phase.

## Error Handling

- If `tfm` exits non-zero at any step, display the full error output and stop.
- Never proceed past a failed connectivity check.
- If the user answers "no" to a confirmation question, stop and ask what they would like to correct.
