from __future__ import annotations

from sqlglot import exp, parse
from sqlglot.errors import ParseError


class UnsafeQueryError(ValueError):
    """Raised when generated SQL is not safe to execute."""


FORBIDDEN_NODES = (
    exp.Alter,
    exp.Command,
    exp.Create,
    exp.Delete,
    exp.Drop,
    exp.Insert,
    exp.Merge,
    exp.Update,
)


def validate_and_limit(sql: str, max_rows: int = 100) -> str:
    """Accept one read-only SQLite query and enforce a result limit."""
    cleaned = sql.strip().removesuffix(";")
    if not cleaned:
        raise UnsafeQueryError("The model returned an empty query.")

    try:
        statements = parse(cleaned, read="sqlite")
    except ParseError as exc:
        raise UnsafeQueryError(f"Invalid SQL: {exc}") from exc

    if len(statements) != 1:
        raise UnsafeQueryError("Only one SQL statement is allowed.")

    tree = statements[0]
    if tree is None or not isinstance(tree, exp.Query):
        raise UnsafeQueryError("Only SELECT queries are allowed.")

    if any(tree.find(node_type) for node_type in FORBIDDEN_NODES):
        raise UnsafeQueryError("The query contains a write or DDL operation.")

    if tree.args.get("limit") is None:
        tree = tree.limit(max_rows)

    return tree.sql(dialect="sqlite")
