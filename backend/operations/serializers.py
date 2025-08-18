from rest_framework import serializers
from .models import (
    AppointmentManagement,
    MedicineInventory,
    Messaging,
    Notification,
    PriorityQueue,
    QueueManagement,
)
from datetime import timedelta


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"


class QueueManagementSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(read_only=True)
    estimated_wait_time = serializers.DurationField(read_only=True)
    actual_wait_time = serializers.DurationField(read_only=True)
    position_in_queue = serializers.IntegerField(read_only=True)
        
    class Meta:
        model = QueueManagement
        fields = "__all__"

    """
        Get the estimated waiting time of arrivals based on total_patient, expected_patients, the time it started and ended
        if in the hospital the average waiting is 1-3 hours we should get it's estimated time tama?
    """
    def get_estimated_wait_time(self, obj):
       return obj.get_estimated_wait_time()
   
    """
    get the number of patients ahead
    """
    def get_patients_ahead(self, obj):
        return QueueManagement.objects.filter(
        department=self.department, status__in=["waiting", "in_progress"],
        position_in_queue__lt=self.position_in_queue
        ).count()

   

class MedicineInventorySerializer(serializers.ModelSerializer):
    inventory = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MedicineInventory
        fields = "__all__"
        read_only_fields = ("is_expired", "is_available", "total_value")


class AppointmentManagementSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(read_only=True)
    doctor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AppointmentManagement
        fields = "__all__"


class PriorityQueueSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(read_only=True)
    estimated_wait_time = serializers.DurationField(read_only=True)
    priority_patients_ahead = serializers.SerializerMethodField()
    

    class Meta:
        model = PriorityQueue
        fields = "__all__"
    
        """
        get estimated waiting time base on their priority level
        """
    def get_estimated_wait_time(self, obj):
        return obj.get_estimated_wait_time()
    
    """
    get the number of patients ahead
    """
    def get_priority_patients_ahead(self, obj):
        return PriorityQueue.objects.filter(
        department=self.department, priority_level=self.priority_level,
        priority_position__lt=self.priority_position
        ).count()

class MessagingSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Messaging
        fields = "__all__"
