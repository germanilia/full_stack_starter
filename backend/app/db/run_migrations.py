import os
import sys
import logging
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """
    Run database migrations using Alembic.
    This function uses the database URL from the config service via alembic/env.py.
    """
    try:
        # Get the path to the alembic directory
        backend_dir = Path(__file__).resolve().parent.parent.parent
        alembic_dir = backend_dir / "alembic"
        
        logger.info("Running database migrations...")
        
        # Run alembic upgrade head
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=str(backend_dir),
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info(f"Migration output:\n{result.stdout}")
        if result.stderr:
            logger.warning(f"Migration warnings/errors:\n{result.stderr}")
            
        logger.info("Database migrations completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed with error code {e.returncode}")
        logger.error(f"Error output:\n{e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        return False

if __name__ == "__main__":
    # This allows the script to be run directly
    success = run_migrations()
    sys.exit(0 if success else 1)
