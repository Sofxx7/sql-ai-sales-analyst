from __future__ import annotations

import sqlite3

from settings import DB_PATH


SCHEMA = """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    segment TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
"""

CUSTOMERS = [
    (1, "Ana Torres", "Lima", "Retail"),
    (2, "Bruno Díaz", "Arequipa", "Small Business"),
    (3, "Carla Ruiz", "Cusco", "Retail"),
    (4, "Diego León", "Lima", "Enterprise"),
    (5, "Elena Soto", "Trujillo", "Small Business"),
    (6, "Fabián Vega", "Piura", "Retail"),
]

PRODUCTS = [
    (1, "Wireless Mouse", "Accessories", 25.0),
    (2, "Mechanical Keyboard", "Accessories", 75.0),
    (3, "27-inch Monitor", "Displays", 240.0),
    (4, "USB-C Dock", "Accessories", 110.0),
    (5, "Business Laptop", "Computers", 980.0),
    (6, "Webcam", "Video", 65.0),
    (7, "Noise-Cancelling Headset", "Audio", 130.0),
    (8, "Portable SSD", "Storage", 145.0),
    (9, "Drawing Tablet", "Creative", 210.0),
]

ORDERS = [
    (101, 1, "2026-01-12", "completed"),
    (102, 2, "2026-01-25", "completed"),
    (103, 4, "2026-02-02", "completed"),
    (104, 3, "2026-02-17", "completed"),
    (105, 1, "2026-03-04", "completed"),
    (106, 5, "2026-03-19", "cancelled"),
    (107, 4, "2026-04-08", "completed"),
    (108, 6, "2026-04-22", "completed"),
    (109, 2, "2026-05-06", "completed"),
    (110, 5, "2026-05-27", "completed"),
]

ORDER_ITEMS = [
    (101, 1, 2, 25.0),
    (101, 6, 1, 65.0),
    (102, 3, 2, 230.0),
    (103, 5, 3, 950.0),
    (103, 4, 3, 105.0),
    (104, 2, 1, 75.0),
    (104, 7, 1, 130.0),
    (105, 8, 2, 140.0),
    (106, 5, 1, 980.0),
    (107, 3, 4, 225.0),
    (107, 7, 4, 125.0),
    (108, 1, 1, 25.0),
    (108, 2, 1, 75.0),
    (109, 4, 2, 110.0),
    (109, 8, 1, 145.0),
    (110, 5, 1, 970.0),
    (110, 6, 2, 60.0),
]


def main() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript(SCHEMA)
        connection.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", CUSTOMERS)
        connection.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", PRODUCTS)
        connection.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", ORDERS)
        connection.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?)", ORDER_ITEMS)
    print(f"Created demo database at {DB_PATH}")


if __name__ == "__main__":
    main()
