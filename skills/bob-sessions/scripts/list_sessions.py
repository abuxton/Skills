#!/usr/bin/env python3
"""
List Bob sessions with rich filtering and formatting options.
"""

import argparse
import json
import sys
from datetime import datetime, date, timedelta
from db_helpers import connect_db, format_timestamp, parse_json_safely

def list_sessions(
    db_path=None,
    filter_date=None,
    days=None,
    limit=20,
    status=None,
    task_type=None,
    query=None,
    json_output=False
):
    conn = connect_db(db_path)
    cursor = conn.cursor()

    conditions = []
    params = []

    if filter_date:
        if filter_date.lower() == "today":
            target_date = date.today().isoformat()
        elif filter_date.lower() == "yesterday":
            target_date = (date.today() - timedelta(days=1)).isoformat()
        else:
            target_date = filter_date
        conditions.append("date(created_at/1000, 'unixepoch', 'localtime') = ?")
        params.append(target_date)
    elif days is not None:
        cutoff_date = (date.today() - timedelta(days=days)).isoformat()
        conditions.append("date(created_at/1000, 'unixepoch', 'localtime') >= ?")
        params.append(cutoff_date)

    if status:
        conditions.append("status = ?")
        params.append(status)

    if task_type:
        conditions.append("task_type = ?")
        params.append(task_type)

    if query:
        conditions.append("(title LIKE ? OR first_message LIKE ? OR id LIKE ?)")
        wildcard = f"%{query}%"
        params.extend([wildcard, wildcard, wildcard])

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"""
        SELECT 
            id,
            parent_id,
            title,
            status,
            task_type,
            first_message,
            directory,
            costs,
            created_at,
            updated_at,
            (SELECT COUNT(*) FROM messages WHERE messages.task_id = tasks.id) AS message_count
        FROM tasks
        {where_clause}
        ORDER BY updated_at DESC
        LIMIT ?
    """
    params.append(limit)

    cursor.execute(sql, params)
    rows = cursor.fetchall()

    sessions = []
    for row in rows:
        cost_obj = parse_json_safely(row["costs"])
        cost_val = cost_obj.get("cost") if isinstance(cost_obj, dict) else None
        
        title_display = row["title"]
        if not title_display and row["first_message"]:
            title_display = row["first_message"].strip().split("\n")[0][:80]
        elif not title_display:
            title_display = "(Empty session)"

        sessions.append({
            "id": row["id"],
            "short_id": row["id"][:8],
            "parent_id": row["parent_id"],
            "title": title_display,
            "status": row["status"],
            "task_type": row["task_type"],
            "message_count": row["message_count"],
            "directory": row["directory"],
            "cost_usd": round(cost_val, 4) if isinstance(cost_val, (int, float)) else None,
            "created_at": format_timestamp(row["created_at"]),
            "updated_at": format_timestamp(row["updated_at"]),
        })

    conn.close()

    if json_output:
        print(json.dumps(sessions, indent=2))
        return

    if not sessions:
        print("No matching Bob sessions found.")
        return

    # Table formatting
    print(f"{'ID':<10} {'Type':<9} {'Status':<10} {'Msgs':<6} {'Created (Local)':<20} {'Last Updated':<20} {'Title / Summary'}")
    print("-" * 110)
    for s in sessions:
        title_trunc = (s['title'][:45] + '...') if len(s['title']) > 48 else s['title']
        print(f"{s['short_id']:<10} {s['task_type']:<9} {s['status']:<10} {s['message_count']:<6} {s['created_at']:<20} {s['updated_at']:<20} {title_trunc}")

def main():
    parser = argparse.ArgumentParser(description="List and search Bob sessions from bob.db.")
    parser.add_argument("--date", help="Filter by date ('today', 'yesterday', or 'YYYY-MM-DD').")
    parser.add_argument("--days", type=int, help="Filter by last N days.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number of sessions to return (default: 20).")
    parser.add_argument("--status", help="Filter by status (e.g. 'active', 'completed', 'error', 'running').")
    parser.add_argument("--type", dest="task_type", help="Filter by task type ('normal', 'subagent', 'subtask').")
    parser.add_argument("--query", "-q", help="Search substring in session id, title, or first message.")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")
    parser.add_argument("--db", help="Custom path to bob.db.")

    args = parser.parse_args()

    try:
        list_sessions(
            db_path=args.db,
            filter_date=args.date,
            days=args.days,
            limit=args.limit,
            status=args.status,
            task_type=args.task_type,
            query=args.query,
            json_output=args.json
        )
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
