from __future__ import annotations

import sqlite3

import pandas as pd

from settings import DB_PATH


def get_schema() -> str:
    """Return only table and column metadata for the LLM prompt."""
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute(
            """
            SELECT sql
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()
    return "\n".join(row[0] for row in rows if row[0])


def run_readonly_query(sql: str) -> pd.DataFrame:
    """Execute SQL through an operating-system-level read-only connection."""
    uri = f"{DB_PATH.resolve().as_uri()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as connection:
        connection.execute("PRAGMA query_only = ON")
        return pd.read_sql_query(sql, connection)
