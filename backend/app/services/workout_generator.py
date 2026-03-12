"""
Workout Plan Generator
----------------------
Returns a structured weekly workout plan based on goal type.

Plans:
  cut      → 4-day Upper / Lower split  (higher rep, moderate weight)
  bulk     → 5-day Push / Pull / Legs    (progressive overload focus)
  maintain → 3-day Full Body             (balanced)
"""

CUT_PLAN = [
    {
        "day": "Monday",
        "focus": "Upper Body",
        "exercises": [
            {"exercise": "Bench Press", "sets": 4, "reps": "12-15", "muscle_group": "Chest"},
            {"exercise": "Bent-Over Row", "sets": 4, "reps": "12-15", "muscle_group": "Back"},
            {"exercise": "Overhead Press", "sets": 3, "reps": "12-15", "muscle_group": "Shoulders"},
            {"exercise": "Bicep Curl", "sets": 3, "reps": "15", "muscle_group": "Biceps"},
            {"exercise": "Tricep Pushdown", "sets": 3, "reps": "15", "muscle_group": "Triceps"},
        ],
    },
    {
        "day": "Tuesday",
        "focus": "Lower Body",
        "exercises": [
            {"exercise": "Squat", "sets": 4, "reps": "12-15", "muscle_group": "Quads"},
            {"exercise": "Romanian Deadlift", "sets": 4, "reps": "12-15", "muscle_group": "Hamstrings"},
            {"exercise": "Leg Press", "sets": 3, "reps": "15", "muscle_group": "Quads"},
            {"exercise": "Leg Curl", "sets": 3, "reps": "15", "muscle_group": "Hamstrings"},
            {"exercise": "Calf Raise", "sets": 4, "reps": "20", "muscle_group": "Calves"},
        ],
    },
    {
        "day": "Thursday",
        "focus": "Upper Body",
        "exercises": [
            {"exercise": "Incline Dumbbell Press", "sets": 4, "reps": "12-15", "muscle_group": "Chest"},
            {"exercise": "Lat Pulldown", "sets": 4, "reps": "12-15", "muscle_group": "Back"},
            {"exercise": "Lateral Raise", "sets": 3, "reps": "15", "muscle_group": "Shoulders"},
            {"exercise": "Hammer Curl", "sets": 3, "reps": "15", "muscle_group": "Biceps"},
            {"exercise": "Overhead Tricep Extension", "sets": 3, "reps": "15", "muscle_group": "Triceps"},
        ],
    },
    {
        "day": "Friday",
        "focus": "Lower Body",
        "exercises": [
            {"exercise": "Front Squat", "sets": 4, "reps": "12-15", "muscle_group": "Quads"},
            {"exercise": "Hip Thrust", "sets": 4, "reps": "12-15", "muscle_group": "Glutes"},
            {"exercise": "Walking Lunge", "sets": 3, "reps": "12 each leg", "muscle_group": "Quads"},
            {"exercise": "Leg Extension", "sets": 3, "reps": "15", "muscle_group": "Quads"},
            {"exercise": "Seated Calf Raise", "sets": 4, "reps": "20", "muscle_group": "Calves"},
        ],
    },
]

BULK_PLAN = [
    {
        "day": "Monday",
        "focus": "Push (Chest / Shoulders / Triceps)",
        "exercises": [
            {"exercise": "Flat Barbell Bench Press", "sets": 4, "reps": "6-8", "muscle_group": "Chest"},
            {"exercise": "Incline Dumbbell Press", "sets": 4, "reps": "8-10", "muscle_group": "Chest"},
            {"exercise": "Overhead Press", "sets": 4, "reps": "6-8", "muscle_group": "Shoulders"},
            {"exercise": "Lateral Raise", "sets": 3, "reps": "12", "muscle_group": "Shoulders"},
            {"exercise": "Tricep Dips", "sets": 3, "reps": "8-10", "muscle_group": "Triceps"},
            {"exercise": "Skull Crushers", "sets": 3, "reps": "10-12", "muscle_group": "Triceps"},
        ],
    },
    {
        "day": "Tuesday",
        "focus": "Pull (Back / Biceps)",
        "exercises": [
            {"exercise": "Deadlift", "sets": 4, "reps": "5-6", "muscle_group": "Back"},
            {"exercise": "Barbell Row", "sets": 4, "reps": "6-8", "muscle_group": "Back"},
            {"exercise": "Lat Pulldown", "sets": 3, "reps": "8-10", "muscle_group": "Back"},
            {"exercise": "Seated Cable Row", "sets": 3, "reps": "10-12", "muscle_group": "Back"},
            {"exercise": "Barbell Curl", "sets": 3, "reps": "8-10", "muscle_group": "Biceps"},
            {"exercise": "Incline Dumbbell Curl", "sets": 3, "reps": "10-12", "muscle_group": "Biceps"},
        ],
    },
    {
        "day": "Wednesday",
        "focus": "Legs",
        "exercises": [
            {"exercise": "Back Squat", "sets": 4, "reps": "6-8", "muscle_group": "Quads"},
            {"exercise": "Leg Press", "sets": 4, "reps": "8-10", "muscle_group": "Quads"},
            {"exercise": "Romanian Deadlift", "sets": 4, "reps": "8-10", "muscle_group": "Hamstrings"},
            {"exercise": "Leg Curl", "sets": 3, "reps": "10-12", "muscle_group": "Hamstrings"},
            {"exercise": "Leg Extension", "sets": 3, "reps": "12", "muscle_group": "Quads"},
            {"exercise": "Calf Raise", "sets": 4, "reps": "15", "muscle_group": "Calves"},
        ],
    },
    {
        "day": "Thursday",
        "focus": "Push (Volume)",
        "exercises": [
            {"exercise": "Dumbbell Bench Press", "sets": 4, "reps": "8-10", "muscle_group": "Chest"},
            {"exercise": "Cable Fly", "sets": 3, "reps": "12", "muscle_group": "Chest"},
            {"exercise": "Arnold Press", "sets": 4, "reps": "8-10", "muscle_group": "Shoulders"},
            {"exercise": "Front Raise", "sets": 3, "reps": "12", "muscle_group": "Shoulders"},
            {"exercise": "Close-Grip Bench Press", "sets": 3, "reps": "8-10", "muscle_group": "Triceps"},
            {"exercise": "Tricep Pushdown", "sets": 3, "reps": "12", "muscle_group": "Triceps"},
        ],
    },
    {
        "day": "Friday",
        "focus": "Pull (Volume) + Rear Delts",
        "exercises": [
            {"exercise": "Pull-Up", "sets": 4, "reps": "6-8", "muscle_group": "Back"},
            {"exercise": "Dumbbell Row", "sets": 4, "reps": "8-10", "muscle_group": "Back"},
            {"exercise": "Face Pull", "sets": 3, "reps": "15", "muscle_group": "Rear Delts"},
            {"exercise": "Shrug", "sets": 3, "reps": "12", "muscle_group": "Traps"},
            {"exercise": "Hammer Curl", "sets": 3, "reps": "10-12", "muscle_group": "Biceps"},
            {"exercise": "Concentration Curl", "sets": 3, "reps": "12", "muscle_group": "Biceps"},
        ],
    },
]

MAINTAIN_PLAN = [
    {
        "day": "Monday",
        "focus": "Full Body A",
        "exercises": [
            {"exercise": "Squat", "sets": 3, "reps": "8-10", "muscle_group": "Quads"},
            {"exercise": "Bench Press", "sets": 3, "reps": "8-10", "muscle_group": "Chest"},
            {"exercise": "Barbell Row", "sets": 3, "reps": "8-10", "muscle_group": "Back"},
            {"exercise": "Overhead Press", "sets": 3, "reps": "10-12", "muscle_group": "Shoulders"},
            {"exercise": "Plank", "sets": 3, "reps": "45 sec", "muscle_group": "Core"},
        ],
    },
    {
        "day": "Wednesday",
        "focus": "Full Body B",
        "exercises": [
            {"exercise": "Deadlift", "sets": 3, "reps": "6-8", "muscle_group": "Back"},
            {"exercise": "Incline Dumbbell Press", "sets": 3, "reps": "10-12", "muscle_group": "Chest"},
            {"exercise": "Lat Pulldown", "sets": 3, "reps": "10-12", "muscle_group": "Back"},
            {"exercise": "Lateral Raise", "sets": 3, "reps": "12-15", "muscle_group": "Shoulders"},
            {"exercise": "Leg Press", "sets": 3, "reps": "10-12", "muscle_group": "Quads"},
        ],
    },
    {
        "day": "Friday",
        "focus": "Full Body C",
        "exercises": [
            {"exercise": "Front Squat", "sets": 3, "reps": "8-10", "muscle_group": "Quads"},
            {"exercise": "Dumbbell Bench Press", "sets": 3, "reps": "10-12", "muscle_group": "Chest"},
            {"exercise": "Seated Cable Row", "sets": 3, "reps": "10-12", "muscle_group": "Back"},
            {"exercise": "Bicep Curl", "sets": 3, "reps": "12", "muscle_group": "Biceps"},
            {"exercise": "Tricep Pushdown", "sets": 3, "reps": "12", "muscle_group": "Triceps"},
            {"exercise": "Calf Raise", "sets": 3, "reps": "15", "muscle_group": "Calves"},
        ],
    },
]

PLANS: dict[str, list[dict]] = {
    "cut": CUT_PLAN,
    "bulk": BULK_PLAN,
    "maintain": MAINTAIN_PLAN,
}


def generate_workout_plan(goal_type: str) -> dict:
    plan = PLANS.get(goal_type, MAINTAIN_PLAN)
    return {"goal_type": goal_type, "plan": plan}
