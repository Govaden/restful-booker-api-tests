import argparse
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = DB_DIR / "schema.sql"
DEFAULT_DB_PATH = DB_DIR / "bookings.db"


def sample_bookings():
    checkin = (date.today() + timedelta(days=7)).isoformat()
    checkout = (date.today() + timedelta(days=14)).isoformat()
    return [
        (1, "John", "Doe", checkin, checkout, 150, 1),
        (2, "Jane", "Smith", checkin, checkout, 250, 1),
        (3, "Alice", "Johnson", checkin, checkout, 300, 1),
        (4, "Bob", "Brown", checkin, checkout, 120, 0),
        (5, "Unique", "Filterable", checkin, checkout, 100, 0),
    ]


def seed(db_path=DEFAULT_DB_PATH):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    rows = sample_bookings()

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("DROP TABLE IF EXISTS bookings")
        conn.executescript(schema)
        conn.executemany(
            "INSERT INTO bookings "
            "(id, firstname, lastname, checkin, checkout, totalprice, depositpaid) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            rows,
        )

    print(f"Seeded {len(rows)} bookings into {db_path}")
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description="Seed the SQLite bookings database.")
    parser.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help="Path to the SQLite database file (default: db/bookings.db).",
    )
    args = parser.parse_args()
    seed(args.db)


if __name__ == "__main__":
    main()
