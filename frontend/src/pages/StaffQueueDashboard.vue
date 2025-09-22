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
          <div class="user-name">{{ user?.full_name || "Staff Member" }}</div>
          <div class="user-role">{{ user?.role?.toUpperCase() }} - Queue Management</div>
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
        <!-- Department Selection -->
        <q-card class="department-card">
          <q-card-section>
            <div class="text-h6 q-mb-md">Select Department</div>
            <q-select
              v-model="selectedDepartment"
              :options="departmentOptions"
              label="Department"
              outlined
              @update:model-value="loadQueueData"
              class="department-select"
            />
          </q-card-section>
        </q-card>

        <!-- Statistics Cards -->
        <div class="stats-grid" v-if="queueStats">
          <q-card class="stat-card">
            <q-card-section>
              <div class="stat-number">{{ queueStats.total_waiting }}</div>
              <div class="stat-label">Waiting</div>
            </q-card-section>
          </q-card>
          <q-card class="stat-card">
            <q-card-section>
              <div class="stat-number">{{ queueStats.total_in_progress }}</div>
              <div class="stat-label">In Progress</div>
            </q-card-section>
          </q-card>
          <q-card class="stat-card">
            <q-card-section>
              <div class="stat-number">{{ queueStats.total_completed_today }}</div>
              <div class="stat-label">Completed Today</div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Queue Management -->
        <div class="queue-management">
          <!-- Normal Queue -->
          <q-card class="queue-card">
            <q-card-section>
              <div class="card-header">
                <div class="text-h6">Normal Queue</div>
                <q-btn
                  color="primary"
                  icon="call"
                  label="Call Next Patient"
                  @click="callNextPatient"
                  :loading="callingNext"
                  :disable="!nextPatientAvailable"
                />
              </div>
              
              <div v-if="normalQueue.length > 0" class="queue-list">
                <div class="queue-header">
                  <div>Queue #</div>
                  <div>Patient Name</div>
                  <div>Status</div>
                  <div>Position</div>
                  <div>Actions</div>
                </div>
                <div 
                  v-for="patient in normalQueue" 
                  :key="patient.id"
                  class="queue-row"
                  :class="{ 'current-patient': patient.status === 'in_progress' }"
                >
                  <div class="queue-number">{{ patient.queue_number }}</div>
                  <div class="patient-name">{{ patient.patient_name }}</div>
                  <div class="status" :class="patient.status">
                    {{ patient.status.replace('_', ' ').toUpperCase() }}
                  </div>
                  <div class="position">{{ patient.position }}</div>
                  <div class="actions">
                    <q-btn
                      v-if="patient.status === 'in_progress'"
                      color="positive"
                      size="sm"
                      icon="check"
                      @click="completeService(patient.id)"
                      :loading="completingService"
                    >
                      Complete
                    </q-btn>
                    <q-btn
                      color="negative"
                      size="sm"
                      icon="remove"
                      @click="removePatient(patient.id)"
                      :loading="removingPatient"
                    >
                      Remove
                    </q-btn>
                  </div>
                </div>
              </div>
              <div v-else class="no-queue">
                No patients in normal queue
              </div>
            </q-card-section>
          </q-card>

          <!-- Priority Queue -->
          <q-card class="queue-card" v-if="priorityQueue.length > 0">
            <q-card-section>
              <div class="text-h6 q-mb-md">Priority Queue</div>
              <div class="queue-list">
                <div class="queue-header">
                  <div>Queue #</div>
                  <div>Patient Name</div>
                  <div>Priority</div>
                  <div>Position</div>
                  <div>Actions</div>
                </div>
                <div 
                  v-for="patient in priorityQueue" 
                  :key="patient.id"
                  class="queue-row priority-row"
                >
                  <div class="queue-number">{{ patient.queue_number }}</div>
                  <div class="patient-name">{{ patient.patient_name }}</div>
                  <div class="priority" :class="patient.priority_level">
                    {{ patient.priority_level.toUpperCase() }}
                  </div>
                  <div class="position">{{ patient.position }}</div>
                  <div class="actions">
                    <q-btn
                      color="primary"
                      size="sm"
                      icon="call"
                      @click="callPriorityPatient(patient.id)"
                    >
                      Call
                    </q-btn>
                    <q-btn
                      color="negative"
                      size="sm"
                      icon="remove"
                      @click="removePatient(patient.id)"
                    >
                      Remove
                    </q-btn>
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Notifications -->
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

    <!-- Remove Patient Dialog -->
    <q-dialog v-model="showRemoveDialog">
      <q-card style="min-width: 300px">
        <q-card-section>
          <div class="text-h6">Remove Patient from Queue</div>
        </q-card-section>
        <q-card-section>
          <q-input
            v-model="removeReason"
            label="Reason for removal"
            outlined
            type="textarea"
            rows="3"
          />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Cancel" @click="showRemoveDialog = false" />
          <q-btn 
            color="negative" 
            label="Remove" 
            @click="confirmRemovePatient"
            :loading="removingPatient"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
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

interface QueuePatient {
  id: number
  queue_number: number
  patient_name: string
  status: string
  position: number
  enqueue_time: string
  estimated_wait_time?: string
}

interface PriorityPatient {
  id: number
  queue_number: number
  patient_name: string
  priority_level: string
  position: number
}

interface QueueStats {
  total_waiting: number
  total_in_progress: number
  total_completed_today: number
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
const callingNext = ref(false)
const completingService = ref(false)
const removingPatient = ref(false)
const normalQueue = ref<QueuePatient[]>([])
const priorityQueue = ref<PriorityPatient[]>([])
const queueStats = ref<QueueStats | null>(null)
const notifications = ref<Notification[]>([])
const selectedDepartment = ref('OPD')
const showRemoveDialog = ref(false)
const removeReason = ref('')
const patientToRemove = ref<number | null>(null)

const departmentOptions = [
  { label: 'Out Patient Department', value: 'OPD' },
  { label: 'Billing', value: 'Billing' },
  { label: 'Pharmacy', value: 'Pharmacy' },
  { label: 'Appointment', value: 'Appointment' }
]

let refreshInterval: NodeJS.Timeout | null = null

// Computed
const nextPatientAvailable = computed(() => {
  return normalQueue.value.some(patient => patient.status === 'waiting')
})

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
    
    // Check if user is staff
    if (user.value && !['nurse', 'doctor'].includes(user.value.role)) {
      $q.notify({
        type: 'negative',
        message: 'Access denied. Only staff members can access this dashboard.'
      })
      void router.push('/')
      return
    }
    
  } catch (error) {
    console.error('Error loading user data:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load user data'
    })
  }
}

const loadQueueData = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get('/api/operations/staff/queue-dashboard/', {
      params: { department: selectedDepartment.value },
      headers: { Authorization: `Bearer ${token}` }
    })
    
    normalQueue.value = response.data.normal_queue || []
    priorityQueue.value = response.data.priority_queue || []
    queueStats.value = response.data.stats
    
  } catch (error) {
    console.error('Error loading queue data:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load queue data'
    })
  }
}

const callNextPatient = async () => {
  try {
    callingNext.value = true
    const token = localStorage.getItem('access_token')
    
    const response = await axios.post('/api/operations/staff/call-next-patient/', {
      department: selectedDepartment.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    $q.notify({
      type: 'positive',
      message: `Called ${response.data.patient_name}`,
      caption: `Queue #${response.data.queue_number}`
    })
    
    await loadQueueData()
    
  } catch (error: unknown) {
    console.error('Error calling next patient:', error)
    const errorMessage = (error as ApiError)?.response?.data?.error || 'Failed to call next patient'
    $q.notify({
      type: 'negative',
      message: errorMessage
    })
  } finally {
    callingNext.value = false
  }
}

const completeService = async (queueId: number) => {
  try {
    completingService.value = true
    const token = localStorage.getItem('access_token')
    
    const response = await axios.post('/api/operations/staff/complete-service/', {
      queue_id: queueId
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    $q.notify({
      type: 'positive',
      message: `Service completed for ${response.data.patient_name}`
    })
    
    await loadQueueData()
    
  } catch (error: unknown) {
    console.error('Error completing service:', error)
    const errorMessage = (error as ApiError)?.response?.data?.error || 'Failed to complete service'
    $q.notify({
      type: 'negative',
      message: errorMessage
    })
  } finally {
    completingService.value = false
  }
}

const removePatient = (queueId: number) => {
  patientToRemove.value = queueId
  showRemoveDialog.value = true
}

const confirmRemovePatient = async () => {
  try {
    removingPatient.value = true
    const token = localStorage.getItem('access_token')
    
    const response = await axios.post('/api/operations/staff/remove-patient/', {
      queue_id: patientToRemove.value,
      reason: removeReason.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    $q.notify({
      type: 'positive',
      message: `Patient removed: ${response.data.patient_name}`
    })
    
    showRemoveDialog.value = false
    removeReason.value = ''
    patientToRemove.value = null
    
    await loadQueueData()
    
  } catch (error: unknown) {
    console.error('Error removing patient:', error)
    const errorMessage = (error as ApiError)?.response?.data?.error || 'Failed to remove patient'
    $q.notify({
      type: 'negative',
      message: errorMessage
    })
  } finally {
    removingPatient.value = false
  }
}

const callPriorityPatient = (queueId: number) => {
  // For priority patients, we can implement special handling
  $q.notify({
    type: 'info',
    message: 'Priority patient handling - implement custom logic as needed'
  })
  console.log('Priority patient queue ID:', queueId)
}

const loadNotifications = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get('/api/operations/notifications/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    notifications.value = response.data.slice(0, 10) // Show last 10 notifications
    
  } catch (error) {
    console.error('Error loading notifications:', error)
  }
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
    void loadQueueData()
    void loadNotifications()
  }, 5000) // Refresh every 5 seconds for staff dashboard
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
    await loadQueueData()
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

.department-card, .queue-card, .notifications-card {
  margin-bottom: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.department-select {
  max-width: 300px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  text-align: center;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.queue-list {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.queue-header {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr 2fr;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e9ecef;
}

.queue-row {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr 2fr;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid #e9ecef;
  transition: background-color 0.2s;
  align-items: center;
}

.queue-row:hover {
  background: #f8f9fa;
}

.queue-row.current-patient {
  background: #d4edda;
  border-left: 4px solid #28a745;
}

.queue-row.priority-row {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
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

.priority {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
}

.priority.senior {
  background: #d1ecf1;
  color: #0c5460;
}

.priority.pwd {
  background: #f8d7da;
  color: #721c24;
}

.position {
  text-align: center;
  font-weight: 600;
  color: #2c3e50;
}

.actions {
  display: flex;
  gap: 8px;
  justify-content: center;
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
