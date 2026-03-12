"""
Fitness calculation and workout API endpoints (v1).

Provides fitness calculations, goal setting, and workout plan generation.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.goal_schema import GoalCreate
from app.repositories.profile_repository import ProfileRepository
from app.repositories.goal_repository import GoalRepository
from app.utils.fitness_helpers import get_full_fitness_calculation, calculate_water_intake
from app.core.exceptions import ProfileRequiredException, ValidationException
from app.core.responses import create_response
from app.core.logging import logger, log_fitness_calculation, log_user_action
from app.middleware.rate_limiter import limiter, READ_LIMIT, WRITE_LIMIT

router = APIRouter()


@router.post("/calculate", response_model=dict)
@limiter.limit(WRITE_LIMIT)
async def calculate_fitness_plan(
    request: Request,
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Calculate comprehensive fitness plan.
    
    Computes BMR, TDEE, macros, and timeline based on user profile
    and selected goal. Creates or updates user's fitness goal.
    
    Args:
        goal_data: Goal type and activity level
        
    Returns:
        Complete fitness calculation with macros and timeline
        
    Raises:
        ProfileRequiredException: If user hasn't created a profile
    """
    profile_repo = ProfileRepository(db)
    goal_repo = GoalRepository(db)
    
    # Get user profile
    profile = profile_repo.get_by_user_id(current_user.id)
    if not profile:
        raise ProfileRequiredException()
    
    # Validate goal type
    valid_goals = ["cut", "bulk", "maintain"]
    if goal_data.goal_type not in valid_goals:
        raise ValidationException(
            f"Invalid goal type. Must be one of: {', '.join(valid_goals)}"
        )
    
    # Use enhanced fitness calculation
    metrics = get_full_fitness_calculation(
        weight_kg=profile.weight_kg,
        height_cm=profile.height_cm,
        age=profile.age,
        sex=profile.sex,
        activity_level=goal_data.activity_level,
        goal_type=goal_data.goal_type,
        body_fat_pct=profile.body_fat_pct,
    )
    
    # Calculate water intake recommendation
    water_liters = calculate_water_intake(profile.weight_kg, goal_data.activity_level)
    
    # Create or update goal
    existing_goal = goal_repo.get_by_user_id(current_user.id)
    
    goal_data_dict = {
        "goal_type": goal_data.goal_type,
        "activity_level": goal_data.activity_level,
        "calorie_target": metrics.calorie_target,
        "protein_g": metrics.macros.protein_g,
        "carbs_g": metrics.macros.carbs_g,
        "fat_g": metrics.macros.fat_g,
        "timeline_weeks": metrics.timeline_weeks,
        "target_weight": metrics.target_weight,
    }
    
    if existing_goal:
        goal = goal_repo.update_goal(existing_goal, **goal_data_dict)
    else:
        goal = goal_repo.create_goal(user_id=current_user.id, **goal_data_dict)
    
    # Log calculation
    log_fitness_calculation(current_user.id, goal_data.goal_type, {
        "calorie_target": metrics.calorie_target,
        "bmr": metrics.bmr,
    })
    log_user_action(current_user.id, "calculate_fitness", {"goal": goal_data.goal_type})
    
    return create_response(
        data={
            "bmr": metrics.bmr,
            "tdee": metrics.tdee,
            "calorie_target": metrics.calorie_target,
            "daily_adjustment": metrics.daily_deficit_surplus,
            "macros": {
                "protein_g": metrics.macros.protein_g,
                "carbs_g": metrics.macros.carbs_g,
                "fat_g": metrics.macros.fat_g,
                "protein_cal": metrics.macros.protein_cal,
                "carbs_cal": metrics.macros.carbs_cal,
                "fat_cal": metrics.macros.fat_cal,
                "protein_pct": metrics.macros.protein_pct,
                "carbs_pct": metrics.macros.carbs_pct,
                "fat_pct": metrics.macros.fat_pct,
            },
            "body_composition": {
                "lean_body_mass": metrics.lean_body_mass,
                "fat_mass": metrics.fat_mass,
            } if metrics.lean_body_mass else None,
            "timeline": {
                "weeks": metrics.timeline_weeks,
                "target_weight": metrics.target_weight,
            } if metrics.timeline_weeks else None,
            "recommendations": {
                "water_liters": water_liters,
                "meals_per_day": 4 if goal_data.goal_type == "bulk" else 3,
            },
            "goal_type": goal_data.goal_type,
            "activity_level": goal_data.activity_level,
        },
        message="Fitness plan calculated successfully"
    )


@router.get("/workout-plan", response_model=dict)
@limiter.limit(READ_LIMIT)
async def get_workout_plan(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get personalized workout plan based on goal.
    
    Returns a structured workout plan with exercises, sets, and reps
    tailored to the user's fitness goal.
    
    Returns:
        Workout plan with daily exercises
        
    Raises:
        ProfileRequiredException: If no goal is set
    """
    goal_repo = GoalRepository(db)
    
    goal = goal_repo.get_by_user_id(current_user.id)
    if not goal:
        from app.core.exceptions import GoalRequiredException
        raise GoalRequiredException()
    
    # Generate workout plan
    plan = WorkoutGenerator.get_plan(goal.goal_type)
    
    log_user_action(current_user.id, "get_workout_plan", {"goal": goal.goal_type})
    
    return create_response(
        data={
            "goal_type": goal.goal_type,
            "plan": plan,
            "tips": _get_workout_tips(goal.goal_type),
        },
        message="Workout plan generated"
    )


@router.get("/calculator/bmr", response_model=dict)
@limiter.limit(READ_LIMIT)
async def calculate_bmr_only(
    request: Request,
    weight: float,
    height: float,
    age: int,
    sex: str,
):
    """
    Calculate BMR without authentication (public endpoint).
    
    Useful for guests to preview calculations.
    
    Args:
        weight: Weight in kg
        height: Height in cm
        age: Age in years
        sex: Sex (M/F)
        
    Returns:
        BMR calculation
    """
    from app.utils.fitness_helpers import calculate_bmr_mifflin
    
    bmr = calculate_bmr_mifflin(weight, height, age, sex)
    
    return create_response(
        data={
            "bmr": bmr,
            "formula": "Mifflin-St Jeor",
            "inputs": {
                "weight_kg": weight,
                "height_cm": height,
                "age": age,
                "sex": sex,
            }
        },
        message="BMR calculated"
    )


def _get_workout_tips(goal_type: str) -> list:
    """Get workout tips based on goal type."""
    tips = {
        "cut": [
            "Keep rest periods short (30-60 seconds) to maintain heart rate",
            "Include cardio 3-4x per week for enhanced fat burning",
            "Focus on compound movements to burn more calories",
            "Maintain intensity even with calorie deficit",
        ],
        "bulk": [
            "Rest 2-3 minutes between heavy sets for full recovery",
            "Progressive overload is key - track your weights",
            "Prioritize compound lifts for maximum muscle stimulus",
            "Get 7-9 hours of sleep for optimal recovery",
        ],
        "maintain": [
            "Focus on consistency and enjoyment",
            "Mix up exercises to prevent boredom",
            "Include mobility work for long-term health",
            "Balance strength and cardio training",
        ],
    }
    return tips.get(goal_type, tips["maintain"])
