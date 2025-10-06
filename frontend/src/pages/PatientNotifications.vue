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
          <q-badge color="red" floating>3</q-badge>
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
          <div class="text-h5 text-grey-8">Notifications</div>
          <q-btn 
            flat 
            color="teal-6" 
            label="Mark All Read" 
            @click="markAllRead"
          />
        </div>

        <!-- Filter Tabs -->
        <q-tabs
          v-model="activeFilter"
          class="text-grey-6 q-mb-lg"
          active-color="teal-6"
          indicator-color="teal-6"
          align="left"
        >
          <q-tab name="all" label="All" />
          <q-tab name="unread" label="Unread" />
          <q-tab name="appointments" label="Appointments" />
          <q-tab name="queue" label="Queue" />
          <q-tab name="medical" label="Medical" />
        </q-tabs>

        <!-- Notifications List -->
        <div class="q-gutter-sm">
          <!-- Unread Notification -->
          <q-card class="notification-card unread" v-for="notification in filteredNotifications" :key="notification.id">
            <q-card-section class="q-pa-md">
              <div class="row items-start">
                <div class="col-1">
                  <q-avatar :color="notification.iconColor" text-color="white" size="40px">
                    <q-icon :name="notification.icon" />
                  </q-avatar>
                </div>
                <div class="col-10 q-ml-md">
                  <div class="row items-center q-mb-xs">
                    <div class="text-weight-medium text-grey-8">{{ notification.title }}</div>
                    <q-space />
                    <div class="text-caption text-grey-5">{{ notification.time }}</div>
                  </div>
                  <div class="text-body2 text-grey-6 q-mb-sm">{{ notification.message }}</div>
                  <div class="row items-center">
                    <q-chip 
                      :color="notification.categoryColor" 
                      text-color="white" 
                      size="sm" 
                      :label="notification.category"
                    />
                    <q-space />
                    <q-btn 
                      v-if="!notification.read"
                      flat 
                      size="sm" 
                      color="teal-6" 
                      label="Mark as Read"
                      @click="markAsRead(notification.id)"
                    />
                  </div>
                </div>
                <div class="col-1 text-right">
                  <q-btn flat round size="sm" icon="more_vert">
                    <q-menu>
                      <q-list>
                        <q-item clickable v-close-popup @click="markAsRead(notification.id)">
                          <q-item-section>Mark as Read</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click="deleteNotification(notification.id)">
                          <q-item-section class="text-red">Delete</q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </q-btn>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Empty State -->
          <div v-if="filteredNotifications.length === 0" class="text-center q-pa-xl">
            <q-icon name="notifications_none" size="80px" class="text-grey-4" />
            <div class="text-h6 text-grey-5 q-mt-md">No notifications</div>
            <div class="text-body2 text-grey-4">You're all caught up!</div>
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
const activeTab = ref('alerts')
const activeFilter = ref('all')

interface Notification {
  id: number
  title: string
  message: string
  time: string
  category: string
  categoryColor: string
  icon: string
  iconColor: string
  read: boolean
  type: string
}

const notifications = ref<Notification[]>([
  {
    id: 1,
    title: 'Appointment Reminder',
    message: 'Your appointment with Dr. Smith is scheduled for tomorrow at 2:00 PM.',
    time: '2 hours ago',
    category: 'Appointment',
    categoryColor: 'blue-6',
    icon: 'event',
    iconColor: 'blue-6',
    read: false,
    type: 'appointments'
  },
  {
    id: 2,
    title: 'Queue Update',
    message: 'You are now #3 in the queue. Estimated wait time: 15 minutes.',
    time: '30 minutes ago',
    category: 'Queue',
    categoryColor: 'orange-6',
    icon: 'queue',
    iconColor: 'orange-6',
    read: false,
    type: 'queue'
  },
  {
    id: 3,
    title: 'Medical Records Ready',
    message: 'Your requested medical records are now available for download.',
    time: '1 day ago',
    category: 'Medical',
    categoryColor: 'green-6',
    icon: 'description',
    iconColor: 'green-6',
    read: false,
    type: 'medical'
  },
  {
    id: 4,
    title: 'Appointment Confirmed',
    message: 'Your appointment for January 15th has been confirmed.',
    time: '2 days ago',
    category: 'Appointment',
    categoryColor: 'blue-6',
    icon: 'check_circle',
    iconColor: 'green-6',
    read: true,
    type: 'appointments'
  },
  {
    id: 5,
    title: 'System Maintenance',
    message: 'The system will be under maintenance on Sunday from 2-4 AM.',
    time: '3 days ago',
    category: 'System',
    categoryColor: 'grey-6',
    icon: 'build',
    iconColor: 'grey-6',
    read: true,
    type: 'system'
  }
])

const filteredNotifications = computed(() => {
  let filtered = notifications.value

  if (activeFilter.value === 'unread') {
    filtered = filtered.filter(n => !n.read)
  } else if (activeFilter.value !== 'all') {
    filtered = filtered.filter(n => n.type === activeFilter.value)
  }

  return filtered
})

const navigateTo = (path: string) => {
  void router.push(path)
}

const markAsRead = (id: number) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) {
    notification.read = true
    $q.notify({
      type: 'positive',
      message: 'Notification marked as read',
      position: 'top'
    })
  }
}

const markAllRead = () => {
  notifications.value.forEach(n => n.read = true)
  $q.notify({
    type: 'positive',
    message: 'All notifications marked as read',
    position: 'top'
  })
}

const deleteNotification = (id: number) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
    $q.notify({
      type: 'positive',
      message: 'Notification deleted',
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
.notification-card {
  border-radius: 8px;
  transition: all 0.2s ease;
  border-left: 4px solid transparent;
}

.notification-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.notification-card.unread {
  border-left-color: #26A69A;
  background-color: #F9FFFE;
}
</style>