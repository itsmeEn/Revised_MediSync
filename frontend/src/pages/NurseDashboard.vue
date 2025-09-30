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
          
          <!-- Search Results Dropdown -->
          <div v-if="searchResults.length > 0" class="search-results">
            <q-list dense>
              <q-item v-for="result in searchResults" :key="`${result.type}-${result.data.id}`" clickable>
                <q-item-section avatar>
                  <q-icon :name="getSearchResultIcon(result.type)" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ getSearchResultTitle(result) }}</q-item-label>
                  <q-item-label caption>{{ getSearchResultSubtitle(result) }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
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
            <h6 class="user-name">{{ userProfile?.first_name }} {{ userProfile?.last_name }}</h6>
            <p class="user-role">Nurse</p>
            <q-chip 
              :color="userProfile?.verification_status === 'approved' ? 'positive' : 'negative'"
              text-color="white"
              size="sm"
              :label="userProfile?.verification_status === 'approved' ? 'Verified' : 'Not Verified'"
            />
          </div>
        </div>

        <!-- Navigation Menu -->
        <q-list class="navigation-menu">
          <q-item clickable v-ripple @click="navigateTo('nurse-dashboard')" class="nav-item active">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('nurse-messaging')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="message" />
            </q-item-section>
            <q-item-section>Messaging</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('patient-assessment')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="assignment" />
            </q-item-section>
            <q-item-section>Patient Assessment</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('nurse-medicine-inventory')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="medication" />
            </q-item-section>
            <q-item-section>Medicine Inventory</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('nurse-analytics')" class="nav-item">
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
              Good {{ getTimeOfDay() }}, Nurse {{ userProfile.full_name }}
            </h2>
            <p class="greeting-subtitle">Manage patient care and medical inventory - {{ currentDate }}</p>
          </q-card-section>
        </q-card>
      </div>
      
      <!-- Dashboard Content -->
      <div class="dashboard-content">
        <div class="dashboard-cards">
          <!-- Today's Tasks Card -->
          <q-card class="dashboard-card tasks-card" clickable @click="showTasksDialog = true">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Today's Tasks</div>
                <div class="card-number">{{ dashboardStats.todaysTasks }}</div>
                <div class="card-description">Tasks to be completed today</div>
              </div>
              <div class="card-icon task-icon">
                <q-icon name="assignment" size="2.5rem" />
              </div>
            </q-card-section>
          </q-card>

          <!-- Patients Under Care Card -->
          <q-card class="dashboard-card patients-card" clickable @click="showPatientsDialog = true">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Patients Under Care</div>
                <div class="card-number">{{ dashboardStats.patientsUnderCare }}</div>
                <div class="card-description">Total patients in queue</div>
              </div>
              <div class="card-icon patients-icon">
                <q-icon name="people" size="2.5rem" />
              </div>
            </q-card-section>
          </q-card>

          <!-- Vitals Checked Card -->
          <q-card class="dashboard-card vitals-card" clickable @click="showVitalsDialog = true">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Vitals Checked</div>
                <div class="card-number">{{ dashboardStats.vitalsChecked }}</div>
                <div class="card-description">Completed patient assessments</div>
              </div>
              <div class="card-icon vitals-icon">
                <q-icon name="favorite" size="2.5rem" />
              </div>
            </q-card-section>
          </q-card>

          <!-- Medications Administered Card -->
          <q-card class="dashboard-card medications-card" clickable @click="showMedicationsDialog = true">
            <q-card-section class="card-content">
              <div class="card-text">
                <div class="card-title">Medications Given</div>
                <div class="card-number">{{ dashboardStats.medicationsGiven }}</div>
                <div class="card-description">Total medications in inventory</div>
              </div>
              <div class="card-icon medications-icon">
                <q-icon name="medication" size="2.5rem" />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Patient Care Management System -->
      <div class="queueing-section">
        <q-card class="queueing-card">
          <q-card-section class="queueing-header">
            <h3 class="queueing-title">QUEUEING MANAGEMENT SYSTEM</h3>
            <div class="queueing-actions">
              <q-btn
                color="primary"
                label="Call Next Patient"
                icon="volume_up"
                size="md"
                @click="callNextPatient"
                class="action-btn"
              />
              <q-btn
                color="secondary"
                label="Manage Queue"
                icon="settings"
                size="md"
                @click="manageQueue"
                class="action-btn"
              />
            </div>
          </q-card-section>

          <q-card-section class="queue-panels-section">
            <!-- Patient Care Panels -->
            <div class="queue-panels-container">
              <!-- Normal Queues Panel -->
              <div class="queue-panel normal-queue-panel">
                <h4 class="queue-panel-title">Normal Queues</h4>
                <div class="queue-content">
                  <div v-if="normalQueue.length === 0" class="empty-queue">
                    <p>No patients in normal queue</p>
                  </div>
                  <div v-else class="queue-list">
                    <!-- Patient list items will go here -->
                  </div>
                </div>
              </div>

              <!-- Priority Queues Panel -->
              <div class="queue-panel priority-queue-panel">
                <h4 class="queue-panel-title">Priority Queues</h4>
                <div class="queue-content">
                  <div v-if="priorityQueue.length === 0" class="empty-queue">
                    <p>No patients in priority queue</p>
                  </div>
                  <div v-else class="queue-list">
                    <!-- Patient list items will go here -->
                  </div>
                </div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
      
      <router-view />
    </q-page-container>

    <!-- Today's Tasks Modal -->
    <q-dialog v-model="showTasksDialog">
      <q-card class="modal-card">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Today's Tasks</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-card-section>
          <div class="tasks-list">
            <q-list v-if="todaysTasks.length > 0">
              <q-item v-for="task in todaysTasks" :key="task.id">
                <q-item-section avatar>
                  <q-icon :name="task.icon" :color="task.color" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ task.title }}</q-item-label>
                  <q-item-label caption>{{ task.description }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-chip :color="task.status_color" text-color="white" :label="task.status" />
                </q-item-section>
              </q-item>
            </q-list>
            <div v-else class="empty-state">
              <q-icon name="assignment" size="3rem" color="grey-4" />
              <p class="text-grey-6">No tasks for today</p>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Patients Under Care Modal -->
    <q-dialog v-model="showPatientsDialog">
      <q-card class="modal-card">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Patients Under Care</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-card-section>
          <div class="patients-list">
            <q-list v-if="normalQueue.length > 0 || priorityQueue.length > 0">
              <q-item v-for="patient in normalQueue" :key="patient.id">
                <q-item-section avatar>
                  <q-icon name="person" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ patient.patient_name }}</q-item-label>
                  <q-item-label caption>Queue #{{ patient.queue_number }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-chip color="blue" text-color="white" label="Normal" />
                </q-item-section>
              </q-item>
              <q-item v-for="patient in priorityQueue" :key="patient.id">
                <q-item-section avatar>
                  <q-icon name="person" color="red" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ patient.patient_name }}</q-item-label>
                  <q-item-label caption>Queue #{{ patient.queue_number }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-chip color="red" text-color="white" label="Priority" />
                </q-item-section>
              </q-item>
            </q-list>
            <div v-else class="empty-state">
              <q-icon name="people" size="3rem" color="grey-4" />
              <p class="text-grey-6">No patients in queue</p>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Vitals Checked Modal -->
    <q-dialog v-model="showVitalsDialog">
      <q-card class="modal-card">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Vitals Checked</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-card-section>
          <div class="vitals-list">
            <q-list v-if="completedAssessments.length > 0">
              <q-item v-for="assessment in completedAssessments" :key="assessment.id">
                <q-item-section avatar>
                  <q-icon name="favorite" color="green" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ assessment.patient_name }}</q-item-label>
                  <q-item-label caption>{{ assessment.vitals_summary }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-chip color="green" text-color="white" label="Completed" />
                </q-item-section>
              </q-item>
            </q-list>
            <div v-else class="empty-state">
              <q-icon name="favorite" size="3rem" color="grey-4" />
              <p class="text-grey-6">No completed assessments yet</p>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Medications Modal -->
    <q-dialog v-model="showMedicationsDialog">
      <q-card class="modal-card">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Medications in Inventory</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-card-section>
          <div class="medications-list">
            <q-list v-if="medicines.length > 0">
              <q-item v-for="medicine in medicines" :key="medicine.id">
                <q-item-section avatar>
                  <q-icon name="medication" color="purple" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ medicine.medicine_name }}</q-item-label>
                  <q-item-label caption>{{ medicine.medicine_name }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-chip 
                    :color="medicine.stock_level === 'Low' ? 'red' : medicine.stock_level === 'Medium' ? 'orange' : 'green'" 
                    text-color="white" 
                    :label="`${medicine.current_stock} units`" 
                  />
                </q-item-section>
              </q-item>
            </q-list>
            <div v-else class="empty-state">
              <q-icon name="medication" size="3rem" color="grey-4" />
              <p class="text-grey-6">No medications in inventory</p>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
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

// Type definitions for search
interface DoctorData {
  id: number
  full_name: string
  specialization: string
  department?: string
  is_available?: boolean
  current_patients?: number
  profile_picture?: string
}

interface MedicineData {
  id: number
  medicine_name: string
  current_stock: number
  unit_price?: number
  minimum_stock_level?: number
  expiry_date?: string
  batch_number?: string
  usage_pattern?: string
  stock_level?: string
}

interface PatientData {
  id: number
  patient_name: string
  queue_number: string
  department?: string
  status?: string
  position_in_queue?: number
  enqueue_time?: string
  priority_level?: string
  priority_position?: number
}

interface SearchResult {
  type: 'patient' | 'doctor' | 'medicine'
  data: PatientData | DoctorData | MedicineData
}

interface TaskData {
  id: number
  title: string
  description: string
  icon: string
  color: string
  status: string
  status_color: string
}

interface AssessmentData {
  id: number
  patient_name: string
  vitals_summary: string
  status: string
}

// Search functionality
const searchResults = ref<SearchResult[]>([])
const isSearching = ref(false)

// Dialog states
const showTasksDialog = ref(false)
const showPatientsDialog = ref(false)
const showVitalsDialog = ref(false)
const showMedicationsDialog = ref(false)

// Queue data
const normalQueue = ref<PatientData[]>([])
const priorityQueue = ref<PatientData[]>([])

// Medicine data
const medicines = ref<MedicineData[]>([])

// Task and assessment data
const todaysTasks = ref<TaskData[]>([])
const completedAssessments = ref<AssessmentData[]>([])

const performSearch = async (query: string) => {
  if (!query.trim()) {
    searchResults.value = []
    return
  }
  
  try {
    isSearching.value = true
    
    // Search patients
    const patientsResponse = await api.get('/operations/nurse/queue/patients/')
    const patients = [
      ...patientsResponse.data.normal_queue,
      ...patientsResponse.data.priority_queue
    ].filter(patient => 
      patient.patient_name.toLowerCase().includes(query.toLowerCase())
    )
    
    // Search doctors
    const doctorsResponse = await api.get('/operations/available-doctors/')
    const doctors = doctorsResponse.data.filter((doctor: DoctorData) =>
      doctor.full_name.toLowerCase().includes(query.toLowerCase()) ||
      doctor.specialization.toLowerCase().includes(query.toLowerCase())
    )
    
    // Search medicines
    const medicinesResponse = await api.get('/operations/medicine-inventory/')
    const medicines = medicinesResponse.data.filter((medicine: MedicineData) =>
      medicine.medicine_name.toLowerCase().includes(query.toLowerCase())
    )
    
    searchResults.value = [
      ...patients.map((p: PatientData) => ({ type: 'patient' as const, data: p })),
      ...doctors.map((d: DoctorData) => ({ type: 'doctor' as const, data: d })),
      ...medicines.map((m: MedicineData) => ({ type: 'medicine' as const, data: m }))
    ]
    
  } catch (error) {
    console.error('Search error:', error)
    $q.notify({
      type: 'negative',
      message: 'Search failed',
      position: 'top',
      timeout: 3000
    })
  } finally {
    isSearching.value = false
  }
}

// Watch for search input changes
watch(text, (newValue: string) => {
  if (newValue && newValue.length > 2) {
    void performSearch(newValue)
  } else {
    searchResults.value = []
  }
})

// Search result helpers
const getSearchResultIcon = (type: string) => {
  switch (type) {
    case 'patient': return 'person'
    case 'doctor': return 'medical_services'
    case 'medicine': return 'medication'
    default: return 'search'
  }
}

const getSearchResultTitle = (result: SearchResult) => {
  switch (result.type) {
    case 'patient': 
      return (result.data as PatientData).patient_name || 'Unknown Patient'
    case 'doctor': 
      return (result.data as DoctorData).full_name || 'Unknown Doctor'
    case 'medicine': 
      return (result.data as MedicineData).medicine_name || 'Unknown Medicine'
    default: return 'Unknown'
  }
}

const getSearchResultSubtitle = (result: SearchResult) => {
  switch (result.type) {
    case 'patient': 
      return `Queue: ${(result.data as PatientData).queue_number || 'N/A'}`
    case 'doctor': 
      return (result.data as DoctorData).specialization || 'General'
    case 'medicine': 
      return `Stock: ${(result.data as MedicineData).current_stock || 0}`
    default: return ''
  }
}

// Dashboard variables

// Dashboard statistics
const dashboardStats = ref({
  todaysTasks: 0,
  patientsUnderCare: 0,
  vitalsChecked: 0,
  medicationsGiven: 0
})

// Queue management (removed duplicate declarations)

// Load dashboard statistics
const loadDashboardStats = async () => {
  try {
    // Load patients in queue (normal + priority)
    const patientsResponse = await api.get('/operations/nurse/queue/patients/')
    const totalPatients = patientsResponse.data.normal_queue.length + patientsResponse.data.priority_queue.length
    
    // Load medicine inventory count
    const medicinesResponse = await api.get('/operations/medicine-inventory/')
    const totalMedicines = medicinesResponse.data.length
    
    // Load completed patient assessments (vitals checked) - this would be from assignments
    // For now, we'll use a placeholder - in real implementation, this would come from completed assignments
    const vitalsChecked = 0 // TODO: Implement actual vitals count from completed assessments
    
    // Today's tasks based on actual patient data
    const todaysTasksCount = totalPatients > 0 ? (totalPatients + (patientsResponse.data.priority_queue.length > 0 ? 1 : 0)) : 0
    
    dashboardStats.value = {
      todaysTasks: todaysTasksCount,
      patientsUnderCare: totalPatients,
      vitalsChecked,
      medicationsGiven: totalMedicines
    }
    
  } catch (error) {
    console.error('Failed to load dashboard stats:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load dashboard statistics',
      position: 'top',
      timeout: 3000
    })
  }
}

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
  full_name: 'Nurse',
  department: 'General Ward',
  role: 'nurse',
  profile_picture: null,
  verification_status: 'not_submitted',
  email: ''
})

const userInitials = computed(() => {
  if (!userProfile.value.full_name) return 'N'
  return userProfile.value.full_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
})

const getTimeOfDay = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'morning'
  if (hour < 18) return 'afternoon'
  return 'evening'
}

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
      
      const response = await api.post('/users/profile/update/picture/', formData)
      
      userProfile.value.profile_picture = response.data.user.profile_picture
      
      // Store profile picture in localStorage for cross-page sync
      localStorage.setItem('profile_picture', response.data.user.profile_picture)
      
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
    case 'nurse-messaging':
      void router.push('/nurse-messaging')
      break
    case 'nurse-medicine-inventory':
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
    
    // Fallback to localStorage
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
    }
  }
}


// Load queue data
const loadQueueData = async () => {
  try {
    const response = await api.get('/operations/nurse/queue/patients/')
    normalQueue.value = response.data.normal_queue || []
    priorityQueue.value = response.data.priority_queue || []
  } catch (error) {
    console.error('Failed to load queue data:', error)
  }
}

// Load medicine data
const loadMedicineData = async () => {
  try {
    const response = await api.get('/operations/medicine-inventory/')
    medicines.value = response.data
  } catch (error) {
    console.error('Failed to load medicine data:', error)
  }
}

// Load today's tasks based on patient data
const loadTodaysTasks = async () => {
  try {
    const tasks = []
    
    // Get queue data to generate tasks
    const queueResponse = await api.get('/operations/nurse/queue/patients/')
    const totalPatients = queueResponse.data.normal_queue.length + queueResponse.data.priority_queue.length
    
    // Generate tasks based on actual patient data
    if (totalPatients > 0) {
      tasks.push({
        id: 1,
        title: 'Patient Assessment',
        description: `Assess ${totalPatients} patients in queue`,
        icon: 'assignment',
        color: 'primary',
        status: 'Pending',
        status_color: 'orange'
      })
      
      if (queueResponse.data.priority_queue.length > 0) {
        tasks.push({
          id: 2,
          title: 'Priority Patient Care',
          description: `Attend to ${queueResponse.data.priority_queue.length} priority patients`,
          icon: 'emergency',
          color: 'red',
          status: 'Urgent',
          status_color: 'red'
        })
      }
    }
    
    todaysTasks.value = tasks
  } catch (error) {
    console.error('Failed to load tasks:', error)
    todaysTasks.value = []
  }
}

// Load completed assessments
const loadCompletedAssessments = () => {
  try {
    // This would typically come from a backend endpoint for completed assessments
    // For now, we'll use empty array as assessments are completed through the patient assessment page
    completedAssessments.value = []
  } catch (error) {
    console.error('Failed to load completed assessments:', error)
    completedAssessments.value = []
  }
}

// Queue management methods
const callNextPatient = () => {
  $q.notify({
    type: 'info',
    message: 'Calling next patient...',
    position: 'top'
  })
}

const manageQueue = () => {
  $q.notify({
    type: 'info',
    message: 'Opening queue management...',
    position: 'top'
  })
}

onMounted(() => {
  // Load user profile data from API
  void fetchUserProfile()
  
  // Load dashboard statistics
  void loadDashboardStats()
  
  // Load queue and medicine data
  void loadQueueData()
  void loadMedicineData()
  
  // Load task and assessment data
  void loadTodaysTasks()
  void loadCompletedAssessments()
  
  // Initialize real-time features
  updateTime() // Set initial time
  timeInterval = setInterval(updateTime, 1000) // Update every second
  
  // Fetch weather data
  void fetchWeather()
  
  // Refresh weather every 30 minutes
  setInterval(() => void fetchWeather(), 30 * 60 * 1000)
  
  // Refresh dashboard stats every 5 minutes
  setInterval(() => void loadDashboardStats(), 5 * 60 * 1000)
  
  // Refresh user profile every 30 seconds to check for verification status updates
  setInterval(() => {
    void fetchUserProfile()
  }, 30000)
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
  background: #f5f5f5;
  min-height: 100vh;
  position: relative;
}

.search-container {
  display: flex;
  justify-content: center;
  width: 100%;
  padding: 0 20px;
  position: relative;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
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

.time-display, .weather-display, .weather-loading, .weather-error {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 14px;
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
  border: 3px solid #1e7668 !important;
  border-radius: 50% !important;
  overflow: hidden !important;
}

.profile-avatar img {
  border-radius: 50% !important;
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
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
  bottom: -5px;
  right: -5px;
  background: #1e7668 !important;
  border-radius: 50% !important;
  width: 24px !important;
  height: 24px !important;
  min-height: 24px !important;
  padding: 0 !important;
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

/* Pill-shaped elements for time, weather, and location */
.time-pill, .weather-pill, .location-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  background: white;
  color: #286660;
  font-size: 14px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.time-text, .weather-text, .location-text {
  white-space: nowrap;
}

.weather-loading, .weather-error {
  display: flex;
  align-items: center;
  gap: 6px;
  color: white;
  font-size: 14px;
  font-weight: 500;
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
  top: -5px;
  right: -5px;
  background: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
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
  background: rgba(255, 255, 255, 0.9);
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

/* Dashboard Content */
.dashboard-content {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

/* Responsive design for smaller screens */
@media (max-width: 1200px) {
  .dashboard-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .dashboard-cards {
    grid-template-columns: 1fr;
  }
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
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
}

.dashboard-card:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.35);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.card-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
}

.card-text {
  flex: 1;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

.card-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #286660;
  margin: 8px 0;
  text-align: center;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

.card-description {
  font-size: 0.9rem;
  color: #34495e;
  line-height: 1.4;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.6);
}

.card-icon {
  margin-left: 16px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  opacity: 0.8;
  transition: all 0.3s ease;
}

.dashboard-card:hover .card-icon {
  opacity: 1;
  transform: scale(1.1);
}

/* Colorful and relevant icons - matching Doctor Dashboard colors */
.task-icon {
  color: #2196f3; /* Blue for tasks/appointments */
}

.patients-icon {
  color: #4caf50; /* Green for patients */
}

.vitals-icon {
  color: #ff9800; /* Orange for completed/vitals */
}

.medications-icon {
  color: #9c27b0; /* Purple for medications/assessment */
}

/* Queueing Section */
.queueing-section {
  padding: 0 24px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.queueing-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.queueing-header {
  text-align: center;
  padding: 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.queueing-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 20px 0;
}

.queueing-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  min-width: 180px;
}

.queue-panels-section {
  padding: 24px;
}

.queue-panels-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.queue-panel {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: 20px;
  min-height: 200px;
}

.queue-panel-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
  text-align: center;
}

.queue-content {
  text-align: center;
}

.empty-queue {
  color: #666;
  font-style: italic;
  padding: 40px 20px;
}

.queue-list {
  /* Patient list styling will be added when patient data is implemented */
  padding: 0;
}

/* Modal Styles */
.modal-card {
  min-width: 500px;
  max-width: 600px;
  max-height: 80vh;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.modal-card .q-card-section {
  padding: 20px;
}

.modal-card .text-h6 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #286660;
  margin: 0;
}

.modal-card .q-list {
  max-height: 400px;
  overflow-y: auto;
}

.modal-card .q-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.modal-card .q-item:last-child {
  border-bottom: none;
}

.modal-card .q-item-section {
  padding: 0 8px;
}

.modal-card .q-item-label {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
}

.modal-card .q-item-label.caption {
  font-size: 0.875rem;
  color: #666;
  margin-top: 4px;
}

.modal-card .q-chip {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 12px;
}

/* Empty state styling */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}

.empty-state .q-icon {
  margin-bottom: 16px;
}

.empty-state p {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

/* Responsive modal */
@media (max-width: 768px) {
  .modal-card {
    min-width: 90vw;
    max-width: 95vw;
    margin: 20px;
  }
  
  .modal-card .q-card-section {
    padding: 16px;
  }
  
  .modal-card .text-h6 {
    font-size: 1.25rem;
  }
}
</style>
