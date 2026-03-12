"""
Analytics API endpoints (v1).

Provides advanced progress analytics, trend analysis, and insights.
"""

from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.progress_analytics import ProgressAnalyticsService
from app.core.responses import create_response
from app.core.logging import logger, log_user_action
from app.middleware.rate_limiter import limiter, READ_LIMIT

router = APIRouter()


@router.get("/dashboard", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_dashboard_analytics(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get comprehensive dashboard analytics.
    
    Returns all analytics data needed for the dashboard in a single call.
    
    Returns:
        Complete analytics data including insights, trends, and recommendations
    """
    analytics_service = ProgressAnalyticsService(db)
    
    analytics = analytics_service.get_comprehensive_analytics(current_user.id)
    
    log_user_action(current_user.id, "view_dashboard_analytics")
    
    return create_response(
        data=analytics,
        message="Dashboard analytics retrieved"
    )


@router.get("/weight-trend", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_weight_trend(
    request: Request,
    days: int = Query(28, ge=7, le=90, description="Days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get weight trend analysis.
    
    Analyzes weight changes over specified period and determines
    trend direction, rate of change, and goal projection.
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Weight trend analysis with direction and projections
    """
    analytics_service = ProgressAnalyticsService(db)
    
    trend = analytics_service.get_weight_trend(current_user.id, days)
    
    if not trend:
        return create_response(
            data=None,
            message="Insufficient data for trend analysis. Log at least 3 entries."
        )
    
    return create_response(
        data={
            "direction": trend.direction,
            "weekly_change_kg": trend.weekly_change,
            "total_change_kg": trend.total_change,
            "consistency_score": trend.consistency_score,
            "projected_weeks_to_goal": trend.projected_weeks_to_goal,
            "on_track": trend.on_track,
            "analysis_period_days": days,
        },
        message="Weight trend analysis complete"
    )


@router.get("/body-fat-trend", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_body_fat_trend(
    request: Request,
    days: int = Query(28, ge=7, le=90, description="Days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get body fat percentage trend analysis.
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Body fat trend analysis or null if insufficient data
    """
    analytics_service = ProgressAnalyticsService(db)
    
    trend = analytics_service.get_body_fat_trend(current_user.id, days)
    
    if not trend:
        return create_response(
            data=None,
            message="Insufficient body fat data for analysis"
        )
    
    return create_response(
        data=trend,
        message="Body fat trend analysis complete"
    )


@router.get("/calorie-adherence", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_calorie_adherence(
    request: Request,
    days: int = Query(14, ge=7, le=30, description="Days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Estimate calorie adherence based on weight changes.
    
    Uses weight change rate to estimate how well the user is
    adhering to their calorie targets.
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Calorie adherence estimation with recommendations
    """
    analytics_service = ProgressAnalyticsService(db)
    
    adherence = analytics_service.estimate_calorie_adherence(current_user.id, days)
    
    if not adherence:
        return create_response(
            data=None,
            message="Insufficient data or no goal set for adherence estimation"
        )
    
    return create_response(
        data=adherence,
        message="Calorie adherence estimated"
    )


@router.get("/insights", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_weekly_insights(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get personalized weekly progress insights.
    
    Provides a summary of progress with achievements and recommendations.
    
    Returns:
        Weekly insights with recommendations and achievements
    """
    analytics_service = ProgressAnalyticsService(db)
    
    insights = analytics_service.get_weekly_insights(current_user.id)
    
    if not insights:
        return create_response(
            data={
                "recommendations": [
                    "Complete your profile to get started",
                    "Set your fitness goal",
                    "Log your first weight entry",
                ],
                "achievements": [],
            },
            message="Complete your profile and log progress for insights"
        )
    
    return create_response(
        data={
            "current_weight": insights.current_weight,
            "starting_weight": insights.starting_weight,
            "goal_weight": insights.goal_weight,
            "total_change": insights.weight_change,
            "change_percentage": insights.weight_change_pct,
            "body_fat_change": insights.body_fat_change,
            "weekly_average": insights.weekly_avg_weight,
            "trend": {
                "direction": insights.trend.direction if insights.trend else None,
                "on_track": insights.trend.on_track if insights.trend else None,
            } if insights.trend else None,
            "recommendations": insights.recommendations,
            "achievements": insights.achievements,
        },
        message="Weekly insights generated"
    )


@router.get("/goal-progress", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_goal_progress(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get progress towards fitness goal.
    
    Returns percentage completion and estimated time remaining.
    
    Returns:
        Goal progress with completion percentage
    """
    from app.repositories.goal_repository import GoalRepository
    from app.repositories.progress_repository import ProgressRepository
    from app.repositories.profile_repository import ProfileRepository
    
    goal_repo = GoalRepository(db)
    progress_repo = ProgressRepository(db)
    profile_repo = ProfileRepository(db)
    
    goal = goal_repo.get_by_user_id(current_user.id)
    profile = profile_repo.get_by_user_id(current_user.id)
    latest = progress_repo.get_latest_log(current_user.id)
    
    if not goal or not profile:
        return create_response(
            data=None,
            message="No goal set or profile incomplete"
        )
    
    current_weight = latest.weight_kg if latest else profile.weight_kg
    starting_weight = profile.weight_kg
    target_weight = goal.target_weight or current_weight
    
    # Calculate progress percentage
    if goal.goal_type == "cut":
        total_to_lose = starting_weight - target_weight
        lost_so_far = starting_weight - current_weight
        progress_pct = (lost_so_far / total_to_lose * 100) if total_to_lose > 0 else 0
    elif goal.goal_type == "bulk":
        total_to_gain = target_weight - starting_weight
        gained_so_far = current_weight - starting_weight
        progress_pct = (gained_so_far / total_to_gain * 100) if total_to_gain > 0 else 0
    else:
        # Maintain - base progress on consistency
        progress_pct = 100 if abs(current_weight - starting_weight) < 1 else 50
    
    progress_pct = max(0, min(100, progress_pct))  # Clamp to 0-100
    
    return create_response(
        data={
            "goal_type": goal.goal_type,
            "starting_weight": starting_weight,
            "current_weight": current_weight,
            "target_weight": target_weight,
            "progress_percentage": round(progress_pct, 1),
            "weight_remaining": round(abs(target_weight - current_weight), 2),
            "timeline_weeks": goal.timeline_weeks,
            "calorie_target": goal.calorie_target,
        },
        message="Goal progress calculated"
    )
