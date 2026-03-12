"""
Timeline Estimator
------------------
Estimates how many weeks it will take to reach a goal weight.

Assumptions:
  cut:  safe rate ≈ 0.45 kg / week   (500 kcal deficit → ~1 lb / week)
  bulk: lean gain ≈ 0.25 kg / week   (350 kcal surplus)
  maintain: no weight change → None
"""

from typing import Optional

WEEKLY_CHANGE_KG: dict[str, float] = {
    "cut": -0.45,
    "bulk": 0.25,
    "maintain": 0.0,
}


def estimate_timeline(
    current_weight_kg: float,
    goal_type: str,
    body_fat_pct: Optional[float] = None,
) -> dict[str, Optional[int | float]]:
    """Return estimated weeks and target weight."""
    rate = WEEKLY_CHANGE_KG.get(goal_type, 0.0)

    if goal_type == "cut":
        # Target: lose 10 % of current body weight (reasonable cut)
        target_weight = round(current_weight_kg * 0.90, 2)
        weight_to_lose = current_weight_kg - target_weight
        weeks = max(1, round(weight_to_lose / abs(rate)))
        return {"timeline_weeks": weeks, "target_weight": target_weight}

    if goal_type == "bulk":
        # Target: gain 5 % of current body weight
        target_weight = round(current_weight_kg * 1.05, 2)
        weight_to_gain = target_weight - current_weight_kg
        weeks = max(1, round(weight_to_gain / rate))
        return {"timeline_weeks": weeks, "target_weight": target_weight}

    # maintain
    return {"timeline_weeks": None, "target_weight": None}
