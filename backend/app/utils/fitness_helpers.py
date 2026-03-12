"""
Fitness calculation utilities and helper functions.

Provides reusable calculations for:
- BMR (Basal Metabolic Rate)
- TDEE (Total Daily Energy Expenditure)
- Macro distribution
- Body composition metrics
- Goal projections
"""

from typing import Optional, Tuple, Dict, Any
from enum import Enum
from dataclasses import dataclass
import math


class GoalType(str, Enum):
    """Fitness goal types."""
    CUT = "cut"
    BULK = "bulk"
    MAINTAIN = "maintain"


class ActivityLevel(str, Enum):
    """Activity level multipliers for TDEE calculation."""
    SEDENTARY = "sedentary"          # Little/no exercise
    LIGHT = "light"                   # Light exercise 1-3 days/week
    MODERATE = "moderate"             # Moderate exercise 3-5 days/week
    ACTIVE = "active"                 # Hard exercise 6-7 days/week
    VERY_ACTIVE = "very_active"       # Very hard exercise + physical job


# Activity level TDEE multipliers
ACTIVITY_MULTIPLIERS = {
    ActivityLevel.SEDENTARY: 1.2,
    ActivityLevel.LIGHT: 1.375,
    ActivityLevel.MODERATE: 1.55,
    ActivityLevel.ACTIVE: 1.725,
    ActivityLevel.VERY_ACTIVE: 1.9,
}

# Goal calorie adjustments
GOAL_CALORIE_OFFSETS = {
    GoalType.CUT: -500,      # 500 calorie deficit for ~0.45kg/week loss
    GoalType.BULK: 350,      # 350 calorie surplus for lean gains
    GoalType.MAINTAIN: 0,    # No adjustment
}

# Macro ratios by goal type (protein, carbs, fat)
MACRO_RATIOS = {
    GoalType.CUT: (0.40, 0.30, 0.30),     # Higher protein for muscle preservation
    GoalType.BULK: (0.30, 0.45, 0.25),    # Higher carbs for energy
    GoalType.MAINTAIN: (0.30, 0.40, 0.30), # Balanced approach
}


@dataclass
class MacroBreakdown:
    """Macro nutrient breakdown."""
    protein_g: int
    carbs_g: int
    fat_g: int
    protein_cal: int
    carbs_cal: int
    fat_cal: int
    protein_pct: float
    carbs_pct: float
    fat_pct: float


@dataclass
class FitnessMetrics:
    """Complete fitness calculation results."""
    bmr: int
    tdee: int
    calorie_target: int
    macros: MacroBreakdown
    lean_body_mass: Optional[float]
    fat_mass: Optional[float]
    timeline_weeks: Optional[int]
    target_weight: Optional[float]
    daily_deficit_surplus: int


def calculate_bmr_mifflin(
    weight_kg: float,
    height_cm: float,
    age: int,
    sex: str,
) -> int:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.
    
    This is considered the most accurate BMR formula for most people.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        sex: Sex ('M' or 'F')
        
    Returns:
        BMR in calories per day
        
    Formula:
        Male: (10 × weight) + (6.25 × height) - (5 × age) + 5
        Female: (10 × weight) + (6.25 × height) - (5 × age) - 161
    """
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    
    if sex.upper() == "M":
        bmr += 5
    else:
        bmr -= 161
    
    return round(bmr)


def calculate_bmr_katch_mcardle(
    weight_kg: float,
    body_fat_pct: float,
) -> int:
    """
    Calculate BMR using Katch-McArdle equation (more accurate with body fat data).
    
    Args:
        weight_kg: Weight in kilograms
        body_fat_pct: Body fat percentage
        
    Returns:
        BMR in calories per day
        
    Formula:
        BMR = 370 + (21.6 × lean body mass in kg)
    """
    lean_mass = weight_kg * (1 - body_fat_pct / 100)
    bmr = 370 + (21.6 * lean_mass)
    return round(bmr)


def calculate_tdee(bmr: int, activity_level: str) -> int:
    """
    Calculate Total Daily Energy Expenditure.
    
    Args:
        bmr: Basal Metabolic Rate
        activity_level: Activity level string
        
    Returns:
        TDEE in calories per day
    """
    try:
        multiplier = ACTIVITY_MULTIPLIERS[ActivityLevel(activity_level)]
    except (ValueError, KeyError):
        multiplier = ACTIVITY_MULTIPLIERS[ActivityLevel.MODERATE]
    
    return round(bmr * multiplier)


def calculate_macros(
    calories: int,
    goal_type: str,
    weight_kg: float = None,
) -> MacroBreakdown:
    """
    Calculate macro nutrient breakdown.
    
    Args:
        calories: Daily calorie target
        goal_type: Type of fitness goal
        weight_kg: Weight in kg (for protein calculation)
        
    Returns:
        MacroBreakdown with grams and percentages
        
    Notes:
        - Protein: 4 calories per gram
        - Carbs: 4 calories per gram
        - Fat: 9 calories per gram
    """
    CAL_PER_G_PROTEIN = 4
    CAL_PER_G_CARBS = 4
    CAL_PER_G_FAT = 9
    
    try:
        protein_ratio, carb_ratio, fat_ratio = MACRO_RATIOS[GoalType(goal_type)]
    except (ValueError, KeyError):
        protein_ratio, carb_ratio, fat_ratio = MACRO_RATIOS[GoalType.MAINTAIN]
    
    # Calculate calories from each macro
    protein_cal = round(calories * protein_ratio)
    carbs_cal = round(calories * carb_ratio)
    fat_cal = round(calories * fat_ratio)
    
    # Convert to grams
    protein_g = round(protein_cal / CAL_PER_G_PROTEIN)
    carbs_g = round(carbs_cal / CAL_PER_G_CARBS)
    fat_g = round(fat_cal / CAL_PER_G_FAT)
    
    # If we have weight, ensure minimum protein intake (1.6g/kg for active people)
    if weight_kg and goal_type in ["cut", "bulk"]:
        min_protein = round(weight_kg * 1.6)
        if protein_g < min_protein:
            extra_protein_g = min_protein - protein_g
            extra_protein_cal = extra_protein_g * CAL_PER_G_PROTEIN
            protein_g = min_protein
            protein_cal = protein_g * CAL_PER_G_PROTEIN
            # Reduce carbs to compensate
            carbs_cal -= extra_protein_cal
            carbs_g = round(carbs_cal / CAL_PER_G_CARBS)
    
    return MacroBreakdown(
        protein_g=protein_g,
        carbs_g=carbs_g,
        fat_g=fat_g,
        protein_cal=protein_cal,
        carbs_cal=carbs_cal,
        fat_cal=fat_cal,
        protein_pct=round(protein_ratio * 100, 1),
        carbs_pct=round(carb_ratio * 100, 1),
        fat_pct=round(fat_ratio * 100, 1),
    )


def calculate_body_composition(
    weight_kg: float,
    body_fat_pct: Optional[float],
) -> Tuple[Optional[float], Optional[float]]:
    """
    Calculate lean body mass and fat mass.
    
    Args:
        weight_kg: Total weight in kilograms
        body_fat_pct: Body fat percentage
        
    Returns:
        Tuple of (lean_mass_kg, fat_mass_kg) or (None, None)
    """
    if body_fat_pct is None:
        return None, None
    
    fat_mass = weight_kg * (body_fat_pct / 100)
    lean_mass = weight_kg - fat_mass
    
    return round(lean_mass, 2), round(fat_mass, 2)


def estimate_timeline(
    current_weight: float,
    goal_type: str,
    body_fat_pct: Optional[float] = None,
) -> Tuple[Optional[int], Optional[float]]:
    """
    Estimate timeline to reach fitness goal.
    
    Args:
        current_weight: Current weight in kg
        goal_type: Type of fitness goal
        body_fat_pct: Current body fat percentage
        
    Returns:
        Tuple of (weeks, target_weight) or (None, None)
        
    Assumptions:
        - Cut: 0.45 kg/week loss, target 10% weight reduction
        - Bulk: 0.25 kg/week gain, target 5% weight gain
        - Maintain: No change
    """
    if goal_type == "cut":
        target_weight = current_weight * 0.90  # 10% reduction
        weekly_change = 0.45
        total_change = current_weight - target_weight
        weeks = math.ceil(total_change / weekly_change)
        return weeks, round(target_weight, 2)
    
    elif goal_type == "bulk":
        target_weight = current_weight * 1.05  # 5% gain
        weekly_change = 0.25
        total_change = target_weight - current_weight
        weeks = math.ceil(total_change / weekly_change)
        return weeks, round(target_weight, 2)
    
    else:  # maintain
        return None, current_weight


def calculate_ideal_weight_range(
    height_cm: float,
    sex: str,
) -> Tuple[float, float]:
    """
    Calculate ideal weight range using BMI formula.
    
    Args:
        height_cm: Height in centimeters
        sex: Sex ('M' or 'F')
        
    Returns:
        Tuple of (min_weight_kg, max_weight_kg)
    """
    height_m = height_cm / 100
    
    # Healthy BMI range: 18.5 - 24.9
    min_bmi = 18.5
    max_bmi = 24.9
    
    min_weight = min_bmi * (height_m ** 2)
    max_weight = max_bmi * (height_m ** 2)
    
    return round(min_weight, 1), round(max_weight, 1)


def calculate_water_intake(weight_kg: float, activity_level: str) -> float:
    """
    Calculate recommended daily water intake.
    
    Args:
        weight_kg: Weight in kilograms
        activity_level: Activity level
        
    Returns:
        Recommended water intake in liters
    """
    # Base: 30-35ml per kg of body weight
    base_ml = weight_kg * 33
    
    # Adjust for activity level
    activity_adjustments = {
        "sedentary": 0,
        "light": 0.3,
        "moderate": 0.5,
        "active": 0.75,
        "very_active": 1.0,
    }
    
    adjustment = activity_adjustments.get(activity_level, 0.5)
    total_liters = (base_ml / 1000) + adjustment
    
    return round(total_liters, 1)


def get_full_fitness_calculation(
    weight_kg: float,
    height_cm: float,
    age: int,
    sex: str,
    activity_level: str,
    goal_type: str,
    body_fat_pct: Optional[float] = None,
) -> FitnessMetrics:
    """
    Perform complete fitness calculation.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        sex: Sex ('M' or 'F')
        activity_level: Activity level
        goal_type: Fitness goal type
        body_fat_pct: Body fat percentage (optional)
        
    Returns:
        Complete FitnessMetrics with all calculations
    """
    # Calculate BMR (use Katch-McArdle if body fat is available)
    if body_fat_pct:
        bmr = calculate_bmr_katch_mcardle(weight_kg, body_fat_pct)
    else:
        bmr = calculate_bmr_mifflin(weight_kg, height_cm, age, sex)
    
    # Calculate TDEE
    tdee = calculate_tdee(bmr, activity_level)
    
    # Get calorie offset for goal
    try:
        offset = GOAL_CALORIE_OFFSETS[GoalType(goal_type)]
    except (ValueError, KeyError):
        offset = 0
    
    calorie_target = tdee + offset
    
    # Calculate macros
    macros = calculate_macros(calorie_target, goal_type, weight_kg)
    
    # Calculate body composition
    lean_mass, fat_mass = calculate_body_composition(weight_kg, body_fat_pct)
    
    # Estimate timeline
    timeline_weeks, target_weight = estimate_timeline(weight_kg, goal_type, body_fat_pct)
    
    return FitnessMetrics(
        bmr=bmr,
        tdee=tdee,
        calorie_target=calorie_target,
        macros=macros,
        lean_body_mass=lean_mass,
        fat_mass=fat_mass,
        timeline_weeks=timeline_weeks,
        target_weight=target_weight,
        daily_deficit_surplus=offset,
    )
