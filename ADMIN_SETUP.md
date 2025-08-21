# 🚀 MediSync Admin Site - Complete Setup Guide

## 📋 **Quick Start (Recommended)**

### **Option 1: Use the Startup Script (Easiest)**
```bash
# Make sure you're in the project root directory
cd /Users/judeibardaloza/Desktop/medisync

# Run the startup script
./start_admin.sh
```

This will automatically:
- ✅ Check if ports are available
- ✅ Start the backend server on port 8001
- ✅ Start the frontend server on port 8080
- ✅ Display login credentials
- ✅ Handle cleanup when you stop the servers

### **Option 2: Manual Setup**

#### **Step 1: Start Backend Server**
```bash
# Activate virtual environment
source /Users/judeibardaloza/.local/share/virtualenvs/medisync-WHaJ4sn5/bin/activate

# Start Django server
python manage.py runserver 8001
```

#### **Step 2: Start Frontend Server (New Terminal)**
```bash
# Navigate to admin frontend directory
cd admin-frontend

# Start HTTP server
python -m http.server 8080
```

## 🌐 **Access the Admin Site**

### **Admin Dashboard**
- **URL**: http://localhost:8080
- **Login Email**: admin@medisync.com
- **Login Password**: admin123456

### **Backend API**
- **Base URL**: http://localhost:8001/api/admin/
- **Documentation**: Available at the endpoints below

## 🔧 **Initial Setup (One-time only)**

### **1. Database Setup**
```bash
# Create migrations
python manage.py makemigrations admin_site

# Apply migrations
python manage.py migrate
```

### **2. Create Admin User**
```bash
# Run the admin creation script
python create_admin.py
```

**Default credentials:**
- Email: admin@medisync.com
- Password: admin123456
- Full Name: Admin User
- Super Admin: Yes

## 📊 **Admin Dashboard Features**

### **Dashboard Overview**
- 📈 **Statistics Cards**: Pending, Approved, Declined, Archived counts
- 🔍 **Search & Filter**: Filter by status, search by name/email
- 📋 **Verification Table**: All verification requests with actions

### **Verification Management**
- ✅ **Accept**: Approve verification and send email notification
- ❌ **Decline**: Decline with reason and optional email notification
- 👁️ **View**: Open document viewer for uploaded files
- 📦 **Archive**: Archive old verification requests

### **Email Notifications**
- **Automatic emails** sent to users when verifications are processed
- **Customizable** - admin can choose to send/not send emails
- **Professional templates** with clear instructions

## 🔌 **API Endpoints**

### **Authentication**
- `POST /api/admin/login/` - Admin login

### **Dashboard**
- `GET /api/admin/dashboard/stats/` - Get statistics

### **Verification Management**
- `GET /api/admin/verifications/` - List all verifications
- `POST /api/admin/verifications/{id}/accept/` - Accept verification
- `POST /api/admin/verifications/{id}/decline/` - Decline verification
- `POST /api/admin/verifications/{id}/archive/` - Archive verification
- `PUT /api/admin/verifications/{id}/update/` - Update verification

### **System Logs**
- `GET /api/admin/logs/` - Get audit logs (Super Admin only)

## 🛠️ **Troubleshooting**

### **Port Already in Use**
```bash
# Check what's using the port
lsof -i :8001
lsof -i :8080

# Kill the process
kill -9 <PID>
```

### **Database Issues**
```bash
# Reset migrations (if needed)
python manage.py migrate admin_site zero
python manage.py makemigrations admin_site
python manage.py migrate
```

### **Admin User Issues**
```bash
# Create new admin user
python create_admin.py

# Or create via Django shell
python manage.py shell
```
```python
from admin_site.models import AdminUser
admin = AdminUser.objects.create_user(
    email='newadmin@medisync.com',
    password='newpassword123',
    full_name='New Admin User',
    is_super_admin=True
)
```

### **CORS Issues**
Make sure your Django settings include:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
```

## 📁 **File Structure**

```
medisync/
├── admin_site/                 # Django admin app
│   ├── models.py              # AdminUser, VerificationRequest models
│   ├── views.py               # API endpoints
│   ├── serializers.py         # Data serialization
│   └── urls.py                # URL routing
├── admin-frontend/            # Frontend files
│   ├── index.html             # Main dashboard page
│   ├── admin.js               # JavaScript functionality
│   └── README.md              # Frontend documentation
├── create_admin.py            # Admin user creation script
├── start_admin.sh             # Startup script
└── ADMIN_SETUP.md             # This file
```

## 🔒 **Security Features**

- **JWT Authentication**: Secure token-based authentication
- **Role-based Access**: Admin vs Super Admin permissions
- **Audit Logging**: All actions logged for compliance
- **Input Validation**: Proper validation for all inputs
- **CORS Protection**: Configured for security

## 📧 **Email Configuration**

### **Environment Variables**
```bash
export DEFAULT_FROM_EMAIL="noreply@medisync.com"
export EMAIL_HOST="smtp.gmail.com"
export EMAIL_PORT="587"
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-app-password"
```

### **Test Email Setup**
```bash
# Test email configuration
python manage.py shell
```
```python
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email from MediSync Admin.',
    'noreply@medisync.com',
    ['test@example.com'],
    fail_silently=False,
)
```

## 🚀 **Production Deployment**

### **Backend (Django)**
- Use Gunicorn or uWSGI
- Configure with Nginx
- Set up SSL certificates
- Use environment variables for sensitive data

### **Frontend**
- Serve static files with Nginx
- Configure CORS for production domain
- Set up SSL certificates
- Use CDN for better performance

## 📞 **Support**

If you encounter any issues:

1. **Check the logs** in the terminal where servers are running
2. **Verify ports** are not in use by other services
3. **Check database** migrations are applied
4. **Verify admin user** exists and credentials are correct
5. **Test API endpoints** directly with curl or Postman

## 🎯 **Next Steps**

1. **Test the admin dashboard** with the provided credentials
2. **Upload test verification documents** from the main MediSync app
3. **Process verifications** through the admin interface
4. **Configure email settings** for production use
5. **Set up monitoring** and logging for production deployment

---

**🎉 You're all set! The MediSync Admin Site is now running and ready to manage user verifications.**
