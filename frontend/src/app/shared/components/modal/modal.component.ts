/**
 * Modal Dialog Component for FitCoach AI
 *
 * A reusable modal dialog with customizable content.
 */

import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  trigger,
  state,
  style,
  transition,
  animate,
} from '@angular/animations';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule],
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('200ms ease-out', style({ opacity: 1 })),
      ]),
      transition(':leave', [animate('150ms ease-in', style({ opacity: 0 }))]),
    ]),
    trigger('slideUp', [
      transition(':enter', [
        style({ transform: 'translateY(20px) scale(0.95)', opacity: 0 }),
        animate(
          '300ms ease-out',
          style({ transform: 'translateY(0) scale(1)', opacity: 1 })
        ),
      ]),
      transition(':leave', [
        animate(
          '200ms ease-in',
          style({ transform: 'translateY(20px) scale(0.95)', opacity: 0 })
        ),
      ]),
    ]),
  ],
  template: `
    @if (isOpen) {
      <div
        class="fixed inset-0 z-50 overflow-y-auto"
        role="dialog"
        aria-modal="true"
      >
        <!-- Backdrop -->
        <div
          [@fadeIn]
          class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm"
          (click)="onBackdropClick()"
        ></div>

        <!-- Modal container -->
        <div class="flex min-h-full items-center justify-center p-4">
          <div
            [@slideUp]
            class="relative w-full bg-white rounded-2xl shadow-2xl"
            [ngClass]="sizeClasses"
          >
            <!-- Header -->
            @if (title || showCloseButton) {
              <div
                class="flex items-center justify-between px-6 py-4 border-b border-gray-100"
              >
                @if (title) {
                  <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
                }
                @if (showCloseButton) {
                  <button
                    type="button"
                    class="p-2 -mr-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 rounded-lg transition-colors"
                    (click)="close()"
                  >
                    <svg
                      class="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                }
              </div>
            }

            <!-- Content -->
            <div class="px-6 py-4">
              <ng-content></ng-content>
            </div>

            <!-- Footer -->
            @if (showFooter) {
              <div
                class="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-100 bg-gray-50 rounded-b-2xl"
              >
                <ng-content select="[slot=footer]"></ng-content>
              </div>
            }
          </div>
        </div>
      </div>
    }
  `,
})
export class ModalComponent {
  /** Whether modal is open */
  @Input() isOpen = false;

  /** Modal title */
  @Input() title?: string;

  /** Whether to show close button */
  @Input() showCloseButton = true;

  /** Whether to show footer slot */
  @Input() showFooter = true;

  /** Modal size */
  @Input() size: 'sm' | 'md' | 'lg' | 'xl' = 'md';

  /** Close when clicking backdrop */
  @Input() closeOnBackdrop = true;

  /** Event emitted when modal is closed */
  @Output() closed = new EventEmitter<void>();

  close(): void {
    this.isOpen = false;
    this.closed.emit();
  }

  onBackdropClick(): void {
    if (this.closeOnBackdrop) {
      this.close();
    }
  }

  get sizeClasses(): string {
    const sizes: Record<string, string> = {
      sm: 'max-w-sm',
      md: 'max-w-md',
      lg: 'max-w-lg',
      xl: 'max-w-xl',
    };
    return sizes[this.size];
  }
}
