import pytest

from schema_validation import assert_matches_schema

VALID_BOOKING = {
    "firstname": "Schema",
    "lastname": "Check",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-01-05", "checkout": "2026-01-10"},
    "additionalneeds": "Breakfast",
}


def test_valid_booking_passes():
    assert_matches_schema(VALID_BOOKING, "Booking")


def test_booking_without_optional_field_passes():
    booking = {key: value for key, value in VALID_BOOKING.items() if key != "additionalneeds"}
    assert_matches_schema(booking, "Booking")


def test_booking_with_wrong_type_fails():
    booking = {**VALID_BOOKING, "totalprice": "150"}
    with pytest.raises(AssertionError, match=r"\$\.totalprice: '150' is not of type"):
        assert_matches_schema(booking, "Booking")


def test_booking_missing_required_field_fails():
    booking = {key: value for key, value in VALID_BOOKING.items() if key != "lastname"}
    with pytest.raises(AssertionError, match="'lastname' is a required property"):
        assert_matches_schema(booking, "Booking")


def test_nested_reference_is_validated():
    created = {"bookingid": 1, "booking": {**VALID_BOOKING, "bookingdates": {"checkin": "2026-01-05"}}}
    with pytest.raises(AssertionError, match=r"\$\.booking\.bookingdates: 'checkout' is a required property"):
        assert_matches_schema(created, "CreatedBooking")


def test_valid_created_booking_passes():
    assert_matches_schema({"bookingid": 1, "booking": VALID_BOOKING}, "CreatedBooking")


def test_booking_list_with_wrong_item_fails():
    with pytest.raises(AssertionError, match=r"\$\[1\]\.bookingid: 'two' is not of type 'integer'"):
        assert_matches_schema([{"bookingid": 1}, {"bookingid": "two"}], "BookingList")


def test_unknown_schema_name_fails():
    with pytest.raises(ValueError, match="Unknown schema 'NoSuchSchema'"):
        assert_matches_schema({}, "NoSuchSchema")
