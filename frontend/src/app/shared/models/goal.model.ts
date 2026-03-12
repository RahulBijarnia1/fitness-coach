export interface Goal {
  id: number;
  user_id: number;
  goal_type: string;
  activity_level: string;
  calorie_target: number | null;
  protein: number | null;
  carbs: number | null;
  fat: number | null;
}

export interface FitnessCalculation {
  bmr: number;
  tdee: number;
  lean_body_mass: number | null;
  calorie_target: number;
  protein: number;
  carbs: number;
  fat: number;
  goal_type: string;
  activity_level: string;
  timeline_weeks: number | null;
  target_weight: number | null;
}

export interface WorkoutExercise {
  exercise: string;
  sets: number;
  reps: string;
  muscle_group: string;
}

export interface WorkoutDay {
  day: string;
  focus: string;
  exercises: WorkoutExercise[];
}

export interface WorkoutPlan {
  goal_type: string;
  plan: WorkoutDay[];
}
