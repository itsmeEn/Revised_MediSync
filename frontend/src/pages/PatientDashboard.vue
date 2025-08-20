<template>
  <q-page class="patient-dashboard">
    <!-- Mobile Header -->
    <div class="mobile-header">
      <div class="header-content">
        <div class="user-info">
          <q-avatar size="50px" color="accent" text-color="white">
            {{ userInitials }}
          </q-avatar>
          <div class="user-details">
            <h6 class="text-h6 q-mb-xs">{{ user?.full_name }}</h6>
            <q-chip
              :color="user?.is_verified ? 'positive' : 'warning'"
              text-color="white"
              :label="user?.is_verified ? 'Verified' : 'Pending'"
              size="xs"
            />
          </div>
        </div>
        <q-btn
          color="negative"
          icon="logout"
          @click="logout"
          flat
          round
        />
      </div>
    </div>

    <!-- Mobile Content -->
    <div class="mobile-content">
      <!-- Health Summary Cards -->
      <div class="health-summary q-mb-md">
        <q-card class="summary-card">
          <q-card-section>
            <div class="row items-center">
              <div class="col">
                <div class="text-h6">{{ healthStats.bloodPressure }}</div>
                <div class="text-caption">Blood Pressure</div>
              </div>
              <div class="col-auto">
                <q-icon name="favorite" size="2rem" color="negative" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="row q-gutter-sm q-mb-md">
        <div class="col-6">
          <q-card class="mini-card">
            <q-card-section class="text-center">
              <q-icon name="thermostat" size="1.5rem" color="warning" />
              <div class="text-subtitle2 q-mt-sm">{{ healthStats.temperature }}°C</div>
              <div class="text-caption">Temperature</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-6">
          <q-card class="mini-card">
            <q-card-section class="text-center">
              <q-icon name="speed" size="1.5rem" color="primary" />
              <div class="text-subtitle2 q-mt-sm">{{ healthStats.heartRate }} bpm</div>
              <div class="text-caption">Heart Rate</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Quick Actions -->
      <q-card class="q-mb-md">
        <q-card-section>
          <h6 class="text-h6 q-mb-md">Quick Actions</h6>
          <div class="row q-gutter-sm">
            <div class="col-6">
              <q-btn
                color="primary"
                label="Book Appointment"
                icon="event"
                class="full-width"
                size="md"
              />
            </div>
            <div class="col-6">
              <q-btn
                color="secondary"
                label="View Records"
                icon="folder"
                class="full-width"
                size="md"
              />
            </div>
          </div>
          <div class="row q-gutter-sm q-mt-sm">
            <div class="col-6">
              <q-btn
                color="accent"
                label="Medications"
                icon="medication"
                class="full-width"
                size="md"
              />
            </div>
            <div class="col-6">
              <q-btn
                color="positive"
                label="Emergency"
                icon="emergency"
                class="full-width"
                size="md"
              />
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Upcoming Appointments -->
      <q-card class="q-mb-md">
        <q-card-section>
          <div class="row items-center q-mb-md">
            <h6 class="text-h6 q-mb-none">Upcoming Appointments</h6>
            <q-space />
            <q-btn
              color="primary"
              label="View All"
              size="sm"
              flat
            />
          </div>
          
          <q-list>
            <q-item v-for="appointment in appointments" :key="appointment.id" class="q-mb-sm">
              <q-item-section avatar>
                <q-avatar color="primary" text-color="white">
                  <q-icon name="medical_services" />
                </q-avatar>
              </q-item-section>
              
              <q-item-section>
                <q-item-label>{{ appointment.doctor }}</q-item-label>
                <q-item-label caption>{{ appointment.type }}</q-item-label>
                <q-item-label caption class="text-caption">
                  <q-icon name="schedule" size="xs" />
                  {{ appointment.date }} at {{ appointment.time }}
                </q-item-label>
              </q-item-section>
              
              <q-item-section side>
                <q-chip
                  :color="appointment.status === 'confirmed' ? 'positive' : 'warning'"
                  text-color="white"
                  :label="appointment.status"
                  size="sm"
                />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <!-- Recent Medical Records -->
      <q-card class="q-mb-md">
        <q-card-section>
          <div class="row items-center q-mb-md">
            <h6 class="text-h6 q-mb-none">Recent Records</h6>
            <q-space />
            <q-btn
              color="primary"
              label="View All"
              size="sm"
              flat
            />
          </div>
          
          <q-list>
            <q-item v-for="record in medicalRecords" :key="record.id" class="q-mb-sm">
              <q-item-section avatar>
                <q-avatar color="secondary" text-color="white">
                  <q-icon name="description" />
                </q-avatar>
              </q-item-section>
              
              <q-item-section>
                <q-item-label>{{ record.title }}</q-item-label>
                <q-item-label caption>{{ record.doctor }}</q-item-label>
                <q-item-label caption class="text-caption">
                  {{ record.date }}
                </q-item-label>
              </q-item-section>
              
              <q-item-section side>
                <q-btn
                  color="primary"
                  label="View"
                  size="sm"
                  flat
                />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>

      <!-- Medications -->
      <q-card class="q-mb-md">
        <q-card-section>
          <h6 class="text-h6 q-mb-md">Current Medications</h6>
          
          <q-list>
            <q-item v-for="medication in medications" :key="medication.id" class="q-mb-sm">
              <q-item-section avatar>
                <q-avatar color="positive" text-color="white">
                  <q-icon name="medication" />
                </q-avatar>
              </q-item-section>
              
              <q-item-section>
                <q-item-label>{{ medication.name }}</q-item-label>
                <q-item-label caption>{{ medication.dosage }}</q-item-label>
                <q-item-label caption class="text-caption">
                  Next dose: {{ medication.nextDose }}
                </q-item-label>
              </q-item-section>
              
              <q-item-section side>
                <q-chip
                  :color="medication.status === 'active' ? 'positive' : 'grey'"
                  text-color="white"
                  :label="medication.status"
                  size="sm"
                />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface User {
  id: number
  email: string
  full_name: string
  role: string
  is_verified: boolean
}

const user = ref<User | null>(null)
const healthStats = ref({
  bloodPressure: '120/80',
  temperature: 36.8,
  heartRate: 72
})

const appointments = ref([
  { id: 1, doctor: 'Dr. Smith', type: 'General Checkup', date: '2024-01-15', time: '10:00 AM', status: 'confirmed' },
  { id: 2, doctor: 'Dr. Johnson', type: 'Follow-up', date: '2024-01-20', time: '02:30 PM', status: 'pending' }
])

const medicalRecords = ref([
  { id: 1, title: 'Blood Test Results', doctor: 'Dr. Smith', date: '2024-01-10' },
  { id: 2, title: 'X-Ray Report', doctor: 'Dr. Johnson', date: '2024-01-08' },
  { id: 3, title: 'Prescription Update', doctor: 'Dr. Smith', date: '2024-01-05' }
])

const medications = ref([
  { id: 1, name: 'Aspirin', dosage: '100mg daily', nextDose: 'Today 8:00 PM', status: 'active' },
  { id: 2, name: 'Vitamin D', dosage: '1000 IU daily', nextDose: 'Tomorrow 9:00 AM', status: 'active' }
])

const userInitials = computed(() => {
  if (!user.value?.full_name) return 'P'
  return user.value.full_name.split(' ').map((n: string) => n[0]).join('').toUpperCase()
})

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  }
  
  if (!user.value || user.value.role !== 'patient') {
    void router.push('/login')
  }
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
}
</script>

<style scoped>
.patient-dashboard {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.mobile-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  padding: 15px;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details h6 {
  color: white;
  margin: 0;
}

.mobile-content {
  padding: 15px;
}

.health-summary {
  margin-top: 10px;
}

.summary-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.mini-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  .mobile-content {
    padding: 10px;
  }
  
  .user-details h6 {
    font-size: 1rem;
  }
}
</style>
