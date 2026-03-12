import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <div
      class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-accent-50 px-4"
    >
      <div class="card w-full max-w-md">
        <h1
          class="text-2xl font-bold text-center bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent mb-6"
        >
          Create Account
        </h1>

        <div
          *ngIf="error"
          class="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600"
        >
          {{ error }}
        </div>

        <form [formGroup]="form" (ngSubmit)="onSubmit()" class="space-y-4">
          <div>
            <label class="label">Email</label>
            <input
              type="email"
              formControlName="email"
              class="input-field"
              placeholder="you&#64;example.com"
            />
            <p
              class="error-text"
              *ngIf="form.get('email')?.touched && form.get('email')?.invalid"
            >
              Please enter a valid email.
            </p>
          </div>

          <div>
            <label class="label">Password</label>
            <input
              type="password"
              formControlName="password"
              class="input-field"
              placeholder="Min 8 characters"
            />
            <p
              class="error-text"
              *ngIf="
                form.get('password')?.touched && form.get('password')?.invalid
              "
            >
              Password must be at least 8 characters.
            </p>
          </div>

          <div>
            <label class="label">Confirm Password</label>
            <input
              type="password"
              formControlName="confirmPassword"
              class="input-field"
              placeholder="••••••••"
            />
            <p
              class="error-text"
              *ngIf="
                form.get('confirmPassword')?.touched &&
                form.get('confirmPassword')?.value !== form.get('password')?.value
              "
            >
              Passwords do not match.
            </p>
          </div>

          <button
            type="submit"
            class="btn-primary w-full"
            [disabled]="form.invalid || loading"
          >
            {{ loading ? 'Creating account...' : 'Sign Up' }}
          </button>
        </form>

        <p class="mt-4 text-center text-sm text-gray-500">
          Already have an account?
          <a routerLink="/login" class="font-semibold text-primary-600 hover:underline"
            >Sign In</a
          >
        </p>
      </div>
    </div>
  `,
})
export class RegisterComponent {
  form: FormGroup;
  loading = false;
  error = '';

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router
  ) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', [Validators.required]],
    });
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    const { email, password, confirmPassword } = this.form.value;
    if (password !== confirmPassword) {
      this.error = 'Passwords do not match';
      return;
    }
    this.loading = true;
    this.error = '';
    this.auth.register(email, password).subscribe({
      next: () => this.router.navigate(['/profile']),
      error: (err) => {
        this.loading = false;
        this.error = err.error?.detail || 'Registration failed';
      },
    });
  }
}
