# backend/app/routers/__init__.py

from fastapi import APIRouter
from .user import user_router  # Import and re-export the user_router

router = APIRouter()

# Include route definitions
from . import user
router.include_router(user.user_router, prefix="/api/v1", tags=["users"])