/**
 * Loading Service for FitCoach AI
 *
 * Manages global and scoped loading states.
 * Uses Angular signals for reactive state tracking.
 */

import { Injectable, signal, computed } from '@angular/core';

interface LoadingState {
  global: boolean;
  scopes: Map<string, boolean>;
}

@Injectable({ providedIn: 'root' })
export class LoadingService {
  /** Internal loading state */
  private state = signal<LoadingState>({
    global: false,
    scopes: new Map(),
  });

  /** Whether global loading is active */
  isLoading = computed(() => this.state().global);

  /** Whether any loading is active (global or scoped) */
  isAnyLoading = computed(() => {
    const s = this.state();
    return s.global || Array.from(s.scopes.values()).some((v) => v);
  });

  /**
   * Start global loading indicator.
   */
  startLoading(): void {
    this.state.update((s) => ({ ...s, global: true }));
  }

  /**
   * Stop global loading indicator.
   */
  stopLoading(): void {
    this.state.update((s) => ({ ...s, global: false }));
  }

  /**
   * Start loading for a specific scope.
   * Useful for showing loading on specific components.
   *
   * @param scope - Unique scope identifier (e.g., 'dashboard', 'progress')
   */
  startScopedLoading(scope: string): void {
    this.state.update((s) => {
      const scopes = new Map(s.scopes);
      scopes.set(scope, true);
      return { ...s, scopes };
    });
  }

  /**
   * Stop loading for a specific scope.
   *
   * @param scope - Scope identifier to stop
   */
  stopScopedLoading(scope: string): void {
    this.state.update((s) => {
      const scopes = new Map(s.scopes);
      scopes.set(scope, false);
      return { ...s, scopes };
    });
  }

  /**
   * Check if a specific scope is loading.
   *
   * @param scope - Scope identifier to check
   */
  isScopeLoading(scope: string): boolean {
    return this.state().scopes.get(scope) ?? false;
  }

  /**
   * Get loading state for scope as signal.
   *
   * @param scope - Scope identifier
   */
  getScopeLoading(scope: string) {
    return computed(() => this.state().scopes.get(scope) ?? false);
  }

  /**
   * Execute an async operation with automatic loading state.
   *
   * @param operation - Promise-returning function to execute
   * @param scope - Optional scope for scoped loading
   */
  async withLoading<T>(
    operation: () => Promise<T>,
    scope?: string
  ): Promise<T> {
    try {
      if (scope) {
        this.startScopedLoading(scope);
      } else {
        this.startLoading();
      }
      return await operation();
    } finally {
      if (scope) {
        this.stopScopedLoading(scope);
      } else {
        this.stopLoading();
      }
    }
  }
}
