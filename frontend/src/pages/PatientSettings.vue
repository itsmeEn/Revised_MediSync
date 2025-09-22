<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header class="settings-header">
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
        <div class="header-title">Account Settings</div>
        <div class="header-spacer"></div>
      </div>
    </q-header>

    <!-- Main content area -->
    <q-page-container class="page-background">
      <div class="q-pa-md">
        <!-- Profile Section -->
        <div class="settings-section">
          <div class="section-title">Profile Information</div>
          
          <q-card class="settings-card">
            <q-card-section>
              <!-- Profile Picture -->
              <div class="profile-picture-section">
                <div class="profile-picture-container">
                  <q-avatar size="100px" class="profile-avatar">
                    <img v-if="profileImageUrl" :src="profileImageUrl" alt="Profile" />
                    <q-icon v-else name="person" size="50px" color="grey-5" />
                  </q-avatar>
                  <q-btn
                    round
                    color="primary"
                    icon="camera_alt"
                    class="camera-btn"
                    @click="triggerFileUpload"
                  />
                </div>
                <input
                  ref="fileInput"
                  type="file"
                  accept="image/*"
                  style="display: none"
                  @change="handleProfilePictureUpload"
                />
                <div class="profile-info">
                  <div class="profile-name">{{ user?.full_name || 'Patient' }}</div>
                  <div class="profile-email">{{ user?.email || 'patient@example.com' }}</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Personal Information Section -->
        <div class="settings-section">
          <div class="section-title">Personal Information</div>
          
          <q-card class="settings-card">
            <q-card-section>
              <div class="form-field">
                <label class="field-label">Full Name</label>
                <q-input
                  v-model="profileForm.fullName"
                  label="Full Name"
                  outlined
                  rounded
                  class="form-input"
                  readonly
                />
              </div>

              <div class="form-field">
                <label class="field-label">Email Address</label>
                <q-input
                  v-model="profileForm.email"
                  label="Email Address"
                  outlined
                  rounded
                  class="form-input"
                  type="email"
                  readonly
                />
              </div>

              <div class="form-field">
                <label class="field-label">Date of Birth</label>
                <q-input
                  v-model="profileForm.dateOfBirth"
                  label="Date of Birth"
                  outlined
                  rounded
                  class="form-input"
                  type="date"
                  readonly
                />
              </div>

              <div class="form-field">
                <label class="field-label">Phone Number</label>
                <q-input
                  v-model="profileForm.phoneNumber"
                  label="Phone Number"
                  outlined
                  rounded
                  class="form-input"
                />
              </div>

              <div class="form-actions">
                <q-btn
                  class="save-btn"
                  color="primary"
                  rounded
                  unelevated
                  label="Save Changes"
                  @click="saveProfile"
                  :loading="isSaving"
                />
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Security Section -->
        <div class="settings-section">
          <div class="section-title">Security</div>
          
          <q-card class="settings-card">
            <q-card-section>
              <div class="security-item">
                <div class="security-info">
                  <div class="security-title">Change Password</div>
                  <div class="security-description">Update your account password</div>
                </div>
                <q-btn
                  color="primary"
                  outline
                  rounded
                  label="Change"
                  @click="showChangePasswordDialog"
                />
              </div>

              <div class="security-item">
                <div class="security-info">
                  <div class="security-title">Two-Factor Authentication</div>
                  <div class="security-description">Add an extra layer of security</div>
                </div>
                <q-btn
                  color="primary"
                  outline
                  rounded
                  label="Enable"
                  @click="showTwoFactorDialog"
                />
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Preferences Section -->
        <div class="settings-section">
          <div class="section-title">Preferences</div>
          
          <q-card class="settings-card">
            <q-card-section>
              <div class="preference-item">
                <div class="preference-info">
                  <div class="preference-title">Email Notifications</div>
                  <div class="preference-description">Receive notifications via email</div>
                </div>
                <q-toggle
                  v-model="preferences.emailNotifications"
                  color="primary"
                />
              </div>


              <div class="preference-item">
                <div class="preference-info">
                  <div class="preference-title">Appointment Reminders</div>
                  <div class="preference-description">Get reminded about upcoming appointments</div>
                </div>
                <q-toggle
                  v-model="preferences.appointmentReminders"
                  color="primary"
                />
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Account Actions Section -->
        <div class="settings-section">
          <div class="section-title">Account Actions</div>
          
          <q-card class="settings-card">
            <q-card-section>
              <div class="action-item">
                <div class="action-info">
                  <div class="action-title">Logout</div>
                  <div class="action-description">Sign out of your account</div>
                </div>
                <q-btn
                  color="negative"
                  outline
                  rounded
                  label="Logout"
                  @click="logout"
                />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-page-container>

    <!-- Change Password Dialog -->
    <q-dialog v-model="changePasswordDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Change Password</div>
        </q-card-section>

        <q-card-section>
          <div class="form-field">
            <label class="field-label">Current Password</label>
            <q-input
              v-model="passwordForm.currentPassword"
              label="Current Password"
              outlined
              rounded
              class="form-input"
              type="password"
            />
          </div>

          <div class="form-field">
            <label class="field-label">New Password</label>
            <q-input
              v-model="passwordForm.newPassword"
              label="New Password"
              outlined
              rounded
              class="form-input"
              type="password"
            />
          </div>

          <div class="form-field">
            <label class="field-label">Confirm New Password</label>
            <q-input
              v-model="passwordForm.confirmPassword"
              label="Confirm New Password"
              outlined
              rounded
              class="form-input"
              type="password"
            />
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn label="Change Password" color="primary" @click="changePassword" />
        </q-card-actions>
      </q-card>
    </q-dialog>

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

interface ProfileForm {
  fullName: string;
  email: string;
  dateOfBirth: string;
  phoneNumber: string;
}

interface PasswordForm {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

interface Preferences {
  emailNotifications: boolean;
  smsNotifications: boolean;
  appointmentReminders: boolean;
}

const router = useRouter();
const $q = useQuasar();

const user = ref<User | null>(null);
const activeTab = ref(4); // Settings tab is active
const isSaving = ref(false);
const changePasswordDialog = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

// Navigation items
const navItems = [
  { name: "home", icon: "home", label: "dashboard", route: "/patient-dashboard" },
  { name: "appointments", icon: "event_note", label: "appointment", route: "/patient-appointment" },
  { name: "medical-request", icon: "medical_services", label: "medical request", route: "/patient-medical-request" },
  { name: "notifications", icon: "notifications_none", label: "notification", route: "/patient-notifications" },
  { name: "settings", icon: "settings", label: "account settings", route: "/patient-settings" },
] as const;

// Form data
const profileForm = ref<ProfileForm>({
  fullName: '',
  email: '',
  dateOfBirth: '',
  phoneNumber: ''
});

const passwordForm = ref<PasswordForm>({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const preferences = ref<Preferences>({
  emailNotifications: true,
  smsNotifications: false,
  appointmentReminders: true
});

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

// Methods
const goBack = () => {
  void router.push('/patient-dashboard');
};

const triggerFileUpload = () => {
  fileInput.value?.click();
};

const handleProfilePictureUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  
  if (!file) return;

  // Validate file type
  if (!file.type.startsWith('image/')) {
    $q.notify({
      type: 'negative',
      message: 'Please select an image file',
      position: 'top'
    });
    return;
  }

  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    $q.notify({
      type: 'negative',
      message: 'Image size must be less than 5MB',
      position: 'top'
    });
    return;
  }

  try {
    const formData = new FormData();
    formData.append('profile_picture', file);

    const response = await api.post('/users/profile-picture/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (user.value) {
      user.value.profile_picture = response.data.profile_picture;
      localStorage.setItem("user", JSON.stringify(user.value));
    }

    $q.notify({
      type: 'positive',
      message: 'Profile picture updated successfully!',
      position: 'top'
    });
  } catch (error) {
    console.error('Error uploading profile picture:', error);
    $q.notify({
      type: 'negative',
      message: 'Failed to update profile picture',
      position: 'top'
    });
  }
};

const saveProfile = async () => {
  isSaving.value = true;
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    $q.notify({
      type: 'positive',
      message: 'Profile updated successfully!',
      position: 'top'
    });
  } catch (error) {
    console.error('Error saving profile:', error);
    $q.notify({
      type: 'negative',
      message: 'Failed to update profile',
      position: 'top'
    });
  } finally {
    isSaving.value = false;
  }
};

const showChangePasswordDialog = () => {
  changePasswordDialog.value = true;
};

const changePassword = () => {
  if (!passwordForm.value.currentPassword || !passwordForm.value.newPassword || !passwordForm.value.confirmPassword) {
    $q.notify({
      type: 'negative',
      message: 'Please fill in all password fields',
      position: 'top'
    });
    return;
  }

  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    $q.notify({
      type: 'negative',
      message: 'New passwords do not match',
      position: 'top'
    });
    return;
  }

  // Simulate password change
  $q.notify({
    type: 'positive',
    message: 'Password changed successfully!',
    position: 'top'
  });

  // Reset form and close dialog
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  };
  changePasswordDialog.value = false;
};

const showTwoFactorDialog = () => {
  $q.notify({
    type: 'info',
    message: 'Two-factor authentication setup coming soon!',
    position: 'top'
  });
};

const logout = () => {
  $q.dialog({
    title: 'Logout',
    message: 'Are you sure you want to logout?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    void router.push('/login');
    $q.notify({
      type: 'positive',
      message: 'Logged out successfully!',
      position: 'top'
    });
  });
};

const navigateToTab = (route: string | undefined) => {
  if (route && route !== '/patient-settings') {
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
    
    // Populate form with user data
    if (user.value) {
      profileForm.value = {
        fullName: user.value.full_name || '',
        email: user.value.email || '',
        dateOfBirth: user.value.date_of_birth || '',
        phoneNumber: '' // This would come from user profile if available
      };
    }
  } catch {
    const cached = localStorage.getItem("user");
    if (cached) {
      try {
        user.value = JSON.parse(cached);
        if (user.value) {
          profileForm.value = {
            fullName: user.value.full_name || '',
            email: user.value.email || '',
            dateOfBirth: user.value.date_of_birth || '',
            phoneNumber: ''
          };
        }
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

.settings-header {
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

.back-btn {
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

.header-spacer {
  width: 24px;
}

.settings-section {
  margin-bottom: 30px;
}

.section-title {
  color: #286660;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.settings-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.profile-picture-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.profile-picture-container {
  position: relative;
}

.profile-avatar {
  border: 3px solid #286660;
}

.camera-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 32px;
  height: 32px;
  min-height: 32px;
}

.profile-info {
  flex: 1;
}

.profile-name {
  color: #286660;
  font-weight: 600;
  font-size: 1.2rem;
  margin-bottom: 4px;
}

.profile-email {
  color: #666;
  font-size: 0.9rem;
}

.form-field {
  margin-bottom: 20px;
}

.field-label {
  display: block;
  color: #286660;
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
}

.form-actions {
  margin-top: 20px;
}

.save-btn {
  width: 100%;
  min-height: 50px;
  font-size: 1rem;
  font-weight: 600;
}

.security-item, .preference-item, .action-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}

.security-item:last-child, .preference-item:last-child, .action-item:last-child {
  border-bottom: none;
}

.security-info, .preference-info, .action-info {
  flex: 1;
}

.security-title, .preference-title, .action-title {
  color: #286660;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 4px;
}

.security-description, .preference-description, .action-description {
  color: #666;
  font-size: 0.9rem;
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

  .profile-picture-section {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .security-item, .preference-item, .action-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
