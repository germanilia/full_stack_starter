"""
Populate test database with test users for testing purposes.
"""
import sys
import asyncio
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.user import User, UserRole
from app.core.config_service import config_service
from app.core.service_factory import get_cognito_service
from app.core.logging_service import get_logger

logger = get_logger(__name__)

# Test users configuration
TEST_USERS = [
    {
        "email": "admin@admin.com",
        "password": "Cowabunga2@",
        "full_name": "Test Admin User",
        "role": UserRole.ADMIN
    },
    {
        "email": "user@test.com", 
        "password": "TestPassword123!",
        "full_name": "Test Regular User",
        "role": UserRole.USER
    }
]


async def create_cognito_test_user(user_data: dict) -> str:
    """Create a test user in Cognito (real or mock)"""
    cognito_service = get_cognito_service()

    try:
        # Check if user already exists (for mock service)
        if hasattr(cognito_service, 'user_exists') and cognito_service.user_exists(user_data["email"]):
            logger.info(f"User {user_data['email']} already exists in Cognito")
            if config_service.use_mock_cognito():
                # For mock, return deterministic user_sub
                import hashlib
                email_hash = hashlib.md5(user_data["email"].encode()).hexdigest()[:8]
                return f"mock-user-{email_hash}"

        # Create new user
        cognito_response = await cognito_service.sign_up(
            email=user_data["email"],
            password=user_data["password"],
            full_name=user_data["full_name"]
        )

        user_sub = cognito_response["user_sub"]
        logger.info(f"✓ Created Cognito user: {user_data['email']} (sub: {user_sub})")
        return user_sub

    except Exception as e:
        logger.error(f"Failed to create Cognito user {user_data['email']}: {e}")
        raise


def create_database_user(db: Session, user_data: dict, cognito_sub: str) -> User:
    """Create a user in the database"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if existing_user:
            logger.info(f"User {user_data['email']} already exists in database")
            return existing_user

        # Create new user
        db_user = User(
            username=user_data["email"],
            email=user_data["email"],
            full_name=user_data["full_name"],
            cognito_sub=cognito_sub,
            role=user_data["role"],
            is_active=True
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"✓ Created database user: {user_data['email']} ({user_data['role'].value})")
        return db_user

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create database user {user_data['email']}: {e}")
        raise


async def populate_test_db():
    """Populate test database with test users"""
    if not config_service.is_testing():
        logger.error("This script should only be run in test environment")
        return False

    logger.info("Populating test database with test users")

    db = SessionLocal()
    try:
        created_users = []
        for user_data in TEST_USERS:
            try:
                # Create user in Cognito (real or mock)
                cognito_sub = await create_cognito_test_user(user_data)

                # Create user in database
                db_user = create_database_user(db, user_data, cognito_sub)
                created_users.append(db_user)

                logger.info(f"✓ Created complete user: {user_data['email']} (Cognito + DB)")

            except Exception as e:
                logger.error(f"Error creating test user {user_data['email']}: {e}")
                # Continue with other users
                continue

        logger.info(f"Successfully created {len(created_users)} test users")

        # If using mock Cognito, log that we're using database-backed authentication
        if config_service.use_mock_cognito():
            logger.info("Mock Cognito service configured to use database for authentication")

        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error populating test database: {e}")
        return False
    finally:
        db.close()


def populate_test_db_sync():
    """Synchronous wrapper for populate_test_db"""
    return asyncio.run(populate_test_db())


if __name__ == "__main__":
    # This allows the script to be run directly
    success = populate_test_db_sync()
    if success:
        logger.info("Test database populated successfully!")
        sys.exit(0)
    else:
        logger.error("Failed to populate test database")
        sys.exit(1)
