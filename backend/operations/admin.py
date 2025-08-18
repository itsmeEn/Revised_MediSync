from django.contrib import admin
from .models import (
    AppointmentManagement,
    MedicineInventory,
    Messaging,
    Notification,
    PriorityQueue,
    QueueManagement,
)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__full_name', 'message')


@admin.register(QueueManagement)
class QueueManagementAdmin(admin.ModelAdmin):
    list_display = ('queue_number', 'patient', 'department', 'status', 'created_at')
    list_filter = ('department', 'status')
    search_fields = ('patient__user__full_name', 'queue_number')


@admin.register(MedicineInventory)
class MedicineInventoryAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'current_stock', 'unit_price', 'expiry_date', 'is_expired')
    list_filter = ('expiry_date',)
    search_fields = ('medicine_name', 'batch_number')
    readonly_fields = ('is_expired', 'is_available', 'total_value')


@admin.register(AppointmentManagement)
class AppointmentManagementAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date', 'doctor')
    search_fields = ('patient__user__full_name', 'doctor__user__full_name')


@admin.register(PriorityQueue)
class PriorityQueueAdmin(admin.ModelAdmin):
    list_display = ('patient', 'priority_level', 'queue_number', 'created_at')
    list_filter = ('priority_level',)
    search_fields = ('patient__user__full_name',)


@admin.register(Messaging)
class MessagingAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('sender__full_name', 'receiver__full_name', 'message')
