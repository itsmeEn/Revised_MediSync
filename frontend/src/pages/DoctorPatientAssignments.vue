<template>
  <q-layout view="lHh Lpr lFf" class="bg-grey-1">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>
          MediSync - Doctor Dashboard
        </q-toolbar-title>
        <q-btn flat round dense icon="notifications" class="q-mr-sm">
          <q-badge color="red" floating>{{ unreadNotifications }}</q-badge>
        </q-btn>
        <q-btn flat round dense icon="account_circle" @click="rightDrawerOpen = !rightDrawerOpen" />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-grey-1"
    >
      <q-list>
        <q-item-label header class="text-grey-8">
          Navigation
        </q-item-label>
        <q-item clickable v-ripple @click="navigateTo('doctor-dashboard')">
          <q-item-section avatar>
            <q-icon name="dashboard" />
          </q-item-section>
          <q-item-section>Dashboard</q-item-section>
        </q-item>
        <q-item clickable v-ripple @click="navigateTo('doctor-patient-assignments')" class="bg-primary text-white">
          <q-item-section avatar>
            <q-icon name="assignment" />
          </q-item-section>
          <q-item-section>Patient Assignments</q-item-section>
        </q-item>
        <q-item clickable v-ripple @click="navigateTo('doctor-messaging')">
          <q-item-section avatar>
            <q-icon name="message" />
          </q-item-section>
          <q-item-section>Messaging</q-item-section>
        </q-item>
        <q-item clickable v-ripple @click="navigateTo('doctor-analytics')">
          <q-item-section avatar>
            <q-icon name="analytics" />
          </q-item-section>
          <q-item-section>Analytics</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-drawer
      v-model="rightDrawerOpen"
      side="right"
      bordered
      class="bg-grey-1"
    >
      <q-list>
        <q-item-label header class="text-grey-8">
          User Profile
        </q-item-label>
        <q-item>
          <q-item-section avatar>
            <q-avatar>
              <img :src="userProfile.profile_picture || 'https://cdn.quasar.dev/img/avatar.png'" />
            </q-avatar>
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ userProfile.full_name || 'Doctor' }}</q-item-label>
            <q-item-label caption>{{ userProfile.specialization || 'General Medicine' }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-ripple @click="logout">
          <q-item-section avatar>
            <q-icon name="logout" />
          </q-item-section>
          <q-item-section>Logout</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container class="page-container-with-fixed-header">
      <!-- Greeting Section -->
      <div class="greeting-section">
        <q-card class="greeting-card">
          <q-card-section class="greeting-content">
            <h2 class="greeting-text">
              Good {{ getTimeOfDay() }}, Dr. {{ userProfile.full_name || 'User' }}
            </h2>
            <p class="greeting-subtitle">Manage your patient assignments and consultation notes - {{ currentDate }}</p>
          </q-card-section>
        </q-card>
      </div>

      <!-- Patient Assignments -->
      <div class="q-pa-md">
        <q-card class="assignments-card">
          <q-card-section>
            <div class="row items-center q-mb-md">
              <q-icon name="assignment" size="md" class="q-mr-sm text-primary" />
              <h6 class="text-h6 q-ma-none">Patient Assignments</h6>
              <q-space />
              <q-btn
                color="primary"
                icon="refresh"
                flat
                round
                @click="loadAssignments"
                :loading="loading"
              />
            </div>

            <q-separator class="q-mb-md" />

            <!-- Assignments List -->
            <div v-if="assignments.length === 0 && !loading" class="text-center q-pa-lg">
              <q-icon name="assignment_turned_in" size="64px" color="grey-5" />
              <p class="text-grey-6 q-mt-md">No patient assignments found</p>
            </div>

            <div v-else>
              <q-list separator>
                <q-item
                  v-for="assignment in assignments"
                  :key="assignment.id"
                  class="assignment-item"
                  @click="selectAssignment(assignment)"
                >
                  <q-item-section avatar>
                    <q-avatar color="primary" text-color="white">
                      {{ assignment.patient_name.charAt(0) }}
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label class="text-weight-medium">{{ assignment.patient_name }}</q-item-label>
                    <q-item-label caption>
                      Specialization: {{ assignment.specialization_required }} |
                      Priority: {{ assignment.priority }} |
                      Status: {{ assignment.status }}
                    </q-item-label>
                    <q-item-label caption>
                      Assigned: {{ formatDate(assignment.assigned_at) }}
                    </q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-chip
                      :color="getStatusColor(assignment.status)"
                      text-color="white"
                      :label="assignment.status"
                    />
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </q-card-section>
        </q-card>

        <!-- Consultation Notes Dialog -->
        <q-dialog v-model="showConsultationDialog" persistent>
          <q-card style="min-width: 800px; max-width: 1000px">
            <q-card-section class="row items-center q-pb-none">
              <div class="text-h6">Consultation Notes</div>
              <q-space />
              <q-btn icon="close" flat round dense v-close-popup />
            </q-card-section>

            <q-card-section>
              <div class="row q-gutter-md">
                <div class="col-12">
                  <q-input
                    v-model="consultationForm.chief_complaint"
                    label="Chief Complaint"
                    outlined
                    type="textarea"
                    rows="3"
                  />
                </div>
                <div class="col-12">
                  <q-input
                    v-model="consultationForm.history_of_present_illness"
                    label="History of Present Illness"
                    outlined
                    type="textarea"
                    rows="4"
                  />
                </div>
                <div class="col-12">
                  <q-input
                    v-model="consultationForm.physical_examination"
                    label="Physical Examination"
                    outlined
                    type="textarea"
                    rows="4"
                  />
                </div>
                <div class="col-12">
                  <q-input
                    v-model="consultationForm.diagnosis"
                    label="Diagnosis"
                    outlined
                    type="textarea"
                    rows="3"
                  />
                </div>
                <div class="col-12">
                  <q-input
                    v-model="consultationForm.treatment_plan"
                    label="Treatment Plan"
                    outlined
                    type="textarea"
                    rows="4"
                  />
                </div>
                <div class="col-12">
                  <q-input
                    v-model="consultationForm.medications_prescribed"
                    label="Medications Prescribed"
                    outlined
                    type="textarea"
                    rows="3"
                  />
                </div>
                <div class="col-12">
                  <q-input
                    v-model="consultationForm.follow_up_instructions"
                    label="Follow-up Instructions"
                    outlined
                    type="textarea"
                    rows="3"
                  />
                </div>
                <div class="col-12">
                  <q-input
                    v-model="consultationForm.additional_notes"
                    label="Additional Notes"
                    outlined
                    type="textarea"
                    rows="3"
                  />
                </div>
                <div class="col-6">
                  <q-select
                    v-model="consultationForm.status"
                    :options="statusOptions"
                    label="Status"
                    outlined
                  />
                </div>
              </div>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn flat label="Cancel" v-close-popup />
              <q-btn
                color="primary"
                label="Save Notes"
                @click="saveConsultationNotes"
                :loading="saving"
              />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from '../boot/axios'

// Router and Quasar
const router = useRouter()
const $q = useQuasar()

// Type definitions
interface PatientAssignment {
  id: number
  patient_name: string
  doctor_name: string
  assigned_by_name: string
  specialization_required: string
  assignment_reason: string
  status: 'pending' | 'accepted' | 'in_progress' | 'completed' | 'rejected'
  assigned_at: string
  accepted_at?: string
  completed_at?: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
}

interface ConsultationForm {
  chief_complaint: string
  history_of_present_illness: string
  physical_examination: string
  diagnosis: string
  treatment_plan: string
  medications_prescribed: string
  follow_up_instructions: string
  additional_notes: string
  status: 'draft' | 'completed' | 'reviewed'
}

// State
const leftDrawerOpen = ref(false)
const rightDrawerOpen = ref(false)
const loading = ref(false)
const saving = ref(false)
const assignments = ref<PatientAssignment[]>([])
const selectedAssignment = ref<PatientAssignment | null>(null)
const showConsultationDialog = ref(false)
const consultationForm = ref<ConsultationForm>({
  chief_complaint: '',
  history_of_present_illness: '',
  physical_examination: '',
  diagnosis: '',
  treatment_plan: '',
  medications_prescribed: '',
  follow_up_instructions: '',
  additional_notes: '',
  status: 'draft'
})

// User profile
const userProfile = ref({
  id: null,
  full_name: '',
  specialization: '',
  profile_picture: null
})

// Computed
const currentDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const unreadNotifications = computed(() => {
  return 0 // TODO: Implement notification count
})

const statusOptions = [
  { label: 'Draft', value: 'draft' },
  { label: 'Completed', value: 'completed' },
  { label: 'Reviewed', value: 'reviewed' }
]

// Methods
const getTimeOfDay = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Morning'
  if (hour < 17) return 'Afternoon'
  return 'Evening'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending': return 'orange'
    case 'accepted': return 'blue'
    case 'in_progress': return 'purple'
    case 'completed': return 'green'
    case 'rejected': return 'red'
    default: return 'grey'
  }
}

const loadAssignments = async () => {
  try {
    loading.value = true
    const response = await api.get('/operations/doctor/assignments/')
    assignments.value = response.data
  } catch (error) {
    console.error('Failed to load assignments:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load patient assignments',
      position: 'top',
      timeout: 3000
    })
  } finally {
    loading.value = false
  }
}

const selectAssignment = async (assignment: PatientAssignment) => {
  selectedAssignment.value = assignment
  showConsultationDialog.value = true
  
  // Load existing consultation notes if any
  try {
    const response = await api.get(`/operations/doctor/assignments/${assignment.id}/consultation-notes/`)
    if (response.data) {
      consultationForm.value = {
        chief_complaint: response.data.chief_complaint || '',
        history_of_present_illness: response.data.history_of_present_illness || '',
        physical_examination: response.data.physical_examination || '',
        diagnosis: response.data.diagnosis || '',
        treatment_plan: response.data.treatment_plan || '',
        medications_prescribed: response.data.medications_prescribed || '',
        follow_up_instructions: response.data.follow_up_instructions || '',
        additional_notes: response.data.additional_notes || '',
        status: response.data.status || 'draft'
      }
    }
  } catch {
    // No existing notes, start with empty form
    console.log('No existing consultation notes found')
  }
}

const saveConsultationNotes = async () => {
  if (!selectedAssignment.value) {
    $q.notify({
      type: 'negative',
      message: 'No assignment selected',
      position: 'top',
      timeout: 3000
    })
    return
  }

  try {
    saving.value = true
    await api.post(`/operations/doctor/assignments/${selectedAssignment.value.id}/consultation-notes/`, consultationForm.value)
    
    $q.notify({
      type: 'positive',
      message: 'Consultation notes saved successfully',
      position: 'top',
      timeout: 3000
    })
    
    showConsultationDialog.value = false
    await loadAssignments() // Refresh assignments
  } catch (error) {
    console.error('Failed to save consultation notes:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to save consultation notes',
      position: 'top',
      timeout: 3000
    })
  } finally {
    saving.value = false
  }
}

const navigateTo = (route: string) => {
  void router.push(`/${route}`)
}

const logout = () => {
  $q.dialog({
    title: 'Confirm Logout',
    message: 'Are you sure you want to logout?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    // TODO: Implement logout logic
    void router.push('/login')
  })
}

// Load user profile
const loadUserProfile = async () => {
  try {
    const response = await api.get('/users/profile/')
    userProfile.value = response.data
  } catch (error) {
    console.error('Failed to load user profile:', error)
  }
}

// Lifecycle
onMounted(() => {
  void loadUserProfile()
  void loadAssignments()
})
</script>

<style scoped>
.page-container-with-fixed-header {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.greeting-section {
  padding: 20px;
}

.greeting-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.greeting-content {
  text-align: center;
}

.greeting-text {
  margin: 0;
  color: #1976d2;
  font-size: 1.8rem;
  font-weight: 600;
}

.greeting-subtitle {
  margin: 8px 0 0 0;
  color: #666;
  font-size: 1rem;
}

.assignments-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.assignment-item {
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.assignment-item:hover {
  background-color: #f0f0f0;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
