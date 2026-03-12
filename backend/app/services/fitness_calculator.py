"""
Fitness Calculation Engine
--------------------------
Implements:
  - BMR  (Mifflin-St Jeor)
  - Lean Body Mass
  - TDEE
  - Calorie targets (cut / bulk / maintain)
  - Macro distribution
"""

from typing import Optional

# Activity level multipliers for TDEE
ACTIVITY_MULTIPLIERS: dict[str, float] = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

# ------------------------------------------------------------------
# Calorie adjustment from TDEE
#   cut:      -500 kcal  (≈ 0.45 kg / week loss)
#   bulk:     +350 kcal  (lean gain)
#   maintain:    0
# ------------------------------------------------------------------
GOAL_CALORIE_OFFSET: dict[str, int] = {
    "cut": -500,
    "bulk": 350,
    "maintain": 0,
}

# ------------------------------------------------------------------
# Macro distribution (percentage of total calories)
#   cut:      40 % protein · 30 % carbs · 30 % fat
#   bulk:     30 % protein · 45 % carbs · 25 % fat
#   maintain: 30 % protein · 40 % carbs · 30 % fat
# ------------------------------------------------------------------
MACRO_RATIOS: dict[str, dict[str, float]] = {
    "cut":      {"protein": 0.40, "carbs": 0.30, "fat": 0.30},
    "bulk":     {"protein": 0.30, "carbs": 0.45, "fat": 0.25},
    "maintain": {"protein": 0.30, "carbs": 0.40, "fat": 0.30},
}

# Calories per gram
CAL_PER_GRAM = {"protein": 4, "carbs": 4, "fat": 9}


def calculate_bmr(weight_kg: float, height_cm: float, age: int, sex: str) -> float:
    """Mifflin-St Jeor equation."""
    if sex == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calculate_lean_body_mass(weight_kg: float, body_fat_pct: Optional[float]) -> Optional[float]:
    """LBM = weight × (1 – body_fat / 100)."""
    if body_fat_pct is None:
        return None
    return round(weight_kg * (1 - body_fat_pct / 100), 2)


def calculate_tdee(bmr: float, activity_level: str) -> float:
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    return round(bmr * multiplier, 2)


def calculate_calorie_target(tdee: float, goal_type: str) -> float:
    offset = GOAL_CALORIE_OFFSET.get(goal_type, 0)
    target = tdee + offset
    # Never go below 1200 kcal for safety
    return round(max(target, 1200), 2)


def calculate_macros(calorie_target: float, goal_type: str) -> dict[str, float]:
    ratios = MACRO_RATIOS.get(goal_type, MACRO_RATIOS["maintain"])
    return {
        "protein": round(calorie_target * ratios["protein"] / CAL_PER_GRAM["protein"], 1),
        "carbs": round(calorie_target * ratios["carbs"] / CAL_PER_GRAM["carbs"], 1),
        "fat": round(calorie_target * ratios["fat"] / CAL_PER_GRAM["fat"], 1),
    }


def full_calculation(
    weight_kg: float,
    height_cm: float,
    age: int,
    sex: str,
    body_fat_pct: Optional[float],
    goal_type: str,
    activity_level: str,
) -> dict:
    bmr = calculate_bmr(weight_kg, height_cm, age, sex)
    lbm = calculate_lean_body_mass(weight_kg, body_fat_pct)
    tdee = calculate_tdee(bmr, activity_level)
    cal_target = calculate_calorie_target(tdee, goal_type)
    macros = calculate_macros(cal_target, goal_type)

    return {
        "bmr": round(bmr, 2),
        "tdee": tdee,
        "lean_body_mass": lbm,
        "calorie_target": cal_target,
        "protein": macros["protein"],
        "carbs": macros["carbs"],
        "fat": macros["fat"],
        "goal_type": goal_type,
        "activity_level": activity_level,
    }
