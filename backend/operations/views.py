from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import AppointmentManagement, QueueManagement, PriorityQueue, Notification, Messaging, DoctorAvailability
from backend.users.models import User, PatientProfile
from .serializers import DashboardStatsSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_dashboard_stats(request):
    """
    Get dashboard statistics for a doctor
    - Total appointments (today and upcoming)
    - Patients in queue (normal and priority)
    - Notifications (unread messages from patients, nurses, other doctors)
    - Pending assessments (nurse charts awaiting doctor review)
    """
    try:
        # Get the current doctor
        doctor = request.user
        
        # Get today's date
        today = timezone.now().date()
        
        # 1. Total Appointments (today and upcoming)
        total_appointments = AppointmentManagement.objects.filter(
            doctor__user=doctor,
            appointment_date__date__gte=today,
            status__in=['scheduled', 'in_progress']
        ).count()
        
        # 2. Patients in Queue (normal and priority)
        # Normal queue - patients waiting in OPD
        normal_queue = QueueManagement.objects.filter(
            department='OPD',
            status='waiting'
        ).count()
        
        # Priority queue - patients with special needs
        priority_queue = PriorityQueue.objects.filter(
            department='OPD'
        ).count()
        
        total_patients = normal_queue + priority_queue
        
        # 3. Notifications (unread messages from patients, nurses, other doctors)
        notifications = Notification.objects.filter(
            user=doctor,
            is_read=False
        ).count()
        
        # 4. Pending Assessments (nurse charts awaiting doctor review)
        # For now, set to 0 since NurseChart model is not implemented yet
        pending_assessment = 0
        # Prepare response data
        stats_data = {
            'total_appointments': total_appointments,
            'total_patients': total_patients,
            'normal_queue': normal_queue,
            'priority_queue': priority_queue,
            'notifications': notifications,
            'pending_assessment': 0
        }
        
        serializer = DashboardStatsSerializer(stats_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch dashboard statistics: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_appointments(request):
    """
    Get appointments for the current doctor
    """
    try:
        doctor = request.user
        today = timezone.now().date()
        
        appointments = AppointmentManagement.objects.filter(
            doctor__user=doctor,
            appointment_date__date__gte=today
        ).order_by('appointment_date')
        
        from .serializers import AppointmentSerializer
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch appointments: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_queue_patients(request):
    """
    Get patients in queue for the current doctor
    """
    try:
        # Get normal queue patients
        normal_queue = QueueManagement.objects.filter(
            department='OPD',
            status='waiting'
        ).order_by('position_in_queue')
        
        # Get priority queue patients
        priority_queue = PriorityQueue.objects.filter(
            department='OPD'
        ).order_by('priority_position')
        
        from .serializers import QueueSerializer, PriorityQueueSerializer
        
        normal_serializer = QueueSerializer(normal_queue, many=True)
        priority_serializer = PriorityQueueSerializer(priority_queue, many=True)
        
        return Response({
            'normal_queue': normal_serializer.data,
            'priority_queue': priority_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch queue patients: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_notifications(request):
    """
    Get notifications for the current doctor
    """
    try:
        doctor = request.user
        
        notifications = Notification.objects.filter(
            user=doctor
        ).order_by('-created_at')[:10]  # Get last 10 notifications
        
        from .serializers import NotificationSerializer
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch notifications: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_pending_assessments(request):
    """
    Get pending nurse charts for the current doctor
    """
    try:
        doctor = request.user
        
        # For now, return empty list since NurseChart model is not implemented yet
        # In the future, this would fetch pending nurse charts
        return Response([], status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch pending assessments: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_blocked_dates(request):
    """
    Get blocked dates for the current doctor
    """
    try:
        doctor = request.user

        # Safely resolve the doctor's profile; return empty list if none exists
        from backend.users.models import GeneralDoctorProfile
        doctor_profile = GeneralDoctorProfile.objects.filter(user=doctor).first()
        if not doctor_profile:
            return Response([], status=status.HTTP_200_OK)
        
        blocked_dates = DoctorAvailability.objects.filter(
            doctor=doctor_profile,
            is_blocked=True
        ).values_list('date', flat=True)
        
        return Response(list(blocked_dates), status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to fetch blocked dates: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def doctor_block_date(request):
    """
    Block a date for the current doctor
    """
    try:
        doctor = request.user
        date = request.data.get('date')
        reason = request.data.get('reason', '')
        
        if not date:
            return Response({
                'error': 'Date is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Resolve the doctor's profile safely
        from backend.users.models import GeneralDoctorProfile
        doctor_profile = GeneralDoctorProfile.objects.filter(user=doctor).first()
        if not doctor_profile:
            return Response({
                'error': 'Doctor profile not found for this user.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if date is already blocked
        existing_block = DoctorAvailability.objects.filter(
            doctor=doctor_profile,
            date=date
        ).first()
        
        if existing_block:
            return Response({
                'error': 'Date is already blocked'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new blocked date
        DoctorAvailability.objects.create(
            doctor=doctor_profile,
            date=date,
            reason=reason,
            is_blocked=True
        )
        
        return Response({
            'message': 'Date blocked successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Failed to block date: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def doctor_create_appointment(request):
    """
    Create a new appointment for the current doctor
    """
    try:
        doctor = request.user
        
        # Get patient by name (in a real app, you'd have patient selection)
        patient_name = request.data.get('patient_name')
        appointment_date = request.data.get('appointment_date')
        appointment_type = request.data.get('appointment_type', 'consultation')
        notes = request.data.get('notes', '')
        
        if not all([patient_name, appointment_date]):
            return Response({
                'error': 'Patient name and appointment date are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # For now, create a mock patient or find existing one
        # In a real app, you'd have proper patient selection
        from backend.users.models import PatientProfile
        
        # Try to find existing patient or create a placeholder
        patient_profile = PatientProfile.objects.filter(
            user__full_name__icontains=patient_name
        ).first()
        
        if not patient_profile:
            return Response({
                'error': 'Patient not found. Please ensure the patient is registered.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create appointment
        appointment = AppointmentManagement.objects.create(
            patient=patient_profile,
            doctor=doctor.doctor_profile,
            appointment_date=appointment_date,
            appointment_type=appointment_type,
            status='scheduled'
        )
        
        return Response({
            'message': 'Appointment created successfully',
            'appointment_id': appointment.appointment_id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Failed to create appointment: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ==================== PATIENT QUEUE MANAGEMENT SYSTEM ====================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def patient_check_in(request):
    """
    Patient online check-in form.
    Allows patients to check in and join the queue.
    """
    try:
        patient = request.user
        
        # Verify user is a patient
        if patient.role != 'patient':
            return Response({
                'error': 'Only patients can check in'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get patient profile
        try:
            patient_profile = patient.patient_profile
        except PatientProfile.DoesNotExist:
            return Response({
                'error': 'Patient profile not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        department = request.data.get('department', 'OPD')
        appointment_id = request.data.get('appointment_id')
        priority_level = request.data.get('priority_level')
        
        # Check if patient is already in queue
        existing_queue = QueueManagement.objects.filter(
            patient=patient_profile,
            department=department,
            status__in=['waiting', 'in_progress']
        ).first()
        
        if existing_queue:
            return Response({
                'error': 'Patient is already in queue',
                'queue_number': existing_queue.queue_number,
                'position': existing_queue.position_in_queue
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create queue entry
        queue_entry = QueueManagement.objects.create(
            patient=patient_profile,
            department=department,
            status='waiting'
        )
        
        # Create notification for patient
        Notification.objects.create(
            user=patient,
            message=f"You have been added to the {department} queue. Your queue number is {queue_entry.queue_number}."
        )
        
        return Response({
            'message': 'Successfully checked in',
            'queue_number': queue_entry.queue_number,
            'position': queue_entry.position_in_queue,
            'estimated_wait_time': str(queue_entry.get_estimated_wait_time()) if queue_entry.get_estimated_wait_time() else None
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Failed to check in: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_queue_status(request):
    """
    Get patient's current queue status and estimated wait time.
    """
    try:
        patient = request.user
        
        if patient.role != 'patient':
            return Response({
                'error': 'Only patients can view queue status'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            patient_profile = patient.patient_profile
        except PatientProfile.DoesNotExist:
            return Response({
                'error': 'Patient profile not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get current queue entries for patient
        queue_entries = QueueManagement.objects.filter(
            patient=patient_profile,
            status__in=['waiting', 'in_progress']
        ).order_by('-created_at')
        
        if not queue_entries.exists():
            return Response({
                'message': 'No active queue entries found'
            }, status=status.HTTP_200_OK)
        
        queue_data = []
        for entry in queue_entries:
            estimated_wait = entry.get_estimated_wait_time()
            queue_data.append({
                'queue_number': entry.queue_number,
                'department': entry.department,
                'status': entry.status,
                'position': entry.position_in_queue,
                'estimated_wait_time': str(estimated_wait) if estimated_wait else None,
                'enqueue_time': entry.enqueue_time,
                'started_at': entry.started_at
            })
        
        return Response({
            'queues': queue_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to get queue status: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def public_queue_display(request):
    """
    Public queue display for patients to see current queue status.
    No authentication required.
    """
    try:
        department = request.GET.get('department', 'OPD')
        
        # Get current queue for department
        current_queue = QueueManagement.objects.filter(
            department=department,
            status__in=['waiting', 'in_progress']
        ).order_by('position_in_queue')[:10]  # Show next 10 patients
        
        queue_data = []
        for entry in current_queue:
            queue_data.append({
                'queue_number': entry.queue_number,
                'patient_name': entry.patient.user.full_name,
                'status': entry.status,
                'position': entry.position_in_queue,
                'estimated_wait_time': str(entry.get_estimated_wait_time()) if entry.get_estimated_wait_time() else None
            })
        
        return Response({
            'department': department,
            'current_queue': queue_data,
            'total_waiting': QueueManagement.objects.filter(
                department=department,
                status='waiting'
            ).count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to get queue display: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ==================== STAFF QUEUE MANAGEMENT ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_queue_dashboard(request):
    """
    Staff dashboard for queue management.
    Access restricted to nurses and doctors.
    """
    try:
        user = request.user
        
        # Check if user is staff (nurse or doctor)
        if user.role not in ['nurse', 'doctor']:
            return Response({
                'error': 'Access denied. Only staff members can access this dashboard.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        department = request.GET.get('department', 'OPD')
        
        # Get all queues for the department
        normal_queue = QueueManagement.objects.filter(
            department=department,
            status__in=['waiting', 'in_progress']
        ).order_by('position_in_queue')
        
        priority_queue = PriorityQueue.objects.filter(
            department=department
        ).order_by('priority_position')
        
        # Get statistics
        stats = {
            'total_waiting': QueueManagement.objects.filter(
                department=department,
                status='waiting'
            ).count(),
            'total_in_progress': QueueManagement.objects.filter(
                department=department,
                status='in_progress'
            ).count(),
            'total_completed_today': QueueManagement.objects.filter(
                department=department,
                status='completed',
                finished_at__date=timezone.now().date()
            ).count()
        }
        
        return Response({
            'department': department,
            'normal_queue': [
                {
                    'id': q.id,
                    'queue_number': q.queue_number,
                    'patient_name': q.patient.user.full_name,
                    'status': q.status,
                    'position': q.position_in_queue,
                    'enqueue_time': q.enqueue_time,
                    'estimated_wait_time': str(q.get_estimated_wait_time()) if q.get_estimated_wait_time() else None
                } for q in normal_queue
            ],
            'priority_queue': [
                {
                    'id': q.id,
                    'queue_number': q.queue_number,
                    'patient_name': q.patient.user.full_name,
                    'priority_level': q.priority_level,
                    'position': q.priority_position
                } for q in priority_queue
            ],
            'stats': stats
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to get staff dashboard: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def call_next_patient(request):
    """
    Call the next patient in the queue.
    Only accessible by staff.
    """
    try:
        user = request.user
        
        if user.role not in ['nurse', 'doctor']:
            return Response({
                'error': 'Access denied. Only staff members can call patients.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        department = request.data.get('department', 'OPD')
        
        # Get next patient in queue
        next_patient = QueueManagement.objects.filter(
            department=department,
            status='waiting'
        ).order_by('position_in_queue').first()
        
        if not next_patient:
            return Response({
                'error': 'No patients waiting in queue'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Mark patient as in progress
        next_patient.start_service()
        
        # Create notification for patient
        Notification.objects.create(
            user=next_patient.patient.user,
            message=f"Your turn is up! Please proceed to the {department} counter. Queue number: {next_patient.queue_number}"
        )
        
        return Response({
            'message': 'Patient called successfully',
            'patient_name': next_patient.patient.user.full_name,
            'queue_number': next_patient.queue_number,
            'position': next_patient.position_in_queue
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to call next patient: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_patient_service(request):
    """
    Mark a patient's service as completed.
    Only accessible by staff.
    """
    try:
        user = request.user
        
        if user.role not in ['nurse', 'doctor']:
            return Response({
                'error': 'Access denied. Only staff members can complete services.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        queue_id = request.data.get('queue_id')
        
        if not queue_id:
            return Response({
                'error': 'Queue ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queue_entry = QueueManagement.objects.get(id=queue_id)
        except QueueManagement.DoesNotExist:
            return Response({
                'error': 'Queue entry not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Complete the service
        queue_entry.complete_service()
        
        # Create notification for patient
        Notification.objects.create(
            user=queue_entry.patient.user,
            message=f"Your service at {queue_entry.department} has been completed. Thank you!"
        )
        
        return Response({
            'message': 'Service completed successfully',
            'patient_name': queue_entry.patient.user.full_name,
            'queue_number': queue_entry.queue_number
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to complete service: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_patient_from_queue(request):
    """
    Remove a patient from the queue.
    Only accessible by staff.
    """
    try:
        user = request.user
        
        if user.role not in ['nurse', 'doctor']:
            return Response({
                'error': 'Access denied. Only staff members can remove patients.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        queue_id = request.data.get('queue_id')
        reason = request.data.get('reason', 'Removed by staff')
        
        if not queue_id:
            return Response({
                'error': 'Queue ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queue_entry = QueueManagement.objects.get(id=queue_id)
        except QueueManagement.DoesNotExist:
            return Response({
                'error': 'Queue entry not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Mark as cancelled
        queue_entry.status = 'cancelled'
        queue_entry.dequeue_time = timezone.now()
        queue_entry.save()
        
        # Update queue positions
        queue_entry.update_queue_positions()
        
        # Create notification for patient
        Notification.objects.create(
            user=queue_entry.patient.user,
            message=f"You have been removed from the {queue_entry.department} queue. Reason: {reason}"
        )
        
        return Response({
            'message': 'Patient removed from queue successfully',
            'patient_name': queue_entry.patient.user.full_name,
            'queue_number': queue_entry.queue_number
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Failed to remove patient: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)