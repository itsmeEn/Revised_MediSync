<template>
  <q-layout view="hHh Lpr fFf">

    <q-header reveal elevated class="text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleRightDrawer" />
        
        <q-toolbar-title>
          <q-avatar>
            <img src="../assets/logo.png" alt="MediSync Logo" />
          </q-avatar>
          MediSync
        </q-toolbar-title>
      </q-toolbar>

      <q-toolbar class="text-white">
        <div class="search-container">
          <q-input 
            dark 
            dense 
            standout 
            v-model="text" 
            placeholder="Search patients, symptoms, appointments..."
            class="search-input"
          >
            <template v-slot:append>
              <q-icon v-if="text === 'Patient Name, Sickness, Appointment'" name="search" />
              <q-icon v-else name="clear" class="cursor-pointer" @click="text = ''" />
            </template>
          </q-input>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="rightDrawerOpen" side="left" overlay bordered>
      <div class="drawer-content">
        <!-- User Profile Section -->
        <div class="user-profile-section">
          <div class="profile-picture-container">
            <q-avatar size="100px" class="profile-avatar">
              <img v-if="userProfile.profile_picture" :src="userProfile.profile_picture" alt="Profile Picture" />
              <div v-else class="profile-placeholder">
                {{ userInitials }}
              </div>
            </q-avatar>
            <q-btn
              round
              color="primary"
              icon="camera_alt"
              size="sm"
              class="upload-btn"
              @click="triggerFileUpload"
            />
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              style="display: none"
              @change="handleProfilePictureUpload"
            />
          </div>
          
          <div class="user-info">
            <h6 class="user-name">{{ userProfile.full_name }}</h6>
            <p class="user-specialization">{{ userProfile.specialization }}</p>
            <q-chip color="primary" text-color="white" size="sm">
              {{ userProfile.role }}
            </q-chip>
          </div>
        </div>

        <!-- Navigation Menu -->
        <q-list class="navigation-menu">
          <q-item clickable v-ripple @click="navigateTo('doctor-dashboard')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('appointments')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="event" />
            </q-item-section>
            <q-item-section>Appointments</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('messaging')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="message" />
            </q-item-section>
            <q-item-section>Messaging</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('patients')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>
            <q-item-section>Patient Management</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('analytics')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="analytics" />
            </q-item-section>
            <q-item-section>Analytics</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="navigateTo('settings')" class="nav-item">
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>
            <q-item-section>Settings</q-item-section>
          </q-item>
        </q-list>

        <!-- Logout Section -->
        <div class="logout-section">
          <q-btn
            color="negative"
            icon="logout"
            label="Logout"
            class="logout-btn"
            @click="logout"
          />
        </div>
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../boot/axios'

const router = useRouter()
const rightDrawerOpen = ref(false)
const text = ref('Patient Name, Sickness, Appointment')
const fileInput = ref<HTMLInputElement>()

// Mock user profile data - replace with actual API call
const userProfile = ref({
  full_name: 'Dr. John Doe',
  specialization: 'Cardiology',
  role: 'Doctor',
  profile_picture: null
})

const userInitials = computed(() => {
  if (!userProfile.value.full_name) return 'U'
  return userProfile.value.full_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
})

const toggleRightDrawer = () => {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleProfilePictureUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    
    try {
      const formData = new FormData()
      formData.append('profile_picture', file)
      
      const response = await api.post('/users/profile-picture/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      userProfile.value.profile_picture = response.data.profile_picture
      alert('Profile picture updated successfully!')
    } catch (error) {
      console.error('Profile picture upload failed:', error)
      alert('Failed to upload profile picture. Please try again.')
    }
  }
}

const navigateTo = (route: string) => {
  // Close drawer first
  rightDrawerOpen.value = false
  
  // Navigate to different sections (you can implement actual routing)
  switch (route) {
    case 'dashboard':
      // Already on dashboard
      break
    case 'appointments':
      alert('Appointments page - Coming soon!')
      break
    case 'messaging':
      alert('Messaging page - Coming soon!')
      break
    case 'patients':
      alert('Patient Management page - Coming soon!')
      break
    case 'analytics':
      alert('Analytics page - Coming soon!')
      break
    case 'settings':
      alert('Settings page - Coming soon!')
      break
  }
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  void router.push('/login')
}

onMounted(() => {
  // Load user profile data from localStorage or API
  const userData = localStorage.getItem('user')
  if (userData) {
    const user = JSON.parse(userData)
    userProfile.value = {
      full_name: user.full_name || 'Dr. John Doe',
      specialization: user.doctor_profile?.specialization || 'General Medicine',
      role: user.role || 'Doctor',
      profile_picture: user.profile_picture || null
    }
  }
})
</script>

<style scoped>
.search-container {
  display: flex;
  justify-content: center;
  width: 100%;
  padding: 0 20px;
}

.search-input {
  max-width: 600px;
  width: 100%;
}

.q-header {
  background: #286660 !important;
}

.q-toolbar {
  background: #286660 !important;
}

.q-avatar {
  background: white;
  border-radius: 8px;
}

.q-avatar img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Drawer Styles */
.drawer-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.user-profile-section {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.profile-picture-container {
  position: relative;
  display: inline-block;
  margin-bottom: 15px;
}

.profile-avatar {
  border: 3px solid #1e7668;
}

.profile-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1e7668;
  color: white;
  font-size: 24px;
  font-weight: bold;
  border-radius: 50%;
}

.upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #1e7668 !important;
}

.user-info {
  margin-top: 10px;
}

.user-name {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.user-specialization {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
}

.navigation-menu {
  flex: 1;
  padding: 10px 0;
}

.nav-item {
  margin: 5px 10px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background: rgba(30, 118, 104, 0.1);
}

.nav-item .q-icon {
  color: #1e7668;
}

.logout-section {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
}

.logout-btn {
  width: 100%;
}
</style>