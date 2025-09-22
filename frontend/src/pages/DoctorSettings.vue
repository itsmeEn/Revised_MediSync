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

          <q-item clickable v-ripple @click="navigateTo('settings')" class="nav-item active">
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

    <!-- Main Content -->
    <q-page-container class="page-container-with-fixed-header">
      <!-- Account Settings Section -->
      <div class="greeting-section">
        <q-card class="greeting-card">
          <q-card-section class="greeting-content">
            <h2 class="greeting-text">Account Settings</h2>
            <p class="greeting-subtitle">Customize your MediSync experience</p>
          </q-card-section>
        </q-card>
      </div>

      <div class="settings-page">
        <div class="settings-container">
          <div class="settings-content">
            <!-- All Settings in One Card -->
            <q-card class="settings-card">
              <!-- Profile Information Section -->
              <q-card-section>
                <div class="text-h6">Profile Information</div>
                <p class="text-caption">Your basic account information (read-only)</p>
              </q-card-section>
              
              <q-card-section>
                <div class="row q-col-gutter-md">
                  <div class="col-12 col-md-6">
                    <q-input
                      v-model="userProfile.full_name"
                      label="Full Name"
                      readonly
                      outlined
                      dense
                    >
                      <template v-slot:prepend>
                        <q-icon name="person" />
                      </template>
                    </q-input>
                  </div>
                  
                  <div class="col-12 col-md-6">
                    <q-input
                      v-model="userProfile.email"
                      label="Email Address"
                      readonly
                      outlined
                      dense
                    >
                      <template v-slot:prepend>
                        <q-icon name="email" />
                      </template>
                    </q-input>
                  </div>
                  
                  <div class="col-12 col-md-6">
                    <q-input
                      v-model="userProfile.role"
                      label="Role"
                      readonly
                      outlined
                      dense
                    >
                      <template v-slot:prepend>
                        <q-icon name="badge" />
                      </template>
                    </q-input>
                  </div>
                  
                  <div class="col-12 col-md-6">
                    <q-input
                      v-model="userProfile.specialization"
                      label="Specialization"
                      readonly
                      outlined
                      dense
                    >
                      <template v-slot:prepend>
                        <q-icon name="medical_services" />
                      </template>
                    </q-input>
                  </div>
                </div>
              </q-card-section>

              <!-- Appearance Section -->
              <q-card-section>
                <div class="text-h6">Appearance</div>
                <p class="text-caption">Customize the look and feel of your interface</p>
              </q-card-section>
              
              <q-card-section>
                <!-- Text Size Setting -->
                <div class="setting-item">
                  <div class="setting-label">
                    <q-icon name="text_fields" class="q-mr-sm" />
                    <span>Text Size</span>
                  </div>
                  <q-slider
                    v-model="settings.textSize"
                    :min="12"
                    :max="24"
                    :step="1"
                    label
                    label-always
                    color="primary"
                    class="q-mt-md"
                    @update:model-value="updateTextSize"
                  />
                </div>

                <!-- Font Family Setting -->
                <div class="setting-item">
                  <div class="setting-label">
                    <q-icon name="font_download" class="q-mr-sm" />
                    <span>Font Family</span>
                  </div>
                  <q-select
                    v-model="settings.fontFamily"
                    :options="fontOptions"
                    outlined
                    dense
                    class="q-mt-sm"
                    @update:model-value="updateFontFamily"
                  />
                </div>
              </q-card-section>

              <!-- Notifications Section -->
              <q-card-section>
                <div class="text-h6">Notifications</div>
                <p class="text-caption">Manage your notification preferences</p>
              </q-card-section>
              
              <q-card-section>
                <div class="setting-item">
                  <div class="setting-label">
                    <q-icon name="notifications" class="q-mr-sm" />
                    <span>Email Notifications</span>
                  </div>
                  <q-toggle
                    v-model="settings.emailNotifications"
                    color="primary"
                  />
                </div>

                <div class="setting-item">
                  <div class="setting-label">
                    <q-icon name="schedule" class="q-mr-sm" />
                    <span>Appointment Reminders</span>
                  </div>
                  <q-toggle
                    v-model="settings.appointmentReminders"
                    color="primary"
                  />
                </div>

                <div class="setting-item">
                  <div class="setting-label">
                    <q-icon name="message" class="q-mr-sm" />
                    <span>Message Notifications</span>
                  </div>
                  <q-toggle
                    v-model="settings.messageNotifications"
                    color="primary"
                  />
                </div>
              </q-card-section>

              <!-- Action Buttons -->
              <q-card-section>
                <div class="settings-actions">
                  <q-btn
                    color="primary"
                    label="Save Settings"
                    icon="save"
                    @click="saveSettings"
                    :loading="saving"
                  />
                  <q-btn
                    color="secondary"
                    label="Reset to Default"
                    icon="restore"
                    @click="resetSettings"
                    class="q-ml-md"
                  />
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from '../boot/axios'
// import { AxiosError } from 'axios' // Unused import

// Reactive data
const rightDrawerOpen = ref(false)
const text = ref('')
// const loading = ref(false) // Unused variable
const saving = ref(false)

// Header functions
const toggleRightDrawer = () => {
  console.log('Toggle drawer called, current state:', rightDrawerOpen.value)
  rightDrawerOpen.value = !rightDrawerOpen.value
  console.log('New state:', rightDrawerOpen.value)
}



// User profile data
const userProfile = ref({
  full_name: '',
  email: '',
  specialization: '',
  role: '',
  profile_picture: '',
  verification_status: 'approved'
})

// Real-time data
const currentTime = ref('')
const weatherData = ref<{
  temperature: number
  condition: string
  location: string
} | null>(null)
const weatherLoading = ref(false)
const weatherError = ref(false)
const timeInterval = ref<ReturnType<typeof setInterval> | null>(null)

// Settings data
const settings = ref({
  textSize: 16,
  fontFamily: 'Roboto',
  emailNotifications: true,
  appointmentReminders: true,
  messageNotifications: true
})

// File input reference for profile picture upload
const fileInput = ref<HTMLInputElement | null>(null)

// Font options
const fontOptions = [
  { label: 'Roboto', value: 'Roboto' },
  { label: 'Arial', value: 'Arial' },
  { label: 'Helvetica', value: 'Helvetica' },
  { label: 'Times New Roman', value: 'Times New Roman' },
  { label: 'Georgia', value: 'Georgia' },
  { label: 'Verdana', value: 'Verdana' }
]

// Computed properties
const userInitials = computed(() => {
  if (!userProfile.value.full_name) return 'U'
  const names = userProfile.value.full_name.split(' ')
  if (names.length >= 2) {
    return `${names[0]?.charAt(0) || ''}${names[names.length - 1]?.charAt(0) || ''}`.toUpperCase()
  }
  return userProfile.value.full_name.charAt(0).toUpperCase()
})

const profilePictureUrl = computed(() => {
  if (!userProfile.value.profile_picture) {
    return null
  }
  
  if (userProfile.value.profile_picture.startsWith('http')) {
    return userProfile.value.profile_picture
  }
  
  return `http://localhost:8000${userProfile.value.profile_picture}`
})


// Router and Quasar
const router = useRouter()
// const route = useRoute() // Unused variable
const $q = useQuasar()

// Methods

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
      // Already on settings page
      break
    default:
      void router.push(`/${route}`)
  }
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
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

// Real-time functions
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', {
    hour12: true,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const fetchWeather = async () => {
  if (!navigator.geolocation) {
    weatherError.value = true
    return
  }

  weatherLoading.value = true
  weatherError.value = false

  try {
    const position = await new Promise<GeolocationPosition>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject)
    })

    const { latitude, longitude } = position.coords
    const apiKey = 'YOUR_OPENWEATHER_API_KEY' // Replace with actual API key
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}&units=metric`
    )

    if (!response.ok) throw new Error('Weather API request failed')

    const data = await response.json()
    weatherData.value = {
      temperature: Math.round(data.main.temp),
      condition: data.weather[0].main.toLowerCase(),
      location: data.name
    }
  } catch (error) {
    console.error('Weather fetch error:', error)
    weatherError.value = true
  } finally {
    weatherLoading.value = false
  }
}

const getWeatherIcon = (condition: string): string => {
  const iconMap: Record<string, string> = {
    clear: 'wb_sunny',
    clouds: 'cloud',
    rain: 'opacity',
    snow: 'ac_unit',
    thunderstorm: 'flash_on',
    drizzle: 'grain',
    mist: 'cloud',
    smoke: 'cloud',
    haze: 'cloud',
    dust: 'cloud',
    fog: 'cloud',
    sand: 'cloud',
    ash: 'cloud',
    squall: 'air',
    tornado: 'air'
  }
  return iconMap[condition] || 'wb_sunny'
}

// Settings functions

const updateTextSize = (size: number | null) => {
  if (size === null) return
  settings.value.textSize = size
  // Apply text size to the application
  document.documentElement.style.setProperty('--text-size', `${size}px`)
  localStorage.setItem('textSize', size.toString())
}

const updateFontFamily = (font: string) => {
  settings.value.fontFamily = font
  // Apply font family to the application
  document.documentElement.style.setProperty('--font-family', font)
  localStorage.setItem('fontFamily', font)
}

const saveSettings = async () => {
  saving.value = true
  
  try {
    // Save settings to backend
    await api.post('/users/settings/', settings.value)
    
    $q.notify({
      type: 'positive',
      message: 'Settings saved successfully!',
      position: 'top',
      timeout: 3000
    })
  } catch (error) {
    console.error('Failed to save settings:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to save settings. Please try again.',
      position: 'top',
      timeout: 4000
    })
  } finally {
    saving.value = false
  }
}

const resetSettings = () => {
  settings.value = {
    textSize: 16,
    fontFamily: 'Roboto',
    emailNotifications: true,
    appointmentReminders: true,
    messageNotifications: true
  }
  
  // Reset CSS variables
  document.documentElement.style.removeProperty('--text-size')
  document.documentElement.style.removeProperty('--font-family')
  
  // Clear localStorage
  localStorage.removeItem('textSize')
  localStorage.removeItem('fontFamily')
  
  $q.notify({
    type: 'info',
    message: 'Settings reset to default values',
    position: 'top',
    timeout: 3000
  })
}

const fetchUserProfile = async () => {
  try {
    const response = await api.get('/users/profile/')
    const userData = response.data.user || response.data
    
    // Check localStorage for updated profile picture
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
    
    userProfile.value = {
      full_name: userData.full_name,
      email: userData.email,
      specialization: userData.doctor_profile?.specialization || userData.specialization,
      role: userData.role,
      profile_picture: storedUser.profile_picture || userData.profile_picture || null,
      verification_status: userData.verification_status
    }
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
  }
}

const loadSettings = () => {
  // Load settings from localStorage
  const textSize = parseInt(localStorage.getItem('textSize') || '16')
  const fontFamily = localStorage.getItem('fontFamily') || 'Roboto'
  
  settings.value.textSize = textSize
  settings.value.fontFamily = fontFamily
  
  // Apply settings
  updateTextSize(textSize)
  updateFontFamily(fontFamily)
}

// Lifecycle hooks
onMounted(() => {
  void fetchUserProfile()
  loadSettings()
  
  // Initialize real-time features
  updateTime()
  timeInterval.value = setInterval(updateTime, 1000)
  void fetchWeather()
})

onUnmounted(() => {
  if (timeInterval.value) {
    clearInterval(timeInterval.value)
  }
})
</script>

<style scoped>
.page-background {
  background: #f8f9fa;
  background-size: cover;
  min-height: 100vh;
}

.settings-page {
  /* background-color: #f5f5f5; */
  min-height: 100vh;
  padding: 20px;
}

.settings-container {
  max-width: 800px;
  margin: 0 auto;
}

.settings-header {
  text-align: center;
  margin-bottom: 30px;
}

.settings-header h2 {
  color: #286660;
  margin-bottom: 10px;
}

.settings-header p {
  color: #666;
  font-size: 16px;
}

.settings-card {
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-label {
  display: flex;
  align-items: center;
  font-weight: 500;
  color: #333;
}

.settings-actions {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  padding: 20px;
}

/* Real-time info styles */
.real-time-info {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-left: auto;
}

.time-display,
.weather-display,
.weather-loading,
.weather-error {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  padding: 8px 12px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
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

/* Drawer styles */
.drawer-content {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.user-profile-section {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.profile-picture-container {
  position: relative;
  display: inline-block;
  margin-bottom: 15px;
}

.upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  transform: translate(25%, 25%);
}

.profile-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #286660;
  color: white;
  font-weight: bold;
  font-size: 24px;
}

.user-name {
  margin: 0 0 5px 0;
  color: #333;
  font-weight: 600;
}

.user-specialization {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
}

.navigation-menu {
  flex: 1;
}

.nav-item {
  margin-bottom: 5px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.nav-item:hover {
  background-color: #f0f0f0;
}

.nav-item.active {
  background-color: #286660;
  color: white;
}

.logout-section {
  margin-top: auto;
  padding-top: 20px;
}

.logout-btn {
  width: 100%;
}

/* Search container */
.search-container {
  flex: 1;
  max-width: 400px;
  margin-right: 20px;
}

.search-input {
  width: 100%;
}

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
  z-index: 2000;
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #f8f9fa;
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

/* Page Container with Off-White Background */
.page-container-with-fixed-header {
  background: #f8f9fa;
  min-height: 100vh;
  position: relative;
}

/* Prototype Header Styles */

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

</style>