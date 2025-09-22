# MediSync Analytics System

A comprehensive asynchronous analytics system for continuous integration and real-time predictive analytics.

## 🚀 Features

- **Continuous Integration**: Automatically triggers analytics when new data is added
- **Asynchronous Processing**: Uses Celery for background processing to prevent app crashes
- **Real-time Updates**: WebSocket-like streaming for live analytics
- **Predictive Analytics**: SARIMA models for patient volume and illness surge prediction
- **Caching**: Redis-based caching for performance optimization
- **Scheduled Tasks**: Automatic cleanup and cache refresh

## 📊 Analytics Types

1. **Patient Health Trends** - Top 5 medical conditions per week
2. **Patient Demographics** - Age and gender distribution analysis
3. **Illness Prediction** - Chi-square test for illness prediction
4. **Medication Analysis** - Pareto analysis of prescribed medications
5. **Patient Volume Prediction** - SARIMA forecasting of patient volumes
6. **Illness Surge Prediction** - Predictive modeling for illness surges

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements_analytics.txt
```

### 2. Install and Start Redis

```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server
```

### 3. Run Migrations

```bash
python manage.py makemigrations analytics
python manage.py migrate
```

### 4. Populate Healthcare Data

```bash
python manage.py populate_healthcare_data /path/to/healthcare_dataset.csv
```

### 5. Start the Analytics System

```bash
./start_analytics.sh
```

## 🔧 API Endpoints

### Analytics API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/` | Get analytics results |
| POST | `/api/analytics/` | Trigger new analysis |
| GET | `/api/analytics/status/{task_id}/` | Check task status |
| GET | `/api/analytics/history/` | Get analytics history |
| POST | `/api/analytics/refresh/` | Trigger data refresh |
| GET | `/api/analytics/realtime/` | Real-time analytics dashboard |
| GET | `/api/analytics/stream/` | Real-time analytics stream |

### Example Usage

#### Trigger Analytics
```bash
curl -X POST http://localhost:8000/api/analytics/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"analysis_type": "full_analysis", "force_refresh": false}'
```

#### Get Analytics Results
```bash
curl -X GET http://localhost:8000/api/analytics/?type=patient_demographics \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Check Task Status
```bash
curl -X GET http://localhost:8000/api/analytics/status/TASK_ID/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔄 Continuous Integration

The system automatically triggers analytics when:

- New patient profiles are created
- Patient profiles are updated
- Patient profiles are deleted

### Signal Handlers

```python
# Automatically triggered on data changes
@receiver(post_save, sender=PatientProfile)
def patient_profile_saved(sender, instance, created, **kwargs):
    # Triggers analytics processing
    process_data_update_analytics.delay(...)
```

## 📈 Real-time Analytics

### WebSocket Streaming
```javascript
// Connect to real-time analytics stream
const eventSource = new EventSource('/api/analytics/stream/');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Analytics update:', data);
};
```

### Dashboard Integration
```javascript
// Get real-time dashboard data
fetch('/api/analytics/realtime/', {
    headers: {
        'Authorization': 'Bearer YOUR_JWT_TOKEN'
    }
})
.then(response => response.json())
.then(data => {
    // Update dashboard with analytics data
    updateDashboard(data.data);
});
```

## 🔧 Configuration

### Celery Configuration
```python
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'UTC'
```

### Scheduled Tasks
- **Hourly**: Full analytics refresh
- **Daily**: Cleanup old analytics data
- **Every 30 minutes**: Cache refresh

## 📊 Analytics Models

### AnalyticsResult
Stores completed analytics results with JSON data.

### AnalyticsTask
Tracks background processing tasks.

### DataUpdateLog
Logs data changes that trigger analytics.

### AnalyticsCache
Caches frequently accessed results.

## 🚨 Error Handling

- **Retry Logic**: Failed tasks are retried with exponential backoff
- **Error Logging**: Comprehensive error logging and monitoring
- **Graceful Degradation**: System continues to function even if analytics fail

## 📝 Monitoring

### Task Monitoring
```bash
# Check Celery worker status
celery -A backend inspect active

# Check scheduled tasks
celery -A backend inspect scheduled
```

### Analytics Status
```bash
# Check analytics results
python manage.py shell
>>> from backend.analytics.models import AnalyticsResult
>>> AnalyticsResult.objects.filter(status='completed').count()
```

## 🔒 Security

- **Authentication Required**: All endpoints require JWT authentication
- **Role-based Access**: Analytics endpoints restricted to authenticated users
- **Data Validation**: Input validation and sanitization

## 🚀 Production Deployment

### Environment Variables
```bash
export CELERY_BROKER_URL=redis://your-redis-server:6379/0
export CELERY_RESULT_BACKEND=redis://your-redis-server:6379/0
export REDIS_URL=redis://your-redis-server:6379/1
```

### Supervisor Configuration
```ini
[program:celery-worker]
command=celery -A backend worker --loglevel=info
directory=/path/to/medisync
user=www-data
autostart=true
autorestart=true

[program:celery-beat]
command=celery -A backend beat --loglevel=info
directory=/path/to/medisync
user=www-data
autostart=true
autorestart=true
```

## 🐛 Troubleshooting

### Common Issues

1. **Redis Connection Error**
   ```bash
   # Check Redis status
   redis-cli ping
   ```

2. **Celery Worker Not Starting**
   ```bash
   # Check Celery logs
   celery -A backend worker --loglevel=debug
   ```

3. **Analytics Not Triggering**
   ```bash
   # Check signal handlers
   python manage.py shell
   >>> from backend.analytics.signals import *
   ```

## 📚 Additional Resources

- [Celery Documentation](https://docs.celeryproject.org/)
- [Redis Documentation](https://redis.io/documentation)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Statsmodels Documentation](https://www.statsmodels.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
