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
        <div class="text-h5 text-grey-8 q-mb-lg">Manage Your Appointments</div>
        
        <div class="row q-gutter-lg">
          <!-- New Appointment Card -->
          <div class="col-12 col-md-4">
            <q-card class="new-appointment-card bg-teal-6 text-white">
              <q-card-section class="q-pa-lg">
                <div class="row items-center q-mb-md">
                  <q-icon name="add_circle" size="32px" class="q-mr-sm" />
                  <div class="text-h6">New Appointment</div>
                </div>
                <div class="text-body2 q-mb-lg">
                  Schedule your next consultation, lab test, or procedure quickly.
                </div>
                <q-btn 
                  color="white" 
                  text-color="teal-6" 
                  label="Book Now" 
                  class="full-width"
                  @click="navigateTo('/patient-appointment-schedule')"
                />
              </q-card-section>
            </q-card>
          </div>

          <!-- Appointments List -->
          <div class="col-12 col-md-8">
            <q-card>
              <q-card-section>
                <!-- Filter Tabs -->
                <q-tabs 
                  v-model="activeFilter" 
                  class="text-teal-7 q-mb-lg"
                  active-color="teal-7"
                  indicator-color="teal-7"
                  align="left"
                >
                  <q-tab name="upcoming" label="Upcoming" />
                  <q-tab name="completed" label="Completed" />
                  <q-tab name="cancelled" label="Cancelled" />
                </q-tabs>

                <!-- Appointments Count -->
                <div class="text-h6 text-grey-8 q-mb-md">
                  {{ activeFilter === 'upcoming' ? 'Upcoming' : activeFilter === 'completed' ? 'Completed' : 'Cancelled' }} 
                  Appointments ({{ filteredAppointments.length }})
                </div>

                <!-- Appointments List -->
                <div class="q-gutter-sm">
                  <q-card 
                    v-for="appointment in filteredAppointments" 
                    :key="appointment.id"
                    flat 
                    bordered 
                    class="appointment-item"
                  >
                    <q-card-section class="q-pa-md">
                      <div class="row items-center">
                        <div class="col-1">
                          <div class="appointment-indicator" :class="getIndicatorClass(appointment.type)"></div>
                        </div>
                        <div class="col-8">
                          <div class="text-weight-medium text-grey-8">{{ appointment.type }}</div>
                          <div class="text-body2 text-grey-6">{{ appointment.doctor }} | {{ appointment.datetime }}</div>
                        </div>
                        <div class="col-3 text-right">
                          <q-btn flat round icon="chevron_right" @click="viewAppointment(appointment)" />
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>

                  <!-- Empty State -->
                  <div v-if="filteredAppointments.length === 0" class="text-center q-pa-xl">
                    <q-icon name="event_busy" size="64px" class="text-grey-4 q-mb-md" />
                    <div class="text-h6 text-grey-5">No {{ activeFilter }} appointments</div>
                    <div class="text-body2 text-grey-4">
                      {{ activeFilter === 'upcoming' ? 'Schedule your first appointment to get started.' : 
                         activeFilter === 'completed' ? 'Your completed appointments will appear here.' : 
                         'Your cancelled appointments will appear here.' }}
                    </div>
                  </div>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeTab = ref('appointments')
const activeFilter = ref('upcoming')

interface Appointment {
  id: number
  type: string
  doctor: string
  datetime: string
  status: 'upcoming' | 'completed' | 'cancelled'
}

const appointments = ref<Appointment[]>([
  {
    id: 1,
    type: 'Follow Up',
    doctor: 'Dr. Amelia Chen',
    datetime: 'Wednesday, October 8, 2025 at 10:00 PM',
    status: 'upcoming'
  },
  {
    id: 2,
    type: 'Lab Test',
    doctor: 'Dr. Robert Wilson',
    datetime: 'Thursday, October 23, 2025 at 7:00 PM',
    status: 'upcoming'
  },
  {
    id: 3,
    type: 'General Consultation',
    doctor: 'Dr. Lisa Wang',
    datetime: 'Thursday, October 23, 2025 at 8:00 PM',
    status: 'upcoming'
  },
  {
    id: 4,
    type: 'General Consultation',
    doctor: 'Dr. Amelia Chen',
    datetime: 'Thursday, October 9, 2025 at 10:00 AM',
    status: 'upcoming'
  }
])

const filteredAppointments = computed(() => {
  return appointments.value.filter(appointment => appointment.status === activeFilter.value)
})

const navigateTo = (path: string) => {
  void router.push(path)
}

const getIndicatorClass = (type: string) => {
  const typeMap: Record<string, string> = {
    'Follow Up': 'bg-blue-5',
    'Lab Test': 'bg-purple-5',
    'General Consultation': 'bg-green-5',
    'Specialist Consultation': 'bg-orange-5'
  }
  return typeMap[type] || 'bg-grey-5'
}

const viewAppointment = (appointment: Appointment) => {
  // Handle appointment view/edit
  console.log('Viewing appointment:', appointment)
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
.new-appointment-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.appointment-item {
  border-radius: 8px;
  transition: all 0.2s ease;
}

.appointment-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.appointment-indicator {
  width: 4px;
  height: 40px;
  border-radius: 2px;
}
</style>