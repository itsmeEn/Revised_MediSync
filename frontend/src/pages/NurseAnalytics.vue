<template>
  <q-page class="nurse-analytics">
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
          <h4 class="page-title">Analytics Dashboard</h4>
        </div>
        <div class="header-right">
          <q-select
            v-model="selectedPeriod"
            :options="periodOptions"
            label="Time Period"
            outlined
            dense
            style="min-width: 150px"
          />
        </div>
      </div>
    </div>

    <div class="page-content">
      <!-- Key Metrics Cards -->
      <div class="metrics-section">
        <div class="metrics-grid">
          <q-card class="metric-card patients-seen">
            <q-card-section class="text-center">
              <div class="metric-icon">
                <q-icon name="people" size="2rem" />
              </div>
              <div class="metric-number">{{ analyticsData.patientsSeen }}</div>
              <div class="metric-label">Patients Seen</div>
              <div class="metric-change positive">
                <q-icon name="trending_up" size="sm" />
                +{{ analyticsData.patientGrowth }}%
              </div>
            </q-card-section>
          </q-card>

          <q-card class="metric-card assessments-completed">
            <q-card-section class="text-center">
              <div class="metric-icon">
                <q-icon name="assignment" size="2rem" />
              </div>
              <div class="metric-number">{{ analyticsData.assessmentsCompleted }}</div>
              <div class="metric-label">Assessments Completed</div>
              <div class="metric-change positive">
                <q-icon name="trending_up" size="sm" />
                +{{ analyticsData.assessmentGrowth }}%
              </div>
            </q-card-section>
          </q-card>

          <q-card class="metric-card medications-administered">
            <q-card-section class="text-center">
              <div class="metric-icon">
                <q-icon name="medication" size="2rem" />
              </div>
              <div class="metric-number">{{ analyticsData.medicationsAdministered }}</div>
              <div class="metric-label">Medications Given</div>
              <div class="metric-change positive">
                <q-icon name="trending_up" size="sm" />
                +{{ analyticsData.medicationGrowth }}%
              </div>
            </q-card-section>
          </q-card>

          <q-card class="metric-card average-wait-time">
            <q-card-section class="text-center">
              <div class="metric-icon">
                <q-icon name="schedule" size="2rem" />
              </div>
              <div class="metric-number">{{ analyticsData.averageWaitTime }}min</div>
              <div class="metric-label">Avg Wait Time</div>
              <div class="metric-change negative">
                <q-icon name="trending_down" size="sm" />
                -{{ analyticsData.waitTimeReduction }}%
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-section">
        <div class="row q-gutter-lg">
          <!-- Patient Volume Chart -->
          <div class="col-12 col-lg-8">
            <q-card class="chart-card">
              <q-card-section>
                <h6 class="text-h6 q-mb-md">Patient Volume Trends</h6>
                <div class="chart-container">
                  <canvas ref="patientVolumeChart" width="400" height="200"></canvas>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <!-- Assessment Categories Chart -->
          <div class="col-12 col-lg-4">
            <q-card class="chart-card">
              <q-card-section>
                <h6 class="text-h6 q-mb-md">Assessment Categories</h6>
                <div class="chart-container">
                  <canvas ref="assessmentCategoriesChart" width="300" height="300"></canvas>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <div class="row q-gutter-lg q-mt-lg">
          <!-- Medication Usage Chart -->
          <div class="col-12 col-lg-6">
            <q-card class="chart-card">
              <q-card-section>
                <h6 class="text-h6 q-mb-md">Top Medications Administered</h6>
                <div class="chart-container">
                  <canvas ref="medicationUsageChart" width="400" height="300"></canvas>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <!-- Wait Time Distribution Chart -->
          <div class="col-12 col-lg-6">
            <q-card class="chart-card">
              <q-card-section>
                <h6 class="text-h6 q-mb-md">Wait Time Distribution</h6>
                <div class="chart-container">
                  <canvas ref="waitTimeChart" width="400" height="300"></canvas>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- Detailed Analytics Tables -->
      <div class="tables-section">
        <div class="row q-gutter-lg">
          <!-- Top Patients Table -->
          <div class="col-12 col-lg-6">
            <q-card class="table-card">
              <q-card-section>
                <h6 class="text-h6 q-mb-md">Most Frequent Patients</h6>
                <q-table
                  :rows="topPatients"
                  :columns="patientColumns"
                  row-key="id"
                  :pagination="{ rowsPerPage: 5 }"
                  flat
                  bordered
                />
              </q-card-section>
            </q-card>
          </div>

          <!-- Recent Activities Table -->
          <div class="col-12 col-lg-6">
            <q-card class="table-card">
              <q-card-section>
                <h6 class="text-h6 q-mb-md">Recent Activities</h6>
                <q-table
                  :rows="recentActivities"
                  :columns="activityColumns"
                  row-key="id"
                  :pagination="{ rowsPerPage: 5 }"
                  flat
                  bordered
                >
                  <template v-slot:body-cell-type="props">
                    <q-td :props="props">
                      <q-chip
                        :color="getActivityTypeColor(props.value)"
                        text-color="white"
                        :label="props.value"
                        size="sm"
                      />
                    </q-td>
                  </template>
                </q-table>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- Performance Insights -->
      <div class="insights-section">
        <q-card class="insights-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Performance Insights</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <div class="insight-item positive">
                  <q-icon name="check_circle" size="md" />
                  <div class="insight-content">
                    <div class="insight-title">Efficiency Improved</div>
                    <div class="insight-description">
                      Patient assessment time reduced by 15% compared to last month
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="insight-item warning">
                  <q-icon name="warning" size="md" />
                  <div class="insight-content">
                    <div class="insight-title">Stock Alert</div>
                    <div class="insight-description">
                      3 medications are running low and need restocking
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="insight-item info">
                  <q-icon name="info" size="md" />
                  <div class="insight-content">
                    <div class="insight-title">Peak Hours</div>
                    <div class="insight-description">
                      Highest patient volume occurs between 9 AM - 11 AM
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="insight-item success">
                  <q-icon name="star" size="md" />
                  <div class="insight-content">
                    <div class="insight-title">Quality Score</div>
                    <div class="insight-description">
                      Patient satisfaction score improved to 4.8/5.0
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Chart references
const patientVolumeChart = ref<HTMLCanvasElement>()
const assessmentCategoriesChart = ref<HTMLCanvasElement>()
const medicationUsageChart = ref<HTMLCanvasElement>()
const waitTimeChart = ref<HTMLCanvasElement>()

// Time period selection
const selectedPeriod = ref('month')

const periodOptions = [
  { label: 'Last 7 Days', value: 'week' },
  { label: 'Last 30 Days', value: 'month' },
  { label: 'Last 3 Months', value: 'quarter' },
  { label: 'Last Year', value: 'year' }
]

// Analytics data
const analyticsData = ref({
  patientsSeen: 156,
  patientGrowth: 12,
  assessmentsCompleted: 89,
  assessmentGrowth: 8,
  medicationsAdministered: 234,
  medicationGrowth: 15,
  averageWaitTime: 18,
  waitTimeReduction: 22
})

// Table data
const topPatients = ref([
  { id: 1, name: 'John Doe', visits: 8, lastVisit: '2024-01-15', status: 'Active' },
  { id: 2, name: 'Jane Smith', visits: 6, lastVisit: '2024-01-14', status: 'Active' },
  { id: 3, name: 'Mike Johnson', visits: 5, lastVisit: '2024-01-13', status: 'Active' },
  { id: 4, name: 'Sarah Wilson', visits: 4, lastVisit: '2024-01-12', status: 'Active' },
  { id: 5, name: 'Robert Brown', visits: 3, lastVisit: '2024-01-11', status: 'Active' }
])

const recentActivities = ref([
  { id: 1, type: 'Assessment', patient: 'John Doe', time: '2 hours ago', duration: '15 min' },
  { id: 2, type: 'Medication', patient: 'Jane Smith', time: '3 hours ago', duration: '5 min' },
  { id: 3, type: 'Assessment', patient: 'Mike Johnson', time: '4 hours ago', duration: '20 min' },
  { id: 4, type: 'Vitals', patient: 'Sarah Wilson', time: '5 hours ago', duration: '8 min' },
  { id: 5, type: 'Medication', patient: 'Robert Brown', time: '6 hours ago', duration: '5 min' }
])

// Table columns
const patientColumns = [
  { name: 'name', label: 'Patient Name', field: 'name', align: 'left' as const },
  { name: 'visits', label: 'Visits', field: 'visits', align: 'center' as const },
  { name: 'lastVisit', label: 'Last Visit', field: 'lastVisit', align: 'center' as const },
  { name: 'status', label: 'Status', field: 'status', align: 'center' as const }
]

const activityColumns = [
  { name: 'type', label: 'Type', field: 'type', align: 'left' as const },
  { name: 'patient', label: 'Patient', field: 'patient', align: 'left' as const },
  { name: 'time', label: 'Time', field: 'time', align: 'center' as const },
  { name: 'duration', label: 'Duration', field: 'duration', align: 'center' as const }
]

// Methods
const goBack = () => {
  void router.push('/nurse-dashboard')
}

const getActivityTypeColor = (type: string) => {
  switch (type.toLowerCase()) {
    case 'assessment': return 'primary'
    case 'medication': return 'secondary'
    case 'vitals': return 'accent'
    default: return 'grey'
  }
}

// Chart initialization functions
const initPatientVolumeChart = () => {
  const ctx = patientVolumeChart.value?.getContext('2d')
  if (!ctx) return

  // Mock chart data - replace with actual Chart.js implementation
  console.log('Initializing patient volume chart')
}

const initAssessmentCategoriesChart = () => {
  const ctx = assessmentCategoriesChart.value?.getContext('2d')
  if (!ctx) return

  // Mock chart data - replace with actual Chart.js implementation
  console.log('Initializing assessment categories chart')
}

const initMedicationUsageChart = () => {
  const ctx = medicationUsageChart.value?.getContext('2d')
  if (!ctx) return

  // Mock chart data - replace with actual Chart.js implementation
  console.log('Initializing medication usage chart')
}

const initWaitTimeChart = () => {
  const ctx = waitTimeChart.value?.getContext('2d')
  if (!ctx) return

  // Mock chart data - replace with actual Chart.js implementation
  console.log('Initializing wait time chart')
}

// Watch for period changes
watch(selectedPeriod, (newPeriod) => {
  console.log('Period changed to:', newPeriod)
  // Reload analytics data based on selected period
  loadAnalyticsData(newPeriod)
})

const loadAnalyticsData = (period: string) => {
  // Mock API call to load data based on period
  console.log('Loading analytics data for period:', period)
  
  // Update analytics data based on period
  switch (period) {
    case 'week':
      analyticsData.value = {
        patientsSeen: 45,
        patientGrowth: 8,
        assessmentsCompleted: 28,
        assessmentGrowth: 5,
        medicationsAdministered: 67,
        medicationGrowth: 12,
        averageWaitTime: 15,
        waitTimeReduction: 18
      }
      break
    case 'month':
      analyticsData.value = {
        patientsSeen: 156,
        patientGrowth: 12,
        assessmentsCompleted: 89,
        assessmentGrowth: 8,
        medicationsAdministered: 234,
        medicationGrowth: 15,
        averageWaitTime: 18,
        waitTimeReduction: 22
      }
      break
    case 'quarter':
      analyticsData.value = {
        patientsSeen: 432,
        patientGrowth: 18,
        assessmentsCompleted: 267,
        assessmentGrowth: 14,
        medicationsAdministered: 689,
        medicationGrowth: 22,
        averageWaitTime: 16,
        waitTimeReduction: 25
      }
      break
    case 'year':
      analyticsData.value = {
        patientsSeen: 1847,
        patientGrowth: 25,
        assessmentsCompleted: 1123,
        assessmentGrowth: 20,
        medicationsAdministered: 2891,
        medicationGrowth: 30,
        averageWaitTime: 14,
        waitTimeReduction: 35
      }
      break
  }
}

onMounted(() => {
  // Initialize charts
  setTimeout(() => {
    initPatientVolumeChart()
    initAssessmentCategoriesChart()
    initMedicationUsageChart()
    initWaitTimeChart()
  }, 100)

  // Load initial data
  loadAnalyticsData(selectedPeriod.value)
})
</script>

<style scoped>
.nurse-analytics {
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

.metrics-section {
  margin-bottom: 30px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.metric-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.metric-icon {
  margin-bottom: 10px;
}

.metric-number {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 1rem;
  color: #666;
  margin-bottom: 10px;
}

.metric-change {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  font-size: 0.9rem;
  font-weight: 500;
}

.metric-change.positive {
  color: #4caf50;
}

.metric-change.negative {
  color: #f44336;
}

/* Card-specific colors */
.patients-seen .metric-icon {
  color: #2196f3;
}

.assessments-completed .metric-icon {
  color: #ff9800;
}

.medications-administered .metric-icon {
  color: #4caf50;
}

.average-wait-time .metric-icon {
  color: #e91e63;
}

.charts-section {
  margin-bottom: 30px;
}

.chart-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 100%;
}

.chart-container {
  position: relative;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tables-section {
  margin-bottom: 30px;
}

.table-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 100%;
}

.insights-section {
  margin-bottom: 20px;
}

.insights-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.insight-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.insight-item.positive {
  background: rgba(76, 175, 80, 0.1);
  border-left: 4px solid #4caf50;
}

.insight-item.warning {
  background: rgba(255, 152, 0, 0.1);
  border-left: 4px solid #ff9800;
}

.insight-item.info {
  background: rgba(33, 150, 243, 0.1);
  border-left: 4px solid #2196f3;
}

.insight-item.success {
  background: rgba(156, 39, 176, 0.1);
  border-left: 4px solid #9c27b0;
}

.insight-content {
  flex: 1;
}

.insight-title {
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.insight-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .page-content {
    padding: 10px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .header-right {
    align-self: flex-end;
  }
  
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .chart-container {
    height: 250px;
  }
}
</style>
