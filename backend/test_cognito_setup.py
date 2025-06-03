"""
Test script to verify Cognito setup with LocalStack.
"""
import asyncio
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.services.cognito_service import cognito_service
from app.core.logging_service import get_logger

logger = get_logger(__name__)


async def test_cognito_setup():
    """Test Cognito service setup"""
    try:
        logger.info("Testing Cognito service setup...")
        
        # Test configuration
        config = cognito_service.config
        logger.info(f"User Pool ID: {config['user_pool_id']}")
        logger.info(f"Client ID: {config['client_id']}")
        logger.info(f"Endpoint URL: {config['endpoint_url']}")
        logger.info(f"Is LocalStack: {cognito_service.is_localstack}")
        
        # Test sign up (this will fail if Cognito is not set up, which is expected)
        try:
            test_username = "testuser123"
            test_email = "test@example.com"
            test_password = "TestPass123!"
            
            result = await cognito_service.sign_up(
                username=test_username,
                password=test_password,
                email=test_email,
                full_name="Test User"
            )
            logger.info(f"Sign up test successful: {result}")
            
        except Exception as e:
            logger.warning(f"Sign up test failed (expected if Cognito not set up): {e}")
        
        logger.info("Cognito service test completed")
        
    except Exception as e:
        logger.error(f"Cognito service test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_cognito_setup())
