---
name: terraform-vault-permanence
description: 'Orchestrate Vault MCP write operations (create_mount, write_secret) and generate smoke-tested Terraform HCL that persists each write as infrastructure-as-code using a locals-map + for_each pattern.'
---

# Terraform Vault Permanence Skill

Given a set of Vault write operations, perform them through the Vault MCP server and then produce validated, formatted Terraform HCL that reproduces those writes as durable infrastructure code. All generated HCL uses a **locals map + `for_each`** pattern so that future writes require only an addition to the `locals` data object — no structural changes to the resource blocks.

## Role

You are an expert in both HashiCorp Vault operations and Terraform infrastructure-as-code. You understand the Vault MCP server write tools (`create_mount`, `write_secret`), the [hashicorp/vault](https://registry.terraform.io/providers/hashicorp/vault/latest) Terraform provider, and HCL best practices.

- Execute Vault MCP write operations on behalf of the user
- Translate each write into a corresponding Terraform resource
- Structure HCL so that all resource data lives in a single `locals` block and resources use `for_each` over that map
- Smoke-test every generated configuration with `tflint`, `terraform validate`, `terraform fmt`, and `terraform plan` before declaring success
- Fix any issues surfaced by smoke tests before returning output

## Vault MCP Write Tools

Refer to `references/vault-mcp-write-tools.md` for the full parameter reference. The two write tools used by this skill are:

| Tool | Vault MCP operation |
| ---- | ------------------- |
| `create_mount` | Enables a new secrets engine at a given path |
| `write_secret` | Writes a key/value pair to a KV secrets engine |

## Terraform Resources

Refer to `references/hcl-patterns.md` for canonical HCL examples. The Terraform resources that correspond to each Vault MCP write operation are:

| Vault MCP tool | Terraform resource |
| -------------- | ------------------ |
| `create_mount` (type `kv` / `kv-v2`) | `vault_mount` |
| `write_secret` on a KV v2 mount | `vault_kv_secret_v2` |
| `write_secret` on a KV v1 mount | `vault_kv_secret` |

## Workflow

### 1. Gather intent

Ask the user (or infer from context) what they want to write to Vault:

- Which secrets engine **type** and **path** to mount (e.g. `kv-v2` at `secret/`)
- Which **secrets** to write (mount, path, key, value tuples)

Confirm the full list before proceeding.

### 2. Execute Vault MCP writes

For each mount the user requires:

```text
create_mount(type="kv-v2", path="<mount-path>", description="<description>")
```

For each secret the user requires:

```text
write_secret(mount="<mount-path>", path="<secret-path>", key="<key>", value="<value>")
```

Record every successful write — mount path, secret path, key name — for use in step 3.

### 3. Determine KV version per mount

After mounting, check whether each mount is KV v1 or KV v2 so the correct Terraform resource is used:

- `type = "kv"` with `options = { version = "2" }` → `vault_kv_secret_v2`
- `type = "kv"` with `options = { version = "1" }` or no version option → `vault_kv_secret`

### 4. Generate Terraform HCL

Produce a Terraform configuration in the target directory (default: `./vault-permanence/`) using the canonical structure from `references/hcl-patterns.md`:

1. **`versions.tf`** — provider version constraints for `hashicorp/vault`
2. **`variables.tf`** — input variables (Vault address, token, namespace)
3. **`main.tf`** — `locals` block containing all mount and secret data, followed by `vault_mount` and `vault_kv_secret_v2` / `vault_kv_secret` resource blocks using `for_each` over the corresponding locals map

The locals map is the **single point of change** for future writes: adding a new mount or secret requires only a new entry in the relevant locals map.

### 5. Smoke-test the HCL

Run each of the following commands in the generated directory, in order. Stop and fix any failure before proceeding to the next step.

```bash
tflint --init && tflint
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
terraform plan
```

Acceptable outcomes:

- `tflint` — zero errors (warnings are acceptable but should be noted)
- `terraform fmt -check` — exits 0 (no formatting changes required)
- `terraform validate` — `Success! The configuration is valid.`
- `terraform plan` — plan succeeds; note any expected diffs

If `terraform plan` requires real Vault credentials that are not available, run it with `-target` scoped to a null resource or accept the authentication error as expected and note it in the output.

### 6. Report results

Return to the user:

- Confirmation of all Vault MCP writes completed in step 2
- The full path of the generated Terraform configuration directory
- The content of `main.tf` (and other generated files if modified)
- A summary of smoke-test results
- Any warnings or caveats (e.g. sensitive values in `locals`, plan requiring live credentials)

## Security Considerations

- **Never hardcode secrets or tokens** in generated HCL. Use `variable` blocks with `sensitive = true` for the Vault token.
- When `write_secret` values contain sensitive data, mark the corresponding locals entry with a comment and advise the user to use `sensitive()` or move the value to a `terraform.tfvars` file that is `.gitignore`d.
- Generated files that contain secret values must not be committed to version control. Include a `.gitignore` entry for `terraform.tfvars` and `*.auto.tfvars` in the generated directory.
- Remind the user that `vault_kv_secret_v2` stores secret data in Terraform state; state should be encrypted and stored remotely.

## Extensibility

Because all resource data lives in the `locals` block, future Vault writes are appended by:

1. Using `write_secret` (or `create_mount`) via the Vault MCP to perform the live write
2. Adding the corresponding entry to the relevant locals map in `main.tf`
3. Re-running the smoke tests
4. Running `terraform apply` to reconcile state

No changes to resource block structure are required.
