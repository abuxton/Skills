# HCL Patterns Reference

Canonical Terraform HCL patterns for the `terraform-vault-permanence` skill. All patterns use a **`locals` map + `for_each`** structure so that new Vault writes require only an addition to the locals data object — no changes to resource block structure.

---

## Directory layout

```text
vault-permanence/
├── .gitignore
├── versions.tf
├── variables.tf
└── main.tf
```

---

## `.gitignore`

```gitignore
# Terraform state and sensitive variable files
.terraform/
.terraform.lock.hcl
terraform.tfstate
terraform.tfstate.backup
*.tfvars
*.auto.tfvars
```

---

## `versions.tf`

```hcl
terraform {
  required_version = ">= 1.3.0"

  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "~> 4.0"
    }
  }
}

provider "vault" {
  address   = var.vault_address
  token     = var.vault_token
  namespace = var.vault_namespace != "" ? var.vault_namespace : null
}
```

---

## `variables.tf`

```hcl
variable "vault_address" {
  description = "Address of the Vault server."
  type        = string
  default     = "http://127.0.0.1:8200"
}

variable "vault_token" {
  description = "Vault authentication token."
  type        = string
  sensitive   = true
}

variable "vault_namespace" {
  description = "Vault namespace (leave empty for root namespace)."
  type        = string
  default     = ""
}
```

---

## `main.tf` — full pattern

The `locals` block is the **single source of truth** for all Vault writes. To add a new mount or secret, append a new entry to the relevant map and re-run smoke tests.

```hcl
locals {
  # -----------------------------------------------------------------------
  # Vault mounts (secrets engine enablement)
  # key   = mount path
  # value = engine configuration
  # To add a mount: append a new key/value entry below.
  # -----------------------------------------------------------------------
  vault_mounts = {
    "secret" = {
      type        = "kv"
      description = "KV v2 secrets engine"
      options     = { version = "2" }
    }
    # "app/config" = {
    #   type        = "kv"
    #   description = "Application configuration secrets"
    #   options     = { version = "2" }
    # }
  }

  # -----------------------------------------------------------------------
  # KV v2 secrets
  # key   = secret path within the mount (e.g. "myapp/database")
  # value = { mount, data }
  # To add a secret: append a new key/value entry below.
  # -----------------------------------------------------------------------
  vault_kv_v2_secrets = {
    "myapp/database" = {
      mount = "secret"
      data  = {
        username = "db_admin"
        # password = var.db_password  # use a variable for sensitive values
      }
    }
    # "myapp/api" = {
    #   mount = "secret"
    #   data  = {
    #     api_key = "replace-me"
    #   }
    # }
  }

  # -----------------------------------------------------------------------
  # KV v1 secrets (only needed when mount options.version = "1")
  # key   = secret path within the mount
  # value = { mount, data }
  # -----------------------------------------------------------------------
  vault_kv_v1_secrets = {
    # "legacy/config" = {
    #   mount = "legacy"
    #   data  = {
    #     setting = "value"
    #   }
    # }
  }
}

# ---------------------------------------------------------------------------
# vault_mount — one resource block manages all mounts via for_each
# ---------------------------------------------------------------------------
resource "vault_mount" "this" {
  for_each    = local.vault_mounts

  path        = each.key
  type        = each.value.type
  description = each.value.description
  options     = each.value.options
}

# ---------------------------------------------------------------------------
# vault_kv_secret_v2 — one resource block manages all KV v2 secrets
# ---------------------------------------------------------------------------
resource "vault_kv_secret_v2" "this" {
  for_each = local.vault_kv_v2_secrets

  mount     = each.value.mount
  name      = each.key
  data_json = jsonencode(each.value.data)

  depends_on = [vault_mount.this]
}

# ---------------------------------------------------------------------------
# vault_kv_secret — one resource block manages all KV v1 secrets
# Omit this block if vault_kv_v1_secrets is empty.
# ---------------------------------------------------------------------------
resource "vault_kv_secret" "this" {
  for_each = local.vault_kv_v1_secrets

  path      = "${each.value.mount}/${each.key}"
  data_json = jsonencode(each.value.data)

  depends_on = [vault_mount.this]
}
```

---

## Smoke-test commands

Run in the `vault-permanence/` directory in order. Fix any failure before proceeding.

```bash
# 1. Lint
tflint --init
tflint

# 2. Format check (no changes should be required after generation)
terraform fmt -check -recursive

# 3. Initialise (no remote backend required for smoke testing)
terraform init -backend=false

# 4. Validate syntax and schema
terraform validate

# 5. Plan (requires Vault credentials; acceptable to see auth errors in CI)
terraform plan
```

Expected results:

| Command | Pass condition |
| ------- | -------------- |
| `tflint` | Exit 0, zero errors |
| `terraform fmt -check` | Exit 0 (no diff) |
| `terraform validate` | `Success! The configuration is valid.` |
| `terraform plan` | Plan succeeds or fails only on Vault auth (not on HCL errors) |

---

## Adding a new write (extensibility pattern)

When a future `write_secret` call adds `myapp/cache` to the `secret` mount:

1. Execute `write_secret(mount="secret", path="myapp/cache", key="host", value="redis.internal")` via Vault MCP.
1. Append to `local.vault_kv_v2_secrets` in `main.tf`:

   ```hcl
   "myapp/cache" = {
     mount = "secret"
     data  = {
       host = "redis.internal"
     }
   }
   ```

1. Re-run smoke tests (`tflint`, `terraform fmt -check`, `terraform validate`, `terraform plan`).
1. Run `terraform apply` to reconcile Terraform state with the live Vault write.

---

## Sensitive values

When a secret value is sensitive (password, API key, certificate):

- Do **not** hardcode the value in the `locals` map.
- Declare a `variable` block in `variables.tf` with `sensitive = true`.
- Reference it in the locals map: `password = var.db_password`.
- Set the value in `terraform.tfvars` (which is `.gitignore`d).

Example addition to `variables.tf`:

```hcl
variable "db_password" {
  description = "Database password stored in Vault."
  type        = string
  sensitive   = true
}
```

Example reference in `main.tf` locals:

```hcl
"myapp/database" = {
  mount = "secret"
  data  = {
    username = "db_admin"
    password = var.db_password
  }
}
```
