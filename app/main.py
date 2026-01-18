from fastapi import FastAPI
from app.models import User
from fastapi import HTTPException

app = FastAPI()

users = []

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return user

@app.get("/users")
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
