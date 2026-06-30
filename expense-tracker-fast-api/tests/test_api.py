import main
import pytest
from fastapi.testclient import TestClient


client = TestClient(main.app)


@pytest.fixture(autouse=True)
def temporary_database(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "test-expense.db")
    main.init_db()


def test_expense_workflow() -> None:
    response = client.post(
        "/expenses",
        json={
            "date": "2026-06-30",
            "amount": 250.5,
            "category": "food",
            "subcategory": "groceries",
            "note": "Weekly groceries",
        },
    )
    assert response.status_code == 201
    assert response.json()["status"] == "ok"

    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "food"

    response = client.get(
        "/expenses/summary",
        params={"start_date": "2026-06-01", "end_date": "2026-06-30"},
    )
    assert response.status_code == 200
    assert response.json() == [{"category": "food", "total_amount": 250.5}]


def test_categories() -> None:
    response = client.get("/categories")
    assert response.status_code == 200
    assert "food" in response.json()


def test_rejects_reversed_date_range() -> None:
    response = client.get(
        "/expenses",
        params={"start_date": "2026-07-01", "end_date": "2026-06-01"},
    )
    assert response.status_code == 422
