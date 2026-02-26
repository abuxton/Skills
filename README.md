# Skills

Agent skills for GitHub Copilot, built following the
[agentskills.io specification](https://agentskills.io/specification).

## Available Skills

| Name | Description |
| ---- | ----------- |
| [shields-badges](skills/shields-badges/SKILL.md) | Analyse a repository to identify its focus and technology stack, then apply appropriate [shields.io](https://shields.io) badges to markdown files. |
| [tfm-migration](skills/tfm-migration/SKILL.md) | Run a stepped TFE/TFC migration using the [`tfm`](https://github.com/hashicorp-services/tfm) CLI. Orchestrates the full migration workflow across setup, workspace copy, state copy, variable set copy, and finalisation phases. |
| [tfm-migration-setup](skills/tfm-migration-setup/SKILL.md) | Validate a `tfm` configuration file and verify connectivity to source and destination TFE/TFC organisations before starting a migration. |
| [tfm-migration-copy-workspaces](skills/tfm-migration-copy-workspaces/SKILL.md) | Copy workspace definitions (metadata, agent pools, VCS connections, SSH keys) from source to destination using `tfm`. |
| [tfm-migration-copy-state](skills/tfm-migration-copy-state/SKILL.md) | Copy Terraform state files from source workspaces to destination workspaces using `tfm`. |
| [tfm-migration-copy-varsets](skills/tfm-migration-copy-varsets/SKILL.md) | Copy variable sets from source to destination TFE/TFC organisation using `tfm`. |
| [tfm-migration-finalize](skills/tfm-migration-finalize/SKILL.md) | Finalise a migration by locking source workspaces, removing source VCS connections, and verifying the destination using `tfm`. |

## Usage

Copy a skill folder to your local skills directory and reference it in your
Copilot prompts, or let the agent discover it automatically.

Each skill folder contains a `SKILL.md` instruction file and optional bundled
reference assets.
