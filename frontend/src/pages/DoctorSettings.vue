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
            placeholder="Search appointments, patients..."
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
    <q-page-container class="page-background">
      <div class="settings-page">
        <div class="settings-container">
          <div class="settings-header">
            <h2>Account Settings</h2>
            <p>Customize your MediSync experience</p>
          </div>

          <div class="settings-content">
            <!-- Profile Settings Section -->
            <q-card class="settings-card">
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
            </q-card>

            <!-- Appearance Settings Section -->
            <q-card class="settings-card">
              <q-card-section>
                <div class="text-h6">Appearance</div>
                <p class="text-caption">Customize the look and feel of your interface</p>
              </q-card-section>
              
              <q-card-section>
                <!-- Dark/Light Mode Toggle -->
                <div class="setting-item">
                  <div class="setting-label">
                    <q-icon name="dark_mode" class="q-mr-sm" />
                    <span>Dark Mode</span>
                  </div>
                  <q-toggle
                    v-model="settings.darkMode"
                    @update:model-value="toggleDarkMode"
                    color="primary"
                  />
                </div>

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
            </q-card>

            <!-- Notification Settings Section -->
            <q-card class="settings-card">
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
            </q-card>

            <!-- Save Settings Button -->
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

// User profile data
const userProfile = ref({
  full_name: '',
  email: '',
  specialization: '',
  role: '',
  profile_picture: ''
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
  darkMode: false,
  textSize: 16,
  fontFamily: 'Roboto',
  emailNotifications: true,
  appointmentReminders: true,
  messageNotifications: true
})

// File input reference
const fileInput = ref<HTMLInputElement>()

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
const profilePictureUrl = computed(() => {
  return userProfile.value.profile_picture || null
})

const userInitials = computed(() => {
  if (!userProfile.value.full_name) return 'U'
  return userProfile.value.full_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

// Router and Quasar
const router = useRouter()
// const route = useRoute() // Unused variable
const $q = useQuasar()

// Methods
const toggleRightDrawer = () => {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

const navigateTo = (path: string) => {
  void router.push(`/${path}`)
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
}

const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleProfilePictureUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files || target.files.length === 0) return

  const file = target.files[0]
  if (!file) return
  
  const formData = new FormData()
  formData.append('profile_picture', file)

  try {
    const response = await api.patch('/users/profile/picture/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    userProfile.value.profile_picture = response.data.profile_picture

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

    // Clear the file input
    target.value = ''
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
const toggleDarkMode = (value: boolean) => {
  settings.value.darkMode = value
  // Apply dark mode to the application
  document.body.classList.toggle('dark-mode', value)
  localStorage.setItem('darkMode', value.toString())
}

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
    darkMode: false,
    textSize: 16,
    fontFamily: 'Roboto',
    emailNotifications: true,
    appointmentReminders: true,
    messageNotifications: true
  }
  
  // Reset CSS variables
  document.documentElement.style.removeProperty('--text-size')
  document.documentElement.style.removeProperty('--font-family')
  document.body.classList.remove('dark-mode')
  
  // Clear localStorage
  localStorage.removeItem('darkMode')
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
    userProfile.value = response.data
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
  }
}

const loadSettings = () => {
  // Load settings from localStorage
  const darkMode = localStorage.getItem('darkMode') === 'true'
  const textSize = parseInt(localStorage.getItem('textSize') || '16')
  const fontFamily = localStorage.getItem('fontFamily') || 'Roboto'
  
  settings.value.darkMode = darkMode
  settings.value.textSize = textSize
  settings.value.fontFamily = fontFamily
  
  // Apply settings
  toggleDarkMode(darkMode)
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
  background: url('/background.png') no-repeat center center;
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
</style>