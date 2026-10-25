import booking_client

SEED_BOOKINGS = [
    (1, "John",  "Doe",     "2026-01-05", "2026-01-10", 150, 1),
    (2, "Jane",  "Smith",   "2026-01-20", "2026-01-25", 250, 1),
    (3, "Alice", "Johnson", "2026-01-28", "2026-02-02", 300, 1),
    (4, "Bob",   "Brown",   "2026-02-10", "2026-02-15", 120, 0),
]

SEED_NEEDS = [
    (1, "Breakfast"),
    (1, "Late checkout"),
    (2, "Breakfast"),
    (3, "Breakfast"),
    (3, "Parking"),
    (3, "Late checkout"),
]

def seed(conn):
    conn.executemany(
        "INSERT INTO bookings (id, firstname, lastname, checkin, checkout, totalprice, depositpaid) VALUES (?, ?, ?, ?, ?, ?, ?)",
        SEED_BOOKINGS
    )
    conn.executemany("INSERT INTO booking_needs (booking_id, need) VALUES (?, ?)", SEED_NEEDS)
    conn.commit()

def test_booking_needs_reconcile_with_db(base_url, auth_token, booking_dates, db_conn):
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    booking_data = {
        "firstname": "Join",
        "lastname": "Check",
        "totalprice": 220,
        "depositpaid": True,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
        },
        "additionalneeds": "Breakfast, Late checkout"
    }

    response = booking_client.create_booking(base_url, booking_data, headers)
    assert response.status_code == 200
    booking_id = response.json()["bookingid"]
    api_booking = response.json()["booking"]
    api_needs = [need.strip() for need in api_booking["additionalneeds"].split(",")]

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
    db_conn.executemany(
        "INSERT INTO booking_needs (booking_id, need) VALUES (?, ?)",
        [(booking_id, need) for need in api_needs]
    )
    db_conn.commit()

    rows = db_conn.execute(
        "SELECT n.need FROM bookings b JOIN booking_needs n ON n.booking_id = b.id WHERE b.id = ?",
        (booking_id,)
    ).fetchall()
    assert sorted(row["need"] for row in rows) == sorted(api_needs)
    assert sorted(api_needs) == ["Breakfast", "Late checkout"]

    booking_client.delete_booking(base_url, booking_id, headers)

def test_bookings_without_needs(db_conn):
    seed(db_conn)
    rows = db_conn.execute(
        "SELECT b.id FROM bookings b LEFT JOIN booking_needs n ON n.booking_id = b.id WHERE n.id IS NULL"
    ).fetchall()
    assert [row["id"] for row in rows] == [4]

def test_count_needs_per_booking(db_conn):
    seed(db_conn)
    rows = db_conn.execute(
        "SELECT b.id, COUNT(n.id) AS cnt FROM bookings b LEFT JOIN booking_needs n ON n.booking_id = b.id GROUP BY b.id ORDER BY b.id"
    ).fetchall()
    assert {row["id"]: row["cnt"] for row in rows} == {1: 2, 2: 1, 3: 3, 4: 0}

def test_sum_totalprice_per_need(db_conn):
    seed(db_conn)
    rows = db_conn.execute(
        "SELECT n.need, SUM(b.totalprice) AS total FROM bookings b JOIN booking_needs n ON n.booking_id = b.id GROUP BY n.need ORDER BY n.need"
    ).fetchall()
    assert {row["need"]: row["total"] for row in rows} == {"Breakfast": 700, "Late checkout": 450, "Parking": 300}
