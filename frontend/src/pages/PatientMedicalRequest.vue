<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header class="medical-request-header">
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
        <div class="header-title">Medical Requests</div>
        <q-btn
          flat
          round
          dense
          icon="add"
          @click="showNewRequestDialog"
          class="add-btn"
          aria-label="New Request"
        />
      </div>
    </q-header>

    <!-- Main content area -->
    <q-page-container class="page-background">
      <div class="q-pa-md">
        <!-- Request Status Tabs -->
        <div class="request-tabs-container">
          <q-btn-toggle
            v-model="selectedTab"
            :options="tabOptions"
            class="request-tabs"
            toggle-color="primary"
            color="white"
            text-color="primary"
            rounded
            unelevated
          />
        </div>

        <!-- Request Cards Section -->
        <div class="requests-section">
          <div class="section-title">{{ getSectionTitle() }}</div>
          
          <!-- Pending Requests -->
          <div v-if="selectedTab === 'pending'" class="request-cards">
            <div 
              v-for="request in pendingRequests" 
              :key="request.id"
              class="request-card pending"
            >
              <div class="card-left-border pending"></div>
              <div class="card-content">
                <div class="request-title">{{ request.title }}</div>
                <div class="request-description">{{ request.description }}</div>
                <div class="request-date">{{ formatDate(request.date) }}</div>
                <div class="request-type-badge pending">
                  Pending
                </div>
                <div class="request-actions">
                  <q-btn 
                    class="cancel-btn"
                    color="negative"
                    outline
                    rounded
                    label="Cancel"
                    @click="cancelRequest(request.id)"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Approved Requests -->
          <div v-if="selectedTab === 'approved'" class="request-cards">
            <div 
              v-for="request in approvedRequests" 
              :key="request.id"
              class="request-card approved"
            >
              <div class="card-left-border approved"></div>
              <div class="card-content">
                <div class="request-title">{{ request.title }}</div>
                <div class="request-description">{{ request.description }}</div>
                <div class="request-date">{{ formatDate(request.date) }}</div>
                <div class="request-type-badge approved">
                  Approved
                </div>
              </div>
            </div>
          </div>

          <!-- Completed Requests -->
          <div v-if="selectedTab === 'completed'" class="request-cards">
            <div 
              v-for="request in completedRequests" 
              :key="request.id"
              class="request-card completed"
            >
              <div class="card-left-border completed"></div>
              <div class="card-content">
                <div class="request-title">{{ request.title }}</div>
                <div class="request-description">{{ request.description }}</div>
                <div class="request-date">{{ formatDate(request.date) }}</div>
                <div class="request-type-badge completed">
                  Completed
                </div>
                <div class="request-actions">
                  <q-btn 
                    class="medical-records-btn"
                    color="primary"
                    outline
                    rounded
                    label="Request Medical Records"
                    @click="requestMedicalRecords(request)"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </q-page-container>

    <!-- New Request Dialog -->
    <q-dialog v-model="newRequestDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">New Medical Request</div>
        </q-card-section>

        <q-card-section>
          <div class="form-field">
            <label class="field-label">Request Type</label>
            <q-select
              v-model="newRequest.type"
              :options="requestTypes"
              label="Select Request Type"
              outlined
              rounded
              class="form-select"
            />
          </div>

          <div class="form-field">
            <label class="field-label">Title</label>
            <q-input
              v-model="newRequest.title"
              label="Request Title"
              outlined
              rounded
              class="form-input"
            />
          </div>

          <div class="form-field">
            <label class="field-label">Description</label>
            <q-input
              v-model="newRequest.description"
              type="textarea"
              label="Describe your request..."
              outlined
              rounded
              rows="3"
              class="form-textarea"
            />
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn label="Submit Request" color="primary" @click="submitRequest" />
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
import { ref, onMounted } from "vue";
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

interface MedicalRequest {
  id: number;
  title: string;
  description: string;
  type: string;
  date: string;
  status: 'pending' | 'approved' | 'completed';
}

interface NewRequest {
  type: string;
  title: string;
  description: string;
}

const router = useRouter();
const $q = useQuasar();

const user = ref<User | null>(null);
const activeTab = ref(2); // Medical Request tab is active
const selectedTab = ref('pending');
const newRequestDialog = ref(false);

// Tab options for request status
const tabOptions = [
  { label: 'Pending', value: 'pending' },
  { label: 'Approved', value: 'approved' },
  { label: 'Completed', value: 'completed' }
];

// Navigation items
const navItems = [
  { name: "home", icon: "home", label: "dashboard", route: "/patient-dashboard" },
  { name: "appointments", icon: "event_note", label: "appointment", route: "/patient-appointment" },
  { name: "medical-request", icon: "medical_services", label: "medical request", route: "/patient-medical-request" },
  { name: "notifications", icon: "notifications_none", label: "notification", route: "/patient-notifications" },
  { name: "settings", icon: "settings", label: "account settings", route: "/patient-settings" },
] as const;

// Request types
const requestTypes = [
  'Prescription Refill',
  'Medical Records Request',
  'Lab Results Request',
  'Insurance Authorization',
  'Referral Request',
  'Other'
];

// New request form
const newRequest = ref<NewRequest>({
  type: '',
  title: '',
  description: ''
});

// Sample request data
const pendingRequests = ref<MedicalRequest[]>([
  {
    id: 1,
    title: 'Prescription Refill - Blood Pressure Medication',
    description: 'Need refill for my blood pressure medication. Running low on current supply.',
    type: 'Prescription Refill',
    date: '2025-01-20',
    status: 'pending'
  }
]);

const approvedRequests = ref<MedicalRequest[]>([
  {
    id: 2,
    title: 'Medical Records Request',
    description: 'Request for complete medical history for insurance purposes.',
    type: 'Medical Records Request',
    date: '2025-01-15',
    status: 'approved'
  }
]);

const completedRequests = ref<MedicalRequest[]>([
  {
    id: 3,
    title: 'Lab Results Request',
    description: 'Request for blood test results from last week.',
    type: 'Lab Results Request',
    date: '2025-01-10',
    status: 'completed'
  }
]);

// Computed properties
const getSectionTitle = () => {
  switch (selectedTab.value) {
    case 'pending': return 'Pending Requests';
    case 'approved': return 'Approved Requests';
    case 'completed': return 'Completed Requests';
    default: return 'Medical Requests';
  }
};

// Methods
const goBack = () => {
  void router.push('/patient-dashboard');
};

const showNewRequestDialog = () => {
  newRequestDialog.value = true;
};

const formatDate = (dateString: string) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
};

const submitRequest = () => {
  if (!newRequest.value.type || !newRequest.value.title || !newRequest.value.description) {
    $q.notify({
      type: 'negative',
      message: 'Please fill in all required fields',
      position: 'top'
    });
    return;
  }

  const newRequestObj: MedicalRequest = {
    id: Date.now(),
    title: newRequest.value.title,
    description: newRequest.value.description,
    type: newRequest.value.type,
    date: new Date().toISOString().split('T')[0] || '',
    status: 'pending'
  };

  pendingRequests.value.push(newRequestObj);

  // Reset form
  newRequest.value = {
    type: '',
    title: '',
    description: ''
  };

  newRequestDialog.value = false;

  $q.notify({
    type: 'positive',
    message: 'Medical request submitted successfully!',
    position: 'top'
  });
};

const cancelRequest = (requestId: number) => {
  $q.dialog({
    title: 'Cancel Request',
    message: 'Are you sure you want to cancel this medical request? This action cannot be undone.',
    persistent: true,
    ok: {
      label: 'Yes, Cancel',
      color: 'negative'
    },
    cancel: {
      label: 'Keep Request',
      color: 'primary'
    }
  }).onOk(() => {
    try {
      const index = pendingRequests.value.findIndex(req => req.id === requestId);
      if (index !== -1) {
        pendingRequests.value.splice(index, 1);
        $q.notify({
          type: 'positive',
          message: 'Medical request cancelled successfully!',
          position: 'top',
          timeout: 3000
        });
      } else {
        $q.notify({
          type: 'negative',
          message: 'Request not found.',
          position: 'top'
        });
      }
    } catch (error) {
      console.error('Error cancelling request:', error);
      $q.notify({
        type: 'negative',
        message: 'Failed to cancel request. Please try again.',
        position: 'top'
      });
    }
  });
};

const requestMedicalRecords = (request: MedicalRequest) => {
  $q.notify({
    type: 'positive',
    message: `Medical records request submitted for: ${request.title}`,
    position: 'top'
  });
};

const navigateToTab = (route: string | undefined) => {
  if (route && route !== '/patient-medical-request') {
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

.medical-request-header {
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

.back-btn, .add-btn {
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

.request-tabs-container {
  margin: 20px 0;
  display: flex;
  justify-content: center;
}

.request-tabs {
  background: white;
  border-radius: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.requests-section {
  margin-bottom: 30px;
}

.section-title {
  color: #286660;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.request-cards {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.request-card {
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

.request-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  background: #d4f0d4;
}

.request-card.approved {
  background: #e8f5e8;
}

.request-card.completed {
  background: #e8f5e8;
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

.card-left-border.approved {
  background: #4caf50;
}

.card-left-border.completed {
  background: #4caf50;
}

.card-content {
  flex: 1;
  margin-left: 10px;
}

.request-title {
  color: #286660;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 5px;
}

.request-description {
  color: #286660;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.request-date {
  color: #286660;
  font-size: 0.85rem;
  margin-bottom: 10px;
}

.request-type-badge {
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

.request-type-badge.approved {
  background: #4caf50;
}

.request-type-badge.completed {
  background: #4caf50;
}

.request-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  flex-wrap: wrap;
}

.cancel-btn, .medical-records-btn {
  flex: 1;
  min-width: 120px;
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

.form-select, .form-input, .form-textarea {
  width: 100%;
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

  .request-card {
    padding: 15px;
  }

  .request-type-badge {
    position: static;
    display: inline-block;
    margin-top: 10px;
  }
}
</style>
