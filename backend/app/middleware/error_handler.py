"""
Global exception handlers for FitCoach AI API.

Converts all exceptions into standardized error responses.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.core.exceptions import FitCoachException
from app.core.logging import logger


def setup_exception_handlers(app: FastAPI):
    """
    Register all exception handlers with the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    
    @app.exception_handler(FitCoachException)
    async def fitcoach_exception_handler(request: Request, exc: FitCoachException):
        """Handle custom FitCoach exceptions."""
        logger.warning(
            f"FitCoach Exception | {exc.error_code} | {exc.message} | "
            f"path={request.url.path}"
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "error_code": exc.error_code,
                "details": exc.details,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors."""
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"],
            })
        
        logger.warning(
            f"Validation Error | path={request.url.path} | errors={errors}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": "Validation failed",
                "error_code": "VALIDATION_ERROR",
                "details": errors,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """Handle database errors."""
        logger.error(
            f"Database Error | path={request.url.path} | error={str(exc)}",
            exc_info=True
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "A database error occurred",
                "error_code": "DATABASE_ERROR",
                "details": None,  # Don't expose DB details in production
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all uncaught exceptions."""
        logger.error(
            f"Unhandled Exception | path={request.url.path} | "
            f"type={type(exc).__name__} | error={str(exc)}",
            exc_info=True
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "An unexpected error occurred",
                "error_code": "INTERNAL_ERROR",
                "details": None,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
