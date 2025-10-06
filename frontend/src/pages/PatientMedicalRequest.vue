<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header elevated class="bg-teal-7 text-white">
      <q-toolbar>
        <q-btn flat round icon="arrow_back" @click="$router.go(-1)" />
        <q-avatar class="q-mr-sm">
          <q-icon name="favorite" color="white" />
        </q-avatar>
        <q-toolbar-title class="text-weight-medium">
          Patient Portal
          <div class="text-caption">Healthcare Dashboard</div>
        </q-toolbar-title>
        
        <q-btn flat round icon="notifications" class="q-mr-sm">
          <q-badge color="red" floating>1</q-badge>
        </q-btn>
        
        <q-btn-dropdown flat round>
          <template v-slot:label>
            <q-avatar size="32px">
              <q-icon name="person" />
            </q-avatar>
            <div class="q-ml-sm text-caption">{{ userName }}</div>
          </template>
          <q-list>
            <q-item clickable v-close-popup>
              <q-item-section avatar>
                <q-icon name="settings" />
              </q-item-section>
              <q-item-section>Settings</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section avatar>
                <q-icon name="help" />
              </q-item-section>
              <q-item-section>FAQ</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup>
              <q-item-section avatar>
                <q-icon name="logout" color="red" />
              </q-item-section>
              <q-item-section class="text-red">Logout</q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <!-- Main Content -->
    <q-page-container>
      <q-page class="bg-grey-1 q-pa-md">
        <div class="text-h5 text-grey-8 q-mb-lg">Medical Records & General Requests</div>
        
        <div class="row q-gutter-lg">
          <!-- Request Form -->
          <div class="col-12 col-md-7">
            <q-card>
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-icon name="description" size="24px" class="text-orange-6 q-mr-sm" />
                  <div class="text-h6 text-grey-8">Request Your Medical Records</div>
                </div>
                <div class="text-body2 text-grey-6 q-mb-lg">
                  Use this form to securely request your medical records. The records will be sent directly to your 
                  designated doctor or nurse for review and release.
                </div>

                <q-form @submit="submitRequest" class="q-gutter-md">
                  <!-- Type of Request -->
                  <div>
                    <div class="text-subtitle2 text-teal-7 q-mb-sm">Type of Request</div>
                    <q-select
                      v-model="requestForm.type"
                      :options="requestTypes"
                      outlined
                      placeholder="Full Medical Records (Last 5 Years)"
                      class="full-width"
                    />
                  </div>

                  <!-- Recipient -->
                  <div>
                    <div class="text-subtitle2 text-teal-7 q-mb-sm">Recipient (Doctor/Nurse)</div>
                    <q-input
                      v-model="requestForm.recipient"
                      outlined
                      placeholder="Dr. Amelia Chen"
                      class="full-width"
                    />
                  </div>

                  <!-- Additional Details -->
                  <div>
                    <div class="text-subtitle2 text-teal-7 q-mb-sm">Additional Details (Optional)</div>
                    <q-input
                      v-model="requestForm.details"
                      type="textarea"
                      outlined
                      rows="4"
                      placeholder="I need these records for my upcoming specialist consultation."
                      class="full-width"
                    />
                  </div>

                  <q-btn 
                    type="submit" 
                    color="teal-7" 
                    label="Submit Request" 
                    class="full-width q-mt-lg"
                    size="lg"
                  />
                </q-form>
              </q-card-section>
            </q-card>
          </div>

          <!-- Request History -->
          <div class="col-12 col-md-4">
            <q-card>
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-icon name="history" size="24px" class="text-grey-6 q-mr-sm" />
                  <div class="text-h6 text-grey-8">Request History</div>
                </div>

                <div class="q-gutter-sm">
                  <!-- Request Item 1 -->
                  <q-card flat bordered class="q-pa-sm">
                    <div class="text-weight-medium text-grey-8">Records Request (Full)</div>
                    <div class="row items-center q-mt-xs">
                      <q-chip 
                        color="red" 
                        text-color="white" 
                        size="sm" 
                        label="Denied - Insufficient authorization"
                      />
                    </div>
                    <div class="text-caption text-grey-6 q-mt-xs">Date: 2024-08-01</div>
                  </q-card>

                  <!-- Request Item 2 -->
                  <q-card flat bordered class="q-pa-sm">
                    <div class="text-weight-medium text-grey-8">Lab Results (Specific)</div>
                    <div class="row items-center q-mt-xs">
                      <q-chip 
                        color="green" 
                        text-color="white" 
                        size="sm" 
                        label="Completed"
                      />
                    </div>
                    <div class="text-caption text-grey-6 q-mt-xs">Date: 2024-06-16</div>
                  </q-card>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </q-page>
    </q-page-container>

    <!-- Bottom Navigation -->
    <q-footer class="bg-teal-7">
      <q-tabs 
        v-model="activeTab" 
        class="text-white"
        active-color="white"
        indicator-color="white"
        align="justify"
      >
        <q-tab name="queue" icon="queue" label="Queue" @click="navigateTo('/patient-queue')" />
        <q-tab name="appointments" icon="event" label="Appointments" @click="navigateTo('/patient-appointments')" />
        <q-tab name="home" icon="home" label="Home" @click="navigateTo('/patient-dashboard')" />
        <q-tab name="alerts" icon="notifications" label="Alerts" @click="navigateTo('/patient-notifications')" />
        <q-tab name="requests" icon="description" label="Requests" @click="navigateTo('/patient-medical-request')" />
      </q-tabs>
    </q-footer>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()
const activeTab = ref('requests')

const requestForm = ref({
  type: '',
  recipient: '',
  details: ''
})

const requestTypes = [
  'Full Medical Records (Last 5 Years)',
  'Lab Results (Specific)',
  'Imaging Reports',
  'Prescription History',
  'Vaccination Records',
  'Specialist Reports'
]

const navigateTo = (path: string) => {
  void router.push(path)
}

const submitRequest = () => {
  // Handle form submission
  console.log('Submitting request:', requestForm.value)
  // Add API call here
}

const userName = computed(() => {
  try {
    const u = JSON.parse(localStorage.getItem('user') || '{}')
    return u.full_name || u.email || 'User'
  } catch {
    return 'User'
  }
})
</script>

<style scoped>
.q-card {
  border-radius: 12px;
}
</style>