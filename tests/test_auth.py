import pytest

VALID = {"name": "Mahir", "email": "mahir@test.com", "age": 30}

WRITE_REQUESTS = [
    ("post", "/users", VALID),
    ("put", "/users/1", VALID),
    ("delete", "/users/1", None),
]


@pytest.mark.parametrize("method, url, body", WRITE_REQUESTS, ids=["POST", "PUT", "DELETE"])
def test_write_without_token_returns_401(client, method, url, body):
    response = client.request(method, url, json=body)

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.parametrize("method, url, body", WRITE_REQUESTS, ids=["POST", "PUT", "DELETE"])
def test_write_with_wrong_token_returns_403(client, method, url, body):
    response = client.request(method, url, json=body, headers={"Authorization": "Bearer wrong"})

    assert response.status_code == 403


@pytest.mark.parametrize(
    "header",
    ["dev-token", "Basic dev-token", "Bearer"],
    ids=["no scheme", "wrong scheme", "scheme without token"],
)
def test_malformed_authorization_header_returns_401(client, header):
    response = client.post("/users", json=VALID, headers={"Authorization": header})

    assert response.status_code == 401


def test_rejected_write_does_not_change_data(client):
    client.post("/users", json=VALID)

    assert client.get("/users").json() == []


def test_reads_do_not_need_a_token(client, created_user):
    assert client.get("/users").status_code == 200
    assert client.get(f"/users/{created_user['id']}").status_code == 200
