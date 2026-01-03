import requests

BASE_URL = "http://127.0.0.1:8000"


def test_create_user():
    payload = {
        "name": "Mahir",
        "email": "mahir@test.com"
    }

    response = requests.post(f"{BASE_URL}/users", json=payload)

    assert response.status_code == 201
    assert response.json()["name"] == "Mahir"


def test_get_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200


def test_get_non_existing_user():
    response = requests.get(f"{BASE_URL}/users/999")
    assert response.status_code == 404

