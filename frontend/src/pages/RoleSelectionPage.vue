<template>
  <div class="role-selection-page">
    <div class="role-selection-container">
      <div class="role-selection-card">
        <div class="role-header">
          <h2>Join MediSync</h2>
          <p>Select your role to get started</p>
        </div>

        <div class="role-options">
          <div class="role-card" :class="{ 'selected': selectedRole === 'doctor' }" @click="selectRole('doctor')">
            <div class="role-icon">👨‍⚕️</div>
            <h3>Doctor</h3>
            <p>Provide medical care and consultations to patients</p>
          </div>

          <div class="role-card" :class="{ 'selected': selectedRole === 'nurse' }" @click="selectRole('nurse')">
            <div class="role-icon">👩‍⚕️</div>
            <h3>Nurse</h3>
            <p>Assist in patient care and medical procedures</p>
          </div>

          <div class="role-card" :class="{ 'selected': selectedRole === 'patient' }" @click="selectRole('patient')">
            <div class="role-icon">👤</div>
            <h3>Patient</h3>
            <p>Access your medical records and appointments</p>
          </div>
        </div>

        <div class="role-actions">
          <button 
            class="continue-btn" 
            :disabled="!selectedRole"
            @click="continueToRegistration"
          >
            Continue
          </button>
          <button class="back-btn" @click="$router.push('/login')">
            Back to Login
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedRole = ref('')

const selectRole = (role: string) => {
  selectedRole.value = role
}

const continueToRegistration = () => {
  if (selectedRole.value) {
    void router.push(`/register/${selectedRole.value}`)
  }
}
</script>

<style scoped>
.role-selection-page {
  min-height: 100vh;
  background: #286660;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.role-selection-container {
  width: 100%;
  max-width: 800px;
}

.role-selection-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.role-header {
  text-align: center;
  margin-bottom: 40px;
}

.role-header h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 32px;
  font-weight: 600;
}

.role-header p {
  margin: 0;
  color: #666;
  font-size: 18px;
}

.role-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.role-card {
  background: #f8f9fa;
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.role-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.role-card.selected {
  border-color: #1e7668;
  background: rgba(30, 118, 104, 0.05);
}

.role-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.role-card h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.role-card p {
  margin: 0;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.role-actions {
  text-align: center;
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.continue-btn {
  padding: 12px 30px;
  background: #1e7668;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.continue-btn:hover:not(:disabled) {
  background: #6ca299;
}

.continue-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.back-btn {
  padding: 12px 30px;
  background: transparent;
  color: #1e7668;
  border: 1px solid #1e7668;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.back-btn:hover {
  background: #1e7668;
  color: white;
}

@media (max-width: 768px) {
  .role-selection-card {
    padding: 20px;
  }
  
  .role-options {
    grid-template-columns: 1fr;
  }
  
  .role-actions {
    flex-direction: column;
  }
  
  .continue-btn,
  .back-btn {
    width: 100%;
  }
}
</style>
