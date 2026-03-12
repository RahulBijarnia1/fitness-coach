import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { ProgressService } from '../../../core/services/progress.service';
import { ProgressLog } from '@shared/models/progress.model';

@Component({
  selector: 'app-progress-log',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="max-w-3xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">Log Progress</h1>

      <!-- Form -->
      <form
        [formGroup]="form"
        (ngSubmit)="onSubmit()"
        class="card mb-8 space-y-4"
      >
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="label">Weight (kg)</label>
            <input
              type="number"
              formControlName="weight"
              class="input-field"
              placeholder="75"
            />
          </div>
          <div>
            <label class="label">Body Fat % (optional)</label>
            <input
              type="number"
              formControlName="body_fat"
              class="input-field"
              placeholder="15"
            />
          </div>
          <div>
            <label class="label">Date</label>
            <input
              type="date"
              formControlName="date"
              class="input-field"
            />
          </div>
        </div>
        <button
          type="submit"
          class="btn-primary"
          [disabled]="form.invalid || loading"
        >
          {{ loading ? 'Saving...' : 'Log Entry' }}
        </button>
      </form>

      <div
        *ngIf="success"
        class="mb-4 rounded-lg bg-accent-50 p-3 text-sm text-accent-700"
      >
        Progress logged!
      </div>

      <!-- History table -->
      <div class="card">
        <h2 class="font-bold text-lg mb-4 text-gray-900">History</h2>
        <div class="overflow-x-auto">
          <table class="w-full text-sm" *ngIf="logs.length; else noLogs">
            <thead>
              <tr
                class="text-left text-xs text-gray-400 uppercase tracking-wider border-b border-gray-100"
              >
                <th class="pb-2">Date</th>
                <th class="pb-2">Weight (kg)</th>
                <th class="pb-2">Body Fat %</th>
              </tr>
            </thead>
            <tbody>
              <tr
                *ngFor="let log of logs"
                class="border-t border-gray-50"
              >
                <td class="py-2">{{ log.date }}</td>
                <td class="py-2 font-semibold">{{ log.weight }}</td>
                <td class="py-2">{{ log.body_fat ?? '—' }}</td>
              </tr>
            </tbody>
          </table>
          <ng-template #noLogs>
            <p class="text-gray-400 text-sm">No progress logged yet.</p>
          </ng-template>
        </div>

        <!-- Pagination -->
        <div
          *ngIf="totalPages > 1"
          class="mt-4 flex items-center justify-between text-sm"
        >
          <button
            class="btn-secondary text-xs"
            [disabled]="currentPage <= 1"
            (click)="loadPage(currentPage - 1)"
          >
            Previous
          </button>
          <span class="text-gray-500"
            >Page {{ currentPage }} of {{ totalPages }}</span
          >
          <button
            class="btn-secondary text-xs"
            [disabled]="currentPage >= totalPages"
            (click)="loadPage(currentPage + 1)"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  `,
})
export class ProgressLogComponent implements OnInit {
  form: FormGroup;
  logs: ProgressLog[] = [];
  loading = false;
  success = false;
  currentPage = 1;
  totalPages = 1;
  pageSize = 10;

  constructor(
    private fb: FormBuilder,
    private progressService: ProgressService
  ) {
    const today = new Date().toISOString().split('T')[0];
    this.form = this.fb.group({
      weight: [null, [Validators.required, Validators.min(1)]],
      body_fat: [null],
      date: [today],
    });
  }

  ngOnInit(): void {
    this.loadPage(1);
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.success = false;
    const data = this.form.value;
    if (!data.body_fat) data.body_fat = null;
    this.progressService.log(data).subscribe({
      next: () => {
        this.loading = false;
        this.success = true;
        this.form.get('weight')?.reset();
        this.form.get('body_fat')?.reset();
        this.loadPage(1);
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  loadPage(page: number): void {
    this.progressService.getHistory(page, this.pageSize).subscribe({
      next: (res) => {
        this.logs = res.logs;
        this.currentPage = res.page;
        this.totalPages = Math.ceil(res.total / res.page_size) || 1;
      },
    });
  }
}
