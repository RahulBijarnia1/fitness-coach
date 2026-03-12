import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { FitnessService } from '../../../core/services/fitness.service';
import { FitnessCalculation } from '@shared/models/goal.model';

@Component({
  selector: 'app-goal-selection',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="max-w-2xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">Set Your Fitness Goal</h1>

      <div
        *ngIf="error"
        class="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600"
      >
        {{ error }}
      </div>

      <form
        [formGroup]="form"
        (ngSubmit)="onSubmit()"
        class="card space-y-6"
      >
        <!-- Goal type -->
        <div>
          <label class="label mb-3">What is your goal?</label>
          <div class="grid grid-cols-3 gap-3">
            <button
              type="button"
              *ngFor="let g of goalTypes"
              (click)="form.get('goal_type')?.setValue(g.value)"
              [class.ring-2]="form.get('goal_type')?.value === g.value"
              [class.ring-primary-500]="form.get('goal_type')?.value === g.value"
              class="card text-center cursor-pointer hover:shadow-md transition"
            >
              <div class="text-3xl mb-1">{{ g.icon }}</div>
              <div class="font-semibold text-sm">{{ g.label }}</div>
            </button>
          </div>
        </div>

        <!-- Activity level -->
        <div>
          <label class="label">Activity Level</label>
          <select formControlName="activity_level" class="input-field">
            <option value="" disabled>Select your activity level</option>
            <option value="sedentary">Sedentary (desk job)</option>
            <option value="light">Light (1-3 days/week)</option>
            <option value="moderate">Moderate (3-5 days/week)</option>
            <option value="active">Active (6-7 days/week)</option>
            <option value="very_active">Very Active (athlete)</option>
          </select>
        </div>

        <button
          type="submit"
          class="btn-primary w-full"
          [disabled]="form.invalid || loading"
        >
          {{ loading ? 'Calculating...' : 'Calculate My Plan' }}
        </button>
      </form>

      <!-- Results preview -->
      <div *ngIf="result" class="mt-8 card">
        <h2 class="text-lg font-bold mb-4 text-gray-900">Your Plan Summary</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <p class="text-xs text-gray-500 uppercase tracking-wider">
              Daily Calories
            </p>
            <p class="text-2xl font-bold text-primary-600">
              {{ result.calorie_target | number : '1.0-0' }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase tracking-wider">
              Protein
            </p>
            <p class="text-2xl font-bold text-accent-600">
              {{ result.protein | number : '1.0-0' }}g
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase tracking-wider">
              Carbs
            </p>
            <p class="text-2xl font-bold text-amber-600">
              {{ result.carbs | number : '1.0-0' }}g
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500 uppercase tracking-wider">Fat</p>
            <p class="text-2xl font-bold text-rose-500">
              {{ result.fat | number : '1.0-0' }}g
            </p>
          </div>
        </div>
        <div class="mt-4 text-center" *ngIf="result.timeline_weeks">
          <p class="text-sm text-gray-500">
            Estimated timeline:
            <span class="font-semibold text-gray-700"
              >{{ result.timeline_weeks }} weeks</span
            >
            to reach
            <span class="font-semibold text-gray-700"
              >{{ result.target_weight }} kg</span
            >
          </p>
        </div>
        <div class="mt-6 flex justify-center">
          <button class="btn-accent" (click)="goToDashboard()">
            Go to Dashboard
          </button>
        </div>
      </div>
    </div>
  `,
})
export class GoalSelectionComponent {
  form: FormGroup;
  loading = false;
  error = '';
  result: FitnessCalculation | null = null;

  goalTypes = [
    { value: 'cut', label: 'Cut', icon: '🔥' },
    { value: 'maintain', label: 'Maintain', icon: '⚖️' },
    { value: 'bulk', label: 'Bulk', icon: '💪' },
  ];

  constructor(
    private fb: FormBuilder,
    private fitnessService: FitnessService,
    private router: Router
  ) {
    this.form = this.fb.group({
      goal_type: ['', Validators.required],
      activity_level: ['', Validators.required],
    });
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';
    this.fitnessService.calculate(this.form.value).subscribe({
      next: (res) => {
        this.loading = false;
        this.result = res;
        localStorage.setItem('fitcoach_calc', JSON.stringify(res));
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.detail || 'Calculation failed. Complete your profile first.';
      },
    });
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
}
