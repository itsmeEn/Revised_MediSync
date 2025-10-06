<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header elevated class="bg-teal-7 text-white">
      <q-toolbar>
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
        <!-- Navigation Cards -->
        <div class="row q-gutter-md q-mb-lg">
          <div class="col-12 col-sm-6 col-md-3">
            <q-card 
              class="dashboard-card cursor-pointer" 
              @click="navigateTo('/patient-queue')"
            >
              <q-card-section class="text-center q-pa-lg">
                <q-icon name="queue" size="48px" class="text-teal-6 q-mb-md" />
                <div class="text-h6 text-grey-8">Queue Status</div>
              </q-card-section>
            </q-card>
          </div>
          
          <div class="col-12 col-sm-6 col-md-3">
            <q-card 
              class="dashboard-card cursor-pointer" 
              @click="navigateTo('/patient-appointments')"
            >
              <q-card-section class="text-center q-pa-lg">
                <q-icon name="event" size="48px" class="text-teal-6 q-mb-md" />
                <div class="text-h6 text-grey-8">Appointments</div>
              </q-card-section>
            </q-card>
          </div>
          
          <div class="col-12 col-sm-6 col-md-3">
            <q-card 
              class="dashboard-card cursor-pointer" 
              @click="navigateTo('/patient-notifications')"
            >
              <q-card-section class="text-center q-pa-lg">
                <q-icon name="notifications" size="48px" class="text-teal-6 q-mb-md" />
                <div class="text-h6 text-grey-8">Notifications</div>
              </q-card-section>
            </q-card>
          </div>
          
          <div class="col-12 col-sm-6 col-md-3">
            <q-card 
              class="dashboard-card cursor-pointer" 
              @click="navigateTo('/patient-medical-request')"
            >
              <q-card-section class="text-center q-pa-lg">
                <q-icon name="description" size="48px" class="text-teal-6 q-mb-md" />
                <div class="text-h6 text-grey-8">Medical Request</div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Live Queue Status -->
        <q-card class="q-mb-lg">
          <q-card-section>
            <div class="text-h6 text-grey-8 q-mb-md">Live Queue Status</div>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-card class="bg-teal-6 text-white">
                  <q-card-section>
                    <div class="text-caption text-teal-2">NOW SERVING</div>
                    <div class="text-h3 text-weight-bold">001</div>
                    <div class="text-body2">Eylissa Rose's Patient</div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-md-6">
                <q-card class="bg-teal-6 text-white">
                  <q-card-section>
                    <div class="text-caption text-teal-2">MY QUEUE STATUS</div>
                    <div class="text-h3 text-weight-bold">005</div>
                    <div class="text-body2">{{ userName }}</div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-card-section>
        </q-card>
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
const activeTab = ref('home')

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
</script>

<style scoped>
.dashboard-card {
  transition: all 0.3s ease;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.dashboard-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
</style>