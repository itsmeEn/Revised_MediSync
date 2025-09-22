<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header class="appointment-header">
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
        <div class="header-title">Appointments</div>
        <q-btn
          flat
          round
          dense
          icon="notifications"
          @click="showNotifications"
          class="notification-btn"
          aria-label="Notifications"
        />
      </div>
    </q-header>

    <!-- Main content area -->
    <q-page-container class="page-background">
      <div class="q-pa-md">
        <!-- Appointment Status Tabs -->
        <div class="appointment-tabs-container">
          <q-btn-toggle
            v-model="selectedTab"
            :options="tabOptions"
            class="appointment-tabs"
            toggle-color="primary"
            color="white"
            text-color="primary"
            rounded
            unelevated
          />
        </div>

        <!-- Appointment Cards Section -->
        <div class="appointments-section">
          <div class="section-title">{{ getSectionTitle() }}</div>
          
          <!-- Upcoming Appointments -->
          <div v-if="selectedTab === 'upcoming'" class="appointment-cards">
            <div 
              v-for="appointment in upcomingAppointments" 
              :key="appointment.id"
              class="appointment-card"
            >
              <div class="card-left-border"></div>
              <div class="card-content">
                <div class="appointment-date">{{ formatDate(appointment.date) }}</div>
                <div class="appointment-time">{{ appointment.time }}</div>
                <div class="appointment-details">{{ appointment.details }}</div>
                <div v-if="appointment.queueNumber" class="queue-number">
                  Queue Number: #{{ appointment.queueNumber }}
                </div>
                <div class="appointment-type-badge onsite">
                  Onsite
                </div>
                <div class="appointment-actions">
                  <q-btn 
                    class="cancel-btn"
                    color="negative"
                    outline
                    rounded
                    label="Cancel"
                    @click="cancelAppointment(appointment.id)"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Completed Appointments -->
          <div v-if="selectedTab === 'completed'" class="appointment-cards">
            <div 
              v-for="appointment in completedAppointments" 
              :key="appointment.id"
              class="appointment-card completed"
            >
              <div class="card-left-border completed"></div>
              <div class="card-content">
                <div class="appointment-date">{{ formatDate(appointment.date) }}</div>
                <div class="appointment-time">{{ appointment.time }}</div>
                <div class="appointment-details">{{ appointment.details }}</div>
                <div class="appointment-type-badge completed">
                  Completed
                </div>
              </div>
            </div>
          </div>

          <!-- Cancelled Appointments -->
          <div v-if="selectedTab === 'cancelled'" class="appointment-cards">
            <div 
              v-for="appointment in cancelledAppointments" 
              :key="appointment.id"
              class="appointment-card cancelled"
            >
              <div class="card-left-border cancelled"></div>
              <div class="card-content">
                <div class="appointment-date">{{ formatDate(appointment.date) }}</div>
                <div class="appointment-time">{{ appointment.time }}</div>
                <div class="appointment-details">{{ appointment.details }}</div>
                <div class="appointment-type-badge cancelled">
                  Cancelled
                </div>
                <div class="appointment-actions">
                  <q-btn 
                    class="reschedule-btn"
                    color="primary"
                    outline
                    rounded
                    label="Reschedule"
                    @click="openRescheduleDialog(appointment)"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Schedule New Appointment Section -->
        <div class="schedule-section">
          <div class="section-title">Schedule New Appointment</div>
          
          <q-card class="schedule-card">
            <q-card-section>
              <!-- Appointment Type -->
              <div class="form-field">
                <label class="field-label">Appointment Type</label>
                <q-select
                  v-model="newAppointment.type"
                  :options="appointmentTypes"
                  label="Select Appointment Type"
                  outlined
                  rounded
                  class="form-select"
                />
              </div>

              <!-- Department -->
              <div class="form-field">
                <label class="field-label">Department</label>
                <q-select
                  v-model="newAppointment.department"
                  :options="departments"
                  label="Select Department"
                  outlined
                  rounded
                  class="form-select"
                />
              </div>

              <!-- Date -->
              <div class="form-field">
                <label class="field-label">Date</label>
                <q-input
                  v-model="newAppointment.date"
                  type="date"
                  outlined
                  rounded
                  class="form-input"
                />
              </div>

              <!-- Time Selection -->
              <div class="form-field">
                <label class="field-label">Appointment Time</label>
                <q-select
                  v-model="newAppointment.time"
                  :options="availableTimeSlots"
                  label="Select Time"
                  outlined
                  rounded
                  class="form-select"
                  :disable="!newAppointment.date"
                  hint="Please select a date first"
                />
              </div>

              <!-- Reason for Appointment -->
              <div class="form-field">
                <label class="field-label">Reason for Appointment</label>
                <q-input
                  v-model="newAppointment.reason"
                  type="textarea"
                  placeholder="Describe the reason for appointment.."
                  outlined
                  rounded
                  rows="3"
                  class="form-textarea"
                /> 
              </div>

              <!-- Schedule Button -->
              <q-btn
                class="schedule-btn"
                color="primary"
                rounded
                unelevated
                label="Schedule Appointment"
                @click="scheduleAppointment"
                :loading="isScheduling"
              />
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-page-container>

    <!-- Reschedule Dialog -->
    <q-dialog v-model="rescheduleDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Reschedule Appointment</div>
        </q-card-section>

        <q-card-section>
          <div class="form-field">
            <label class="field-label">New Date</label>
            <q-input
              v-model="rescheduleData.date"
              type="date"
              outlined
              rounded
              class="form-input"
            />
          </div>

          <div class="form-field">
            <label class="field-label">New Time</label>
            <q-select
              v-model="rescheduleData.time"
              :options="availableTimeSlots"
              label="Select Time"
              outlined
              rounded
              class="form-select"
            />
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn label="Reschedule" color="primary" @click="confirmReschedule" />
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

interface Appointment {
  id: number;
  date: string;
  time: string;
  details: string;
  type: string;
  queueNumber?: string;
  status: 'upcoming' | 'completed' | 'cancelled';
}


interface NewAppointment {
  type: string;
  department: string;
  date: string;
  time: string;
  reason: string;
}

const router = useRouter();
const $q = useQuasar();

const user = ref<User | null>(null);
const activeTab = ref(1); // Appointment tab is active
const selectedTab = ref('upcoming');
const isScheduling = ref(false);

// Tab options for appointment status
const tabOptions = [
  { label: 'Upcoming', value: 'upcoming' },
  { label: 'Completed', value: 'completed' },
  { label: 'Cancelled', value: 'cancelled' }
];

// Navigation items
const navItems = [
  { name: "home", icon: "home", label: "dashboard", route: "/patient-dashboard" },
  { name: "appointments", icon: "event_note", label: "appointment", route: "/patient-appointment" },
  { name: "medical-request", icon: "medical_services", label: "medical request", route: "/patient-medical-request" },
  { name: "notifications", icon: "notifications_none", label: "notification", route: "/patient-notifications" },
  { name: "settings", icon: "settings", label: "account settings", route: "/patient-settings" },
] as const;

// Appointment types
const appointmentTypes = [
  'Routine Appointment',
  'Follow-Up Appointments',
  'Specialist Consultations',
  'Procedure/Diagnostic Appointments'
];

// Departments
const departments = [
  'Clinical (Cardiology, Oncology, Pediatrics)',
  'Support (Pharmacy, Radiology, Nursing)',
  'Administrative (Human Resources, Finance, Medical Records)'
];

// Generate 24-hour time slots with 1-hour intervals
const generateTimeSlots = () => {
  const slots = [];
  for (let hour = 0; hour < 24; hour++) {
    const timeString = hour === 0 ? '12:00 AM' : 
                      hour < 12 ? `${hour}:00 AM` : 
                      hour === 12 ? '12:00 PM' : 
                      `${hour - 12}:00 PM`;
    slots.push(timeString);
  }
  return slots;
};

const availableTimeSlots = generateTimeSlots();

// New appointment form
const newAppointment = ref<NewAppointment>({
  type: '',
  department: '',
  date: '',
  time: '',
  reason: ''
});

// Appointment data - will be loaded from localStorage
const upcomingAppointments = ref<Appointment[]>([]);
const completedAppointments = ref<Appointment[]>([]);
const cancelledAppointments = ref<Appointment[]>([]);

// Computed properties
const getSectionTitle = () => {
  switch (selectedTab.value) {
    case 'upcoming': return 'Upcoming Appointments';
    case 'completed': return 'Completed Appointments';
    case 'cancelled': return 'Cancelled Appointments';
    default: return 'Appointments';
  }
};

// Methods
const goBack = () => {
  void router.push('/patient-dashboard');
};

const showNotifications = () => {
  $q.notify({
    type: 'info',
    message: 'Notifications feature coming soon!',
    position: 'top'
  });
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




const scheduleAppointment = () => {
  // Validate form
  if (!newAppointment.value.type || !newAppointment.value.department || 
      !newAppointment.value.date || !newAppointment.value.time || 
      !newAppointment.value.reason) {
    $q.notify({
      type: 'negative',
      message: 'Please fill in all required fields',
      position: 'top'
    });
    return;
  }

  isScheduling.value = true;

  try {
    // Get the next queue number
    const queueNumber = getNextQueueNumber(newAppointment.value.date, newAppointment.value.time);
    
    // Create new appointment object
    const newAppointmentObj: Appointment = {
      id: Date.now(),
      date: newAppointment.value.date,
      time: newAppointment.value.time,
      details: `${newAppointment.value.reason} - ${newAppointment.value.department}`,
      type: 'Onsite',
      queueNumber: String(queueNumber),
      status: 'upcoming'
    };

    // Get existing appointments and add new one
    const existingAppointments = JSON.parse(localStorage.getItem('patient_appointments') || '[]') as Appointment[];
    existingAppointments.push(newAppointmentObj);
    localStorage.setItem('patient_appointments', JSON.stringify(existingAppointments));
    
    // Reload appointments to update UI
    loadAppointments();

    // Reset form
    newAppointment.value = {
      type: '',
      department: '',
      date: '',
      time: '',
      reason: ''
    };

    $q.notify({
      type: 'positive',
      message: 'Appointment scheduled successfully!',
      position: 'top'
    });

    // Switch to upcoming tab to show the new appointment
    selectedTab.value = 'upcoming';

  } catch (error) {
    console.error('Error scheduling appointment:', error);
    $q.notify({
      type: 'negative',
      message: 'Failed to schedule appointment. Please try again.',
      position: 'top'
    });
  } finally {
    isScheduling.value = false;
  }
};

// Simple queue management - just count all appointments for same date/time
const getNextQueueNumber = (date: string, time: string) => {
  const appointments = JSON.parse(localStorage.getItem('patient_appointments') || '[]') as Appointment[];
  const sameDateTimeCount = appointments.filter((apt: Appointment) => 
    apt.date === date && apt.time === time
  ).length;
  return sameDateTimeCount + 1;
};


// Enhanced cancel appointment with better error handling
const cancelAppointment = (appointmentId: number) => {
  $q.dialog({
    title: 'Cancel Appointment',
    message: 'Are you sure you want to cancel this appointment? This action cannot be undone.',
    persistent: true,
    ok: {
      label: 'Yes, Cancel',
      color: 'negative'
    },
    cancel: {
      label: 'Keep Appointment',
      color: 'primary'
    }
  }).onOk(() => {
    try {
      // Get all appointments from localStorage
      const appointments = JSON.parse(localStorage.getItem('patient_appointments') || '[]') as Appointment[];
      
      // Find and update the appointment
      const appointmentIndex = appointments.findIndex((apt: Appointment) => apt.id === appointmentId);
      if (appointmentIndex !== -1 && appointments[appointmentIndex]) {
        appointments[appointmentIndex].status = 'cancelled';
        
        // Save back to localStorage
        localStorage.setItem('patient_appointments', JSON.stringify(appointments));
        
        // Reload appointments to update UI
        loadAppointments();
        
        $q.notify({
          type: 'positive',
          message: 'Appointment cancelled successfully!',
          position: 'top',
          timeout: 3000
        });
      } else {
        $q.notify({
          type: 'negative',
          message: 'Appointment not found.',
          position: 'top'
        });
      }
    } catch (error) {
      console.error('Error cancelling appointment:', error);
      $q.notify({
        type: 'negative',
        message: 'Failed to cancel appointment. Please try again.',
        position: 'top'
      });
    }
  });
};

// Reschedule appointment
const rescheduleAppointment = ref<Appointment | null>(null);
const rescheduleDialog = ref(false);
const rescheduleData = ref({
  date: '',
  time: ''
});

const openRescheduleDialog = (appointment: Appointment) => {
  rescheduleAppointment.value = appointment;
  rescheduleData.value = {
    date: appointment.date,
    time: appointment.time
  };
  rescheduleDialog.value = true;
};

const confirmReschedule = () => {
  if (!rescheduleAppointment.value) return;
  
  try {
    // Find the appointment in cancelled list
    const cancelledIndex = cancelledAppointments.value.findIndex(apt => apt.id === rescheduleAppointment.value!.id);
    if (cancelledIndex !== -1) {
      const appointment = cancelledAppointments.value[cancelledIndex];
      if (appointment) {
        // Update appointment details
        appointment.date = rescheduleData.value.date;
        appointment.time = rescheduleData.value.time;
        appointment.status = 'upcoming';
        
        // Move from cancelled to upcoming
        cancelledAppointments.value.splice(cancelledIndex, 1);
        upcomingAppointments.value.push(appointment);
        
        // Update localStorage
        const allAppointments = [...upcomingAppointments.value, ...completedAppointments.value, ...cancelledAppointments.value];
        localStorage.setItem('patient_appointments', JSON.stringify(allAppointments));
      }
    }
    
    rescheduleDialog.value = false;
    $q.notify({
      type: 'positive',
      message: 'Appointment rescheduled successfully!',
      position: 'top'
    });
  } catch (error) {
    console.error('Error rescheduling appointment:', error);
    $q.notify({
      type: 'negative',
      message: 'Failed to reschedule appointment. Please try again.',
      position: 'top'
    });
  }
};

// Simple load appointments from localStorage
const loadAppointments = () => {
  try {
    const appointments = JSON.parse(localStorage.getItem('patient_appointments') || '[]') as Appointment[];
    
    upcomingAppointments.value = appointments.filter((apt: Appointment) => apt.status === 'upcoming');
    completedAppointments.value = appointments.filter((apt: Appointment) => apt.status === 'completed');
    cancelledAppointments.value = appointments.filter((apt: Appointment) => apt.status === 'cancelled');
  } catch (error) {
    console.error('Error loading appointments:', error);
  }
};

const navigateToTab = (route: string | undefined) => {
  if (route && route !== '/patient-appointment') {
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
  // Load existing appointments from localStorage
  loadAppointments();
  // Set default date to today
  const today = new Date();
  const dateString = today.toISOString().split('T')[0];
  if (dateString) {
    newAppointment.value.date = dateString;
  }
});
</script>

<style scoped>
.page-background {
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 50%, #d4edda 100%);
  min-height: 100vh;
}

.appointment-header {
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

.back-btn, .notification-btn {
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

.appointment-tabs-container {
  margin: 20px 0;
  display: flex;
  justify-content: center;
}

.appointment-tabs {
  background: white;
  border-radius: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.appointments-section {
  margin-bottom: 30px;
}

.section-title {
  color: #286660;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.appointment-cards {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.appointment-card {
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
.appointment-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  background: #d4f0d4;
}

.appointment-card.completed {
  background: #f0f0f0;
  opacity: 0.8;
}

.appointment-card.cancelled {
  background: #ffeaea;
  opacity: 0.8;
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

.card-left-border.completed {
  background: #666;
}

.card-left-border.cancelled {
  background: #e74c3c;
}

.card-content {
  flex: 1;
  margin-left: 10px;
}

.appointment-date {
  color: #286660;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 5px;
}

.appointment-time {
  color: #286660;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.appointment-details {
  color: #286660;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.queue-number {
  color: #286660;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 10px;
}

.appointment-type-badge {
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

.appointment-type-badge.completed {
  background: #666;
}

.appointment-type-badge.cancelled {
  background: #e74c3c;
}

.appointment-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  flex-wrap: wrap;
}
.cancel-btn, .reschedule-btn {
  flex: 1;
  min-width: 120px;
}

.schedule-section {
  margin-bottom: 100px;
}

.schedule-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  margin-bottom: 20px;
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


.schedule-btn {
  width: 100%;
  min-height: 50px;
  font-size: 1rem;
  font-weight: 600;
  margin-top: 10px;
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


  .appointment-card {
    padding: 15px;
  }

  .appointment-type-badge {
    position: static;
    display: inline-block;
    margin-top: 10px;
  }
}
</style>
