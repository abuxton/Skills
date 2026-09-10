#!/usr/bin/env python3
"""
Common database utilities for reading and parsing Bob SQLite databases.
"""

import os
import json
import sqlite3
from typing import Optional, List, Dict, Any

DEFAULT_DB_PATH = os.path.expanduser("~/.bob/db/bob.db")

def get_db_path(custom_path: Optional[str] = None) -> str:
    """Return the resolved path to bob.db."""
    if custom_path:
        return os.path.abspath(os.path.expanduser(custom_path))
    env_path = os.environ.get("BOB_DB_PATH")
    if env_path:
        return os.path.abspath(os.path.expanduser(env_path))
    return DEFAULT_DB_PATH

def connect_db(custom_path: Optional[str] = None) -> sqlite3.Connection:
    """Connect to the bob.db database (read-only mode preferred)."""
    db_path = get_db_path(custom_path)
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Bob database not found at {db_path}")
    
    # Connect with URI read-only if supported to avoid locking issues
    uri = f"file:{db_path}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError:
        conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def format_timestamp(epoch_ms: Optional[int]) -> str:
    """Format an epoch millisecond timestamp into a human-readable string."""
    if not epoch_ms:
        return "N/A"
    import datetime
    dt = datetime.datetime.fromtimestamp(epoch_ms / 1000.0)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_json_safely(data: Any) -> Any:
    """Safely parse a JSON string or return original structure if not valid JSON."""
    if not isinstance(data, str):
        return data
    try:
        return json.loads(data)
    except Exception:
        return data
