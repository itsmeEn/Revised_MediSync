<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header class="dashboard-header">
      <div class="header-content">
        <q-avatar size="48px" class="profile-avatar uploadable-avatar">
          <img v-if="profileImageUrl" :src="profileImageUrl" alt="Profile" />
          <q-icon v-else name="person" size="40px" />
          <!-- Avatar upload overlay -->
          <input
            type="file"
            accept="image/*"
            class="avatar-upload-input"
            @change="handleProfilePictureUpload"
            title="Upload profile picture"
          />
          <q-tooltip anchor="bottom middle" self="top middle" class="avatar-tooltip">
            Upload profile picture
          </q-tooltip>
        </q-avatar>
        <div class="user-info">
          <div class="user-name">{{ user?.full_name || "Fetch Users Name Here" }}</div>
          <div class="user-age">Age: {{ age !== null ? age : "" }}</div>
        </div>
        <q-space />
        <q-btn
          flat
          round
          dense
          icon="logout"
          @click="logout"
          class="logout-btn"
          aria-label="Logout"
        />
      </div>
    </q-header>

    <!-- Main content area -->
    <q-page-container class="page-background">
      <div class="q-pa-md">
        <div v-if="activeTab === 0">
          <!-- Welcome Section -->
          <div class="welcome-section">
            <div class="welcome-header">
              <div class="welcome-title">Welcome back, {{ user?.full_name || 'Patient' }}!</div>
              <div class="welcome-subtitle">Here's your health overview for today</div>
            </div>
          </div>
          
          <!-- Quick Stats Cards -->
          <div class="stats-section">
            <div class="stats-grid">
              <q-card class="stat-card">
                <q-card-section class="stat-content">
                  <q-icon name="event_note" size="32px" color="primary" />
                  <div class="stat-info">
                    <div class="stat-number">2</div>
                    <div class="stat-label">Upcoming Appointments</div>
                  </div>
                </q-card-section>
              </q-card>
              
              <q-card class="stat-card">
                <q-card-section class="stat-content">
                  <q-icon name="medical_services" size="32px" color="secondary" />
                  <div class="stat-info">
                    <div class="stat-number">1</div>
                    <div class="stat-label">Pending Requests</div>
                  </div>
                </q-card-section>
              </q-card>
              
              <q-card class="stat-card">
                <q-card-section class="stat-content">
                  <q-icon name="notifications" size="32px" color="warning" />
                  <div class="stat-info">
                    <div class="stat-number">3</div>
                    <div class="stat-label">New Notifications</div>
                  </div>
                </q-card-section>
              </q-card>
            </div>
          </div>
          
          <!-- Queue Status Card -->
          <div class="queue-status-section">
            <q-card class="queue-status-card">
              <q-card-section>
                <div class="queue-status-header">
                  <q-icon name="schedule" size="24px" color="primary" />
                  <div class="queue-status-title">Current Queue Status</div>
                </div>
                
                <div class="queue-info">
                  <div class="queue-item">
                    <div class="queue-label">Your Queue Number:</div>
                    <div class="queue-value primary">#3</div>
                  </div>
                  
                  <div class="queue-item">
                    <div class="queue-label">Estimated Wait Time:</div>
                    <div class="queue-value">15-20 minutes</div>
                  </div>
                  
                  <div class="queue-item">
                    <div class="queue-label">Department:</div>
                    <div class="queue-value">Cardiology</div>
                  </div>
                  
                  <div class="queue-item">
                    <div class="queue-label">Doctor:</div>
                    <div class="queue-value">Dr. Smith</div>
                  </div>
                </div>
                
                <div class="queue-progress">
                  <div class="progress-label">Progress</div>
                  <q-linear-progress 
                    :value="0.6" 
                    color="primary" 
                    size="8px" 
                    rounded
                    class="progress-bar"
                  />
                  <div class="progress-text">3 of 5 patients ahead of you</div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <!-- Quick Actions -->
          <div class="quick-actions-section">
            <div class="section-title">Quick Actions</div>
            <div class="actions-grid">
              <q-btn
                class="action-btn"
                color="primary"
                icon="event_note"
                label="Schedule Appointment"
                @click="navigateToTab('/patient-appointment')"
                rounded
                unelevated
              />
              <q-btn
                class="action-btn"
                color="secondary"
                icon="medical_services"
                label="Medical Request"
                @click="navigateToTab('/patient-medical-request')"
                rounded
                unelevated
              />
              <q-btn
                class="action-btn"
                color="warning"
                icon="notifications"
                label="View Notifications"
                @click="navigateToTab('/patient-notifications')"
                rounded
                unelevated
              />
            </div>
          </div>
        </div>
        <div v-else-if="activeTab === 1">
          <div class="text-subtitle1 q-mb-sm">Appointments</div>
          <div class="text-body2">Your appointments will appear here.</div>
        </div>
        <div v-else-if="activeTab === 2">
          <div class="text-subtitle1 q-mb-sm">Medical Request</div>
          <div class="text-body2">Create and track your medical requests here.</div>
        </div>
        <div v-else-if="activeTab === 3">
          <div class="text-subtitle1 q-mb-sm">Notification History</div>
          <div class="text-body2">Past notifications will be listed here.</div>
        </div>
        <div v-else-if="activeTab === 4">
          <div class="text-subtitle1 q-mb-sm">Account Settings</div>
          <div class="text-body2">Manage your account preferences here.</div>
        </div>
      </div>
    </q-page-container>

    <!-- Footer with Quasar QTabs -->
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
            @click="navigateToTab(item.route)"
          >
            <div class="footer-tab-inner">
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

// Type definitions for API error handling
interface ApiErrorResponse {
  profile_picture?: string[];
  detail?: string;
}

interface ApiError {
  response?: {
    data?: ApiErrorResponse;
  };
}

const router = useRouter();
const $q = useQuasar();

const user = ref<User | null>(null);
const activeTab = ref(0);

const navItems = [
  { name: "home", icon: "home", label: "dashboard", route: "/patient-dashboard" },
  { name: "calendar", icon: "event_note", label: "appointment", route: "/patient-appointment" },
  { name: "queue", icon: "queue", label: "queue", route: "/patient-queue" },
  { name: "medical-request", icon: "medical_services", label: "medical request", route: "/patient-medical-request" },
  { name: "notifications", icon: "notifications_none", label: "notification", route: "/patient-notifications" },
  { name: "settings", icon: "settings", label: "account settings", route: "/patient-settings" },
];

// Profile Image URL (computed)
const profileImageUrl = computed(() => {
  const pic = user.value?.profile_picture || null;
  if (!pic) return null;
  if (/^https?:/i.test(pic)) return pic;
  try {
    const u = new URL(api.defaults.baseURL || "");
    return `${u.origin}${pic.startsWith("/") ? "" : "/"}${pic}`;
  } catch {
    return `${window.location.origin}${pic.startsWith("/") ? "" : "/"}${pic}`;
  }
});

// Avatar upload handler - all fixes applied
const handleProfilePictureUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg']
    if (!allowedTypes.includes(file.type)) {
      $q.notify({
        type: 'negative',
        message: 'Please select a valid image file (JPG, PNG)',
        position: 'top',
        timeout: 3000
      })
      return
    }
    
    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      $q.notify({
        type: 'negative',
        message: 'File size must be less than 5MB',
        position: 'top',
        timeout: 3000
      })
      return
    }
    
    try {
      const formData = new FormData()
      formData.append('profile_picture', file)
      
      const response = await api.post('/users/profile/update/picture/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      // Update user.value.profile_picture (not userProfile)
      if (user.value) {
        user.value.profile_picture = response.data.user.profile_picture
      }
      
      $q.notify({
        type: 'positive',
        message: 'Profile picture updated successfully!',
        position: 'top',
        timeout: 3000
      })
      
      target.value = ''
    } catch (error: unknown) {
      console.error('Profile picture upload failed:', error)
      
      let errorMessage = 'Failed to upload profile picture. Please try again.'
      // Defensive error extraction
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as ApiError
        if (axiosError.response?.data?.profile_picture?.[0]) {
          errorMessage = axiosError.response.data.profile_picture[0]
        } else if (axiosError.response?.data?.detail) {
          errorMessage = axiosError.response.data.detail
        }
      }
      
      $q.notify({
        type: 'negative',
        message: errorMessage,
        position: 'top',
        timeout: 4000
      })
    }
  }
}

function calcAge(dobStr?: string | null): number | null {
  if (!dobStr) return null;
  const dob = new Date(dobStr);
  if (isNaN(dob.getTime())) return null; 
  const today = new Date();
  let age = today.getFullYear() - dob.getFullYear();
  const m = today.getMonth() - dob.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
    age--;
  }
  return age;
}

const age = computed(() => calcAge(user.value?.date_of_birth));

function capitalize(str: string) {
  return str.replace(/\b\w/g, c => c.toUpperCase());
}

const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  void router.push('/login');
};

const navigateToTab = (route: string | undefined) => {
  if (route && route !== '/patient-dashboard') {
    void router.push(route);
  }
};

async function loadUser() {
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
}

onMounted(loadUser);
</script>

<style scoped>
.page-background {
  background: url('/background.png') no-repeat center center;
  background-size: cover;
  min-height: 100vh;
}

.dashboard-header {
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
  padding: 0 18px;
  height: 100%;
  width: 100%;
}
.profile-avatar {
  background: #b8d2ce;
  border-radius: 50%;
  margin-right: 14px;
  flex-shrink: 0;
  position: relative;
}
.uploadable-avatar:hover .avatar-upload-input {
  opacity: 1;
}
.avatar-upload-input {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
  opacity: 0;
  z-index: 10;
}
.avatar-tooltip {
  font-size: 0.9em;
}
.user-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.user-name {
  color: #fff;
  font-weight: 600;
  font-size: 1.12rem;
  line-height: 1.2;
  margin-bottom: 2px;
}
.user-age {
  color: #e0e0e0;
  font-size: 0.99rem;
  font-weight: 400;
}
.logout-btn {
  color: white;
  margin-left: 16px;
}

/* Footer with white background */
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

/* Highlighted tab background and border - now on top of icon */
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

/* Welcome Section Styles */
.welcome-section {
  margin-bottom: 25px;
}

.welcome-header {
  text-align: center;
  padding: 20px 0;
}

.welcome-title {
  color: #286660;
  font-weight: 700;
  font-size: 1.8rem;
  margin-bottom: 8px;
}

.welcome-subtitle {
  color: #666;
  font-size: 1rem;
  font-weight: 400;
}

/* Stats Section Styles */
.stats-section {
  margin-bottom: 25px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.stat-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
}

.stat-info {
  flex: 1;
}

.stat-number {
  color: #286660;
  font-weight: 700;
  font-size: 1.8rem;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Quick Actions Section */
.quick-actions-section {
  margin-top: 25px;
}

.section-title {
  color: #286660;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.action-btn {
  min-height: 60px;
  font-weight: 600;
  font-size: 0.95rem;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

/* Queue Status Card Styles */
.queue-status-section {
  margin-top: 20px;
}

.queue-status-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-left: 4px solid #286660;
}

.queue-status-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.queue-status-title {
  color: #286660;
  font-weight: 600;
  font-size: 1.1rem;
}

.queue-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.queue-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.queue-label {
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.queue-value {
  color: #286660;
  font-weight: 600;
  font-size: 1rem;
}

.queue-value.primary {
  color: #286660;
  font-size: 1.2rem;
  font-weight: 700;
}

.queue-progress {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.progress-label {
  color: #286660;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.progress-bar {
  margin-bottom: 8px;
}

.progress-text {
  color: #666;
  font-size: 0.85rem;
  text-align: center;
}

/* Responsive adjustments for mobile */
@media (max-width: 600px) {
  .welcome-title {
    font-size: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .queue-info {
    grid-template-columns: 1fr;
    gap: 10px;
  }
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
}
</style>