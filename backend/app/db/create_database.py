import logging
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config_service import config_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """
    Create the database if it doesn't exist.
    """
    # Get database connection parameters from config
    db_url = config_service.get_database_url()

    # Parse the database URL to get connection parameters
    # Format: postgresql://username:password@host:port/database
    db_url_parts = db_url.replace("postgresql://", "").split("/")
    connection_string = db_url_parts[0]
    db_name = db_url_parts[1] if len(db_url_parts) > 1 else "mydatabase"

    # Parse connection string to get user, password, host, port
    user_pass, host_port = connection_string.split("@")
    user, password = user_pass.split(":") if ":" in user_pass else (user_pass, "")
    host, port = host_port.split(":") if ":" in host_port else (host_port, 5432)

    db_params = {
        "user": user,
        "password": password,
        "host": host,
        "port": port,
    }

    logger.info(f"Using database name: {db_name}")
    logger.info(f"Using host: {host}, port: {port}")

    try:
        # Connect to PostgreSQL server (to postgres database)
        logger.info(f"Connecting to PostgreSQL server at {db_params['host']}:{db_params['port']}")
        conn = psycopg2.connect(**db_params, database="postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            logger.info(f"Creating database '{db_name}'")
            cursor.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"Database '{db_name}' created successfully")
        else:
            logger.info(f"Database '{db_name}' already exists")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        return False

if __name__ == "__main__":
    # This allows the script to be run directly
    success = create_database()
    sys.exit(0 if success else 1)
