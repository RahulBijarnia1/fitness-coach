import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from '../../../core/services/user.service';

@Component({
  selector: 'app-profile-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="max-w-2xl mx-auto px-4 py-10">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">
        {{ isEdit ? 'Update Profile' : 'Complete Your Profile' }}
      </h1>

      <div
        *ngIf="success"
        class="mb-4 rounded-lg bg-accent-50 p-3 text-sm text-accent-700"
      >
        Profile saved successfully!
      </div>
      <div
        *ngIf="error"
        class="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600"
      >
        {{ error }}
      </div>

      <form
        [formGroup]="form"
        (ngSubmit)="onSubmit()"
        class="card space-y-5"
      >
        <div>
          <label class="label">Full Name</label>
          <input formControlName="name" class="input-field" placeholder="John Doe" />
          <p class="error-text" *ngIf="form.get('name')?.touched && form.get('name')?.invalid">
            Name is required.
          </p>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">Age</label>
            <input
              type="number"
              formControlName="age"
              class="input-field"
              placeholder="25"
            />
          </div>
          <div>
            <label class="label">Sex</label>
            <select formControlName="sex" class="input-field">
              <option value="" disabled>Select</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">Height (cm)</label>
            <input
              type="number"
              formControlName="height"
              class="input-field"
              placeholder="175"
            />
          </div>
          <div>
            <label class="label">Weight (kg)</label>
            <input
              type="number"
              formControlName="weight"
              class="input-field"
              placeholder="75"
            />
          </div>
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

        <button
          type="submit"
          class="btn-primary w-full"
          [disabled]="form.invalid || loading"
        >
          {{ loading ? 'Saving...' : isEdit ? 'Update Profile' : 'Save Profile' }}
        </button>
      </form>
    </div>
  `,
})
export class ProfileFormComponent implements OnInit {
  form: FormGroup;
  isEdit = false;
  loading = false;
  success = false;
  error = '';

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private router: Router
  ) {
    this.form = this.fb.group({
      name: ['', [Validators.required]],
      age: [null, [Validators.required, Validators.min(13), Validators.max(120)]],
      sex: ['', [Validators.required]],
      height: [null, [Validators.required, Validators.min(1)]],
      weight: [null, [Validators.required, Validators.min(1)]],
      body_fat: [null],
    });
  }

  ngOnInit(): void {
    this.userService.getProfile().subscribe({
      next: (profile) => {
        this.isEdit = true;
        this.form.patchValue(profile);
      },
      error: () => {
        // profile doesn't exist yet; stay on create mode
      },
    });
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';
    this.success = false;

    const data = this.form.value;
    const request$ = this.isEdit
      ? this.userService.updateProfile(data)
      : this.userService.createProfile(data);

    request$.subscribe({
      next: () => {
        this.loading = false;
        this.success = true;
        this.isEdit = true;
        setTimeout(() => this.router.navigate(['/goals']), 800);
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.detail || 'Failed to save profile';
      },
    });
  }
}
