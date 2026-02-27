#!/usr/bin/env python3
"""
extract_commands.py — Extract the command sequence from an asciinema v3 .cast file.

Strategy (in preference order):
  1. Collect "i" (stdin) events, join characters into lines, and yield each
     line that ends with a newline (i.e. a submitted command).
  2. If no "i" events are present, fall back to reconstructing the visible
     output stream and heuristically extracting lines that follow a shell
     prompt pattern ($ , % , ❯ , > ).

Usage:
    python3 extract_commands.py <file.cast>

Output:
    Numbered list of commands to stdout, one per line:
        1  git status
        2  git checkout -b feature/my-branch
        ...
"""

import json
import re
import sys
from pathlib import Path


# Matches common shell prompt endings, capturing the command that follows.
PROMPT_RE = re.compile(
    r"(?:[$%❯>])\s+(.+)$",
    re.MULTILINE,
)

# ANSI escape sequence stripper
ANSI_ESCAPE = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub("", text)


def extract_via_input_events(events: list) -> list[str]:
    """Reconstruct commands from "i" (stdin) events."""
    buffer = ""
    commands: list[str] = []
    for event in events:
        if len(event) != 3 or event[1] != "i":
            continue
        data: str = event[2]
        for ch in data:
            if ch in ("\r", "\n"):
                cmd = buffer.strip()
                if cmd:
                    commands.append(cmd)
                buffer = ""
            elif ch == "\x7f":  # backspace
                buffer = buffer[:-1]
            else:
                buffer += ch
    if buffer.strip():
        commands.append(buffer.strip())
    return commands


def extract_via_output_events(events: list) -> list[str]:
    """Fall back: reconstruct visible output and grep for prompt lines."""
    output = "".join(
        event[2] for event in events if len(event) == 3 and event[1] == "o"
    )
    output = strip_ansi(output)
    commands: list[str] = []
    for match in PROMPT_RE.finditer(output):
        cmd = match.group(1).strip()
        if cmd:
            commands.append(cmd)
    return commands


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: extract_commands.py <file.cast>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        print("ERROR: empty cast file", file=sys.stderr)
        sys.exit(1)

    events: list = []
    for line in lines[1:]:   # skip header
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    has_input = any(len(e) == 3 and e[1] == "i" for e in events)
    commands = (
        extract_via_input_events(events)
        if has_input
        else extract_via_output_events(events)
    )

    if not commands:
        print("No commands found in cast file.", file=sys.stderr)
        sys.exit(1)

    for i, cmd in enumerate(commands, start=1):
        print(f"{i:>3}  {cmd}")


if __name__ == "__main__":
    main()
