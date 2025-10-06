<template>
  <q-page class="nurse-patient-assessment">
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
          <h4 class="page-title">Patient Assessment</h4>
        </div>
        <div class="header-right">
          <q-btn
            color="primary"
            label="Save Assessment"
            icon="save"
            @click="saveAssessment"
            :loading="saving"
          />
        </div>
      </div>
    </div>

    <div class="page-content">
      <!-- Patient Selection -->
      <q-card class="patient-selection-card">
        <q-card-section>
          <div class="row items-center q-mb-md">
            <h6 class="text-h6 q-mb-none">Select Patient</h6>
            <q-space />
            <q-btn
              color="secondary"
              label="Add New Patient"
              icon="person_add"
              size="sm"
            />
          </div>
          
          <q-select
            v-model="selectedPatient"
            :options="patientOptions"
            label="Choose Patient"
            option-label="name"
            option-value="id"
            emit-value
            map-options
            clearable
            class="patient-select"
          >
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps">
                <q-item-section avatar>
                  <q-avatar color="primary" text-color="white">
                    {{ scope.opt.name.charAt(0) }}
                  </q-avatar>
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ scope.opt.name }}</q-item-label>
                  <q-item-label caption>ID: {{ scope.opt.id }} | Age: {{ scope.opt.age }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </q-card-section>
      </q-card>

      <!-- Assessment Form -->
      <div v-if="selectedPatient" class="assessment-form">
        <!-- Patient Info Card -->
        <q-card class="patient-info-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Patient Information</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.patientName"
                  label="Full Name"
                  readonly
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model="assessment.patientAge"
                  label="Age"
                  readonly
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model="assessment.patientGender"
                  label="Gender"
                  readonly
                  outlined
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Vital Signs -->
        <q-card class="vital-signs-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Vital Signs</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.bloodPressure"
                  label="Blood Pressure (mmHg)"
                  type="text"
                  placeholder="120/80"
                  outlined
                  :rules="[ (val: string | null) => !!val || 'Blood pressure is required' ]"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.heartRate"
                  label="Heart Rate (bpm)"
                  type="number"
                  outlined
                  :rules="[ (val: string | null) => !!val || 'Heart rate is required' ]"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.temperature"
                  label="Temperature (°C)"
                  type="number"
                  step="0.1"
                  outlined
                  :rules="[ (val: string | null) => !!val || 'Temperature is required' ]"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.respiratoryRate"
                  label="Respiratory Rate (breaths/min)"
                  type="number"
                  outlined
                  :rules="[ (val: string | null) => !!val || 'Respiratory rate is required' ]"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.oxygenSaturation"
                  label="Oxygen Saturation (%)"
                  type="number"
                  outlined
                  :rules="[ (val: string | null) => !!val || 'Oxygen saturation is required' ]"
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.weight"
                  label="Weight (kg)"
                  type="number"
                  step="0.1"
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model.number="assessment.vitals.height"
                  label="Height (cm)"
                  type="number"
                  outlined
                />
              </div>
              <div class="col-12 col-md-3">
                <q-input
                  v-model="assessment.vitals.bmi"
                  label="BMI"
                  readonly
                  outlined
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Pain Assessment -->
        <q-card class="pain-assessment-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Pain Assessment</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-4">
                <q-select
                  v-model="assessment.pain.level"
                  :options="painLevels"
                  label="Pain Level (0-10)"
                  outlined
                  emit-value
                  map-options
                />
              </div>
              <div class="col-12 col-md-4">
                <q-select
                  v-model="assessment.pain.location"
                  :options="painLocations"
                  label="Pain Location"
                  outlined
                  multiple
                  use-chips
                />
              </div>
              <div class="col-12 col-md-4">
                <q-select
                  v-model="assessment.pain.type"
                  :options="painTypes"
                  label="Pain Type"
                  outlined
                  multiple
                  use-chips
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.pain.description"
                  label="Pain Description"
                  type="textarea"
                  outlined
                  rows="3"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Physical Examination -->
        <q-card class="physical-exam-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Physical Examination</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.generalAppearance"
                  label="General Appearance"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.skinCondition"
                  label="Skin Condition"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.cardiovascular"
                  label="Cardiovascular"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.respiratory"
                  label="Respiratory"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.gastrointestinal"
                  label="Gastrointestinal"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input
                  v-model="assessment.physicalExam.neurological"
                  label="Neurological"
                  type="textarea"
                  outlined
                  rows="2"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Assessment Notes -->
        <q-card class="assessment-notes-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Assessment Notes</h6>
            <div class="row q-gutter-md">
              <div class="col-12">
                <q-input
                  v-model="assessment.notes.subjective"
                  label="Subjective Assessment"
                  type="textarea"
                  outlined
                  rows="4"
                  placeholder="Patient's chief complaint and history..."
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.notes.objective"
                  label="Objective Assessment"
                  type="textarea"
                  outlined
                  rows="4"
                  placeholder="Observations and findings..."
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.notes.assessment"
                  label="Clinical Assessment"
                  type="textarea"
                  outlined
                  rows="4"
                  placeholder="Diagnosis and clinical impression..."
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.notes.plan"
                  label="Plan of Care"
                  type="textarea"
                  outlined
                  rows="4"
                  placeholder="Treatment plan and recommendations..."
                />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Emergency Assessment -->
        <q-card class="emergency-assessment-card">
          <q-card-section>
            <h6 class="text-h6 q-mb-md">Emergency Assessment</h6>
            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-select
                  v-model="assessment.emergency.priority"
                  :options="priorityLevels"
                  label="Priority Level"
                  outlined
                  emit-value
                  map-options
                />
              </div>
              <div class="col-12 col-md-6">
                <q-select
                  v-model="assessment.emergency.requiresImmediate"
                  :options="[
                    { label: 'No', value: false },
                    { label: 'Yes', value: true }
                  ]"
                  label="Requires Immediate Attention"
                  outlined
                  emit-value
                  map-options
                />
              </div>
              <div class="col-12">
                <q-input
                  v-model="assessment.emergency.notes"
                  label="Emergency Notes"
                  type="textarea"
                  outlined
                  rows="3"
                  placeholder="Any urgent concerns or immediate actions needed..."
                />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- No Patient Selected Message -->
      <div v-else class="no-patient-message">
        <q-card class="text-center">
          <q-card-section>
            <q-icon name="person_search" size="4rem" color="grey-5" />
            <h6 class="text-h6 q-mt-md">Select a Patient</h6>
            <p class="text-body2 text-grey-6">
              Please select a patient from the dropdown above to begin the assessment.
            </p>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

const router = useRouter()
const $q = useQuasar()

// Patient selection
const selectedPatient = ref(null)
const saving = ref(false)

// Patient options (mock data)
const patientOptions = ref([
  { id: 1, name: 'John Doe', age: 45, gender: 'Male' },
  { id: 2, name: 'Jane Smith', age: 32, gender: 'Female' },
  { id: 3, name: 'Mike Johnson', age: 58, gender: 'Male' },
  { id: 4, name: 'Sarah Wilson', age: 29, gender: 'Female' },
  { id: 5, name: 'Robert Brown', age: 67, gender: 'Male' }
])

// Assessment data
const assessment = ref({
  patientName: '',
  patientAge: '',
  patientGender: '',
  vitals: {
    bloodPressure: '',
    heartRate: null,
    temperature: null,
    respiratoryRate: null,
    oxygenSaturation: null,
    weight: null,
    height: null,
    bmi: ''
  },
  pain: {
    level: null,
    location: [],
    type: [],
    description: ''
  },
  physicalExam: {
    generalAppearance: '',
    skinCondition: '',
    cardiovascular: '',
    respiratory: '',
    gastrointestinal: '',
    neurological: ''
  },
  notes: {
    subjective: '',
    objective: '',
    assessment: '',
    plan: ''
  },
  emergency: {
    priority: 'normal',
    requiresImmediate: false,
    notes: ''
  }
})

// Options for dropdowns
const painLevels = [
  { label: '0 - No Pain', value: 0 },
  { label: '1-3 - Mild Pain', value: 1 },
  { label: '4-6 - Moderate Pain', value: 4 },
  { label: '7-9 - Severe Pain', value: 7 },
  { label: '10 - Worst Pain', value: 10 }
]

const painLocations = [
  'Head', 'Neck', 'Chest', 'Back', 'Abdomen', 'Arms', 'Legs', 'Joints'
]

const painTypes = [
  'Sharp', 'Dull', 'Throbbing', 'Burning', 'Cramping', 'Aching', 'Stabbing'
]

const priorityLevels = [
  { label: 'Normal', value: 'normal' },
  { label: 'Low Priority', value: 'low' },
  { label: 'Medium Priority', value: 'medium' },
  { label: 'High Priority', value: 'high' },
  { label: 'Emergency', value: 'emergency' }
]

// Watch for patient selection changes
watch(selectedPatient, (newPatient) => {
  if (newPatient) {
    const patient = patientOptions.value.find(p => p.id === newPatient)
    if (patient) {
      assessment.value.patientName = patient.name
      assessment.value.patientAge = patient.age.toString()
      assessment.value.patientGender = patient.gender
    }
  } else {
    // Reset form when no patient is selected
    assessment.value = {
      patientName: '',
      patientAge: '',
      patientGender: '',
      vitals: {
        bloodPressure: '',
        heartRate: null,
        temperature: null,
        respiratoryRate: null,
        oxygenSaturation: null,
        weight: null,
        height: null,
        bmi: ''
      },
      pain: {
        level: null,
        location: [],
        type: [],
        description: ''
      },
      physicalExam: {
        generalAppearance: '',
        skinCondition: '',
        cardiovascular: '',
        respiratory: '',
        gastrointestinal: '',
        neurological: ''
      },
      notes: {
        subjective: '',
        objective: '',
        assessment: '',
        plan: ''
      },
      emergency: {
        priority: 'normal',
        requiresImmediate: false,
        notes: ''
      }
    }
  }
})

// Calculate BMI when weight or height changes
watch([() => assessment.value.vitals.weight, () => assessment.value.vitals.height], ([weight, height]) => {
  if (weight && height) {
    const heightInMeters = height / 100
    const bmi = (weight / (heightInMeters * heightInMeters)).toFixed(1)
    assessment.value.vitals.bmi = bmi
  } else {
    assessment.value.vitals.bmi = ''
  }
})

const goBack = () => {
  void router.push('/nurse-dashboard')
}

const saveAssessment = async () => {
  if (!selectedPatient.value) {
    $q.notify({
      type: 'warning',
      message: 'Please select a patient first',
      position: 'top'
    })
    return
  }

  saving.value = true

  try {
    // Validate required fields
    const requiredVitals = ['bloodPressure', 'heartRate', 'temperature', 'respiratoryRate', 'oxygenSaturation'] as const
    const missingVitals = requiredVitals.filter(vital => !assessment.value.vitals[vital])
    
    if (missingVitals.length > 0) {
      $q.notify({
        type: 'warning',
        message: `Please fill in all required vital signs: ${missingVitals.join(', ')}`,
        position: 'top'
      })
      return
    }

    // Mock API call - replace with actual API
    await new Promise(resolve => setTimeout(resolve, 2000))

    $q.notify({
      type: 'positive',
      message: 'Assessment saved successfully!',
      position: 'top'
    })

    // Reset form after successful save
    selectedPatient.value = null

  } catch (error) {
    console.error('Error saving assessment:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to save assessment. Please try again.',
      position: 'top'
    })
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.nurse-patient-assessment {
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

.patient-selection-card,
.patient-info-card,
.vital-signs-card,
.pain-assessment-card,
.physical-exam-card,
.assessment-notes-card,
.emergency-assessment-card {
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.patient-select {
  max-width: 400px;
}

.assessment-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.no-patient-message {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.no-patient-message .q-card {
  max-width: 400px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
}
</style>
