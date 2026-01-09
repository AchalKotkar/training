from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    return f"My name is {user.name} and I am {user.age} years old"

users = [
    {"id": 1, "name": "Rahul", "age": 25},
    {"id": 2, "name": "Anita", "age": 30},
    {"id": 3, "name": "Achal", "age": 22}
]

@app.get("/users")
#def get_users():
 #   return users

def get_users(age: int = None, name: str = None):
    result = users
    if age is not None:
        result = [u for u in result if u["age"] == age]
    if name is not None:
        result = [u for u in result if u["name"].lower() == name.lower()]
    return result


@app.get("/users/{user_id}")
def get_user(user_id: int):
    # search in list
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}
