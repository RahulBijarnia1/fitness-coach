"""
Progress tracking API endpoints (v1).

Provides progress logging and history retrieval with pagination.
"""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.progress_schema import ProgressCreate
from app.repositories.progress_repository import ProgressRepository
from app.core.responses import create_response, create_paginated_response
from app.core.logging import logger, log_progress_entry, log_user_action
from app.middleware.rate_limiter import limiter, READ_LIMIT, WRITE_LIMIT

router = APIRouter()


@router.post("/log", response_model=dict)
@limiter.limit(WRITE_LIMIT)
async def log_progress(
    request: Request,
    progress_data: ProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Log a progress entry.
    
    Records weight and optional body fat percentage for tracking.
    
    Args:
        progress_data: Progress entry data
        
    Returns:
        Created progress entry
    """
    progress_repo = ProgressRepository(db)
    
    # Create progress log
    log = progress_repo.create_log(
        user_id=current_user.id,
        weight_kg=progress_data.weight_kg,
        body_fat_pct=progress_data.body_fat_pct,
        log_date=progress_data.log_date or date.today(),
    )
    
    # Log for analytics
    log_progress_entry(current_user.id, log.weight_kg, log.body_fat_pct)
    log_user_action(current_user.id, "log_progress", {"weight": log.weight_kg})
    
    return create_response(
        data={
            "id": log.id,
            "weight_kg": log.weight_kg,
            "body_fat_pct": log.body_fat_pct,
            "log_date": log.log_date.isoformat(),
        },
        message="Progress logged successfully"
    )


@router.get("/history", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_progress_history(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get paginated progress history.
    
    Returns progress logs ordered by date (newest first).
    
    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page (max 100)
        
    Returns:
        Paginated list of progress entries
    """
    progress_repo = ProgressRepository(db)
    
    # Calculate offset
    skip = (page - 1) * page_size
    
    # Get logs and total count
    logs = progress_repo.get_user_logs(current_user.id, skip=skip, limit=page_size)
    total = progress_repo.count_user_logs(current_user.id)
    
    # Format logs
    formatted_logs = [
        {
            "id": log.id,
            "weight_kg": log.weight_kg,
            "body_fat_pct": log.body_fat_pct,
            "log_date": log.log_date.isoformat(),
        }
        for log in logs
    ]
    
    return create_paginated_response(
        data=formatted_logs,
        page=page,
        page_size=page_size,
        total_items=total,
        message="Progress history retrieved"
    )


@router.get("/latest", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_latest_progress(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get most recent progress entry.
    
    Returns:
        Latest progress entry or null
    """
    progress_repo = ProgressRepository(db)
    
    log = progress_repo.get_latest_log(current_user.id)
    
    if not log:
        return create_response(
            data=None,
            message="No progress entries found"
        )
    
    return create_response(
        data={
            "id": log.id,
            "weight_kg": log.weight_kg,
            "body_fat_pct": log.body_fat_pct,
            "log_date": log.log_date.isoformat(),
        },
        message="Latest progress retrieved"
    )


@router.get("/summary", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_progress_summary(
    request: Request,
    days: int = Query(30, ge=7, le=365, description="Days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get progress summary statistics.
    
    Returns summary of progress over specified period.
    
    Args:
        days: Number of days to include in summary
        
    Returns:
        Progress statistics and summary
    """
    progress_repo = ProgressRepository(db)
    
    # Get weekly averages
    weeks = days // 7
    weekly_averages = progress_repo.get_weekly_averages(current_user.id, weeks)
    
    # Get overall stats
    stats = progress_repo.get_weight_stats(current_user.id)
    
    # Get first and latest for total change
    first = progress_repo.get_first_log(current_user.id)
    latest = progress_repo.get_latest_log(current_user.id)
    
    total_change = None
    if first and latest:
        total_change = round(latest.weight_kg - first.weight_kg, 2)
    
    return create_response(
        data={
            "period_days": days,
            "weekly_averages": weekly_averages,
            "statistics": {
                "min_weight": stats["min_weight"],
                "max_weight": stats["max_weight"],
                "avg_weight": stats["avg_weight"],
                "total_change": total_change,
            },
            "latest_entry": {
                "weight_kg": latest.weight_kg,
                "body_fat_pct": latest.body_fat_pct,
                "date": latest.log_date.isoformat(),
            } if latest else None,
        },
        message="Progress summary retrieved"
    )


@router.get("/chart-data", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_chart_data(
    request: Request,
    days: int = Query(90, ge=7, le=365, description="Days of data"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get data formatted for charts.
    
    Returns arrays of dates, weights, and body fat percentages
    suitable for direct use in Chart.js.
    
    Args:
        days: Number of days of data to return
        
    Returns:
        Chart-ready data arrays
    """
    progress_repo = ProgressRepository(db)
    
    logs = progress_repo.get_recent_logs(current_user.id, days)
    
    # Sort by date ascending for charts
    logs.sort(key=lambda x: x.log_date)
    
    dates = [log.log_date.isoformat() for log in logs]
    weights = [log.weight_kg for log in logs]
    body_fats = [log.body_fat_pct for log in logs if log.body_fat_pct]
    body_fat_dates = [
        log.log_date.isoformat()
        for log in logs
        if log.body_fat_pct
    ]
    
    return create_response(
        data={
            "dates": dates,
            "weights": weights,
            "body_fat_data": {
                "dates": body_fat_dates,
                "values": body_fats,
            },
            "total_entries": len(logs),
        },
        message="Chart data retrieved"
    )
