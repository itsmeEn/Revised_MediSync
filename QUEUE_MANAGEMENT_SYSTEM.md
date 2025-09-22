# Patient Queuing Management System

A comprehensive patient queuing management system built for MediSync Hospital that streamlines patient flow, reduces waiting times, and provides a seamless experience for both patients and staff.

## 🎯 System Overview

The Patient Queuing Management System is designed to:
- **Streamline patient flow** with automated queue management
- **Reduce waiting times** through efficient queue processing
- **Provide real-time updates** to patients about their queue status
- **Enable staff control** over queue operations
- **Ensure security** with role-based access control

## 🏗️ System Architecture

### Backend Components
- **Django REST Framework** for API endpoints
- **PostgreSQL/SQLite** for data persistence
- **JWT Authentication** for secure access
- **Real-time notifications** system

### Frontend Components
- **Vue.js 3** with TypeScript
- **Quasar Framework** for UI components
- **Real-time updates** with auto-refresh
- **Responsive design** for mobile and desktop

## 📋 Core Features

### For Patients

#### 1. Online Check-in Form
- **Secure authentication** required
- **Department selection** (OPD, Billing, Pharmacy, Appointment)
- **Optional appointment ID** linking
- **Priority level** selection (Normal, Senior Citizen, PWD)
- **Automatic queue number** assignment

#### 2. Real-time Queue Display
- **Live queue status** updates every 10 seconds
- **Current position** in queue
- **Estimated wait time** calculation
- **Queue number** tracking
- **Status updates** (Waiting, In Progress, Completed)

#### 3. Automated Notifications
- **Check-in confirmation** notifications
- **Turn approaching** alerts
- **Service completion** notifications
- **Queue status changes** updates

### For Staff (Nurses and Doctors)

#### 1. Secure Dashboard
- **Role-based access control** (Nurse/Doctor only)
- **Department-specific** queue management
- **Real-time statistics** display
- **Queue overview** with patient details

#### 2. Queue Management Features
- **Call next patient** with single button
- **Mark service as completed**
- **Remove patients** from queue
- **View queue statistics**
- **Priority queue** handling

## 🔧 API Endpoints

### Patient Endpoints
```
POST /api/operations/patient/check-in/
GET  /api/operations/patient/queue-status/
GET  /api/operations/public/queue-display/
```

### Staff Endpoints
```
GET  /api/operations/staff/queue-dashboard/
POST /api/operations/staff/call-next-patient/
POST /api/operations/staff/complete-service/
POST /api/operations/staff/remove-patient/
```

### Public Endpoints
```
GET  /api/operations/public/queue-display/
```

## 🗄️ Database Models

### QueueManagement Model
```python
class QueueManagement(models.Model):
    patient = ForeignKey(PatientProfile)
    queue_number = PositiveIntegerField(unique=True)
    department = CharField(choices=[...])
    status = CharField(choices=[...])
    position_in_queue = PositiveIntegerField()
    enqueue_time = DateTimeField()
    started_at = DateTimeField(null=True)
    finished_at = DateTimeField(null=True)
    estimated_wait_time = DurationField()
    actual_wait_time = DurationField()
```

### PriorityQueue Model
```python
class PriorityQueue(models.Model):
    patient = ForeignKey(PatientProfile)
    priority_level = CharField(choices=[...])
    department = CharField()
    queue_number = PositiveIntegerField(unique=True)
    priority_position = PositiveIntegerField()
```

### Notification Model
```python
class Notification(models.Model):
    user = ForeignKey(User)
    message = TextField()
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
```

## 🎨 Frontend Pages

### 1. Patient Queue Page (`/patient-queue`)
- **Check-in form** for joining queue
- **Personal queue status** display
- **Public queue** overview
- **Real-time updates** every 10 seconds
- **Notification** display

### 2. Staff Queue Dashboard (`/staff-queue-dashboard`)
- **Department selection** dropdown
- **Queue statistics** cards
- **Normal queue** management
- **Priority queue** handling
- **Action buttons** for queue control

### 3. Public Queue Display (`/public-queue-display`)
- **No authentication** required
- **Department selection** toggle
- **Current queue** display
- **Wait time** estimates
- **Auto-refresh** every 10 seconds

## 🔄 Queue Logic

### FIFO Implementation
1. **First In, First Out** for normal queue
2. **Priority handling** for special cases
3. **Automatic position** calculation
4. **Queue reordering** when patients leave

### Wait Time Calculation
```python
def get_estimated_wait_time(self):
    # Calculate average service time from completed queues
    # Count patients ahead in queue
    # Return estimated wait time
```

### Queue Status Flow
```
waiting → in_progress → completed
    ↓
cancelled
```

## 🔐 Security Features

### Authentication
- **JWT token** based authentication
- **Role-based** access control
- **Secure API** endpoints

### Authorization
- **Patient endpoints** - Patient role only
- **Staff endpoints** - Nurse/Doctor roles only
- **Public endpoints** - No authentication required

## 📱 Mobile Responsiveness

- **Mobile-first** design approach
- **Touch-friendly** interface
- **Responsive** grid layouts
- **Optimized** for small screens

## 🚀 Getting Started

### Backend Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Start server**:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

## 📊 Usage Examples

### Patient Check-in
1. Navigate to `/patient-queue`
2. Select department (OPD, Billing, etc.)
3. Optionally enter appointment ID
4. Select priority level if applicable
5. Click "Check In" button
6. Receive queue number and position

### Staff Queue Management
1. Navigate to `/staff-queue-dashboard`
2. Select department to manage
3. View current queue and statistics
4. Click "Call Next Patient" to call next in line
5. Mark service as completed when done
6. Remove patients if necessary

### Public Queue Display
1. Navigate to `/public-queue-display`
2. Select department to view
3. See current queue status
4. View estimated wait times
5. No login required

## 🔧 Configuration

### Auto-refresh Intervals
- **Patient page**: 10 seconds
- **Staff dashboard**: 5 seconds
- **Public display**: 10 seconds

### Queue Settings
- **Default departments**: OPD, Billing, Pharmacy, Appointment
- **Priority levels**: Normal, Senior Citizen, PWD
- **Status options**: Waiting, In Progress, Completed, Cancelled

## 🐛 Troubleshooting

### Common Issues
1. **Queue not updating**: Check auto-refresh settings
2. **Authentication errors**: Verify JWT token validity
3. **Permission denied**: Check user role permissions
4. **Queue position errors**: Verify FIFO logic implementation

### Debug Mode
Enable debug logging in Django settings:
```python
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 🚀 Future Enhancements

### Planned Features
1. **WebSocket integration** for real-time updates
2. **SMS notifications** for patients
3. **Queue analytics** and reporting
4. **Mobile app** integration
5. **Voice announcements** system
6. **Queue prediction** algorithms

### Performance Optimizations
1. **Database indexing** for faster queries
2. **Caching** for frequently accessed data
3. **API rate limiting** for security
4. **Background tasks** for heavy operations

## 📞 Support

For technical support or questions about the Patient Queuing Management System:

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs through the project issue tracker
- **Features**: Request new features through the project repository

## 📄 License

This project is part of the MediSync Healthcare Management System and follows the same licensing terms as the main project.

---

**Built with ❤️ for MediSync Hospital**
