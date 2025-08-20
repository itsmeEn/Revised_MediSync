<template>
  <q-page class="verification-page">
    <div class="verification-container">
      <q-card class="verification-card">
        <q-card-section class="text-center">
          <h4 class="text-h4 q-mb-md">Account Verification</h4>
          <p class="text-subtitle1 q-mb-lg">Please upload a document to verify your identity</p>
        </q-card-section>

        <q-card-section>
          <div class="upload-section q-mb-lg">
            <q-file
              v-model="verificationDocument"
              label="Upload Verification Document"
              accept=".pdf,.jpg,.jpeg,.png"
              outlined
              dense
              class="q-mb-md"
              :rules="[val => !!val || 'Please upload a verification document']"
            >
              <template v-slot:prepend>
                <q-icon name="upload_file" />
              </template>
              <template v-slot:hint>
                Accepted formats: PDF, JPG, PNG (Max 5MB)
              </template>
            </q-file>

            <div v-if="verificationDocument" class="uploaded-file q-mb-md">
              <q-chip
                :label="verificationDocument.name"
                color="primary"
                icon="description"
                removable
                @remove="verificationDocument = null"
              />
            </div>
          </div>

          <div class="verification-options">
            <p class="text-body2 q-mb-md">
              Choose how you'd like to proceed with verification:
            </p>
            
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-btn
                  color="primary"
                  label="Verify Now"
                  icon="check_circle"
                  class="full-width"
                  size="lg"
                  :loading="verifying"
                  :disable="!verificationDocument"
                  @click="verifyNow"
                />
                <p class="text-caption q-mt-sm text-center">
                  Upload document and verify immediately
                </p>
              </div>
              
              <div class="col-12 col-md-6">
                <q-btn
                  color="secondary"
                  label="Verify Later"
                  icon="schedule"
                  class="full-width"
                  size="lg"
                  :loading="verifying"
                  @click="verifyLater"
                />
                <p class="text-caption q-mt-sm text-center">
                  Skip verification for now
                </p>
              </div>
            </div>
          </div>
        </q-card-section>

        <q-card-section class="text-center">
          <q-btn
            flat
            color="grey"
            label="Back to Registration"
            @click="$router.push('/role-selection')"
            no-caps
          />
        </q-card-section>
      </q-card>
    </div>
  </q-page>
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
      message: 'Please upload a verification document first'
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
      message: 'Account verified successfully!'
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
      message: errorMessage
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
      message: 'You can verify your account later from your dashboard.'
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
      message: errorMessage
    })
  } finally {
    verifying.value = false
  }
}
</script>

<style scoped>
.verification-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.verification-container {
  width: 100%;
  max-width: 600px;
}

.verification-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.uploaded-file {
  display: flex;
  justify-content: center;
}

.verification-options {
  border-top: 1px solid #e0e0e0;
  padding-top: 20px;
}
</style>
