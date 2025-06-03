"""
Unit tests for authentication endpoints focusing on admin role assignment.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db
from app.models.user import UserRole


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth_endpoints.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """Create a test client."""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


class TestAuthEndpoints:
    """Test authentication endpoints with focus on admin role assignment."""

    @patch('app.services.cognito_service.cognito_service.sign_up')
    def test_signup_endpoint_creates_first_user_as_admin(self, mock_sign_up, client):
        """Test that signup endpoint creates first user as admin."""
        # Mock Cognito signup
        mock_sign_up.return_value = {
            "user_sub": "cognito_sub_123",
            "user_confirmed": True
        }
        
        # Test signup
        response = client.post("/api/v1/auth/signup", json={
            "email": "admin@example.com",
            "password": "TestPass123!",
            "full_name": "Admin User"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_sub"] == "cognito_sub_123"
        assert "message" in data
        
        # Verify Cognito was called
        mock_sign_up.assert_called_once()

    @patch('app.services.cognito_service.cognito_service.sign_up')
    def test_signup_endpoint_prevents_duplicate_email(self, mock_sign_up, client):
        """Test that signup endpoint prevents duplicate email registration."""
        # Mock Cognito signup
        mock_sign_up.return_value = {
            "user_sub": "cognito_sub_123",
            "user_confirmed": True
        }
        
        # First signup
        response1 = client.post("/api/v1/auth/signup", json={
            "email": "user@example.com",
            "password": "TestPass123!",
            "full_name": "User One"
        })
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = client.post("/api/v1/auth/signup", json={
            "email": "user@example.com",
            "password": "TestPass123!",
            "full_name": "User Two"
        })
        assert response2.status_code == 400
        assert "Email already registered" in response2.json()["detail"]

    @patch('app.services.cognito_service.cognito_service.sign_in')
    @patch('app.services.cognito_service.cognito_service.get_user_info')
    @patch('app.services.cognito_service.cognito_service.sign_up')
    def test_signin_endpoint_returns_admin_role_for_first_user(
        self, 
        mock_sign_up,
        mock_get_user_info,
        mock_sign_in,
        client
    ):
        """Test that signin endpoint returns admin role for first user."""
        # Mock Cognito responses
        mock_sign_up.return_value = {
            "user_sub": "cognito_sub_123",
            "user_confirmed": True
        }
        
        mock_sign_in.return_value = {
            "access_token": "mock_access_token",
            "id_token": "mock_id_token",
            "refresh_token": "mock_refresh_token",
            "expires_in": 3600
        }
        
        mock_get_user_info.return_value = {
            "user_sub": "cognito_sub_123",
            "email": "admin@example.com",
            "name": "Admin User"
        }
        
        # First, signup the user
        signup_response = client.post("/api/v1/auth/signup", json={
            "email": "admin@example.com",
            "password": "TestPass123!",
            "full_name": "Admin User"
        })
        assert signup_response.status_code == 200
        
        # Then signin
        signin_response = client.post("/api/v1/auth/signin", json={
            "email": "admin@example.com",
            "password": "TestPass123!"
        })
        
        assert signin_response.status_code == 200
        data = signin_response.json()
        
        # Verify response structure
        assert "access_token" in data
        assert "user" in data
        
        # Verify user has admin role
        user_info = data["user"]
        assert user_info["role"] == "admin"
        assert user_info["email"] == "admin@example.com"

    @patch('app.services.cognito_service.cognito_service.sign_in')
    @patch('app.services.cognito_service.cognito_service.get_user_info')
    @patch('app.services.cognito_service.cognito_service.sign_up')
    def test_signin_creates_user_if_not_exists(
        self,
        mock_sign_up,
        mock_get_user_info,
        mock_sign_in,
        client
    ):
        """Test that signin creates user in database if they don't exist."""
        # Mock Cognito responses for signin without prior signup
        mock_sign_in.return_value = {
            "access_token": "mock_access_token",
            "id_token": "mock_id_token",
            "refresh_token": "mock_refresh_token",
            "expires_in": 3600
        }
        
        mock_get_user_info.return_value = {
            "user_sub": "cognito_sub_456",
            "email": "newuser@example.com",
            "name": "New User"
        }
        
        # Signin without prior signup (user exists in Cognito but not in our DB)
        signin_response = client.post("/api/v1/auth/signin", json={
            "email": "newuser@example.com",
            "password": "TestPass123!"
        })
        
        assert signin_response.status_code == 200
        data = signin_response.json()
        
        # Verify user was created and has admin role (first user)
        user_info = data["user"]
        assert user_info["role"] == "admin"  # Should be admin as first user
        assert user_info["email"] == "newuser@example.com"

    def test_signup_endpoint_validation(self, client):
        """Test signup endpoint input validation."""
        # Test missing email
        response = client.post("/api/v1/auth/signup", json={
            "password": "TestPass123!",
            "full_name": "Test User"
        })
        assert response.status_code == 422
        
        # Test invalid email
        response = client.post("/api/v1/auth/signup", json={
            "email": "invalid-email",
            "password": "TestPass123!",
            "full_name": "Test User"
        })
        assert response.status_code == 422
        
        # Test short password
        response = client.post("/api/v1/auth/signup", json={
            "email": "test@example.com",
            "password": "short",
            "full_name": "Test User"
        })
        assert response.status_code == 422

    def test_signin_endpoint_validation(self, client):
        """Test signin endpoint input validation."""
        # Test missing email
        response = client.post("/api/v1/auth/signin", json={
            "password": "TestPass123!"
        })
        assert response.status_code == 422
        
        # Test missing password
        response = client.post("/api/v1/auth/signin", json={
            "email": "test@example.com"
        })
        assert response.status_code == 422
        
        # Test invalid email format
        response = client.post("/api/v1/auth/signin", json={
            "email": "invalid-email",
            "password": "TestPass123!"
        })
        assert response.status_code == 422

    @patch('app.services.cognito_service.cognito_service.sign_in')
    def test_signin_handles_cognito_errors(self, mock_sign_in, client):
        """Test that signin endpoint handles Cognito errors gracefully."""
        # Mock Cognito error
        mock_sign_in.side_effect = Exception("Invalid credentials")
        
        response = client.post("/api/v1/auth/signin", json={
            "email": "test@example.com",
            "password": "WrongPass123!"
        })
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
