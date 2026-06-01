# Restful-Booker API Test Suite

Postman collection covering full CRUD operations for the
[Restful-Booker API](https://restful-booker.herokuapp.com/apidoc/).

## Endpoints Covered
- POST /auth
- POST /booking
- GET /booking
- GET /booking/:id
- PUT /booking/:id
- PATCH /booking/:id
- DELETE /booking/:id
- GET /booking/:id (deletion verification)

## How to Import
1. Open Postman
2. Click **Import**
3. Import `collections/restful-booker-collection.json`
4. Import `environments/restful-booker-environment.json`
5. Select the environment from the top-right dropdown
6. Run **POST /auth** first to generate a token
7. Run the full collection via Collection Runner

## Environment Variables
| Variable | Description | Set by |
|---|---|---|
| `baseUrl` | API base URL | Manual |
| `authToken` | Session token | POST /auth |
| `bookingId` | Created booking ID | POST /booking |

## How to work with Newman

### Resources

- [Node.js](https://nodejs.org) (LTS version)
- [Newman](https://www.npmjs.com/package/newman) — Postman's CLI runner

### Install Newman

```bash
npm install -g newman
```

### Basic Run

```bash
newman run collections/restful-booker-collection.json -e environments/restful-booker-environment.json
```

### Run with Delay (recommended — gives the API time between requests)

```bash
newman run collections/restful-booker-collection.json -e environments/restful-booker-environment.json --delay-request 500
```