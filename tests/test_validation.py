import pytest

from app.models import AGE_MAX, AGE_MIN, NAME_MAX_LENGTH

VALID = {"name": "Mahir", "email": "mahir@test.com", "age": 30}


# ---------- Boundary values ----------

@pytest.mark.parametrize(
    "field, value",
    [
        ("name", "A"),
        ("name", "A" * NAME_MAX_LENGTH),
        ("age", AGE_MIN),
        ("age", AGE_MAX),
    ],
    ids=["name min length", "name max length", "age min", "age max"],
)
def test_boundary_values_are_accepted(auth_client, field, value):
    response = auth_client.post("/users", json={**VALID, field: value})

    assert response.status_code == 201
    assert response.json()[field] == value


@pytest.mark.parametrize(
    "field, value",
    [
        ("name", ""),
        ("name", "A" * (NAME_MAX_LENGTH + 1)),
        ("age", AGE_MIN - 1),
        ("age", AGE_MAX + 1),
    ],
    ids=["name empty", "name too long", "age below min", "age above max"],
)
def test_values_just_outside_boundaries_are_rejected(auth_client, field, value):
    response = auth_client.post("/users", json={**VALID, field: value})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]


@pytest.mark.parametrize("user_id", [0, -1], ids=["zero", "negative"])
def test_path_id_below_one_is_rejected(client, user_id):
    assert client.get(f"/users/{user_id}").status_code == 422


def test_non_numeric_path_id_is_rejected(client):
    assert client.get("/users/abc").status_code == 422


# ---------- Negative: invalid payloads (data-driven) ----------

INVALID_PAYLOADS = [
    ({"email": "a@test.com", "age": 30}, "name", "missing name"),
    ({"name": "A", "age": 30}, "email", "missing email"),
    ({"name": "A", "email": "a@test.com"}, "age", "missing age"),
    ({**VALID, "email": "not-an-email"}, "email", "email without @"),
    ({**VALID, "email": "user@"}, "email", "email without domain"),
    ({**VALID, "age": "thirty"}, "age", "age as text"),
    ({**VALID, "age": 30.5}, "age", "age as decimal"),
    ({**VALID, "name": None}, "name", "name null"),
]


@pytest.mark.parametrize(
    "payload, bad_field",
    [(p, f) for p, f, _ in INVALID_PAYLOADS],
    ids=[i for _, _, i in INVALID_PAYLOADS],
)
def test_invalid_payload_is_rejected(auth_client, payload, bad_field):
    response = auth_client.post("/users", json=payload)

    assert response.status_code == 422
    assert ["body", bad_field] in [error["loc"] for error in response.json()["detail"]]


def test_empty_body_is_rejected(auth_client):
    assert auth_client.post("/users", json={}).status_code == 422


def test_malformed_json_is_rejected(auth_client):
    response = auth_client.post(
        "/users", content="{not json", headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422


def test_invalid_payload_does_not_create_user(client, auth_client):
    auth_client.post("/users", json={**VALID, "email": "bad"})

    assert client.get("/users").json() == []


# ---------- Negative: not found and conflicts ----------

def test_get_non_existing_user(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_non_existing_user(auth_client):
    assert auth_client.put("/users/999", json=VALID).status_code == 404


def test_delete_non_existing_user(auth_client):
    assert auth_client.delete("/users/999").status_code == 404


def test_delete_twice_returns_404(auth_client, created_user):
    auth_client.delete(f"/users/{created_user['id']}")

    assert auth_client.delete(f"/users/{created_user['id']}").status_code == 404


@pytest.mark.parametrize("email", ["mahir@test.com", "MAHIR@TEST.COM"], ids=["same", "different case"])
def test_duplicate_email_is_rejected(auth_client, created_user, email):
    response = auth_client.post("/users", json={**VALID, "name": "Other", "email": email})

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


def test_update_to_another_users_email_is_rejected(auth_client, created_user):
    other = auth_client.post("/users", json={**VALID, "email": "other@test.com"}).json()

    response = auth_client.put(f"/users/{other['id']}", json={**VALID, "email": created_user["email"]})

    assert response.status_code == 409
