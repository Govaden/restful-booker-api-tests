import sqlite3
from datetime import date, timedelta
from pathlib import Path

import requests
import pytest

@pytest.fixture(scope="session")
def base_url():
    return "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def auth_token(base_url):
    response = requests.post(f"{base_url}/auth", json={"username": "admin", "password": "password123"})
    assert response.status_code == 200, f"Authentication failed: {response.status_code}"
    token = response.json().get("token")
    assert token, "Token not found in response"
    return token

@pytest.fixture
def booking_dates():
    return {
        "checkin": (date.today() + timedelta(days=7)).isoformat(),
        "checkout": (date.today() + timedelta(days=14)).isoformat()
    }

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    schema_path = Path(__file__).resolve().parent / "db" / "schema.sql"
    conn.executescript(schema_path.read_text())
    yield conn
    conn.close()