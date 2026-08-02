import pytest

SEED_BOOKINGS = [
    (1, "John",  "Doe",     "2026-01-05", "2026-01-10", 150, 1),
    (2, "Jane",  "Smith",   "2026-01-20", "2026-01-25", 250, 1),
    (3, "Alice", "Johnson", "2026-01-28", "2026-02-02", 300, 1),
    (4, "Bob",   "Brown",   "2026-02-10", "2026-02-15", 120, 0),
    (5, "Carol", "White",   "2026-03-03", "2026-03-09", 100, 0),
    (6, "Dave",  "Green",   "2026-03-15", "2026-03-20", 200, 0),
    (7, "Erin",  "Black",   "2026-03-25", "2026-03-30", 180, 1),
]

@pytest.fixture
def seeded_db(db_conn):
    db_conn.executemany(
        "INSERT INTO bookings (id, firstname, lastname, checkin, checkout, totalprice, depositpaid) VALUES (?, ?, ?, ?, ?, ?, ?)",
        SEED_BOOKINGS
    )
    db_conn.commit()
    return db_conn

def count_bookings_in_range(conn, start, end):
    row = conn.execute(
        "SELECT COUNT(*) AS cnt FROM bookings WHERE checkin BETWEEN ? AND ?",
        (start, end)
    ).fetchone()
    return row["cnt"]

def test_count_bookings_per_date_range(seeded_db):
    assert count_bookings_in_range(seeded_db, "2026-01-01", "2026-01-31") == 3
    assert count_bookings_in_range(seeded_db, "2026-02-01", "2026-02-28") == 1
    assert count_bookings_in_range(seeded_db, "2026-03-01", "2026-03-31") == 3
    assert count_bookings_in_range(seeded_db, "2026-01-01", "2026-03-31") == 7

def test_avg_totalprice(seeded_db):
    row = seeded_db.execute("SELECT COUNT(*) AS cnt, AVG(totalprice) AS avg_price FROM bookings").fetchone()
    assert row["cnt"] == 7
    assert row["avg_price"] == pytest.approx(1300 / 7)

def test_group_by_depositpaid(seeded_db):
    rows = seeded_db.execute(
        "SELECT depositpaid, COUNT(*) AS cnt, AVG(totalprice) AS avg_price FROM bookings GROUP BY depositpaid ORDER BY depositpaid"
    ).fetchall()
    results = {row["depositpaid"]: (row["cnt"], row["avg_price"]) for row in rows}

    assert results[0] == (3, pytest.approx(140))
    assert results[1] == (4, pytest.approx(220))
