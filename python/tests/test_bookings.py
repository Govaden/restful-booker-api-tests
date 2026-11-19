import booking_client
from schema_validation import assert_matches_schema

def test_get_bookings(base_url):
    response = booking_client.get_all_bookings(base_url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all("bookingid" in b for b in response.json())
    assert_matches_schema(response.json(), "BookingList")

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
    assert_matches_schema(booking_details, "Booking")

def test_get_bookings_filter_by_name(base_url, booking):
    payload = booking["payload"]
    response = booking_client.get_bookings_by_name(base_url, payload["firstname"], payload["lastname"])
    assert response.status_code == 200
    assert {"bookingid": booking["id"]} in response.json()

def test_create_booking(booking):
    payload = booking["payload"]
    response = booking["response"]
    assert response.status_code == 200
    created_booking = response.json()
    assert created_booking["bookingid"] == booking["id"]
    assert created_booking["booking"]["firstname"] == payload["firstname"]
    assert created_booking["booking"]["lastname"] == payload["lastname"]
    assert created_booking["booking"]["totalprice"] == payload["totalprice"]
    assert created_booking["booking"]["depositpaid"] == payload["depositpaid"]
    assert created_booking["booking"]["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
    assert created_booking["booking"]["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]
    assert created_booking["booking"]["additionalneeds"] == payload["additionalneeds"]
    assert_matches_schema(created_booking, "CreatedBooking")

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

def test_update_booking(base_url, auth_token, booking_dates, booking):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    payload = booking["payload"]
    updated_data = {
        "firstname": payload["firstname"],
        "lastname": payload["lastname"],
        "totalprice": 250,
        "depositpaid": False,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
        },
        "additionalneeds": "Dinner"
    }

    response = booking_client.update_booking(base_url, booking["id"], updated_data, headers)
    assert response.status_code == 200
    updated_booking = response.json()
    assert updated_booking["firstname"] == payload["firstname"]
    assert updated_booking["lastname"] == payload["lastname"]
    assert updated_booking["totalprice"] == 250
    assert updated_booking["depositpaid"] == False
    assert updated_booking["bookingdates"]["checkin"] == booking_dates["checkin"]
    assert updated_booking["bookingdates"]["checkout"] == booking_dates["checkout"]
    assert updated_booking["additionalneeds"] == "Dinner"
    assert_matches_schema(updated_booking, "Booking")

def test_update_booking_without_auth(base_url, booking):
    response = booking_client.update_booking(base_url, booking["id"], booking["payload"], headers=None)
    assert response.status_code == 403

def test_partial_update_booking(base_url, auth_token, booking):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = booking_client.partial_update_booking(base_url, booking["id"], {"firstname": "Patched"}, headers)
    assert response.status_code == 200
    assert response.json()["firstname"] == "Patched"
    assert_matches_schema(response.json(), "Booking")

def test_delete_booking(base_url, auth_token, booking):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = booking_client.delete_booking(base_url, booking["id"], headers)
    assert response.status_code == 201
    response = booking_client.get_booking_by_id(base_url, booking["id"])
    assert response.status_code == 404

def test_delete_booking_without_auth(base_url, booking):
    response = booking_client.delete_booking(base_url, booking["id"], headers=None)
    assert response.status_code == 403
