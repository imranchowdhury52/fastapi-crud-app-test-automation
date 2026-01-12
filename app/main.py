from fastapi import FastAPI, HTTPException
from app.models import User

app = FastAPI()

# In-memory storage
users = []


@app.get("/")
def health_check():
    return {"status": "running"}


@app.post("/users", status_code=201)
def create_user(user: User):
    user.id = len(users) + 1
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


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            updated_user.id = user_id
            users[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return
    raise HTTPException(status_code=404, detail="User not found")
