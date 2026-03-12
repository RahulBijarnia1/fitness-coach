import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-ui-form',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="card" [ngClass]="extraClass">
      <h2 *ngIf="title" class="text-lg font-bold text-gray-900 mb-4">{{ title }}</h2>
      <ng-content></ng-content>
    </div>
  `,
})
export class UiFormComponent {
  @Input() title = '';
  @Input() extraClass = '';
}
