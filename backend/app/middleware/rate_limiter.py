"""
Rate limiting middleware for FitCoach AI API.

Uses SlowAPI to protect authentication endpoints from brute force attacks
and prevent API abuse.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime

from app.core.logging import logger


def get_client_identifier(request: Request) -> str:
    """
    Get unique identifier for rate limiting.
    
    Uses X-Forwarded-For header if behind proxy, otherwise uses client IP.
    Authenticated users get a different limit pool.
    
    Args:
        request: FastAPI request object
        
    Returns:
        String identifier for rate limiting
    """
    # Check for forwarded header (if behind load balancer)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = get_remote_address(request)
    
    return ip


# Initialize rate limiter
limiter = Limiter(
    key_func=get_client_identifier,
    default_limits=["200/minute"],  # Default limit for all endpoints
    storage_uri="memory://",  # In-memory storage (use Redis for production clusters)
)


def setup_rate_limiting(app: FastAPI):
    """
    Configure rate limiting for the application.
    
    Args:
        app: FastAPI application instance
    """
    app.state.limiter = limiter
    
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        """Handle rate limit exceeded errors."""
        logger.warning(
            f"Rate Limit Exceeded | ip={get_client_identifier(request)} | "
            f"path={request.url.path}"
        )
        
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "message": "Too many requests. Please try again later.",
                "error_code": "RATE_LIMIT_EXCEEDED",
                "details": {
                    "retry_after": "60 seconds"
                },
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    
    logger.info("Rate limiting configured")


# Rate limit decorators for different endpoint types
# Usage: @limiter.limit("5/minute") on route handlers

# Predefined limits:
# - Authentication endpoints: 5 requests per minute
# - Data mutation endpoints: 30 requests per minute
# - Read endpoints: 100 requests per minute

AUTH_LIMIT = "5/minute"  # Strict limit for login/register
WRITE_LIMIT = "30/minute"  # Moderate limit for create/update
READ_LIMIT = "100/minute"  # Generous limit for read operations
