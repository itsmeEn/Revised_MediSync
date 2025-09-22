<template>
  <q-layout view="hHh Lpr fFf">

    <q-header reveal elevated class="text-white" height-hint="98">
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
            placeholder="Search patients, medications, tasks..."
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
            <p class="user-specialization">{{ userProfile.department }}</p>
            <q-chip color="primary" text-color="white" size="sm">
              {{ userProfile.role }}
            </q-chip>
          </div>
        </div>

        <!-- Navigation Menu -->
        <q-list class="navigation-menu">
          <q-item clickable v-ripple @click="navigateTo('nurse-dashboard')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('patient-assessment')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="assignment" />
            </q-item-section>
            <q-item-section>Patient Assessment</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('medicine-inventory')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="medication" />
            </q-item-section>
            <q-item-section>Medicine Inventory</q-item-section>
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

    <q-page-container class="page-background">
      <!-- Greeting Section -->
      <div class="greeting-section">
        <div class="greeting-content">
          <h2 class="greeting-text">
            {{ greetingMessage }} {{ userProfile.role.charAt(0).toUpperCase() + userProfile.role.slice(1) }}
          </h2>
          <p class="greeting-subtitle">Manage patient care and medical inventory</p>
        </div>
      </div>
      
      <!-- Carousel Section -->
      <div class="carousel-section">
        <q-carousel
          animated
          v-model="slide"
          navigation
          infinite
          :autoplay="autoplay"
          arrows
          transition-prev="slide-right"
          transition-next="slide-left"
          @mouseenter="autoplay = false"
          @mouseleave="autoplay = true"
          class="dashboard-carousel"
        >
          <q-carousel-slide :name="1" img-src="https://cdn.quasar.dev/img/mountains.jpg" />
          <q-carousel-slide :name="2" img-src="https://cdn.quasar.dev/img/parallax1.jpg" />
          <q-carousel-slide :name="3" img-src="https://cdn.quasar.dev/img/parallax2.jpg" />
          <q-carousel-slide :name="4" img-src="https://cdn.quasar.dev/img/quasar.jpg" />
        </q-carousel>
      </div>
      
      <!-- Dashboard Statistics Cards -->
      <div class="stats-section">
        <div class="stats-grid">
          <!-- Patients Under Care Card -->
          <q-card class="stat-card patients-card">
            <q-card-section class="text-center">
              <div class="stat-icon">
                <q-icon name="people" size="2rem" />
              </div>
              <div class="stat-number">{{ dashboardStats.patientsUnderCare }}</div>
              <div class="stat-label">Patients Under Care</div>
              <div class="text-caption text-grey-6">Currently assigned patients</div>
            </q-card-section>
          </q-card>

          <!-- Pending Tasks Card -->
          <q-card class="stat-card tasks-card">
            <q-card-section class="text-center">
              <div class="stat-icon">
                <q-icon name="assignment" size="2rem" />
              </div>
              <div class="stat-number">{{ dashboardStats.pendingTasks }}</div>
              <div class="stat-label">Pending Tasks</div>
              <div class="tasks-breakdown">
                <div class="task-item">
                  <span class="task-type urgent">Urgent: {{ dashboardStats.urgentTasks }}</span>
                </div>
                <div class="task-item">
                  <span class="task-type routine">Routine: {{ dashboardStats.routineTasks }}</span>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Vitals Checked Card -->
          <q-card class="stat-card vitals-card">
            <q-card-section class="text-center">
              <div class="stat-icon">
                <q-icon name="favorite" size="2rem" />
              </div>
              <div class="stat-number">{{ dashboardStats.vitalsChecked }}</div>
              <div class="stat-label">Vitals Checked Today</div>
            </q-card-section>
          </q-card>

          <!-- Medications Administered Card -->
          <q-card class="stat-card medications-card">
            <q-card-section class="text-center">
              <div class="stat-icon">
                <q-icon name="medication" size="2rem" />
              </div>
              <div class="stat-number">{{ dashboardStats.medicationsAdministered }}</div>
              <div class="stat-label">Medications Given</div>
            </q-card-section>
          </q-card>
        </div>
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
const rightDrawerOpen = ref(false)
const text = ref('')
const fileInput = ref<HTMLInputElement>()

// Carousel variables
const slide = ref(1)
const autoplay = ref(true)

// Dashboard statistics
const dashboardStats = ref({
  patientsUnderCare: 0,
  pendingTasks: 0,
  urgentTasks: 0,
  routineTasks: 0,
  vitalsChecked: 0,
  medicationsAdministered: 0
})

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
  department?: string
  role: string
  profile_picture: string | null
}>({
  full_name: 'Nurse',
  department: 'General Ward',
  role: 'nurse',
  profile_picture: null
})

const userInitials = computed(() => {
  if (!userProfile.value.full_name) return 'N'
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
  
  // Navigate to different sections
  switch (route) {
    case 'nurse-dashboard':
      // Already on dashboard
      break
    case 'patient-assessment':
      void router.push('/nurse-patient-assessment')
      break
    case 'medicine-inventory':
      void router.push('/nurse-medicine-inventory')
      break
    case 'analytics':
      void router.push('/nurse-analytics')
      break
    case 'settings':
      void router.push('/nurse-settings')
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
      department: userData.nurse_profile?.department,
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
        department: user.nurse_profile?.department,
        role: user.role,
        profile_picture: user.profile_picture || null
      }
    }
  }
}

// Fetch dashboard statistics
const fetchDashboardStats = () => {
  try {
    // Mock data for now - replace with actual API call
    dashboardStats.value = {
      patientsUnderCare: 12,
      pendingTasks: 8,
      urgentTasks: 3,
      routineTasks: 5,
      vitalsChecked: 15,
      medicationsAdministered: 22
    }
    console.log('Dashboard stats loaded:', dashboardStats.value)
  } catch (error) {
    console.error('Failed to fetch dashboard stats, using fallback:', error)
    // Fallback data
    dashboardStats.value = {
      patientsUnderCare: 0,
      pendingTasks: 0,
      urgentTasks: 0,
      routineTasks: 0,
      vitalsChecked: 0,
      medicationsAdministered: 0
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
.page-background {
  background: url('/background.png') no-repeat center center;
  background-size: cover;
  min-height: 100vh;
}

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

.tasks-breakdown {
  margin-top: 10px;
  font-size: 0.9rem;
}

.task-item {
  margin: 2px 0;
}

.task-type {
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.task-type.urgent {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.task-type.routine {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

/* Card-specific colors */
.patients-card .stat-icon {
  color: #2196f3;
}

.tasks-card .stat-icon {
  color: #ff9800;
}

.vitals-card .stat-icon {
  color: #e91e63;
}

.medications-card .stat-icon {
  color: #4caf50;
}

.q-header {
  background: #286660 !important;
}

.q-toolbar {
  background: #286660 !important;
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
</style>
