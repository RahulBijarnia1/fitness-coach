/**
 * Progress Ring Component for FitCoach AI
 *
 * Displays a circular progress indicator with percentage.
 */

import { Component, Input, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-progress-ring',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="relative inline-flex items-center justify-center">
      <svg
        class="transform -rotate-90"
        [attr.width]="size"
        [attr.height]="size"
      >
        <!-- Background circle -->
        <circle
          class="text-gray-200"
          stroke="currentColor"
          fill="transparent"
          [attr.stroke-width]="strokeWidth"
          [attr.r]="radius"
          [attr.cx]="center"
          [attr.cy]="center"
        />
        <!-- Progress circle -->
        <circle
          class="transition-all duration-500 ease-out"
          [ngClass]="colorClasses"
          stroke="currentColor"
          fill="transparent"
          stroke-linecap="round"
          [attr.stroke-width]="strokeWidth"
          [attr.stroke-dasharray]="circumference"
          [attr.stroke-dashoffset]="strokeDashoffset"
          [attr.r]="radius"
          [attr.cx]="center"
          [attr.cy]="center"
        />
      </svg>
      <!-- Center content -->
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="text-2xl font-bold" [ngClass]="textColorClasses">
          {{ displayValue }}%
        </span>
        @if (label) {
          <span class="text-xs text-gray-500 mt-1">{{ label }}</span>
        }
      </div>
    </div>
  `,
})
export class ProgressRingComponent {
  /** Progress value (0-100) */
  @Input({ required: true }) value!: number;

  /** Ring size in pixels */
  @Input() size = 120;

  /** Stroke width in pixels */
  @Input() strokeWidth = 8;

  /** Color scheme */
  @Input() color: 'primary' | 'success' | 'warning' | 'danger' = 'primary';

  /** Optional label below percentage */
  @Input() label?: string;

  get radius(): number {
    return (this.size - this.strokeWidth) / 2;
  }

  get center(): number {
    return this.size / 2;
  }

  get circumference(): number {
    return 2 * Math.PI * this.radius;
  }

  get strokeDashoffset(): number {
    const clampedValue = Math.min(100, Math.max(0, this.value));
    return this.circumference - (clampedValue / 100) * this.circumference;
  }

  get displayValue(): number {
    return Math.round(Math.min(100, Math.max(0, this.value)));
  }

  get colorClasses(): string {
    const colors: Record<string, string> = {
      primary: 'text-indigo-500',
      success: 'text-emerald-500',
      warning: 'text-amber-500',
      danger: 'text-red-500',
    };
    return colors[this.color];
  }

  get textColorClasses(): string {
    const colors: Record<string, string> = {
      primary: 'text-indigo-600',
      success: 'text-emerald-600',
      warning: 'text-amber-600',
      danger: 'text-red-600',
    };
    return colors[this.color];
  }
}
