import { Component, OnInit, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FitnessCalculation } from '@shared/models/goal.model';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-macro-plan',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="max-w-3xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">Macro Breakdown</h1>

      <div *ngIf="calc; else noPlan">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
          <div class="card text-center">
            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Protein</p>
            <p class="text-3xl font-extrabold text-accent-600">
              {{ calc.protein | number : '1.0-0' }}g
            </p>
            <p class="text-xs text-gray-400">{{ proteinCal | number : '1.0-0' }} kcal</p>
          </div>
          <div class="card text-center">
            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Carbs</p>
            <p class="text-3xl font-extrabold text-amber-600">
              {{ calc.carbs | number : '1.0-0' }}g
            </p>
            <p class="text-xs text-gray-400">{{ carbsCal | number : '1.0-0' }} kcal</p>
          </div>
          <div class="card text-center">
            <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Fat</p>
            <p class="text-3xl font-extrabold text-rose-500">
              {{ calc.fat | number : '1.0-0' }}g
            </p>
            <p class="text-xs text-gray-400">{{ fatCal | number : '1.0-0' }} kcal</p>
          </div>
        </div>

        <!-- Doughnut chart -->
        <div class="card flex justify-center">
          <div class="w-72 h-72">
            <canvas #chartCanvas></canvas>
          </div>
        </div>
      </div>

      <ng-template #noPlan>
        <div class="card text-center py-12 text-gray-500">
          No plan calculated yet. Go to
          <a routerLink="/goals" class="text-primary-600 font-semibold hover:underline">Goals</a>
          to generate your plan.
        </div>
      </ng-template>
    </div>
  `,
})
export class MacroPlanComponent implements OnInit, AfterViewInit {
  @ViewChild('chartCanvas') chartCanvas!: ElementRef<HTMLCanvasElement>;

  calc: FitnessCalculation | null = null;
  proteinCal = 0;
  carbsCal = 0;
  fatCal = 0;

  ngOnInit(): void {
    const cached = localStorage.getItem('fitcoach_calc');
    if (cached) {
      try {
        this.calc = JSON.parse(cached);
        if (this.calc) {
          this.proteinCal = this.calc.protein * 4;
          this.carbsCal = this.calc.carbs * 4;
          this.fatCal = this.calc.fat * 9;
        }
      } catch {
        // ignore
      }
    }
  }

  ngAfterViewInit(): void {
    if (this.calc && this.chartCanvas) {
      new Chart(this.chartCanvas.nativeElement, {
        type: 'doughnut',
        data: {
          labels: ['Protein', 'Carbs', 'Fat'],
          datasets: [
            {
              data: [this.proteinCal, this.carbsCal, this.fatCal],
              backgroundColor: ['#22c55e', '#f59e0b', '#f43f5e'],
              hoverOffset: 8,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { position: 'bottom' },
          },
        },
      });
    }
  }
}
