# Role-Based Analytics System

A comprehensive analytics system with specialized endpoints for doctors and nurses, including PDF report generation.

## 🎯 **Role-Specific Analytics**

### **Doctor Analytics** (`/api/analytics/doctor/`)
**Access**: Doctors only

**Analytics Included**:
- **Patient Demographics** - Age and gender distribution
- **Illness Prediction** - Chi-square statistical analysis
- **Health Trends** - Top medical conditions by week
- **Surge Prediction** - Illness surge forecasting

**Key Features**:
- Specialized for clinical decision-making
- Focus on patient outcomes and disease patterns
- Predictive models for patient care planning

### **Nurse Analytics** (`/api/analytics/nurse/`)
**Access**: Nurses only

**Analytics Included**:
- **Medication Analysis** - Most prescribed medications (Pareto analysis)
- **Patient Demographics** - Age and gender distribution
- **Health Trends** - Top medical conditions by week
- **Volume Prediction** - Patient volume forecasting

**Key Features**:
- Focused on medication management
- Patient care coordination insights
- Resource planning and workload management

## 📊 **PDF Report Generation**

### **Endpoint**: `/api/analytics/pdf/`

**Features**:
- **Professional Formatting** - Clean, medical-grade reports
- **Role-Specific Content** - Different reports for doctors vs nurses
- **Comprehensive Sections** - All analytics findings with headings
- **Timestamps** - Report generation date and time
- **Downloadable** - Direct PDF download

### **Report Types**:

#### **Doctor Report** (`?type=doctor`)
```
1. Patient Demographics
   - Age Distribution
   - Gender Distribution

2. Patient Health Trends
   - Top Medical Conditions by Week

3. Illness Prediction Analysis
   - Statistical Analysis Results
   - Chi-Square Statistics
   - P-Values

4. Illness Surge Prediction
   - Forecasted Cases for Next 6 Months

5. Summary
```

#### **Nurse Report** (`?type=nurse`)
```
1. Patient Demographics
   - Age Distribution
   - Gender Distribution

2. Patient Health Trends
   - Top Medical Conditions by Week

3. Medication Analysis
   - Most Prescribed Medications
   - Prescription Frequency

4. Patient Volume Prediction
   - Model Performance Metrics
   - Forecasting Accuracy

5. Summary
```

#### **Full Report** (`?type=full`)
```
1. Patient Demographics
2. Patient Health Trends
3. Medication Analysis
4. Illness Prediction Analysis
5. Patient Volume Prediction
6. Illness Surge Prediction
7. Summary
```

## 🔧 **API Usage Examples**

### **Get Doctor Analytics**
```bash
curl -X GET http://localhost:8000/api/analytics/doctor/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response**:
```json
{
  "success": true,
  "message": "Doctor analytics retrieved successfully",
  "data": {
    "patient_demographics": {...},
    "illness_prediction": {...},
    "health_trends": {...},
    "surge_prediction": {...},
    "doctor_name": "Dr. John Smith",
    "specialization": "Cardiology",
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

### **Get Nurse Analytics**
```bash
curl -X GET http://localhost:8000/api/analytics/nurse/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### **Generate PDF Report**
```bash
# Doctor-specific report
curl -X GET "http://localhost:8000/api/analytics/pdf/?type=doctor" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  --output "doctor_analytics_report.pdf"

# Nurse-specific report
curl -X GET "http://localhost:8000/api/analytics/pdf/?type=nurse" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  --output "nurse_analytics_report.pdf"

# Full analytics report
curl -X GET "http://localhost:8000/api/analytics/pdf/?type=full" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  --output "full_analytics_report.pdf"
```

## 🎨 **PDF Report Features**

### **Professional Styling**:
- **Header**: Role-specific title with user name
- **Metadata**: Generation timestamp
- **Sections**: Numbered sections with clear headings
- **Subsections**: Color-coded subsections
- **Content**: Bullet points and structured data
- **Summary**: Comprehensive conclusion

### **Color Scheme**:
- **Section Headers**: Dark Blue
- **Subsections**: Dark Green
- **Content**: Black
- **Metadata**: Grey

### **Layout**:
- **Page Size**: A4
- **Margins**: Standard document margins
- **Spacing**: Professional spacing between sections
- **Fonts**: Clean, readable fonts

## 🔒 **Security & Access Control**

### **Role-Based Access**:
- **Doctor Analytics**: Only accessible by users with `role='doctor'`
- **Nurse Analytics**: Only accessible by users with `role='nurse'`
- **PDF Reports**: Role-specific content based on user role
- **Authentication**: JWT token required for all endpoints

### **Error Handling**:
- **403 Forbidden**: When wrong role tries to access endpoint
- **503 Service Unavailable**: When PDF generation is not available
- **500 Internal Server Error**: For other server errors

## 📈 **Analytics Data Structure**

### **Patient Demographics**:
```json
{
  "age_distribution": {
    "20-39": 150,
    "40-59": 200,
    "60-79": 180,
    "80+": 70
  },
  "gender_proportions": {
    "Male": 45.2,
    "Female": 54.8
  }
}
```

### **Health Trends**:
```json
{
  "top_illnesses_by_week": [
    {
      "medical_condition": "Hypertension",
      "count": 25,
      "date_of_admission": "2024-01-15"
    }
  ]
}
```

### **Medication Analysis**:
```json
{
  "medication_pareto_data": [
    {
      "medication": "Aspirin",
      "frequency": 150,
      "cumulative_percentage": 25.5
    }
  ]
}
```

## 🚀 **Setup Instructions**

### **1. Install Dependencies**
```bash
pip install reportlab==4.0.7
```

### **2. Run Migrations**
```bash
python manage.py migrate
```

### **3. Test Endpoints**
```bash
# Test doctor analytics
curl -X GET http://localhost:8000/api/analytics/doctor/ \
  -H "Authorization: Bearer DOCTOR_JWT_TOKEN"

# Test nurse analytics
curl -X GET http://localhost:8000/api/analytics/nurse/ \
  -H "Authorization: Bearer NURSE_JWT_TOKEN"

# Test PDF generation
curl -X GET http://localhost:8000/api/analytics/pdf/?type=doctor \
  -H "Authorization: Bearer DOCTOR_JWT_TOKEN" \
  --output "report.pdf"
```

## 📋 **Frontend Integration**

### **Doctor Dashboard**:
```javascript
// Fetch doctor analytics
const fetchDoctorAnalytics = async () => {
  const response = await fetch('/api/analytics/doctor/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  return data.data;
};

// Generate PDF report
const generatePDF = async () => {
  const response = await fetch('/api/analytics/pdf/?type=doctor', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'doctor_analytics_report.pdf';
  a.click();
};
```

### **Nurse Dashboard**:
```javascript
// Fetch nurse analytics
const fetchNurseAnalytics = async () => {
  const response = await fetch('/api/analytics/nurse/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const data = await response.json();
  return data.data;
};
```

## 🎯 **Use Cases**

### **For Doctors**:
- **Clinical Decision Making**: Use illness prediction data for treatment planning
- **Patient Care**: Monitor health trends and patient demographics
- **Resource Planning**: Use surge prediction for capacity planning
- **Research**: Generate reports for medical research and presentations

### **For Nurses**:
- **Medication Management**: Track most prescribed medications
- **Patient Care**: Monitor patient demographics and health trends
- **Workload Planning**: Use volume prediction for staffing
- **Quality Improvement**: Generate reports for care quality assessment

### **For Administrators**:
- **Full Analytics**: Access comprehensive analytics across all departments
- **Reporting**: Generate full reports for management and stakeholders
- **Monitoring**: Track system-wide health trends and patterns

## 🔧 **Customization**

### **Adding New Analytics Types**:
1. Add new analysis type to `AnalyticsResult.ANALYSIS_TYPES`
2. Update role-specific endpoints to include new analytics
3. Add new section to PDF report generation
4. Update frontend to display new analytics

### **Customizing PDF Reports**:
1. Modify `add_analytics_sections()` function
2. Add new sections or modify existing ones
3. Customize styling and formatting
4. Add custom headers and footers

## 📚 **Additional Resources**

- [ReportLab Documentation](https://docs.reportlab.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Role-Based Access Control](https://docs.djangoproject.com/en/stable/topics/auth/customizing/)

## 🤝 **Support**

For issues or questions:
1. Check the API response for error messages
2. Verify user role and permissions
3. Ensure all dependencies are installed
4. Check server logs for detailed error information
