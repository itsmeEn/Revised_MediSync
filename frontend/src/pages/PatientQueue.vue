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
        <div class="row items-center justify-between q-mb-lg">
          <div class="text-h5 text-grey-8">Live Queue & Wait Time</div>
          <q-chip color="teal-6" text-color="white" icon="person">{{ userName }}</q-chip>
        </div>
        
        <!-- Current Status Cards -->
        <div class="row q-gutter-md q-mb-lg">
          <div class="col-12 col-md-6">
            <q-card class="status-card">
              <q-card-section class="q-pa-lg">
                <div class="row items-center">
                  <div class="col-8">
                    <div class="text-caption text-grey-6">NOW SERVING</div>
                    <div class="text-h2 text-weight-bold text-grey-8">001</div>
                    <div class="text-body2 text-grey-6">{{ userName }}</div>
                  </div>
                  <div class="col-4 text-right">
                    <q-circular-progress
                      :value="75"
                      size="60px"
                      :thickness="0.1"
                      color="teal-6"
                      track-color="grey-3"
                      class="q-ma-md"
                    />
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
          
          <div class="col-12 col-md-6">
            <q-card class="status-card">
              <q-card-section class="q-pa-lg">
                <div class="row items-center">
                  <div class="col-8">
                    <div class="text-caption text-grey-6">YOUR QUEUE STATUS</div>
                    <div class="text-h2 text-weight-bold text-teal-6">001</div>
                    <div class="text-body2 text-grey-6">Estimated Wait: ~15 mins</div>
                  </div>
                  <div class="col-4 text-right">
                    <q-icon name="schedule" size="60px" class="text-teal-6" />
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <div class="row q-gutter-lg">
          <!-- Current Queue -->
          <div class="col-12 col-md-7">
            <q-card>
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-icon name="list" size="24px" class="text-teal-6 q-mr-sm" />
                  <div class="text-h6 text-grey-8">Current Queue</div>
                  <q-space />
                  <q-chip color="teal-6" text-color="white" label="Position: 1" />
                </div>

                <!-- Queue List -->
                <div class="q-gutter-sm">
                  <!-- Current Patient -->
                  <q-card flat bordered class="queue-item current-patient">
                    <q-card-section class="q-pa-md">
                      <div class="row items-center">
                        <div class="col-1">
                          <q-icon name="person" size="24px" class="text-teal-6" />
                        </div>
                        <div class="col-6">
                          <div class="text-weight-medium">{{ userName }} (001)</div>
                          <div class="text-caption text-grey-6">You</div>
                        </div>
                        <div class="col-3">
                          <q-chip size="sm" color="orange" text-color="white" label="Next" />
                        </div>
                        <div class="col-2 text-right">
                          <div class="text-caption text-grey-6">~15 mins</div>
                          <div class="text-caption text-grey-5">general</div>
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>

                  <!-- Other Patient -->
                  <q-card flat bordered class="queue-item">
                    <q-card-section class="q-pa-md">
                      <div class="row items-center">
                        <div class="col-1">
                          <q-icon name="person" size="24px" class="text-grey-5" />
                        </div>
                        <div class="col-6">
                          <div class="text-weight-medium">{{ userName }} (001)</div>
                          <div class="text-caption text-grey-6">You</div>
                        </div>
                        <div class="col-3">
                          <q-chip size="sm" color="grey-5" text-color="white" label="You" />
                        </div>
                        <div class="col-2 text-right">
                          <div class="text-caption text-grey-6">~15 mins</div>
                          <div class="text-caption text-grey-5">dermatology</div>
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <!-- Queue Alerts & Info -->
          <div class="col-12 col-md-5">
            <q-card>
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-icon name="info" size="24px" class="text-grey-6 q-mr-sm" />
                  <div class="text-h6 text-grey-8">Queue Alerts & Info</div>
                </div>

                <div class="text-body2 text-grey-6 q-mb-lg">
                  Request a text message alert when you are the **next patient** in line.
                </div>

                <!-- Current Wait Time Alert -->
                <q-card flat class="bg-orange-1 q-mb-md">
                  <q-card-section class="q-pa-md">
                    <div class="text-weight-medium text-orange-8">
                      Current estimated total wait time: ~15 minutes.
                    </div>
                  </q-card-section>
                </q-card>

                <!-- SMS Alert Button -->
                <q-btn 
                  color="indigo-6" 
                  icon="sms" 
                  label="Activate SMS Alert" 
                  class="full-width"
                  @click="activateSMSAlert"
                  :disable="smsAlertActive"
                />

                <div v-if="smsAlertActive" class="text-center q-mt-md">
                  <q-chip color="green" text-color="white" icon="check_circle">
                    SMS Alert Active
                  </q-chip>
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
import { useQuasar } from 'quasar'

const router = useRouter()
const $q = useQuasar()
const activeTab = ref('queue')
const smsAlertActive = ref(false)

const userName = computed(() => {
  try {
    const u = JSON.parse(localStorage.getItem('user') || '{}')
    return u.full_name || u.email || 'User'
  } catch {
    return 'User'
  }
})

const navigateTo = (path: string) => {
  void router.push(path)
}

const activateSMSAlert = () => {
  $q.notify({
    type: 'positive',
    message: 'SMS alert activated! You will receive a text when you are next in line.',
    position: 'top'
  })
  smsAlertActive.value = true
}
</script>

<style scoped>
.status-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.queue-item {
  border-radius: 8px;
  transition: all 0.2s ease;
}

.queue-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.current-patient {
  border-left: 4px solid #26A69A;
  background-color: #E0F2F1;
}
</style>