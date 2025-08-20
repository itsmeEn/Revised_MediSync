<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <h2>Create Account</h2>
          <p>{{ roleTitle }} Registration</p>
        </div>

        <div class="register-form">
          <form @submit.prevent="onRegister">
            <!-- Common Fields -->
            <div class="form-row">
              <div class="form-group">
                <label for="full_name">Full Name *</label>
                <input
                  id="full_name"
                  v-model="formData.full_name"
                  type="text"
                  required
                  placeholder="Enter your full name"
                />
              </div>
              <div class="form-group">
                <label for="email">Email Address *</label>
                <input
                  id="email"
                  v-model="formData.email"
                  type="email"
                  required
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="date_of_birth">Date of Birth</label>
                <input
                  id="date_of_birth"
                  v-model="formData.date_of_birth"
                  type="date"
                />
              </div>
              <div class="form-group">
                <label for="gender">Gender</label>
                <select id="gender" v-model="formData.gender">
                  <option value="">Select gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="password">Password *</label>
                <input
                  id="password"
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  placeholder="Enter password (min 8 chars, alphanumeric)"
                />
                <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                  {{ showPassword ? 'Hide' : 'Show' }}
                </button>
              </div>
              <div class="form-group">
                <label for="password2">Confirm Password *</label>
                <input
                  id="password2"
                  v-model="formData.password2"
                  :type="showPassword2 ? 'text' : 'password'"
                  required
                  placeholder="Confirm your password"
                />
                <button type="button" class="toggle-password" @click="showPassword2 = !showPassword2">
                  {{ showPassword2 ? 'Hide' : 'Show' }}
                </button>
              </div>
            </div>

            <!-- Role-specific Fields -->
            <div v-if="role === 'doctor'" class="role-specific-fields">
              <div class="form-row">
                <div class="form-group">
                  <label for="license_number">Medical License Number *</label>
                  <input
                    id="license_number"
                    v-model="formData.license_number"
                    type="text"
                    required
                    placeholder="Enter your medical license number"
                  />
                </div>
                <div class="form-group">
                  <label for="specialization">Specialization *</label>
                  <input
                    id="specialization"
                    v-model="formData.specialization"
                    type="text"
                    required
                    placeholder="e.g., Cardiology, Pediatrics"
                  />
                </div>
              </div>
            </div>

            <div v-if="role === 'nurse'" class="role-specific-fields">
              <div class="form-group">
                <label for="nurse_license">Nursing License Number *</label>
                <input
                  id="nurse_license"
                  v-model="formData.license_number"
                  type="text"
                  required
                  placeholder="Enter your nursing license number"
                />
              </div>
            </div>

            <div v-if="role === 'patient'" class="role-specific-fields">
              <!-- Patient registration - no additional fields required -->
            </div>

            <button type="submit" :disabled="loading" class="register-btn">
              {{ loading ? 'Creating Account...' : 'Create Account' }}
            </button>
          </form>
        </div>

        <div class="register-footer">
          <p>
            Already have an account?
            <button @click="$router.push('/login')" class="link-btn">
              Sign In
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { api } from '../boot/axios'
import { AxiosError } from 'axios'

const router = useRouter()
const route = useRoute()

const role = ref('')
const loading = ref(false)
const showPassword = ref(false)
const showPassword2 = ref(false)

const formData = ref({
  full_name: '',
  email: '',
  date_of_birth: '',
  gender: '',
  password: '',
  password2: '',
  license_number: '',
  specialization: ''
})

const roleTitle = computed(() => {
  switch (role.value) {
    case 'doctor': return 'Doctor'
    case 'nurse': return 'Nurse'
    case 'patient': return 'Patient'
    default: return ''
  }
})

onMounted(() => {
  role.value = route.params.role as string
  if (!['doctor', 'nurse', 'patient'].includes(role.value)) {
    void router.push('/role-selection')
  }
})

const onRegister = async () => {
  loading.value = true
  
  try {
    const registrationData = {
      ...formData.value,
      role: role.value
    }

    console.log('Sending registration data:', registrationData)

    const response = await api.post('/users/register/', registrationData)

    // Store tokens
    localStorage.setItem('access_token', response.data.tokens.access)
    localStorage.setItem('refresh_token', response.data.tokens.refresh)
    
    // Store user data
    localStorage.setItem('user', JSON.stringify(response.data.user))

    alert('Account created successfully!')

    // Redirect to verification page
    void router.push('/verification')

  } catch (error: unknown) {
    console.error('Registration error:', error)
    
    let errorMessage = 'Registration failed. Please try again.'
    
    if (error instanceof AxiosError) {
      if (error.response?.data) {
        if (typeof error.response.data === 'string') {
          errorMessage = error.response.data
        } else if (typeof error.response.data === 'object' && error.response.data !== null) {
          const data = error.response.data as Record<string, unknown>
          if (data.error && typeof data.error === 'string') {
            errorMessage = data.error
          } else if (data.detail && typeof data.detail === 'string') {
            errorMessage = data.detail
          } else if (data.message && typeof data.message === 'string') {
            errorMessage = data.message
          } else if (data.error && typeof data.error === 'object') {
            errorMessage = JSON.stringify(data.error)
          } else if (data.detail && typeof data.detail === 'object') {
            errorMessage = JSON.stringify(data.detail)
          } else if (data.message && typeof data.message === 'object') {
            errorMessage = JSON.stringify(data.message)
          }
        }
      } else if (error.response?.status === 400) {
        errorMessage = 'Invalid data provided. Please check your information.'
      } else if (error.response?.status === 500) {
        errorMessage = 'Server error. Please try again later.'
      }
    }
    
    alert(`Registration failed: ${errorMessage}`)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 600px;
}

.register-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 28px;
  font-weight: 600;
}

.register-header p {
  margin: 0;
  color: #666;
  font-size: 18px;
}

.register-form {
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.toggle-password {
  margin-top: 8px;
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
}

.role-specific-fields {
  border-top: 1px solid #eee;
  padding-top: 20px;
  margin-top: 20px;
}

.register-btn {
  width: 100%;
  padding: 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-btn:hover:not(:disabled) {
  background: #5a6fd8;
}

.register-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.register-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.register-footer p {
  margin: 0;
  color: #666;
}

.link-btn {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
}

.link-btn:hover {
  color: #5a6fd8;
}

@media (max-width: 768px) {
  .register-card {
    padding: 20px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
