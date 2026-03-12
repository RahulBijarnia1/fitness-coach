import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@env/environment';
import {
  FitnessCalculation,
  WorkoutPlan,
} from '@shared/models/goal.model';

@Injectable({ providedIn: 'root' })
export class FitnessService {
  private baseUrl = `${environment.apiUrl}/fitness`;

  constructor(private http: HttpClient) {}

  calculate(data: {
    goal_type: string;
    activity_level: string;
  }): Observable<FitnessCalculation> {
    return this.http.post<FitnessCalculation>(
      `${this.baseUrl}/calculate`,
      data
    );
  }

  getWorkoutPlan(): Observable<WorkoutPlan> {
    return this.http.get<WorkoutPlan>(`${this.baseUrl}/workout-plan`);
  }
}
