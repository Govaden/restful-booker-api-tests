import requests

DEFAULT_TIMEOUT = (5, 30)

session = requests.Session()

def get_all_bookings(base_url):
    return session.get(f"{base_url}/booking", timeout=DEFAULT_TIMEOUT)

def get_bookings_by_name(base_url, firstname, lastname):
    return session.get(f"{base_url}/booking", params={"firstname": firstname, "lastname": lastname}, timeout=DEFAULT_TIMEOUT)

def get_booking_by_id(base_url, booking_id):
    return session.get(f"{base_url}/booking/{booking_id}", timeout=DEFAULT_TIMEOUT)

def create_booking(base_url, payload, headers):
    return session.post(f"{base_url}/booking", json=payload, headers=headers, timeout=DEFAULT_TIMEOUT)

def update_booking(base_url, booking_id, payload, headers):
    return session.put(f"{base_url}/booking/{booking_id}", json=payload, headers=headers, timeout=DEFAULT_TIMEOUT)

def delete_booking(base_url, booking_id, headers):
    return session.delete(f"{base_url}/booking/{booking_id}", headers=headers, timeout=DEFAULT_TIMEOUT)

def partial_update_booking(base_url, booking_id, payload, headers):
    return session.patch(f"{base_url}/booking/{booking_id}", json=payload, headers=headers, timeout=DEFAULT_TIMEOUT)
