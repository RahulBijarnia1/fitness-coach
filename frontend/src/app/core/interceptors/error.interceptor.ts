/**
 * Error Interceptor for FitCoach AI
 *
 * Handles HTTP errors globally and provides user feedback.
 */

import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { NotificationService } from '../services/notification.service';
import { AuthService } from '../services/auth.service';
import { LoadingService } from '../services/loading.service';

/**
 * Error response structure from API.
 */
interface ApiErrorResponse {
  success: false;
  message: string;
  error_code: string;
  details?: unknown;
}

/**
 * HTTP Error Interceptor.
 *
 * Intercepts all HTTP errors and:
 * - Shows user-friendly error notifications
 * - Handles authentication errors (401)
 * - Handles validation errors (422)
 * - Logs errors for debugging
 */
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const notification = inject(NotificationService);
  const auth = inject(AuthService);
  const router = inject(Router);
  const loading = inject(LoadingService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      // Stop any loading indicators
      loading.stopLoading();

      // Parse error response
      const apiError = error.error as ApiErrorResponse | null;
      const message = apiError?.message || getDefaultMessage(error.status);

      // Handle specific status codes
      switch (error.status) {
        case 0:
          // Network error
          notification.error({
            title: 'Connection Error',
            message: 'Unable to connect to the server. Please check your internet connection.',
          });
          break;

        case 401:
          // Unauthorized - token expired or invalid
          auth.logout();
          router.navigate(['/login']);
          notification.warning({
            title: 'Session Expired',
            message: 'Please log in again to continue.',
          });
          break;

        case 403:
          // Forbidden
          notification.error({
            title: 'Access Denied',
            message: 'You do not have permission to perform this action.',
          });
          break;

        case 404:
          // Not found
          notification.error({
            title: 'Not Found',
            message: message,
          });
          break;

        case 409:
          // Conflict
          notification.warning({
            title: 'Conflict',
            message: message,
          });
          break;

        case 422:
          // Validation error
          handleValidationError(notification, apiError);
          break;

        case 429:
          // Rate limit exceeded
          notification.warning({
            title: 'Too Many Requests',
            message: 'Please wait a moment before trying again.',
          });
          break;

        case 500:
        case 502:
        case 503:
        case 504:
          // Server errors
          notification.error({
            title: 'Server Error',
            message: 'Something went wrong on our end. Please try again later.',
          });
          break;

        default:
          // Generic error
          notification.error({
            title: 'Error',
            message: message,
          });
      }

      // Log error for debugging (in development)
      console.error(`HTTP Error ${error.status}:`, {
        url: req.url,
        method: req.method,
        error: error.error,
      });

      return throwError(() => error);
    })
  );
};

/**
 * Get default error message based on status code.
 */
function getDefaultMessage(status: number): string {
  const messages: Record<number, string> = {
    0: 'Unable to connect to server',
    400: 'Invalid request',
    401: 'Please log in to continue',
    403: 'Access denied',
    404: 'Resource not found',
    409: 'Resource conflict',
    422: 'Validation failed',
    429: 'Too many requests',
    500: 'Internal server error',
    502: 'Bad gateway',
    503: 'Service unavailable',
    504: 'Gateway timeout',
  };
  return messages[status] || 'An unexpected error occurred';
}

/**
 * Handle validation errors with detailed field feedback.
 */
function handleValidationError(
  notification: NotificationService,
  apiError: ApiErrorResponse | null
): void {
  if (!apiError?.details) {
    notification.error({
      title: 'Validation Error',
      message: apiError?.message || 'Please check your input',
    });
    return;
  }

  // If details is an array of field errors
  if (Array.isArray(apiError.details)) {
    const fieldErrors = apiError.details
      .map((err: { field?: string; message?: string }) => 
        `${err.field}: ${err.message}`
      )
      .slice(0, 3) // Show max 3 errors
      .join('\n');

    notification.error({
      title: 'Validation Error',
      message: fieldErrors || apiError.message,
    });
  } else {
    notification.error({
      title: 'Validation Error',
      message: apiError.message,
    });
  }
}
