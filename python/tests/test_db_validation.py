import booking_client

def test_booking_reconciles_with_db(base_url, booking, db_conn):
    booking_id = booking["id"]
    response = booking_client.get_booking_by_id(base_url, booking_id)
    assert response.status_code == 200
    api_booking = response.json()
    assert api_booking == booking["response"].json()["booking"]

    db_conn.execute(
        "INSERT INTO bookings (id, firstname, lastname, checkin, checkout, totalprice, depositpaid) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            booking_id,
            api_booking["firstname"],
            api_booking["lastname"],
            api_booking["bookingdates"]["checkin"],
            api_booking["bookingdates"]["checkout"],
            api_booking["totalprice"],
            1 if api_booking["depositpaid"] else 0
        )
    )
    db_conn.commit()

    row = db_conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
    assert row["id"] == booking_id
    assert row["firstname"] == api_booking["firstname"]
    assert row["lastname"] == api_booking["lastname"]
    assert row["checkin"] == api_booking["bookingdates"]["checkin"]
    assert row["checkout"] == api_booking["bookingdates"]["checkout"]
    assert row["totalprice"] == api_booking["totalprice"]
    assert bool(row["depositpaid"]) == api_booking["depositpaid"]
