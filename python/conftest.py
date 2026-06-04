from datetime import date, timedelta

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