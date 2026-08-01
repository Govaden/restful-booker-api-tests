from collections import defaultdict

import pytest

def test_count_bookings_per_date_range(seeded_db_conn, seeded_bookings):
    rows = seeded_db_conn.execute(
        "SELECT checkin, checkout, COUNT(*) AS cnt FROM bookings GROUP BY checkin, checkout ORDER BY checkin"
    ).fetchall()

    expected_counts = defaultdict(int)
    for _, _, _, checkin, checkout, _, _ in seeded_bookings:
        expected_counts[(checkin, checkout)] += 1

    assert len(rows) == len(expected_counts)
    for row in rows:
        assert row["cnt"] == expected_counts[(row["checkin"], row["checkout"])]

def test_avg_totalprice(seeded_db_conn, seeded_bookings):
    row = seeded_db_conn.execute("SELECT AVG(totalprice) AS avg_price FROM bookings").fetchone()
    expected_avg = sum(b[5] for b in seeded_bookings) / len(seeded_bookings)
    assert row["avg_price"] == pytest.approx(expected_avg)

def test_group_by_depositpaid(seeded_db_conn, seeded_bookings):
    rows = seeded_db_conn.execute(
        "SELECT depositpaid, COUNT(*) AS cnt, AVG(totalprice) AS avg_price FROM bookings GROUP BY depositpaid ORDER BY depositpaid"
    ).fetchall()

    expected_prices = defaultdict(list)
    for booking in seeded_bookings:
        expected_prices[booking[6]].append(booking[5])

    assert len(rows) == len(expected_prices)
    for row in rows:
        prices = expected_prices[row["depositpaid"]]
        assert row["cnt"] == len(prices)
        assert row["avg_price"] == pytest.approx(sum(prices) / len(prices))
