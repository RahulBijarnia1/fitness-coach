/**
 * Loading Spinner Component for FitCoach AI
 *
 * Displays a full-screen or inline loading spinner.
 */

import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loading-spinner',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (fullScreen) {
      <div
        class="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-50 flex items-center justify-center"
      >
        <div class="bg-white rounded-2xl p-8 shadow-2xl flex flex-col items-center gap-4">
          <div class="spinner" [ngClass]="sizeClasses"></div>
          @if (message) {
            <p class="text-gray-600 font-medium">{{ message }}</p>
          }
        </div>
      </div>
    } @else {
      <div class="flex items-center justify-center gap-3" [ngClass]="containerClasses">
        <div class="spinner" [ngClass]="sizeClasses"></div>
        @if (message) {
          <span class="text-gray-600">{{ message }}</span>
        }
      </div>
    }
  `,
  styles: `
    .spinner {
      border-radius: 50%;
      border-style: solid;
      border-color: #e5e7eb;
      border-top-color: #6366f1;
      animation: spin 0.8s linear infinite;
    }

    .spinner-sm {
      width: 1.25rem;
      height: 1.25rem;
      border-width: 2px;
    }

    .spinner-md {
      width: 2rem;
      height: 2rem;
      border-width: 3px;
    }

    .spinner-lg {
      width: 3rem;
      height: 3rem;
      border-width: 4px;
    }

    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }
  `,
})
export class LoadingSpinnerComponent {
  /** Show as full-screen overlay */
  @Input() fullScreen = false;

  /** Loading message to display */
  @Input() message?: string;

  /** Spinner size: 'sm', 'md', 'lg' */
  @Input() size: 'sm' | 'md' | 'lg' = 'md';

  /** Additional container classes */
  @Input() containerClasses = '';

  get sizeClasses(): string {
    return `spinner-${this.size}`;
  }
}
