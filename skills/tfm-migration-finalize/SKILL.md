---
name: tfm-migration-finalize
description: 'Finalise a TFE/TFC migration by locking source workspaces, removing source VCS connections, and verifying the destination organisation using the tfm CLI.'
---

# TFM Migration — Finalise Sub-skill

Complete the migration by locking source workspaces to prevent new runs, optionally removing VCS connections from the source (so runs are no longer triggered there), and confirming the destination organisation is healthy.

## Role

You are an expert in safely completing Terraform Enterprise/Cloud migrations. You understand that finalisation involves potentially destructive operations — locking workspaces and removing VCS connections on the source — and you never proceed without explicit confirmation.

- Pause and ask for confirmation before every destructive operation
- Lock workspaces on the source to prevent concurrent runs during cutover
- Optionally remove VCS connections on the source after the user confirms migration is complete
- Provide a final migration summary

## Prerequisites

- All earlier migration phases (workspaces, state, variable sets) completed successfully
- `CONFIG_PATH` is known from the setup phase
- The user has manually verified that the destination organisation looks correct

## Workflow

### Step 1 — Final pre-finalisation check

Ask:
> "Before finalising, confirm that you have verified the destination organisation and are ready to lock the source workspaces. Once locked, new runs in the source will be prevented. Do you want to proceed? (yes/no)"

If no, stop and return to the user without taking any action.

### Step 2 — Lock source workspaces

Lock all workspaces in scope on the source side to prevent new Terraform runs from starting while the migration is being verified:

```bash
tfm lock workspaces --config "$CONFIG_PATH"
```

Display the full output to the user.

Ask:
> "Source workspaces have been locked. You can unlock them at any time with `tfm unlock workspaces`. Do you want to continue to VCS clean-up? (yes/no)"

### Step 3 — Optional: remove VCS connections from source workspaces

> **Warning:** This is a destructive operation. Removing VCS connections from source workspaces means VCS-triggered runs will no longer be possible on the source. The workspaces themselves are **not** deleted. VCS connections can be restored manually if needed.

Ask:
> "Do you want to remove VCS connections from the source workspaces now? This will prevent VCS-triggered runs on the source. (yes/no)"

If yes, run:

```bash
tfm delete workspaces-vcs --config "$CONFIG_PATH"
```

> Note: `tfm` will ask for confirmation before proceeding. Review the output carefully and confirm when prompted.

Display the full output to the user.

Ask:
> "VCS connections have been removed from source workspaces. Does this look correct? (yes/no)"

### Step 4 — Optional: unlock destination workspaces

If the destination workspaces were locked during any earlier phase (for example, if a pre-migration lock was applied), unlock them now:

Ask:
> "Do the destination workspaces need to be unlocked? (yes/no)"

If yes, run:

```bash
tfm unlock workspaces --side destination --config "$CONFIG_PATH"
```

Display the output to the user.

### Step 5 — Final verification checklist

Display the following checklist and ask the user to confirm each item:

```text
Please confirm the following before completing the migration:

  [ ] Destination workspaces are present and correctly named
  [ ] Terraform state is visible in destination workspaces
  [ ] Variable sets are present in the destination organisation
  [ ] VCS connections in the destination are pointing to the correct repositories
  [ ] Agent pool assignments are correct in the destination
  [ ] Source workspaces are locked (runs will not start on the source)
  [ ] Any VCS connections removed from source are intentional
```

Ask:
> "Have you confirmed all items above? (yes/no)"

### Step 6 — Final summary

Display the completed migration summary:

```text
🎉 Migration finalised
   Config file:                    <CONFIG_PATH>
   Source organisation:            <src_tfe_org> @ <src_tfe_hostname>
   Destination organisation:       <dst_tfc_org> @ <dst_tfc_hostname>
   Source workspaces locked:       yes
   Source VCS connections removed: yes/no/skipped
   Destination workspaces unlocked: yes/no/skipped

Next steps:
  - Monitor the destination organisation for a period to confirm stability
  - Decommission the source TFE/TFC organisation when ready
  - To unlock the source at any time: tfm unlock workspaces --config <CONFIG_PATH>
```

## Error Handling

- If `tfm lock workspaces` exits non-zero, display the full output and stop.
- If `tfm delete workspaces-vcs` exits non-zero, display the full output and stop. Do not attempt to retry automatically — VCS removal is partially destructive.
- If the user answers "no" to any confirmation, stop and ask what they would like to do.
