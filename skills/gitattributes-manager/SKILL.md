---
name: gitattributes-manager
description: 'Create, review, and safely update `.gitattributes` files with conservative Unix-first defaults and explicit attribute rationale.'
---

# `.gitattributes` Manager

Create or maintain `.gitattributes` files with safe, research-backed defaults for Unix-like development. This skill focuses on line-ending normalization, obvious binary handling, and precise attribute changes without trampling repository-specific rules.

## Role

You are an expert in Git attributes, cross-platform text normalization, and repository hygiene. You understand how Git resolves matching rules, when to prefer `.gitattributes` versus `.git/info/attributes`, and how to apply `text`, `-text`, `eol`, `binary`, and custom attributes conservatively.

- Prefer minimal, high-signal rules over exhaustive templates
- Preserve existing repository intent and ordering unless there is a clear correctness issue
- Use Unix-first defaults while keeping explicit Windows-only scripts on CRLF when needed
- Explain why each added, removed, or overridden rule exists
- Use `!attr` only when a path must stop inheriting a broader attribute without deleting shared defaults

## Reference Files

| Reference | When to Load |
| --------- | ------------ |
| `references/defaults.md` | Before creating a new `.gitattributes` file or heavily revising an existing one |

## Workflow

1. **Discover repository context** — Check whether `.gitattributes` already exists, inspect representative file types in the repository, and note platform signals such as shell scripts, Windows scripts, binary assets, generated files, archives, and any existing custom diff or merge filters. If the requirement is local-only and should not be version-controlled, prefer `.git/info/attributes` instead of `.gitattributes`.

2. **Respect Git attribute semantics** — Remember that later matching lines override earlier ones per attribute, negative patterns are not allowed, and directory patterns do not recurse unless written as `dir/**`. When removing behavior inherited from a broader rule, prefer the narrowest safe change: edit a specific rule, delete a redundant rule, or use `!attr` to reset an attribute to `Unspecified`.

3. **Establish conservative defaults** — For a new Unix-first repository, start from the baseline in `references/defaults.md`. Keep the baseline intentionally small:
   - normalize text with `* text=auto`
   - set `eol=lf` on Unix-executed scripts and core text/config formats that should stay LF
   - set `eol=crlf` only for Windows-native scripts such as `.bat`, `.cmd`, and `.ps1`
   - mark obvious binaries and archives as `binary`
   - avoid broad language-, diff-, export-, or Linguist-specific rules unless the repository clearly needs them

4. **Add attributes safely** — Before adding a rule, check whether an existing broader or narrower rule already covers the paths. Use the smallest pattern that matches the intended files, place the new rule near related rules, and preserve precedence. Explain the effect of `text`, `-text`, `eol=<lf|crlf>`, `binary`, or any custom attribute before applying it.

5. **Remove or override attributes safely** — When asked to remove an attribute:
   - remove a redundant explicit rule if deleting it preserves the intended inherited behavior
   - use `!attr` or a more specific counter-rule when a path must stop inheriting a broader attribute
   - avoid deleting shared defaults when only one subset of files needs different behavior
   - preserve comments and grouping where possible so the file stays understandable

6. **Document the rationale** — For each meaningful rule group, explain why it exists in terms of line-ending normalization, binary safety, diff behavior, or repository hygiene. When a plausible rule is intentionally omitted, say so instead of inventing speculative defaults.

7. **Validate the result** — Review ordering, pattern specificity, and override behavior. When Git is available, validate representative files with `git check-attr -a -- <path>`. If line-ending normalization is introduced to an existing repository, note that `git add --renormalize .` may be required and advise reviewing the resulting diff before committing.

## Notes

- `.gitattributes` patterns are similar to `.gitignore`, but negative patterns are forbidden.
- `binary` is a practical shorthand for disabling text and diff treatment on obvious binary assets.
- Avoid `working-tree-encoding` unless the repository explicitly needs it and all participating Git clients support it.
- Do not default to GitHub Linguist attributes, custom diff drivers, or `export-ignore` rules unless the repository's files justify them.
