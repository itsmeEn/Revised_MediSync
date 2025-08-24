<template>
  <q-page class="nurse-settings">
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <q-btn
            flat
            round
            icon="arrow_back"
            @click="goBack"
            class="back-btn"
          />
          <h4 class="page-title">Account Settings</h4>
        </div>
      </div>
    </div>

    <div class="page-content">
      <div class="row q-gutter-lg">
        <!-- Profile Settings -->
        <div class="col-12 col-lg-8">
          <q-card class="settings-card">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Profile Information</h6>
              
              <div class="profile-section">
                <div class="profile-picture-container">
                  <q-avatar size="120px" class="profile-avatar">
                    <img v-if="profilePictureUrl" :src="profilePictureUrl" alt="Profile Picture" />
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
                
                <div class="profile-form">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.firstName"
                        label="First Name"
                        outlined
                        :rules="[val => !!val || 'First name is required']"
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.lastName"
                        label="Last Name"
                        outlined
                        :rules="[val => !!val || 'Last name is required']"
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.email"
                        label="Email Address"
                        type="email"
                        outlined
                        readonly
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.phone"
                        label="Phone Number"
                        outlined
                        mask="(###) ### - ####"
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-select
                        v-model="profileForm.department"
                        :options="departmentOptions"
                        label="Department"
                        outlined
                        emit-value
                        map-options
                      />
                    </div>
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="profileForm.licenseNumber"
                        label="Nursing License Number"
                        outlined
                      />
                    </div>
                    <div class="col-12">
                      <q-input
                        v-model="profileForm.bio"
                        label="Bio"
                        type="textarea"
                        outlined
                        rows="3"
                        placeholder="Tell us about yourself..."
                      />
                    </div>
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Security Settings -->
          <q-card class="settings-card q-mt-lg">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Security Settings</h6>
              
              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="securityForm.currentPassword"
                    label="Current Password"
                    type="password"
                    outlined
                    :rules="[val => !!val || 'Current password is required']"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="securityForm.newPassword"
                    label="New Password"
                    type="password"
                    outlined
                    :rules="[
                      val => !!val || 'New password is required',
                      val => val.length >= 8 || 'Password must be at least 8 characters'
                    ]"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="securityForm.confirmPassword"
                    label="Confirm New Password"
                    type="password"
                    outlined
                    :rules="[
                      val => !!val || 'Please confirm your password',
                      val => val === securityForm.newPassword || 'Passwords do not match'
                    ]"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-toggle
                    v-model="securityForm.twoFactorAuth"
                    label="Enable Two-Factor Authentication"
                    color="primary"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Notification Settings -->
          <q-card class="settings-card q-mt-lg">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Notification Preferences</h6>
              
              <div class="notification-settings">
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">Patient Alerts</div>
                    <div class="notification-description">Receive notifications for patient emergencies and urgent care needs</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.patientAlerts"
                    color="primary"
                  />
                </div>
                
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">Medication Reminders</div>
                    <div class="notification-description">Get reminded about medication schedules and administration</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.medicationReminders"
                    color="primary"
                  />
                </div>
                
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">Assessment Updates</div>
                    <div class="notification-description">Notifications for completed assessments and pending tasks</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.assessmentUpdates"
                    color="primary"
                  />
                </div>
                
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">Inventory Alerts</div>
                    <div class="notification-description">Low stock and expiry notifications for medications</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.inventoryAlerts"
                    color="primary"
                  />
                </div>
                
                <div class="notification-item">
                  <div class="notification-info">
                    <div class="notification-title">System Updates</div>
                    <div class="notification-description">Important system maintenance and feature updates</div>
                  </div>
                  <q-toggle
                    v-model="notificationSettings.systemUpdates"
                    color="primary"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Sidebar Settings -->
        <div class="col-12 col-lg-4">
          <!-- Quick Actions -->
          <q-card class="settings-card">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Quick Actions</h6>
              
              <div class="q-gutter-md">
                <q-btn
                  color="primary"
                  label="Save Changes"
                  icon="save"
                  class="full-width"
                  @click="saveSettings"
                  :loading="saving"
                />
                
                <q-btn
                  color="secondary"
                  label="Export Data"
                  icon="download"
                  class="full-width"
                  @click="exportData"
                />
                
                <q-btn
                  color="accent"
                  label="Backup Settings"
                  icon="backup"
                  class="full-width"
                  @click="backupSettings"
                />
              </div>
            </q-card-section>
          </q-card>

          <!-- Account Status -->
          <q-card class="settings-card q-mt-lg">
            <q-card-section>
              <h6 class="text-h6 q-mb-md">Account Status</h6>
              
              <div class="status-item">
                <div class="status-label">Account Type</div>
                <div class="status-value">Nurse</div>
              </div>
              
              <div class="status-item">
                <div class="status-label">Verification Status</div>
                <div class="status-value">
                  <q-chip
                    :color="accountStatus.verified ? 'positive' : 'warning'"
                    text-color="white"
                    :label="accountStatus.verified ? 'Verified' : 'Pending'"
                    size="sm"
                  />
                </div>
              </div>
              
              <div class="status-item">
                <div class="status-label">Last Login</div>
                <div class="status-value">{{ accountStatus.lastLogin }}</div>
              </div>
              
              <div class="status-item">
                <div class="status-label">Member Since</div>
                <div class="status-value">{{ accountStatus.memberSince }}</div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Danger Zone -->
          <q-card class="settings-card q-mt-lg danger-zone">
            <q-card-section>
              <h6 class="text-h6 q-mb-md text-negative">Danger Zone</h6>
              
              <div class="q-gutter-md">
                <q-btn
                  color="negative"
                  label="Deactivate Account"
                  icon="block"
                  class="full-width"
                  outline
                  @click="showDeactivateDialog = true"
                />
                
                <q-btn
                  color="negative"
                  label="Delete Account"
                  icon="delete_forever"
                  class="full-width"
                  outline
                  @click="showDeleteDialog = true"
                />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>

    <!-- Deactivate Account Dialog -->
    <q-dialog v-model="showDeactivateDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Deactivate Account</div>
        </q-card-section>

        <q-card-section>
          <p>Are you sure you want to deactivate your account? You can reactivate it later by contacting support.</p>
          <q-input
            v-model="deactivateReason"
            label="Reason for deactivation (optional)"
            type="textarea"
            outlined
            rows="3"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" @click="showDeactivateDialog = false" />
          <q-btn
            label="Deactivate"
            color="negative"
            @click="deactivateAccount"
            :loading="deactivating"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Delete Account Dialog -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6 text-negative">Delete Account</div>
        </q-card-section>

        <q-card-section>
          <p class="text-negative">
            <strong>Warning:</strong> This action cannot be undone. All your data will be permanently deleted.
          </p>
          <q-input
            v-model="deleteConfirmation"
            label="Type 'DELETE' to confirm"
            outlined
            placeholder="DELETE"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" @click="showDeleteDialog = false" />
          <q-btn
            label="Delete Account"
            color="negative"
            @click="deleteAccount"
            :loading="deleting"
            :disable="deleteConfirmation !== 'DELETE'"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from '../boot/axios'

const router = useRouter()
const $q = useQuasar()

// File input reference
const fileInput = ref<HTMLInputElement>()

// Dialog states
const showDeactivateDialog = ref(false)
const showDeleteDialog = ref(false)

// Loading states
const saving = ref(false)
const deactivating = ref(false)
const deleting = ref(false)

// Form data
const profileForm = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  department: '',
  licenseNumber: '',
  bio: ''
})

const securityForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
  twoFactorAuth: false
})

const notificationSettings = ref({
  patientAlerts: true,
  medicationReminders: true,
  assessmentUpdates: true,
  inventoryAlerts: true,
  systemUpdates: false
})

// Account status
const accountStatus = ref({
  verified: true,
  lastLogin: '2024-01-15 10:30 AM',
  memberSince: '2023-06-15'
})

// Dialog form data
const deactivateReason = ref('')
const deleteConfirmation = ref('')

// Options
const departmentOptions = [
  { label: 'Emergency Department', value: 'emergency' },
  { label: 'Intensive Care Unit', value: 'icu' },
  { label: 'General Ward', value: 'general' },
  { label: 'Pediatrics', value: 'pediatrics' },
  { label: 'Maternity', value: 'maternity' },
  { label: 'Surgery', value: 'surgery' },
  { label: 'Outpatient', value: 'outpatient' },
  { label: 'Other', value: 'other' }
]

// Computed properties
const userInitials = computed(() => {
  const firstName = profileForm.value.firstName || ''
  const lastName = profileForm.value.lastName || ''
  return (firstName.charAt(0) + lastName.charAt(0)).toUpperCase()
})

const profilePictureUrl = computed(() => {
  // Mock profile picture URL - replace with actual implementation
  return null
})

// Methods
const goBack = () => {
  void router.push('/nurse-dashboard')
}

const triggerFileUpload = () => {
  fileInput.value?.click()
}

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
      
            await api.post('/users/profile/update/picture/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        } 
      })
      
      $q.notify({
        type: 'positive',
        message: 'Profile picture updated successfully!',
        position: 'top',
        timeout: 3000
      })
      
      // Clear the file input
      target.value = ''
    } catch (error) {
      console.error('Profile picture upload failed:', error)
      $q.notify({
        type: 'negative',
        message: 'Failed to upload profile picture. Please try again.',
        position: 'top',
        timeout: 4000
      })
    }
  }
}

const saveSettings = async () => {
  saving.value = true

  try {
    // Mock API call - replace with actual API
    await new Promise(resolve => setTimeout(resolve, 2000))

    $q.notify({
      type: 'positive',
      message: 'Settings saved successfully!',
      position: 'top'
    })

    // Reset password fields
    securityForm.value.currentPassword = ''
    securityForm.value.newPassword = ''
    securityForm.value.confirmPassword = ''

  } catch (error) {
    console.error('Error saving settings:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to save settings. Please try again.',
      position: 'top'
    })
  } finally {
    saving.value = false
  }
}

const exportData = () => {
  $q.notify({
    type: 'info',
    message: 'Data export feature coming soon!',
    position: 'top'
  })
}

const backupSettings = () => {
  $q.notify({
    type: 'info',
    message: 'Settings backup feature coming soon!',
    position: 'top'
  })
}

const deactivateAccount = async () => {
  deactivating.value = true

  try {
    // Mock API call
    await new Promise(resolve => setTimeout(resolve, 2000))

    $q.notify({
      type: 'positive',
      message: 'Account deactivated successfully',
      position: 'top'
    })

    showDeactivateDialog.value = false
    deactivateReason.value = ''

    // Redirect to login
    setTimeout(() => {
      void router.push('/login')
    }, 2000)

  } catch (error) {
    console.error('Error deactivating account:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to deactivate account. Please try again.',
      position: 'top'
    })
  } finally {
    deactivating.value = false
  }
}

const deleteAccount = async () => {
  deleting.value = true

  try {
    // Mock API call
    await new Promise(resolve => setTimeout(resolve, 2000))

    $q.notify({
      type: 'positive',
      message: 'Account deleted successfully',
      position: 'top'
    })

    showDeleteDialog.value = false
    deleteConfirmation.value = ''

    // Redirect to login
    setTimeout(() => {
      void router.push('/login')
    }, 2000)

  } catch (error) {
    console.error('Error deleting account:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to delete account. Please try again.',
      position: 'top'
    })
  } finally {
    deleting.value = false
  }
}

// Load user profile data
const loadUserProfile = async () => {
  try {
    const response = await api.get('/users/profile/')
    const userData = response.data.user
    
    profileForm.value = {
      firstName: userData.first_name || '',
      lastName: userData.last_name || '',
      email: userData.email || '',
      phone: userData.phone || '',
      department: userData.nurse_profile?.department || '',
      licenseNumber: userData.nurse_profile?.license_number || '',
      bio: userData.bio || ''
    }
    
  } catch (error) {
    console.error('Failed to load user profile:', error)
    
    // Fallback to localStorage
    const userData = localStorage.getItem('user')
    if (userData) {
      const user = JSON.parse(userData)
      profileForm.value = {
        firstName: user.first_name || '',
        lastName: user.last_name || '',
        email: user.email || '',
        phone: user.phone || '',
        department: user.nurse_profile?.department || '',
        licenseNumber: user.nurse_profile?.license_number || '',
        bio: user.bio || ''
      }
    }
  }
}

onMounted(() => {
  void loadUserProfile()
})
</script>

<style scoped>
.nurse-settings {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.page-header {
  background: linear-gradient(135deg, #286660 0%, #1e7668 100%);
  color: white;
  padding: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-btn {
  color: white;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.page-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.settings-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.profile-picture-container {
  position: relative;
  display: inline-block;
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
  font-size: 36px;
  font-weight: bold;
  border-radius: 50%;
}

.upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #1e7668 !important;
}

.profile-form {
  width: 100%;
}

.notification-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.notification-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  background: #f8f9fa;
}

.notification-info {
  flex: 1;
  margin-right: 20px;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.notification-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #e0e0e0;
}

.status-item:last-child {
  border-bottom: none;
}

.status-label {
  font-weight: 500;
  color: #666;
}

.status-value {
  font-weight: 600;
  color: #333;
}

.danger-zone {
  border: 2px solid #f44336;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .page-content {
    padding: 10px;
  }
  
  .profile-section {
    align-items: stretch;
  }
  
  .notification-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .notification-info {
    margin-right: 0;
  }
}
</style>
