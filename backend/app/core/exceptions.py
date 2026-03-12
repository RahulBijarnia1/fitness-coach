"""
Custom exception classes for FitCoach AI API.

Provides a standardized exception hierarchy for consistent error handling
across the application.
"""

from typing import Any, Optional


class FitCoachException(Exception):
    """Base exception for FitCoach API."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Any] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)


class ValidationException(FitCoachException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class AuthenticationException(FitCoachException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR",
        )


class AuthorizationException(FitCoachException):
    """Raised when user lacks permissions."""
    
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR",
        )


class NotFoundException(FitCoachException):
    """Raised when a resource is not found."""
    
    def __init__(self, resource: str, identifier: Any = None):
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} with id '{identifier}' not found"
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
        )


class ConflictException(FitCoachException):
    """Raised when there's a resource conflict (e.g., duplicate entry)."""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=409,
            error_code="CONFLICT",
        )


class RateLimitException(FitCoachException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Too many requests. Please try again later."):
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
        )


class DatabaseException(FitCoachException):
    """Raised when database operation fails."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
        )


class ProfileRequiredException(FitCoachException):
    """Raised when user profile is required but not found."""
    
    def __init__(self):
        super().__init__(
            message="Please complete your profile before proceeding",
            status_code=400,
            error_code="PROFILE_REQUIRED",
        )


class GoalRequiredException(FitCoachException):
    """Raised when fitness goal is required but not set."""
    
    def __init__(self):
        super().__init__(
            message="Please set your fitness goal before proceeding",
            status_code=400,
            error_code="GOAL_REQUIRED",
        )
