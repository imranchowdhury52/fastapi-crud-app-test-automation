from app.models import User, UserIn


class DuplicateEmailError(Exception):
    pass


class UserStore:
    """In-memory storage. IDs come from a counter so they are never reused after a delete."""

    def __init__(self):
        self.reset()

    def reset(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def list(self) -> list[User]:
        return list(self._users.values())

    def get(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def create(self, data: UserIn) -> User:
        self._check_email_free(data.email)
        user = User(id=self._next_id, **data.model_dump())
        self._users[user.id] = user
        self._next_id += 1
        return user

    def replace(self, user_id: int, data: UserIn) -> User | None:
        if user_id not in self._users:
            return None
        self._check_email_free(data.email, ignore_id=user_id)
        user = User(id=user_id, **data.model_dump())
        self._users[user_id] = user
        return user

    def delete(self, user_id: int) -> bool:
        return self._users.pop(user_id, None) is not None

    def _check_email_free(self, email: str, ignore_id: int | None = None):
        for user in self._users.values():
            if user.id != ignore_id and user.email.lower() == email.lower():
                raise DuplicateEmailError(email)
