CREATE TABLE IF NOT EXISTS bookings (
    id          INTEGER PRIMARY KEY,
    firstname   TEXT    NOT NULL,
    lastname    TEXT    NOT NULL,
    checkin     TEXT    NOT NULL,
    checkout    TEXT    NOT NULL,
    totalprice  INTEGER NOT NULL CHECK (totalprice >= 0),
    depositpaid INTEGER NOT NULL CHECK (depositpaid IN (0, 1)),
    CHECK (date(checkin)  IS NOT NULL),
    CHECK (date(checkout) IS NOT NULL),
    CHECK (checkout >= checkin)
);
