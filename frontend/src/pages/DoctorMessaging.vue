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
            placeholder="Search messages, patients..."
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

          <q-item clickable v-ripple @click="navigateTo('messaging')" class="nav-item active">
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

    <q-page-container class="page-background">
      <!-- Page Header -->
      <div class="page-header">
        <div class="page-header-left">
          <h2 class="page-title">Messaging</h2>
          <p class="page-subtitle">Communicate with patients and staff</p>
        </div>
        <div class="page-header-right">
          <q-btn 
            color="primary" 
            icon="add" 
            label="New Message" 
            @click="showNewMessageDialog = true"
          />
        </div>
      </div>

      <!-- Messaging Content -->
      <div class="messaging-container">
        <div class="q-pa-md row justify-center">
          <div style="width: 100%; max-width: 800px">
            <q-chat-message
              :text="['Have you seen Quasar?']"
              sent
              text-color="white"
              bg-color="primary"
            >
              <template v-slot:name>me</template>
              <template v-slot:stamp>7 minutes ago</template>
              <template v-slot:avatar>
                <img
                  class="q-message-avatar q-message-avatar--sent"
                  src="https://cdn.quasar.dev/img/avatar4.jpg"
                >
              </template>
            </q-chat-message>

            <q-chat-message
              bg-color="amber"
            >
              <template v-slot:name>Mary</template>
              <template v-slot:avatar>
                <img
                  class="q-message-avatar q-message-avatar--received"
                  src="https://cdn.quasar.dev/img/avatar2.jpg"
                >
              </template>

              <div>
                Already building an app with it...
                <img src="https://cdn.quasar.dev/img/discord-qeart.png" class="my-emoji">
              </div>

              <q-spinner-dots size="2rem" />
            </q-chat-message>
          </div>
        </div>
      </div>
    </q-page-container>

    <!-- New Message Dialog -->
    <q-dialog v-model="showNewMessageDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center">
          <div class="text-h6">New Message</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="sendMessage" class="q-gutter-md">
            <q-select
              v-model="newMessage.recipient"
              :options="recipientOptions"
              label="Recipient"
              outlined
              :rules="[val => !!val || 'Recipient is required']"
            />

            <q-input
              v-model="newMessage.subject"
              label="Subject"
              outlined
              :rules="[val => !!val || 'Subject is required']"
            />

            <q-input
              v-model="newMessage.content"
              label="Message"
              outlined
              type="textarea"
              rows="4"
              :rules="[val => !!val || 'Message is required']"
            />

            <div class="row q-gutter-sm justify-end">
              <q-btn label="Cancel" color="grey" v-close-popup />
              <q-btn label="Send Message" type="submit" color="primary" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from 'src/boot/axios'

const router = useRouter()
const $q = useQuasar()

// Drawer and navigation
const rightDrawerOpen = ref(false)
const text = ref('')

// Real-time info
const currentTime = ref('')
const weatherData = ref<{
  temperature: number
  condition: string
  location: string
} | null>(null)
const weatherLoading = ref(false)
const weatherError = ref(false)
const timeInterval = ref<ReturnType<typeof setInterval> | null>(null)

// User profile
const userProfile = ref({
  full_name: 'Dr. John Doe',
  specialization: 'Cardiology',
  role: 'Doctor'
})
const fileInput = ref<HTMLInputElement>() 
const userInitials = computed(() => {
  const names = userProfile.value.full_name.split(' ')
  return names.map(name => name[0]).join('').toUpperCase()
})
const profilePictureUrl = ref('')

// Messaging
const showNewMessageDialog = ref(false)
const newMessage = ref({
  recipient: '',
  subject: '',
  content: ''
})

const recipientOptions = [
  { label: 'Patient - Mary Johnson', value: 'patient_mary' },
  { label: 'Nurse - Sarah Wilson', value: 'nurse_sarah' },
  { label: 'Dr. Smith - Cardiology', value: 'doctor_smith' },
  { label: 'Admin - Support Team', value: 'admin_support' }
]

// Time update function
function updateTime() {
  const now = new Date()
  const hours = now.getHours()
  const minutes = now.getMinutes()
  const seconds = now.getSeconds()
  const ampm = hours >= 12 ? 'PM' : 'AM'
  const displayHours = hours % 12 || 12
  currentTime.value = `${displayHours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')} ${ampm}`
}

// Weather functions
function getWeatherIcon(condition: string): string {
  const iconMap: { [key: string]: string } = {
    'clear': 'wb_sunny',
    'clouds': 'cloud',
    'rain': 'grain',
    'snow': 'ac_unit',
    'thunderstorm': 'flash_on',
    'drizzle': 'opacity',
    'mist': 'opacity',
    'smoke': 'opacity',
    'haze': 'opacity',
    'dust': 'opacity',
    'fog': 'opacity',
    'sand': 'opacity',
    'ash': 'opacity',
    'squall': 'air',
    'tornado': 'air'
  }
  return iconMap[condition.toLowerCase()] || 'wb_sunny'
}

async function fetchWeather() {
  weatherLoading.value = true
  weatherError.value = false
  
  try {
    // Get user location
    const position = await new Promise<GeolocationPosition>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject)
    })
    
    const { latitude, longitude } = position.coords
    
    // Fetch weather data (using a mock API for now)
    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=YOUR_API_KEY&units=metric`)
    
    if (!response.ok) {
      throw new Error('Weather API not available')
    }
    
    const data = await response.json()
    weatherData.value = {
      temperature: Math.round(data.main.temp),
      condition: data.weather[0].main,
      location: data.name
    }
  } catch (error) {
    console.error('Failed to fetch weather:', error)
    weatherError.value = true
  } finally {
    weatherLoading.value = false
  }
}

// Navigation functions
function toggleRightDrawer() {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

function navigateTo(route: string) {
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
      // Already on messaging page
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

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
}

// Profile picture functions
function triggerFileUpload() {
  fileInput.value?.click()
}

async function handleProfilePictureUpload(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  try {
    const formData = new FormData()
    formData.append('profile_picture', file)
    
    await api.post('/users/profile-picture/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Update profile picture URL
    profilePictureUrl.value = URL.createObjectURL(file)
    
    $q.notify({
      type: 'positive',
      message: 'Profile picture updated successfully',
      position: 'top'
    })
  } catch (error) {
    console.error('Failed to upload profile picture:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to upload profile picture',
      position: 'top'
    })
  }
}

// Messaging functions
function sendMessage() {
  try {
    // Here you would send the message to your backend
    console.log('Sending message:', newMessage.value)
    
    // Reset form
    newMessage.value = {
      recipient: '',
      subject: '',
      content: ''
    }
    
    showNewMessageDialog.value = false
    
    $q.notify({
      type: 'positive',
      message: 'Message sent successfully',
      position: 'top'
    })
  } catch (error) {
    console.error('Failed to send message:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to send message',
      position: 'top'
    })
  }
}

// Fetch user profile
async function fetchUserProfile() {
  try {
    const response = await api.get('/users/profile/')
    userProfile.value = response.data
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
  }
}

// Lifecycle
onMounted(() => {
  updateTime()
  timeInterval.value = setInterval(updateTime, 1000)
  void fetchWeather()
  void fetchUserProfile()
})

onUnmounted(() => {
  if (timeInterval.value) {
    clearInterval(timeInterval.value)
  }
})
</script>

<style lang="scss" scoped>
.page-background {
  background: url('/background.png') no-repeat center center;
  background-size: cover;
  min-height: 100vh;
}

/* Header Styles */
.search-container {
  flex: 1;
  max-width: 400px;
  margin-right: 20px;
}

.search-input {
  width: 100%;
}

.real-time-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.time-display {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  padding: 8px 12px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.time-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.weather-display {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  padding: 8px 12px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.weather-text {
  font-size: 14px;
  font-weight: 500;
}

.weather-location {
  font-size: 12px;
  opacity: 0.8;
}

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

/* Page Header Styles */
.page-header {
  padding: 30px 20px 20px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  max-width: 1200px;
  margin: 0 auto 20px;
}

.page-header-left {
  flex: 1;
}

.page-header-right {
  display: flex;
  gap: 10px;
  align-items: center;
}

.page-title {
  color: #333;
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.page-subtitle {
  color: #666;
  font-size: 16px;
  margin: 0;
  font-weight: 400;
}

/* Messaging Container */
.messaging-container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
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
  padding: 20px 0;
}

.nav-item {
  margin: 4px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: #f0f0f0;
}

.nav-item.active {
  background: #286660;
  color: white;
}

.nav-item.active .q-icon {
  color: white;
}

.logout-section {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
}

.logout-btn {
  width: 100%;
}

/* Message Styles */
.my-emoji {
  vertical-align: middle;
  height: 2em;
  width: 2em;
}
</style>
