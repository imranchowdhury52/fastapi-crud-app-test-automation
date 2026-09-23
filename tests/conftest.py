import pytest
from fastapi.testclient import TestClient

from app.auth import API_TOKEN
from app.main import app, store

AUTH_HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}


@pytest.fixture(autouse=True)
def clean_store():
    """Every test starts with an empty user store."""
    store.reset()
    yield
    store.reset()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_client():
    with TestClient(app, headers=AUTH_HEADERS) as c:
        yield c


@pytest.fixture
def user_payload():
    return {"name": "Mahir", "email": "mahir@test.com", "age": 30}


@pytest.fixture
def created_user(auth_client, user_payload):
    response = auth_client.post("/users", json=user_payload)
    assert response.status_code == 201
    return response.json()
