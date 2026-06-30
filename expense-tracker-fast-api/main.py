import json
import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "expense.db"
CATEGORIES_PATH = BASE_DIR / "categories.json"


class ExpenseCreate(BaseModel):
    date: date
    amount: Annotated[float, Field(gt=0)]
    category: Annotated[str, Field(min_length=1)]
    subcategory: str = ""
    note: str = ""


class Expense(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    amount: float
    category: str
    subcategory: str
    note: str


class ExpenseCreated(BaseModel):
    status: str = "ok"
    id: int


class CategorySummary(BaseModel):
    category: str
    total_amount: float


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
            """
        )


@contextmanager
def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


init_db()

app = FastAPI(
    title="Expense Tracker API",
    description="A REST version of the Expense Tracker MCP server.",
    version="0.1.0",
)


@app.get("/", tags=["health"])
def root() -> dict[str, str]:
    return {"message": "Expense Tracker API is running"}


@app.post(
    "/expenses",
    response_model=ExpenseCreated,
    status_code=status.HTTP_201_CREATED,
    tags=["expenses"],
)
def add_expense(expense: ExpenseCreate) -> ExpenseCreated:
    with get_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO expenses(date, amount, category, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                expense.date.isoformat(),
                expense.amount,
                expense.category,
                expense.subcategory,
                expense.note,
            ),
        )
        return ExpenseCreated(id=cursor.lastrowid)


@app.get("/expenses", response_model=list[Expense], tags=["expenses"])
def list_expenses(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
) -> list[Expense]:
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="start_date must be before or equal to end_date",
        )

    query = """
        SELECT id, date, amount, category, subcategory, note
        FROM expenses
        WHERE (? IS NULL OR date >= ?)
          AND (? IS NULL OR date <= ?)
        ORDER BY id ASC
    """
    start = start_date.isoformat() if start_date else None
    end = end_date.isoformat() if end_date else None

    with get_db() as connection:
        rows = connection.execute(query, (start, start, end, end)).fetchall()
        return [Expense.model_validate(dict(row)) for row in rows]


@app.get(
    "/expenses/summary",
    response_model=list[CategorySummary],
    tags=["expenses"],
)
def summarize_expenses(
    start_date: date,
    end_date: date,
    category: str | None = None,
) -> list[CategorySummary]:
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="start_date must be before or equal to end_date",
        )

    query = """
        SELECT category, SUM(amount) AS total_amount
        FROM expenses
        WHERE date BETWEEN ? AND ?
    """
    params: list[str] = [start_date.isoformat(), end_date.isoformat()]

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " GROUP BY category ORDER BY category ASC"

    with get_db() as connection:
        rows = connection.execute(query, params).fetchall()
        return [CategorySummary.model_validate(dict(row)) for row in rows]


@app.get("/categories", response_model=dict[str, list[str]], tags=["categories"])
def categories() -> dict[str, list[str]]:
    try:
        with CATEGORIES_PATH.open(encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not load categories",
        ) from error
