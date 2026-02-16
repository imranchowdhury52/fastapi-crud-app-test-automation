# FastAPI CRUD API

A simple RESTful API built with FastAPI demonstrating full CRUD operations and automated testing.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Pytest

## Features

- Create user
- Retrieve all users
- Retrieve user by ID
- Update user
- Delete user
- Positive and negative test coverage
- In-memory data storage

## Run Application

1. Create virtual environment:
   python -m venv venv

2. Activate environment:
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Start server:
   uvicorn app.main:app --reload

5. Open Swagger UI:
   http://127.0.0.1:8000/docs

## Run Tests

pytest -v
