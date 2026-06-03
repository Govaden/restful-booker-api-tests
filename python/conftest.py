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