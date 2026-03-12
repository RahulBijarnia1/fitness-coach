import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-ui-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="card" [ngClass]="extraClass">
      <ng-content></ng-content>
    </div>
  `,
})
export class UiCardComponent {
  @Input() extraClass = '';
}
