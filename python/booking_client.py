import requests

def get_all_bookings(base_url):
    return requests.get(f"{base_url}/booking")

def get_booking_by_id(base_url, booking_id):
    return requests.get(f"{base_url}/booking/{booking_id}")

def create_booking(base_url, payload, headers):
    return requests.post(f"{base_url}/booking", json=payload, headers=headers)

def update_booking(base_url, booking_id, payload, headers):
    return requests.put(f"{base_url}/booking/{booking_id}", json=payload, headers=headers)

def delete_booking(base_url, booking_id, headers):
    return requests.delete(f"{base_url}/booking/{booking_id}", headers=headers)