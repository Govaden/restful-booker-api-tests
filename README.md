# restful-booker-api-tests

[![API Tests](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/api-tests.yml/badge.svg)](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/api-tests.yml)
[![Newman](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/newman.yml/badge.svg)](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/newman.yml)

API test automation built against the [Restful-Booker API](https://restful-booker.herokuapp.com/apidoc/). Two parallel implementations of the same suite cover full CRUD operations, authentication, and negative cases:

- **Python** (`python/`) — pytest + requests with a dedicated HTTP client module, shared fixtures, and documented API defects
- **Postman** (`postman/`) — a collection with environment variables, runnable via Collection Runner or Newman CLI

---

## Project Structure

```
restful-booker-api-tests/
├── python/
│   ├── booking_client.py   # HTTP wrapper functions for all endpoints
│   ├── conftest.py         # shared fixtures: base_url, auth_token, booking_dates, db_conn
│   ├── db/
│   │   ├── schema.sql      # SQLite bookings table definition
│   │   └── seed.py         # CLI script to seed a local bookings.db (git-ignored)
│   ├── pytest.ini          # test discovery config
│   ├── requirements.txt    # pinned dependencies
│   ├── Dockerfile          # builds the test runner image
│   ├── .dockerignore
│   ├── compose.yaml        # docker compose service for one-command test runs
│   ├── results/            # test reports land here after a Docker run (git-ignored)
│   └── tests/
│       ├── __init__.py
│       ├── test_bookings.py
│       ├── test_db_validation.py   # API-created booking reconciled against a mirrored SQLite row
│       └── test_db_aggregates.py   # COUNT/AVG/GROUP BY assertions against a seeded SQLite dataset
├── postman/
│   ├── restful-booker-collection.json
│   └── restful-booker-environment.json
├── .github/workflows/
│   ├── api-tests.yml       # Python pytest CI
│   └── newman.yml          # Postman/Newman CI
└── README.md
```

---

## Setup — Python

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

## Setup — Docker (no local Python required)

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.

The Docker build context is scoped to the `python/` folder only, so the `postman/` folder is never included in the image.

---

## Running Tests — Python

Run all tests:
```bash
python -m pytest
```

Run a specific test:
```bash
python -m pytest tests/test_bookings.py::test_create_booking
```

---

## Running Tests — Docker

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

**Running without Compose:**
```bash
cd python
docker build -t booker-python-tests .
docker run --rm -v "$(pwd)/results:/app/results" booker-python-tests
```

---

## Running Tests — Postman

1. Open Postman → **Import**
2. Import `postman/restful-booker-collection.json`
3. Import `postman/restful-booker-environment.json`
4. Select the environment from the top-right dropdown
5. Run **POST /auth** first to generate a token
6. Run the full collection via Collection Runner

**Newman (CLI):**
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

---

## Test Coverage — Python

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

## Test Coverage — Python (SQLite DB)

Pure-DB tests against an in-memory SQLite connection (`db_conn` fixture, schema from `python/db/schema.sql`). No live API calls except where noted.

| Test | Scenario |
|---|---|
| `test_booking_reconciles_with_db` | Creates a booking via the live API, mirrors it into SQLite, and asserts the read-back row matches the API response field-for-field |
| `test_count_bookings_per_date_range` | `COUNT(*) ... WHERE checkin BETWEEN ? AND ?` against a seeded multi-booking dataset, per month and full range |
| `test_avg_totalprice` | `AVG(totalprice)` over all seeded bookings |
| `test_group_by_depositpaid` | `GROUP BY depositpaid` count and average totalprice per group |

## Test Coverage — Postman

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
| `GET/booking/:id - Verify Deletion (404)` | GET /booking/:id | Positive — confirms the booking is gone after delete |

---

## Known API Behaviour

Restful-booker has a few known bugs. Tests assert on what it actually returns, with comments noting where a real API would differ:

| Scenario | Expected | Actual |
|---|---|---|
| PUT without auth | 403 | 200 |
| DELETE without auth | 403 | 201 |
| POST successful create | 201 | 200 |
| POST with invalid field types | 400 | 500 |

It's also sometimes slow, which can show up as a false `403` on a valid authenticated request. Reruns fix it — not a test bug.

---

## Reports & Artifacts

| Suite | Artifact | Location |
|---|---|---|
| Python (CI) | JUnit XML | `python/reports/junit/results.xml`, uploaded as the `junit-results` workflow artifact and rendered as a Checks-tab summary |
| Python (Docker) | HTML/JUnit | `python/results/` on the host, via a mounted volume |
| Postman (CI) | JSON + HTML (htmlextra) | uploaded as the `newman-report` workflow artifact |

---

## Dependencies

| Package | Version |
|---|---|
| pytest | 8.3.5 |
| requests | 2.32.3 |

---

## Continuous Integration

GitHub Actions runs both suites independently:

- [`api-tests.yml`](.github/workflows/api-tests.yml) — Python/pytest suite, on every push/PR to `main` plus a nightly scheduled run
- [`newman.yml`](.github/workflows/newman.yml) — Postman collection via Newman, on every push/PR to `main`

---

## Resources

- [Restful-Booker API — Docs](https://restful-booker.herokuapp.com/apidoc/)
- [pytest — Official Docs](https://docs.pytest.org/)
- [requests — Official Docs](https://requests.readthedocs.io/)
- [Newman — GitHub](https://github.com/postmanlabs/newman)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
