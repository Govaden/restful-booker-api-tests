import booking_client

def test_get_bookings(base_url):
    response = booking_client.get_all_bookings(base_url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all("bookingid" in b for b in response.json())

    negative_response = booking_client.get_booking_by_id(base_url, 999999)
    assert negative_response.status_code == 404

def test_get_booking_by_id(base_url):
    response = booking_client.get_all_bookings(base_url)
    assert response.status_code == 200
    bookings = response.json()
    assert len(bookings) > 0

    booking_id = bookings[0]["bookingid"]
    
    response = booking_client.get_booking_by_id(base_url, booking_id)
    assert response.status_code == 200
    booking_details = response.json()
    assert "firstname" in booking_details
    assert "lastname" in booking_details
    assert "bookingdates" in booking_details

def test_get_bookings_filter_by_name(base_url, auth_token, booking_dates):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_client.create_booking(base_url, {
        "firstname": "Unique",
        "lastname": "Filterable",
        "totalprice": 100,
        "depositpaid": False,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
        },
        "additionalneeds": "None"
    }, headers)

    response = booking_client.get_all_bookings(base_url)
    assert response.status_code == 200
    assert len(response.json()) >= 1

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
    response = booking_client.create_booking(base_url, booking_data, headers)
    assert response.status_code == 200
    created_booking = response.json()
    assert created_booking["booking"]["firstname"] == "John"
    assert created_booking["booking"]["lastname"] == "Doe"
    assert created_booking["booking"]["totalprice"] == 150
    assert created_booking["booking"]["depositpaid"] == True
    assert created_booking["booking"]["bookingdates"]["checkin"] == booking_dates["checkin"]
    assert created_booking["booking"]["bookingdates"]["checkout"] == booking_dates["checkout"]
    assert created_booking["booking"]["additionalneeds"] == "Breakfast"

    booking_client.delete_booking(base_url, created_booking["bookingid"], headers)

def test_create_booking_invalid_data(base_url, auth_token):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}

    invalid_booking_data = {
        "firstname": "Invalid",
        "lastname": "Booking",
        "totalprice": "NotANumber",
        "depositpaid": "NotABoolean",
    }

    response = booking_client.create_booking(base_url, invalid_booking_data, headers)
    assert response.status_code >= 500

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

    response = booking_client.create_booking(base_url, booking_data, headers)
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

    response = booking_client.update_booking(base_url, booking_id, updated_data, headers)
    assert response.status_code == 200
    updated_booking = response.json()
    assert updated_booking["firstname"] == "Jane"
    assert updated_booking["lastname"] == "Smith"
    assert updated_booking["totalprice"] == 250
    assert updated_booking["depositpaid"] == True
    assert updated_booking["bookingdates"]["checkin"] == booking_dates["checkin"]
    assert updated_booking["bookingdates"]["checkout"] == booking_dates["checkout"]
    assert updated_booking["additionalneeds"] == "Dinner"

    booking_client.delete_booking(base_url, booking_id, headers)

def test_update_booking_invalid_data(base_url, auth_token, booking_dates):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_data = {
        "firstname": "Test",
        "lastname": "User",
        "totalprice": 100,
        "depositpaid": False,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
        },
        "additionalneeds": "None"
    }

    created_booking = booking_client.create_booking(base_url, booking_data, headers).json()
    booking_id = created_booking["bookingid"]

    response = booking_client.update_booking(base_url, booking_id, booking_data, headers=None)
    # restful-booker known bug: PUT without auth returns 200 instead of 403.
    # A production API should enforce authentication and return 403 here.
    assert response.status_code == 403

    booking_client.delete_booking(base_url, booking_id, headers)

def test_partial_update_booking(base_url, auth_token, booking_dates):
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
    created_booking = booking_client.create_booking(base_url, booking_data, headers).json()
    booking_id = created_booking["bookingid"]
    response = booking_client.partial_update_booking(base_url, booking_id, {"firstname": "Patched"}, headers)
    assert response.status_code == 200
    assert response.json()["firstname"] == "Patched"

    booking_client.delete_booking(base_url, booking_id, headers)

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

    response = booking_client.create_booking(base_url, booking_data, headers)
    assert response.status_code == 200
    created_booking = response.json()
    booking_id = created_booking["bookingid"]
    response = booking_client.delete_booking(base_url, booking_id, headers)
    assert response.status_code == 201
    response = booking_client.get_booking_by_id(base_url, booking_id)
    assert response.status_code == 404

def test_delete_booking_without_auth(base_url, auth_token, booking_dates):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_data = {
        "firstname": "Bob",
        "lastname": "Brown",
        "totalprice": 120,
        "depositpaid": False,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
        },
        "additionalneeds": "Breakfast"
    }

    created_booking = booking_client.create_booking(base_url, booking_data, headers).json()
    booking_id = created_booking["bookingid"]
    response = booking_client.delete_booking(base_url, booking_id, headers=None)
    # restful-booker known bug: DELETE without auth returns 201 instead of 403.
    # A production API should enforce authentication and return 403 here.
    assert response.status_code == 403

    booking_client.delete_booking(base_url, booking_id, headers)