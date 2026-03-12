import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FitnessCalculation } from '@shared/models/goal.model';

@Component({
  selector: 'app-calorie-plan',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="max-w-3xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">Calorie Plan</h1>

      <div *ngIf="calc; else noPlan">
        <div class="card mb-6">
          <div class="text-center">
            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">
              Daily Calorie Target
            </p>
            <p class="text-5xl font-extrabold text-primary-600">
              {{ calc.calorie_target | number : '1.0-0' }}
            </p>
            <p class="text-sm text-gray-400 mt-1">kcal / day</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="card text-center">
            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">BMR</p>
            <p class="text-2xl font-bold text-gray-800">
              {{ calc.bmr | number : '1.0-0' }}
            </p>
            <p class="text-xs text-gray-400">kcal</p>
          </div>
          <div class="card text-center">
            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">TDEE</p>
            <p class="text-2xl font-bold text-gray-800">
              {{ calc.tdee | number : '1.0-0' }}
            </p>
            <p class="text-xs text-gray-400">kcal</p>
          </div>
          <div class="card text-center">
            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Goal</p>
            <p class="text-2xl font-bold capitalize text-primary-600">
              {{ calc.goal_type }}
            </p>
          </div>
        </div>

        <div class="card mt-6" *ngIf="calc.timeline_weeks">
          <h2 class="font-bold text-lg mb-2">Goal Timeline</h2>
          <p class="text-sm text-gray-600">
            At your current plan you should reach
            <span class="font-semibold">{{ calc.target_weight }} kg</span>
            in approximately
            <span class="font-semibold">{{ calc.timeline_weeks }} weeks</span>.
          </p>
          <div class="mt-3 h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-primary-500 to-accent-500 rounded-full transition-all duration-500"
              [style.width.%]="timelineProgress"
            ></div>
          </div>
        </div>
      </div>

      <ng-template #noPlan>
        <div class="card text-center py-12 text-gray-500">
          No plan calculated yet. Go to
          <a routerLink="/goals" class="text-primary-600 font-semibold hover:underline">Goals</a>
          to generate your plan.
        </div>
      </ng-template>
    </div>
  `,
})
export class CaloriePlanComponent implements OnInit {
  calc: FitnessCalculation | null = null;
  timelineProgress = 10;

  ngOnInit(): void {
    const cached = localStorage.getItem('fitcoach_calc');
    if (cached) {
      try {
        this.calc = JSON.parse(cached);
        this.timelineProgress = 10; // initial progress
      } catch {
        // ignore
      }
    }
  }
}
