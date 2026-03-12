import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FitnessService } from '../../../core/services/fitness.service';
import { WorkoutPlan, WorkoutDay } from '@shared/models/goal.model';

@Component({
  selector: 'app-workout-plan',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="max-w-4xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">Workout Plan</h1>
      <p class="text-gray-500 mb-8" *ngIf="plan">
        Goal:
        <span class="font-semibold capitalize text-primary-600">{{
          plan.goal_type
        }}</span>
      </p>

      <div *ngIf="error" class="card text-center py-12 text-gray-500">
        {{ error }}
      </div>

      <div *ngIf="plan" class="space-y-6">
        <div *ngFor="let day of plan.plan" class="card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-bold text-gray-900">{{ day.day }}</h2>
            <span
              class="text-xs font-semibold uppercase tracking-wider text-primary-600 bg-primary-50 px-3 py-1 rounded-full"
            >
              {{ day.focus }}
            </span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr
                  class="text-left text-gray-400 text-xs uppercase tracking-wider border-b border-gray-100"
                >
                  <th class="pb-2 pr-4">Exercise</th>
                  <th class="pb-2 pr-4">Muscle Group</th>
                  <th class="pb-2 pr-4">Sets</th>
                  <th class="pb-2">Reps</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  *ngFor="let ex of day.exercises"
                  class="border-t border-gray-50 hover:bg-gray-50 transition"
                >
                  <td class="py-2.5 pr-4 font-medium text-gray-900">
                    {{ ex.exercise }}
                  </td>
                  <td class="py-2.5 pr-4 text-gray-500">
                    {{ ex.muscle_group }}
                  </td>
                  <td class="py-2.5 pr-4 font-semibold">{{ ex.sets }}</td>
                  <td class="py-2.5 font-semibold">{{ ex.reps }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  `,
})
export class WorkoutPlanComponent implements OnInit {
  plan: WorkoutPlan | null = null;
  error = '';

  constructor(private fitnessService: FitnessService) {}

  ngOnInit(): void {
    this.fitnessService.getWorkoutPlan().subscribe({
      next: (wp) => (this.plan = wp),
      error: (err) =>
        (this.error =
          err.error?.detail || 'Set your fitness goal first to view workout plan.'),
    });
  }
}
