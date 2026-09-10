#!/usr/bin/env python3
"""
Dump a full Bob session into clean Markdown format for review or archiving.
"""

import argparse
import json
import sys
import os
from db_helpers import connect_db, format_timestamp, parse_json_safely

def export_session_markdown(session_id, db_path=None, output_file=None):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tasks 
        WHERE id = ? OR id LIKE ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (session_id, f"{session_id}%"))
    
    task = cursor.fetchone()
    if not task:
        sys.stderr.write(f"Session with ID matching '{session_id}' not found.\n")
        sys.exit(1)

    full_id = task["id"]
    cost_obj = parse_json_safely(task["costs"])

    cursor.execute("""
        SELECT id, role, data, created_at 
        FROM messages 
        WHERE task_id = ?
        ORDER BY created_at ASC
    """, (full_id,))
    msg_rows = cursor.fetchall()
    conn.close()

    lines = []
    lines.append(f"# Bob Session Report: `{full_id}`\n")
    lines.append(f"- **Title**: {task['title'] or '(None)'}")
    lines.append(f"- **Task Type**: {task['task_type']}")
    lines.append(f"- **Status**: {task['status']}")
    lines.append(f"- **Directory**: `{task['directory']}`")
    lines.append(f"- **Created At**: {format_timestamp(task['created_at'])}")
    lines.append(f"- **Updated At**: {format_timestamp(task['updated_at'])}")
    
    if cost_obj and isinstance(cost_obj, dict):
        cost_val = cost_obj.get('cost')
        ctx = cost_obj.get('contextTokens')
        lines.append(f"- **Cost**: ${round(cost_val, 4) if cost_val else 0} USD (Tokens: {ctx or 'N/A'})")
    
    lines.append(f"- **Total Messages**: {len(msg_rows)}\n")
    lines.append("---\n")
    lines.append("## Conversation History\n")

    for i, row in enumerate(msg_rows, 1):
        role = row["role"]
        timestamp = format_timestamp(row["created_at"])
        data = parse_json_safely(row["data"])

        lines.append(f"### {i}. {role.upper()} — `{timestamp}`\n")

        if isinstance(data, dict):
            content = data.get("content", "")
            if content:
                lines.append(f"{content}\n")
            
            tool_calls = data.get("toolCalls") or data.get("tool_calls")
            if tool_calls and isinstance(tool_calls, list):
                lines.append("**Tool Calls:**\n")
                for tc in tool_calls:
                    lines.append(f"- `{tc.get('name')}`")
                    args = tc.get("arguments") or tc.get("input")
                    if args:
                        lines.append("```json")
                        lines.append(json.dumps(args, indent=2))
                        lines.append("```")
                lines.append("")
        elif role == "tool":
            lines.append("```text")
            lines.append(str(data))
            lines.append("```\n")
        else:
            lines.append(f"{data}\n")

    markdown_text = "\n".join(lines)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_text)
        print(f"Session successfully exported to {output_file}")
    else:
        print(markdown_text)

def main():
    parser = argparse.ArgumentParser(description="Export a Bob session to Markdown.")
    parser.add_argument("session_id", help="Full session ID or leading prefix.")
    parser.add_argument("-o", "--output", help="Output file path (prints to stdout if omitted).")
    parser.add_argument("--db", help="Custom path to bob.db.")

    args = parser.parse_args()
    export_session_markdown(args.session_id, db_path=args.db, output_file=args.output)

if __name__ == "__main__":
    main()
