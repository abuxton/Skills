# Vault MCP Write Tools Reference

The Vault MCP Server exposes the following **write** tools. This reference covers only write operations; read-only tools (`list_mounts`, `list_secrets`, `read_secret`) are out of scope for this skill.

## create_mount

Enables a new secrets engine at the given path in Vault.

### Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| `type` | Yes | Secrets engine type. Use `kv` for KV v1 or `kv-v2` for KV v2. |
| `path` | Yes | Path at which the engine is mounted (e.g. `secret`, `app/config`). |
| `description` | No | Human-readable description for the mount. |

### Example invocation

```json
{
  "tool": "create_mount",
  "parameters": {
    "type": "kv-v2",
    "path": "secret",
    "description": "KV v2 secrets engine"
  }
}
```

### Terraform equivalent — `vault_mount`

```hcl
resource "vault_mount" "this" {
  for_each    = local.vault_mounts
  path        = each.key
  type        = each.value.type
  description = each.value.description
  options     = each.value.options
}
```

---

## write_secret

Writes a single key/value pair to a path within a KV secrets engine.

### Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| `mount` | Yes | The mount path of the secrets engine (must already exist). |
| `path` | Yes | The path within the mount to write the secret to. |
| `key` | Yes | The key name of the secret. |
| `value` | Yes | The value to store. |

### Example invocation

```json
{
  "tool": "write_secret",
  "parameters": {
    "mount": "secret",
    "path": "myapp/database",
    "key": "username",
    "value": "db_admin"
  }
}
```

### Terraform equivalents

KV v2 — `vault_kv_secret_v2`:

```hcl
resource "vault_kv_secret_v2" "this" {
  for_each  = local.vault_kv_v2_secrets
  mount     = each.value.mount
  name      = each.key
  data_json = jsonencode(each.value.data)
}
```

KV v1 — `vault_kv_secret`:

```hcl
resource "vault_kv_secret" "this" {
  for_each  = local.vault_kv_v1_secrets
  path      = "${each.value.mount}/${each.key}"
  data_json = jsonencode(each.value.data)
}
```

---

## delete_mount

Removes a secrets engine from Vault. Included here for completeness; this skill does not generate Terraform code for deletions (use `terraform destroy` instead).

### Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| `path` | Yes | The mount path to remove. |

---

## Notes

- Multiple `write_secret` calls to the same path but different keys are **merged** by the Vault MCP server into a single secret at that path.
- When generating HCL, group all keys for a given `mount/path` combination into one `data` map so a single `vault_kv_secret_v2` (or `vault_kv_secret`) resource manages all keys for that path.
- The `create_mount` tool accepts `type = "kv-v2"` as a convenience alias; the Vault API and Terraform provider both use `type = "kv"` with `options = { version = "2" }`. Translate accordingly when generating HCL.
