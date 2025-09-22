<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header class="notifications-header">
      <div class="header-content">
        <q-btn
          flat
          round
          dense
          icon="arrow_back"
          @click="goBack"
          class="back-btn"
          aria-label="Go back"
        />
        <div class="header-title">Notifications</div>
        <q-btn
          flat
          round
          dense
          icon="mark_email_read"
          @click="markAllAsRead"
          class="mark-read-btn"
          aria-label="Mark all as read"
        />
      </div>
    </q-header>

    <!-- Main content area -->
    <q-page-container class="page-background">
      <div class="q-pa-md">
        <!-- Notification Filter Tabs -->
        <div class="notification-tabs-container">
          <q-btn-toggle
            v-model="selectedTab"
            :options="tabOptions"
            class="notification-tabs"
            toggle-color="primary"
            color="white"
            text-color="primary"
            rounded
            unelevated
          />
        </div>

        <!-- Notifications Section -->
        <div class="notifications-section">
          <div class="section-title">{{ getSectionTitle() }}</div>
          
          <!-- All Notifications -->
          <div v-if="selectedTab === 'all'" class="notification-cards">
            <div 
              v-for="notification in allNotifications" 
              :key="notification.id"
              class="notification-card"
              :class="{ 'unread': !notification.read }"
            >
              <div class="card-left-border" :class="notification.type"></div>
              <div class="card-content">
                <div class="notification-header">
                  <div class="notification-title">{{ notification.title }}</div>
                  <div class="notification-time">{{ formatTime(notification.timestamp) }}</div>
                </div>
                <div class="notification-message">{{ notification.message }}</div>
                <div class="notification-type-badge" :class="notification.type">
                  {{ capitalize(notification.type) }}
                </div>
                <div v-if="!notification.read" class="unread-indicator"></div>
              </div>
            </div>
          </div>

          <!-- Unread Notifications -->
          <div v-if="selectedTab === 'unread'" class="notification-cards">
            <div 
              v-for="notification in unreadNotifications" 
              :key="notification.id"
              class="notification-card unread"
            >
              <div class="card-left-border" :class="notification.type"></div>
              <div class="card-content">
                <div class="notification-header">
                  <div class="notification-title">{{ notification.title }}</div>
                  <div class="notification-time">{{ formatTime(notification.timestamp) }}</div>
                </div>
                <div class="notification-message">{{ notification.message }}</div>
                <div class="notification-type-badge" :class="notification.type">
                  {{ capitalize(notification.type) }}
                </div>
                <div class="unread-indicator"></div>
                <div class="notification-actions">
                  <q-btn 
                    class="mark-read-btn"
                    color="primary"
                    outline
                    rounded
                    label="Mark as Read"
                    @click="markAsRead(notification.id)"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Read Notifications -->
          <div v-if="selectedTab === 'read'" class="notification-cards">
            <div 
              v-for="notification in readNotifications" 
              :key="notification.id"
              class="notification-card read"
            >
              <div class="card-left-border" :class="notification.type"></div>
              <div class="card-content">
                <div class="notification-header">
                  <div class="notification-title">{{ notification.title }}</div>
                  <div class="notification-time">{{ formatTime(notification.timestamp) }}</div>
                </div>
                <div class="notification-message">{{ notification.message }}</div>
                <div class="notification-type-badge" :class="notification.type">
                  {{ capitalize(notification.type) }}
                </div>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-if="getCurrentNotifications().length === 0" class="empty-state">
            <q-icon name="notifications_none" size="64px" color="grey-5" />
            <div class="empty-text">No {{ selectedTab }} notifications</div>
          </div>
        </div>
      </div>
    </q-page-container>

    <!-- Footer with Navigation -->
    <q-footer class="custom-footer transparent-footer">
      <div class="footer-tabs-wrapper">
        <q-tabs
          v-model="activeTab"
          class="footer-tabs"
          align="justify"
          dense
          inverted
          indicator-color="transparent"
        >
          <q-tab
            v-for="(item, idx) in navItems"
            :key="item.name"
            :name="idx"
            class="footer-tab"
            :class="{ 'highlighted-tab': activeTab === idx }"
            @click="navigateToTab(item.route as string)"
          >
            <div class="footer-tab-inner">
              <div
                class="footer-highlight-bg"
                v-if="activeTab === idx"
              />
              <q-icon :name="item.icon" class="footer-icon" :class="{ active: activeTab === idx }"/>
              <div class="footer-tab-label" :class="{ active: activeTab === idx }">{{ capitalize(item.label) }}</div>
            </div>
          </q-tab>
        </q-tabs>
      </div>
    </q-footer>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { api } from "../boot/axios";

interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_verified: boolean;
  date_of_birth?: string | null;
  profile_picture?: string | null;
}

interface Notification {
  id: number;
  title: string;
  message: string;
  type: 'appointment' | 'medical' | 'system' | 'reminder';
  timestamp: string;
  read: boolean;
}

const router = useRouter();
const $q = useQuasar();

const user = ref<User | null>(null);
const activeTab = ref(3); // Notifications tab is active
const selectedTab = ref('all');

// Tab options for notification filter
const tabOptions = [
  { label: 'All', value: 'all' },
  { label: 'Unread', value: 'unread' },
  { label: 'Read', value: 'read' }
];

// Navigation items
const navItems = [
  { name: "home", icon: "home", label: "dashboard", route: "/patient-dashboard" },
  { name: "appointments", icon: "event_note", label: "appointment", route: "/patient-appointment" },
  { name: "medical-request", icon: "medical_services", label: "medical request", route: "/patient-medical-request" },
  { name: "notifications", icon: "notifications_none", label: "notification", route: "/patient-notifications" },
  { name: "settings", icon: "settings", label: "account settings", route: "/patient-settings" },
] as const;

// Sample notification data
const allNotifications = ref<Notification[]>([
  {
    id: 1,
    title: 'Appointment Reminder',
    message: 'Your appointment with Dr. Smith is scheduled for tomorrow at 10:00 AM.',
    type: 'appointment',
    timestamp: '2025-01-20T09:00:00Z',
    read: false
  },
  {
    id: 2,
    title: 'Medical Request Approved',
    message: 'Your prescription refill request has been approved. You can pick up your medication at the pharmacy.',
    type: 'medical',
    timestamp: '2025-01-19T14:30:00Z',
    read: false
  },
  {
    id: 3,
    title: 'System Update',
    message: 'We have updated our system. Please log out and log back in to experience the new features.',
    type: 'system',
    timestamp: '2025-01-18T08:00:00Z',
    read: true
  },
  {
    id: 4,
    title: 'Lab Results Available',
    message: 'Your recent lab test results are now available in your patient portal.',
    type: 'medical',
    timestamp: '2025-01-17T16:45:00Z',
    read: true
  },
  {
    id: 5,
    title: 'Appointment Cancelled',
    message: 'Your appointment scheduled for January 25th has been cancelled. Please reschedule at your convenience.',
    type: 'appointment',
    timestamp: '2025-01-16T11:20:00Z',
    read: true
  }
]);

// Computed properties
const unreadNotifications = computed(() => 
  allNotifications.value.filter(notification => !notification.read)
);

const readNotifications = computed(() => 
  allNotifications.value.filter(notification => notification.read)
);

const getSectionTitle = () => {
  switch (selectedTab.value) {
    case 'all': return 'All Notifications';
    case 'unread': return 'Unread Notifications';
    case 'read': return 'Read Notifications';
    default: return 'Notifications';
  }
};

const getCurrentNotifications = () => {
  switch (selectedTab.value) {
    case 'unread': return unreadNotifications.value;
    case 'read': return readNotifications.value;
    default: return allNotifications.value;
  }
};

// Methods
const goBack = () => {
  void router.push('/patient-dashboard');
};

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
  
  if (diffInHours < 1) {
    return 'Just now';
  } else if (diffInHours < 24) {
    return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;
  } else {
    const diffInDays = Math.floor(diffInHours / 24);
    return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`;
  }
};

const markAsRead = (notificationId: number) => {
  const notification = allNotifications.value.find(n => n.id === notificationId);
  if (notification) {
    notification.read = true;
    $q.notify({
      type: 'positive',
      message: 'Notification marked as read',
      position: 'top'
    });
  }
};

const markAllAsRead = () => {
  allNotifications.value.forEach(notification => {
    notification.read = true;
  });
  $q.notify({
    type: 'positive',
    message: 'All notifications marked as read',
    position: 'top'
  });
};

const navigateToTab = (route: string | undefined) => {
  if (route && route !== '/patient-notifications') {
    void router.push(route);
  }
};

const capitalize = (str: string) => {
  return str.replace(/\b\w/g, c => c.toUpperCase());
};

const loadUser = async () => {
  try {
    const resp = await api.get("/users/profile/");
    user.value = resp.data.user;
    localStorage.setItem("user", JSON.stringify(user.value));
  } catch {
    const cached = localStorage.getItem("user");
    if (cached) {
      try {
        user.value = JSON.parse(cached);
        return;
      } catch {
        localStorage.removeItem("user");
        user.value = null;
      }
    }
    $q.notify({
      type: "negative",
      message: "Session expired. Please log in again.",
      position: "top",
    });
    void router.push("/login");
  }
};

onMounted(() => {
  void loadUser();
});
</script>

<style scoped>
.page-background {
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 50%, #d4edda 100%);
  min-height: 100vh;
}

.notifications-header {
  background: #286660;
  min-height: 70px;
  max-height: 70px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 12px 0 rgba(64,110,101,0.08);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18px;
  height: 100%;
  width: 100%;
}

.back-btn, .mark-read-btn {
  color: white;
  font-size: 24px;
}

.header-title {
  color: white;
  font-weight: 600;
  font-size: 1.25rem;
  text-align: center;
  flex: 1;
}

.notification-tabs-container {
  margin: 20px 0;
  display: flex;
  justify-content: center;
}

.notification-tabs {
  background: white;
  border-radius: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.notifications-section {
  margin-bottom: 30px;
}

.section-title {
  color: #286660;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.notification-cards {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.notification-card {
  background: #e8f5e8;
  border-radius: 12px;
  padding: 20px;
  position: relative;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: flex-start;
  transition: all 0.3s ease;
  cursor: pointer;
}

.notification-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  background: #d4f0d4;
}

.notification-card.unread {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
}

.notification-card.read {
  opacity: 0.7;
}

.card-left-border {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: #286660;
  border-radius: 12px 0 0 12px;
}

.card-left-border.appointment {
  background: #2196f3;
}

.card-left-border.medical {
  background: #4caf50;
}

.card-left-border.system {
  background: #ff9800;
}

.card-left-border.reminder {
  background: #9c27b0;
}

.card-content {
  flex: 1;
  margin-left: 10px;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.notification-title {
  color: #286660;
  font-weight: 600;
  font-size: 1rem;
  flex: 1;
}

.notification-time {
  color: #666;
  font-size: 0.8rem;
  margin-left: 10px;
}

.notification-message {
  color: #286660;
  font-size: 0.9rem;
  margin-bottom: 10px;
  line-height: 1.4;
}

.notification-type-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #286660;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.notification-type-badge.appointment {
  background: #2196f3;
}

.notification-type-badge.medical {
  background: #4caf50;
}

.notification-type-badge.system {
  background: #ff9800;
}

.notification-type-badge.reminder {
  background: #9c27b0;
}

.unread-indicator {
  position: absolute;
  top: 15px;
  right: 80px;
  width: 8px;
  height: 8px;
  background: #ff4444;
  border-radius: 50%;
}

.notification-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  flex-wrap: wrap;
}

.mark-read-btn {
  flex: 1;
  min-width: 120px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.empty-text {
  margin-top: 16px;
  font-size: 1.1rem;
  color: #666;
}

/* Footer styles with white background */
.custom-footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100vw;
  background: white !important;
  box-shadow: 0 -2px 12px rgba(0,0,0,0.1);
  border: none;
  z-index: 1000;
  padding: 0;
}

.transparent-footer {
  background: white !important;
}

.footer-tabs-wrapper {
  width: 100vw;
  background: white !important;
}

.footer-tabs {
  width: 100vw;
  background: white !important;
  min-height: 74px;
  border-bottom: none;
  box-shadow: none;
}

.footer-tab {
  flex: 1 1 0;
  min-width: 0;
  background: transparent !important;
  margin: 0 !important;
  padding: 0 !important;
  max-width: 20vw;
  transition: all 0.3s ease;
  cursor: pointer;
}

.footer-tab:hover {
  transform: translateY(-2px);
}

.footer-tab-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  min-width: 0;
  width: 100%;
  padding: 0;
  position: relative;
  transition: all 0.3s ease;
}

.footer-highlight-bg {
  position: absolute;
  left: 50%;
  top: -9px;
  width: 44px;
  height: 24px;
  background: #eaf6f3;
  border-radius: 10px 10px 12px 12px;
  transform: translateX(-50%);
  z-index: 3;
  box-sizing: border-box;
  border-top: 5px solid #6ca299;
  border-bottom: none;
  border-left: none;
  border-right: none;
  pointer-events: none;
}

.footer-icon {
  color: #6ca299b3;
  font-size: 29px;
  min-width: 32px;
  min-height: 32px;
  transition: all 0.3s ease;
  margin-bottom: 2px;
  z-index: 2;
  position: relative;
}

.footer-tab:hover .footer-icon {
  color: #286660;
  transform: scale(1.1);
}

.footer-icon.active {
  color: #6ca299 !important;
  z-index: 4;
}

.footer-tab-label {
  font-size: 0.82rem;
  color: #6ca299b3;
  font-weight: 500;
  letter-spacing: 0.01em;
  text-align: center;
  margin-bottom: 2px;
  margin-top: 2px;
  transition: all 0.3s ease;
  max-width: 95px;
  overflow: visible;
  white-space: normal;
  z-index: 2;
  text-transform: capitalize;
  line-height: 1.1;
}

.footer-tab:hover .footer-tab-label {
  color: #286660;
  font-weight: 600;
  transform: scale(1.05);
}

.footer-tab-label.active {
  font-weight: 700;
  color: #6ca299;
}

.highlighted-tab .footer-icon,
.highlighted-tab .footer-tab-label {
  color: #6ca299 !important;
}

.highlighted-tab .footer-icon {
  font-weight: 700;
  z-index: 4;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .footer-tabs,
  .footer-tabs-wrapper {
    min-height: 60px;
    height: 60px;
  }
  
  .footer-tab-label {
    font-size: 0.74rem;
    max-width: 80px;
    margin-bottom: 2px;
    margin-top: 1px;
    line-height: 1.1;
    overflow: visible;
    white-space: normal;
  }
  
  .footer-tab {
    max-width: 24vw;
  }
  
  .footer-icon {
    font-size: 20px;
    min-width: 20px;
    min-height: 20px;
    margin-bottom: 1px;
    margin-top: 1px;
  }
  
  .footer-tab-inner {
    min-width: 0;
    width: 100%;
    padding: 0 1px;
  }
  
  .footer-highlight-bg {
    border-radius: 8px 8px 10px 10px;
    border-top-width: 4px;
    width: 35px;
    height: 18px;
    top: -7px;
  }

  .notification-card {
    padding: 15px;
  }

  .notification-type-badge {
    position: static;
    display: inline-block;
    margin-top: 10px;
  }

  .notification-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .notification-time {
    margin-left: 0;
    margin-top: 4px;
  }
}
</style>
