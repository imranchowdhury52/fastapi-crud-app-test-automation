from fastapi import Depends, FastAPI, HTTPException, Path, Response, status

from app.auth import require_token
from app.models import User, UserIn
from app.store import DuplicateEmailError, UserStore

app = FastAPI(title="Users API", version="1.1.0")
store = UserStore()

UserId = Path(ge=1, description="User ID, starting at 1")


def not_found():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def email_taken():
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")


@app.get("/")
def health_check():
    return {"status": "running"}


@app.get("/users", response_model=list[User])
def get_users():
    return store.list()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int = UserId):
    user = store.get(user_id)
    if user is None:
        raise not_found()
    return user


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED,
          dependencies=[Depends(require_token)])
def create_user(user: UserIn):
    try:
        return store.create(user)
    except DuplicateEmailError:
        raise email_taken()


@app.put("/users/{user_id}", response_model=User, dependencies=[Depends(require_token)])
def update_user(user: UserIn, user_id: int = UserId):
    try:
        updated = store.replace(user_id, user)
    except DuplicateEmailError:
        raise email_taken()
    if updated is None:
        raise not_found()
    return updated


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
            dependencies=[Depends(require_token)])
def delete_user(user_id: int = UserId):
    if not store.delete(user_id):
        raise not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
