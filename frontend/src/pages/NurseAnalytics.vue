<template>
  <q-layout view="hHh Lpr fFf">

    <q-header elevated class="prototype-header">
      <q-toolbar class="header-toolbar">
        <!-- Menu button to open sidebar -->
        <q-btn dense flat round icon="menu" @click="toggleRightDrawer" class="menu-toggle-btn" />
        
        <!-- Left side - Search bar -->
        <div class="header-left">
        <div class="search-container">
          <q-input 
            outlined
            dense
            v-model="text" 
              placeholder="Search Patient, symptoms and Appointments"
            class="search-input"
              bg-color="white"
            >
              <template v-slot:prepend>
                <q-icon name="search" color="grey-6" />
              </template>
              <template v-slot:append v-if="text">
                <q-icon name="clear" class="cursor-pointer" @click="text = ''" />
            </template>
          </q-input>
        </div>
      </div>
        
        <!-- Right side - Notifications, Time, Weather -->
        <div class="header-right">
          <!-- Notifications -->
          <q-btn flat round icon="notifications" class="notification-btn">
            <q-badge color="red" floating>1</q-badge>
          </q-btn>
          
          <!-- Time Display -->
          <div class="time-display">
            <q-icon name="schedule" size="md" />
            <span class="time-text">{{ currentTime }}</span>
          </div>
          
          <!-- Weather Display -->
          <div class="weather-display" v-if="weatherData">
            <q-icon :name="getWeatherIcon(weatherData.condition)" size="sm" />
            <span class="weather-text">{{ weatherData.temperature }}°C</span>
            <span class="weather-location">{{ weatherData.location }}</span>
          </div>
          
          <!-- Loading Weather -->
          <div class="weather-loading" v-else-if="weatherLoading">
            <q-spinner size="sm" />
            <span class="weather-text">Loading weather...</span>
          </div>
          
          <!-- Weather Error -->
          <div class="weather-error" v-else-if="weatherError">
            <q-icon name="error" size="sm" />
            <span class="weather-text">Weather Update and Place</span>
          </div>
              </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="rightDrawerOpen" side="left" overlay bordered class="prototype-sidebar" :width="280">
      <div class="sidebar-content">
        <!-- Logo Section -->
        <div class="logo-section">
          <div class="logo-container">
            <q-avatar size="40px" class="logo-avatar">
              <img src="../assets/logo.png" alt="MediSync Logo" />
            </q-avatar>
            <span class="logo-text">MediSync</span>
              </div>
          <q-btn dense flat round icon="menu" @click="toggleRightDrawer" class="menu-btn" />
              </div>

        <!-- User Profile Section - Centered -->
        <div class="sidebar-user-profile-centered">
          <div class="profile-picture-container">
            <q-avatar size="80px" class="profile-avatar">
              <img v-if="profilePictureUrl" :src="profilePictureUrl" alt="Profile Picture" />
              <div v-else class="profile-placeholder">
                {{ userInitials }}
              </div>
            </q-avatar>
            <q-btn
              round
              color="primary"
              icon="camera_alt"
              size="sm"
              class="upload-btn"
              @click="triggerFileUpload"
            />
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              style="display: none"
              @change="handleProfilePictureUpload"
            />
              </div>
          
          <div class="user-info">
            <h6 class="user-name">{{ userProfile?.first_name }} {{ userProfile?.last_name }}</h6>
            <p class="user-role">Nurse</p>
            <q-chip 
              :color="userProfile?.verification_status === 'verified' ? 'green' : 'orange'"
              text-color="white"
              size="sm"
              :label="userProfile?.verification_status === 'verified' ? 'Verified' : 'Pending'"
            />
        </div>
      </div>

        <!-- Navigation Menu -->
        <q-list class="navigation-menu">
          <q-item clickable v-ripple @click="navigateTo('nurse-dashboard')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="grid_view" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('nurse-medicine-inventory')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="medication" />
            </q-item-section>
            <q-item-section>Medicine Inventory</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('patient-assessment')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="assignment" />
            </q-item-section>
            <q-item-section>Patient Assessment</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('patients')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>
            <q-item-section>Patient Management</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('nurse-analytics')" class="nav-item active">
            <q-item-section avatar>
              <q-icon name="analytics" />
            </q-item-section>
            <q-item-section>Analytics</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('nurse-settings')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>
            <q-item-section>Settings</q-item-section>
          </q-item>
        </q-list>

        <!-- Logout Section - Footer -->
        <div class="sidebar-footer">
          <q-btn
            color="negative"
            icon="logout"
            label="Logout"
            class="logout-btn"
            @click="logout"
          />
                </div>
      </div>
    </q-drawer>

    <q-page-container class="page-container-with-fixed-header">
      <!-- Greeting Section -->
      <div class="greeting-section">
        <q-card class="greeting-card">
          <q-card-section class="greeting-content">
          <h2 class="greeting-text">
              Nurse Analytics Dashboard, {{ userProfile.role.charAt(0).toUpperCase() + userProfile.role.slice(1) }} {{ userProfile.full_name }}
          </h2>
            <p class="greeting-subtitle">Data-driven insights for patient care and medication management - {{ currentDate }}</p>
              </q-card-section>
            </q-card>
          </div>

      <!-- Analytics Cards Section -->
      <div class="dashboard-cards-section">
        <div class="dashboard-cards-grid">
          <!-- Medication Analysis Card -->
          <q-card class="dashboard-card medication-card" @click="viewMedicationAnalysis">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Medication Analysis</div>
                <div class="card-description">Most prescribed medications and patterns</div>
              </div>
              <div class="card-icon">
                <q-icon name="medication" size="2.5rem" />
                </div>
              </q-card-section>
            </q-card>

          <!-- Patient Demographics Card -->
          <q-card class="dashboard-card demographics-card" @click="viewDemographics">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Patient Demographics</div>
                <div class="card-description">Age distribution and gender analysis</div>
              </div>
              <div class="card-icon">
                <q-icon name="people" size="2.5rem" />
                </div>
              </q-card-section>
            </q-card>

          <!-- Health Trends Card -->
          <q-card class="dashboard-card trends-card" @click="viewHealthTrends">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Health Trends</div>
                <div class="card-description">Top medical conditions and patterns</div>
              </div>
              <div class="card-icon">
                <q-icon name="trending_up" size="2.5rem" />
                </div>
              </q-card-section>
            </q-card>

          <!-- Volume Prediction Card -->
          <q-card class="dashboard-card volume-card" @click="viewVolumePrediction">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Volume Prediction</div>
                <div class="card-description">Forecast patient volume and workload</div>
          </div>
              <div class="card-icon">
                <q-icon name="timeline" size="2.5rem" />
        </div>
              </q-card-section>
            </q-card>
        </div>
          </div>

      <!-- Analytics Data Display Section -->
      <div class="analytics-section">
        <q-card class="analytics-card">
          <q-card-section class="analytics-header">
            <h3 class="analytics-title">NURSE ANALYTICS INSIGHTS</h3>
            <div class="analytics-actions">
              <q-btn
                color="primary"
                label="Generate PDF Report"
                icon="picture_as_pdf"
                size="md"
                @click="generatePDFReport"
                class="action-btn"
              />
              <q-btn
                color="secondary"
                label="Refresh Data"
                icon="refresh"
                size="md"
                @click="refreshAnalytics"
                class="action-btn"
              />
            </div>
              </q-card-section>

          <q-card-section class="analytics-content">
            <!-- Analytics Panels -->
            <div class="analytics-panels-container">
              <!-- Medication Analysis Panel -->
              <div class="analytics-panel medication-panel">
                <h4 class="panel-title">Medication Analysis</h4>
                <div class="panel-content">
                  <div v-if="analyticsData.medication_analysis" class="analytics-data">
                    <div class="data-item">
                      <span class="data-label">Most Prescribed Medications:</span>
                      <div class="data-values">
                        <div v-for="med in analyticsData.medication_analysis.medication_pareto_data?.slice(0, 5)" :key="med.medication" class="value-item">
                          {{ med.medication }}: {{ med.frequency }} prescriptions
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="empty-data">
                    <p>No medication analysis data available</p>
          </div>
        </div>
      </div>

              <!-- Demographics Panel -->
              <div class="analytics-panel demographics-panel">
                <h4 class="panel-title">Patient Demographics</h4>
                <div class="panel-content">
                  <div v-if="analyticsData.patient_demographics" class="analytics-data">
                    <div class="data-item">
                      <span class="data-label">Age Distribution:</span>
                      <div class="data-values">
                        <div v-for="(count, ageGroup) in analyticsData.patient_demographics.age_distribution" :key="ageGroup" class="value-item">
                          {{ ageGroup }}: {{ count }} patients
                    </div>
                  </div>
                </div>
                    <div class="data-item">
                      <span class="data-label">Gender Distribution:</span>
                      <div class="data-values">
                        <div v-for="(percentage, gender) in analyticsData.patient_demographics.gender_proportions" :key="gender" class="value-item">
                          {{ gender }}: {{ percentage }}%
              </div>
                    </div>
                  </div>
                </div>
                  <div v-else class="empty-data">
                    <p>No demographics data available</p>
              </div>
                    </div>
                  </div>

              <!-- Health Trends Panel -->
              <div class="analytics-panel trends-panel">
                <h4 class="panel-title">Health Trends</h4>
                <div class="panel-content">
                  <div v-if="analyticsData.health_trends" class="analytics-data">
                    <div class="data-item">
                      <span class="data-label">Top Medical Conditions:</span>
                      <div class="data-values">
                        <div v-for="illness in analyticsData.health_trends.top_illnesses_by_week?.slice(0, 5)" :key="illness.medical_condition" class="value-item">
                          {{ illness.medical_condition }}: {{ illness.count }} cases
                </div>
              </div>
                    </div>
                  </div>
                  <div v-else class="empty-data">
                    <p>No health trends data available</p>
                  </div>
                </div>
              </div>

              <!-- Volume Prediction Panel -->
              <div class="analytics-panel volume-panel">
                <h4 class="panel-title">Volume Prediction</h4>
                <div class="panel-content">
                  <div v-if="analyticsData.volume_prediction" class="analytics-data">
                    <div class="data-item">
                      <span class="data-label">Model Performance:</span>
                      <div class="data-values">
                        <div class="value-item">MAE: {{ analyticsData.volume_prediction.evaluation_metrics?.mae }}</div>
                        <div class="value-item">RMSE: {{ analyticsData.volume_prediction.evaluation_metrics?.rmse }}</div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="empty-data">
                    <p>No volume prediction data available</p>
                  </div>
                </div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
      
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from '../boot/axios'

const router = useRouter()
const $q = useQuasar()

const rightDrawerOpen = ref(false)
const text = ref('')

// Analytics data interfaces
interface MedicationAnalysis {
  medication_pareto_data?: Array<{
    medication: string
    frequency: number
    cumulative_percentage: number
  }>
}

interface PatientDemographics {
  age_distribution?: { [key: string]: number }
  gender_proportions?: { [key: string]: number }
}

interface HealthTrends {
  top_illnesses_by_week?: Array<{
    medical_condition: string
    count: number
    date_of_admission: string
  }>
}

interface VolumePrediction {
  evaluation_metrics?: {
    mae: number
    rmse: number
  }
}

interface AnalyticsData {
  medication_analysis: MedicationAnalysis | null
  patient_demographics: PatientDemographics | null
  health_trends: HealthTrends | null
  volume_prediction: VolumePrediction | null
}

// Analytics data
const analyticsData = ref<AnalyticsData>({
  medication_analysis: null,
  patient_demographics: null,
  health_trends: null,
  volume_prediction: null
})

// Real-time features
const currentTime = ref('')
const weatherData = ref<{
  temperature: number
  condition: string
  location: string
} | null>(null)
const weatherLoading = ref(false)
const weatherError = ref(false)
let timeInterval: NodeJS.Timeout | null = null

// User profile data
const userProfile = ref<{
  first_name?: string
  last_name?: string
  full_name: string
  department?: string
  role: string
  profile_picture: string | null
  verification_status: string
  email?: string
}>({
  first_name: '',
  last_name: '',
  full_name: 'Loading...',
  department: 'Loading department...',
  role: 'nurse',
  profile_picture: null,
  verification_status: 'not_submitted',
  email: ''
})

// File input reference for profile picture upload
const fileInput = ref<HTMLInputElement | null>(null)

/**
 * Computed property that generates user initials from the full name
 * @returns {string} The initials of the user's name in uppercase
 * 
 * How it works:
 * 1. Checks if full_name exists, returns 'U' if not
 * 2. Splits the full name by spaces to get individual names
 * 3. Maps each name to its first character
 * 4. Joins all first characters together
 * 5. Converts to uppercase for consistency
 */
const userInitials = computed(() => {
  if (!userProfile.value.full_name) return 'U'
  return userProfile.value.full_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
})

/**
 * Computed property that formats the current date for display in the greeting
 * @returns {string} Formatted date string (e.g., "Monday, January 15, 2024")
 * 
 * How it works:
 * 1. Gets the current date using new Date()
 * 2. Formats it using toLocaleDateString with specific options
 * 3. Returns a human-readable date string with weekday, month, day, and year
 */
const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})

/**
 * Computed property that formats the profile picture URL for display
 * @returns {string | null} Complete URL for the profile picture or null if no picture
 * 
 * How it works:
 * 1. Checks if profile_picture exists, returns null if not
 * 2. If the URL already starts with 'http', returns it as-is (external URL)
 * 3. Otherwise, prepends the backend server URL to create a complete path
 * 4. This handles both relative paths from the backend and absolute URLs
 */
const profilePictureUrl = computed(() => {
  if (!userProfile.value.profile_picture) {
    return null
  }
  
  if (userProfile.value.profile_picture.startsWith('http')) {
    return userProfile.value.profile_picture
  }
  
  return `http://localhost:8000${userProfile.value.profile_picture}`
})

/**
 * Updates the current time display in the header
 * @returns {void}
 * 
 * How it works:
 * 1. Gets the current date and time using new Date()
 * 2. Formats it using toLocaleTimeString with 12-hour format
 * 3. Updates the currentTime reactive reference
 * 4. This function is called every second by setInterval
 */
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', { 
    hour12: true, 
    hour: 'numeric', 
    minute: '2-digit', 
    second: '2-digit' 
  })
}

/**
 * Maps weather conditions to appropriate Material Design icons
 * @param {string} condition - The weather condition (sunny, cloudy, rainy, etc.)
 * @returns {string} The corresponding Material Design icon name
 * 
 * How it works:
 * 1. Takes a weather condition string as input
 * 2. Converts it to lowercase for case-insensitive matching
 * 3. Looks up the condition in the iconMap object
 * 4. Returns the corresponding icon name or defaults to 'wb_sunny' if not found
 * 5. This ensures the weather widget always displays an appropriate icon
 */
const getWeatherIcon = (condition: string) => {
  const iconMap: { [key: string]: string } = {
    'sunny': 'wb_sunny',
    'cloudy': 'cloud',
    'rainy': 'grain',
    'stormy': 'thunderstorm',
    'snowy': 'ac_unit',
    'foggy': 'foggy'
  }
  return iconMap[condition.toLowerCase()] || 'wb_sunny'
}

/**
 * Fetches weather data for display in the header
 * @returns {Promise<void>}
 * 
 * How it works:
 * 1. Sets loading state to true and clears any previous errors
 * 2. Simulates API call with a 1-second delay (replace with real API)
 * 3. Sets mock weather data (temperature, condition, location)
 * 4. Handles errors by setting error state and logging to console
 * 5. Always sets loading to false in the finally block
 * 
 * Note: Currently uses mock data - replace with actual weather API integration
 */
const fetchWeatherData = async () => {
  weatherLoading.value = true
  weatherError.value = false
  
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    weatherData.value = {
      temperature: 28,
      condition: 'sunny',
      location: 'Mandaluyong City'
    }
  } catch (error) {
    console.error('Failed to fetch weather data:', error)
    weatherError.value = true
  } finally {
    weatherLoading.value = false
  }
}

/**
 * Toggles the sidebar drawer open/closed state
 * @returns {void}
 * 
 * How it works:
 * 1. Flips the boolean value of rightDrawerOpen
 * 2. This controls the visibility of the sidebar navigation
 * 3. Used by the menu button in the header
 */
const toggleRightDrawer = () => {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

/**
 * Triggers the file input dialog for profile picture upload
 * @returns {void}
 * 
 * How it works:
 * 1. Uses optional chaining to safely access the file input reference
 * 2. Programmatically clicks the hidden file input element
 * 3. This opens the native file selection dialog
 * 4. The actual file handling is done in handleProfilePictureUpload
 */
const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleProfilePictureUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    
    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg']
    if (!allowedTypes.includes(file.type)) {
      $q.notify({
        type: 'negative',
        message: 'Please select a valid image file (JPG, PNG)',
        position: 'top',
        timeout: 3000
      })
      return
    }
    
    if (file.size > 5 * 1024 * 1024) {
      $q.notify({
        type: 'negative',
        message: 'File size must be less than 5MB',
        position: 'top',
        timeout: 3000
      })
      return
    }
    
    try {
      const formData = new FormData()
      formData.append('profile_picture', file)
      
      const response = await api.post('/users/profile/update/picture/', formData)
      
      userProfile.value.profile_picture = response.data.user.profile_picture
      
      // Store profile picture in localStorage for cross-page sync
      localStorage.setItem('profile_picture', response.data.user.profile_picture)
      
      $q.notify({
        type: 'positive',
        message: 'Profile picture updated successfully!',
        position: 'top',
        timeout: 3000
      })
      
      target.value = ''
    } catch (error: unknown) {
      console.error('Profile picture upload failed:', error)
      
      let errorMessage = 'Failed to upload profile picture. Please try again.'
      
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as { response?: { data?: { profile_picture?: string[], detail?: string } } }
        if (axiosError.response?.data?.profile_picture?.[0]) {
          errorMessage = axiosError.response.data.profile_picture[0]
        } else if (axiosError.response?.data?.detail) {
          errorMessage = axiosError.response.data.detail
        }
      }
      
      $q.notify({
        type: 'negative',
        message: errorMessage,
        position: 'top',
        timeout: 4000
      })
    }
  }
}

/**
 * Fetches user profile data from the API and updates the local state
 * @returns {Promise<void>}
 * 1. Makes API call to /users/profile/ endpoint
 * 2. Extracts user data from the response
 * 3. Updates the userProfile reactive reference with the data
 * 4. Handles errors by falling back to localStorage data
 * 5. Shows error notification if both API and localStorage fail
 * 
 * Fallback strategy:
 * - If API fails, tries to load from localStorage
 * - If localStorage also fails, shows error notification
 * - This ensures the app doesn't break if the API is down
 */
const fetchUserProfile = async () => {
  try {
    const response = await api.get('/users/profile/')
    const userData = response.data.user
    
    userProfile.value = {
      first_name: userData.first_name,
      last_name: userData.last_name,
      full_name: userData.full_name,
      department: userData.nurse_profile?.department,
      role: userData.role,
      profile_picture: userData.profile_picture || localStorage.getItem('profile_picture'),
      verification_status: userData.verification_status,
      email: userData.email
    }
    
    // Store profile picture in localStorage if available
    if (userData.profile_picture) {
      localStorage.setItem('profile_picture', userData.profile_picture)
    }
    
    console.log('User profile loaded:', userProfile.value)
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
    
    const userData = localStorage.getItem('user')
    if (userData) {
      const user = JSON.parse(userData)
      userProfile.value = {
        full_name: user.full_name,
        department: user.nurse_profile?.department,
        role: user.role,
        profile_picture: user.profile_picture || null,
        verification_status: user.verification_status || 'not_submitted'
      }
    } else {
      $q.notify({
        type: 'negative',
        message: 'Failed to load user profile',
        position: 'top',
        timeout: 3000
      })
    }
  }
}

/**
 * Fetches nurse-specific analytics data from the API
 * @returns {Promise<void>}
 * 
 * How it works:
 * 1. Makes API call to /analytics/nurse/ endpoint
 * 2. Extracts analytics data from the response
 * 3. Updates the analyticsData reactive reference
 * 4. Handles errors by showing notification to user
 * 5. Logs errors to console for debugging
 * 
 * Analytics data includes:
 * - Medication analysis (most prescribed medications)
 * - Patient demographics (age, gender distribution)
 * - Health trends (top medical conditions)
 * - Volume prediction (patient volume forecasting)
 */
const fetchNurseAnalytics = async () => {
  try {
    const response = await api.get('/analytics/nurse/')
    analyticsData.value = response.data.data
    console.log('Nurse analytics loaded:', analyticsData.value)
  } catch (error) {
    console.error('Failed to fetch nurse analytics:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load analytics data',
      position: 'top',
      timeout: 3000
    })
  }
}

/**
 * Handles navigation between different pages in the application
 * @param {string} route - The route name to navigate to
 * @returns {void}
 * 
 * How it works:
 * 1. Closes the sidebar drawer first
 * 2. Uses a switch statement to handle different routes
 * 3. Uses Vue Router to navigate to the appropriate page
 * 4. Shows notifications for pages that are not yet implemented
 * 5. Logs unknown routes to console for debugging
 * 
 * Supported routes:
 * - nurse-dashboard: Navigate to main dashboard
 * - medicine-inventory: Navigate to medicine inventory page
 * - patient-assessment: Navigate to patient assessment page
 * - analytics: Already on analytics page (no action)
 * - settings: Navigate to settings page
 */
const navigateTo = (route: string) => {
  rightDrawerOpen.value = false
  
  switch (route) {
    case 'nurse-dashboard':
      void router.push('/nurse-dashboard')
      break
    case 'nurse-medicine-inventory':
      void router.push('/nurse-medicine-inventory')
      break
    case 'patient-assessment':
      void router.push('/nurse-patient-assessment')
      break
    case 'patients':
      void router.push('/nurse-patient-management')
      break
    case 'nurse-analytics':
      // Already on analytics page
      break
    case 'settings':
      void router.push('/nurse-settings')
      break
    default:
      console.log('Navigation to:', route)
  }
}

/**
 * Handles user logout by clearing stored data and redirecting to login
 * @returns {void}
 * 
 * How it works:
 * 1. Removes access token from localStorage
 * 2. Removes refresh token from localStorage
 * 3. Removes user data from localStorage
 * 4. Redirects to the login page
 * 
 * This ensures a clean logout by removing all authentication data
 * and user information from the browser's local storage
 */
const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
}

/**
 * Shows notification when medication analysis card is clicked
 * @returns {void}
 * 
 * How it works:
 * 1. Displays an info notification to the user
 * 2. Indicates that medication analysis is being viewed
 * 3. Auto-dismisses after 2 seconds
 * 
 * Future enhancement: Could navigate to detailed medication analysis view
 */
const viewMedicationAnalysis = () => {
  $q.notify({
    type: 'info',
    message: 'Viewing Medication Analysis...',
    position: 'top',
    timeout: 2000
  })
}

/**
 * Shows notification when demographics card is clicked
 * @returns {void}
 * 
 * How it works:
 * 1. Displays an info notification to the user
 * 2. Indicates that demographics data is being viewed
 * 3. Auto-dismisses after 2 seconds
 * 
 * Future enhancement: Could navigate to detailed demographics view
 */
const viewDemographics = () => {
  $q.notify({
    type: 'info',
    message: 'Viewing Patient Demographics...',
    position: 'top',
    timeout: 2000
  })
}

/**
 * Shows notification when health trends card is clicked
 * @returns {void}
 * 
 * How it works:
 * 1. Displays an info notification to the user
 * 2. Indicates that health trends are being viewed
 * 3. Auto-dismisses after 2 seconds
 * 
 * Future enhancement: Could navigate to detailed trends view
 */
const viewHealthTrends = () => {
  $q.notify({
    type: 'info',
    message: 'Viewing Health Trends...',
    position: 'top',
    timeout: 2000
  })
}

/**
 * Shows notification when volume prediction card is clicked
 * @returns {void}
 * 
 * How it works:
 * 1. Displays an info notification to the user
 * 2. Indicates that volume prediction is being viewed
 * 3. Auto-dismisses after 2 seconds
 * 
 * Future enhancement: Could navigate to detailed volume prediction view
 */
const viewVolumePrediction = () => {
  $q.notify({
    type: 'info',
    message: 'Viewing Volume Prediction...',
    position: 'top',
    timeout: 2000
  })
}

/**
 * Generates and downloads a PDF report of nurse analytics
 * @returns {Promise<void>}
 * 
 * How it works:
 * 1. Makes API call to /analytics/pdf/?type=nurse with blob response type
 * 2. Creates a Blob object from the response data
 * 3. Creates a temporary URL for the blob
 * 4. Creates a temporary anchor element for download
 * 5. Sets the filename with current date
 * 6. Programmatically clicks the anchor to trigger download
 * 7. Cleans up by removing the anchor and revoking the URL
 * 8. Shows success/error notifications
 * 
 * The PDF contains comprehensive analytics data formatted for nurses
 */
const generatePDFReport = async () => {
  try {
    const response = await api.get('/analytics/pdf/?type=nurse', {
      responseType: 'blob'
    })
    
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `nurse_analytics_report_${new Date().toISOString().split('T')[0]}.pdf`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
    
    $q.notify({
      type: 'positive',
      message: 'PDF report generated successfully!',
      position: 'top',
      timeout: 3000
    })
  } catch (error) {
    console.error('Failed to generate PDF report:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to generate PDF report',
      position: 'top',
      timeout: 3000
    })
  }
}

/**
 * Refreshes analytics data by fetching the latest data from the API
 * @returns {Promise<void>}
 * 
 * How it works:
 * 1. Shows info notification that data is being refreshed
 * 2. Calls fetchNurseAnalytics to get latest data from API
 * 3. Waits for the data to be loaded
 * 4. Shows success notification when refresh is complete
 * 
 * This ensures users always have the most up-to-date analytics data
 */
const refreshAnalytics = async () => {
  $q.notify({
    type: 'info',
    message: 'Refreshing analytics data...',
    position: 'top',
    timeout: 2000
  })
  
  await fetchNurseAnalytics()
  
  $q.notify({
    type: 'positive',
    message: 'Analytics data refreshed!',
    position: 'top',
    timeout: 2000
  })
}

/**
 * Vue lifecycle hook that runs when the component is mounted
 * @returns {void}
 * 
 * How it works:
 * 1. Fetches user profile data from API
 * 2. Fetches nurse analytics data from API
 * 3. Sets initial time display
 * 4. Starts interval to update time every second
 * 5. Fetches weather data for display
 * 
 * This ensures all necessary data is loaded when the page opens
 */
onMounted(() => {
  void fetchUserProfile()
  void fetchNurseAnalytics()
  
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  
  void fetchWeatherData()
})

/**
 * Vue lifecycle hook that runs when the component is unmounted
 * @returns {void}
 * 
 * How it works:
 * 1. Checks if timeInterval exists
 * 2. Clears the interval to prevent memory leaks
 * 3. This prevents the time update from continuing after component destruction
 * 
 * This is important for preventing memory leaks and unnecessary background processes
 */
onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
/* Prototype Header Styles */
.prototype-header {
  background: linear-gradient(135deg, #286660 0%, #4a7c59 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-toolbar {
  padding: 0 24px;
  min-height: 64px;
}

.menu-toggle-btn {
  color: white;
  margin-right: 16px;
}

.header-left {
  flex: 1;
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.search-container {
  width: 100%;
  max-width: 500px;
}

.search-input {
  background: white;
  border-radius: 8px;
}

.notification-btn {
  color: white;
}

.time-display, .weather-display, .weather-loading, .weather-error {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 14px;
}

/* Prototype Sidebar Styles */
.prototype-sidebar {
  background: white;
  border-right: 1px solid #e0e0e0;
}

.sidebar-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding-bottom: 80px; /* Space for footer */
}

.logo-section {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #286660;
}

.menu-btn {
  color: #666;
}

.sidebar-user-profile {
  padding: 24px 20px;
  border-bottom: 1px solid #e0e0e0;
  text-align: center;
}

.sidebar-user-profile-centered {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-picture-container {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
}

.upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  transform: translate(25%, 25%);
}

.verified-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background: white;
  border-radius: 50%;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
}

.user-role {
  font-size: 14px;
  color: #666;
  margin: 0 0 12px 0;
}

.navigation-menu {
  flex: 1;
  padding: 16px 0;
}

.nav-item {
  margin: 4px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item.active {
  background: #286660;
  color: white;
}

.nav-item.active .q-icon {
  color: white;
}

.nav-item:hover:not(.active) {
  background: #f5f5f5;
}

.sidebar-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.logout-btn {
  width: 100%;
  border-radius: 8px;
  font-weight: 600;
  text-transform: uppercase;
}

/* Page Container with Background */
.page-container-with-fixed-header {
  background: #f8f9fa;
  min-height: 100vh;
  position: relative;
}

/* Greeting Section */
.greeting-section {
  padding: 24px;
  background: transparent;
}

.greeting-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
}

.greeting-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #286660, #6ca299, #b8d2ce);
  border-radius: 16px 16px 0 0;
}

.greeting-content {
  padding: 24px;
}

.greeting-text {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0 0 8px 0;
}

.greeting-subtitle {
  font-size: 16px;
  color: #666;
  margin: 0;
}

/* Dashboard Cards Section */
.dashboard-cards-section {
  padding: 24px;
}

.dashboard-cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Glassmorphism Dashboard Cards */
.dashboard-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  overflow: hidden;
  position: relative;
}

.dashboard-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #286660, #6ca299, #b8d2ce);
  border-radius: 16px 16px 0 0;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  background: rgba(255, 255, 255, 0.35);
}

.dashboard-card:hover::before {
  opacity: 1;
}

.card-content {
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.card-text {
  flex: 1;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.3;
}

.card-description {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.card-icon {
  margin-left: 16px;
  color: #286660;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.dashboard-card:hover .card-icon {
  opacity: 1;
  transform: scale(1.1);
}

/* Card-specific colors */
.medication-card .card-icon { color: #9c27b0; }
.demographics-card .card-icon { color: #2196f3; }
.trends-card .card-icon { color: #4caf50; }
.volume-card .card-icon { color: #ff9800; }

/* Analytics Section */
.analytics-section {
  padding: 24px;
}

.analytics-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.05);
  max-width: 1200px;
  margin: 0 auto;
}

.analytics-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 24px 24px 0 24px;
}

.analytics-content {
  padding: 0 24px 24px 24px;
}

.analytics-title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin: 0 0 24px 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.analytics-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.action-btn {
  border-radius: 8px;
  font-weight: 500;
  padding: 12px 24px;
  min-width: 160px;
}

/* Analytics Panels */
.analytics-panels-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.analytics-panel {
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
  min-height: 300px;
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
  text-align: center;
}

.panel-content {
  height: 100%;
}

.analytics-data {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.data-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.data-label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.data-values {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.value-item {
  font-size: 13px;
  color: #666;
  padding: 4px 8px;
  background: white;
  border-radius: 4px;
  border-left: 3px solid #286660;
}

.empty-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #666;
}

.empty-data p {
  margin-top: 12px;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-cards-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .analytics-panels-container {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .greeting-text {
    font-size: 24px;
  }
  
  .card-content {
    padding: 20px;
  }
  
  .card-title {
    font-size: 16px;
  }
  
  .card-description {
    font-size: 13px;
  }

  .analytics-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .action-btn {
    width: 100%;
    max-width: 200px;
  }
}

@media (max-width: 480px) {
  .dashboard-cards-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .greeting-text {
    font-size: 20px;
  }
  
  .card-content {
    padding: 16px;
  }
  
  .card-title {
    font-size: 15px;
  }
  
  .card-description {
    font-size: 12px;
  }
}

/* Header Styles */
.prototype-header {
  background: #286660;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-toolbar {
  padding: 0 16px;
}

.header-left, .header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.search-container {
  min-width: 300px;
}

.search-input {
  border-radius: 8px;
}

.time-display, .weather-display, .weather-loading, .weather-error {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 14px;
  font-size: 14px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.time-text,
.weather-text,
.weather-location {
  font-size: 14px;
  font-weight: 500;
  color: white;
}

.weather-location {
  font-size: 12px;
  opacity: 0.8;
}

.weather-loading, .weather-error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: white;
  font-size: 14px;
  font-weight: 500;
}

.weather-error .q-icon {
  color: #ff6b6b;
}
</style>