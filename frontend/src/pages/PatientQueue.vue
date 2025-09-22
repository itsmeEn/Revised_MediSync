<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header class="dashboard-header">
      <div class="header-content">
        <q-avatar size="48px" class="profile-avatar">
          <img v-if="profileImageUrl" :src="profileImageUrl" alt="Profile" />
          <q-icon v-else name="person" size="40px" />
        </q-avatar>
        <div class="user-info">
          <div class="user-name">{{ user?.full_name || "Patient" }}</div>
          <div class="user-role">Patient Queue Management</div>
        </div>
        <q-space />
        <q-btn
          flat
          round
          dense
          icon="logout"
          @click="logout"
          class="logout-btn"
          aria-label="Logout"
        />
      </div>
    </q-header>

    <!-- Main content area -->
    <q-page-container class="page-background">
      <div class="q-pa-md">
        <!-- Queue Management Section -->
        <div class="queue-management-section">
          <div class="section-header">
            <h2 class="section-title">Queue Management</h2>
            <p class="section-subtitle">Check in and monitor your queue status</p>
          </div>

          <!-- Check-in Form -->
          <q-card class="checkin-card" v-if="!isInQueue">
            <q-card-section>
              <div class="text-h6 q-mb-md">Online Check-in</div>
              <q-form @submit="checkIn" class="q-gutter-md">
                <q-select
                  v-model="checkInForm.department"
                  :options="departmentOptions"
                  label="Department"
                  outlined
                  required
                />
                <q-input
                  v-model="checkInForm.appointmentId"
                  label="Appointment ID (Optional)"
                  outlined
                />
                <q-select
                  v-model="checkInForm.priorityLevel"
                  :options="priorityOptions"
                  label="Priority Level (Optional)"
                  outlined
                />
                <q-btn
                  type="submit"
                  color="primary"
                  size="lg"
                  class="full-width"
                  :loading="checkingIn"
                >
                  Check In
                </q-btn>
              </q-form>
            </q-card-section>
          </q-card>

          <!-- Queue Status Display -->
          <q-card class="queue-status-card" v-if="isInQueue">
            <q-card-section>
              <div class="text-h6 q-mb-md">Your Queue Status</div>
              <div v-for="queue in queueStatus" :key="queue.queue_number" class="queue-item">
                <div class="queue-info">
                  <div class="queue-number">Queue #{{ queue.queue_number }}</div>
                  <div class="queue-department">{{ queue.department }}</div>
                  <div class="queue-position">Position: {{ queue.position }}</div>
                  <div class="queue-status" :class="queue.status">
                    {{ queue.status.replace('_', ' ').toUpperCase() }}
                  </div>
                </div>
                <div class="queue-timing">
                  <div v-if="queue.estimated_wait_time" class="wait-time">
                    Est. Wait: {{ formatWaitTime(queue.estimated_wait_time) }}
                  </div>
                  <div class="enqueue-time">
                    Joined: {{ formatTime(queue.enqueue_time) }}
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Public Queue Display -->
          <q-card class="public-queue-card">
            <q-card-section>
              <div class="text-h6 q-mb-md">Current Queue Status</div>
              <q-select
                v-model="selectedDepartment"
                :options="departmentOptions"
                label="Select Department"
                outlined
                @update:model-value="loadPublicQueue"
                class="q-mb-md"
              />
              
              <div v-if="publicQueue.length > 0" class="queue-list">
                <div class="queue-header">
                  <div>Queue #</div>
                  <div>Patient</div>
                  <div>Status</div>
                  <div>Position</div>
                </div>
                <div 
                  v-for="item in publicQueue" 
                  :key="item.queue_number"
                  class="queue-row"
                  :class="{ 'current-patient': item.status === 'in_progress' }"
                >
                  <div class="queue-number">{{ item.queue_number }}</div>
                  <div class="patient-name">{{ item.patient_name }}</div>
                  <div class="status" :class="item.status">
                    {{ item.status.replace('_', ' ').toUpperCase() }}
                  </div>
                  <div class="position">{{ item.position }}</div>
                </div>
              </div>
              <div v-else class="no-queue">
                No patients currently in queue
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Notifications Section -->
        <q-card class="notifications-card" v-if="notifications.length > 0">
          <q-card-section>
            <div class="text-h6 q-mb-md">Recent Notifications</div>
            <div v-for="notification in notifications" :key="notification.id" class="notification-item">
              <div class="notification-message">{{ notification.message }}</div>
              <div class="notification-time">{{ formatTime(notification.created_at) }}</div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </q-page-container>

    <!-- Loading Overlay -->
    <q-inner-loading :showing="loading" />
  </q-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import axios from 'axios'

// Type definitions
interface User {
  id: number
  email: string
  full_name: string
  role: string
  profile_picture?: string
}

interface QueueStatus {
  queue_number: number
  department: string
  status: string
  position: number
  estimated_wait_time?: string
  enqueue_time: string
  started_at?: string
}

interface PublicQueueItem {
  queue_number: number
  patient_name: string
  status: string
  position: number
  estimated_wait_time?: string
}

interface Notification {
  id: number
  message: string
  created_at: string
}

interface ApiError {
  response?: {
    data?: {
      error?: string
    }
  }
}

// Reactive data
const router = useRouter()
const $q = useQuasar()

const user = ref<User | null>(null)
const profileImageUrl = ref('')
const loading = ref(false)
const checkingIn = ref(false)
const isInQueue = ref(false)
const queueStatus = ref<QueueStatus[]>([])
const publicQueue = ref<PublicQueueItem[]>([])
const notifications = ref<Notification[]>([])
const selectedDepartment = ref('OPD')

const checkInForm = ref({
  department: 'OPD',
  appointmentId: '',
  priorityLevel: ''
})

const departmentOptions = [
  { label: 'Out Patient Department', value: 'OPD' },
  { label: 'Billing', value: 'Billing' },
  { label: 'Pharmacy', value: 'Pharmacy' },
  { label: 'Appointment', value: 'Appointment' }
]

const priorityOptions = [
  { label: 'Normal', value: 'normal' },
  { label: 'Senior Citizen', value: 'senior' },
  { label: 'Person with Disability', value: 'pwd' }
]

let refreshInterval: NodeJS.Timeout | null = null

// Methods
const loadUserData = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      void router.push('/login')
      return
    }

    const response = await axios.get('/api/users/profile/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    user.value = response.data
    profileImageUrl.value = response.data.profile_picture || ''
  } catch (error) {
    console.error('Error loading user data:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load user data'
    })
  }
}

const checkIn = async () => {
  try {
    checkingIn.value = true
    const token = localStorage.getItem('access_token')
    
    const response = await axios.post('/api/operations/patient/check-in/', {
      department: checkInForm.value.department,
      appointment_id: checkInForm.value.appointmentId,
      priority_level: checkInForm.value.priorityLevel
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    $q.notify({
      type: 'positive',
      message: response.data.message,
      caption: `Queue #${response.data.queue_number}`
    })
    
    // Refresh queue status
    await loadQueueStatus()
    await loadPublicQueue()
    
  } catch (error: unknown) {
    console.error('Error checking in:', error)
    const errorMessage = (error as ApiError)?.response?.data?.error || 'Failed to check in'
    $q.notify({
      type: 'negative',
      message: errorMessage
    })
  } finally {
    checkingIn.value = false
  }
}

const loadQueueStatus = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get('/api/operations/patient/queue-status/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    queueStatus.value = response.data.queues || []
    isInQueue.value = queueStatus.value.length > 0
    
  } catch (error) {
    console.error('Error loading queue status:', error)
  }
}

const loadPublicQueue = async () => {
  try {
    const response = await axios.get('/api/operations/public/queue-display/', {
      params: { department: selectedDepartment.value }
    })
    
    publicQueue.value = response.data.current_queue || []
    
  } catch (error) {
    console.error('Error loading public queue:', error)
  }
}

const loadNotifications = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get('/api/operations/notifications/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    notifications.value = response.data.slice(0, 5) // Show last 5 notifications
    
  } catch (error) {
    console.error('Error loading notifications:', error)
  }
}

const formatWaitTime = (waitTime: string) => {
  if (!waitTime) return 'Calculating...'
  // Parse duration string and format nicely
  return waitTime
}

const formatTime = (timeString: string) => {
  return new Date(timeString).toLocaleTimeString()
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  void router.push('/login')
}

const startAutoRefresh = () => {
  refreshInterval = setInterval(() => {
    void loadQueueStatus()
    void loadPublicQueue()
    void loadNotifications()
  }, 10000) // Refresh every 10 seconds
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

// Lifecycle
onMounted(async () => {
  loading.value = true
  try {
    await loadUserData()
    await loadQueueStatus()
    await loadPublicQueue()
    await loadNotifications()
    startAutoRefresh()
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.dashboard-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  gap: 16px;
}

.profile-avatar {
  border: 3px solid rgba(255,255,255,0.3);
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
}

.user-role {
  font-size: 14px;
  opacity: 0.8;
}

.logout-btn {
  color: white;
}

.page-background {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.queue-management-section {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.section-subtitle {
  font-size: 16px;
  color: #7f8c8d;
}

.checkin-card, .queue-status-card, .public-queue-card, .notifications-card {
  margin-bottom: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.queue-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 12px;
}

.queue-info {
  flex: 1;
}

.queue-number {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.queue-department {
  font-size: 14px;
  color: #7f8c8d;
  margin: 4px 0;
}

.queue-position {
  font-size: 14px;
  color: #34495e;
  margin: 4px 0;
}

.queue-status {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.queue-status.waiting {
  background: #fff3cd;
  color: #856404;
}

.queue-status.in_progress {
  background: #d4edda;
  color: #155724;
}

.queue-timing {
  text-align: right;
}

.wait-time {
  font-size: 14px;
  color: #e74c3c;
  font-weight: 600;
}

.enqueue-time {
  font-size: 12px;
  color: #7f8c8d;
  margin-top: 4px;
}

.queue-list {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.queue-header {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e9ecef;
}

.queue-row {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid #e9ecef;
  transition: background-color 0.2s;
}

.queue-row:hover {
  background: #f8f9fa;
}

.queue-row.current-patient {
  background: #d4edda;
  border-left: 4px solid #28a745;
}

.queue-number {
  font-weight: 600;
  color: #2c3e50;
}

.patient-name {
  color: #34495e;
}

.status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
}

.status.waiting {
  background: #fff3cd;
  color: #856404;
}

.status.in_progress {
  background: #d4edda;
  color: #155724;
}

.position {
  text-align: center;
  font-weight: 600;
  color: #2c3e50;
}

.no-queue {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
  font-style: italic;
}

.notification-item {
  padding: 12px;
  border-left: 4px solid #3498db;
  background: #f8f9fa;
  margin-bottom: 8px;
  border-radius: 0 8px 8px 0;
}

.notification-message {
  font-size: 14px;
  color: #2c3e50;
  margin-bottom: 4px;
}

.notification-time {
  font-size: 12px;
  color: #7f8c8d;
}
</style>
