from rest_framework import serializers
from .models import AppointmentManagement, QueueManagement, PriorityQueue, Notification, Messaging
from backend.users.models import User

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_appointments = serializers.IntegerField()
    total_patients = serializers.IntegerField()
    normal_queue = serializers.IntegerField()
    priority_queue = serializers.IntegerField()
    notifications = serializers.IntegerField()
    pending_assessment = serializers.IntegerField()

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.full_name', read_only=True)
    
    class Meta:
        model = AppointmentManagement
        fields = ['appointment_id', 'patient_name', 'doctor_name', 'appointment_date', 'status', 'appointment_type']

class QueueSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    
    class Meta:
        model = QueueManagement
        fields = ['queue_number', 'patient_name', 'department', 'status', 'position_in_queue', 'enqueue_time']

class PriorityQueueSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    
    class Meta:
        model = PriorityQueue
        fields = ['queue_number', 'patient_name', 'priority_level', 'department', 'priority_position']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']

# NurseChartSerializer commented out until NurseChart model is fully implemented
# class NurseChartSerializer(serializers.ModelSerializer):
#     patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
#     nurse_name = serializers.CharField(source='nurse.user.full_name', read_only=True)
#     
#     class Meta:
#         model = NurseChart
#         fields = ['id', 'patient_name', 'nurse_name', 'chief_complaint', 'status', 'priority', 'created_at']
