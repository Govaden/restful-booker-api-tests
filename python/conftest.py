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

@pytest.fixture
def seeded_bookings():
    today = date.today()
    range_a = ((today + timedelta(days=7)).isoformat(), (today + timedelta(days=10)).isoformat())
    range_b = ((today + timedelta(days=20)).isoformat(), (today + timedelta(days=25)).isoformat())
    range_c = ((today + timedelta(days=40)).isoformat(), (today + timedelta(days=42)).isoformat())
    return [
        (1, "Alice", "Anderson", range_a[0], range_a[1], 100, 1),
        (2, "Ben", "Baker", range_a[0], range_a[1], 200, 0),
        (3, "Carla", "Cole", range_b[0], range_b[1], 150, 1),
        (4, "Dan", "Diaz", range_b[0], range_b[1], 250, 0),
        (5, "Eve", "Evans", range_b[0], range_b[1], 300, 1),
        (6, "Finn", "Foster", range_c[0], range_c[1], 120, 0),
        (7, "Grace", "Green", range_c[0], range_c[1], 180, 1),
    ]

@pytest.fixture
def seeded_db_conn(db_conn, seeded_bookings):
    db_conn.executemany(
        "INSERT INTO bookings (id, firstname, lastname, checkin, checkout, totalprice, depositpaid) VALUES (?, ?, ?, ?, ?, ?, ?)",
        seeded_bookings
    )
    db_conn.commit()
    return db_conn