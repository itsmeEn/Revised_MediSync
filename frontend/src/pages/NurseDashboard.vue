<template>
  <q-page class="nurse-dashboard">
    <div class="dashboard-header">
      <div class="header-content">
        <div class="user-info">
          <q-avatar size="60px" color="secondary" text-color="white">
            {{ userInitials }}
          </q-avatar>
          <div class="user-details">
            <h5 class="text-h5 q-mb-xs">Nurse {{ user?.full_name }}</h5>
            <p class="text-subtitle2 q-mb-none">Licensed Nurse</p>
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
                  <div class="text-subtitle2">Patients Under Care</div>
                </div>
                <div class="col-auto">
                  <q-icon name="people" size="2rem" color="secondary" />
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
                  <div class="text-h6">{{ stats.tasks }}</div>
                  <div class="text-subtitle2">Pending Tasks</div>
                </div>
                <div class="col-auto">
                  <q-icon name="assignment" size="2rem" color="primary" />
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
                  <div class="text-h6">{{ stats.vitals }}</div>
                  <div class="text-subtitle2">Vitals Checked</div>
                </div>
                <div class="col-auto">
                  <q-icon name="favorite" size="2rem" color="negative" />
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
                  <div class="text-h6">{{ stats.medications }}</div>
                  <div class="text-subtitle2">Medications Given</div>
                </div>
                <div class="col-auto">
                  <q-icon name="medication" size="2rem" color="positive" />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Main Content -->
      <div class="row q-gutter-lg">
        <!-- Patient Care Tasks -->
        <div class="col-12 col-md-8">
          <q-card>
            <q-card-section>
              <div class="row items-center q-mb-md">
                <h6 class="text-h6 q-mb-none">Patient Care Tasks</h6>
                <q-space />
                <q-btn
                  color="secondary"
                  label="Add Task"
                  icon="add"
                  size="sm"
                />
              </div>
              
              <q-list>
                <q-item v-for="task in tasks" :key="task.id" class="q-mb-sm">
                  <q-item-section avatar>
                    <q-avatar :color="task.priority === 'high' ? 'negative' : task.priority === 'medium' ? 'warning' : 'positive'" text-color="white">
                      {{ task.patient.charAt(0) }}
                    </q-avatar>
                  </q-item-section>
                  
                  <q-item-section>
                    <q-item-label>{{ task.patient }}</q-item-label>
                    <q-item-label caption>{{ task.description }}</q-item-label>
                    <q-item-label caption class="text-caption">
                      <q-icon name="schedule" size="xs" />
                      {{ task.time }}
                    </q-item-label>
                  </q-item-section>
                  
                  <q-item-section side>
                    <q-chip
                      :color="task.priority === 'high' ? 'negative' : task.priority === 'medium' ? 'warning' : 'positive'"
                      text-color="white"
                      :label="task.priority"
                      size="sm"
                    />
                  </q-item-section>
                  
                  <q-item-section side>
                    <q-btn
                      color="secondary"
                      label="Complete"
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
                  color="secondary"
                  label="Check Vitals"
                  icon="favorite"
                  class="full-width"
                  size="lg"
                />
                
                <q-btn
                  color="primary"
                  label="Administer Medication"
                  icon="medication"
                  class="full-width"
                  size="lg"
                />
                
                <q-btn
                  color="accent"
                  label="Patient Records"
                  icon="folder"
                  class="full-width"
                  size="lg"
                />
                
                <q-btn
                  color="positive"
                  label="Emergency Alert"
                  icon="emergency"
                  class="full-width"
                  size="lg"
                />
              </div>
            </q-card-section>
          </q-card>

          <!-- Recent Alerts -->
          <q-card class="q-mt-md">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Recent Alerts</h6>
              
              <q-list dense>
                <q-item v-for="alert in alerts" :key="alert.id">
                  <q-item-section avatar>
                    <q-icon :name="alert.icon" :color="alert.color" />
                  </q-item-section>
                  
                  <q-item-section>
                    <q-item-label>{{ alert.message }}</q-item-label>
                    <q-item-label caption>{{ alert.time }}</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
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
}

const user = ref<User | null>(null)
const stats = ref({
  patients: 12,
  tasks: 5,
  vitals: 8,
  medications: 15
})

const tasks = ref([
  { id: 1, patient: 'John Doe', description: 'Blood pressure check', time: '09:00 AM', priority: 'high' },
  { id: 2, patient: 'Jane Smith', description: 'Medication administration', time: '10:30 AM', priority: 'medium' },
  { id: 3, patient: 'Mike Johnson', description: 'Temperature check', time: '11:00 AM', priority: 'low' },
  { id: 4, patient: 'Sarah Wilson', description: 'IV replacement', time: '02:00 PM', priority: 'high' }
])

const alerts = ref([
  { id: 1, message: 'Patient John Doe BP elevated', time: '5 min ago', icon: 'warning', color: 'warning' },
  { id: 2, message: 'Medication due for Jane Smith', time: '15 min ago', icon: 'schedule', color: 'info' },
  { id: 3, message: 'New patient admitted', time: '1 hour ago', icon: 'person_add', color: 'positive' }
])

const userInitials = computed(() => {
  if (!user.value?.full_name) return 'N'
  return user.value.full_name.split(' ').map((n: string) => n[0]).join('').toUpperCase()
})

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  }
  
  if (!user.value || user.value.role !== 'nurse') {
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
.nurse-dashboard {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.dashboard-header {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
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
