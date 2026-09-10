---
name: bob-sessions
description: Gather, list, inspect, search, and export Bob session IDs, conversation history, and tool executions from the local Bob SQLite database (bob.db). Use whenever the user asks to "list bob sessions", "show todays sessions", "inspect session <id>", "find bob tasks", "export session history", or review past Bob work.
---

# Bob Sessions Skill

Manage, query, search, and export Bob session history and tool usage trails directly from the local Bob SQLite database (`~/.bob/db/bob.db`).

## Role

You are an expert in Bob session analysis and telemetry inspection. You help users list past or current sessions, inspect prompt history, trace tool execution calls, and export session transcripts to Markdown or JSON.

## Key Capabilities

- **List sessions**: Filter by date (`today`, `yesterday`, or `YYYY-MM-DD`), relative days, status (`running`, `active`, `completed`, `error`), or task type (`normal`, `subagent`, `subtask`).
- **Search sessions**: Filter by session ID prefix, title, or prompt keywords.
- **Inspect session detail**: View message history, metadata, token consumption, context usage, and costs.
- **Trace tool executions**: Extract exact tool names, arguments, and return outputs chronologically.
- **Export transcripts**: Generate formatted Markdown or JSON transcripts of any session.

---

## Bundled CLI Tools

The skill provides production-tested Python utilities in `scripts/`:

| Script | Purpose | Common Flags |
|---|---|---|
| `list_sessions.py` | List & filter sessions | `--date today`, `--days 7`, `--status completed`, `--type subagent`, `-q <query>`, `--json` |
| `inspect_session.py` | Inspect single session & tools | `<session_id>`, `--tools`, `--limit 50`, `--json` |
| `export_session.py` | Export session to Markdown | `<session_id>`, `-o report.md` |

---

## Workflow

Follow these steps when the user asks about Bob sessions:

### 1. Discover and List Sessions

To find session IDs or inspect what was worked on:

```bash
# List sessions from today
python3 .agents/skills/bob-sessions/scripts/list_sessions.py --date today

# List sessions from the last 3 days
python3 .agents/skills/bob-sessions/scripts/list_sessions.py --days 3

# Search for a specific keyword in prompts or titles
python3 .agents/skills/bob-sessions/scripts/list_sessions.py -q "jira"

# Filter by subagents or errors
python3 .agents/skills/bob-sessions/scripts/list_sessions.py --type subagent
python3 .agents/skills/bob-sessions/scripts/list_sessions.py --status error
```

### 2. Inspect Session Details & History

To inspect what happened in a given session using its full or short ID:

```bash
# View session metadata and recent messages
python3 .agents/skills/bob-sessions/scripts/inspect_session.py <session_id>

# View tool call timeline only
python3 .agents/skills/bob-sessions/scripts/inspect_session.py <session_id> --tools

# Output full session history in JSON
python3 .agents/skills/bob-sessions/scripts/inspect_session.py <session_id> --json
```

### 3. Export Session for Documentation

To export the conversation for review or archiving:

```bash
# Export to a Markdown file
python3 .agents/skills/bob-sessions/scripts/export_session.py <session_id> -o session_transcript.md
```

---

## Database Architecture Reference

- **Database Location**: `~/.bob/db/bob.db` (override with `--db` or `BOB_DB_PATH`)
- **Key Tables**:
  - `tasks`: Holds session IDs, titles, first messages, statuses (`running`, `active`, `completed`, `error`), costs, timestamps, directory, and `task_type` (`normal`, `subagent`, `subtask`).
  - `messages`: Stores JSON-encoded messages, roles (`user`, `assistant`, `tool`), tool calls (`toolCalls`), and timestamps associated with `task_id`.
