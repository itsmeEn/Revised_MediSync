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
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('patient-assessment')" class="nav-item active">
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
              Good {{ getTimeOfDay() }}, {{ userProfile.role ? userProfile.role.charAt(0).toUpperCase() + userProfile.role.slice(1) : 'Nurse' }} {{ userProfile.full_name || 'User' }}
            </h2>
            <p class="greeting-subtitle">Patient assessment and doctor assignment - {{ currentDate }}</p>
          </q-card-section>
        </q-card>
      </div>

      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <div class="header-left">
            <h4 class="page-title">Patient Assessment</h4>
          </div>
          <div class="header-right">
            <q-btn
              color="primary"
              label="Save Assessment"
              icon="save"
              @click="saveAssessment"
              :loading="saving"
            />
          </div>
        </div>
      </div>

    <div class="page-content">
      <!-- Patient Selection -->
      <q-card class="patient-selection-card">
        <q-card-section>
          <div class="row items-center q-mb-md">
            <h6 class="text-h6 q-mb-none">Select Patient</h6>
            <q-space />
            <q-btn
              color="secondary"
              label="Add New Patient"
              icon="person_add"
              size="sm"
            />
          </div>
          
          <q-select
            v-model="selectedPatient"
            :options="patientOptions"
            label="Choose Patient"
            option-label="name"
            option-value="id"
            emit-value
            map-options
            clearable
            class="patient-select"
          >
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps">
                <q-item-section avatar>
                  <q-avatar color="primary" text-color="white">
                    {{ scope.opt.name.charAt(0) }}
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ scope.opt.name }}</q-item-label>
                  <q-item-label caption>ID: {{ scope.opt.id }} | Queue: {{ scope.opt.queueNumber }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </q-card-section>
      </q-card>

      <!-- Doctor Selection Form -->
      <div v-if="selectedPatient" class="doctor-selection-form">
        <!-- Patient Info Card -->
        <q-card class="patient-info-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Patient Information</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  :model-value="selectedPatient.name"
                  label="Full Name"
                  readonly
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  :model-value="selectedPatient.queueNumber"
                  label="Queue Number"
                  readonly
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  :model-value="selectedPatient.priority"
                  label="Priority"
                  readonly
                  outlined
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Doctor Selection Card -->
        <q-card class="doctor-selection-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Select Doctor</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-select
                  v-model="selectedSpecialization"
                  :options="doctorSpecializations"
                  label="Specialization Required"
                  outlined
                  clearable
                  @update:model-value="onSpecializationChange"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-select
                  v-model="selectedDoctor"
                  :options="availableDoctors"
                  label="Available Doctors"
                  option-label="name"
                  option-value="id"
                  emit-value
                  map-options
                  outlined
                  clearable
                  :disable="!selectedSpecialization"
                >
                  <template v-slot:option="scope">
                    <q-item v-bind="scope.itemProps">
                      <q-item-section avatar>
                        <q-avatar color="primary" text-color="white">
                          {{ scope.opt.name.charAt(0) }}
                        </q-avatar>
                      </q-item-section>
                      <q-item-section>
                        <q-item-label>{{ scope.opt.name }}</q-item-label>
                        <q-item-label caption>
                          {{ scope.opt.specialization }} | 
                          Patients: {{ scope.opt.currentPatients }}/10 |
                          <span :class="scope.opt.isAvailable ? 'text-green' : 'text-red'">
                            {{ scope.opt.isAvailable ? 'Available' : 'Busy' }}
                          </span>
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </template>
                </q-select>
              </div>
            </div>
            
            <!-- Assignment Button -->
            <div class="row q-mt-md">
              <div class="col-12">
                <q-btn
                  color="primary"
                  label="Assign Patient to Doctor"
                  icon="person_add"
                  @click="assignPatientToDoctor"
                  :loading="saving"
                  :disable="!selectedPatient || !selectedDoctor"
                  class="full-width"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Assessment Form (Hidden for now) -->
      <div v-if="false" class="assessment-form">
        <!-- Patient Info Card -->
        <q-card class="patient-info-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Patient Information</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.patientName"
                  label="Full Name"
                  readonly
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model="assessment.patientAge"
                  label="Age"
                  readonly
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model="assessment.patientGender"
                  label="Gender"
                  readonly
                  outlined
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Vital Signs -->
        <q-card class="vital-signs-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Vital Signs</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.bloodPressure"
                  label="Blood Pressure (mmHg)"
                  type="text"
                  placeholder="120/80"
                  outlined
                  :rules="[val => !!val || 'Blood pressure is required']"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.heartRate"
                  label="Heart Rate (bpm)"
                  type="number"
                  outlined
                  :rules="[val => !!val || 'Heart rate is required']"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.temperature"
                  label="Temperature (°C)"
                  type="number"
                  step="0.1"
                  outlined
                  :rules="[val => !!val || 'Temperature is required']"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.respiratoryRate"
                  label="Respiratory Rate (breaths/min)"
                  type="number"
                  outlined
                  :rules="[val => !!val || 'Respiratory rate is required']"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.oxygenSaturation"
                  label="Oxygen Saturation (%)"
                  type="number"
                  outlined
                  :rules="[val => !!val || 'Oxygen saturation is required']"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.weight"
                  label="Weight (kg)"
                  type="number"
                  step="0.1"
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.height"
                  label="Height (cm)"
                  type="number"
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model="assessment.vitals.bmi"
                  label="BMI"
                  readonly
                  outlined
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Pain Assessment -->
        <q-card class="pain-assessment-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Pain Assessment</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-4">
                <q-select
                  v-model="assessment.pain.level"
                  :options="painLevels"
                  label="Pain Level (0-10)"
                  outlined
                  emit-value
                  map-options
                />
              </div>
              <div class="col-12 col-md-4">
                <q-select
                  v-model="assessment.pain.location"
                  :options="painLocations"
                  label="Pain Location"
                  outlined
                  multiple
                  use-chips
                />
              </div>
              <div class="col-12 col-md-4">
                <q-select
                  v-model="assessment.pain.type"
                  :options="painTypes"
                  label="Pain Type"
                  outlined
                  multiple
                  use-chips
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.pain.description"
                  label="Pain Description"
                  type="textarea"
                  outlined
                  rows="3"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Physical Examination -->
        <q-card class="physical-exam-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Physical Examination</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.generalAppearance"
                  label="General Appearance"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.skinCondition"
                  label="Skin Condition"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.cardiovascular"
                  label="Cardiovascular"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.respiratory"
                  label="Respiratory"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.gastrointestinal"
                  label="Gastrointestinal"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.neurological"
                  label="Neurological"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Assessment Notes -->
        <q-card class="assessment-notes-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Assessment Notes</h6>
            <div class="row q-gutter-md">
              <div class="col-12">
                <q-input
                  v-model="assessment.notes.subjective"
                  label="Subjective Assessment"
                  type="textarea"
                  outlined
                  rows="4"
                  placeholder="Patient's chief complaint and history..."
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.notes.objective"
                  label="Objective Assessment"
                  type="textarea"
                  outlined
                  rows="4"
                  placeholder="Observations and findings..."
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.notes.assessment"
                  label="Clinical Assessment"
                  type="textarea"
                  outlined
                  rows="4"
                  placeholder="Diagnosis and clinical impression..."
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.notes.plan"
                  label="Plan of Care"
                  type="textarea"
                  outlined
                  rows="4"
                  placeholder="Treatment plan and recommendations..."
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Emergency Assessment -->
        <q-card class="emergency-assessment-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Emergency Assessment</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-select
                  v-model="assessment.emergency.priority"
                  :options="priorityLevels"
                  label="Priority Level"
                  outlined
                  emit-value
                  map-options
                />
              </div>
              <div class="col-12 col-md-6">
                <q-select
                  v-model="assessment.emergency.requiresImmediate"
                  :options="[
                    { label: 'No', value: false },
                    { label: 'Yes', value: true }
                  ]"
                  label="Requires Immediate Attention"
                  outlined
                  emit-value
                  map-options
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.emergency.notes"
                  label="Emergency Notes"
                  type="textarea"
                  outlined
                  rows="3"
                  placeholder="Any urgent concerns or immediate actions needed..."
                />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- No Patient Selected Message -->
      <div v-else class="no-patient-message">
        <q-card class="text-center">
          <q-card-section>
            <q-icon name="person_search" size="4rem" color="grey-5" />
            <h6 class="text-h6 q-mt-md">Select a Patient</h6>
            <p class="text-body2 text-grey-6">
              Please select a patient from the dropdown above to begin the assessment.
            </p>
          </q-card-section>
        </q-card>
      </div>
    </div>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from 'src/boot/axios'

const router = useRouter()
const $q = useQuasar()

// Sidebar and navigation
const rightDrawerOpen = ref(false)
const text = ref('')

// Time and weather
const currentTime = ref('')
const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
})
const weatherData = ref<{
  temperature: number
  condition: string
  location: string
} | null>(null)
const weatherLoading = ref(false)
const weatherError = ref(false)
let timeInterval: NodeJS.Timeout | null = null

// Get time of day for greeting
const getTimeOfDay = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Morning'
  if (hour < 17) return 'Afternoon'
  return 'Evening'
}

// Profile picture
const fileInput = ref<HTMLInputElement | null>(null)

// User profile
const userProfile = ref<{
  id?: number
  first_name?: string
  last_name?: string
  full_name?: string
  role?: string
  verification_status?: string
  profile_picture?: string | null
  email?: string
}>({})

// Computed properties for profile picture
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

const userInitials = computed(() => {
  if (!userProfile.value.first_name || !userProfile.value.last_name) {
    return 'NU'
  }
  return `${userProfile.value.first_name.charAt(0)}${userProfile.value.last_name.charAt(0)}`.toUpperCase()
})

// Type definitions
interface Patient {
  id: number
  name: string
  queueNumber: string
  department: string
  status: string
  position: number
  enqueueTime: string
  priority: string
  priorityLevel?: string
}

interface Doctor {
  id: number
  name: string
  specialization: string
  department: string
  isAvailable: boolean
  currentPatients: number
}

// Patient selection
const selectedPatient = ref<Patient | null>(null)
const saving = ref(false)
const loading = ref(false)

// Patient options (from queue)
const patients = ref<Patient[]>([])
const patientOptions = computed(() => patients.value)

// Doctor selection
const selectedDoctor = ref<Doctor | null>(null)
const availableDoctors = ref<Doctor[]>([])
const doctorSpecializations = ref([
  'General Medicine',
  'Cardiology',
  'Neurology',
  'Pediatrics',
  'Orthopedics',
  'Dermatology',
  'Psychiatry',
  'Emergency Medicine',
  'Internal Medicine',
  'Surgery'
])
const selectedSpecialization = ref('')

// Assessment data
const assessment = ref({
  patientName: '',
  patientAge: '',
  patientGender: '',
  vitals: {
    bloodPressure: '',
    heartRate: null,
    temperature: null,
    respiratoryRate: null,
    oxygenSaturation: null,
    weight: null,
    height: null,
    bmi: ''
  },
  pain: {
    level: null,
    location: [],
    type: [],
    description: ''
  },
  physicalExam: {
    generalAppearance: '',
    skinCondition: '',
    cardiovascular: '',
    respiratory: '',
    gastrointestinal: '',
    neurological: ''
  },
  notes: {
    subjective: '',
    objective: '',
    assessment: '',
    plan: ''
  },
  emergency: {
    priority: 'normal',
    requiresImmediate: false,
    notes: ''
  }
})

// Options for dropdowns
const painLevels = [
  { label: '0 - No Pain', value: 0 },
  { label: '1-3 - Mild Pain', value: 1 },
  { label: '4-6 - Moderate Pain', value: 4 },
  { label: '7-9 - Severe Pain', value: 7 },
  { label: '10 - Worst Pain', value: 10 }
]

const painLocations = [
  'Head', 'Neck', 'Chest', 'Back', 'Abdomen', 'Arms', 'Legs', 'Joints'
]

const painTypes = [
  'Sharp', 'Dull', 'Throbbing', 'Burning', 'Cramping', 'Aching', 'Stabbing'
]

const priorityLevels = [
  { label: 'Normal', value: 'normal' },
  { label: 'Low Priority', value: 'low' },
  { label: 'Medium Priority', value: 'medium' },
  { label: 'High Priority', value: 'high' },
  { label: 'Emergency', value: 'emergency' }
]

// Watch for patient selection changes
watch(selectedPatient, (newPatient) => {
  if (newPatient) {
    // Patient is already selected, no need to find it again
    assessment.value.patientName = newPatient.name
    assessment.value.patientAge = 'N/A' // Age not available in queue data
    assessment.value.patientGender = 'N/A' // Gender not available in queue data
  } else {
    // Reset form when no patient is selected
    assessment.value = {
      patientName: '',
      patientAge: '',
      patientGender: '',
      vitals: {
        bloodPressure: '',
        heartRate: null,
        temperature: null,
        respiratoryRate: null,
        oxygenSaturation: null,
        weight: null,
        height: null,
        bmi: ''
      },
      pain: {
        level: null,
        location: [],
        type: [],
        description: ''
      },
      physicalExam: {
        generalAppearance: '',
        skinCondition: '',
        cardiovascular: '',
        respiratory: '',
        gastrointestinal: '',
        neurological: ''
      },
      notes: {
        subjective: '',
        objective: '',
        assessment: '',
        plan: ''
      },
      emergency: {
        priority: 'normal',
        requiresImmediate: false,
        notes: ''
      }
    }
  }
})

// Calculate BMI when weight or height changes
watch([() => assessment.value.vitals.weight, () => assessment.value.vitals.height], ([weight, height]) => {
  if (weight && height) {
    const heightInMeters = height / 100
    const bmi = (weight / (heightInMeters * heightInMeters)).toFixed(1)
    assessment.value.vitals.bmi = bmi
  } else {
    assessment.value.vitals.bmi = ''
  }
})

// Sidebar and navigation functions
const toggleRightDrawer = () => {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

const navigateTo = (route: string) => {
  void router.push(`/${route}`)
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
}

// Profile picture functions
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
        const axiosError = error as { response: { data: { message?: string } } }
        errorMessage = axiosError.response.data.message || errorMessage
      }
      
      $q.notify({
        type: 'negative',
        message: errorMessage,
        position: 'top',
        timeout: 3000
      })
    }
  }
}

// Time and weather functions
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
    'squall': 'cloud',
    'tornado': 'cloud'
  }
  return iconMap[condition.toLowerCase()] || 'wb_sunny'
}

const fetchWeather = async () => {
  weatherLoading.value = true
  weatherError.value = false
  
  try {
    // Mock weather data for now
    await new Promise(resolve => setTimeout(resolve, 1000))
    weatherData.value = {
      temperature: 22,
      condition: 'clear',
      location: 'Manila, PH'
    }
  } catch (error) {
    console.error('Weather fetch failed:', error)
    weatherError.value = true
  } finally {
    weatherLoading.value = false
  }
}

// Fetch user profile
const fetchUserProfile = async () => {
  try {
    const response = await api.get('/users/profile/')
    const userData = response.data.user
    
    userProfile.value = {
      first_name: userData.first_name,
      last_name: userData.last_name,
      full_name: userData.full_name,
      verification_status: userData.verification_status,
      profile_picture: userData.profile_picture || localStorage.getItem('profile_picture'),
      email: userData.email
    }
    
    // Store profile picture in localStorage if available
    if (userData.profile_picture) {
      localStorage.setItem('profile_picture', userData.profile_picture)
    }
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
  }
}

const saveAssessment = async () => {
  if (!selectedPatient.value) {
    $q.notify({
      type: 'warning',
      message: 'Please select a patient first',
      position: 'top'
    })
    return
  }

  saving.value = true

  try {
    // Validate required fields
    const requiredVitals = ['bloodPressure', 'heartRate', 'temperature', 'respiratoryRate', 'oxygenSaturation'] as const
    const missingVitals = requiredVitals.filter(vital => !assessment.value.vitals[vital])
    
    if (missingVitals.length > 0) {
      $q.notify({
        type: 'warning',
        message: `Please fill in all required vital signs: ${missingVitals.join(', ')}`,
        position: 'top'
      })
      return
    }

    // Mock API call - replace with actual API
    await new Promise(resolve => setTimeout(resolve, 2000))

    $q.notify({
      type: 'positive',
      message: 'Assessment saved successfully!',
      position: 'top'
    })

    // Reset form after successful save
    selectedPatient.value = null

  } catch (error) {
    console.error('Error saving assessment:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to save assessment. Please try again.',
      position: 'top'
    })
  } finally {
    saving.value = false
  }
}

// Load patients from queue
const loadQueuePatients = async () => {
  try {
    loading.value = true
    const response = await api.get('/operations/nurse/queue/patients/')
    
    // Transform queue data to patient format
    const normalPatients = response.data.normal_queue.map((queueItem: {
      patient_id?: number
      id: number
      patient_name: string
      queue_number: string
      department: string
      status: string
      position_in_queue: number
      enqueue_time: string
    }) => ({
      id: queueItem.patient_id || queueItem.id,
      name: queueItem.patient_name,
      queueNumber: queueItem.queue_number,
      department: queueItem.department,
      status: queueItem.status,
      position: queueItem.position_in_queue,
      enqueueTime: queueItem.enqueue_time,
      priority: 'normal'
    }))
    
    const priorityPatients = response.data.priority_queue.map((queueItem: {
      patient_id?: number
      id: number
      patient_name: string
      queue_number: string
      department: string
      priority_level: string
      priority_position: number
    }) => ({
      id: queueItem.patient_id || queueItem.id,
      name: queueItem.patient_name,
      queueNumber: queueItem.queue_number,
      department: queueItem.department,
      priorityLevel: queueItem.priority_level,
      position: queueItem.priority_position,
      priority: 'high'
    }))
    
    // Combine all patients
    patients.value = [...normalPatients, ...priorityPatients]
    
  } catch (error) {
    console.error('Failed to load queue patients:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load patient queue',
      position: 'top',
      timeout: 3000
    })
  } finally {
    loading.value = false
  }
}

// Load available doctors by specialization
const loadAvailableDoctors = async (specialization: string) => {
  try {
    const response = await api.get('/operations/available-doctors/', {
      params: { specialization }
    })
    
    availableDoctors.value = response.data.map((doctor: {
      id: number
      full_name: string
      specialization: string
      department: string
      is_available: boolean
      current_patients: number
      profile_picture?: string
    }) => ({
      id: doctor.id,
      name: doctor.full_name,
      specialization: doctor.specialization,
      department: doctor.department,
      isAvailable: doctor.is_available,
      currentPatients: doctor.current_patients || 0
    }))
    
  } catch (error) {
    console.error('Failed to load available doctors:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load available doctors',
      position: 'top',
      timeout: 3000
    })
  }
}

// Handle specialization selection
const onSpecializationChange = (specialization: string) => {
  selectedSpecialization.value = specialization
  selectedDoctor.value = null
  if (specialization) {
    void loadAvailableDoctors(specialization)
  } else {
    availableDoctors.value = []
  }
}

// Assign patient to doctor
const assignPatientToDoctor = async () => {
  if (!selectedPatient.value || !selectedDoctor.value) {
    $q.notify({
      type: 'warning',
      message: 'Please select both patient and doctor',
      position: 'top',
      timeout: 3000
    })
    return
  }
  
  try {
    saving.value = true
    
    await api.post('/operations/assign-patient/', {
      patient_id: selectedPatient.value?.id,
      doctor_id: selectedDoctor.value?.id,
      specialization: selectedSpecialization.value,
      reason: `Patient assessment - ${selectedPatient.value?.name}`,
      priority: selectedPatient.value?.priority === 'high' ? 'high' : 'medium'
    })
    
    $q.notify({
      type: 'positive',
      message: `Patient ${selectedPatient.value?.name} assigned to Dr. ${selectedDoctor.value?.name}`,
      position: 'top',
      timeout: 3000
    })
    
    // Reset selections
    selectedPatient.value = null
    selectedDoctor.value = null
    selectedSpecialization.value = ''
    availableDoctors.value = []
    
    // Reload patients to update queue
    void loadQueuePatients()
    
  } catch (error) {
    console.error('Failed to assign patient:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to assign patient to doctor',
      position: 'top',
      timeout: 3000
    })
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  // Load user profile first
  void fetchUserProfile()
  
  // Initialize real-time features
  updateTime() // Set initial time
  timeInterval = setInterval(updateTime, 1000) // Update every second
  
  // Fetch weather data
  void fetchWeather()
  
  // Load patients from queue
  void loadQueuePatients()
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
/* Page Container with Background */
.page-container-with-fixed-header {
  background: #f5f5f5;
  min-height: 100vh;
  padding-top: 64px; /* Account for fixed header */
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
  position: relative;
  overflow: hidden;
}

.greeting-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  pointer-events: none;
}

.greeting-content {
  position: relative;
  z-index: 1;
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

.page-header {
  background: linear-gradient(135deg, #286660 0%, #1e7668 100%);
  color: white;
  padding: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-btn {
  color: white;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.page-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.patient-selection-card,
.patient-info-card,
.vital-signs-card,
.pain-assessment-card,
.physical-exam-card,
.assessment-notes-card,
.emergency-assessment-card {
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.patient-select {
  max-width: 400px;
}

.assessment-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.no-patient-message {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.no-patient-message .q-card {
  max-width: 400px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .page-content {
    padding: 10px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .header-right {
    align-self: flex-end;
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

/* Sidebar Styles */
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

.user-info {
  text-align: center;
}

.user-name {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.user-role {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #666;
}

.navigation-menu {
  flex: 1;
  padding: 8px 0;
}

.nav-item {
  margin: 4px 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-item.active {
  background: #e8f5e8;
  color: #286660;
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
</style>
