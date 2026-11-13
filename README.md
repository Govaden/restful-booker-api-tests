# restful-booker-api-tests

[![API Tests](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/api-tests.yml/badge.svg)](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/api-tests.yml)
[![Newman](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/newman.yml/badge.svg)](https://github.com/Govaden/restful-booker-api-tests/actions/workflows/newman.yml)

API test automation built against the [Restful-Booker API](https://restful-booker.herokuapp.com/apidoc/). Two parallel implementations of the same suite cover full CRUD operations, authentication, and negative cases:

- **Python** (`python/`) — pytest + requests with a dedicated HTTP client module, shared fixtures, documented API defects, and response bodies validated against an OpenAPI specification
- **Postman** (`postman/`) — a collection with environment variables, runnable via Collection Runner or Newman CLI

---

## Project Structure

```
restful-booker-api-tests/
├── python/
│   ├── booking_client.py   # HTTP wrapper functions for all endpoints
│   ├── conftest.py         # shared fixtures: base_url, auth_token, booking_dates, db_conn
│   ├── db/
│   │   ├── schema.sql      # SQLite bookings and booking_needs table definitions
│   │   └── seed.py         # CLI script to seed a local bookings.db (git-ignored)
│   ├── openapi/
│   │   └── restful-booker.yaml   # OpenAPI 3.1 spec of the API's observed behaviour
│   ├── schema_validation.py      # loads the spec and validates response bodies against its schemas
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
│       ├── test_db_aggregates.py   # COUNT/AVG/GROUP BY assertions against a seeded SQLite dataset
│       ├── test_db_joins.py        # INNER/LEFT JOIN and JOIN + GROUP BY assertions across bookings and booking_needs
│       ├── test_openapi_spec.py    # the spec passes openapi-spec-validator and its schemas are valid JSON Schema 2020-12
│       └── test_schema_validation.py   # offline checks of the schema helper with static response bodies
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

Five of these tests also validate the response body against a schema from the OpenAPI spec: `test_get_bookings` (`BookingList`), `test_get_booking_by_id` (`Booking`), `test_create_booking` (`CreatedBooking`), `test_update_booking` (`Booking`) and `test_partial_update_booking` (`Booking`).

## Test Coverage — Python (OpenAPI spec and schema helper)

Offline tests. No live API calls.

| Test | Scenario |
|---|---|
| `test_openapi_spec_is_valid` | The spec file passes `openapi-spec-validator` |
| `test_spec_uses_json_schema_2020_12_dialect` | The spec declares the JSON Schema 2020-12 dialect that the helper validates with |
| `test_component_schema_is_valid_json_schema` | Each schema under `components/schemas` is a valid JSON Schema 2020-12 schema (one case per schema) |
| `test_valid_booking_passes` | A complete booking body matches `Booking` |
| `test_booking_without_optional_field_passes` | A booking without `additionalneeds` matches `Booking` |
| `test_booking_with_wrong_type_fails` | A string `totalprice` fails and the message names the field |
| `test_booking_missing_required_field_fails` | A booking without `lastname` fails |
| `test_nested_reference_is_validated` | A `CreatedBooking` whose nested `bookingdates` lacks `checkout` fails at the nested path |
| `test_valid_created_booking_passes` | A complete create response matches `CreatedBooking` |
| `test_booking_list_with_wrong_item_fails` | A non-integer `bookingid` in a list fails at its index |
| `test_unknown_schema_name_fails` | An unknown schema name raises a clear error |

## Test Coverage — Python (SQLite DB)

Pure-DB tests against an in-memory SQLite connection (`db_conn` fixture, schema from `python/db/schema.sql`). No live API calls except where noted.

| Test | Scenario |
|---|---|
| `test_booking_reconciles_with_db` | Creates a booking via the live API, mirrors it into SQLite, and asserts the read-back row matches the API response field-for-field |
| `test_count_bookings_per_date_range` | `COUNT(*) ... WHERE checkin BETWEEN ? AND ?` against a seeded multi-booking dataset, per month and full range |
| `test_avg_totalprice` | `AVG(totalprice)` over all seeded bookings |
| `test_group_by_depositpaid` | `GROUP BY depositpaid` count and average totalprice per group |
| `test_booking_needs_reconcile_with_db` | Creates a booking with `additionalneeds` via the live API, mirrors it into `bookings` and `booking_needs` (split on commas), and asserts an `INNER JOIN` returns the same needs as the API |
| `test_bookings_without_needs` | `LEFT JOIN ... WHERE n.id IS NULL` finds bookings that have no needs |
| `test_count_needs_per_booking` | `LEFT JOIN` + `COUNT` + `GROUP BY` per booking on a seeded dataset |
| `test_sum_totalprice_per_need` | `JOIN` + `SUM(totalprice)` + `GROUP BY need` on a seeded dataset |

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

## API Specification

[`python/openapi/restful-booker.yaml`](python/openapi/restful-booker.yaml) is an OpenAPI 3.1 specification of the endpoints this suite tests: `POST /auth`, `GET /booking`, `GET /booking/{id}`, `POST /booking`, `PUT /booking/{id}`, `PATCH /booking/{id}` and `DELETE /booking/{id}`.

It describes the API's actual behaviour as observed against the live API, not idealised REST behaviour. Where the API differs from REST conventions, the operation's description says so, and the quirk is listed under [Known API Behaviour](#known-api-behaviour).

It lives in `python/` so that local runs, CI (working directory `python/`) and the Docker image (build context `python/`) can all read it.

To view it, open [Swagger Editor](https://editor.swagger.io/) and paste the file's contents, or import the file.

### How schema validation works

- [`python/schema_validation.py`](python/schema_validation.py) loads the spec once and caches it.
- `assert_matches_schema(body, "Booking")` validates a parsed JSON body against `#/components/schemas/Booking`, resolving any `$ref` to other component schemas.
- The spec sets `jsonSchemaDialect` to JSON Schema 2020-12, and the helper validates with `jsonschema`'s `Draft202012Validator`, so both use the same dialect.
- On a mismatch the test fails with an `AssertionError` that lists every error with its JSON path, for example `Booking: $.totalprice: '150' is not of type 'integer', 'null'`.
- `format` keywords are not enforced; the date fields are typed as plain strings because the API can return `0NaN-aN-aN` (see below).

---

## Known API Behaviour

Restful-booker has a few known bugs. Tests assert on what it actually returns, with comments noting where a real API would differ:

| Scenario | Expected | Actual |
|---|---|---|
| PUT without auth | 403 | 200 |
| DELETE without auth | 403 | 201 |
| POST successful create | 201 | 200 |
| POST with invalid field types | 400 | 500 |
| POST /auth with wrong credentials | 401 | 200 with `{"reason": "Bad credentials"}` |
| POST without `bookingdates` | 400 | 500 |
| POST with non-numeric `totalprice` and `bookingdates` present | 400 | 200, `totalprice` saved as `null` |
| POST with string `depositpaid` and `bookingdates` present | 400 | 200, `depositpaid` saved as `true` |
| POST with decimal `totalprice` | 400 or value kept | 200, saved as an integer (150.5 → 150) |
| GET /booking/:id or POST /booking without an Accept header | 200 | 418 |
| PUT without `additionalneeds` | field cleared | previous value kept |
| PATCH with only `bookingdates.checkin` | `checkout` unchanged | `checkout` becomes `0NaN-aN-aN` |
| DELETE successful | 200 or 204 | 201 with plain-text `Created` |
| DELETE an already-deleted booking | 404 | 405 |

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
| jsonschema | 4.26.0 |
| PyYAML | 6.0.3 |
| openapi-spec-validator | 0.9.0 |

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
