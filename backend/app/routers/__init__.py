# backend/app/routers/__init__.py

from fastapi import APIRouter
from .user import user_router

router = APIRouter()

# Include route definitions
router.include_router(user_router, prefix="/api/v1", tags=["users"])