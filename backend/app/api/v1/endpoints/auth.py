"""
Authentication API endpoints (v1).

Provides user registration and login with JWT token generation.
Includes rate limiting for security.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse
from app.repositories.user_repository import UserRepository
from app.utils.password_hash import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.core.exceptions import AuthenticationException, ConflictException, ValidationException
from app.core.responses import create_response
from app.core.logging import logger, log_user_action
from app.middleware.rate_limiter import limiter, AUTH_LIMIT

router = APIRouter()


@router.post("/register", response_model=dict)
@limiter.limit(AUTH_LIMIT)
async def register(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.
    
    Creates a new user with hashed password and returns JWT token.
    
    Args:
        user_data: User registration data (email, password)
        
    Returns:
        JWT access token and user data
        
    Raises:
        ConflictException: If email already exists
        ValidationException: If password requirements not met
    """
    user_repo = UserRepository(db)
    
    # Check if email exists
    if user_repo.email_exists(user_data.email):
        logger.warning(f"Registration failed: Email already exists - {user_data.email}")
        raise ConflictException("An account with this email already exists")
    
    # Validate password strength
    if len(user_data.password) < 8:
        raise ValidationException("Password must be at least 8 characters long")
    
    # Create user
    hashed = hash_password(user_data.password)
    user = user_repo.create_user(email=user_data.email, password_hash=hashed)
    
    # Generate token
    token = create_access_token({"sub": str(user.id)})
    
    # Log action
    log_user_action(user.id, "register", {"email": user.email})
    logger.info(f"New user registered: {user.email}")
    
    return create_response(
        data={
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
        },
        message="Registration successful"
    )


@router.post("/login", response_model=dict)
@limiter.limit(AUTH_LIMIT)
async def login(
    request: Request,
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT token.
    
    Validates email and password, returns access token on success.
    
    Args:
        credentials: Login credentials (email, password)
        
    Returns:
        JWT access token and user data
        
    Raises:
        AuthenticationException: If credentials are invalid
    """
    user_repo = UserRepository(db)
    
    # Find user
    user = user_repo.get_by_email(credentials.email)
    
    if not user or not verify_password(credentials.password, user.password_hash):
        logger.warning(f"Login failed: Invalid credentials for {credentials.email}")
        raise AuthenticationException("Invalid email or password")
    
    # Generate token
    token = create_access_token({"sub": str(user.id)})
    
    # Log action
    log_user_action(user.id, "login", {"ip": request.client.host if request.client else "unknown"})
    logger.info(f"User logged in: {user.email}")
    
    return create_response(
        data={
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
        },
        message="Login successful"
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Refresh access token.
    
    Currently uses same token expiration. Will be enhanced with
    refresh token support in future version.
    
    Returns:
        New JWT access token
    """
    # TODO: Implement proper refresh token logic
    # For now, this is a placeholder
    return create_response(
        data=None,
        message="Token refresh not yet implemented",
        success=False
    )
