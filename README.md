# FastAPI CRUD Service + API Test Suite

![CI](https://github.com/imranchowdhury52/fastapi-crud-app-test-automation/actions/workflows/ci.yml/badge.svg)

A REST API for managing users, built with FastAPI and Pydantic, and its end-to-end Pytest suite.
The suite covers CRUD flows, authentication, negative and boundary cases, and contract and
response-schema validation. It runs in-process with FastAPI's `TestClient`, so it needs no running
server and executes in CI on every push.

---

## Tech Stack

- Python 3.10+
- FastAPI, Pydantic v2
- Pytest, FastAPI TestClient (httpx)
- jsonschema
- GitHub Actions

---

## API

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/` | none | Health check |
| GET | `/users` | none | List users |
| GET | `/users/{id}` | none | Get a user |
| POST | `/users` | Bearer | Create a user |
| PUT | `/users/{id}` | Bearer | Replace a user |
| DELETE | `/users/{id}` | Bearer | Delete a user |

**Validation rules:** `name` 1–50 characters, `email` must be a valid address and unique
(case-insensitive), `age` 18–120, `id` ≥ 1.

**Status codes:** `201` created, `204` deleted, `401` missing or malformed token, `403` wrong token,
`404` not found, `409` duplicate email, `422` validation error.

---

## Test Coverage (55 tests)

| File | What it covers |
|---|---|
| `tests/test_crud.py` | Create, read, list, update, delete, and a full lifecycle test. Regression test for ID reuse after delete |
| `tests/test_validation.py` | **Boundary values** (min/max and one step outside for name length, age, and ID). **Negative cases**, data-driven: missing fields, bad email formats, wrong types, null, empty and malformed JSON. 404 and 409 handling |
| `tests/test_auth.py` | 401 without a token, 403 with a wrong token, malformed `Authorization` headers, rejected writes leave no data behind, reads stay public |
| `tests/test_contract.py` | Contract tests on the published OpenAPI document: endpoints, required fields, constraints, security schemes |
| `tests/schema.py` | **Response schema validation**: responses are checked with `jsonschema` against the schema the API publishes in OpenAPI |

Each test starts with an empty store (autouse fixture), so tests are independent and can run in any order.

---

## Project Structure

```text
fastapi-crud-app-test-automation/
├── app/
│   ├── main.py      # routes
│   ├── models.py    # Pydantic models + validation rules
│   ├── store.py     # in-memory storage
│   └── auth.py      # bearer token dependency
├── tests/
│   ├── conftest.py  # TestClient fixtures, store reset
│   ├── schema.py    # OpenAPI-based response schema validation
│   ├── test_crud.py
│   ├── test_validation.py
│   ├── test_auth.py
│   └── test_contract.py
└── .github/workflows/ci.yml
```

---

## Run the Tests

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt

pytest -v
pytest tests/test_validation.py -k boundary    # just the boundary tests
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Open Swagger UI at http://127.0.0.1:8000/docs. Click **Authorize** and enter the token
(default `dev-token`, override with the `API_TOKEN` environment variable).

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Authorization: Bearer dev-token" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mahir", "email": "mahir@test.com", "age": 30}'
```

---

## Author

Imran Chowdhury · [GitHub](https://github.com/imranchowdhury52) · [LinkedIn](https://www.linkedin.com/in/imran-chowdhury-187599102)
