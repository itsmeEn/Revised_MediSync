# Predictive Analytics Frontend

A comprehensive frontend implementation for role-based predictive analytics with the same design structure as the existing dashboards.

## 🎯 **Analytics Pages**

### **DoctorPredictiveAnalytics.vue**
**Route**: `/doctor-predictive-analytics`

**Features**:
- **Same Design Structure** - Identical to DoctorDashboard.vue
- **Doctor-Specific Analytics** - Patient demographics, illness prediction, health trends, surge prediction
- **Real-time Data** - Live analytics updates
- **PDF Report Generation** - Download comprehensive reports
- **Interactive Cards** - Clickable analytics cards with hover effects

### **NurseAnalytics.vue**
**Route**: `/nurse-analytics`

**Features**:
- **Same Design Structure** - Identical to NurseDashboard.vue
- **Nurse-Specific Analytics** - Medication analysis, patient demographics, health trends, volume prediction
- **Real-time Data** - Live analytics updates
- **PDF Report Generation** - Download comprehensive reports
- **Interactive Cards** - Clickable analytics cards with hover effects

## 🎨 **Design Features**

### **Consistent UI/UX**:
- **Glassmorphism Design** - Same backdrop blur and transparency effects
- **Color Scheme** - Matching the existing dashboard colors (#286660, #4a7c59)
- **Typography** - Consistent font sizes and weights
- **Spacing** - Same padding and margins as existing dashboards
- **Responsive Design** - Mobile-first approach with breakpoints

### **Header Section**:
- **Search Bar** - "Search Analytics, Reports and Insights"
- **Time Display** - Real-time clock with 12-hour format
- **Weather Widget** - Temperature and location display
- **Notifications** - Badge with notification count

### **Sidebar Navigation**:
- **User Profile** - Profile picture, name, role, verification status
- **Navigation Menu** - Role-specific menu items
- **Active State** - Analytics page highlighted
- **Logout Button** - Consistent styling

### **Main Content**:
- **Greeting Section** - Personalized welcome message
- **Analytics Cards** - 4 interactive cards with hover effects
- **Data Panels** - 2x2 grid layout for analytics data
- **Action Buttons** - PDF generation and data refresh

## 📊 **Analytics Cards**

### **Doctor Analytics Cards**:
1. **Patient Demographics** - Age and gender distribution
2. **Illness Prediction** - Statistical analysis and disease patterns
3. **Health Trends** - Top medical conditions and patterns
4. **Surge Prediction** - Forecast illness outbreaks and capacity

### **Nurse Analytics Cards**:
1. **Medication Analysis** - Most prescribed medications and patterns
2. **Patient Demographics** - Age and gender distribution
3. **Health Trends** - Top medical conditions and patterns
4. **Volume Prediction** - Forecast patient volume and workload

## 🔧 **Technical Implementation**

### **Vue 3 Composition API**:
```typescript
// Reactive data
const analyticsData = ref({
  patient_demographics: null,
  illness_prediction: null,
  health_trends: null,
  surge_prediction: null
})

// Computed properties
const userInitials = computed(() => {
  if (!userProfile.value.full_name) return 'U'
  return userProfile.value.full_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
})
```

### **API Integration**:
```typescript
// Fetch doctor analytics
const fetchDoctorAnalytics = async () => {
  try {
    const response = await api.get('/analytics/doctor/')
    analyticsData.value = response.data.data
  } catch (error) {
    console.error('Failed to fetch doctor analytics:', error)
  }
}

// Generate PDF report
const generatePDFReport = async () => {
  try {
    const response = await api.get('/analytics/pdf/?type=doctor', {
      responseType: 'blob'
    })
    
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `doctor_analytics_report_${new Date().toISOString().split('T')[0]}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Failed to generate PDF report:', error)
  }
}
```

### **Real-time Features**:
```typescript
// Time update
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', { 
    hour12: true, 
    hour: 'numeric', 
    minute: '2-digit', 
    second: '2-digit' 
  })
}

// Weather data
const fetchWeatherData = async () => {
  weatherLoading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    weatherData.value = {
      temperature: 28,
      condition: 'sunny',
      location: 'Mandaluyong City'
    }
  } catch (error) {
    weatherError.value = true
  } finally {
    weatherLoading.value = false
  }
}
```

## 🎨 **Styling Features**

### **Glassmorphism Effects**:
```css
.dashboard-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  background: rgba(255, 255, 255, 0.35);
}
```

### **Card-Specific Colors**:
```css
/* Doctor Analytics */
.demographics-card .card-icon { color: #2196f3; }
.prediction-card .card-icon { color: #ff9800; }
.trends-card .card-icon { color: #4caf50; }
.surge-card .card-icon { color: #f44336; }

/* Nurse Analytics */
.medication-card .card-icon { color: #9c27b0; }
.demographics-card .card-icon { color: #2196f3; }
.trends-card .card-icon { color: #4caf50; }
.volume-card .card-icon { color: #ff9800; }
```

### **Responsive Design**:
```css
@media (max-width: 768px) {
  .dashboard-cards-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .analytics-panels-container {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .dashboard-cards-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
```

## 📱 **Responsive Breakpoints**

### **Desktop (1200px+)**:
- 4-column grid for analytics cards
- 2x2 grid for analytics panels
- Full sidebar navigation
- Complete header with all elements

### **Tablet (768px - 1199px)**:
- 2-column grid for analytics cards
- Single column for analytics panels
- Collapsible sidebar
- Condensed header elements

### **Mobile (480px - 767px)**:
- Single column layout
- Stacked analytics panels
- Overlay sidebar
- Minimal header with essential elements

### **Small Mobile (< 480px)**:
- Single column everything
- Touch-friendly buttons
- Optimized spacing
- Essential content only

## 🔄 **Navigation Flow**

### **Doctor Navigation**:
```
Doctor Dashboard → Analytics → Doctor Predictive Analytics
```

### **Nurse Navigation**:
```
Nurse Dashboard → Analytics → Nurse Analytics
```

### **Router Configuration**:
```typescript
{
  path: '/doctor-predictive-analytics',
  name: 'DoctorPredictiveAnalytics',
  component: () => import('pages/DoctorPredictiveAnalytics.vue')
},
{
  path: '/nurse-analytics',
  component: () => import('pages/NurseAnalytics.vue')
}
```

## 🎯 **User Experience**

### **Loading States**:
- **Profile Loading** - "Loading..." placeholders
- **Weather Loading** - Spinner with "Loading weather..."
- **Data Loading** - Empty state messages
- **Error Handling** - User-friendly error messages

### **Interactive Elements**:
- **Hover Effects** - Cards lift and glow on hover
- **Click Feedback** - Toast notifications for actions
- **Smooth Transitions** - 0.3s ease transitions
- **Visual Feedback** - Color changes and animations

### **Accessibility**:
- **Keyboard Navigation** - Tab-friendly interface
- **Screen Reader Support** - Proper ARIA labels
- **Color Contrast** - WCAG compliant colors
- **Focus Indicators** - Clear focus states

## 🚀 **Performance Features**

### **Optimized Loading**:
- **Lazy Loading** - Components loaded on demand
- **Image Optimization** - Compressed profile pictures
- **API Caching** - Reduced redundant requests
- **Efficient Updates** - Minimal re-renders

### **Real-time Updates**:
- **Time Updates** - Every second
- **Weather Updates** - Periodic refresh
- **Analytics Updates** - On-demand refresh
- **Profile Updates** - Real-time sync

## 📋 **Data Display**

### **Analytics Panels**:
- **Structured Data** - Organized information display
- **Empty States** - "No data available" messages
- **Loading States** - Spinner indicators
- **Error States** - Error message display

### **Data Formatting**:
- **Numbers** - Proper formatting with commas
- **Percentages** - Rounded to 2 decimal places
- **Dates** - User-friendly date formats
- **Categories** - Clear labeling and grouping

## 🔧 **Development Setup**

### **Prerequisites**:
- Node.js 18+
- Vue 3 with Composition API
- Quasar Framework
- TypeScript support

### **Installation**:
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### **File Structure**:
```
frontend/src/pages/
├── DoctorPredictiveAnalytics.vue
├── NurseAnalytics.vue
└── ... (other pages)

frontend/src/router/
└── routes.ts (updated with new routes)
```

## 🎨 **Customization**

### **Adding New Analytics Types**:
1. Add new card to dashboard
2. Add new panel to analytics section
3. Update API calls
4. Add new styling

### **Modifying Colors**:
1. Update CSS custom properties
2. Modify card-specific colors
3. Update hover effects
4. Test accessibility

### **Adding New Features**:
1. Create new Vue component
2. Add to router configuration
3. Update navigation
4. Add styling

## 📚 **Best Practices**

### **Code Organization**:
- **Single Responsibility** - Each function has one purpose
- **Composition API** - Use reactive and computed
- **TypeScript** - Strong typing for better development
- **Error Handling** - Comprehensive error management

### **Performance**:
- **Lazy Loading** - Load components when needed
- **Memoization** - Cache expensive computations
- **Debouncing** - Limit API calls
- **Optimization** - Minimize bundle size

### **Accessibility**:
- **Semantic HTML** - Proper element usage
- **ARIA Labels** - Screen reader support
- **Keyboard Navigation** - Full keyboard support
- **Color Contrast** - WCAG compliance

## 🤝 **Support**

For issues or questions:
1. Check the browser console for errors
2. Verify API endpoints are working
3. Test with different user roles
4. Check network connectivity and API responses

## 📈 **Future Enhancements**

### **Planned Features**:
- **Real-time Charts** - Interactive data visualization
- **Export Options** - Multiple export formats
- **Custom Dashboards** - User-configurable layouts
- **Advanced Filtering** - Date range and category filters

### **Performance Improvements**:
- **Virtual Scrolling** - For large datasets
- **Web Workers** - Background processing
- **Service Workers** - Offline support
- **Caching Strategies** - Improved data caching
