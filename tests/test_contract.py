"""Contract tests: the published OpenAPI document is what clients rely on."""
import pytest


@pytest.fixture
def openapi(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    return response.json()


def test_all_endpoints_are_documented(openapi):
    paths = openapi["paths"]

    assert set(paths["/users"]) == {"get", "post"}
    assert set(paths["/users/{user_id}"]) == {"get", "put", "delete"}


def test_user_schema_fields(openapi):
    user = openapi["components"]["schemas"]["User"]

    assert set(user["required"]) == {"id", "name", "email", "age"}
    assert user["properties"]["email"]["format"] == "email"
    assert user["properties"]["age"]["minimum"] == 18
    assert user["properties"]["age"]["maximum"] == 120
    assert user["properties"]["name"]["maxLength"] == 50


def test_write_endpoints_declare_bearer_auth(openapi):
    assert openapi["components"]["securitySchemes"]["HTTPBearer"]["scheme"] == "bearer"
    assert openapi["paths"]["/users"]["post"]["security"] == [{"HTTPBearer": []}]
    for method in ("put", "delete"):
        assert openapi["paths"]["/users/{user_id}"][method]["security"] == [{"HTTPBearer": []}]


def test_read_endpoints_are_public(openapi):
    assert "security" not in openapi["paths"]["/users"]["get"]
    assert "security" not in openapi["paths"]["/users/{user_id}"]["get"]


def test_swagger_ui_is_served(client):
    response = client.get("/docs")

    assert response.status_code == 200
    assert "swagger-ui" in response.text
