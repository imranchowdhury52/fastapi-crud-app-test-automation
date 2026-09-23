from pydantic import BaseModel, EmailStr, Field

NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 50
AGE_MIN = 18
AGE_MAX = 120


class UserIn(BaseModel):
    """Payload for creating or replacing a user."""

    name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
    email: EmailStr
    age: int = Field(ge=AGE_MIN, le=AGE_MAX)


class User(UserIn):
    id: int
