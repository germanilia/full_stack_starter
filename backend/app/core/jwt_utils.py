"""
JWT utilities for token validation and user authentication.
"""
import jwt
import requests
from typing import Dict, Optional, Any
from datetime import datetime, timezone
from jose import JWTError, jwt as jose_jwt
from app.core.config_service import config_service
from app.core.logging_service import get_logger
from app.schemas.auth import TokenData

logger = get_logger(__name__)


class JWTValidator:
    """JWT token validator for Cognito tokens"""

    def __init__(self):
        self.cognito_config = config_service.get_cognito_config()
        self.is_localstack = config_service.is_localstack_enabled()
        self._jwks_cache: Optional[Dict[str, Any]] = None

    def _get_jwks_url(self) -> str:
        """Get the JWKS URL for token validation"""
        if self.is_localstack:
            # LocalStack JWKS endpoint
            return f"{self.cognito_config['endpoint_url']}/{self.cognito_config['user_pool_id']}/.well-known/jwks.json"
        else:
            # AWS Cognito JWKS endpoint
            region = self.cognito_config["region"]
            user_pool_id = self.cognito_config["user_pool_id"]
            return f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"

    def _get_jwks(self) -> Dict[str, Any]:
        """Get JSON Web Key Set (JWKS) for token validation"""
        if self._jwks_cache is None:
            try:
                jwks_url = self._get_jwks_url()
                response = requests.get(jwks_url, timeout=10)
                response.raise_for_status()
                self._jwks_cache = response.json()
                logger.info("Successfully fetched JWKS")
            except Exception as e:
                logger.error(f"Failed to fetch JWKS: {e}")
                raise Exception("Failed to fetch JWKS for token validation")
        
        return self._jwks_cache

    def _get_signing_key(self, token_header: Dict[str, Any]) -> str:
        """Get the signing key for token validation"""
        jwks = self._get_jwks()
        
        # Find the key that matches the token's kid
        kid = token_header.get("kid")
        if not kid:
            raise Exception("Token header missing 'kid' field")

        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                # Convert JWK to PEM format
                return jwt.algorithms.RSAAlgorithm.from_jwk(key)
        
        raise Exception(f"Unable to find signing key with kid: {kid}")

    def validate_token(self, token: str) -> TokenData:
        """Validate JWT token and return token data"""
        try:
            # Decode token header to get key ID
            unverified_header = jose_jwt.get_unverified_header(token)
            
            # Get signing key
            signing_key = self._get_signing_key(unverified_header)
            
            # Verify and decode token
            payload = jose_jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience=self.cognito_config["client_id"],
                options={"verify_exp": True}
            )
            
            # Extract token data
            username = payload.get("cognito:username") or payload.get("username")
            user_sub = payload.get("sub")
            email = payload.get("email")
            
            # Verify token type
            token_use = payload.get("token_use")
            if token_use not in ["access", "id"]:
                raise Exception("Invalid token type")
            
            # Check expiration
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                raise Exception("Token has expired")
            
            logger.info(f"Token validated successfully for user: {username}")
            
            return TokenData(
                username=username,
                user_sub=user_sub,
                email=email
            )
            
        except JWTError as e:
            logger.error(f"JWT validation error: {e}")
            raise Exception("Invalid token")
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
            raise Exception("Token validation failed")

    def decode_token_without_verification(self, token: str) -> Dict[str, Any]:
        """Decode token without verification (for debugging)"""
        try:
            return jose_jwt.get_unverified_claims(token)
        except Exception as e:
            logger.error(f"Failed to decode token: {e}")
            raise Exception("Failed to decode token")


# Global instance
jwt_validator = JWTValidator()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Create a local access token (fallback for development)"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc).timestamp() + expires_delta
    else:
        expire = datetime.now(timezone.utc).timestamp() + 3600  # 1 hour default
    
    to_encode.update({"exp": expire})
    
    # Use the secret key from configuration
    secret_key = config_service.get_secret_key()
    algorithm = config_service.get("security.algorithm", "HS256")
    
    encoded_jwt = jose_jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_local_token(token: str) -> Dict[str, Any]:
    """Verify a locally created token"""
    try:
        secret_key = config_service.get_secret_key()
        algorithm = config_service.get("security.algorithm", "HS256")
        
        payload = jose_jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError as e:
        logger.error(f"Local token validation error: {e}")
        raise Exception("Invalid local token")
