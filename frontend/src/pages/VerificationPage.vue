<template>
  <div class="verification-page">
    <div class="verification-container">
      <div class="verification-card">
        <div class="text-center">
          <h4>Account Verification</h4>
          <p>Please upload a document to verify your identity</p>
        </div>

        <div class="upload-section">
          <div class="form-group">
            <label for="verification-document">Upload Verification Document</label>
            <input
              id="verification-document"
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              @change="handleFileChange"
              class="file-input"
            />
            <small>Accepted formats: PDF, JPG, PNG (Max 5MB)</small>
          </div>

          <div v-if="verificationDocument" class="uploaded-file">
            <div class="file-chip">
              <span>{{ verificationDocument.name }}</span>
              <button @click="verificationDocument = null" class="remove-btn">×</button>
            </div>
          </div>
        </div>

          <div class="verification-options">
            <p>
              Choose how you'd like to proceed with verification:
            </p>
            
            <div class="button-row">
              <div class="button-group">
                <button
                  class="btn btn-primary"
                  :disabled="!verificationDocument || verifying"
                  @click="verifyNow"
                >
                  {{ verifying ? 'Verifying...' : 'Verify Now' }}
                </button>
                <p class="button-caption">
                  Upload document and verify immediately
                </p>
              </div>
              
              <div class="button-group">
                <button
                  class="btn btn-secondary"
                  :disabled="verifying"
                  @click="verifyLater"
                >
                  {{ verifying ? 'Processing...' : 'Verify Later' }}
                </button>
                <p class="button-caption">
                  Skip verification for now
                </p>
              </div>
            </div>
          </div>

        <div class="text-center">
          <button
            class="btn btn-link"
            @click="$router.push('/role-selection')"
          >Back to Registration</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from '../boot/axios'

const router = useRouter()
const $q = useQuasar()

interface User {
  id: number
  email: string
  full_name: string
  role: string
  is_verified: boolean
}

const verificationDocument = ref<File | null>(null)
const verifying = ref(false)

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    verificationDocument.value = target.files[0]
  }
}

onMounted(() => {
  // Check if user is logged in
  const user = localStorage.getItem('user')
  if (!user) {
    void router.push('/login')
  }
})

const getCurrentUser = (): User | null => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
}

const redirectToDashboard = (role: string) => {
  switch (role) {
    case 'doctor':
      void router.push('/doctor-dashboard')
      break
    case 'nurse':
      void router.push('/nurse-dashboard')
      break
    case 'patient':
      void router.push('/patient-dashboard')
      break
    default:
      void router.push('/')
  }
}

const verifyNow = async () => {
      if (!verificationDocument.value) {
      $q.notify({
        type: 'negative',
        message: 'Please upload a verification document first',
        position: 'top',
        timeout: 3000
      })
      return
    }

  verifying.value = true
  
  try {
    const formData = new FormData()
    formData.append('verification_document', verificationDocument.value)

    // Upload verification document
    await api.post('/users/verification/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })

    // Mark as verified
    await api.post('/users/verification/verify-now/', {}, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })

          $q.notify({
        type: 'positive',
        message: 'Account verified successfully!',
        position: 'top',
        timeout: 3000
      })

    const user = getCurrentUser()
    if (user) {
      redirectToDashboard(user.role)
    }

  } catch (error: unknown) {
    console.error('Verification error:', error)
    const errorMessage = error instanceof Error ? error.message : 'Verification failed. Please try again.'
    $q.notify({
      type: 'negative',
      message: `Error: ${errorMessage}`,
      position: 'top',
      timeout: 4000
    })
  } finally {
    verifying.value = false
  }
}

const verifyLater = async () => {
  verifying.value = true
  
  try {
    if (verificationDocument.value) {
      const formData = new FormData()
      formData.append('verification_document', verificationDocument.value)

      await api.post('/users/verification/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
    }

    $q.notify({
      type: 'info',
      message: 'You can verify your account later from your dashboard.',
      position: 'top',
      timeout: 3000
    })

    const user = getCurrentUser()
    if (user) {
      redirectToDashboard(user.role)
    }

  } catch (error: unknown) {
    console.error('Verification error:', error)
    const errorMessage = error instanceof Error ? error.message : 'Failed to save document. Please try again.'
    $q.notify({
      type: 'negative',
      message: `Error: ${errorMessage}`,
      position: 'top',
      timeout: 4000
    })
  } finally {
    verifying.value = false
  }
}
</script>

<style scoped>
.verification-page {
  min-height: 100vh;
  background: #286660;
  justify-content: center;
  padding: 20px;
}

.verification-container {
  width: 100%;
  max-width: 600px;
}

.verification-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.text-center {
  text-align: center;
}

.text-center h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.text-center p {
  margin: 0 0 20px 0;
  color: #666;
  font-size: 16px;
}

.upload-section {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.file-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group small {
  color: #666;
  font-size: 14px;
}

.uploaded-file {
  display: flex;
  justify-content: center;
  margin-top: 15px;
}

.file-chip {
  background: #1e7668;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.remove-btn {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.verification-options {
  border-top: 1px solid #e0e0e0;
  padding-top: 20px;
  margin-bottom: 20px;
}

.verification-options p {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 16px;
}

.button-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.button-group {
  text-align: center;
}

.btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 8px;
}

.btn-primary {
  background: #1e7668;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #6ca299;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #5a6268;
}

.btn-secondary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-link {
  background: none;
  color: #1e7668;
  text-decoration: underline;
  cursor: pointer;
}

.btn-link:hover {
  color: #6ca299;
}

.button-caption {
  margin: 0;
  color: #666;
  font-size: 14px;
}

@media (max-width: 768px) {
  .verification-card {
    padding: 20px;
  }
  
  .button-row {
    grid-template-columns: 1fr;
  }
}
</style>
