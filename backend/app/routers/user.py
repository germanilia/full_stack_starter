from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.user import UserResponse

user_router = APIRouter()

# Mock user data (in a real app, this would come from a database)
MOCK_USERS = [
    {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "is_active": True
    },
    {
        "id": 2,
        "username": "janedoe",
        "email": "jane@example.com",
        "full_name": "Jane Doe",
        "is_active": True
    }
]

@user_router.get("/users/", response_model=List[UserResponse])
async def read_users():
    """
    Retrieve all users.
    """
    return MOCK_USERS

@user_router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int):
    """
    Retrieve a specific user by ID.
    """
    for user in MOCK_USERS:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")