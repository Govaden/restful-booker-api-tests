import pytest
import requests
from datetime import date, timedelta

checkin = (date.today() + timedelta(days=7)).isoformat()
checkout = (date.today() + timedelta(days=14)).isoformat()

def test_get_bookings(base_url):
    response = requests.get(f"{base_url}/booking")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all("bookingid" in b for b in response.json())

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
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout
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
    assert created_booking["booking"]["bookingdates"]["checkin"] == checkin
    assert created_booking["booking"]["bookingdates"]["checkout"] == checkout
    assert created_booking["booking"]["additionalneeds"] == "Breakfast"

    requests.delete(f"{base_url}/booking/{created_booking['bookingid']}", headers=headers)

def test_update_booking(base_url, auth_token):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_data = {
        "firstname": "Jane",
        "lastname": "Smith",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2024-02-01",
            "checkout": "2024-02-10"
        },
        "additionalneeds": "Lunch"
    }

    response = requests.post(f"{base_url}/booking", json=booking_data, headers=headers)
    assert response.status_code == 200
    created_booking = response.json()
    booking_id = created_booking["bookingid"]
    updated_data = {
        "firstname": "Jane",
        "lastname": "Smith",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout
        },
        "additionalneeds": "Dinner"
    }

    response = requests.put(f"{base_url}/booking/{booking_id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    updated_booking = response.json()
    assert updated_booking["firstname"] == "Jane"
    assert updated_booking["lastname"] == "Smith"
    assert updated_booking["totalprice"] == 250
    assert updated_booking["depositpaid"] == True
    assert updated_booking["bookingdates"]["checkin"] == checkin
    assert updated_booking["bookingdates"]["checkout"] == checkout
    assert updated_booking["additionalneeds"] == "Dinner"

def test_delete_booking(base_url, auth_token):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_data = {
        "firstname": "Alice",
        "lastname": "Johnson",
        "totalprice": 300,
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout
        },
        "additionalneeds": "None"
    }

    response = requests.post(f"{base_url}/booking", json=booking_data, headers=headers)
    assert response.status_code == 200
    created_booking = response.json()
    booking_id = created_booking["bookingid"]
    response = requests.delete(f"{base_url}/booking/{booking_id}", headers=headers)
    assert response.status_code == 201
    response = requests.get(f"{base_url}/booking/{booking_id}")
    assert response.status_code == 404