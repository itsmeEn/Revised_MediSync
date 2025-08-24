from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import AppointmentManagement, QueueManagement, PriorityQueue, Notification, Messaging, DoctorAvailability
from backend.users.models import User
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
        
        blocked_dates = DoctorAvailability.objects.filter(
            doctor=doctor.doctor_profile,
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
        
        # Check if date is already blocked
        existing_block = DoctorAvailability.objects.filter(
            doctor__user=doctor,
            date=date
        ).first()
        
        if existing_block:
            return Response({
                'error': 'Date is already blocked'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new blocked date
        DoctorAvailability.objects.create(
            doctor=doctor.doctor_profile,
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