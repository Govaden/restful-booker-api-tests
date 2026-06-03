import pytest
import requests

def test_get_bookings(base_url):
    response = requests.get(f"{base_url}/booking")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_booking_by_id(base_url):
    response = requests.get(f"{base_url}/booking")
    assert response.status_code == 200
    bookings = response.json()
    assert len(bookings) > 0

    booking_id = bookings[0]["bookingid"]
    
    response = requests.get(f"{base_url}/booking/{booking_id}")
    assert response.status_code == 200
    booking_details = response.json()
    assert "firstname" in booking_details
    assert "lastname" in booking_details
    assert "bookingdates" in booking_details

def test_create_booking(base_url, auth_token):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"}
    booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-10"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post(f"{base_url}/booking", json=booking_data, headers=headers)
    assert response.status_code == 200
    created_booking = response.json()
    assert created_booking["booking"]["firstname"] == "John"
    assert created_booking["booking"]["lastname"] == "Doe"
    assert created_booking["booking"]["totalprice"] == 150
    assert created_booking["booking"]["depositpaid"] == True
    assert created_booking["booking"]["bookingdates"]["checkin"] == "2024-01-01"
    assert created_booking["booking"]["bookingdates"]["checkout"] == "2024-01-10"
    assert created_booking["booking"]["additionalneeds"] == "Breakfast"

