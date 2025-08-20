<template>
  <q-page class="doctor-dashboard">
    <div class="dashboard-header">
      <div class="header-content">
        <div class="user-info">
          <q-avatar size="60px" color="primary" text-color="white">
            {{ userInitials }}
          </q-avatar>
          <div class="user-details">
            <h5 class="text-h5 q-mb-xs">Dr. {{ user?.full_name }}</h5>
            <p class="text-subtitle2 q-mb-none">{{ user?.doctor_profile?.specialization }}</p>
            <q-chip
              :color="user?.is_verified ? 'positive' : 'warning'"
              text-color="white"
              :label="user?.is_verified ? 'Verified' : 'Pending Verification'"
              size="sm"
            />
          </div>
        </div>
        <q-btn
          color="negative"
          label="Logout"
          icon="logout"
          @click="logout"
          flat
        />
      </div>
    </div>

    <div class="dashboard-content">
      <!-- Stats Cards -->
      <div class="row q-gutter-md q-mb-lg">
        <div class="col-12 col-md-3">
          <q-card class="stat-card">
            <q-card-section>
              <div class="row items-center">
                <div class="col">
                  <div class="text-h6">{{ stats.patients }}</div>
                  <div class="text-subtitle2">Total Patients</div>
                </div>
                <div class="col-auto">
                  <q-icon name="people" size="2rem" color="primary" />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        
        <div class="col-12 col-md-3">
          <q-card class="stat-card">
            <q-card-section>
              <div class="row items-center">
                <div class="col">
                  <div class="text-h6">{{ stats.appointments }}</div>
                  <div class="text-subtitle2">Today's Appointments</div>
                </div>
                <div class="col-auto">
                  <q-icon name="event" size="2rem" color="secondary" />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        
        <div class="col-12 col-md-3">
          <q-card class="stat-card">
            <q-card-section>
              <div class="row items-center">
                <div class="col">
                  <div class="text-h6">{{ stats.consultations }}</div>
                  <div class="text-subtitle2">Consultations</div>
                </div>
                <div class="col-auto">
                  <q-icon name="medical_services" size="2rem" color="accent" />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        
        <div class="col-12 col-md-3">
          <q-card class="stat-card">
            <q-card-section>
              <div class="row items-center">
                <div class="col">
                  <div class="text-h6">{{ stats.revenue }}</div>
                  <div class="text-subtitle2">Monthly Revenue</div>
                </div>
                <div class="col-auto">
                  <q-icon name="attach_money" size="2rem" color="positive" />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Main Content -->
      <div class="row q-gutter-lg">
        <!-- Patient List -->
        <div class="col-12 col-md-8">
          <q-card>
            <q-card-section>
              <div class="row items-center q-mb-md">
                <h6 class="text-h6 q-mb-none">Recent Patients</h6>
                <q-space />
                <q-btn
                  color="primary"
                  label="Add Patient"
                  icon="add"
                  size="sm"
                />
              </div>
              
              <q-list>
                <q-item v-for="patient in patients" :key="patient.id" class="q-mb-sm">
                  <q-item-section avatar>
                    <q-avatar color="primary" text-color="white">
                      {{ patient.name.charAt(0) }}
                    </q-avatar>
                  </q-item-section>
                  
                  <q-item-section>
                    <q-item-label>{{ patient.name }}</q-item-label>
                    <q-item-label caption>{{ patient.condition }}</q-item-label>
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
        </div>

        <!-- Quick Actions -->
        <div class="col-12 col-md-4">
          <q-card>
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Quick Actions</h6>
              
              <div class="q-gutter-md">
                <q-btn
                  color="primary"
                  label="Schedule Appointment"
                  icon="event"
                  class="full-width"
                  size="lg"
                />
                
                <q-btn
                  color="secondary"
                  label="Patient Records"
                  icon="folder"
                  class="full-width"
                  size="lg"
                />
                
                <q-btn
                  color="accent"
                  label="Medical Reports"
                  icon="description"
                  class="full-width"
                  size="lg"
                />
                
                <q-btn
                  color="positive"
                  label="Consultations"
                  icon="video_call"
                  class="full-width"
                  size="lg"
                />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
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
  doctor_profile?: {
    specialization: string
  }
}

const user = ref<User | null>(null)
const stats = ref({
  patients: 45,
  appointments: 8,
  consultations: 12,
  revenue: '$12,450'
})

const patients = ref([
  { id: 1, name: 'John Doe', condition: 'Hypertension' },
  { id: 2, name: 'Jane Smith', condition: 'Diabetes' },
  { id: 3, name: 'Mike Johnson', condition: 'Asthma' },
  { id: 4, name: 'Sarah Wilson', condition: 'Heart Disease' }
])

const userInitials = computed(() => {
  if (!user.value?.full_name) return 'D'
  return user.value.full_name.split(' ').map((n: string) => n[0]).join('').toUpperCase()
})

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  }
  
  if (!user.value || user.value.role !== 'doctor') {
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
.doctor-dashboard {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.dashboard-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-details h5 {
  color: white;
  margin: 0;
}

.user-details p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.stat-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-card .text-h6 {
  font-weight: bold;
  color: #333;
}

.stat-card .text-subtitle2 {
  color: #666;
}
</style>
