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

        <!-- User Profile Section -->
        <div class="sidebar-user-profile">
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
            <q-icon 
              :name="userProfile.verification_status === 'approved' ? 'check_circle' : 'cancel'" 
              :color="userProfile.verification_status === 'approved' ? 'positive' : 'negative'" 
              class="verified-badge" 
            />
          </div>
          
          <div class="user-info">
            <h6 class="user-name">{{ userProfile.full_name || 'Loading...' }}</h6>
            <p class="user-role">{{ userProfile.specialization || 'Loading specialization...' }}</p>
            <q-chip 
              :color="userProfile.verification_status === 'approved' ? 'positive' : 'negative'" 
              text-color="white" 
              size="sm"
            >
              {{ userProfile.verification_status === 'approved' ? 'Verified' : 'Not Verified' }}
            </q-chip>
          </div>
        </div>

        <!-- Navigation Menu -->
        <q-list class="navigation-menu">
          <q-item clickable v-ripple @click="navigateTo('doctor-dashboard')" class="nav-item active">
            <q-item-section avatar>
              <q-icon name="grid_view" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('appointments')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="event" />
            </q-item-section>
            <q-item-section>Appointments</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('messaging')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="message" />
            </q-item-section>
            <q-item-section>Messaging</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('patients')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>
            <q-item-section>Patient Management</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('analytics')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="bar_chart" />
            </q-item-section>
            <q-item-section>Analytics</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('settings')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>
            <q-item-section>Settings</q-item-section>
          </q-item>
        </q-list>

        <!-- Logout Section -->
        <div class="logout-section">
          <q-btn
            color="negative"
            icon="logout"
            label="LOGOUT"
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
              Good {{ getTimeOfDay() }}, {{ userProfile.role.charAt(0).toUpperCase() + userProfile.role.slice(1) }} {{ userProfile.full_name }}
          </h2>
            <p class="greeting-subtitle">See what's happening today - {{ currentDate }}</p>
          </q-card-section>
        </q-card>
      </div>
      
      <!-- Dashboard Cards Section -->
      <div class="dashboard-cards-section">
        <div class="dashboard-cards-grid">
          <!-- Today's Appointment Card -->
          <q-card class="dashboard-card appointments-card" @click="showTodayAppointmentsModal">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Today's Appointment</div>
                <div class="card-description">{{ dashboardStats.todayAppointments }} appointments today</div>
                <div class="card-value">
                  <q-spinner v-if="statsLoading" size="md" />
                  <span v-else>{{ dashboardStats.todayAppointments }}</span>
                </div>
              </div>
              <div class="card-icon">
                <q-icon name="event" size="2.5rem" />
              </div>
            </q-card-section>
          </q-card>

          <!-- Total Patient Card -->
          <q-card class="dashboard-card patients-card" @click="showTotalPatientsModal">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Total Patient</div>
                <div class="card-description">Based on completed assessments</div>
                <div class="card-value">
                  <q-spinner v-if="statsLoading" size="md" />
                  <span v-else>{{ dashboardStats.totalPatients }}</span>
                </div>
              </div>
              <div class="card-icon">
                <q-icon name="people" size="2.5rem" />
              </div>
            </q-card-section>
          </q-card>

          <!-- Completed Appointment Card -->
          <q-card class="dashboard-card completed-card" @click="showCompletedAppointmentsModal">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Completed Appointment</div>
                <div class="card-description">All transaction history</div>
                <div class="card-value">
                  <q-spinner v-if="statsLoading" size="md" />
                  <span v-else>{{ dashboardStats.completedAppointments }}</span>
                </div>
              </div>
              <div class="card-icon">
                <q-icon name="check_circle" size="2.5rem" />
              </div>
            </q-card-section>
          </q-card>

          <!-- Pending Assessment Card -->
          <q-card class="dashboard-card assessment-card" @click="showPendingAssessmentsModal">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Pending Assessment</div>
                <div class="card-description">Currently being assessed by nurses</div>
                <div class="card-value">
                  <q-spinner v-if="statsLoading" size="md" />
                  <span v-else>{{ dashboardStats.pendingAssessments }}</span>
                </div>
              </div>
              <div class="card-icon">
                <q-icon name="assignment" size="2.5rem" />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Modals -->
      
      <!-- Today's Appointments Modal -->
      <q-dialog v-model="todayAppointmentsModal" persistent>
        <q-card style="min-width: 800px; max-width: 90vw;">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Today's Appointments</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>
          
          <q-card-section>
            <q-list separator>
              <q-item v-for="appointment in todayAppointments" :key="appointment.id" class="q-pa-md">
                <q-item-section avatar>
                  <q-avatar color="primary" text-color="white">
                    {{ appointment.patient?.name?.charAt(0) || 'P' }}
                  </q-avatar>
                </q-item-section>
                
                <q-item-section>
                  <q-item-label>{{ appointment.patient?.name || 'Unknown Patient' }}</q-item-label>
                  <q-item-label caption>Appointment Time: {{ formatTime(appointment.appointment_time) }}</q-item-label>
                  <q-item-label caption>Status: {{ appointment.status }}</q-item-label>
                </q-item-section>
                
                <q-item-section side>
                  <q-chip :color="getStatusColor(appointment.status)" text-color="white">
                    {{ appointment.status }}
                  </q-chip>
                </q-item-section>
              </q-item>
            </q-list>
            
            <div v-if="todayAppointments.length === 0" class="text-center q-pa-md text-grey-6">
              No appointments scheduled for today.
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Total Patients Modal -->
      <q-dialog v-model="totalPatientsModal" persistent>
        <q-card style="min-width: 800px; max-width: 90vw;">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Total Patients (Completed Assessments)</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>
          
          <q-card-section>
            <q-list separator>
              <q-item v-for="patient in totalPatients" :key="patient.id" class="q-pa-md">
                <q-item-section avatar>
                  <q-avatar color="green" text-color="white">
                    {{ patient.patient?.name?.charAt(0) || 'P' }}
                  </q-avatar>
                </q-item-section>
                
                <q-item-section>
                  <q-item-label>{{ patient.patient?.name || 'Unknown Patient' }}</q-item-label>
                  <q-item-label caption>Assessment Date: {{ formatDate(patient.assessment_date) }}</q-item-label>
                  <q-item-label caption>Completed by: {{ patient.nurse?.name || 'Unknown Nurse' }}</q-item-label>
                </q-item-section>
                
                <q-item-section side>
                  <q-chip color="green" text-color="white">
                    Completed
                  </q-chip>
                </q-item-section>
              </q-item>
            </q-list>
            
            <div v-if="totalPatients.length === 0" class="text-center q-pa-md text-grey-6">
              No completed assessments found.
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Completed Appointments Modal -->
      <q-dialog v-model="completedAppointmentsModal" persistent>
        <q-card style="min-width: 800px; max-width: 90vw;">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Completed Appointments (Transaction History)</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>
          
          <q-card-section>
            <q-list separator>
              <q-item v-for="appointment in completedAppointments" :key="appointment.id" class="q-pa-md">
                <q-item-section avatar>
                  <q-avatar color="orange" text-color="white">
                    {{ appointment.patient?.name?.charAt(0) || 'P' }}
                  </q-avatar>
                </q-item-section>
                
                <q-item-section>
                  <q-item-label>{{ appointment.patient?.name || 'Unknown Patient' }}</q-item-label>
                  <q-item-label caption>Appointment Date: {{ formatDate(appointment.appointment_date) }}</q-item-label>
                  <q-item-label caption>Completed: {{ formatDateTime(appointment.completed_at) }}</q-item-label>
                </q-item-section>
                
                <q-item-section side>
                  <q-chip color="orange" text-color="white">
                    Completed
                  </q-chip>
                </q-item-section>
              </q-item>
            </q-list>
            
            <div v-if="completedAppointments.length === 0" class="text-center q-pa-md text-grey-6">
              No completed appointments found.
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Pending Assessments Modal -->
      <q-dialog v-model="pendingAssessmentsModal" persistent>
        <q-card style="min-width: 800px; max-width: 90vw;">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Pending Assessments</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>
          
          <q-card-section>
            <q-list separator>
              <q-item v-for="assessment in pendingAssessments" :key="assessment.id" class="q-pa-md">
                <q-item-section avatar>
                  <q-avatar color="purple" text-color="white">
                    {{ assessment.patient?.name?.charAt(0) || 'P' }}
                  </q-avatar>
                </q-item-section>
                
                <q-item-section>
                  <q-item-label>{{ assessment.patient?.name || 'Unknown Patient' }}</q-item-label>
                  <q-item-label caption>Assessment Started: {{ formatDateTime(assessment.created_at) }}</q-item-label>
                  <q-item-label caption>Assigned Nurse: {{ assessment.nurse?.name || 'Unknown Nurse' }}</q-item-label>
                </q-item-section>
                
                <q-item-section side>
                  <q-chip color="purple" text-color="white">
                    In Progress
                  </q-chip>
                </q-item-section>
              </q-item>
            </q-list>
            
            <div v-if="pendingAssessments.length === 0" class="text-center q-pa-md text-grey-6">
              No pending assessments found.
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>

      
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from '../boot/axios'

// Type definitions
interface Patient {
  id: number
  name: string
  [key: string]: unknown
}

interface Nurse {
  id: number
  name: string
  [key: string]: unknown
}

interface Appointment {
  id: number
  patient?: Patient
  appointment_time?: string
  appointment_date?: string
  status: string
  completed_at?: string
  [key: string]: unknown
}

interface Assessment {
  id: number
  patient?: Patient
  nurse?: Nurse
  assessment_date?: string
  status: string
  created_at?: string
  [key: string]: unknown
}


const router = useRouter()
const $q = useQuasar()


const rightDrawerOpen = ref(false)
const text = ref('')

// Carousel variables (removed but keeping for potential future use)
// const slide = ref(1)
// const autoplay = ref(true)

// Dashboard statistics
const dashboardStats = ref({
  todayAppointments: 0,
  totalPatients: 0,
  completedAppointments: 0,
  pendingAssessments: 0
})

// Loading states for dashboard stats
const statsLoading = ref(true)

// Modal states
const todayAppointmentsModal = ref(false)
const totalPatientsModal = ref(false)
const completedAppointmentsModal = ref(false)
const pendingAssessmentsModal = ref(false)

// Modal data
const todayAppointments = ref<Appointment[]>([])
const totalPatients = ref<Assessment[]>([])
const completedAppointments = ref<Appointment[]>([])
const pendingAssessments = ref<Assessment[]>([])

// Loading states for modals
const modalLoading = ref(false)


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

// User profile data - fetched from API
const userProfile = ref<{
  id?: number
  full_name: string
  specialization?: string
  role: string
  profile_picture: string | null
  verification_status: string
}>({
  full_name: 'Loading...',
  specialization: 'Loading specialization...',
  role: 'doctor',
  profile_picture: null,
  verification_status: 'not_submitted'
})

// File input reference for profile picture upload
const fileInput = ref<HTMLInputElement | null>(null)

const userInitials = computed(() => {
  if (!userProfile.value.full_name) return 'U'
  return userProfile.value.full_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
})

// Get time of day for greeting
const getTimeOfDay = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'morning'
  if (hour < 18) return 'afternoon'
  return 'evening'
}

// Current date for greeting
const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})

// Format profile picture URL
const profilePictureUrl = computed(() => {
  if (!userProfile.value.profile_picture) {
    return null
  }
  
  // If it's already a full URL, return as is
  if (userProfile.value.profile_picture.startsWith('http')) {
    return userProfile.value.profile_picture
  }
  
  // Otherwise, construct the full URL
    return `http://localhost:8000${userProfile.value.profile_picture}`
})

// Time update function
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', { 
    hour12: true, 
    hour: 'numeric', 
    minute: '2-digit', 
    second: '2-digit' 
  })
}

// Weather icon mapping
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

// Fetch weather data
const fetchWeatherData = async () => {
  weatherLoading.value = true
  weatherError.value = false
  
  try {
    // Mock weather data - replace with actual API call
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

const toggleRightDrawer = () => {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

// Profile picture upload functions
const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleProfilePictureUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    
    // Validate file type
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
    
    // Validate file size (max 5MB)
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
      
      // Store the updated profile picture in localStorage for cross-page sync
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}')
      currentUser.profile_picture = response.data.user.profile_picture
      localStorage.setItem('user', JSON.stringify(currentUser))
      
      // Show success toast
      $q.notify({
        type: 'positive',
        message: 'Profile picture updated successfully!',
        position: 'top',
        timeout: 3000
      })
      
      // Clear the file input
      target.value = ''
    } catch (error: unknown) {
      console.error('Profile picture upload failed:', error)
      
      let errorMessage = 'Failed to upload profile picture. Please try again.'
      
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as { response?: { data?: { profile_picture?: string[], detail?: string, error?: string }, status?: number } }
        console.error('Upload error response:', axiosError.response?.data)
        
        if (axiosError.response?.data?.profile_picture?.[0]) {
          errorMessage = axiosError.response.data.profile_picture[0]
        } else if (axiosError.response?.data?.detail) {
          errorMessage = axiosError.response.data.detail
        } else if (axiosError.response?.data?.error) {
          errorMessage = axiosError.response.data.error
        } else if (axiosError.response?.status === 413) {
          errorMessage = 'File too large. Please select a smaller image.'
        } else if (axiosError.response?.status === 400) {
          errorMessage = 'Invalid file format. Please select a valid image file.'
        } else if (axiosError.response?.status === 500) {
          errorMessage = 'Server error. Please try again later.'
        }
      } else if (error && typeof error === 'object' && 'message' in error) {
        const errorMsg = (error as { message: string }).message
        if (errorMsg.includes('Network Error')) {
          errorMessage = 'Network error. Please check your connection and try again.'
        }
      }
      
      $q.notify({
        type: 'negative',
        message: errorMessage,
        position: 'top',
        timeout: 5000
      })
    }
  }
}

// Fetch user profile data
const fetchUserProfile = async () => {
  try {
    const response = await api.get('/users/profile/')
    const userData = response.data.user // The API returns nested user data
    
    // Check localStorage for updated profile picture
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
    
    userProfile.value = {
      id: userData.id,
      full_name: userData.full_name,
      specialization: userData.doctor_profile?.specialization,
      role: userData.role,
      profile_picture: storedUser.profile_picture || userData.profile_picture || null,
      verification_status: userData.verification_status
    }
    
    console.log('User profile loaded:', userProfile.value)
    
    // Fetch dashboard stats after profile is loaded
    await fetchDashboardStats()
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
    
    // Fallback to localStorage
    const userData = localStorage.getItem('user')
    if (userData) {
      const user = JSON.parse(userData)
      userProfile.value = {
        id: user.id,
        full_name: user.full_name,
        specialization: user.doctor_profile?.specialization,
        role: user.role,
        profile_picture: user.profile_picture || null,
        verification_status: user.verification_status || 'not_submitted'
      }
      
      // Still try to fetch dashboard stats
      await fetchDashboardStats()
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

const navigateTo = (route: string) => {
  // Close drawer first
  rightDrawerOpen.value = false
  
  // Navigate to different sections
  switch (route) {
    case 'doctor-dashboard':
      void router.push('/doctor-dashboard')
      break
    case 'appointments':
      void router.push('/doctor-appointments')
      break
    case 'messaging':
      void router.push('/doctor-messaging')
      break
    case 'patients':
      void router.push('/doctor-patient-management')
      break
    case 'analytics':
      void router.push('/doctor-predictive-analytics')
      break
    case 'settings':
      void router.push('/doctor-settings')
      break
    default:
      console.log('Navigation to:', route)
  }
}

// Modal functions
const showTodayAppointmentsModal = async () => {
  modalLoading.value = true
  todayAppointmentsModal.value = true
  
  try {
    const response = await api.get('/operations/appointments/', {
      params: {
        doctor: userProfile.value.id,
        date: new Date().toISOString().split('T')[0],
        status: 'scheduled'
      }
    })
    todayAppointments.value = response.data.results || response.data || []
  } catch (error) {
    console.error('Failed to fetch today\'s appointments:', error)
    todayAppointments.value = []
  } finally {
    modalLoading.value = false
  }
}

const showTotalPatientsModal = async () => {
  modalLoading.value = true
  totalPatientsModal.value = true
  
  try {
    const response = await api.get('/operations/patient-assessments/', {
      params: {
        status: 'completed'
      }
    })
    totalPatients.value = response.data.results || response.data || []
  } catch (error) {
    console.error('Failed to fetch total patients:', error)
    totalPatients.value = []
  } finally {
    modalLoading.value = false
  }
}

const showCompletedAppointmentsModal = async () => {
  modalLoading.value = true
  completedAppointmentsModal.value = true
  
  try {
    const response = await api.get('/operations/appointments/', {
      params: {
        doctor: userProfile.value.id,
        status: 'completed'
      }
    })
    completedAppointments.value = response.data.results || response.data || []
  } catch (error) {
    console.error('Failed to fetch completed appointments:', error)
    completedAppointments.value = []
  } finally {
    modalLoading.value = false
  }
}

const showPendingAssessmentsModal = async () => {
  modalLoading.value = true
  pendingAssessmentsModal.value = true
  
  try {
    const response = await api.get('/operations/patient-assessments/', {
      params: {
        status: 'in_progress'
      }
    })
    pendingAssessments.value = response.data.results || response.data || []
  } catch (error) {
    console.error('Failed to fetch pending assessments:', error)
    pendingAssessments.value = []
  } finally {
    modalLoading.value = false
  }
}

// Utility functions for formatting
const formatTime = (timeString?: string) => {
  if (!timeString) return 'N/A'
  return new Date(timeString).toLocaleTimeString('en-US', {
    hour12: true,
    hour: 'numeric',
    minute: '2-digit'
  })
}

const formatDate = (dateString?: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatDateTime = (dateString?: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

const getStatusColor = (status?: string) => {
  switch (status?.toLowerCase()) {
    case 'scheduled':
      return 'blue'
    case 'completed':
      return 'green'
    case 'cancelled':
      return 'red'
    case 'in_progress':
      return 'orange'
    default:
      return 'grey'
  }
}


const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
}

// Fetch dashboard statistics
const fetchDashboardStats = async () => {
  try {
    statsLoading.value = true
    
    // Fetch all required data in parallel
    const [todayAppointmentsRes, totalPatientsRes, completedAppointmentsRes, pendingAssessmentsRes] = await Promise.all([
      // Today's appointments for doctor
      api.get('/operations/appointments/', {
        params: {
          doctor: userProfile.value.id,
          date: new Date().toISOString().split('T')[0],
          status: 'scheduled'
        }
      }).catch(() => ({ data: { count: 0 } })),
      
      // Total patients based on completed assessments
      api.get('/operations/patient-assessments/', {
        params: {
          status: 'completed'
        }
      }).catch(() => ({ data: { count: 0 } })),
      
      // Completed appointments (transaction history)
      api.get('/operations/appointments/', {
        params: {
          doctor: userProfile.value.id,
          status: 'completed'
        }
      }).catch(() => ({ data: { count: 0 } })),
      
      // Pending assessments (currently being assessed by nurses)
      api.get('/operations/patient-assessments/', {
        params: {
          status: 'in_progress'
        }
      }).catch(() => ({ data: { count: 0 } }))
    ])
    
    dashboardStats.value = {
      todayAppointments: todayAppointmentsRes.data.count || todayAppointmentsRes.data.results?.length || 0,
      totalPatients: totalPatientsRes.data.count || totalPatientsRes.data.results?.length || 0,
      completedAppointments: completedAppointmentsRes.data.count || completedAppointmentsRes.data.results?.length || 0,
      pendingAssessments: pendingAssessmentsRes.data.count || pendingAssessmentsRes.data.results?.length || 0
    }
    
    console.log('Dashboard stats loaded:', dashboardStats.value)
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error)
    
    // Set default values on error
    dashboardStats.value = {
      todayAppointments: 0,
      totalPatients: 0,
      completedAppointments: 0,
      pendingAssessments: 0
    }
  } finally {
    statsLoading.value = false
  }
}


// Daily refresh functionality
const setupDailyRefresh = () => {
  const now = new Date()
  const tomorrow = new Date(now)
  tomorrow.setDate(tomorrow.getDate() + 1)
  tomorrow.setHours(0, 0, 0, 0)
  
  const msUntilMidnight = tomorrow.getTime() - now.getTime()
  
  setTimeout(() => {
    // Refresh dashboard stats at midnight
    void fetchDashboardStats()
    
    // Set up daily refresh
    setInterval(() => {
      void fetchDashboardStats()
    }, 24 * 60 * 60 * 1000) // 24 hours
  }, msUntilMidnight)
}

onMounted(() => {
  // Load user profile data from API (this will also fetch dashboard stats)
  void fetchUserProfile()
  
  // Initialize real-time features
  updateTime() // Set initial time
  timeInterval = setInterval(updateTime, 1000) // Update every second
  
  // Fetch weather data
  void fetchWeatherData()
  
  // Setup daily refresh
  setupDailyRefresh()
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
/* Prototype Header Styles */
.prototype-header {
  background: #286660;
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

.logout-section {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
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
  background-size: cover;
  min-height: 100vh;
  position: relative;
}

.page-container-with-fixed-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(248, 249, 250, 0.15) 50%, rgba(240, 242, 245, 0.08) 100%);
  z-index: 0;
  pointer-events: none;
}

.page-container-with-fixed-header > * {
  position: relative;
  z-index: 1;
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
  min-height: 140px;
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
  margin-bottom: 8px;
}

.card-value {
  font-size: 32px;
  font-weight: 700;
  color: #286660;
  line-height: 1;
  margin-top: 8px;
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
.appointments-card .card-icon { color: #2196f3; }
.appointments-card .card-value { color: #2196f3; }

.patients-card .card-icon { color: #4caf50; }
.patients-card .card-value { color: #4caf50; }

.completed-card .card-icon { color: #ff9800; }
.completed-card .card-value { color: #ff9800; }

.assessment-card .card-icon { color: #9c27b0; }
.assessment-card .card-value { color: #9c27b0; }


/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-cards-grid {
    grid-template-columns: repeat(2, 1fr);
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
</style>