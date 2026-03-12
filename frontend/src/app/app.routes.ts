import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full',
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./modules/auth/login/login.component').then(
        (m) => m.LoginComponent
      ),
  },
  {
    path: 'register',
    loadComponent: () =>
      import('./modules/auth/register/register.component').then(
        (m) => m.RegisterComponent
      ),
  },
  {
    path: 'profile',
    canActivate: [authGuard],
    loadComponent: () =>
      import(
        './modules/profile/profile-form/profile-form.component'
      ).then((m) => m.ProfileFormComponent),
  },
  {
    path: 'goals',
    canActivate: [authGuard],
    loadComponent: () =>
      import(
        './modules/goals/goal-selection/goal-selection.component'
      ).then((m) => m.GoalSelectionComponent),
  },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () =>
      import(
        './modules/dashboard/dashboard.component'
      ).then((m) => m.DashboardComponent),
  },
  {
    path: 'fitness-plan',
    canActivate: [authGuard],
    children: [
      {
        path: '',
        redirectTo: 'calories',
        pathMatch: 'full',
      },
      {
        path: 'calories',
        loadComponent: () =>
          import(
            './modules/fitness-plan/calorie-plan/calorie-plan.component'
          ).then((m) => m.CaloriePlanComponent),
      },
      {
        path: 'macros',
        loadComponent: () =>
          import(
            './modules/fitness-plan/macro-plan/macro-plan.component'
          ).then((m) => m.MacroPlanComponent),
      },
      {
        path: 'workout',
        loadComponent: () =>
          import(
            './modules/fitness-plan/workout-plan/workout-plan.component'
          ).then((m) => m.WorkoutPlanComponent),
      },
    ],
  },
  {
    path: 'progress',
    canActivate: [authGuard],
    children: [
      {
        path: '',
        redirectTo: 'log',
        pathMatch: 'full',
      },
      {
        path: 'log',
        loadComponent: () =>
          import(
            './modules/progress/progress-log/progress-log.component'
          ).then((m) => m.ProgressLogComponent),
      },
      {
        path: 'chart',
        loadComponent: () =>
          import(
            './modules/progress/progress-chart/progress-chart.component'
          ).then((m) => m.ProgressChartComponent),
      },
    ],
  },
  { path: '**', redirectTo: 'dashboard' },
];
