from __future__ import annotations

import os

import requests


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "sql": {"type": "string"},
        "explanation": {"type": "string"},
    },
    "required": ["sql", "explanation"],
}


def generate_sql(question: str, database_schema: str) -> str:
    """Ask a local LLM for one SQLite query as structured JSON."""
    system_prompt = f"""
You are a SQLite analytics assistant.
Convert the user's business question into exactly one read-only SELECT query.
Use only tables and columns from the schema below.
Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, ATTACH, or PRAGMA.
Do not invent columns. Prefer explicit JOIN conditions.
Dates are stored as ISO-8601 text (YYYY-MM-DD).
Business rule: revenue includes completed orders only. For every revenue or
sales-total question, join the orders table and filter status = 'completed'
unless the user explicitly requests another status or all statuses.

DATABASE SCHEMA:
{database_schema}
""".strip()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "stream": False,
            "format": RESPONSE_SCHEMA,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            "options": {"temperature": 0},
        },
        timeout=90,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]
