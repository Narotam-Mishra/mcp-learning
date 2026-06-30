# Expense Tracker FastAPI

A REST API version of the expense tracker MCP server, built with FastAPI,
Pydantic, and SQLite.

## Run locally

```bash
uv sync --dev
uv run uvicorn main:app --reload
```

Open the interactive API documentation at <http://127.0.0.1:8000/docs>.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/expenses` | Add an expense |
| `GET` | `/expenses` | List expenses with optional date filters |
| `GET` | `/expenses/summary` | Summarize expenses by category |
| `GET` | `/categories` | Return categories and subcategories |

### Add an expense

```bash
curl -X POST http://127.0.0.1:8000/expenses \
  -H 'Content-Type: application/json' \
  -d '{
    "date": "2026-06-30",
    "amount": 250.50,
    "category": "food",
    "subcategory": "groceries",
    "note": "Weekly groceries"
  }'
```

### List expenses

```bash
curl 'http://127.0.0.1:8000/expenses?start_date=2026-06-01&end_date=2026-06-30'
```

Both date filters are optional. Calling `/expenses` without them returns all
expenses.

### Summarize expenses

```bash
curl 'http://127.0.0.1:8000/expenses/summary?start_date=2026-06-01&end_date=2026-06-30'
```

Add `&category=food` to summarize only one category.

## Run tests

```bash
uv run pytest
```
