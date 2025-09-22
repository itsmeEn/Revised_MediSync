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
    
    # Messaging endpoints
    path('messaging/conversations/', views.get_conversations, name='get_conversations'),
    path('messaging/conversations/create/', views.create_conversation, name='create_conversation'),
    path('messaging/conversations/<int:conversation_id>/messages/', views.get_messages, name='get_messages'),
    path('messaging/conversations/<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('messaging/messages/<int:message_id>/react/', views.add_reaction, name='add_reaction'),
    path('messaging/available-users/', views.get_available_users, name='get_available_users'),
]
