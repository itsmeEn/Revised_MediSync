<template>
  <q-layout view="hHh Lpr fFf">

    <q-header elevated class="text-white fixed-header" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleRightDrawer" />
        
        <q-toolbar-title>
          <q-avatar>
            <img src="../assets/logo.png" alt="MediSync Logo" />
          </q-avatar>
          MediSync
        </q-toolbar-title>
      </q-toolbar>

      <q-toolbar class="text-white">
        <div class="search-container">
          <q-input 
            dark 
            dense 
            standout 
            v-model="text" 
            placeholder="Search patients, symptoms, appointments..."
            class="search-input"
          >
            <template v-slot:append>
              <q-icon v-if="text === ''" name="search" />
              <q-icon v-else name="clear" class="cursor-pointer" @click="text = ''" />
            </template>
          </q-input>
        </div>
        
        <!-- Real-time Time and Weather -->
        <div class="real-time-info">
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
            <span class="weather-text">Weather unavailable</span>
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="rightDrawerOpen" side="left" overlay bordered>
      <div class="drawer-content">
        <!-- User Profile Section -->
        <div class="user-profile-section">
          <div class="profile-picture-container">
            <q-avatar size="100px" class="profile-avatar">
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
            <h6 class="user-name">{{ userProfile.full_name }}</h6>
            <p class="user-specialization">{{ userProfile.specialization }}</p>
            <q-chip color="primary" text-color="white" size="sm">
              {{ userProfile.role }}
            </q-chip>
          </div>
        </div>

        <!-- Navigation Menu -->
        <q-list class="navigation-menu">
          <q-item clickable v-ripple @click="navigateTo('doctor-dashboard')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="dashboard" />
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
              <q-icon name="analytics" />
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
        <div class="greeting-content">
          <h2 class="greeting-text">
            {{ greetingMessage }} {{ userProfile.role.charAt(0).toUpperCase() + userProfile.role.slice(1) }}
          </h2>
          <p class="greeting-subtitle">See what's happening today</p>
        </div>
      </div>
      
      <!-- All Dashboard Cards in One Row -->
      <div class="dashboard-cards-section">
        <div class="dashboard-cards-grid">
          <!-- Today's Schedule Card -->
          <q-card class="dashboard-card schedule-card">
            <q-card-section class="text-center">
              <div class="card-icon">
                <q-icon name="schedule" size="2rem" />
              </div>
              <div class="card-number">{{ dashboardStats.todaySchedule }}</div>
              <div class="card-label">Today's Schedule</div>
              <div class="text-caption text-grey-6">Appointments scheduled for today</div>
            </q-card-section>
          </q-card>

          <!-- Completed Patients Card -->
          <q-card class="dashboard-card completed-card">
            <q-card-section class="text-center">
              <div class="card-icon">
                <q-icon name="check_circle" size="2rem" />
              </div>
              <div class="card-number">{{ dashboardStats.completedPatients }}</div>
              <div class="card-label">Completed Today</div>
              <div class="text-caption text-grey-6">Patients seen today</div>
            </q-card-section>
          </q-card>

          <!-- Emergency Cases Card -->
          <q-card class="dashboard-card emergency-card">
            <q-card-section class="text-center">
              <div class="card-icon">
                <q-icon name="emergency" size="2rem" />
              </div>
              <div class="card-number">{{ dashboardStats.emergencyCases }}</div>
              <div class="card-label">Emergency Cases</div>
              <div class="text-caption text-grey-6">Urgent cases today</div>
            </q-card-section>
          </q-card>

          <!-- Average Wait Time Card -->
          <q-card class="dashboard-card wait-time-card">
            <q-card-section class="text-center">
              <div class="card-icon">
                <q-icon name="timer" size="2rem" />
              </div>
              <div class="card-number">{{ dashboardStats.averageWaitTime }}min</div>
              <div class="card-label">Avg Wait Time</div>
              <div class="text-caption text-grey-6">Average patient wait time</div>
            </q-card-section>
          </q-card>

          <!-- Total Appointments Card -->
          <q-card class="dashboard-card appointments-card" @click="void navigateToAppointments()" style="cursor: pointer;">
            <q-card-section class="text-center">
              <div class="card-icon">
                <q-icon name="event" size="2rem" />
              </div>
              <div class="card-number">{{ dashboardStats.totalAppointments }}</div>
              <div class="card-label">Total Appointments</div>
              <div class="text-caption text-grey-6">Click to manage appointments</div>
            </q-card-section>
          </q-card>

          <!-- Patient Queue Card -->
          <q-card class="dashboard-card queue-card">
            <q-card-section class="text-center">
              <div class="card-icon">
                <q-icon name="people" size="2rem" />
              </div>
              <div class="card-number">{{ dashboardStats.totalPatients }}</div>
              <div class="card-label">Patients in Queue</div>
              <div class="queue-breakdown">
                <div class="queue-item">
                  <span class="queue-type normal">Normal: {{ dashboardStats.normalQueue }}</span>
                </div>
                <div class="queue-item">
                  <span class="queue-type priority">Priority: {{ dashboardStats.priorityQueue }}</span>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Notifications Card -->
          <q-card class="dashboard-card notifications-card">
            <q-card-section class="text-center">
              <div class="card-icon">
                <q-icon name="notifications" size="2rem" />
              </div>
              <div class="card-number">{{ dashboardStats.notifications }}</div>
              <div class="card-label">Notifications</div>
            </q-card-section>
          </q-card>

          <!-- Pending Assessment Card -->
          <q-card class="dashboard-card assessment-card">
            <q-card-section class="text-center">
              <div class="card-icon">
                <q-icon name="assignment" size="2rem" />
              </div>
              <div class="card-number">{{ dashboardStats.pendingAssessment }}</div>
              <div class="card-label">Pending Assessment</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Operations Queue Management System -->
      <div class="queueing-section">
        <div class="queueing-header">
          <h3 class="queueing-title">Operations Queue Management</h3>
          <div class="queueing-actions">
            <q-btn
              color="primary"
              label="Add Patient"
              icon="person_add"
              size="sm"
              @click="addPatientToQueue"
            />
            <q-btn
              color="secondary"
              label="Call Next"
              icon="volume_up"
              size="sm"
              @click="callNextPatient"
            />
            <q-btn
              color="accent"
              label="Manage Queue"
              icon="settings"
              size="sm"
              @click="manageQueue"
            />
          </div>
        </div>



        <!-- Combined Queue Management Card -->
        <q-card class="combined-queue-card">
          <q-card-section>
            <div class="combined-queue-header">
              <h6 class="combined-queue-title">
                <q-icon name="queue" color="primary" />
                Operations Queue Management
              </h6>
              <div class="combined-queue-stats">
                <q-chip color="primary" text-color="white" :label="`Normal: ${normalQueue.length}`" />
                <q-chip color="negative" text-color="white" :label="`Priority: ${priorityQueue.length}`" />
                <q-chip color="info" text-color="white" :label="`Est. Wait: ${estimatedWaitTime}min`" />
              </div>
            </div>
            
            <div class="combined-queue-content">
              <!-- Normal Queue Section -->
              <div class="queue-section normal-queue-section">
                <div class="queue-section-header">
                  <h6 class="queue-section-title">
                    <q-icon name="queue" color="primary" />
                    Normal Queue (FIFO)
                  </h6>
                  <q-chip color="primary" text-color="white" size="sm" :label="`${normalQueue.length} patients`" />
                </div>
                
                <div class="queue-section-content">
                  <div v-if="normalQueue.length === 0" class="empty-queue">
                    <q-icon name="queue_outline" size="2rem" color="grey-4" />
                    <p>No patients in normal queue</p>
                    <q-btn
                      color="primary"
                      label="Add First Patient"
                      icon="add"
                      size="sm"
                      @click="addPatientToQueue"
                    />
                  </div>
                  
                  <div v-else class="queue-items">
                    <div
                      v-for="(patient, index) in normalQueue"
                      :key="patient.id"
                      class="queue-item"
                      :class="{ 
                        'current-patient': patient.isCurrent,
                        'next-in-line': index === 0 && !patient.isCurrent
                      }"
                    >
                      <div class="patient-info">
                        <div class="patient-number">
                          <div class="queue-position">{{ index + 1 }}</div>
                          <div class="queue-number">{{ patient.queueNumber }}</div>
                        </div>
                        <div class="patient-details">
                          <div class="patient-name">{{ patient.name }}</div>
                          <div class="patient-time">Arrived: {{ patient.arrivalTime }}</div>
                          <div class="patient-status" v-if="patient.isCurrent">
                            <q-chip color="positive" text-color="white" size="sm" label="In Progress" />
                          </div>
                        </div>
                      </div>
                      <div class="patient-actions">
                        <q-btn
                          round
                          flat
                          dense
                          color="primary"
                          icon="visibility"
                          @click="viewPatient(patient)"
                          size="sm"
                        >
                          <q-tooltip>View Details</q-tooltip>
                        </q-btn>
                        <q-btn
                          round
                          flat
                          dense
                          color="positive"
                          icon="play_arrow"
                          @click="startConsultation(patient)"
                          size="sm"
                          v-if="!patient.isCurrent"
                        >
                          <q-tooltip>Start Consultation</q-tooltip>
                        </q-btn>
                        <q-btn
                          round
                          flat
                          dense
                          color="warning"
                          icon="pause"
                          @click="pauseConsultation(patient)"
                          size="sm"
                          v-if="patient.isCurrent"
                        >
                          <q-tooltip>Pause Consultation</q-tooltip>
                        </q-btn>
                        <q-btn
                          round
                          flat
                          dense
                          color="negative"
                          icon="close"
                          @click="removeFromQueue(patient)"
                          size="sm"
                        >
                          <q-tooltip>Remove from Queue</q-tooltip>
                        </q-btn>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Priority Queue Section -->
              <div class="queue-section priority-queue-section">
                <div class="queue-section-header">
                  <h6 class="queue-section-title">
                    <q-icon name="priority_high" color="negative" />
                    Priority Queue
                  </h6>
                  <q-chip color="negative" text-color="white" size="sm" :label="`${priorityQueue.length} patients`" />
                </div>
                
                <div class="queue-section-content">
                  <div v-if="priorityQueue.length === 0" class="empty-queue">
                    <q-icon name="priority_high" size="2rem" color="grey-4" />
                    <p>No patients in priority queue</p>
                    <q-btn
                      color="negative"
                      label="Add Priority Patient"
                      icon="add"
                      size="sm"
                      @click="addPriorityPatient"
                    />
                  </div>
                  
                  <div v-else class="queue-items">
                    <div
                      v-for="(patient, index) in priorityQueue"
                      :key="patient.id"
                      class="queue-item priority"
                      :class="{ 
                        'current-patient': patient.isCurrent,
                        'next-in-line': index === 0 && !patient.isCurrent
                      }"
                    >
                      <div class="patient-info">
                        <div class="patient-number priority">
                          <div class="priority-level">{{ patient.priorityLevel || 'PWD' }}</div>
                          <div class="queue-number">{{ patient.queueNumber }}</div>
                        </div>
                        <div class="patient-details">
                          <div class="patient-name">{{ patient.name }}</div>
                          <div class="patient-time">Arrived: {{ patient.arrivalTime }}</div>
                          <div class="patient-priority">{{ patient.priorityReason }}</div>
                          <div class="patient-status" v-if="patient.isCurrent">
                            <q-chip color="positive" text-color="white" size="sm" label="In Progress" />
                          </div>
                        </div>
                      </div>
                      <div class="patient-actions">
                        <q-btn
                          round
                          flat
                          dense
                          color="primary"
                          icon="visibility"
                          @click="viewPatient(patient)"
                          size="sm"
                        >
                          <q-tooltip>View Details</q-tooltip>
                        </q-btn>
                        <q-btn
                          round
                          flat
                          dense
                          color="positive"
                          icon="play_arrow"
                          @click="startConsultation(patient)"
                          size="sm"
                          v-if="!patient.isCurrent"
                        >
                          <q-tooltip>Start Consultation</q-tooltip>
                        </q-btn>
                        <q-btn
                          round
                          flat
                          dense
                          color="warning"
                          icon="pause"
                          @click="pauseConsultation(patient)"
                          size="sm"
                          v-if="patient.isCurrent"
                        >
                          <q-tooltip>Pause Consultation</q-tooltip>
                        </q-btn>
                        <q-btn
                          round
                          flat
                          dense
                          color="negative"
                          icon="close"
                          @click="removeFromQueue(patient)"
                          size="sm"
                        >
                          <q-tooltip>Remove from Queue</q-tooltip>
                        </q-btn>
                      </div>
                    </div>
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

// Type definitions for error handling
interface ApiErrorResponse {
  profile_picture?: string[]
  detail?: string
}

interface ApiError {
  response?: {
    data?: ApiErrorResponse
  }
}

const router = useRouter()
const $q = useQuasar()
// Patient interface
interface Patient {
  id: number
  name: string
  queueNumber: string
  arrivalTime: string
  priorityReason?: string
  priorityLevel?: string
  isCurrent: boolean
}

const rightDrawerOpen = ref(false)
const text = ref('')
const fileInput = ref<HTMLInputElement>()

// Carousel variables (removed but keeping for potential future use)
// const slide = ref(1)
// const autoplay = ref(true)

// Dashboard statistics - empty data for nurses to input
const dashboardStats = ref({
  totalAppointments: 0,
  totalPatients: 0,
  normalQueue: 0,
  priorityQueue: 0,
  notifications: 0,
  pendingAssessment: 0,
  todaySchedule: 0,
  completedPatients: 0,
  emergencyCases: 0,
  averageWaitTime: 0
})

// Queue data - empty for nurses to manage
const normalQueue = ref<Patient[]>([])
const priorityQueue = ref<Patient[]>([])

// Queue management variables
const estimatedWaitTime = ref(15)

// Real-time time and weather
const currentTime = ref('')
const weatherData = ref<{
  temperature: number
  condition: string
  location: string
  description: string
} | null>(null)
const weatherLoading = ref(false)
const weatherError = ref(false)
let timeInterval: NodeJS.Timeout | null = null

// Mock user profile data - replace with actual API call
const userProfile = ref<{
  full_name: string
  specialization?: string
  role: string
  profile_picture: string | null
}>({
  full_name: 'user',
  specialization: 'specialization',
  role: 'role',
  profile_picture: null
})

const userInitials = computed(() => {
  if (!userProfile.value.full_name) return 'U'
  return userProfile.value.full_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
})

// Dynamic greeting based on time of day
const greetingMessage = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning!'
  if (hour < 17) return 'Good Afternoon!'
  return 'Good Evening!'
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
  
  // If it's a relative path, construct the full URL
  if (userProfile.value.profile_picture.startsWith('/')) {
    return `http://localhost:8000${userProfile.value.profile_picture}`
  }
  
  // If it's just a filename, construct the full URL
  return `http://localhost:8000/media/profile_pictures/${userProfile.value.profile_picture}`
})

// Update current time
const updateTime = () => {
  const now = new Date()
  
  // Convert to 12-hour format with AM/PM beside the time
  const hour = now.getHours()
  const ampm = hour >= 12 ? 'PM' : 'AM'
  const hour12 = hour % 12 || 12
  const minute = now.getMinutes().toString().padStart(2, '0')
  const second = now.getSeconds().toString().padStart(2, '0')
  
  currentTime.value = `${hour12}:${minute}:${second} ${ampm}`
}

// Get weather icon based on condition
const getWeatherIcon = (condition: string) => {
  const iconMap: Record<string, string> = {
    'clear': 'wb_sunny',
    'clouds': 'cloud',
    'rain': 'opacity',
    'snow': 'ac_unit',
    'thunderstorm': 'flash_on',
    'drizzle': 'grain',
    'mist': 'cloud',
    'fog': 'cloud',
    'haze': 'cloud',
    'smoke': 'cloud',
    'dust': 'cloud',
    'sand': 'cloud',
    'ash': 'cloud',
    'squall': 'air',
    'tornado': 'air'
  }
  return iconMap[condition.toLowerCase()] || 'wb_sunny'
}

// Fetch weather data
const fetchWeather = async () => {
  weatherLoading.value = true
  weatherError.value = false
  
  try {
    // Get user's location (default to Manila if geolocation fails)
    let latitude = 14.5995 // Default: Manila
    let longitude = 120.9842
    
    if (navigator.geolocation) {
      try {
        const position = await new Promise<GeolocationPosition>((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject, {
            timeout: 5000,
            enableHighAccuracy: false
          })
        })
        latitude = position.coords.latitude
        longitude = position.coords.longitude
      } catch {
        console.log('Geolocation failed, using default location (Manila)')
      }
    }
    
    // Use OpenWeatherMap API
    const apiKey = '5c328a0059938745d143138d206eb570'
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}&units=metric`)
    
    if (!response.ok) {
      throw new Error('Weather API request failed')
    }
    
    const data = await response.json()
    
    weatherData.value = {
      temperature: Math.round(data.main.temp),
      condition: data.weather[0].main.toLowerCase(),
      location: data.name,
      description: data.weather[0].description
    }
    
  } catch (error) {
    console.error('Weather fetch error:', error)
    weatherError.value = true
    
    // Fallback weather data
    weatherData.value = {
      temperature: 22,
      condition: 'clear',
      location: 'Local Area',
      description: 'Partly cloudy'
    }
  } finally {
    weatherLoading.value = false
  }
}

const toggleRightDrawer = () => {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

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
      
      const response = await api.post('/users/profile/update/picture/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      userProfile.value.profile_picture = response.data.user.profile_picture
      
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
        const axiosError = error as ApiError
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

const navigateTo = (route: string) => {
  // Close drawer first
  rightDrawerOpen.value = false
  
  // Navigate to different sections (you can implement actual routing)
  switch (route) {
    case 'dashboard':
      // Already on dashboard
      break
    case 'appointments':
      void navigateToAppointments()
      break
               case 'messaging':
             void router.push('/doctor-messaging')
             break
    case 'patients':
      $q.notify({
        type: 'info',
        message: 'Patient Management page - Coming soon!',
        position: 'top',
        timeout: 3000
      })
      break
    case 'analytics':
      $q.notify({
        type: 'info',
        message: 'Analytics page - Coming soon!',
        position: 'top',
        timeout: 3000
      })
      break
    case 'settings':
      $q.notify({
        type: 'info',
        message: 'Settings page - Coming soon!',
        position: 'top',
        timeout: 3000
      })
      break
  }
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
}

// Fetch user profile from API
const fetchUserProfile = async () => {
  try {
    const response = await api.get('/users/profile/')
    const userData = response.data.user // The API returns nested user data
    
    userProfile.value = {
      full_name: userData.full_name,
      specialization: userData.doctor_profile?.specialization,
      role: userData.role,
      profile_picture: userData.profile_picture || null
    }
    
    console.log('User profile loaded:', userProfile.value)
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
    
    // Fallback to localStorage
    const userData = localStorage.getItem('user')
    if (userData) {
      const user = JSON.parse(userData)
      userProfile.value = {
        full_name: user.full_name,
        specialization: user.doctor_profile?.specialization,
        role: user.role,
        profile_picture: user.profile_picture || null
      }
    }
  }
}

// Fetch dashboard statistics
const fetchDashboardStats = async () => {
  try {
    const response = await api.get('/operations/dashboard/stats/')
    dashboardStats.value = {
      totalAppointments: response.data.total_appointments,
      totalPatients: response.data.total_patients,
      normalQueue: response.data.normal_queue,
      priorityQueue: response.data.priority_queue,
      notifications: response.data.notifications,
      pendingAssessment: response.data.pending_assessment,
      todaySchedule: response.data.today_schedule || 8,
      completedPatients: response.data.completed_patients || 5,
      emergencyCases: response.data.emergency_cases || 2,
      averageWaitTime: response.data.average_wait_time || 15
    }
    console.log('Dashboard stats loaded from API:', dashboardStats.value)
  } catch (error) {
    console.error('Failed to fetch dashboard stats, using fallback:', error)
    // Fallback data
    dashboardStats.value = {
      totalAppointments: 12,
      totalPatients: 8,
      normalQueue: 5,
      priorityQueue: 3,
      notifications: 4,
      pendingAssessment: 2,
      todaySchedule: 8,
      completedPatients: 5,
      emergencyCases: 2,
      averageWaitTime: 15
    }
  }
}

// Patient queue interface
interface PatientQueueRequest {
  id: number
  name: string
  priorityLevel?: 'normal' | 'pwd' | 'senior' | 'pregnant' | 'emergency'
  priorityReason?: string
  department: string
  timestamp: string
}

// Queue management methods
const addPatientToQueue = () => {
  // Simulate patient clicking "Get in Queue" button
  const newPatient: PatientQueueRequest = {
    id: Date.now(),
    name: `Patient ${normalQueue.value.length + 1}`,
    priorityLevel: 'normal',
    department: 'OPD',
    timestamp: new Date().toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    })
  }
  
  // Automatically add to normal queue
  const queueNumber = generateQueueNumber('N')
  const patient: Patient = {
    id: newPatient.id,
    name: newPatient.name,
    queueNumber: queueNumber,
    arrivalTime: newPatient.timestamp,
    isCurrent: false
  }
  
  normalQueue.value.push(patient)
  
  $q.notify({
    type: 'positive',
    message: `Patient ${patient.name} automatically added to normal queue (${queueNumber})`,
    position: 'top',
    timeout: 3000
  })
  
  // Update estimated wait time
  updateEstimatedWaitTime()
}

const callNextPatient = () => {
  $q.notify({
    type: 'info',
    message: 'Call next patient feature coming soon!',
    position: 'top'
  })
}

const manageQueue = () => {
  $q.notify({
    type: 'info',
    message: 'Queue management settings coming soon!',
    position: 'top'
  })
}

// Helper functions for queue management
const generateQueueNumber = (prefix: string): string => {
  const timestamp = Date.now().toString().slice(-6)
  return `${prefix}${timestamp}`
}

const updateEstimatedWaitTime = () => {
  const totalPatients = normalQueue.value.length + priorityQueue.value.length
  const avgTimePerPatient = 15 // minutes
  estimatedWaitTime.value = Math.max(5, totalPatients * avgTimePerPatient)
}

const addPriorityPatient = () => {
  // Simulate priority patient clicking "Get in Queue" button
  const priorityLevels = ['pwd', 'senior', 'pregnant', 'emergency']
  const randomPriority = priorityLevels[Math.floor(Math.random() * priorityLevels.length)]
  
  const newPatient: PatientQueueRequest = {
    id: Date.now(),
    name: `Priority Patient ${priorityQueue.value.length + 1}`,
    priorityLevel: randomPriority as 'normal' | 'pwd' | 'senior' | 'pregnant' | 'emergency',
    priorityReason: getPriorityReason(randomPriority || 'normal'),
    department: 'OPD',
    timestamp: new Date().toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    })
  }
  
  // Automatically add to priority queue
  const queueNumber = generateQueueNumber('P')
  const patient: Patient = {
    id: newPatient.id,
    name: newPatient.name,
    queueNumber: queueNumber,
    arrivalTime: newPatient.timestamp,
    isCurrent: false,
    ...(newPatient.priorityReason && { priorityReason: newPatient.priorityReason })
  }
  
  priorityQueue.value.push(patient)
  
  $q.notify({
    type: 'warning',
    message: `Priority patient ${patient.name} automatically added to priority queue (${queueNumber})`,
    position: 'top',
    timeout: 3000
  })
  
  // Update estimated wait time
  updateEstimatedWaitTime()
}

const getPriorityReason = (priorityLevel: string): string => {
  const reasons: Record<string, string> = {
    pwd: 'Person with Disability',
    senior: 'Senior Citizen (60+)',
    pregnant: 'Pregnant Patient',
    emergency: 'Emergency Case'
  }
  return reasons[priorityLevel] || 'Priority Patient'
}

const pauseConsultation = (patient: Patient) => {
  $q.notify({
    type: 'warning',
    message: `Paused consultation with ${patient.name}`,
    position: 'top'
  })
}

const removeFromQueue = (patient: Patient) => {
  $q.notify({
    type: 'negative',
    message: `Removed ${patient.name} from queue`,
    position: 'top'
  })
}

interface Patient {
  id: number
  name: string
  queueNumber: string
  arrivalTime: string
  isCurrent: boolean
  priorityReason?: string | undefined
}

const viewPatient = (patient: Patient) => {
  $q.notify({
    type: 'info',
    message: `Viewing patient: ${patient.name}`,
    position: 'top'
  })
}

const startConsultation = (patient: Patient) => {
  $q.notify({
    type: 'positive',
    message: `Starting consultation with: ${patient.name}`,
    position: 'top'
  })
}

// Navigation function
async function navigateToAppointments() {
  console.log('🔄 NAVIGATION STARTED: Navigating to appointments...')
  console.log('📍 Current route:', router.currentRoute.value.path)
  console.log('🗺️ Available routes:', router.getRoutes().map(r => ({ name: r.name, path: r.path })))
  
  try {
    await router.push({ name: 'DoctorAppointments' })
    console.log('Navigation successful with name')
  } catch (error) {
    console.error('Navigation error with name:', error)
    try {
      await router.push('/doctor-appointments')
      console.log('Navigation successful with path')
    } catch (pathError) {
      console.error('Navigation error with path:', pathError)
      $q.notify({
        type: 'negative',
        message: 'Navigation failed: ' + String(pathError),
        position: 'top'
      })
    }
  }
}

onMounted(() => {
  // Load user profile data from API
  void fetchUserProfile()
  
  // Load dashboard statistics
  void fetchDashboardStats()
  
  // Initialize real-time features
  updateTime() // Set initial time
  timeInterval = setInterval(updateTime, 1000) // Update every second
  
  // Fetch weather data
  void fetchWeather()
  
  // Refresh weather every 30 minutes
  setInterval(() => void fetchWeather(), 30 * 60 * 1000)
})

// Cleanup on component unmount
onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
.search-container {
  display: flex;
  justify-content: center;
  width: 100%;
  padding: 0 20px;
}

.search-input {
  max-width: 600px;
  width: 100%;
}

/* Real-time info styles */
.real-time-info {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-left: 20px;
}

.time-display,
.weather-display,
.weather-loading,
.weather-error {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.time-display .q-icon,
.weather-display .q-icon {
  color: #286660;
}

.time-text,
.weather-text {
  font-size: 14px;
  font-weight: 500;
  color: #286660;
  white-space: nowrap;
}

.weather-location {
  font-size: 12px;
  color: #666;
  margin-left: 4px;
}

.weather-loading .q-spinner {
  color: #286660;
}

.weather-error .q-icon {
  color: #ff6b6b;
}

/* Greeting Section Styles */
.greeting-section {
  padding: 30px 20px;
  margin-bottom: 20px;
}

.greeting-content {
  max-width: 1200px;
  margin: 0 auto;
}

.greeting-text {
  color: #333;
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.greeting-subtitle {
  color: #666;
  font-size: 16px;
  margin: 0;
  font-weight: 400;
}

/* Carousel Section Styles */
.carousel-section {
  padding: 20px;
  margin-bottom: 20px;
}

.dashboard-carousel {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 1200px;
  margin: 0 auto;
}

/* Dashboard Statistics Styles */
.stats-section {
  padding: 20px;
  margin-bottom: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  margin-bottom: 10px;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 1rem;
  color: #666;
  margin-bottom: 10px;
}

.queue-breakdown {
  margin-top: 6px;
  font-size: 0.75rem;
  line-height: 1.2;
}

.queue-item {
  margin: 2px 0;
  display: flex;
  justify-content: center;
}

.queue-type {
  padding: 2px 6px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.7rem;
}

.queue-item {
  margin: 2px 0;
}

.queue-type {
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.queue-type.normal {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.queue-type.priority {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

/* Card-specific colors */
.appointments-card .stat-icon {
  color: #2196f3;
}

.queue-card .stat-icon {
  color: #ff9800;
}

.notifications-card .stat-icon {
  color: #9c27b0;
}

.assessment-card .stat-icon {
  color: #f44336;
}

.q-header {
  background: #286660 !important;
  position: fixed !important;
  top: 0;
  left: 0;
  right: 0;
  z-index: 2000;
}

.q-toolbar {
  background: #286660 !important;
}

.fixed-header {
  position: fixed !important;
  top: 0;
  left: 0;
  right: 0;
  z-index: 2000;
}

.page-container-with-fixed-header {
  padding-top: 98px !important;
}

.q-avatar {
  background: white;
  border-radius: 8px;
}

.q-avatar img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Drawer Styles */
.drawer-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.user-profile-section {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.profile-picture-container {
  position: relative;
  display: inline-block;
  margin-bottom: 15px;
}

.profile-avatar {
  border: 3px solid #1e7668;
}

.profile-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1e7668;
  color: white;
  font-size: 24px;
  font-weight: bold;
  border-radius: 50%;
}

.upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #1e7668 !important;
}

.user-info {
  margin-top: 10px;
}

.user-name {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.user-specialization {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
}

.navigation-menu {
  flex: 1;
  padding: 10px 0;
}

.nav-item {
  margin: 5px 10px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background: rgba(30, 118, 104, 0.1);
}

.nav-item .q-icon {
  color: #1e7668;
}

.logout-section {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
}

.logout-btn {
  width: 100%;
}

/* Dashboard Cards Section - All 8 cards in one row */
.dashboard-cards-section {
  padding: 20px;
  margin-bottom: 20px;
}

.dashboard-cards-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 15px;
  max-width: 1400px;
  margin: 0 auto;
  overflow-x: auto;
}

.dashboard-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
  min-width: 160px;
  height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 15px 10px;
}

.dashboard-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-icon {
  margin-bottom: 8px;
  display: flex;
  justify-content: center;
}

.card-number {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 4px;
  line-height: 1.2;
}

.card-label {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 6px;
  line-height: 1.2;
}

.text-caption {
  font-size: 0.7rem;
  line-height: 1.2;
  margin-bottom: 0;
}

/* Card-specific colors */
.schedule-card .card-icon {
  color: #2196f3;
}

.completed-card .card-icon {
  color: #4caf50;
}

.emergency-card .card-icon {
  color: #f44336;
}

.wait-time-card .card-icon {
  color: #ff9800;
}

.appointments-card .card-icon {
  color: #2196f3;
}

.queue-card .card-icon {
  color: #ff9800;
}

.notifications-card .card-icon {
  color: #9c27b0;
}

.assessment-card .card-icon {
  color: #f44336;
}

/* Queueing System Styles */
.queueing-section {
  padding: 20px;
  margin-bottom: 20px;
}

.queueing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.queueing-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.queueing-actions {
  display: flex;
  gap: 10px;
}



.combined-queue-card {
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.combined-queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
}

.combined-queue-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #333;
}

.combined-queue-stats {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.combined-queue-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  min-height: 500px;
}

.queue-section {
  border-radius: 8px;
  padding: 15px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
}

.normal-queue-section {
  border-left: 4px solid #2196f3;
}

.priority-queue-section {
  border-left: 4px solid #f44336;
}

.queue-section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #dee2e6;
}

.queue-section-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
}

.queue-section-content {
  flex: 1;
  overflow-y: auto;
  max-height: 400px;
}

/* Responsive design for combined queue layout */
@media (max-width: 768px) {
  .combined-queue-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .combined-queue-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .combined-queue-stats {
    justify-content: flex-start;
  }
  
  .queue-section-content {
    max-height: 300px;
  }
}

@media (max-width: 480px) {
  .combined-queue-card {
    margin: 0 10px;
  }
  
  .queue-section {
    padding: 10px;
  }
  
  .queue-section-content {
    max-height: 250px;
  }
}

.queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.queue-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.queue-stats {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.queue-list {
  flex: 1;
  overflow-y: auto;
}

.empty-queue {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  text-align: center;
}

.empty-queue p {
  margin: 10px 0 0 0;
  font-size: 14px;
}

.queue-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.queue-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  background: #f8f9fa;
  border-left: 4px solid #2196f3;
  transition: all 0.2s ease;
}

.queue-item:hover {
  background: #e3f2fd;
  transform: translateX(5px);
}

.queue-item.priority {
  border-left-color: #f44336;
  background: #ffebee;
}

.queue-item.priority:hover {
  background: #ffcdd2;
}

.queue-item.current-patient {
  background: #e8f5e8;
  border-left-color: #4caf50;
}

.queue-item.next-in-line {
  background: #fff3e0;
}

/* Responsive design for queue layout */
@media (max-width: 768px) {
  .queueing-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    padding: 0 15px;
  }
  
  .queue-card {
    height: auto;
    min-height: 400px;
  }
}

@media (max-width: 480px) {
  .queueing-grid {
    padding: 0 10px;
  }
  
  .queue-card {
    min-height: 350px;
  }
}

.queue-item.next-in-line {
  border-left-color: #ff9800;
}

.patient-info {
  display: flex;
  align-items: center;
  gap: 15px;
  flex: 1;
}

.patient-number {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.queue-position {
  background: #2196f3;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 10px;
}

.queue-number {
  background: #2196f3;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 12px;
}

.patient-number.priority .queue-position {
  background: #f44336;
}

.patient-number.priority .queue-number {
  background: #f44336;
}

.priority-level {
  background: #ff9800;
  color: white;
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 8px;
  font-weight: bold;
  text-transform: uppercase;
}

.patient-details {
  flex: 1;
}

.patient-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 2px;
}

.patient-time {
  font-size: 12px;
  color: #666;
}

.patient-priority {
  font-size: 11px;
  color: #f44336;
  font-weight: 500;
  margin-top: 2px;
}

.patient-actions {
  display: flex;
  gap: 5px;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .dashboard-cards-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
  }
  
  .dashboard-card {
    height: 120px;
    padding: 12px 8px;
  }
  
  .card-number {
    font-size: 1.4rem;
  }
  
  .card-label {
    font-size: 0.75rem;
  }
  
  .text-caption {
    font-size: 0.65rem;
  }
}

@media (max-width: 768px) {
  .queueing-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .dashboard-cards-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .dashboard-card {
    height: 110px;
    padding: 10px 6px;
  }
  
  .card-number {
    font-size: 1.2rem;
  }
  
  .card-label {
    font-size: 0.7rem;
  }
  
  .text-caption {
    font-size: 0.6rem;
  }
}

@media (max-width: 480px) {
  .dashboard-cards-grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .dashboard-card {
    height: 100px;
    padding: 8px 4px;
  }
  
  .card-number {
    font-size: 1.1rem;
  }
  
  .card-label {
    font-size: 0.65rem;
  }
  
  .text-caption {
    font-size: 0.55rem;
  }
}
</style>