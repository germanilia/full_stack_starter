from typing import Generator
from app.db import SessionLocal


def get_db() -> Generator:
    """
    Dependency for database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
