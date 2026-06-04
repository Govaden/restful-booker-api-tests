import pytest
import requests

def test_get_bookings(base_url):
    response = requests.get(f"{base_url}/booking")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all("bookingid" in b for b in response.json())

    negative_response = requests.get(f"{base_url}/booking/999999")
    assert negative_response.status_code == 404

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

def test_create_booking(base_url, auth_token, booking_dates):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
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
    assert created_booking["booking"]["bookingdates"]["checkin"] == booking_dates["checkin"]
    assert created_booking["booking"]["bookingdates"]["checkout"] == booking_dates["checkout"]
    assert created_booking["booking"]["additionalneeds"] == "Breakfast"

    requests.delete(f"{base_url}/booking/{created_booking['bookingid']}", headers=headers)

def test_create_booking_invalid_data(base_url, auth_token):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}

    invalid_booking_data = {
        "firstname": "Invalid",
        "lastname": "Booking",
        "totalprice": "NotANumber",
        "depositpaid": "NotABoolean",
    }

    response = requests.post(f"{base_url}/booking", json=invalid_booking_data, headers=headers)
    assert response.status_code >= 400

def test_update_booking(base_url, auth_token, booking_dates):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_data = {
        "firstname": "Jane",
        "lastname": "Smith",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
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
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
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
    assert updated_booking["bookingdates"]["checkin"] == booking_dates["checkin"]
    assert updated_booking["bookingdates"]["checkout"] == booking_dates["checkout"]
    assert updated_booking["additionalneeds"] == "Dinner"

    response = requests.put(f"{base_url}/booking/{booking_id}", json=updated_data)
    assert response.status_code == 403

    requests.delete(f"{base_url}/booking/{booking_id}", headers=headers)

def test_delete_booking(base_url, auth_token, booking_dates):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_data = {
        "firstname": "Alice",
        "lastname": "Johnson",
        "totalprice": 300,
        "depositpaid": True,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
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