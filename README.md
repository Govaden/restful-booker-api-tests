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