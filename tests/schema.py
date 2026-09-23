from jsonschema import validate

from app.main import app


def _openapi_schema(name):
    return app.openapi()["components"]["schemas"][name]


def assert_is_user(payload):
    """Validate a response body against the User schema the API itself publishes."""
    validate(instance=payload, schema=_openapi_schema("User"))


def assert_is_user_list(payload):
    validate(instance=payload, schema={"type": "array", "items": _openapi_schema("User")})
