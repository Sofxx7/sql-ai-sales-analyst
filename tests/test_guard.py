import pytest

from guard import UnsafeQueryError, validate_and_limit


def test_adds_limit_to_select() -> None:
    safe_sql = validate_and_limit("SELECT name FROM products")
    assert safe_sql == "SELECT name FROM products LIMIT 100"


def test_keeps_existing_limit() -> None:
    safe_sql = validate_and_limit("SELECT name FROM products LIMIT 3")
    assert safe_sql == "SELECT name FROM products LIMIT 3"


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE products",
        "DELETE FROM orders",
        "UPDATE products SET unit_price = 0",
        "SELECT * FROM products; DROP TABLE products",
        "PRAGMA table_info(products)",
    ],
)
def test_rejects_unsafe_sql(sql: str) -> None:
    with pytest.raises(UnsafeQueryError):
        validate_and_limit(sql)
