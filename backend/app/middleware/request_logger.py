"""
Request logging middleware for FitCoach AI API.

Logs all incoming requests with timing information for
performance monitoring and debugging.
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import logger, log_api_request


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs all HTTP requests with timing information.
    
    Captures:
    - Request method and path
    - Response status code
    - Request duration in milliseconds
    - Client IP address
    """
    
    # Paths to exclude from logging (health checks, docs, etc.)
    EXCLUDED_PATHS = {
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
    }
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process request and log timing information.
        
        Args:
            request: Incoming request
            call_next: Next middleware/route handler
            
        Returns:
            Response from the route handler
        """
        # Skip logging for excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        # Start timing
        start_time = time.perf_counter()
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        # Extract user ID from request state if available
        user_id = getattr(request.state, "user_id", None)
        
        # Log the request
        log_api_request(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            user_id=user_id,
            client_ip=client_ip,
        )
        
        # Add timing header to response
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Extract client IP from request.
        
        Handles X-Forwarded-For header for proxy setups.
        
        Args:
            request: Incoming request
            
        Returns:
            Client IP address string
        """
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        if request.client:
            return request.client.host
        
        return "unknown"
