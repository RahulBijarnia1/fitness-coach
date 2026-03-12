/**
 * Stat Card Component for FitCoach AI
 *
 * Displays a statistic with label, value, and optional trend indicator.
 * Perfect for dashboard metrics.
 */

import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export type TrendDirection = 'up' | 'down' | 'neutral';
export type CardColorScheme =
  | 'primary'
  | 'success'
  | 'warning'
  | 'danger'
  | 'info'
  | 'purple';

@Component({
  selector: 'app-stat-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div
      class="stat-card relative overflow-hidden rounded-xl p-6 transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
      [ngClass]="cardClasses"
    >
      <!-- Background decoration -->
      <div
        class="absolute -right-4 -top-4 w-24 h-24 rounded-full opacity-10"
        [ngClass]="decorationClasses"
      ></div>

      <!-- Icon -->
      @if (icon) {
        <div
          class="w-12 h-12 rounded-lg flex items-center justify-center mb-4"
          [ngClass]="iconBgClasses"
        >
          <ng-content select="[slot=icon]"></ng-content>
        </div>
      }

      <!-- Label -->
      <p class="text-sm font-medium opacity-80 mb-1">{{ label }}</p>

      <!-- Value -->
      <div class="flex items-baseline gap-2">
        <p class="text-3xl font-bold tracking-tight">{{ value }}</p>
        @if (unit) {
          <span class="text-sm font-medium opacity-70">{{ unit }}</span>
        }
      </div>

      <!-- Trend -->
      @if (trend !== undefined && trendLabel) {
        <div class="flex items-center gap-1 mt-3">
          <span
            class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
            [ngClass]="trendClasses"
          >
            @if (trend === 'up') {
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
            } @else if (trend === 'down') {
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
            } @else {
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z"
                  clip-rule="evenodd"
                />
              </svg>
            }
            {{ trendLabel }}
          </span>
          @if (trendDescription) {
            <span class="text-xs opacity-60">{{ trendDescription }}</span>
          }
        </div>
      }

      <!-- Subtitle / Description -->
      @if (description) {
        <p class="text-sm opacity-70 mt-2">{{ description }}</p>
      }
    </div>
  `,
  styles: `
    .stat-card {
      backdrop-filter: blur(8px);
    }
  `,
})
export class StatCardComponent {
  /** Card label/title */
  @Input({ required: true }) label!: string;

  /** Main value to display */
  @Input({ required: true }) value!: string | number;

  /** Unit suffix (e.g., 'kg', 'cal', '%') */
  @Input() unit?: string;

  /** Color scheme */
  @Input() colorScheme: CardColorScheme = 'primary';

  /** Show icon slot */
  @Input() icon = false;

  /** Trend direction */
  @Input() trend?: TrendDirection;

  /** Trend label (e.g., '+2.5%') */
  @Input() trendLabel?: string;

  /** Trend description (e.g., 'vs last week') */
  @Input() trendDescription?: string;

  /** Whether trend up is positive (true) or negative (false) */
  @Input() trendUpPositive = true;

  /** Additional description text */
  @Input() description?: string;

  get cardClasses(): string {
    const schemes: Record<CardColorScheme, string> = {
      primary: 'bg-gradient-to-br from-indigo-500 to-indigo-600 text-white',
      success: 'bg-gradient-to-br from-emerald-500 to-emerald-600 text-white',
      warning: 'bg-gradient-to-br from-amber-500 to-amber-600 text-white',
      danger: 'bg-gradient-to-br from-red-500 to-red-600 text-white',
      info: 'bg-gradient-to-br from-sky-500 to-sky-600 text-white',
      purple: 'bg-gradient-to-br from-purple-500 to-purple-600 text-white',
    };
    return schemes[this.colorScheme];
  }

  get decorationClasses(): string {
    return 'bg-white';
  }

  get iconBgClasses(): string {
    return 'bg-white/20';
  }

  get trendClasses(): string {
    if (this.trend === 'neutral') {
      return 'bg-white/20 text-white';
    }

    const isPositive =
      (this.trend === 'up' && this.trendUpPositive) ||
      (this.trend === 'down' && !this.trendUpPositive);

    return isPositive
      ? 'bg-green-400/30 text-green-100'
      : 'bg-red-400/30 text-red-100';
  }
}
