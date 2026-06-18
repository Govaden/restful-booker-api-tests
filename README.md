# 🔖 restful-booker-api-tests

A practice repository for learning and experimenting with API test automation using **Python**, **pytest**, and **requests** — as well as **Postman** — built against the [Restful-Booker API](https://restful-booker.herokuapp.com/apidoc/).

![API Tests](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/api-tests.yml/badge.svg)

---

## 📌 About

This repo contains two parallel implementations of the same API test suite covering full CRUD operations, authentication, and negative cases:

- **Python** (`python/`) — pytest + requests with a dedicated HTTP client module, shared fixtures, and documented API defects
- **Postman** (`postman/`) — a collection with environment variables, runnable via Collection Runner or Newman CLI

---

## 🗂️ Project Structure

```
restful-booker-api-tests/
├── python/
│   ├── booking_client.py   # HTTP wrapper functions for all endpoints
│   ├── conftest.py         # shared fixtures: base_url, auth_token, booking_dates
│   ├── pytest.ini          # test discovery config
│   ├── requirements.txt    # pinned dependencies
│   └── tests/
│       ├── __init__.py
│       └── test_bookings.py
├── postman/
│   ├── restful-booker-collection.json
│   └── restful-booker-environment.json
└── README.md
```

---

## ⚙️ Setup — Python

**1. Clone the repo**
```bash
git clone https://github.com/Govaden/restful-booker-api-tests.git
cd restful-booker-api-tests/python
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## ▶️ Running Tests — Python

Run all tests:
```bash
python -m pytest
```

Run a specific test:
```bash
python -m pytest tests/test_bookings.py::test_create_booking
```

---

## 📋 Test Coverage

| Test | Endpoint | Scenario |
|---|---|---|
| `test_get_bookings` | GET /booking | Positive + invalid ID |
| `test_get_booking_by_id` | GET /booking/:id | Positive |
| `test_get_bookings_filter_by_name` | GET /booking?firstname=&lastname= | Query params |
| `test_create_booking` | POST /booking | Positive |
| `test_create_booking_invalid_data` | POST /booking | Invalid payload |
| `test_update_booking` | PUT /booking/:id | Positive |
| `test_update_booking_invalid_data` | PUT /booking/:id | No auth |
| `test_partial_update_booking` | PATCH /booking/:id | Positive |
| `test_delete_booking` | DELETE /booking/:id | Positive + deletion verification |
| `test_delete_booking_without_auth` | DELETE /booking/:id | No auth |

---

## 🐛 Known API Behaviour

Restful-booker is an intentionally buggy sandbox. Tests assert on actual responses and include inline comments where a production API would behave differently:

| Scenario | Expected | Actual |
|---|---|---|
| PUT without auth | 403 | 200 |
| DELETE without auth | 403 | 201 |
| POST successful create | 201 | 200 |
| POST with invalid field types | 400 | 500 |

---

## 📮 Running Tests — Postman

1. Open Postman → **Import**
2. Import `postman/restful-booker-collection.json`
3. Import `postman/restful-booker-environment.json`
4. Select the environment from the top-right dropdown
5. Run **POST /auth** first to generate a token
6. Run the full collection via Collection Runner

### Newman (CLI)

```bash
npm install -g newman
newman run postman/restful-booker-collection.json \
  -e postman/restful-booker-environment.json \
  --delay-request 500
```

---

## 📦 Dependencies

| Package | Version |
|---|---|
| pytest | 8.3.5 |
| requests | 2.32.3 |

---

## 📚 Resources

- [Restful-Booker API — Docs](https://restful-booker.herokuapp.com/apidoc/)
- [pytest — Official Docs](https://docs.pytest.org/)
- [requests — Official Docs](https://requests.readthedocs.io/)
- [Newman — GitHub](https://github.com/postmanlabs/newman)
