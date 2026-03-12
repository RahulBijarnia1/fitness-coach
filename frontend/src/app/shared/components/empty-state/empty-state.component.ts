/**
 * Empty State Component for FitCoach AI
 *
 * Displays a placeholder when there's no data to show.
 */

import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-empty-state',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
      <!-- Icon -->
      <div
        class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center mb-6"
      >
        <ng-content select="[slot=icon]"></ng-content>
        @if (!hasIcon) {
          <svg
            class="w-10 h-10 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
            />
          </svg>
        }
      </div>

      <!-- Title -->
      <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ title }}</h3>

      <!-- Description -->
      @if (description) {
        <p class="text-gray-500 max-w-sm mb-6">{{ description }}</p>
      }

      <!-- Action button -->
      @if (actionLabel) {
        <button
          type="button"
          class="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors"
          (click)="actionClick.emit()"
        >
          @if (showActionIcon) {
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
          }
          {{ actionLabel }}
        </button>
      }
    </div>
  `,
})
export class EmptyStateComponent {
  /** Title text */
  @Input({ required: true }) title!: string;

  /** Description text */
  @Input() description?: string;

  /** Action button label */
  @Input() actionLabel?: string;

  /** Show plus icon on action button */
  @Input() showActionIcon = true;

  /** Whether icon slot has content */
  @Input() hasIcon = false;

  /** Emitted when action button is clicked */
  @Output() actionClick = new EventEmitter<void>();
}
