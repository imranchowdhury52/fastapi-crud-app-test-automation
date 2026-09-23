from tests.schema import assert_is_user, assert_is_user_list


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "running"}


def test_list_is_empty_initially(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == []


def test_create_user(auth_client, user_payload):
    response = auth_client.post("/users", json=user_payload)

    assert response.status_code == 201
    body = response.json()
    assert_is_user(body)
    assert body == {"id": 1, **user_payload}


def test_get_user_by_id(client, created_user):
    response = client.get(f"/users/{created_user['id']}")

    assert response.status_code == 200
    assert_is_user(response.json())
    assert response.json() == created_user


def test_list_users(client, auth_client):
    auth_client.post("/users", json={"name": "A", "email": "a@test.com", "age": 20})
    auth_client.post("/users", json={"name": "B", "email": "b@test.com", "age": 40})

    response = client.get("/users")

    assert response.status_code == 200
    assert_is_user_list(response.json())
    assert [u["name"] for u in response.json()] == ["A", "B"]


def test_update_user(auth_client, created_user):
    changes = {"name": "Mahir Updated", "email": "new@test.com", "age": 31}

    response = auth_client.put(f"/users/{created_user['id']}", json=changes)

    assert response.status_code == 200
    assert_is_user(response.json())
    assert response.json() == {"id": created_user["id"], **changes}


def test_update_keeps_own_email(auth_client, created_user, user_payload):
    response = auth_client.put(f"/users/{created_user['id']}", json={**user_payload, "age": 45})

    assert response.status_code == 200
    assert response.json()["age"] == 45


def test_delete_user(client, auth_client, created_user):
    response = auth_client.delete(f"/users/{created_user['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/users/{created_user['id']}").status_code == 404


def test_full_user_lifecycle(client, auth_client, user_payload):
    """End-to-end: create -> read -> update -> read -> delete -> gone."""
    user_id = auth_client.post("/users", json=user_payload).json()["id"]
    assert client.get(f"/users/{user_id}").json()["name"] == "Mahir"

    auth_client.put(f"/users/{user_id}", json={**user_payload, "name": "Renamed"})
    assert client.get(f"/users/{user_id}").json()["name"] == "Renamed"

    auth_client.delete(f"/users/{user_id}")
    assert client.get(f"/users/{user_id}").status_code == 404
    assert client.get("/users").json() == []


def test_ids_are_not_reused_after_delete(auth_client):
    """Regression: IDs used to be len(users) + 1, which gave duplicate IDs after a delete."""
    first = auth_client.post("/users", json={"name": "A", "email": "a@test.com", "age": 20}).json()
    second = auth_client.post("/users", json={"name": "B", "email": "b@test.com", "age": 20}).json()
    auth_client.delete(f"/users/{first['id']}")

    third = auth_client.post("/users", json={"name": "C", "email": "c@test.com", "age": 20}).json()

    assert third["id"] not in (first["id"], second["id"])
