# Local AI Sales Analyst

A small Text-to-SQL application that answers retail analytics questions using:

- Ollama for local language-model inference
- SQLite for the demonstration database
- SQLGlot for syntax-tree validation
- Streamlit for the user interface

The model never connects directly to the database. It proposes SQL, the
application validates the syntax tree, and SQLite executes the accepted query
through a read-only connection.

## Quick start

Requirements: Python 3.10+ and [Ollama](https://ollama.com/).

```bash
ollama pull qwen2.5-coder:3b
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS or Linux
source .venv/bin/activate
```

Install, create the database, and run:

```bash
pip install -r requirements.txt
python seed.py
streamlit run app.py
```

Open `http://localhost:8501`.

## Example questions

- Which three product categories generated the most revenue?
- Who are the five customers with the highest lifetime spend?
- Show monthly revenue and number of completed orders.
- Which products have never been ordered?

Expected SQL for the first question:

```sql
SELECT
  p.category,
  ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM order_items AS oi
JOIN orders AS o ON o.order_id = oi.order_id
JOIN products AS p ON p.product_id = oi.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC
LIMIT 3;
```

## Safety design

1. The prompt exposes schema metadata, not table rows.
2. Ollama must return structured JSON.
3. SQLGlot parses the answer into an abstract syntax tree.
4. The guard accepts one query and rejects write/DDL operations.
5. A row limit is added when the model omits one.
6. SQLite is opened with `mode=ro` and `PRAGMA query_only = ON`.

This is an educational project. A production system should also implement
authentication, per-user authorization, audit logs, timeouts, cost limits,
approved views, and tests against adversarial prompts.

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Project structure

```text
.
├── app.py
├── database.py
├── guard.py
├── llm.py
├── seed.py
├── settings.py
├── tests/
│   └── test_guard.py
├── requirements.txt
└── README.md
```

## License

MIT
