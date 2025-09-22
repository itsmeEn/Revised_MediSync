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
              v-model="searchText" 
              placeholder="Search Patient, symptoms and Appointments"
              class="search-input"
              bg-color="white"
            >
              <template v-slot:prepend>
                <q-icon name="search" color="grey-6" />
              </template>
              <template v-slot:append v-if="searchText">
                <q-icon name="clear" class="cursor-pointer" @click="searchText = ''" />
              </template>
            </q-input>
          </div>
        </div>
        
        <!-- Right side - Notifications, Time, Weather -->
        <div class="header-right">
          <!-- Notifications -->
          <q-btn flat round icon="notifications" class="notification-btn">
            <q-badge color="red" floating>{{ unreadCount }}</q-badge>
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
            <span class="weather-text">Loading...</span>
          </div>
          
          <!-- Weather Error -->
          <div class="weather-error" v-else-if="weatherError">
            <q-icon name="error" size="sm" />
            <span class="weather-text">Weather unavailable</span>
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Sidebar -->
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
          <q-btn dense flat round icon="menu" @click="toggleRightDrawer" class="menu-btn-right" />
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

          <q-item clickable v-ripple @click="navigateTo('patients')" class="nav-item active">
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

      </div>

      <!-- Footer with Logout Button -->
      <div class="sidebar-footer">
        <q-btn
          color="negative"
          label="LOGOUT"
          icon="logout"
          class="logout-btn"
          @click="logout"
        />
      </div>
    </q-drawer>

    <q-page-container class="page-container-with-fixed-header">
      <!-- Main Content -->
      <div class="patient-management-content">
        <!-- Header Section -->
        <div class="greeting-section">
          <q-card class="greeting-card">
            <q-card-section class="greeting-content">
              <div class="greeting-text">
                <h4 class="greeting-title">Patient Management</h4>
                <p class="greeting-subtitle">Manage your patients and their medical records</p>
              </div>
              <div class="greeting-icon">
                <q-icon name="people" size="3rem" />
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Patient Management Cards -->
        <div class="management-cards-grid">
          <!-- Patient List Card -->
          <q-card class="glassmorphism-card patient-list-card">
            <q-card-section class="card-header">
              <h5 class="card-title">Patient List</h5>
              <q-btn
                color="primary"
                icon="refresh"
                size="sm"
                @click="loadPatients"
                :loading="loading"
              />
            </q-card-section>
            
            <q-card-section class="card-content">
              <div v-if="loading" class="loading-section">
                <q-spinner color="primary" size="2em" />
                <p class="loading-text">Loading patients...</p>
              </div>
              
              <div v-else-if="patients.length === 0" class="empty-section">
                <q-icon name="people" size="48px" color="grey-5" />
                <p class="empty-text">No patients found</p>
              </div>
              
              <div v-else class="patients-list">
                <div
                  v-for="patient in filteredPatients"
                  :key="patient.id"
                  class="patient-card"
                  @click="selectPatient(patient)"
                >
                  <div class="patient-avatar">
                    <q-avatar size="50px">
                      <img
                        v-if="patient.profile_picture"
                        :src="patient.profile_picture.startsWith('http') ? patient.profile_picture : `http://localhost:8000${patient.profile_picture}`"
                        :alt="patient.full_name"
                      />
                      <q-icon
                        v-else
                        name="person"
                        size="25px"
                        color="white"
                      />
                    </q-avatar>
                  </div>
                  
                  <div class="patient-info">
                    <h6 class="patient-name">{{ patient.full_name }}</h6>
                    <p class="patient-details">
                      Age: {{ patient.age || 'N/A' }} | 
                      {{ patient.gender || 'N/A' }} | 
                      {{ patient.blood_type || 'N/A' }}
                    </p>
                    <p class="patient-condition">{{ patient.medical_condition || 'No condition specified' }}</p>
                    <div class="patient-status">
                      <q-chip
                        :color="patient.is_dummy ? 'orange' : 'primary'"
                        text-color="white"
                        size="sm"
                      >
                        {{ patient.is_dummy ? 'Dummy Data' : 'Real Patient' }}
                      </q-chip>
                    </div>
                  </div>
                  
                  <div class="patient-actions">
                    <q-btn
                      flat
                      round
                      icon="visibility"
                      color="primary"
                      size="sm"
                      @click.stop="viewPatientDetails(patient)"
                    />
                    <q-btn
                      flat
                      round
                      icon="edit"
                      color="secondary"
                      size="sm"
                      @click.stop="editPatient(patient)"
                    />
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Patient Statistics Card -->
          <q-card class="glassmorphism-card statistics-card">
            <q-card-section class="card-header">
              <h5 class="card-title">Patient Statistics</h5>
            </q-card-section>
            
            <q-card-section class="card-content">
              <div class="stats-grid">
                <div class="stat-item">
                  <div class="stat-number">{{ patients.length }}</div>
                  <div class="stat-label">Total Patients</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ realPatientsCount }}</div>
                  <div class="stat-label">Real Patients</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ dummyPatientsCount }}</div>
                  <div class="stat-label">Dummy Data</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ activePatientsCount }}</div>
                  <div class="stat-label">Active</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'

// Types
interface Patient {
  id: number
  user_id: number
  full_name: string
  email: string
  age: number | null
  gender: string
  blood_type: string
  medical_condition: string
  hospital: string
  insurance_provider: string
  billing_amount: number | null
  room_number: string
  admission_type: string
  date_of_admission: string
  discharge_date: string
  medication: string
  test_results: string
  is_dummy: boolean
  assigned_doctor: string | null
  profile_picture?: string | null
}

// Reactive data
const $q = useQuasar()
const router = useRouter()
const rightDrawerOpen = ref(false)
const loading = ref(false)
const searchText = ref('')
const currentTime = ref('')
const patients = ref<Patient[]>([])
const selectedPatient = ref<Patient | null>(null)

// User profile data
const userProfile = ref<{
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

// Weather data
const weatherData = ref<{
  temperature: number
  condition: string
  location: string
} | null>(null)
const weatherLoading = ref(false)
const weatherError = ref(false)

// Profile picture handling
const userInitials = computed(() => {
  const name = userProfile.value.full_name || 'User'
  return name.split(' ').map(n => n.charAt(0)).join('').toUpperCase()
})

const triggerFileUpload = () => {
  const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
  if (fileInput) {
    fileInput.click()
  }
}

const handleProfilePictureUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    // Handle file upload logic here
    console.log('File selected:', file.name)
  }
}

// Computed properties
const unreadCount = computed(() => 0) // Placeholder for unread count

const profilePictureUrl = computed(() => {
  if (!userProfile.value.profile_picture) {
    return null
  }
  
  if (userProfile.value.profile_picture.startsWith('http')) {
    return userProfile.value.profile_picture
  }
  
  return `http://localhost:8000${userProfile.value.profile_picture}`
})

const filteredPatients = computed(() => {
  if (!searchText.value) return patients.value
  
  const search = searchText.value.toLowerCase()
  return patients.value.filter(patient => 
    patient.full_name.toLowerCase().includes(search) ||
    patient.medical_condition.toLowerCase().includes(search) ||
    patient.hospital.toLowerCase().includes(search)
  )
})

const realPatientsCount = computed(() => 
  patients.value.filter(p => !p.is_dummy).length
)

const dummyPatientsCount = computed(() => 
  patients.value.filter(p => p.is_dummy).length
)

const activePatientsCount = computed(() => 
  patients.value.filter(p => p.discharge_date === null || p.discharge_date === '').length
)

// Methods
const toggleRightDrawer = () => {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

const updateTime = () => {
  currentTime.value = new Date().toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const getWeatherIcon = (condition: string): string => {
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

const fetchWeatherData = async (): Promise<void> => {
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

const loadPatients = async () => {
  loading.value = true
  try {
    const response = await api.get('/users/doctor/patients/')
    if (response.data.success) {
      patients.value = response.data.patients
      console.log('Patients loaded:', patients.value.length)
    }
  } catch (error) {
    console.error('Failed to load patients:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load patients',
      position: 'top'
    })
  } finally {
    loading.value = false
  }
}

const selectPatient = (patient: Patient) => {
  selectedPatient.value = patient
  console.log('Selected patient:', patient)
}

const viewPatientDetails = (patient: Patient) => {
  $q.notify({
    type: 'info',
    message: `Viewing details for ${patient.full_name}`,
    position: 'top'
  })
}

const editPatient = (patient: Patient) => {
  $q.notify({
    type: 'info',
    message: `Editing ${patient.full_name}`,
    position: 'top'
  })
}

const fetchUserProfile = async () => {
  try {
    const response = await api.get('/users/profile/')
    const userData = response.data.user
    
    userProfile.value = {
      full_name: userData.full_name,
      specialization: userData.doctor_profile?.specialization,
      role: userData.role,
      profile_picture: userData.profile_picture || null,
      verification_status: userData.verification_status
    }
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
  }
}

const navigateTo = (route: string) => {
  rightDrawerOpen.value = false
  
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
      // Already on patient management
      break
    case 'analytics':
      void router.push('/doctor-predictive-analytics')
      break
    case 'settings':
      void router.push('/doctor-settings')
      break
  }
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
}

// Lifecycle
onMounted(() => {
  console.log('🚀 DoctorPatientManagement component mounted')
  void fetchUserProfile()
  updateTime()
  setInterval(updateTime, 1000)
  void loadPatients()
  void fetchWeatherData()
})
</script>

<style scoped>
/* Import the same styles as DoctorDashboard */
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
}

.time-text, .weather-text, .weather-location {
  font-size: 14px;
  font-weight: 500;
}

/* Drawer Styles */
.drawer-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.user-profile-section {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  margin-bottom: 20px;
  position: relative;
}

.user-avatar-container {
  position: relative;
}

.user-avatar {
  border: 3px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
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

/* Sidebar Content */
.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #f8f9fa;
  position: relative;
  padding-bottom: 80px; /* Space for footer */
}

/* Logo Section */
.logo-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
}

.logo-container {
  display: flex;
  align-items: center;
  flex: 1;
}

.logo-avatar {
  margin-right: 12px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #286660;
}

.menu-btn-right {
  color: #666;
  margin-left: auto;
}

/* Centered User Profile Section */
.sidebar-user-profile-centered {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  text-align: center;
  background: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
}

.sidebar-user-profile-centered .profile-picture-container {
  position: relative;
  margin-bottom: 20px;
}

.sidebar-user-profile-centered .user-info {
  text-align: center;
}

.sidebar-user-profile-centered .user-name {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.sidebar-user-profile-centered .user-role {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0 0 12px 0;
}

/* Footer with Logout Button */
.sidebar-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: #f8f9fa;
  border-top: 1px solid #e0e0e0;
}

.logout-btn {
  width: 100%;
  border-radius: 8px;
  font-weight: 600;
  text-transform: uppercase;
}

/* Page Container */
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
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  z-index: 0;
}

.patient-management-content {
  position: relative;
  z-index: 1;
  padding: 20px;
}

/* Greeting Section */
.greeting-section {
  margin-bottom: 30px;
}

.greeting-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.greeting-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30px;
}

.greeting-text {
  flex: 1;
}

.greeting-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 10px 0;
  background: linear-gradient(135deg, #286660, #4a7c59);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.greeting-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
  font-weight: 500;
}

.greeting-icon {
  color: #286660;
  opacity: 0.8;
}

/* Management Cards */
.management-cards-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.glassmorphism-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 20px 0 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.card-content {
  padding: 20px;
}

/* Patient List */
.patients-list {
  max-height: 500px;
  overflow-y: auto;
}

.patient-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.patient-card:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.patient-avatar {
  flex-shrink: 0;
}

.patient-info {
  flex: 1;
  min-width: 0;
}

.patient-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 5px 0;
}

.patient-details {
  font-size: 12px;
  color: #666;
  margin: 0 0 5px 0;
}

.patient-condition {
  font-size: 13px;
  color: #555;
  margin: 0 0 8px 0;
  font-style: italic;
}

.patient-status {
  margin-top: 5px;
}

.patient-actions {
  display: flex;
  gap: 5px;
  flex-shrink: 0;
}

/* Statistics */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #286660;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

/* Loading and Empty States */
.loading-section, .empty-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #666;
}

.loading-text, .empty-text {
  margin-top: 15px;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .management-cards-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .greeting-content {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .greeting-title {
    font-size: 2rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .patient-card {
    flex-direction: column;
    text-align: center;
  }
  
  .patient-actions {
    justify-content: center;
  }
}
</style>
