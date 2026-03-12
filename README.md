# FitCoach AI

A professional, production-ready personal fitness coaching platform that generates personalized calorie targets, macro nutrition breakdowns, workout plans, progress analytics, and goal timeline projections.

Built with **Angular 19**, **FastAPI**, **MySQL**, **Tailwind CSS**, and modern software engineering patterns.

---

## ✨ Features

### Core Fitness Features
- **User Authentication** — JWT-based login and registration with bcrypt password hashing
- **Profile Management** — Store body metrics (age, sex, height, weight, body fat %)
- **Fitness Goal Selection** — Choose between Cut, Bulk, or Maintain goals
- **Calculation Engine** — BMR (Mifflin-St Jeor), TDEE, calorie targets, macro distribution
- **Workout Plan Generator** — Structured weekly plans (Upper/Lower, Push/Pull/Legs, Full Body)
- **Timeline Estimator** — Estimated weeks to reach goal weight
- **Progress Tracking** — Log weight and body fat over time with paginated history

### Advanced Analytics
- **Weight Trend Analysis** — Track weekly changes, direction, consistency scores
- **Body Fat Trend Analysis** — Monitor body composition changes over time
- **Calorie Adherence Estimation** — Assess how well targets are being met
- **Weekly Insights** — Personalized recommendations and achievements
- **Goal Progress Visualization** — Interactive progress rings and stat cards

### Professional UI/UX
- **Modern Dashboard** — Comprehensive analytics with animated cards and charts
- **Toast Notifications** — Real-time feedback for user actions
- **Loading States** — Global and scoped loading indicators
- **Responsive Design** — Mobile-first Tailwind CSS with glassmorphism effects
- **Custom Animations** — Fade, slide, scale, bounce, shimmer effects

---

## 🏗️ Architecture

### Backend Architecture
```
backend/
├── main.py                      # FastAPI app with lifespan, middleware, routers
├── requirements.txt             # Python dependencies
├── schema.sql                   # MySQL schema reference
├── .env.example                 # Environment template
└── app/
    ├── api/
    │   └── v1/                  # Versioned API (v1)
    │       ├── router.py        # V1 router aggregator
    │       └── endpoints/       # Route handlers
    │           ├── auth.py      # Authentication endpoints
    │           ├── users.py     # User & profile management
    │           ├── fitness.py   # Fitness calculations
    │           ├── progress.py  # Progress logging
    │           └── analytics.py # Dashboard analytics
    ├── config/
    │   └── database.py          # SQLAlchemy engine & session
    ├── core/
    │   ├── config.py            # Legacy settings
    │   ├── settings.py          # Pydantic Settings (enhanced)
    │   ├── security.py          # JWT creation & verification
    │   ├── exceptions.py        # Custom exception hierarchy
    │   ├── responses.py         # Standardized API responses
    │   └── logging.py           # Loguru configuration
    ├── middleware/
    │   ├── error_handler.py     # Global exception handlers
    │   ├── rate_limiter.py      # SlowAPI rate limiting
    │   └── request_logger.py    # Request/response logging
    ├── models/                   # SQLAlchemy ORM models
    ├── repositories/             # Data access layer
    │   ├── base_repository.py   # Generic CRUD operations
    │   ├── user_repository.py
    │   ├── profile_repository.py
    │   ├── goal_repository.py
    │   └── progress_repository.py
    ├── schemas/                  # Pydantic request/response models
    ├── services/
    │   ├── fitness_calculator.py
    │   ├── workout_generator.py
    │   ├── timeline_estimator.py
    │   └── progress_analytics.py # Advanced analytics service
    └── utils/
        ├── jwt_handler.py
        ├── password_hash.py
        ├── validators.py
        ├── fitness_helpers.py    # BMR, TDEE, macro calculations
        └── transformers.py       # Data transformation utilities
```

### Frontend Architecture
```
frontend/
├── angular.json
├── package.json
├── tailwind.config.js           # Extended with custom animations
├── postcss.config.js
└── src/
    ├── index.html
    ├── main.ts
    ├── styles.css               # Global styles with animations
    └── app/
        ├── app.component.ts     # Root with toast & loading
        ├── app.config.ts        # Providers & interceptors
        ├── app.routes.ts
        ├── core/
        │   ├── guards/
        │   │   └── auth.guard.ts
        │   ├── interceptors/
        │   │   ├── jwt.interceptor.ts
        │   │   └── error.interceptor.ts  # Global error handling
        │   └── services/
        │       ├── auth.service.ts
        │       ├── fitness.service.ts
        │       ├── progress.service.ts
        │       ├── user.service.ts
        │       ├── analytics.service.ts  # Dashboard analytics
        │       ├── notification.service.ts # Toast notifications
        │       └── loading.service.ts    # Loading state
        ├── modules/
        │   ├── auth/
        │   │   ├── login/
        │   │   └── register/
        │   ├── dashboard/        # Professional analytics dashboard
        │   ├── fitness-plan/
        │   │   ├── calorie-plan/
        │   │   ├── macro-plan/
        │   │   └── workout-plan/
        │   ├── goals/
        │   ├── profile/
        │   └── progress/
        │       ├── progress-chart/
        │       └── progress-log/
        └── shared/
            ├── components/
            │   ├── ui-button/
            │   ├── ui-card/
            │   ├── ui-form/
            │   ├── toast-container/    # Toast notifications
            │   ├── loading-spinner/    # Loading indicators
            │   ├── stat-card/          # Dashboard stat cards
            │   ├── progress-ring/      # Circular progress
            │   ├── modal/              # Reusable modal
            │   ├── confirm-dialog/     # Confirmation dialogs
            │   ├── empty-state/        # Empty state placeholders
            │   └── macro-card/         # Macro nutrient cards
            └── models/
                ├── goal.model.ts
                ├── progress.model.ts
                └── user.model.ts
```

---

## 🛠️ Tech Stack

| Layer          | Technology                                          |
| -------------- | --------------------------------------------------- |
| Frontend       | Angular 19, Tailwind CSS 3.4, Chart.js 4.4          |
| Backend        | Python 3.10+, FastAPI 0.115, SQLAlchemy 2.0         |
| Database       | MySQL 8.0+                                          |
| Authentication | JWT (python-jose), bcrypt (passlib)                 |
| Logging        | Loguru                                              |
| Rate Limiting  | SlowAPI                                             |
| Analytics      | pandas, numpy                                       |
| Validation     | Pydantic v2                                         |

---

## 📋 Prerequisites

- **Python 3.10+**
- **Node.js 20+** and **npm**
- **MySQL 8.0+**
- **Angular CLI** (`npm install -g @angular/cli`)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fitness-coach
```

### 2. MySQL Database Setup

```sql
CREATE DATABASE IF NOT EXISTS fitcoach
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Or execute the full schema:

```bash
mysql -u root -p < backend/schema.sql
```

> **Note:** The backend auto-creates tables on startup via SQLAlchemy.

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file:

```env
# Database
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fitcoach

# Security
SECRET_KEY=your-random-secret-key-minimum-32-characters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application
DEBUG=false
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:4200
```

Start the backend:

```bash
uvicorn main:app --reload --port 8000
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
ng serve
```

The application will be available at `http://localhost:4200`.

---

## 📡 API Documentation

### Interactive Docs
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### API Versioning

The API supports versioning. Current version: **v1**

- Versioned endpoints: `/api/v1/...`
- Legacy endpoints: `/api/...` (deprecated, maintained for compatibility)

### Authentication Endpoints

| Method | Endpoint                  | Description         | Rate Limit |
| ------ | ------------------------- | ------------------- | ---------- |
| POST   | `/api/v1/auth/register`   | Register new user   | 5/min      |
| POST   | `/api/v1/auth/login`      | Login & get JWT     | 10/min     |

### User Endpoints

| Method | Endpoint                  | Description           |
| ------ | ------------------------- | --------------------- |
| GET    | `/api/v1/users/me`        | Get current user      |
| GET    | `/api/v1/users/profile`   | Get user profile      |
| POST   | `/api/v1/users/profile`   | Create profile        |
| PUT    | `/api/v1/users/profile`   | Update profile        |
| GET    | `/api/v1/users/goal`      | Get current goal      |
| POST   | `/api/v1/users/goal`      | Set fitness goal      |

### Fitness Endpoints

| Method | Endpoint                       | Description                    |
| ------ | ------------------------------ | ------------------------------ |
| POST   | `/api/v1/fitness/calculate`    | Calculate calories & macros    |
| GET    | `/api/v1/fitness/workout-plan` | Get personalized workout plan  |

### Progress Endpoints

| Method | Endpoint                    | Description               |
| ------ | --------------------------- | ------------------------- |
| POST   | `/api/v1/progress/log`      | Log weight & body fat     |
| GET    | `/api/v1/progress/history`  | Get paginated history     |
| GET    | `/api/v1/progress/latest`   | Get latest entry          |

### Analytics Endpoints

| Method | Endpoint                         | Description                      |
| ------ | -------------------------------- | -------------------------------- |
| GET    | `/api/v1/analytics/dashboard`    | Comprehensive dashboard data     |
| GET    | `/api/v1/analytics/weight-trend` | Weight trend analysis (±days)    |
| GET    | `/api/v1/analytics/body-fat-trend` | Body fat trend analysis        |
| GET    | `/api/v1/analytics/insights`     | Personalized insights & tips     |

### Standardized Response Format

All API responses follow this structure:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... },
  "timestamp": "2026-03-13T10:30:00Z"
}
```

Error responses:

```json
{
  "success": false,
  "message": "Error description",
  "error_code": "VALIDATION_ERROR",
  "details": { ... },
  "timestamp": "2026-03-13T10:30:00Z"
}
```

---

## 🧮 Fitness Calculation Details

### BMR (Mifflin-St Jeor)

- **Male:** `10 × weight(kg) + 6.25 × height(cm) − 5 × age + 5`
- **Female:** `10 × weight(kg) + 6.25 × height(cm) − 5 × age − 161`

### TDEE

`TDEE = BMR × Activity Multiplier`

| Level       | Multiplier |
| ----------- | ---------- |
| Sedentary   | 1.20       |
| Light       | 1.375      |
| Moderate    | 1.55       |
| Active      | 1.725      |
| Very Active | 1.90       |

### Calorie Adjustments

| Goal     | Adjustment |
| -------- | ---------- |
| Cut      | TDEE − 500 |
| Bulk     | TDEE + 350 |
| Maintain | TDEE       |

### Macro Distribution

| Goal     | Protein | Carbs | Fat  |
| -------- | ------- | ----- | ---- |
| Cut      | 40%     | 30%   | 30%  |
| Bulk     | 30%     | 45%   | 25%  |
| Maintain | 30%     | 40%   | 30%  |

---

## 🎨 UI Components

### Reusable Components

| Component          | Description                                    |
| ------------------ | ---------------------------------------------- |
| `StatCardComponent` | Dashboard stat cards with gradients & trends  |
| `ProgressRingComponent` | Circular SVG progress indicators         |
| `MacroCardComponent` | Macro nutrient display with percentages      |
| `ToastContainerComponent` | Animated toast notifications           |
| `LoadingSpinnerComponent` | Full-screen & inline loading states   |
| `ModalComponent`   | Reusable modal dialog                          |
| `ConfirmDialogComponent` | Confirmation dialogs with variants      |
| `EmptyStateComponent` | Placeholder for empty data states           |

### Animation Classes

```css
/* Fade animations */
.animate-fade-in
.animate-fade-out

/* Slide animations */
.animate-slide-up
.animate-slide-down
.animate-slide-left
.animate-slide-right

/* Scale animations */
.animate-scale-in
.animate-bounce-in

/* Effects */
.animate-pulse-glow
.animate-shimmer

/* Hover effects */
.hover-lift
.hover-scale
.hover-glow

/* Animation delays */
.animation-delay-100 through .animation-delay-500
```

---

## 🔒 Security Features

- **JWT Authentication** — Secure token-based auth with configurable expiration
- **Password Hashing** — bcrypt with automatic salt generation
- **Rate Limiting** — Configurable limits per endpoint (auth: 5-10/min, reads: 60/min, writes: 30/min)
- **CORS Protection** — Configurable allowed origins
- **Input Validation** — Pydantic v2 schema validation
- **SQL Injection Prevention** — SQLAlchemy ORM parameterized queries

---

## 📊 Logging & Monitoring

The application uses **Loguru** for structured logging:

- **Request Logging** — All API requests with timing
- **Error Logging** — Detailed error traces with context
- **User Action Logging** — Authentication and key actions
- **File Rotation** — Automatic log file management

Log location: `backend/logs/`

---

## 🧪 Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
ng test
```

### Code Quality

```bash
# Backend linting
cd backend
flake8 .
black . --check

# Frontend linting
cd frontend
ng lint
```

---

## 📝 Environment Variables

| Variable                     | Description                    | Default        |
| ---------------------------- | ------------------------------ | -------------- |
| `DB_USER`                    | MySQL username                 | root           |
| `DB_PASSWORD`                | MySQL password                 | -              |
| `DB_HOST`                    | MySQL host                     | localhost      |
| `DB_PORT`                    | MySQL port                     | 3306           |
| `DB_NAME`                    | Database name                  | fitcoach       |
| `SECRET_KEY`                 | JWT signing key                | -              |
| `JWT_ALGORITHM`              | JWT algorithm                  | HS256          |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| Token expiration               | 1440 (24h)     |
| `DEBUG`                      | Debug mode                     | false          |
| `LOG_LEVEL`                  | Logging level                  | INFO           |
| `CORS_ORIGINS`               | Allowed CORS origins           | localhost:4200 |

---

## 📜 License

This project is for educational purposes (college final project).

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support

For questions or issues, please open a GitHub issue.