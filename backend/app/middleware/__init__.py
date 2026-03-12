"""
Middleware components for FitCoach AI API.
"""

from .error_handler import setup_exception_handlers
from .rate_limiter import limiter, setup_rate_limiting
from .request_logger import RequestLoggingMiddleware

__all__ = [
    "setup_exception_handlers",
    "limiter",
    "setup_rate_limiting",
    "RequestLoggingMiddleware",
]
