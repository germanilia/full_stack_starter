# backend/app/models/__init__.py

from app.db import Base
from .user import User

__all__ = ["User", "Base"]  # Export your models for easier access