# 🔖 restful-booker-api-tests

A practice repository for learning and experimenting with API test automation using **Python**, **pytest**, and **requests** — as well as **Postman** — built against the [Restful-Booker API](https://restful-booker.herokuapp.com/apidoc/).

![API Tests](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/api-tests.yml/badge.svg)
![Newman](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/newman.yml/badge.svg)

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
│   ├── Dockerfile          # builds the test runner image
│   ├── .dockerignore
│   ├── compose.yaml        # docker compose service for one-command test runs
│   ├── results/            # test reports land here after a Docker run (git-ignored)
│   └── tests/
│       ├── __init__.py
│       └── test_bookings.py
├── postman/
│   ├── restful-booker-collection.json
│   └── restful-booker-environment.json
├── .github/workflows/
│   ├── api-tests.yml        # Python pytest CI
│   └── newman.yml           # Postman/Newman CI
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

## 🐳 Setup — Docker (no local Python required)

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.

The Docker build context is scoped to the `python/` folder only, so the `postman/` folder is never included in the image.

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

## ▶️ Running Tests — Docker

From inside the `python/` folder:

```bash
cd python
docker compose up --build
```

This builds the image, runs the full pytest suite inside a container, and prints results to your terminal.

To see full build output:
```bash
docker compose build --progress=plain
```

**Test reports:** after a run, HTML/JUnit reports are available in `python/results/` the host machine — the container writes them there via a mounted volume, so they persist after the container exits.

**Running without Compose:**
```bash
cd python
docker build -t booker-python-tests .
docker run --rm -v "$(pwd)/results:/app/results" booker-python-tests
```

---

## 📋 Python Test Coverage

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

With the HTML/JSON report (same reporter used in CI):
```bash
npm install -g newman newman-reporter-htmlextra
newman run postman/restful-booker-collection.json \
  -e postman/restful-booker-environment.json \
  --delay-request 500 \
  --reporters cli,json,htmlextra \
  --reporter-json-export newman/report.json \
  --reporter-htmlextra-export newman/report.html
```

### CI

The collection runs automatically on every push/PR to `main` via [`.github/workflows/newman.yml`](.github/workflows/newman.yml). The JSON and HTML reports are uploaded as a `newman-report` workflow artifact.

---

## 📋 Postman Test Coverage

| Request | Endpoint | Scenario |
|---|---|---|
| `GET/ping` | GET /ping | Health check |
| `POST/auth` | POST /auth | Positive — valid credentials, token issued |
| `POST/auth - Invalid Credentials` | POST /auth | Negative — wrong password (no token issued) |
| `POST/booking` | POST /booking | Positive — creates a booking |
| `POST/booking - Malformed Body` | POST /booking | Negative — invalid field types (500) |
| `GET/booking` | GET /booking | Positive — lists all bookings |
| `GET/booking/:id` | GET /booking/:id | Positive — fetches a known booking |
| `GET/booking/:id - Non-existent ID (404)` | GET /booking/:id | Negative — unknown booking ID (404) |
| `PUT/booking - No Auth (403)` | PUT /booking/:id | Negative — missing auth token (403) |
| `PUT/booking` | PUT /booking/:id | Positive — full update with auth |
| `PATCH/booking` | PATCH /booking/:id | Positive — partial update with auth |
| `DELETE/booking - No Auth (403)` | DELETE /booking/:id | Negative — missing auth token (403) |
| `DELETE/booking` | DELETE /booking/:id | Positive — deletes the booking |

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
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
