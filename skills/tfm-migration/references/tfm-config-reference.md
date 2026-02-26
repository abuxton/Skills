# TFM Configuration File Reference

Full reference for the `tfm` HCL configuration file (`~/.tfm.hcl` or a file supplied via `--config`).

Use `tfm generate config` to produce a starter configuration file for quick editing.

## Minimum Configuration (TFE ↔ TFC migration)

```hcl
src_tfe_hostname = "tf.local.com"
src_tfe_org      = "source-org"
src_tfe_token    = "<owner token for source organisation>"

dst_tfc_hostname = "app.terraform.io"
dst_tfc_org      = "destination-org"
dst_tfc_token    = "<owner token for destination organisation>"
```

## Full Parameter Reference

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `src_tfe_hostname` | string | Yes (TFE/TFC migrations) | Hostname of the source TFE server or `app.terraform.io` for TFC |
| `src_tfe_org` | string | Yes (TFE/TFC migrations) | Source TFE/TFC organisation name |
| `src_tfe_token` | string | Yes (TFE/TFC migrations) | Owner token for the source organisation |
| `dst_tfc_hostname` | string | Yes (all migrations) | Hostname of the destination TFE server or `app.terraform.io` for TFC |
| `dst_tfc_org` | string | Yes (all migrations) | Destination TFE/TFC organisation name |
| `dst_tfc_token` | string | Yes (all migrations) | Owner token for the destination organisation |
| `dst_tfc_project_id` | string | No | Destination project ID; if unset the Default Project is used |
| `workspaces` | list(string) | No | Explicit list of workspace names to migrate; if omitted all workspaces are migrated |
| `exclude-workspaces` | list(string) | No | Workspaces to skip; conflicts with `workspaces` and `workspaces-map` |
| `workspaces-map` | list(string) | No | `source-name=destination-name` pairs; takes precedence over `workspaces` |
| `projects` | list(string) | No | List of project names to migrate |
| `projects-map` | list(string) | No | `source-name=destination-name` pairs for projects |
| `agents-map` | list(string) | No | `source-agent-pool-id=destination-agent-pool-id` pairs; conflicts with `agent-assignment-id` |
| `agent-assignment-id` | string | No | Single destination agent pool ID to assign to all workspaces; conflicts with `agents-map` |
| `varsets-map` | list(string) | No | `source-varset-name=destination-varset-name` pairs |
| `vcs-map` | list(string) | No | `source-vcs-oauth-id=destination-vcs-oauth-id` or GitHub App ID pairs |
| `ssh-map` | list(string) | No | `source-ssh-key-id=destination-ssh-key-id` pairs |
| `exclude-ws-remote-state-resources` | bool | No | Skip workspaces that use remote state data sources |
| `repos_to_clone` | list(string) | No | VCS repository names to clone (used with `tfm core clone`) |
| `vcs_type` | string | Yes (`tfm core`) | VCS provider type: `"github"` or `"gitlab"` |
| `vcs_provider_id` | string | Yes (`tfm core link-vcs`) | VCS provider ID in the destination |
| `clone_repos_path` | string | Yes (`tfm core`) | Local filesystem path to clone repositories into |
| `github_token` | string | Yes (`tfm core` + GitHub) | GitHub personal access token |
| `github_organization` | string | Yes (`tfm core` + GitHub) | GitHub organisation name |
| `github_username` | string | Yes (`tfm core` + GitHub) | GitHub username |
| `gitlab_token` | string | Yes (`tfm core` + GitLab) | GitLab personal access token |
| `gitlab_username` | string | Yes (`tfm core` + GitLab) | GitLab username |
| `gitlab_group` | string | Yes (`tfm core` + GitLab) | GitLab group name |
| `commit_message` | string | Yes (`tfm core remove-backend`) | Commit message for the backend-removal branch |
| `commit_author_name` | string | Yes (`tfm core remove-backend`) | Author name for the backend-removal commit |
| `commit_author_email` | string | Yes (`tfm core remove-backend`) | Author email for the backend-removal commit |

## Environment Variable Equivalents

All configuration values can be supplied as environment variables instead of (or to override) the config file.

```bash
export SRC_TFE_HOSTNAME="tf.local.com"
export SRC_TFE_ORG="source-org"
export SRC_TFE_TOKEN="<owner token>"
export DST_TFC_HOSTNAME="app.terraform.io"
export DST_TFC_ORG="destination-org"
export DST_TFC_TOKEN="<owner token>"
export DST_TFC_PROJECT_ID="prj-xxxxxxxxxxxx"
```

## Workspace List Example

```hcl
workspaces = [
  "appAFrontEnd",
  "appABackEnd",
  "appBDataLake",
  "appBInfra"
]
```

## Workspace Map Example

```hcl
"workspaces-map" = [
  "tf-demo-workflow=dst-demo-workflow",
  "api-test=dst-api-test"
]
```

## Agent Pool Map Example

```hcl
agents-map = [
  "apool-DgzkahoomwHsBHcJ=apool-vbrJZKLnPy6aLVxE",
  "apool-DgzkahoomwHsBHc3=apool-vbrJZKLnPy6aLVx4"
]
```

## Variable Set Map Example

```hcl
varsets-map = [
  "Azure-creds=New-Azure-Creds",
  "aws-creds2=New-AWS-Creds"
]
```

## VCS Map Example

```hcl
vcs-map = [
  "ot-5uwu2Kq8mEyLFPzP=ot-coPDFTEr66YZ9X9n",
  "ghain-sc8a3b12S212gy45=ghain-B3asgvX3oF541aDo"
]
```

## SSH Key Map Example

```hcl
ssh-map = [
  "sshkey-sPLAKMcqnWtHPSgx=sshkey-CRLmPJpoHwsNFAoN"
]
```

## Security Notes

- **Never commit** tokens or credentials to source control
- Use environment variables from a secrets manager in CI/CD pipelines
- Multiple config files can be created to segment large migrations
