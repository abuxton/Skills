# Skills

Agent skills for GitHub Copilot, built following the
[agentskills.io specification](https://agentskills.io/specification).

## Available Skills

| Name | Description |
| ---- | ----------- |
| [shields-badges](skills/shields-badges/SKILL.md) | Analyse a repository to identify its focus and technology stack, then apply appropriate [shields.io](https://shields.io) badges to markdown files. |
| [terraform-vault-permanence](skills/terraform-vault-permanence/SKILL.md) | Orchestrate Vault MCP write operations (`create_mount`, `write_secret`) and generate smoke-tested Terraform HCL that persists each write as infrastructure-as-code using a locals-map + `for_each` pattern. |

## Usage

Copy a skill folder to your local skills directory and reference it in your
Copilot prompts, or let the agent discover it automatically.

Each skill folder contains a `SKILL.md` instruction file and optional bundled
reference assets.
