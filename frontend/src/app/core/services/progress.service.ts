import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '@env/environment';
import { ProgressHistory, ProgressLog } from '@shared/models/progress.model';

@Injectable({ providedIn: 'root' })
export class ProgressService {
  private baseUrl = `${environment.apiUrl}/progress`;

  constructor(private http: HttpClient) {}

  log(data: {
    weight: number;
    body_fat?: number | null;
    date?: string;
  }): Observable<ProgressLog> {
    return this.http.post<ProgressLog>(`${this.baseUrl}/log`, data);
  }

  getHistory(page = 1, pageSize = 20): Observable<ProgressHistory> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());
    return this.http.get<ProgressHistory>(`${this.baseUrl}/history`, {
      params,
    });
  }
}
