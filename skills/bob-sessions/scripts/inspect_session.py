#!/usr/bin/env python3
"""
Inspect a specific Bob session, its history, tool calls, or dump messages.
"""

import argparse
import json
import sys
from db_helpers import connect_db, format_timestamp, parse_json_safely

def inspect_session(session_id, db_path=None, limit_messages=50, tools_only=False, json_output=False):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    # Match exact or prefix ID
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

    parsed_messages = []
    tool_calls_extracted = []

    for row in msg_rows:
        raw_data = parse_json_safely(row["data"])
        msg_entry = {
            "id": row["id"],
            "role": row["role"],
            "created_at": format_timestamp(row["created_at"]),
            "data": raw_data
        }
        parsed_messages.append(msg_entry)

        # Check for tool invocations
        if isinstance(raw_data, dict):
            # Assistant calling tools
            tool_calls = raw_data.get("toolCalls") or raw_data.get("tool_calls")
            if tool_calls and isinstance(tool_calls, list):
                for tc in tool_calls:
                    tool_calls_extracted.append({
                        "type": "call",
                        "role": "assistant",
                        "name": tc.get("name"),
                        "arguments": tc.get("arguments") or tc.get("input"),
                        "time": format_timestamp(row["created_at"])
                    })
            # Tool returning output
            if row["role"] == "tool":
                tool_calls_extracted.append({
                    "type": "result",
                    "role": "tool",
                    "content": (str(raw_data.get("content", ""))[:300] + "...") if len(str(raw_data.get("content", ""))) > 300 else str(raw_data.get("content", "")),
                    "isError": raw_data.get("isError", False),
                    "time": format_timestamp(row["created_at"])
                })

    session_summary = {
        "id": full_id,
        "parent_id": task["parent_id"],
        "title": task["title"],
        "status": task["status"],
        "task_type": task["task_type"],
        "directory": task["directory"],
        "created_at": format_timestamp(task["created_at"]),
        "updated_at": format_timestamp(task["updated_at"]),
        "costs": cost_obj,
        "total_messages": len(msg_rows),
        "tool_events_count": len(tool_calls_extracted)
    }

    if json_output:
        out = {
            "session": session_summary,
            "tool_calls": tool_calls_extracted if tools_only else None,
            "messages": parsed_messages if not tools_only else None
        }
        print(json.dumps(out, indent=2))
        return

    # Text Display
    print("=" * 80)
    print(f"SESSION DETAILS: {full_id}")
    print("=" * 80)
    print(f"Title:       {task['title'] or '(None)'}")
    print(f"Type:        {task['task_type']} | Status: {task['status']}")
    print(f"Directory:   {task['directory']}")
    print(f"Created:     {format_timestamp(task['created_at'])}")
    print(f"Updated:     {format_timestamp(task['updated_at'])}")
    if cost_obj and isinstance(cost_obj, dict):
        cost_val = cost_obj.get('cost')
        tokens = cost_obj.get('contextTokens')
        print(f"Cost / Usage: ${round(cost_val, 4) if cost_val else 0} USD | Context Tokens: {tokens or 'N/A'}")
    print(f"Total Msgs:  {len(msg_rows)}")
    print("-" * 80)

    if tools_only:
        print("\n--- TOOL USAGE TRAIL ---")
        if not tool_calls_extracted:
            print("No tool invocations found.")
        for tc in tool_calls_extracted:
            if tc["type"] == "call":
                print(f"[{tc['time']}] -> Tool Call: {tc['name']}")
                args_str = json.dumps(tc['arguments']) if isinstance(tc['arguments'], dict) else str(tc['arguments'])
                if len(args_str) > 120:
                    args_str = args_str[:120] + "..."
                print(f"    Arguments: {args_str}")
            else:
                err_flag = " (ERROR)" if tc.get("isError") else ""
                print(f"[{tc['time']}] <- Tool Result{err_flag}: {tc['content']}")
        return

    print("\n--- RECENT MESSAGES ---")
    display_messages = parsed_messages[-limit_messages:]
    for m in display_messages:
        role = m["role"].upper()
        data = m["data"]
        content = ""
        if isinstance(data, dict):
            content = data.get("content", "")
            if not content and "toolCalls" in data:
                calls = [c.get("name", "tool") for c in data["toolCalls"]]
                content = f"[Called tools: {', '.join(calls)}]"
        else:
            content = str(data)

        preview = content.strip()
        if len(preview) > 200:
            preview = preview[:200] + "..."
        print(f"[{m['created_at']}] [{role}]: {preview}\n")

def main():
    parser = argparse.ArgumentParser(description="Inspect details, history, and tools for a Bob session.")
    parser.add_argument("session_id", help="Full session ID or leading prefix (e.g. '0468c585').")
    parser.add_argument("--tools", action="store_true", help="Display only the tool invocations and results timeline.")
    parser.add_argument("--limit", type=int, default=20, help="Number of recent messages to show (default: 20).")
    parser.add_argument("--json", action="store_true", help="Output full data as JSON.")
    parser.add_argument("--db", help="Custom path to bob.db.")

    args = parser.parse_args()
    inspect_session(
        session_id=args.session_id,
        db_path=args.db,
        limit_messages=args.limit,
        tools_only=args.tools,
        json_output=args.json
    )

if __name__ == "__main__":
    main()
