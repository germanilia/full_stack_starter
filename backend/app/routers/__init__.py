# backend/app/routers/__init__.py

from fastapi import APIRouter
from .user import user_router
from .auth import auth_router
from .dev import dev_router

router = APIRouter()

# Include route definitions
router.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
router.include_router(user_router, prefix="/api/v1", tags=["users"])
router.include_router(dev_router, prefix="/api/v1/dev", tags=["development"])