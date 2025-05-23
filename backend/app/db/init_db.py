import sys
from sqlalchemy.exc import SQLAlchemyError
from app.db import engine
from app.models import Base
from app.db.create_database import create_database
from app.core.logging_service import get_logger

# Get logger for this module
logger = get_logger(__name__)


def init_db():
    """
    Initialize the database by creating all tables if they don't exist.
    """
    try:
        logger.info("Creating database tables if they don't exist", operation="create_tables")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully", operation="create_tables", status="success")
        return True
    except SQLAlchemyError as e:
        logger.error(
            "Error creating database tables",
            operation="create_tables",
            status="error",
            error=str(e)
        )
        return False


if __name__ == "__main__":
    # This allows the script to be run directly

    # First, create the database if it doesn't exist
    logger.info("Ensuring database exists...")
    if not create_database():
        logger.error("Failed to create database")
        sys.exit(1)

    # Then initialize the database schema
    success = init_db()
    sys.exit(0 if success else 1)
