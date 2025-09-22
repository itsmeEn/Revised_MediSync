<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header class="display-header">
      <div class="header-content">
        <div class="logo-section">
          <q-icon name="local_hospital" size="32px" />
          <div class="hospital-name">MediSync Hospital</div>
        </div>
        <div class="queue-info">
          <div class="current-time">{{ currentTime }}</div>
          <div class="last-updated">Last updated: {{ lastUpdated }}</div>
        </div>
      </div>
    </q-header>

    <!-- Main content area -->
    <q-page-container class="display-background">
      <div class="display-container">
        <!-- Department Selection -->
        <div class="department-selector">
          <q-btn-toggle
            v-model="selectedDepartment"
            :options="departmentOptions"
            color="primary"
            toggle-color="white"
            @update:model-value="loadQueueData"
            class="department-toggle"
          />
        </div>

        <!-- Current Queue Display -->
        <div class="queue-display-section">
          <div class="section-title">
            <h1>{{ getDepartmentName(selectedDepartment) }} Queue</h1>
            <div class="queue-stats">
              <div class="stat-item">
                <div class="stat-number">{{ totalWaiting }}</div>
                <div class="stat-label">Waiting</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ currentlyServing }}</div>
                <div class="stat-label">Currently Serving</div>
              </div>
            </div>
          </div>

          <!-- Queue List -->
          <div class="queue-container">
            <div v-if="currentQueue.length > 0" class="queue-list">
              <div class="queue-header">
                <div class="header-item">Queue #</div>
                <div class="header-item">Patient</div>
                <div class="header-item">Status</div>
                <div class="header-item">Position</div>
              </div>
              
              <div 
                v-for="patient in currentQueue" 
                :key="patient.queue_number"
                class="queue-item"
                :class="{ 
                  'current-patient': patient.status === 'in_progress',
                  'next-patient': isNextPatient(patient)
                }"
              >
                <div class="queue-number">{{ patient.queue_number }}</div>
                <div class="patient-name">{{ patient.patient_name }}</div>
                <div class="status" :class="patient.status">
                  {{ getStatusText(patient.status) }}
                </div>
                <div class="position">{{ patient.position }}</div>
              </div>
            </div>
            
            <div v-else class="no-queue">
              <q-icon name="check_circle" size="64px" color="positive" />
              <h3>No patients currently in queue</h3>
              <p>All patients have been served</p>
            </div>
          </div>
        </div>

        <!-- Estimated Wait Times -->
        <div class="wait-time-section" v-if="currentQueue.length > 0">
          <h3>Estimated Wait Times</h3>
          <div class="wait-time-grid">
            <div class="wait-time-item" v-for="patient in currentQueue.slice(0, 5)" :key="patient.queue_number">
              <div class="wait-queue-number">#{{ patient.queue_number }}</div>
              <div class="wait-time">{{ formatWaitTime(patient.estimated_wait_time || '') }}</div>
            </div>
          </div>
        </div>

        <!-- Instructions -->
        <div class="instructions-section">
          <h3>Queue Instructions</h3>
          <div class="instructions-grid">
            <div class="instruction-item">
              <q-icon name="person_add" size="24px" color="primary" />
              <div>
                <div class="instruction-title">Check In</div>
                <div class="instruction-text">Use the patient portal to check in online</div>
              </div>
            </div>
            <div class="instruction-item">
              <q-icon name="notifications" size="24px" color="primary" />
              <div>
                <div class="instruction-title">Notifications</div>
                <div class="instruction-text">You'll be notified when it's your turn</div>
              </div>
            </div>
            <div class="instruction-item">
              <q-icon name="schedule" size="24px" color="primary" />
              <div>
                <div class="instruction-title">Wait Time</div>
                <div class="instruction-text">Estimated wait times are shown above</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </q-page-container>

    <!-- Auto-refresh indicator -->
    <div class="refresh-indicator" v-if="autoRefresh">
      <q-icon name="refresh" size="16px" />
      <span>Auto-refreshing every 10 seconds</span>
    </div>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useQuasar } from 'quasar'
import axios from 'axios'

// Type definitions
interface QueueItem {
  queue_number: number
  patient_name: string
  status: string
  position: number
  estimated_wait_time?: string
}

// Reactive data
const $q = useQuasar()

const selectedDepartment = ref('OPD')
const currentQueue = ref<QueueItem[]>([])
const totalWaiting = ref(0)
const currentlyServing = ref(0)
const currentTime = ref('')
const lastUpdated = ref('')
const autoRefresh = ref(true)

const departmentOptions = [
  { label: 'OPD', value: 'OPD' },
  { label: 'Billing', value: 'Billing' },
  { label: 'Pharmacy', value: 'Pharmacy' },
  { label: 'Appointment', value: 'Appointment' }
]

let refreshInterval: NodeJS.Timeout | null = null
let timeInterval: NodeJS.Timeout | null = null

// Computed
const isNextPatient = (patient: QueueItem) => {
  return patient.status === 'waiting' && patient.position === 1
}

// Methods
const loadQueueData = async () => {
  try {
    const response = await axios.get('/api/operations/public/queue-display/', {
      params: { department: selectedDepartment.value }
    })
    
    currentQueue.value = response.data.current_queue || []
    totalWaiting.value = response.data.total_waiting || 0
    currentlyServing.value = currentQueue.value.filter(p => p.status === 'in_progress').length
    lastUpdated.value = new Date().toLocaleTimeString()
    
  } catch (error: unknown) {
    console.error('Error loading queue data:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load queue data'
    })
  }
}

const getDepartmentName = (dept: string) => {
  const names: Record<string, string> = {
    'OPD': 'Out Patient Department',
    'Billing': 'Billing Department',
    'Pharmacy': 'Pharmacy',
    'Appointment': 'Appointment Booking'
  }
  return names[dept] || dept
}

const getStatusText = (status: string) => {
  const statusTexts: Record<string, string> = {
    'waiting': 'WAITING',
    'in_progress': 'CURRENTLY SERVING',
    'completed': 'COMPLETED',
    'cancelled': 'CANCELLED'
  }
  return statusTexts[status] || status.toUpperCase()
}

const formatWaitTime = (waitTime: string) => {
  if (!waitTime) return 'Calculating...'
  
  // Parse duration string (format: "0:15:00" for 15 minutes)
  const parts = waitTime.split(':')
  if (parts.length === 3) {
    const hours = parseInt(parts[0] || '0')
    const minutes = parseInt(parts[1] || '0')
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`
    } else {
      return `${minutes}m`
    }
  }
  
  return waitTime
}

const updateCurrentTime = () => {
  currentTime.value = new Date().toLocaleTimeString()
}

const startAutoRefresh = () => {
  if (autoRefresh.value) {
    refreshInterval = setInterval(() => {
      void loadQueueData()
    }, 10000) // Refresh every 10 seconds
    timeInterval = setInterval(updateCurrentTime, 1000) // Update time every second
  }
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
  if (timeInterval) {
    clearInterval(timeInterval)
    timeInterval = null
  }
}

// Lifecycle
onMounted(async () => {
  await loadQueueData()
  updateCurrentTime()
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.display-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.hospital-name {
  font-size: 20px;
  font-weight: 600;
}

.queue-info {
  text-align: right;
}

.current-time {
  font-size: 18px;
  font-weight: 600;
}

.last-updated {
  font-size: 12px;
  opacity: 0.8;
}

.display-background {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.display-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.department-selector {
  margin-bottom: 32px;
  text-align: center;
}

.department-toggle {
  border-radius: 8px;
  overflow: hidden;
}

.queue-display-section {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  margin-bottom: 24px;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e9ecef;
}

.section-title h1 {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.queue-stats {
  display: flex;
  gap: 32px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  color: #3498db;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 4px;
}

.queue-container {
  background: #f8f9fa;
  border-radius: 12px;
  overflow: hidden;
}

.queue-list {
  background: white;
}

.queue-header {
  display: grid;
  grid-template-columns: 1fr 2fr 1.5fr 1fr;
  gap: 16px;
  padding: 20px;
  background: #2c3e50;
  color: white;
  font-weight: 600;
  font-size: 16px;
}

.queue-item {
  display: grid;
  grid-template-columns: 1fr 2fr 1.5fr 1fr;
  gap: 16px;
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  transition: all 0.3s ease;
  align-items: center;
}

.queue-item:hover {
  background: #f8f9fa;
}

.queue-item.current-patient {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border-left: 6px solid #28a745;
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.queue-item.next-patient {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  border-left: 6px solid #ffc107;
  transform: scale(1.01);
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.3);
}

.queue-number {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  text-align: center;
}

.patient-name {
  font-size: 16px;
  color: #34495e;
  font-weight: 500;
}

.status {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.status.waiting {
  background: #fff3cd;
  color: #856404;
}

.status.in_progress {
  background: #d4edda;
  color: #155724;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.position {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.no-queue {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.no-queue h3 {
  font-size: 24px;
  margin: 16px 0 8px;
  color: #2c3e50;
}

.no-queue p {
  font-size: 16px;
  margin: 0;
}

.wait-time-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  margin-bottom: 24px;
}

.wait-time-section h3 {
  font-size: 20px;
  color: #2c3e50;
  margin-bottom: 16px;
}

.wait-time-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.wait-time-item {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px solid #e9ecef;
}

.wait-queue-number {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 4px;
}

.wait-time {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.instructions-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.instructions-section h3 {
  font-size: 20px;
  color: #2c3e50;
  margin-bottom: 16px;
}

.instructions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.instruction-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.instruction-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.instruction-text {
  font-size: 14px;
  color: #7f8c8d;
}

.refresh-indicator {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 768px) {
  .display-container {
    padding: 16px;
  }
  
  .section-title {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .queue-stats {
    justify-content: center;
  }
  
  .queue-header,
  .queue-item {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  
  .queue-header .header-item:nth-child(3),
  .queue-item .status {
    display: none;
  }
}
</style>
