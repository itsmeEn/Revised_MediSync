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
        <div class="row items-center q-mb-lg">
          <q-btn flat round icon="arrow_back" @click="$router.go(-1)" class="q-mr-sm" />
          <div class="text-h5 text-grey-8">Schedule Appointment</div>
        </div>
        
        <div class="row justify-center">
          <div class="col-12 col-md-8 col-lg-6">
            <q-card class="appointment-card">
              <q-card-section class="q-pa-lg">
                <q-form @submit="scheduleAppointment" class="q-gutter-lg">
                  <!-- Appointment Type -->
                  <div>
                    <div class="text-subtitle1 text-teal-7 q-mb-sm">Appointment Type</div>
                    <q-select
                      v-model="appointmentForm.type"
                      :options="appointmentTypes"
                      outlined
                      placeholder="Select Appointment Type"
                      class="full-width"
                      :rules="[ (val: string | null) => !!val || 'Please select appointment type']"
                    />
                  </div>

                  <!-- Department -->
                  <div>
                    <div class="text-subtitle1 text-teal-7 q-mb-sm">Department</div>
                    <q-select
                      v-model="appointmentForm.department"
                      :options="departments"
                      outlined
                      placeholder="Select Department"
                      class="full-width"
                      :rules="[ (val: string | null) => !!val || 'Please select department']"
                    />
                  </div>

                  <!-- Date -->
                  <div>
                    <div class="text-subtitle1 text-teal-7 q-mb-sm">Date</div>
                    <q-input
                      v-model="appointmentForm.date"
                      outlined
                      placeholder="mm/dd/yyyy"
                      class="full-width"
                      :rules="[ (val: string | null) => !!val || 'Please select date']"
                    >
                      <template v-slot:append>
                        <q-icon name="event" class="cursor-pointer">
                          <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                            <q-date v-model="appointmentForm.date" mask="MM/DD/YYYY">
                              <div class="row items-center justify-end">
                                <q-btn v-close-popup label="Close" color="primary" flat />
                              </div>
                            </q-date>
                          </q-popup-proxy>
                        </q-icon>
                      </template>
                    </q-input>
                  </div>

                  <!-- Appointment Time -->
                  <div>
                    <div class="text-subtitle1 text-teal-7 q-mb-sm">Appointment Time</div>
                    <q-select
                      v-model="appointmentForm.time"
                      :options="timeSlots"
                      outlined
                      placeholder="Select Time"
                      class="full-width"
                      :rules="[ (val: string | null) => !!val || 'Please select time']"
                    />
                  </div>

                  <!-- Reason for Appointment -->
                  <div>
                    <div class="text-subtitle1 text-teal-7 q-mb-sm">Reason for Appointment</div>
                    <q-input
                      v-model="appointmentForm.reason"
                      type="textarea"
                      outlined
                      rows="4"
                      placeholder="Please describe the reason for your appointment, any symptoms, or concerns you would like to discuss..."
                      class="full-width"
                      :rules="[ (val: string | null) => !!val || 'Please provide reason for appointment']"
                    />
                  </div>

                  <q-btn 
                    type="submit" 
                    color="teal-7" 
                    label="Schedule Appointment" 
                    class="full-width q-mt-xl"
                    size="lg"
                    :loading="isSubmitting"
                  />
                </q-form>
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
import { useQuasar } from 'quasar'
import { computed } from 'vue'

const router = useRouter()
const $q = useQuasar()
const activeTab = ref('appointments')
const isSubmitting = ref(false)

const appointmentForm = ref({
  type: '',
  department: '',
  date: '',
  time: '',
  reason: ''
})

const appointmentTypes = [
  'General Consultation',
  'Follow-up Visit',
  'Lab Test',
  'Specialist Consultation',
  'Emergency Visit',
  'Routine Check-up',
  'Vaccination',
  'Physical Therapy'
]

const departments = [
  'General Medicine',
  'Cardiology',
  'Dermatology',
  'Orthopedics',
  'Pediatrics',
  'Gynecology',
  'Neurology',
  'Emergency',
  'Laboratory',
  'Radiology'
]

const timeSlots = [
  '8:00 AM',
  '8:30 AM',
  '9:00 AM',
  '9:30 AM',
  '10:00 AM',
  '10:30 AM',
  '11:00 AM',
  '11:30 AM',
  '1:00 PM',
  '1:30 PM',
  '2:00 PM',
  '2:30 PM',
  '3:00 PM',
  '3:30 PM',
  '4:00 PM',
  '4:30 PM'
]

const navigateTo = (path: string) => {
  void router.push(path)
}

const scheduleAppointment = () => {
  try {
    $q.notify({
      type: 'positive',
      message: 'Appointment scheduled successfully!',
      position: 'top'
    })

    // Navigate back to appointments
    void router.push('/patient-appointments')
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Failed to schedule appointment. Please try again.',
      position: 'top'
    })
  }
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
.appointment-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>