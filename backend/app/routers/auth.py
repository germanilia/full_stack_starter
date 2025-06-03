"""
Authentication router for user registration, login, and token management.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_active_user
from app.schemas.auth import (
    SignUpRequest, SignUpResponse, ConfirmSignUpRequest, ConfirmSignUpResponse,
    SignInRequest, SignInResponse, RefreshTokenRequest, RefreshTokenResponse,
    UserInfo, MessageResponse
)
from app.services.cognito_service import cognito_service
from app.crud.user import UserCRUD
from app.models.user import User
from app.core.logging_service import get_logger
from app.utils.username_utils import validate_and_transform_email

logger = get_logger(__name__)

auth_router = APIRouter()


@auth_router.post("/signup", response_model=SignUpResponse)
async def sign_up(request: SignUpRequest, db: Session = Depends(get_db)):
    """
    Register a new user with Cognito and create user record in database.
    """
    try:
        # Validate and normalize email
        normalized_email, cognito_username = validate_and_transform_email(request.email)

        # Check if user already exists in database
        existing_email = UserCRUD.get_user_by_email(db, normalized_email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Sign up user with Cognito
        cognito_response = await cognito_service.sign_up(
            email=normalized_email,
            password=request.password,
            full_name=request.full_name or ""
        )

        # Create user record in database
        user = UserCRUD.create_user(
            db=db,
            username=normalized_email,  # Use email as username
            email=normalized_email,
            full_name=request.full_name,
            cognito_sub=cognito_response["user_sub"]
        )

        logger.info(f"User {normalized_email} signed up successfully")

        return SignUpResponse(
            message="User registered successfully. Please check your email for confirmation code.",
            user_sub=cognito_response["user_sub"],
            user_confirmed=cognito_response["user_confirmed"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Sign up failed for {request.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@auth_router.post("/confirm-signup", response_model=ConfirmSignUpResponse)
async def confirm_sign_up(request: ConfirmSignUpRequest):
    """
    Confirm user sign up with confirmation code.
    """
    try:
        await cognito_service.confirm_sign_up(
            email=request.email,
            confirmation_code=request.confirmation_code
        )

        logger.info(f"User {request.email} confirmed successfully")

        return ConfirmSignUpResponse(
            message="User confirmed successfully. You can now sign in."
        )

    except Exception as e:
        logger.error(f"Confirmation failed for {request.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@auth_router.post("/signin", response_model=SignInResponse)
async def sign_in(request: SignInRequest, db: Session = Depends(get_db)):
    """
    Sign in user and return access tokens.
    """
    try:
        # Authenticate with Cognito
        tokens = await cognito_service.sign_in(
            email=request.email,
            password=request.password
        )

        # Get user info from Cognito
        user_info = await cognito_service.get_user_info(tokens["access_token"])

        # Get or update user in database
        user = UserCRUD.get_user_by_cognito_sub(db, user_info["user_sub"])
        if not user:
            # User might exist with email but no cognito_sub
            user = UserCRUD.get_user_by_email(db, request.email)
            if user:
                # Update user with cognito_sub
                UserCRUD.update_user(db, user.id, cognito_sub=user_info["user_sub"])
            else:
                # Create new user record
                user = UserCRUD.create_user(
                    db=db,
                    username=request.email,  # Use email as username
                    email=user_info["email"],
                    full_name=user_info["name"],
                    cognito_sub=user_info["user_sub"]
                )

        logger.info(f"User {request.email} signed in successfully")
        
        return SignInResponse(
            access_token=tokens["access_token"],
            id_token=tokens["id_token"],
            refresh_token=tokens.get("refresh_token"),
            expires_in=tokens["expires_in"],
            user=UserInfo(
                username=str(user.username),
                email=str(user.email),
                full_name=str(user.full_name) if user.full_name is not None else None,
                role=user.role,
                is_active=bool(user.is_active),
                user_sub=str(user.cognito_sub) if user.cognito_sub is not None else None
            )
        )

    except Exception as e:
        logger.error(f"Sign in failed for {request.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@auth_router.post("/refresh-token", response_model=RefreshTokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token using refresh token.
    """
    try:
        tokens = await cognito_service.refresh_token(
            refresh_token=request.refresh_token,
            email=request.email
        )

        logger.info(f"Token refreshed successfully for {request.email}")

        return RefreshTokenResponse(
            access_token=tokens["access_token"],
            id_token=tokens["id_token"],
            expires_in=tokens["expires_in"]
        )

    except Exception as e:
        logger.error(f"Token refresh failed for {request.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )


@auth_router.get("/me", response_model=UserInfo)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information.
    """
    return UserInfo(
        username=str(current_user.username),
        email=str(current_user.email),
        full_name=str(current_user.full_name) if current_user.full_name is not None else None,
        role=current_user.role,
        is_active=bool(current_user.is_active),
        user_sub=str(current_user.cognito_sub) if current_user.cognito_sub is not None else None
    )


@auth_router.post("/signout", response_model=MessageResponse)
async def sign_out():
    """
    Sign out user (client should discard tokens).
    """
    return MessageResponse(
        message="Signed out successfully. Please discard your tokens."
    )
