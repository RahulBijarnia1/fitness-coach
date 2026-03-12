/**
 * Macro Card Component for FitCoach AI
 *
 * Displays macro nutrient information in an attractive card format.
 */

import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface MacroData {
  protein: { grams: number; calories: number; percentage: number };
  carbs: { grams: number; calories: number; percentage: number };
  fat: { grams: number; calories: number; percentage: number };
}

@Component({
  selector: 'app-macro-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">
        {{ title }}
      </h3>

      <!-- Total Calories -->
      <div class="text-center mb-6 pb-6 border-b border-gray-100">
        <p class="text-sm text-gray-500 mb-1">Total Daily Calories</p>
        <p class="text-4xl font-bold text-indigo-600">{{ totalCalories }}</p>
        <p class="text-sm text-gray-400">kcal</p>
      </div>

      <!-- Macro Bars -->
      <div class="space-y-4">
        <!-- Protein -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-sm font-medium text-gray-700">Protein</span>
            <span class="text-sm text-gray-500">
              {{ macros.protein.grams }}g ({{ macros.protein.percentage }}%)
            </span>
          </div>
          <div class="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full transition-all duration-500"
              [style.width.%]="macros.protein.percentage"
            ></div>
          </div>
          <p class="text-xs text-gray-400 mt-1">
            {{ macros.protein.calories }} calories
          </p>
        </div>

        <!-- Carbs -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-sm font-medium text-gray-700">Carbohydrates</span>
            <span class="text-sm text-gray-500">
              {{ macros.carbs.grams }}g ({{ macros.carbs.percentage }}%)
            </span>
          </div>
          <div class="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-amber-500 to-amber-600 rounded-full transition-all duration-500"
              [style.width.%]="macros.carbs.percentage"
            ></div>
          </div>
          <p class="text-xs text-gray-400 mt-1">
            {{ macros.carbs.calories }} calories
          </p>
        </div>

        <!-- Fat -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-sm font-medium text-gray-700">Fat</span>
            <span class="text-sm text-gray-500">
              {{ macros.fat.grams }}g ({{ macros.fat.percentage }}%)
            </span>
          </div>
          <div class="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-rose-500 to-rose-600 rounded-full transition-all duration-500"
              [style.width.%]="macros.fat.percentage"
            ></div>
          </div>
          <p class="text-xs text-gray-400 mt-1">
            {{ macros.fat.calories }} calories
          </p>
        </div>
      </div>
    </div>
  `,
})
export class MacroCardComponent {
  /** Card title */
  @Input() title = 'Daily Macros';

  /** Macro nutrients data */
  @Input({ required: true }) macros!: MacroData;

  get totalCalories(): number {
    return (
      this.macros.protein.calories +
      this.macros.carbs.calories +
      this.macros.fat.calories
    );
  }
}
