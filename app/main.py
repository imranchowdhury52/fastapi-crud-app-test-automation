from fastapi import FastAPI
from app.models import User

app = FastAPI()

users = []

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return user

@app.get("/users")
def get_users():
    return users
