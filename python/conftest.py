import sqlite3
import uuid
from datetime import date, timedelta
from pathlib import Path

import requests
import pytest

import booking_client

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
def booking_payload(booking_dates):
    suffix = uuid.uuid4().hex[:8]
    return {
        "firstname": f"Guest-{suffix}",
        "lastname": f"Test-{suffix}",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
        },
        "additionalneeds": "Breakfast"
    }

@pytest.fixture
def booking(base_url, auth_token, booking_payload):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = booking_client.create_booking(base_url, booking_payload, headers)
    assert response.status_code == 200, f"Booking setup failed: {response.status_code}"
    booking_id = response.json()["bookingid"]
    yield {"id": booking_id, "payload": booking_payload, "response": response}
    try:
        booking_client.delete_booking(base_url, booking_id, headers)
    except requests.RequestException:
        pass

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    schema_path = Path(__file__).resolve().parent / "db" / "schema.sql"
    conn.executescript(schema_path.read_text())
    yield conn
    conn.close()
