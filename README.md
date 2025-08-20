# MediSync - Healthcare Management System

A comprehensive healthcare management system with role-based authentication for doctors, nurses, and patients.

## Features

### Authentication System
- **Role-based Registration**: Different signup forms for doctors, nurses, and patients
- **Email-only Login**: Secure authentication using registered email addresses
- **Password Requirements**: Alphanumeric combinations with minimum 8 characters
- **Account Verification**: Document upload system (PDF, JPG, PNG) for identity verification
- **JWT Token Authentication**: Secure token-based authentication

### Role-Specific Features

#### Doctor Dashboard
- Patient management and records
- Appointment scheduling
- Medical consultations
- Revenue tracking
- Professional profile management

#### Nurse Dashboard
- Patient care tasks
- Vital signs monitoring
- Medication administration
- Emergency alerts
- Care coordination

#### Patient Dashboard (Mobile-Optimized)
- Health summary and vitals
- Appointment booking and management
- Medical records access
- Medication tracking
- Emergency contact features

## Technology Stack

### Backend
- **Django 5.0+**: Python web framework
- **Django REST Framework**: API development
- **Django Simple JWT**: JWT authentication
- **SQLite**: Database (can be configured for PostgreSQL/MySQL)

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **Quasar Framework**: Vue.js UI framework
- **TypeScript**: Type-safe JavaScript
- **Axios**: HTTP client for API communication

## Installation & Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:9000`

## API Endpoints

### Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/token/refresh/` - Token refresh

### User Management
- `GET /api/users/profile/` - Get user profile
- `POST /api/users/profile/update/picture/` - Update profile picture

### Verification
- `POST /api/users/verification/upload/` - Upload verification document
- `POST /api/users/verification/verify-now/` - Mark user as verified

## User Flow

### Registration Process
1. User visits the application
2. Clicks "Create Account" → Redirected to role selection
3. Selects role (Doctor/Nurse/Patient) → Redirected to role-specific registration form
4. Fills out registration form with role-specific fields
5. Submits form → Redirected to verification page
6. Uploads identity document (PDF/JPG/PNG)
7. Chooses "Verify Now" or "Verify Later"
8. Redirected to appropriate dashboard based on role

### Login Process
1. User enters registered email and password
2. System validates credentials
3. Upon successful login, user is redirected to role-specific dashboard:
   - Doctors → `/doctor-dashboard`
   - Nurses → `/nurse-dashboard`
   - Patients → `/patient-dashboard`

## Password Requirements

- Minimum 8 characters
- Must contain at least one letter and one number
- Alphanumeric combinations allowed
- Special characters: `@$!%*?&`

## File Upload Requirements

### Verification Documents
- **Accepted formats**: PDF, JPG, PNG
- **Maximum size**: 5MB
- **Purpose**: Identity verification for account approval

## Security Features

- JWT token-based authentication
- Password validation with strong requirements
- File upload validation and size limits
- Role-based access control
- Automatic token refresh
- Secure logout with token cleanup

## Mobile Optimization

The patient dashboard is specifically optimized for mobile devices with:
- Responsive design
- Touch-friendly interface
- Mobile-first layout
- Optimized navigation
- Compact information display

## Development Notes

### Backend Structure
```
backend/
├── users/                 # User management app
│   ├── models.py         # User and profile models
│   ├── views.py          # API views
│   ├── serializers.py    # Data serialization
│   └── urls.py           # URL routing
├── operations/           # Medical operations app
├── predictive_analytics/ # Analytics features
└── settings.py          # Django settings
```

### Frontend Structure
```
frontend/
├── src/
│   ├── pages/           # Vue page components
│   │   ├── LoginPage.vue
│   │   ├── RoleSelectionPage.vue
│   │   ├── RegisterPage.vue
│   │   ├── VerificationPage.vue
│   │   ├── DoctorDashboard.vue
│   │   ├── NurseDashboard.vue
│   │   └── PatientDashboard.vue
│   ├── router/          # Vue Router configuration
│   └── boot/            # Application boot files
└── package.json
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
