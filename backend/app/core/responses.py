"""
Standardized API response models for FitCoach AI.

Provides consistent response structure across all API endpoints.
"""

from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel
from datetime import datetime

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    Standard API response wrapper.
    
    Attributes:
        success: Whether the request was successful
        message: Human-readable message
        data: Response payload
        timestamp: Response timestamp (ISO 8601)
    """
    success: bool = True
    message: str = "Request successful"
    data: Optional[T] = None
    timestamp: str = datetime.utcnow().isoformat()
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Request successful",
                "data": {},
                "timestamp": "2026-03-12T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response model.
    
    Attributes:
        success: Always False for errors
        message: Error description
        error_code: Machine-readable error code
        details: Additional error details
        timestamp: Error timestamp
    """
    success: bool = False
    message: str
    error_code: str
    details: Optional[Any] = None
    timestamp: str = datetime.utcnow().isoformat()
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Validation failed",
                "error_code": "VALIDATION_ERROR",
                "details": {"field": "email", "error": "Invalid email format"},
                "timestamp": "2026-03-12T10:30:00"
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated response wrapper for list endpoints.
    
    Attributes:
        success: Whether the request was successful
        message: Human-readable message
        data: List of items
        pagination: Pagination metadata
        timestamp: Response timestamp
    """
    success: bool = True
    message: str = "Request successful"
    data: list[T]
    pagination: "PaginationMeta"
    timestamp: str = datetime.utcnow().isoformat()


class PaginationMeta(BaseModel):
    """
    Pagination metadata.
    """
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "page_size": 20,
                "total_items": 100,
                "total_pages": 5,
                "has_next": True,
                "has_previous": False
            }
        }


def create_response(
    data: Any = None,
    message: str = "Request successful",
    success: bool = True
) -> dict:
    """
    Create a standardized API response.
    
    Args:
        data: Response payload
        message: Human-readable message
        success: Whether the request was successful
        
    Returns:
        Dictionary with standardized response format
    """
    return {
        "success": success,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }


def create_paginated_response(
    data: list,
    page: int,
    page_size: int,
    total_items: int,
    message: str = "Request successful"
) -> dict:
    """
    Create a standardized paginated API response.
    
    Args:
        data: List of items
        page: Current page number
        page_size: Items per page
        total_items: Total number of items
        message: Human-readable message
        
    Returns:
        Dictionary with paginated response format
    """
    total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0
    
    return {
        "success": True,
        "message": message,
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        },
        "timestamp": datetime.utcnow().isoformat()
    }
