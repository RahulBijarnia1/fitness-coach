import {
  Component,
  OnInit,
  ViewChild,
  ElementRef,
  AfterViewInit,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ProgressService } from '../../../core/services/progress.service';
import { ProgressLog } from '@shared/models/progress.model';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-progress-chart',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="max-w-4xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">Progress Charts</h1>

      <div *ngIf="logs.length === 0" class="card text-center py-12 text-gray-500">
        No progress data yet.
        <a routerLink="/progress/log" class="text-primary-600 font-semibold hover:underline">
          Log your first entry
        </a>
      </div>

      <div *ngIf="logs.length" class="space-y-8">
        <div class="card">
          <h2 class="font-bold text-lg mb-4">Weight Over Time</h2>
          <canvas #weightChart></canvas>
        </div>

        <div class="card" *ngIf="hasBf">
          <h2 class="font-bold text-lg mb-4">Body Fat % Over Time</h2>
          <canvas #bfChart></canvas>
        </div>
      </div>
    </div>
  `,
})
export class ProgressChartComponent implements OnInit, AfterViewInit {
  @ViewChild('weightChart') weightChartRef!: ElementRef<HTMLCanvasElement>;
  @ViewChild('bfChart') bfChartRef!: ElementRef<HTMLCanvasElement>;

  logs: ProgressLog[] = [];
  hasBf = false;
  private ready = false;

  constructor(private progressService: ProgressService) {}

  ngOnInit(): void {
    this.progressService.getHistory(1, 100).subscribe({
      next: (res) => {
        this.logs = res.logs.slice().reverse(); // chronological
        this.hasBf = this.logs.some((l) => l.body_fat !== null);
        if (this.ready) this.renderCharts();
      },
    });
  }

  ngAfterViewInit(): void {
    this.ready = true;
    if (this.logs.length) this.renderCharts();
  }

  private renderCharts(): void {
    const labels = this.logs.map((l) => l.date);

    if (this.weightChartRef) {
      new Chart(this.weightChartRef.nativeElement, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'Weight (kg)',
              data: this.logs.map((l) => l.weight),
              borderColor: '#6366f1',
              backgroundColor: 'rgba(99,102,241,0.1)',
              fill: true,
              tension: 0.3,
              pointRadius: 4,
              pointBackgroundColor: '#6366f1',
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            y: { title: { display: true, text: 'kg' } },
          },
        },
      });
    }

    if (this.hasBf && this.bfChartRef) {
      new Chart(this.bfChartRef.nativeElement, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'Body Fat %',
              data: this.logs.map((l) => l.body_fat),
              borderColor: '#f43f5e',
              backgroundColor: 'rgba(244,63,94,0.1)',
              fill: true,
              tension: 0.3,
              pointRadius: 4,
              pointBackgroundColor: '#f43f5e',
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            y: { title: { display: true, text: '%' } },
          },
        },
      });
    }
  }
}
