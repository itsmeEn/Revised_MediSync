<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h2>Welcome to MediSync</h2>
          <p>Sign in to your account</p>
        </div>

        <div class="login-form">
          <form @submit.prevent="onLogin">
            <div class="form-group">
              <label for="email">Email Address</label>
              <input
                id="email"
                v-model="email"
                type="email"
                required
                placeholder="Enter your email"
              />
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="Enter your password"
              />
              <button type="button" @click="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>

            <div class="forgot-password">
              <button type="button" @click="$router.push('/forgot-password')" class="forgot-btn">
                Forgot Password?
              </button>
            </div>

            <button type="submit" :disabled="loading" class="login-btn">
              {{ loading ? 'Signing In...' : 'Sign In' }}
            </button>
          </form>
        </div>

        <div class="login-footer">
          <p>
            Don't have an account?
            <button @click="$router.push('/role-selection')" class="link-btn">
              Create Account
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from '../boot/axios'
import { AxiosError } from 'axios'

const router = useRouter()
const $q = useQuasar()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)

const onLogin = async () => {
  loading.value = true
  
  try {
    const response = await api.post('/users/login/', {
      email: email.value,
      password: password.value
    })

    console.log('Login response:', response.data)  // Add debug logging
    console.log('Response status:', response.status)  // Add debug logging

    // Check if response has the expected structure
    if (!response.data.access || !response.data.refresh) {
      console.error('Response missing tokens:', response.data)  // Add debug logging
      throw new Error('Invalid response structure: missing tokens')
    }

    // Store tokens
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    
    // Store user data (if available)
    if (response.data.user) {
      localStorage.setItem('user', JSON.stringify(response.data.user))
    }

    // Show success toast notification
    $q.notify({
      type: 'positive',
      message: 'Login successful!',
      position: 'top',
      timeout: 2000
    })

    // Redirect based on user role
    const user = response.data.user
    console.log('=== LOGIN DEBUG INFO ===')
    console.log('Full response data:', response.data)
    console.log('User data for redirect:', user)
    console.log('User role:', user?.role)
    console.log('User is_verified:', user?.is_verified)
    console.log('User email:', user?.email)
    console.log('========================')
    
    // Check if user is verified
    if (user && !user.is_verified) {
      console.log('User not verified, redirecting to verification page')
      setTimeout(() => {
        console.log('Executing redirect to verification page...')
        router.push('/verification').then(() => {
          console.log('Successfully redirected to verification page')
        }).catch((error) => {
          console.error('Error redirecting to verification page:', error)
        })
      }, 1000) // Small delay to show the toast
      return
    }
    
    // If user is verified or no verification required, redirect to role-based dashboard
    setTimeout(() => {
      console.log('Executing role-based redirect...')
      if (!user || !user.role) {
        console.log('No user data or role, redirecting to home')
        router.push('/').then(() => {
          console.log('Successfully redirected to home')
        }).catch((error) => {
          console.error('Error redirecting to home:', error)
        })
        return
      }
      
      console.log(`Redirecting to ${user.role} dashboard...`)
      let redirectPromise: Promise<unknown>
      
      switch (user.role) {
        case 'doctor':
          console.log('Redirecting to doctor dashboard')
          redirectPromise = router.push('/doctor-dashboard')
          break
        case 'nurse':
          console.log('Redirecting to nurse dashboard')
          redirectPromise = router.push('/nurse-dashboard')
          break
        case 'patient':
          console.log('Redirecting to patient dashboard')
          redirectPromise = router.push('/patient-dashboard')
          break
        default:
          console.log('No matching role, redirecting to home')
          redirectPromise = router.push('/')
      }
      
      redirectPromise.then(() => {
        console.log(`Successfully redirected to ${user.role} dashboard`)
      }).catch((error) => {
        console.error('Error during redirect:', error)
      })
    }, 1000) // Small delay to show the toast

  } catch (error: unknown) {
    console.error('Login error:', error)
    
    let errorMessage = 'Login failed. Please try again.'
    
    if (error instanceof AxiosError) {
      if (error.response?.data) {
        errorMessage = error.response.data.message || error.response.data.error || errorMessage
      }
    } else if (error instanceof Error) {
      errorMessage = error.message
    }
    
    // Show error toast notification
    $q.notify({
      type: 'negative',
      message: `Login failed: ${errorMessage}`,
      position: 'top',
      timeout: 4000
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #286660;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 24px;
}

.login-header p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.login-form {
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

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #1e7668;
  box-shadow: 0 0 0 2px rgba(30, 118, 104, 0.2);
}

.forgot-password {
  text-align: right;
  margin-bottom: 20px;
}

.forgot-btn {
  background: none;
  border: none;
  color: #1e7668;
  font-size: 14px;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
}

.forgot-btn:hover {
  color: #5a6fd8;
}

.form-group button {
  margin-top: 8px;
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: #1e7668;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover:not(:disabled) {
  background: #6ca299;
}

.login-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.login-footer p {
  margin: 0;
  color: #666;
}

.link-btn {
  background: none;
  border: none;
  color: #1e7668;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
}

.link-btn:hover {
  color: #6ca299;
}
</style>
