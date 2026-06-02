import requests
from config import BASE_URL

### POST/auth

auth_respone = requests.post(f"{BASE_URL}/auth",
 json={"username": "admin", "password": "password123"})

token = auth_respone.json().get("token")

### GET/booking

print("POST/auth")
print("Status code:", auth_respone.status_code)
print("Token:", token)
print("Header:", auth_respone.headers)
print("Elapsed time:", auth_respone.elapsed.total_seconds(), "seconds")
print()

list_of_bookings = requests.get(f"{BASE_URL}/booking")

print("GET/booking")
print("Status code:", list_of_bookings.status_code)
print("Response body:", list_of_bookings.json())
print("Text:", list_of_bookings.text)
print("Elapsed time:", list_of_bookings.elapsed.total_seconds(), "seconds")
print()

### GET/booking/{id}

booking_id = list_of_bookings.json()[0]["bookingid"]

single_booking = requests.get(f"{BASE_URL}/booking/{booking_id}")

print("GET/booking/{id}")
print("Status code:", single_booking.status_code)
print("Response body:", single_booking.json())
print("Elapsed time:", single_booking.elapsed.total_seconds(), "seconds")
