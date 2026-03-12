"""
User management API endpoints (v1).

Provides user profile and account management.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.profile_schema import ProfileCreate, ProfileUpdate, ProfileResponse
from app.repositories.profile_repository import ProfileRepository
from app.repositories.goal_repository import GoalRepository
from app.core.exceptions import NotFoundException, ConflictException
from app.core.responses import create_response
from app.core.logging import logger, log_user_action
from app.middleware.rate_limiter import limiter, READ_LIMIT, WRITE_LIMIT

router = APIRouter()


@router.get("/me", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_current_user_info(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get current authenticated user information.
    
    Returns user profile and goal status.
    
    Returns:
        User information with profile and goal flags
    """
    profile_repo = ProfileRepository(db)
    goal_repo = GoalRepository(db)
    
    profile = profile_repo.get_by_user_id(current_user.id)
    has_goal = goal_repo.has_goal(current_user.id)
    
    return create_response(
        data={
            "id": current_user.id,
            "email": current_user.email,
            "has_profile": profile is not None,
            "has_goal": has_goal,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        },
        message="User information retrieved"
    )


@router.get("/profile", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_profile(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get user profile.
    
    Returns:
        User profile data or null if not created
    """
    profile_repo = ProfileRepository(db)
    profile = profile_repo.get_by_user_id(current_user.id)
    
    if not profile:
        return create_response(
            data=None,
            message="Profile not yet created"
        )
    
    return create_response(
        data={
            "id": profile.id,
            "age": profile.age,
            "sex": profile.sex,
            "height_cm": profile.height_cm,
            "weight_kg": profile.weight_kg,
            "body_fat_pct": profile.body_fat_pct,
        },
        message="Profile retrieved"
    )


@router.post("/profile", response_model=dict)
@limiter.limit(WRITE_LIMIT)
async def create_profile(
    request: Request,
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create user profile.
    
    Args:
        profile_data: Profile information
        
    Returns:
        Created profile data
        
    Raises:
        ConflictException: If profile already exists
    """
    profile_repo = ProfileRepository(db)
    
    # Check if profile exists
    existing = profile_repo.get_by_user_id(current_user.id)
    if existing:
        raise ConflictException("Profile already exists. Use PUT to update.")
    
    # Create profile
    profile = profile_repo.create_profile(
        user_id=current_user.id,
        age=profile_data.age,
        sex=profile_data.sex,
        height_cm=profile_data.height_cm,
        weight_kg=profile_data.weight_kg,
        body_fat_pct=profile_data.body_fat_pct,
    )
    
    log_user_action(current_user.id, "create_profile", {"weight": profile.weight_kg})
    logger.info(f"Profile created for user {current_user.id}")
    
    return create_response(
        data={
            "id": profile.id,
            "age": profile.age,
            "sex": profile.sex,
            "height_cm": profile.height_cm,
            "weight_kg": profile.weight_kg,
            "body_fat_pct": profile.body_fat_pct,
        },
        message="Profile created successfully"
    )


@router.put("/profile", response_model=dict)
@limiter.limit(WRITE_LIMIT)
async def update_profile(
    request: Request,
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update user profile.
    
    Args:
        profile_data: Updated profile information
        
    Returns:
        Updated profile data
        
    Raises:
        NotFoundException: If profile doesn't exist
    """
    profile_repo = ProfileRepository(db)
    
    profile = profile_repo.get_by_user_id(current_user.id)
    if not profile:
        raise NotFoundException("Profile", current_user.id)
    
    # Update profile
    update_dict = profile_data.model_dump(exclude_unset=True)
    profile = profile_repo.update_profile(profile, **update_dict)
    
    log_user_action(current_user.id, "update_profile", update_dict)
    logger.info(f"Profile updated for user {current_user.id}")
    
    return create_response(
        data={
            "id": profile.id,
            "age": profile.age,
            "sex": profile.sex,
            "height_cm": profile.height_cm,
            "weight_kg": profile.weight_kg,
            "body_fat_pct": profile.body_fat_pct,
        },
        message="Profile updated successfully"
    )


@router.get("/goal", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_goal(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get user's fitness goal.
    
    Returns:
        Current fitness goal or null if not set
    """
    goal_repo = GoalRepository(db)
    goal = goal_repo.get_by_user_id(current_user.id)
    
    if not goal:
        return create_response(
            data=None,
            message="No fitness goal set"
        )
    
    return create_response(
        data={
            "id": goal.id,
            "goal_type": goal.goal_type,
            "activity_level": goal.activity_level,
            "calorie_target": goal.calorie_target,
            "protein_g": goal.protein_g,
            "carbs_g": goal.carbs_g,
            "fat_g": goal.fat_g,
            "timeline_weeks": goal.timeline_weeks,
            "target_weight": goal.target_weight,
        },
        message="Goal retrieved"
    )
