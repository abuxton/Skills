# Conservative Unix-first `.gitattributes` defaults

Use this baseline when a repository is developed primarily on Unix-like systems and needs predictable line-ending behavior without an aggressive or language-exhaustive template.

```gitattributes
* text=auto

# Unix shell and automation
*.sh    text eol=lf
*.bash  text eol=lf
*.zsh   text eol=lf
*.fish  text eol=lf

# Common source, config, and docs that should stay LF in Unix-first repos
*.py    text eol=lf
*.rb    text eol=lf
*.pl    text eol=lf
*.js    text eol=lf
*.ts    text eol=lf
*.json  text eol=lf
*.toml  text eol=lf
*.yaml  text eol=lf
*.yml   text eol=lf
*.md    text eol=lf

# Windows-native scripts keep CRLF when checked out
*.bat   text eol=crlf
*.cmd   text eol=crlf
*.ps1   text eol=crlf

# Obvious binaries and archives
*.png   binary
*.jpg   binary
*.jpeg  binary
*.gif   binary
*.pdf   binary
*.zip   binary
*.gz    binary
*.tar   binary
```

## Decision guide

- Start with `* text=auto`, then add explicit `eol` rules only where the working-tree line ending truly matters.
- Avoid `* text=auto eol=lf` as a blanket rule; it can surprise repositories that legitimately contain Windows-oriented files.
- Use `binary` for assets and archives that should never be normalized or diffed as text.
- If a repository already has narrower rules, preserve them unless they are clearly incorrect.
- If a file should stop inheriting an attribute from a broad rule, prefer a targeted override or `!attr` over deleting shared defaults.
- Use `.git/info/attributes` for local-only preferences that should not be committed.
