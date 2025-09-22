from django.urls import path
from . import views

urlpatterns = [
    # Dashboard statistics
    path('dashboard/stats/', views.doctor_dashboard_stats, name='doctor_dashboard_stats'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('queue/patients/', views.doctor_queue_patients, name='doctor_queue_patients'),
    path('notifications/', views.doctor_notifications, name='doctor_notifications'),
    # path('pending-assessments/', views.doctor_pending_assessments, name='doctor_pending_assessments'),
    
    # Appointment management
    path('blocked-dates/', views.doctor_blocked_dates, name='doctor_blocked_dates'),
    path('block-date/', views.doctor_block_date, name='doctor_block_date'),
    path('create-appointment/', views.doctor_create_appointment, name='doctor_create_appointment'),
    
    # Patient Queue Management System
    path('patient/check-in/', views.patient_check_in, name='patient_check_in'),
    path('patient/queue-status/', views.patient_queue_status, name='patient_queue_status'),
    path('public/queue-display/', views.public_queue_display, name='public_queue_display'),
    
    # Staff Queue Management
    path('staff/queue-dashboard/', views.staff_queue_dashboard, name='staff_queue_dashboard'),
    path('staff/call-next-patient/', views.call_next_patient, name='call_next_patient'),
    path('staff/complete-service/', views.complete_patient_service, name='complete_patient_service'),
    path('staff/remove-patient/', views.remove_patient_from_queue, name='remove_patient_from_queue'),
]
