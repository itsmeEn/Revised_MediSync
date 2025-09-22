from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import uuid

from backend.users.models import PatientProfile

# Import tasks with error handling
try:
    from .tasks import process_data_update_analytics
    TASKS_AVAILABLE = True
except ImportError as e:
    print(f"Analytics tasks not available: {e}")
    TASKS_AVAILABLE = False

@receiver(post_save, sender=PatientProfile)
def patient_profile_saved(sender, instance, created, **kwargs):
    """
    Trigger analytics when a patient profile is created or updated
    """
    if not TASKS_AVAILABLE:
        return
        
    try:
        action = 'create' if created else 'update'
        process_data_update_analytics.delay(
        model_name='PatientProfile',
        record_id=instance.id,
        action=action
        )
    except Exception as e:
        # Log error but don't break the save operation
        print(f"Error triggering analytics for patient profile {instance.id}: {str(e)}")

@receiver(post_delete, sender=PatientProfile)
def patient_profile_deleted(sender, instance, **kwargs):
    """
    Trigger analytics when a patient profile is deleted
    """
    if not TASKS_AVAILABLE:
        return
        
    try:
        process_data_update_analytics.delay(
            model_name='PatientProfile',
            record_id=instance.id,
            action='delete'
        )
    except Exception as e:
        # Log error but don't break the delete operation
        print(f"Error triggering analytics for deleted patient profile {instance.id}: {str(e)}")

# You can add more signal handlers for other models that affect analytics
# For example, if you have appointment models, medicine inventory, etc.

# @receiver(post_save, sender=AppointmentManagement)
# def appointment_saved(sender, instance, created, **kwargs):
#     """
#     Trigger analytics when an appointment is created or updated
#     """
#     try:
#         action = 'create' if created else 'update'
#         process_data_update_analytics.delay(
#             model_name='AppointmentManagement',
#             record_id=instance.id,
#             action=action
#         )
#     except Exception as e:
#         print(f"Error triggering analytics for appointment {instance.id}: {str(e)}")
