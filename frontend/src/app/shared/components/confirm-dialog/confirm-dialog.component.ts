/**
 * Confirm Dialog Component for FitCoach AI
 *
 * A confirmation dialog with customizable actions.
 */

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ModalComponent } from '../modal/modal.component';

export type ConfirmDialogType = 'danger' | 'warning' | 'info';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [CommonModule, ModalComponent],
  template: `
    <app-modal
      [isOpen]="isOpen"
      [title]="title"
      [showCloseButton]="false"
      [closeOnBackdrop]="false"
      size="sm"
      (closed)="onCancel()"
    >
      <div class="flex flex-col items-center text-center py-2">
        <!-- Icon -->
        <div
          class="w-16 h-16 rounded-full flex items-center justify-center mb-4"
          [ngClass]="iconBgClasses"
        >
          <svg
            class="w-8 h-8"
            [ngClass]="iconClasses"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            @if (type === 'danger') {
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            } @else if (type === 'warning') {
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            } @else {
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            }
          </svg>
        </div>

        <!-- Message -->
        <p class="text-gray-600 mb-6">{{ message }}</p>
      </div>

      <!-- Actions -->
      <ng-container slot="footer">
        <button
          type="button"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          (click)="onCancel()"
        >
          {{ cancelText }}
        </button>
        <button
          type="button"
          class="px-4 py-2 text-sm font-medium text-white rounded-lg transition-colors"
          [ngClass]="confirmButtonClasses"
          (click)="onConfirm()"
        >
          {{ confirmText }}
        </button>
      </ng-container>
    </app-modal>
  `,
})
export class ConfirmDialogComponent {
  /** Whether dialog is open */
  @Input() isOpen = false;

  /** Dialog title */
  @Input() title = 'Confirm Action';

  /** Dialog message */
  @Input() message = 'Are you sure you want to proceed?';

  /** Dialog type affects styling */
  @Input() type: ConfirmDialogType = 'warning';

  /** Confirm button text */
  @Input() confirmText = 'Confirm';

  /** Cancel button text */
  @Input() cancelText = 'Cancel';

  /** Emitted when confirmed */
  @Output() confirmed = new EventEmitter<void>();

  /** Emitted when cancelled */
  @Output() cancelled = new EventEmitter<void>();

  onConfirm(): void {
    this.isOpen = false;
    this.confirmed.emit();
  }

  onCancel(): void {
    this.isOpen = false;
    this.cancelled.emit();
  }

  get iconBgClasses(): string {
    const classes: Record<ConfirmDialogType, string> = {
      danger: 'bg-red-100',
      warning: 'bg-amber-100',
      info: 'bg-blue-100',
    };
    return classes[this.type];
  }

  get iconClasses(): string {
    const classes: Record<ConfirmDialogType, string> = {
      danger: 'text-red-600',
      warning: 'text-amber-600',
      info: 'text-blue-600',
    };
    return classes[this.type];
  }

  get confirmButtonClasses(): string {
    const classes: Record<ConfirmDialogType, string> = {
      danger: 'bg-red-600 hover:bg-red-700',
      warning: 'bg-amber-600 hover:bg-amber-700',
      info: 'bg-blue-600 hover:bg-blue-700',
    };
    return classes[this.type];
  }
}
