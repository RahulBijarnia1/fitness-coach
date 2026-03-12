/**
 * Professional Dashboard Component for FitCoach AI
 *
 * Displays comprehensive fitness analytics, progress tracking,
 * and personalized recommendations using modern Angular patterns.
 */

import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule, DecimalPipe, DatePipe, PercentPipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { UserService } from '../../core/services/user.service';
import { FitnessService } from '../../core/services/fitness.service';
import { ProgressService } from '../../core/services/progress.service';
import {
  AnalyticsService,
  DashboardAnalytics,
} from '../../core/services/analytics.service';
import { LoadingService } from '../../core/services/loading.service';
import { NotificationService } from '../../core/services/notification.service';
import { Profile } from '@shared/models/user.model';
import { FitnessCalculation, WorkoutPlan, WorkoutDay } from '@shared/models/goal.model';
import { StatCardComponent } from '@shared/components/stat-card/stat-card.component';
import { ProgressRingComponent } from '@shared/components/progress-ring/progress-ring.component';
import { EmptyStateComponent } from '@shared/components/empty-state/empty-state.component';
import { MacroCardComponent } from '@shared/components/macro-card/macro-card.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    StatCardComponent,
    ProgressRingComponent,
    EmptyStateComponent,
    MacroCardComponent,
    DecimalPipe,
    DatePipe,
    PercentPipe,
  ],
  template: `
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-primary-50/30">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Header Section -->
        <div class="mb-8 animate-fade-in">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                Dashboard
              </h1>
              <p class="text-gray-500 mt-1 text-lg" *ngIf="profile()">
                Welcome back, <span class="text-primary-600 font-semibold">{{ profile()?.name }}</span>
              </p>
            </div>
            <div class="flex items-center gap-3" *ngIf="profile()">
              <span class="text-sm text-gray-500">
                {{ currentDate() | date:'EEEE, MMMM d' }}
              </span>
              <button
                (click)="refreshData()"
                class="p-2 rounded-lg bg-white shadow-sm border border-gray-200 hover:bg-gray-50 transition-all duration-200"
                title="Refresh data"
              >
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Onboarding States -->
        <ng-container *ngIf="!isLoading()">
          <!-- No Profile State -->
          <div *ngIf="!profile()" class="animate-fade-in">
            <app-empty-state
              icon="user"
              title="Complete Your Profile"
              message="Set up your profile to get personalized fitness recommendations, calorie targets, and workout plans tailored just for you."
              actionText="Create Profile"
              actionLink="/profile"
            />
          </div>

          <!-- No Goal State -->
          <div *ngIf="profile() && !fitness()" class="animate-fade-in">
            <app-empty-state
              icon="target"
              title="Set Your Fitness Goal"
              message="Choose your goal — lose weight, build muscle, or maintain — and we'll create your personalized nutrition and workout plan."
              actionText="Set Goal"
              actionLink="/goals"
            />
          </div>
        </ng-container>

        <!-- Main Dashboard Content -->
        <ng-container *ngIf="fitness() && !isLoading()">
          <!-- Goal Progress Hero -->
          <div class="mb-8 animate-slide-up">
            <div class="bg-gradient-to-r from-primary-600 via-primary-500 to-accent-500 rounded-2xl p-6 sm:p-8 text-white shadow-xl shadow-primary-500/20">
              <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-2">
                    <span class="px-3 py-1 bg-white/20 rounded-full text-sm font-medium capitalize">
                      {{ fitness()?.goal_type }} Goal
                    </span>
                    <span *ngIf="analytics()?.weight_trend?.on_track"
                      class="px-3 py-1 bg-green-400/30 rounded-full text-sm font-medium flex items-center gap-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                      </svg>
                      On Track
                    </span>
                  </div>
                  <h2 class="text-2xl sm:text-3xl font-bold mb-3">Your Fitness Journey</h2>
                  <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 text-sm">
                    <div>
                      <p class="text-white/70">Current Weight</p>
                      <p class="text-xl font-bold">{{ currentWeight() | number:'1.1-1' }} kg</p>
                    </div>
                    <div *ngIf="fitness()?.target_weight">
                      <p class="text-white/70">Target Weight</p>
                      <p class="text-xl font-bold">{{ fitness()?.target_weight | number:'1.1-1' }} kg</p>
                    </div>
                    <div *ngIf="fitness()?.timeline_weeks">
                      <p class="text-white/70">Est. Timeline</p>
                      <p class="text-xl font-bold">{{ fitness()?.timeline_weeks }} weeks</p>
                    </div>
                  </div>
                </div>
                <div class="flex justify-center lg:justify-end">
                  <app-progress-ring
                    [progress]="goalProgressPercent()"
                    [size]="140"
                    [strokeWidth]="12"
                    color="white"
                    backgroundColor="rgba(255,255,255,0.2)"
                    [showLabel]="true"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Main Stats Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8 animate-slide-up" style="animation-delay: 100ms">
            <app-stat-card
              title="Daily Calories"
              [value]="fitness()?.calorie_target || 0"
              unit="kcal"
              icon="fire"
              gradient="orange"
              [trend]="getCalorieTrend()"
              [trendLabel]="getCalorieTrendLabel()"
            />
            <app-stat-card
              title="Protein Target"
              [value]="fitness()?.protein || 0"
              unit="g"
              icon="protein"
              gradient="blue"
            />
            <app-stat-card
              title="Weekly Change"
              [value]="getWeeklyChange()"
              unit="kg"
              icon="scale"
              gradient="green"
              [trend]="getWeightTrend()"
              [trendLabel]="getWeightTrendLabel()"
            />
            <app-stat-card
              title="Consistency"
              [value]="getConsistencyScore()"
              unit="%"
              icon="chart"
              gradient="purple"
            />
          </div>

          <!-- Two-Column Layout -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <!-- Left Column: Macros + Fitness Details -->
            <div class="lg:col-span-2 space-y-6">
              <!-- Macro Breakdown -->
              <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 animate-slide-up" style="animation-delay: 150ms">
                <div class="flex items-center justify-between mb-6">
                  <h3 class="text-lg font-bold text-gray-900">Daily Macro Breakdown</h3>
                  <a routerLink="/fitness-plan/macros"
                    class="text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1 transition-colors">
                    View Details
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                  </a>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <app-macro-card
                    name="Protein"
                    [amount]="fitness()?.protein || 0"
                    [calories]="(fitness()?.protein || 0) * 4"
                    [percentage]="getProteinPercent()"
                    colorClass="bg-blue-500"
                  />
                  <app-macro-card
                    name="Carbs"
                    [amount]="fitness()?.carbs || 0"
                    [calories]="(fitness()?.carbs || 0) * 4"
                    [percentage]="getCarbsPercent()"
                    colorClass="bg-amber-500"
                  />
                  <app-macro-card
                    name="Fat"
                    [amount]="fitness()?.fat || 0"
                    [calories]="(fitness()?.fat || 0) * 9"
                    [percentage]="getFatPercent()"
                    colorClass="bg-rose-500"
                  />
                </div>
              </div>

              <!-- Fitness Details Card -->
              <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 animate-slide-up" style="animation-delay: 200ms">
                <h3 class="text-lg font-bold text-gray-900 mb-6">Metabolic Profile</h3>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-6">
                  <div class="text-center p-4 bg-gray-50 rounded-xl">
                    <p class="text-2xl font-bold text-gray-900">{{ fitness()?.bmr | number:'1.0-0' }}</p>
                    <p class="text-sm text-gray-500 mt-1">BMR (kcal)</p>
                  </div>
                  <div class="text-center p-4 bg-gray-50 rounded-xl">
                    <p class="text-2xl font-bold text-gray-900">{{ fitness()?.tdee | number:'1.0-0' }}</p>
                    <p class="text-sm text-gray-500 mt-1">TDEE (kcal)</p>
                  </div>
                  <div class="text-center p-4 bg-gray-50 rounded-xl" *ngIf="fitness()?.lean_body_mass">
                    <p class="text-2xl font-bold text-gray-900">{{ fitness()?.lean_body_mass | number:'1.1-1' }}</p>
                    <p class="text-sm text-gray-500 mt-1">LBM (kg)</p>
                  </div>
                  <div class="text-center p-4 bg-primary-50 rounded-xl">
                    <p class="text-2xl font-bold text-primary-600">{{ getDeficitSurplus() | number:'1.0-0' }}</p>
                    <p class="text-sm text-gray-500 mt-1">{{ getDeficitSurplusLabel() }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column: Today's Workout -->
            <div class="space-y-6">
              <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 animate-slide-up" style="animation-delay: 250ms">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-bold text-gray-900">Today's Workout</h3>
                  <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                    {{ getDayName() }}
                  </span>
                </div>
                <div *ngIf="todayWorkout(); else restDay">
                  <div class="flex items-center gap-3 mb-4 pb-4 border-b border-gray-100">
                    <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                      </svg>
                    </div>
                    <div>
                      <p class="font-semibold text-gray-900">{{ todayWorkout()?.focus }}</p>
                      <p class="text-sm text-gray-500">{{ todayWorkout()?.exercises?.length || 0 }} exercises</p>
                    </div>
                  </div>
                  <ul class="space-y-2 max-h-48 overflow-y-auto">
                    <li *ngFor="let ex of todayWorkout()?.exercises; let i = index"
                      class="flex items-center justify-between text-sm py-2 px-3 rounded-lg hover:bg-gray-50 transition-colors">
                      <span class="font-medium text-gray-700">{{ ex.exercise }}</span>
                      <span class="text-gray-500">{{ ex.sets }} × {{ ex.reps }}</span>
                    </li>
                  </ul>
                </div>
                <ng-template #restDay>
                  <div class="text-center py-6">
                    <div class="w-16 h-16 mx-auto mb-3 rounded-full bg-green-100 flex items-center justify-center">
                      <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M5 13l4 4L19 7"/>
                      </svg>
                    </div>
                    <p class="font-semibold text-gray-900">Rest Day</p>
                    <p class="text-sm text-gray-500 mt-1">Take time to recover</p>
                  </div>
                </ng-template>
                <a routerLink="/fitness-plan/workout"
                  class="mt-4 w-full block text-center py-2.5 px-4 bg-primary-50 text-primary-600 rounded-xl font-medium hover:bg-primary-100 transition-colors">
                  View Full Plan
                </a>
              </div>

              <!-- Insights & Recommendations -->
              <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 animate-slide-up" style="animation-delay: 300ms"
                *ngIf="analytics()?.insights?.recommendations?.length || analytics()?.insights?.achievements?.length">
                <h3 class="text-lg font-bold text-gray-900 mb-4">Insights</h3>
                
                <!-- Achievements -->
                <div *ngIf="analytics()?.insights?.achievements?.length" class="mb-4">
                  <p class="text-xs uppercase tracking-wider text-gray-500 mb-2">Achievements</p>
                  <ul class="space-y-2">
                    <li *ngFor="let achievement of analytics()?.insights?.achievements"
                      class="flex items-start gap-2 text-sm text-gray-700 bg-green-50 p-3 rounded-lg">
                      <svg class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                      </svg>
                      {{ achievement }}
                    </li>
                  </ul>
                </div>

                <!-- Recommendations -->
                <div *ngIf="analytics()?.insights?.recommendations?.length">
                  <p class="text-xs uppercase tracking-wider text-gray-500 mb-2">Recommendations</p>
                  <ul class="space-y-2">
                    <li *ngFor="let rec of analytics()?.insights?.recommendations"
                      class="flex items-start gap-2 text-sm text-gray-700 bg-blue-50 p-3 rounded-lg">
                      <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      {{ rec }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 animate-slide-up" style="animation-delay: 350ms">
            <a routerLink="/fitness-plan/calories"
              class="group bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary-200 transition-all duration-300 text-center">
              <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"/>
                </svg>
              </div>
              <p class="font-semibold text-gray-900">Calorie Plan</p>
              <p class="text-xs text-gray-500 mt-1">View breakdown</p>
            </a>
            <a routerLink="/fitness-plan/macros"
              class="group bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary-200 transition-all duration-300 text-center">
              <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                </svg>
              </div>
              <p class="font-semibold text-gray-900">Macro Plan</p>
              <p class="text-xs text-gray-500 mt-1">Balance nutrients</p>
            </a>
            <a routerLink="/progress/log"
              class="group bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary-200 transition-all duration-300 text-center">
              <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-blue-400 to-indigo-500 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
              </div>
              <p class="font-semibold text-gray-900">Log Progress</p>
              <p class="text-xs text-gray-500 mt-1">Track daily</p>
            </a>
            <a routerLink="/progress/chart"
              class="group bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary-200 transition-all duration-300 text-center">
              <div class="w-14 h-14 mx-auto mb-3 rounded-xl bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/>
                </svg>
              </div>
              <p class="font-semibold text-gray-900">Progress Charts</p>
              <p class="text-xs text-gray-500 mt-1">Visualize trends</p>
            </a>
          </div>
        </ng-container>

        <!-- Loading Skeleton -->
        <div *ngIf="isLoading()" class="animate-pulse space-y-6">
          <div class="h-48 bg-gray-200 rounded-2xl"></div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <div class="h-32 bg-gray-200 rounded-xl"></div>
            <div class="h-32 bg-gray-200 rounded-xl"></div>
            <div class="h-32 bg-gray-200 rounded-xl"></div>
            <div class="h-32 bg-gray-200 rounded-xl"></div>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="lg:col-span-2 h-64 bg-gray-200 rounded-xl"></div>
            <div class="h-64 bg-gray-200 rounded-xl"></div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes slideUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in {
      animation: fadeIn 0.5s ease-out forwards;
    }
    .animate-slide-up {
      opacity: 0;
      animation: slideUp 0.5s ease-out forwards;
    }
  `]
})
export class DashboardComponent implements OnInit {
  // Services
  private userService = inject(UserService);
  private fitnessService = inject(FitnessService);
  private analyticsService = inject(AnalyticsService);
  private loadingService = inject(LoadingService);
  private notificationService = inject(NotificationService);

  // State signals
  profile = signal<Profile | null>(null);
  fitness = signal<FitnessCalculation | null>(null);
  todayWorkout = signal<WorkoutDay | null>(null);
  analytics = signal<DashboardAnalytics | null>(null);
  isLoading = signal<boolean>(true);
  currentDate = signal<Date>(new Date());

  // Computed values
  currentWeight = computed(() => {
    const analyticsData = this.analytics();
    const profileData = this.profile();
    return analyticsData?.insights?.current_weight ?? profileData?.weight ?? 0;
  });

  goalProgressPercent = computed(() => {
    const fitnessData = this.fitness();
    const analyticsData = this.analytics();
    if (!fitnessData?.target_weight) return 0;

    const startWeight = analyticsData?.insights?.starting_weight ?? this.profile()?.weight ?? 0;
    const currentWt = this.currentWeight();
    const targetWt = fitnessData.target_weight;

    if (startWeight === targetWt) return 100;
    const progress = Math.abs(startWeight - currentWt) / Math.abs(startWeight - targetWt) * 100;
    return Math.min(Math.max(progress, 0), 100);
  });

  ngOnInit(): void {
    this.loadDashboardData();
  }

  refreshData(): void {
    this.loadDashboardData(true);
  }

  private loadDashboardData(showNotification = false): void {
    this.isLoading.set(true);

    this.userService.getProfile().subscribe({
      next: (p: Profile) => {
        this.profile.set(p);
        this.loadFitnessData();
        this.loadAnalytics();
        if (showNotification) {
          this.notificationService.success('Dashboard refreshed');
        }
      },
      error: () => {
        this.isLoading.set(false);
      },
    });
  }

  private loadFitnessData(): void {
    this.fitnessService.getWorkoutPlan().subscribe({
      next: (wp: WorkoutPlan) => {
        this.setTodayWorkout(wp);
        this.loadCachedCalculation();
        this.isLoading.set(false);
      },
      error: () => {
        this.loadCachedCalculation();
        this.isLoading.set(false);
      },
    });
  }

  private loadAnalytics(): void {
    this.analyticsService.fetchDashboardAnalytics().subscribe({
      next: (res: { success: boolean; data: DashboardAnalytics }) => {
        if (res.success) {
          this.analytics.set(res.data);
        }
      },
      error: () => {
        // Analytics are optional, don't show error
      },
    });
  }

  private loadCachedCalculation(): void {
    const cached = localStorage.getItem('fitcoach_calc');
    if (cached) {
      try {
        this.fitness.set(JSON.parse(cached));
      } catch {
        // ignore
      }
    }
  }

  private setTodayWorkout(wp: WorkoutPlan): void {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const today = days[new Date().getDay()];
    this.todayWorkout.set(wp.plan.find((d) => d.day === today) || wp.plan[0] || null);
  }

  // Helper methods for template
  getDayName(): string {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return days[new Date().getDay()];
  }

  getWeeklyChange(): number {
    return this.analytics()?.weight_trend?.weekly_change_kg ?? 0;
  }

  getWeightTrend(): 'up' | 'down' | 'neutral' {
    const dir = this.analytics()?.weight_trend?.direction;
    if (dir === 'losing') return 'down';
    if (dir === 'gaining') return 'up';
    return 'neutral';
  }

  getWeightTrendLabel(): string {
    const dir = this.analytics()?.weight_trend?.direction;
    if (dir === 'losing') return 'Losing';
    if (dir === 'gaining') return 'Gaining';
    return 'Stable';
  }

  getCalorieTrend(): 'up' | 'down' | 'neutral' {
    const adherence = this.analytics()?.calorie_adherence;
    if (!adherence) return 'neutral';
    if (adherence.adherence_score >= 80) return 'up';
    if (adherence.adherence_score < 60) return 'down';
    return 'neutral';
  }

  getCalorieTrendLabel(): string {
    const score = this.analytics()?.calorie_adherence?.adherence_score;
    if (!score) return '';
    return `${Math.round(score)}% adherence`;
  }

  getConsistencyScore(): number {
    return Math.round((this.analytics()?.weight_trend?.consistency_score ?? 0) * 100);
  }

  getProteinPercent(): number {
    const f = this.fitness();
    if (!f) return 0;
    const total = (f.protein * 4) + (f.carbs * 4) + (f.fat * 9);
    return total > 0 ? Math.round((f.protein * 4 / total) * 100) : 0;
  }

  getCarbsPercent(): number {
    const f = this.fitness();
    if (!f) return 0;
    const total = (f.protein * 4) + (f.carbs * 4) + (f.fat * 9);
    return total > 0 ? Math.round((f.carbs * 4 / total) * 100) : 0;
  }

  getFatPercent(): number {
    const f = this.fitness();
    if (!f) return 0;
    const total = (f.protein * 4) + (f.carbs * 4) + (f.fat * 9);
    return total > 0 ? Math.round((f.fat * 9 / total) * 100) : 0;
  }

  getDeficitSurplus(): number {
    const f = this.fitness();
    if (!f) return 0;
    return Math.abs((f.calorie_target || 0) - (f.tdee || 0));
  }

  getDeficitSurplusLabel(): string {
    const f = this.fitness();
    if (!f) return 'Balance';
    const diff = (f.calorie_target || 0) - (f.tdee || 0);
    if (diff < -50) return 'Deficit (kcal)';
    if (diff > 50) return 'Surplus (kcal)';
    return 'Maintenance';
  }
}
