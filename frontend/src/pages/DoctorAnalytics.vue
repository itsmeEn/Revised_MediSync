<template>
  <q-page class="doctor-analytics">
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
          <h4 class="page-title">Doctor Analytics Dashboard</h4>
        </div>
      </div>
    </div>

    <div class="page-content">
      <q-card class="analytics-card">
        <q-card-section>
          <h6 class="text-h6">Analytics Coming Soon</h6>
          <p>Doctor analytics dashboard will be implemented here.</p>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = async () => {
  await router.push('/doctor-dashboard')
}
</script>

<style scoped>
.doctor-analytics {
  background: url('/background.png') no-repeat center center;
  background-size: cover;
  min-height: 100vh;
}

.page-header {
  background: white;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  gap: 1rem;
}

.back-btn {
  color: #666;
}

.page-title {
  margin: 0;
  color: #333;
  font-weight: 600;
}

.page-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.analytics-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
