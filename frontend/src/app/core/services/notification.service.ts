/**
 * Notification Service for FitCoach AI
 *
 * Provides toast notifications for user feedback.
 * Uses Angular signals for reactive state management.
 */

import { Injectable, signal, computed } from '@angular/core';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message?: string;
  duration: number;
  dismissible: boolean;
}

interface NotificationConfig {
  title: string;
  message?: string;
  duration?: number;
  dismissible?: boolean;
}

@Injectable({ providedIn: 'root' })
export class NotificationService {
  /** Active notifications queue */
  private notificationsSignal = signal<Notification[]>([]);

  /** Read-only access to notifications */
  notifications = this.notificationsSignal.asReadonly();

  /** Whether there are any active notifications */
  hasNotifications = computed(() => this.notificationsSignal().length > 0);

  /** Default durations by type (milliseconds) */
  private readonly DEFAULT_DURATIONS: Record<NotificationType, number> = {
    success: 3000,
    error: 5000,
    warning: 4000,
    info: 3000,
  };

  /**
   * Show a success notification.
   */
  success(config: NotificationConfig | string): void {
    const cfg = typeof config === 'string' ? { title: config } : config;
    this.show('success', cfg);
  }

  /**
   * Show an error notification.
   */
  error(config: NotificationConfig | string): void {
    const cfg = typeof config === 'string' ? { title: config } : config;
    this.show('error', cfg);
  }

  /**
   * Show a warning notification.
   */
  warning(config: NotificationConfig | string): void {
    const cfg = typeof config === 'string' ? { title: config } : config;
    this.show('warning', cfg);
  }

  /**
   * Show an info notification.
   */
  info(config: NotificationConfig | string): void {
    const cfg = typeof config === 'string' ? { title: config } : config;
    this.show('info', cfg);
  }

  /**
   * Dismiss a specific notification.
   */
  dismiss(id: string): void {
    this.notificationsSignal.update((notifications: Notification[]) =>
      notifications.filter((n: Notification) => n.id !== id)
    );
  }

  /**
   * Dismiss all notifications.
   */
  dismissAll(): void {
    this.notificationsSignal.set([]);
  }

  /**
   * Internal method to show notification.
   */
  private show(type: NotificationType, config: NotificationConfig): void {
    const id = this.generateId();
    const duration = config.duration ?? this.DEFAULT_DURATIONS[type];

    const notification: Notification = {
      id,
      type,
      title: config.title,
      message: config.message,
      duration,
      dismissible: config.dismissible ?? true,
    };

    this.notificationsSignal.update((notifications: Notification[]) => [
      ...notifications,
      notification,
    ]);

    // Auto-dismiss after duration
    if (duration > 0) {
      setTimeout(() => this.dismiss(id), duration);
    }
  }

  /**
   * Generate unique notification ID.
   */
  private generateId(): string {
    return `notification-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
  }
}
