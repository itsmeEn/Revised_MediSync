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

          <q-item clickable v-ripple @click="navigateTo('settings')" class="nav-item active">
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
      <div class="page-content">
      <div class="row q-gutter-lg">
        <!-- Profile Settings -->
        <div class="col-12 col-lg-8">
          <q-card class="settings-card">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Profile Information</h6>
              
              <div class="profile-section">
                <div class="profile-picture-container">
                  <q-avatar size="120px" class="profile-avatar">
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
                
                <div class="profile-form">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.firstName"
                        label="First Name"
                        outlined
                        :rules="[val => !!val || 'First name is required']"
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.lastName"
                        label="Last Name"
                        outlined
                        :rules="[val => !!val || 'Last name is required']"
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.email"
                        label="Email Address"
                        type="email"
                        outlined
                        readonly
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.phone"
                        label="Phone Number"
                        outlined
                        mask="(###) ### - ####"
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-select
                        v-model="profileForm.department"
                        :options="departmentOptions"
                        label="Department"
                        outlined
                        emit-value
                        map-options
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.licenseNumber"
                        label="Nursing License Number"
                        outlined
                      />
                    </div>
                    <div class="col-12">
                      <q-input
                        v-model="profileForm.bio"
                        label="Bio"
                        type="textarea"
                        outlined
                        rows="3"
                        placeholder="Tell us about yourself..."
                      />
                    </div>
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Security Settings -->
          <q-card class="settings-card q-mt-lg">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Security Settings</h6>
              
              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="securityForm.currentPassword"
                    label="Current Password"
                    type="password"
                    outlined
                    :rules="[val => !!val || 'Current password is required']"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="securityForm.newPassword"
                    label="New Password"
                    type="password"
                    outlined
                    :rules="[
                      val => !!val || 'New password is required',
                      val => val.length >= 8 || 'Password must be at least 8 characters'
                    ]"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="securityForm.confirmPassword"
                    label="Confirm New Password"
                    type="password"
                    outlined
                    :rules="[
                      val => !!val || 'Please confirm your password',
                      val => val === securityForm.newPassword || 'Passwords do not match'
                    ]"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-toggle
                    v-model="securityForm.twoFactorAuth"
                    label="Enable Two-Factor Authentication"
                    color="primary"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Notification Settings -->
          <q-card class="settings-card q-mt-lg">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Notification Preferences</h6>
              
              <div class="notification-settings">
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">Patient Alerts</div>
                    <div class="notification-description">Receive notifications for patient emergencies and urgent care needs</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.patientAlerts"
                    color="primary"
                  />
                </div>
                
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">Medication Reminders</div>
                    <div class="notification-description">Get reminded about medication schedules and administration</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.medicationReminders"
                    color="primary"
                  />
                </div>
                
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">Assessment Updates</div>
                    <div class="notification-description">Notifications for completed assessments and pending tasks</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.assessmentUpdates"
                    color="primary"
                  />
                </div>
                
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">Inventory Alerts</div>
                    <div class="notification-description">Low stock and expiry notifications for medications</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.inventoryAlerts"
                    color="primary"
                  />
                </div>
                
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">System Updates</div>
                    <div class="notification-description">Important system maintenance and feature updates</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.systemUpdates"
                    color="primary"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Sidebar Settings -->
        <div class="col-12 col-lg-4">
          <!-- Quick Actions -->
          <q-card class="settings-card">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Quick Actions</h6>
              
              <div class="q-gutter-md">
                <q-btn
                  color="primary"
                  label="Save Changes"
                  icon="save"
                  class="full-width"
                  @click="saveSettings"
                  :loading="saving"
                />
                
                <q-btn
                  color="secondary"
                  label="Export Data"
                  icon="download"
                  class="full-width"
                  @click="exportData"
                />
                
                <q-btn
                  color="accent"
                  label="Backup Settings"
                  icon="backup"
                  class="full-width"
                  @click="backupSettings"
                />
              </div>
            </q-card-section>
          </q-card>

          <!-- Account Status -->
          <q-card class="settings-card q-mt-lg">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Account Status</h6>
              
              <div class="status-item">
                <div class="status-label">Account Type</div>
                <div class="status-value">Nurse</div>
              </div>
              
              <div class="status-item">
                <div class="status-label">Verification Status</div>
                <div class="status-value">
                  <q-chip
                    :color="accountStatus.verified ? 'positive' : 'warning'"
                    text-color="white"
                    :label="accountStatus.verified ? 'Verified' : 'Pending'"
                    size="sm"
                  />
                </div>
              </div>
              
              <div class="status-item">
                <div class="status-label">Last Login</div>
                <div class="status-value">{{ accountStatus.lastLogin }}</div>
              </div>
              
              <div class="status-item">
                <div class="status-label">Member Since</div>
                <div class="status-value">{{ accountStatus.memberSince }}</div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Danger Zone -->
          <q-card class="settings-card q-mt-lg danger-zone">
            <q-card-section>
              <h6 class="text-h6 q-mb-md text-negative">Danger Zone</h6>
              
              <div class="q-gutter-md">
                <q-btn
                  color="negative"
                  label="Deactivate Account"
                  icon="block"
                  class="full-width"
                  outline
                  @click="showDeactivateDialog = true"
                />
                
                <q-btn
                  color="negative"
                  label="Delete Account"
                  icon="delete_forever"
                  class="full-width"
                  outline
                  @click="showDeleteDialog = true"
                />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>

    <!-- Deactivate Account Dialog -->
    <q-dialog v-model="showDeactivateDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Deactivate Account</div>
        </q-card-section>

        <q-card-section>
          <p>Are you sure you want to deactivate your account? You can reactivate it later by contacting support.</p>
          <q-input
            v-model="deactivateReason"
            label="Reason for deactivation (optional)"
            type="textarea"
            outlined
            rows="3"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" @click="showDeactivateDialog = false" />
          <q-btn
            label="Deactivate"
            color="negative"
            @click="deactivateAccount"
            :loading="deactivating"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Delete Account Dialog -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6 text-negative">Delete Account</div>
        </q-card-section>

        <q-card-section>
          <p class="text-negative">
            <strong>Warning:</strong> This action cannot be undone. All your data will be permanently deleted.
          </p>
          <q-input
            v-model="deleteConfirmation"
            label="Type 'DELETE' to confirm"
            outlined
            placeholder="DELETE"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" @click="showDeleteDialog = false" />
          <q-btn
            label="Delete Account"
            color="negative"
            @click="deleteAccount"
            :loading="deleting"
            :disable="deleteConfirmation !== 'DELETE'"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
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

// Header functionality
const rightDrawerOpen = ref(false)
const text = ref('')
const currentTime = ref('')
const weatherData = ref<{
  temperature: number
  condition: string
  location: string
} | null>(null)
const weatherLoading = ref(false)
const weatherError = ref(false)
let timeInterval: NodeJS.Timeout | null = null

// File input reference
const fileInput = ref<HTMLInputElement>()

// User profile
const userProfile = ref<{
  first_name?: string
  last_name?: string
  full_name?: string
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

// Header methods
const toggleRightDrawer = () => {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', { 
    hour12: true, 
    hour: 'numeric', 
    minute: '2-digit', 
    second: '2-digit' 
  })
}

const getWeatherIcon = (condition: string) => {
  const conditionLower = condition.toLowerCase()
  if (conditionLower.includes('sun') || conditionLower.includes('clear')) return 'wb_sunny'
  if (conditionLower.includes('cloud')) return 'cloud'
  if (conditionLower.includes('rain')) return 'grain'
  if (conditionLower.includes('storm')) return 'thunderstorm'
  return 'wb_sunny'
}

const fetchWeather = async () => {
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
    console.error('Failed to fetch weather:', error)
    weatherError.value = true
  } finally {
    weatherLoading.value = false
  }
}

// Navigation functions
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

// Dialog states
const showDeactivateDialog = ref(false)
const showDeleteDialog = ref(false)

// Loading states
const saving = ref(false)
const deactivating = ref(false)
const deleting = ref(false)

// Form data
const profileForm = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  department: '',
  licenseNumber: '',
  bio: ''
})

const securityForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
  twoFactorAuth: false
})

const notificationSettings = ref({
  patientAlerts: true,
  medicationReminders: true,
  assessmentUpdates: true,
  inventoryAlerts: true,
  systemUpdates: false
})

// Account status
const accountStatus = ref({
  verified: true,
  lastLogin: '2024-01-15 10:30 AM',
  memberSince: '2023-06-15'
})

// Dialog form data
const deactivateReason = ref('')
const deleteConfirmation = ref('')

// Options
const departmentOptions = [
  { label: 'Emergency Department', value: 'emergency' },
  { label: 'Intensive Care Unit', value: 'icu' },
  { label: 'General Ward', value: 'general' },
  { label: 'Pediatrics', value: 'pediatrics' },
  { label: 'Maternity', value: 'maternity' },
  { label: 'Surgery', value: 'surgery' },
  { label: 'Outpatient', value: 'outpatient' },
  { label: 'Other', value: 'other' }
]

// Computed properties
// Methods

const saveSettings = async () => {
  saving.value = true

  try {
    // Mock API call - replace with actual API
    await new Promise(resolve => setTimeout(resolve, 2000))

    $q.notify({
      type: 'positive',
      message: 'Settings saved successfully!',
      position: 'top'
    })

    // Reset password fields
    securityForm.value.currentPassword = ''
    securityForm.value.newPassword = ''
    securityForm.value.confirmPassword = ''

  } catch (error) {
    console.error('Error saving settings:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to save settings. Please try again.',
      position: 'top'
    })
  } finally {
    saving.value = false
  }
}

const exportData = () => {
  $q.notify({
    type: 'info',
    message: 'Data export feature coming soon!',
    position: 'top'
  })
}

const backupSettings = () => {
  $q.notify({
    type: 'info',
    message: 'Settings backup feature coming soon!',
    position: 'top'
  })
}

const deactivateAccount = async () => {
  deactivating.value = true

  try {
    // Mock API call
    await new Promise(resolve => setTimeout(resolve, 2000))

    $q.notify({
      type: 'positive',
      message: 'Account deactivated successfully',
      position: 'top'
    })

    showDeactivateDialog.value = false
    deactivateReason.value = ''

    // Redirect to login
    setTimeout(() => {
      void router.push('/login')
    }, 2000)

  } catch (error) {
    console.error('Error deactivating account:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to deactivate account. Please try again.',
      position: 'top'
    })
  } finally {
    deactivating.value = false
  }
}

const deleteAccount = async () => {
  deleting.value = true

  try {
    // Mock API call
    await new Promise(resolve => setTimeout(resolve, 2000))

    $q.notify({
      type: 'positive',
      message: 'Account deleted successfully',
      position: 'top'
    })

    showDeleteDialog.value = false
    deleteConfirmation.value = ''

    // Redirect to login
    setTimeout(() => {
      void router.push('/login')
    }, 2000)

  } catch (error) {
    console.error('Error deleting account:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to delete account. Please try again.',
      position: 'top'
    })
  } finally {
    deleting.value = false
  }
}

// Load user profile data
const loadUserProfile = async () => {
  try {
    const response = await api.get('/users/profile/')
    const userData = response.data.user
    
    profileForm.value = {
      firstName: userData.first_name || '',
      lastName: userData.last_name || '',
      email: userData.email || '',
      phone: userData.phone || '',
      department: userData.nurse_profile?.department || '',
      licenseNumber: userData.nurse_profile?.license_number || '',
      bio: userData.bio || ''
    }
    
  } catch (error) {
    console.error('Failed to load user profile:', error)
    
    // Fallback to localStorage
    const userData = localStorage.getItem('user')
    if (userData) {
      const user = JSON.parse(userData)
      profileForm.value = {
        firstName: user.first_name || '',
        lastName: user.last_name || '',
        email: user.email || '',
        phone: user.phone || '',
        department: user.nurse_profile?.department || '',
        licenseNumber: user.nurse_profile?.license_number || '',
        bio: user.bio || ''
      }
    }
  }
}

onMounted(() => {
  void loadUserProfile()
  void fetchUserProfile()
  
  // Initialize time and weather
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  void fetchWeather()
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

.search-container {
  width: 100%;
  max-width: 500px;
}

.search-input {
  background: white;
  border-radius: 8px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-btn {
  color: white;
}

.time-display {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
}

.time-text {
  font-size: 14px;
  font-weight: 500;
}

.weather-display {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
}

.weather-text {
  font-size: 14px;
  font-weight: 500;
}

.weather-location {
  font-size: 14px;
  font-weight: 500;
}

.weather-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
}

.weather-error {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
}

/* Page Container */
.page-container-with-fixed-header {
  background: url('/background.png') no-repeat center center;
  background-size: cover;
  min-height: 100vh;
  padding-top: 64px;
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

.page-content {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.nurse-settings {
  background: url('/background.png') no-repeat center center;
  background-size: cover;
  min-height: 100vh;
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

.settings-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.profile-picture-container {
  position: relative;
  display: inline-block;
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
  font-size: 36px;
  font-weight: bold;
  border-radius: 50%;
}

.upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #1e7668 !important;
}

.profile-form {
  width: 100%;
}

.notification-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.notification-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  background: #f8f9fa;
}

.notification-info {
  flex: 1;
  margin-right: 20px;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.notification-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e0e0e0;
}

.status-item:last-child {
  border-bottom: none;
}

.status-label {
  font-weight: 500;
  color: #666;
}

.status-value {
  font-weight: 600;
  color: #333;
}

.danger-zone {
  border: 2px solid #f44336;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .page-content {
    padding: 10px;
  }
  
  .profile-section {
    align-items: stretch;
  }
  
  .notification-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .notification-info {
    margin-right: 0;
  }
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
