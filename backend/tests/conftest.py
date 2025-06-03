"""
Pytest configuration and shared fixtures for backend tests.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.crud.user import UserDAO
from app.services.user_service import UserService


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user_dao():
    """Create a UserDAO instance."""
    return UserDAO()


@pytest.fixture
def user_service(user_dao):
    """Create a UserService instance with injected UserDAO."""
    return UserService(user_dao)
