/**
 * Analytics Service for FitCoach AI
 *
 * Provides access to progress analytics and insights.
 */

import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, catchError, of } from 'rxjs';
import { environment } from '@env/environment';

export interface WeightTrend {
  direction: 'losing' | 'gaining' | 'stable';
  weekly_change_kg: number;
  total_change_kg: number;
  consistency_score: number;
  projected_weeks_to_goal: number | null;
  on_track: boolean;
}

export interface BodyFatTrend {
  current_body_fat: number;
  starting_body_fat: number;
  total_change: number;
  weekly_change: number;
  direction: 'decreasing' | 'increasing' | 'stable';
  entries_count: number;
}

export interface CalorieAdherence {
  estimated_daily_balance: number;
  target_daily_balance: number;
  adherence_score: number;
  on_target: boolean;
  days_analyzed: number;
  assessment: string;
}

export interface WeeklyAverage {
  week_start: string;
  avg_weight: number;
  avg_body_fat: number | null;
  entries: number;
}

export interface WeightStats {
  min_weight: number | null;
  max_weight: number | null;
  avg_weight: number | null;
  total_change: number | null;
}

export interface Insights {
  current_weight: number | null;
  starting_weight: number | null;
  goal_weight: number | null;
  total_change: number | null;
  change_percentage: number | null;
  recommendations: string[];
  achievements: string[];
}

export interface DashboardAnalytics {
  insights: Insights | null;
  weight_trend: WeightTrend | null;
  body_fat_trend: BodyFatTrend | null;
  calorie_adherence: CalorieAdherence | null;
  weekly_averages: WeeklyAverage[];
  weight_stats: WeightStats;
}

export interface GoalProgress {
  goal_type: string;
  starting_weight: number;
  current_weight: number;
  target_weight: number;
  progress_percentage: number;
  weight_remaining: number;
  timeline_weeks: number | null;
  calorie_target: number;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  timestamp: string;
}

@Injectable({ providedIn: 'root' })
export class AnalyticsService {
  private readonly apiUrl = `${environment.apiUrl}/analytics`;

  /** Cached dashboard analytics */
  private dashboardData = signal<DashboardAnalytics | null>(null);

  /** Goal progress */
  private goalProgressData = signal<GoalProgress | null>(null);

  /** Read-only access to dashboard analytics */
  dashboard = this.dashboardData.asReadonly();

  /** Read-only access to goal progress */
  goalProgress = this.goalProgressData.asReadonly();

  /** Whether data is loaded */
  hasData = computed(() => this.dashboardData() !== null);

  constructor(private http: HttpClient) {}

  /**
   * Fetch comprehensive dashboard analytics.
   * Caches results in signal state.
   */
  fetchDashboardAnalytics(): Observable<ApiResponse<DashboardAnalytics>> {
    return this.http
      .get<ApiResponse<DashboardAnalytics>>(`${this.apiUrl}/dashboard`)
      .pipe(
        tap((res) => {
          if (res.success) {
            this.dashboardData.set(res.data);
          }
        }),
        catchError((err) => {
          console.error('Failed to fetch dashboard analytics', err);
          return of({
            success: false,
            message: 'Failed to load analytics',
            data: null as unknown as DashboardAnalytics,
            timestamp: new Date().toISOString(),
          });
        })
      );
  }

  /**
   * Fetch weight trend analysis.
   */
  fetchWeightTrend(days: number = 28): Observable<ApiResponse<WeightTrend>> {
    return this.http.get<ApiResponse<WeightTrend>>(
      `${this.apiUrl}/weight-trend?days=${days}`
    );
  }

  /**
   * Fetch body fat trend analysis.
   */
  fetchBodyFatTrend(days: number = 28): Observable<ApiResponse<BodyFatTrend>> {
    return this.http.get<ApiResponse<BodyFatTrend>>(
      `${this.apiUrl}/body-fat-trend?days=${days}`
    );
  }

  /**
   * Fetch calorie adherence estimation.
   */
  fetchCalorieAdherence(
    days: number = 14
  ): Observable<ApiResponse<CalorieAdherence>> {
    return this.http.get<ApiResponse<CalorieAdherence>>(
      `${this.apiUrl}/calorie-adherence?days=${days}`
    );
  }

  /**
   * Fetch weekly insights with recommendations.
   */
  fetchInsights(): Observable<ApiResponse<Insights>> {
    return this.http.get<ApiResponse<Insights>>(`${this.apiUrl}/insights`);
  }

  /**
   * Fetch goal progress.
   */
  fetchGoalProgress(): Observable<ApiResponse<GoalProgress>> {
    return this.http
      .get<ApiResponse<GoalProgress>>(`${this.apiUrl}/goal-progress`)
      .pipe(
        tap((res) => {
          if (res.success) {
            this.goalProgressData.set(res.data);
          }
        })
      );
  }

  /**
   * Clear cached analytics data.
   */
  clearCache(): void {
    this.dashboardData.set(null);
    this.goalProgressData.set(null);
  }

  /**
   * Refresh all analytics data.
   */
  refresh(): void {
    this.fetchDashboardAnalytics().subscribe();
    this.fetchGoalProgress().subscribe();
  }
}
