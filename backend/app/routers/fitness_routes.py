from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.profile import Profile
from app.models.goal import Goal
from app.schemas.goal_schema import (
    FitnessCalculationRequest,
    FitnessCalculationResponse,
    WorkoutPlanResponse,
)
from app.services.fitness_calculator import full_calculation
from app.services.workout_generator import generate_workout_plan
from app.services.timeline_estimator import estimate_timeline

router = APIRouter(prefix="/fitness", tags=["Fitness"])


@router.post("/calculate", response_model=FitnessCalculationResponse)
def calculate_fitness(
    payload: FitnessCalculationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complete your profile before calculating fitness plan",
        )

    result = full_calculation(
        weight_kg=profile.weight,
        height_cm=profile.height,
        age=profile.age,
        sex=profile.sex,
        body_fat_pct=profile.body_fat,
        goal_type=payload.goal_type,
        activity_level=payload.activity_level,
    )

    timeline = estimate_timeline(
        current_weight_kg=profile.weight,
        goal_type=payload.goal_type,
        body_fat_pct=profile.body_fat,
    )
    result.update(timeline)

    # Upsert goal record
    goal = db.query(Goal).filter(Goal.user_id == current_user.id).first()
    if goal:
        goal.goal_type = result["goal_type"]
        goal.activity_level = result["activity_level"]
        goal.calorie_target = result["calorie_target"]
        goal.protein = result["protein"]
        goal.carbs = result["carbs"]
        goal.fat = result["fat"]
    else:
        goal = Goal(
            user_id=current_user.id,
            goal_type=result["goal_type"],
            activity_level=result["activity_level"],
            calorie_target=result["calorie_target"],
            protein=result["protein"],
            carbs=result["carbs"],
            fat=result["fat"],
        )
        db.add(goal)

    db.commit()
    return FitnessCalculationResponse(**result)


@router.get("/workout-plan", response_model=WorkoutPlanResponse)
def get_workout_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    goal = db.query(Goal).filter(Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Set your fitness goal first",
        )

    plan = generate_workout_plan(goal.goal_type)
    return WorkoutPlanResponse(**plan)
