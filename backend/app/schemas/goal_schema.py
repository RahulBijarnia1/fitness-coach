from pydantic import BaseModel, Field
from typing import Optional


class GoalCreate(BaseModel):
    goal_type: str = Field(..., pattern=r"^(cut|bulk|maintain)$")
    activity_level: str = Field(
        ..., pattern=r"^(sedentary|light|moderate|active|very_active)$"
    )


class GoalOut(BaseModel):
    id: int
    user_id: int
    goal_type: str
    activity_level: str
    calorie_target: Optional[float]
    protein: Optional[float]
    carbs: Optional[float]
    fat: Optional[float]

    model_config = {"from_attributes": True}


class FitnessCalculationRequest(BaseModel):
    goal_type: str = Field(..., pattern=r"^(cut|bulk|maintain)$")
    activity_level: str = Field(
        ..., pattern=r"^(sedentary|light|moderate|active|very_active)$"
    )


class FitnessCalculationResponse(BaseModel):
    bmr: float
    tdee: float
    lean_body_mass: Optional[float]
    calorie_target: float
    protein: float
    carbs: float
    fat: float
    goal_type: str
    activity_level: str
    timeline_weeks: Optional[int]
    target_weight: Optional[float]


class WorkoutExercise(BaseModel):
    exercise: str
    sets: int
    reps: str
    muscle_group: str


class WorkoutDay(BaseModel):
    day: str
    focus: str
    exercises: list[WorkoutExercise]


class WorkoutPlanResponse(BaseModel):
    goal_type: str
    plan: list[WorkoutDay]
