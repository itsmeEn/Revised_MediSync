import asyncio
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import threading
from concurrent.futures import ThreadPoolExecutor

# PDF generation imports
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

from .models import AnalyticsResult, AnalyticsTask, DataUpdateLog, AnalyticsCache
from .serializers import (
    AnalyticsResultSerializer, AnalyticsTaskSerializer, 
    AnalyticsRequestSerializer, AnalyticsResponseSerializer
)
from .tasks import run_analytics_task_async
from backend.users.models import PatientProfile

class AnalyticsView(APIView):
    """
    Main analytics API endpoint for triggering and retrieving analytics
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get analytics results"""
        analysis_type = request.query_params.get('type', 'full_analysis')
        force_refresh = request.query_params.get('force_refresh', 'false').lower() == 'true'
        
        # Check cache first
        cache_key = f"analytics_{analysis_type}_{request.user.id}"
        if not force_refresh:
            cached_result = cache.get(cache_key)
            if cached_result:
                return Response({
                    'success': True,
                    'message': 'Analytics results retrieved from cache',
                    'data': cached_result,
                    'cached': True
                })
        
        # Get latest result from database
        try:
            latest_result = AnalyticsResult.objects.filter(
                analysis_type=analysis_type,
                status='completed'
            ).order_by('-created_at').first()
            
            if latest_result:
                serializer = AnalyticsResultSerializer(latest_result)
                # Cache the result for 1 hour
                cache.set(cache_key, serializer.data, 3600)
                
                return Response({
                    'success': True,
                    'message': 'Analytics results retrieved',
                    'data': serializer.data,
                    'cached': False
                })
            else:
                return Response({
                    'success': False,
                    'message': 'No analytics results found. Please trigger an analysis first.',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error retrieving analytics: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Trigger new analytics analysis"""
        serializer = AnalyticsRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request parameters',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        analysis_type = serializer.validated_data['analysis_type']
        force_refresh = serializer.validated_data['force_refresh']
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        try:
            # Create analytics task
            task = AnalyticsTask.objects.create(
                task_id=task_id,
                analysis_type=analysis_type,
                status='pending'
            )
            
            # Start async analytics processing
            run_analytics_task_async.delay(task_id, analysis_type)
            
            return Response({
                'success': True,
                'message': 'Analytics task started',
                'task_id': task_id,
                'data': {
                    'task_id': task_id,
                    'analysis_type': analysis_type,
                    'status': 'pending'
                }
            }, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error starting analytics task: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analytics_status(request, task_id):
    """Get the status of a specific analytics task"""
    try:
        task = AnalyticsTask.objects.get(task_id=task_id)
        serializer = AnalyticsTaskSerializer(task)
        
        return Response({
            'success': True,
            'message': 'Task status retrieved',
            'data': serializer.data
        })
        
    except AnalyticsTask.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Task not found',
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error retrieving task status: {str(e)}',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analytics_history(request):
    """Get analytics history"""
    analysis_type = request.query_params.get('type')
    limit = int(request.query_params.get('limit', 10))
    
    queryset = AnalyticsResult.objects.all()
    if analysis_type:
        queryset = queryset.filter(analysis_type=analysis_type)
    
    queryset = queryset.order_by('-created_at')[:limit]
    serializer = AnalyticsResultSerializer(queryset, many=True)
    
    return Response({
        'success': True,
        'message': 'Analytics history retrieved',
        'data': serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_data_refresh(request):
    """Manually trigger analytics refresh for new data"""
    try:
        # This would typically be called when new data is added
        # For now, we'll trigger a full analysis
        task_id = str(uuid.uuid4())
        
        task = AnalyticsTask.objects.create(
            task_id=task_id,
            analysis_type='full_analysis',
            status='pending'
        )
        
        # Start async processing
        run_analytics_task_async.delay(task_id, 'full_analysis')
        
        return Response({
            'success': True,
            'message': 'Data refresh triggered',
            'task_id': task_id
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error triggering refresh: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_real_time_analytics(request):
    """Get real-time analytics dashboard data"""
    try:
        # Get latest results for different analysis types
        dashboard_data = {}
        
        analysis_types = [
            'patient_health_trends',
            'patient_demographics', 
            'illness_prediction',
            'medication_analysis',
            'patient_volume_prediction'
        ]
        
        for analysis_type in analysis_types:
            latest_result = AnalyticsResult.objects.filter(
                analysis_type=analysis_type,
                status='completed'
            ).order_by('-created_at').first()
            
            if latest_result:
                dashboard_data[analysis_type] = {
                    'status': 'completed',
                    'last_updated': latest_result.updated_at.isoformat(),
                    'data': latest_result.results
                }
            else:
                dashboard_data[analysis_type] = {
                    'status': 'no_data',
                    'last_updated': None,
                    'data': None
                }
        
        return Response({
            'success': True,
            'message': 'Real-time analytics data retrieved',
            'data': dashboard_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error retrieving real-time analytics: {str(e)}',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# WebSocket-like endpoint for real-time updates (using Server-Sent Events)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_stream(request):
    """Stream analytics updates in real-time"""
    import time
    
    def event_stream():
        while True:
            # Get latest analytics results
            latest_results = AnalyticsResult.objects.filter(
                status='completed'
            ).order_by('-updated_at')[:5]
            
            data = {
                'timestamp': timezone.now().isoformat(),
                'results': AnalyticsResultSerializer(latest_results, many=True).data
            }
            
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(5)  # Update every 5 seconds
    
    from django.http import StreamingHttpResponse
    response = StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    return response

# Doctor Analytics Endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_analytics(request):
    """
    Get analytics specifically for doctors
    """
    if request.user.role != 'doctor':
        return Response({
            'error': 'Only doctors can access this endpoint.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get doctor-specific analytics
        analytics_data = {}
        
        # Patient demographics for doctor's patients
        patient_demographics = AnalyticsResult.objects.filter(
            analysis_type='patient_demographics',
            status='completed'
        ).order_by('-created_at').first()
        
        # Illness prediction for doctor's specialty
        illness_prediction = AnalyticsResult.objects.filter(
            analysis_type='illness_prediction',
            status='completed'
        ).order_by('-created_at').first()
        
        # Patient health trends
        health_trends = AnalyticsResult.objects.filter(
            analysis_type='patient_health_trends',
            status='completed'
        ).order_by('-created_at').first()
        
        # Illness surge prediction
        surge_prediction = AnalyticsResult.objects.filter(
            analysis_type='illness_surge_prediction',
            status='completed'
        ).order_by('-created_at').first()
        
        analytics_data = {
            'patient_demographics': patient_demographics.results if patient_demographics else None,
            'illness_prediction': illness_prediction.results if illness_prediction else None,
            'health_trends': health_trends.results if health_trends else None,
            'surge_prediction': surge_prediction.results if surge_prediction else None,
            'doctor_name': request.user.full_name,
            'specialization': getattr(request.user.doctor_profile, 'specialization', 'General Practice') if hasattr(request.user, 'doctor_profile') else 'General Practice',
            'generated_at': timezone.now().isoformat()
        }
        
        return Response({
            'success': True,
            'message': 'Doctor analytics retrieved successfully',
            'data': analytics_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error retrieving doctor analytics: {str(e)}',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nurse_analytics(request):
    """
    Get analytics specifically for nurses
    """
    if request.user.role != 'nurse':
        return Response({
            'error': 'Only nurses can access this endpoint.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Get nurse-specific analytics
        analytics_data = {}
        
        # Medication analysis
        medication_analysis = AnalyticsResult.objects.filter(
            analysis_type='medication_analysis',
            status='completed'
        ).order_by('-created_at').first()
        
        # Patient demographics
        patient_demographics = AnalyticsResult.objects.filter(
            analysis_type='patient_demographics',
            status='completed'
        ).order_by('-created_at').first()
        
        # Patient health trends
        health_trends = AnalyticsResult.objects.filter(
            analysis_type='patient_health_trends',
            status='completed'
        ).order_by('-created_at').first()
        
        # Patient volume prediction
        volume_prediction = AnalyticsResult.objects.filter(
            analysis_type='patient_volume_prediction',
            status='completed'
        ).order_by('-created_at').first()
        
        analytics_data = {
            'medication_analysis': medication_analysis.results if medication_analysis else None,
            'patient_demographics': patient_demographics.results if patient_demographics else None,
            'health_trends': health_trends.results if health_trends else None,
            'volume_prediction': volume_prediction.results if volume_prediction else None,
            'nurse_name': request.user.full_name,
            'department': getattr(request.user.nurse_profile, 'department', 'General') if hasattr(request.user, 'nurse_profile') else 'General',
            'generated_at': timezone.now().isoformat()
        }
        
        return Response({
            'success': True,
            'message': 'Nurse analytics retrieved successfully',
            'data': analytics_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error retrieving nurse analytics: {str(e)}',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_analytics_pdf(request):
    """
    Generate PDF report of analytics findings
    """
    if not PDF_AVAILABLE:
        return Response({
            'error': 'PDF generation not available. Please install reportlab.'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    user_role = request.user.role
    report_type = request.GET.get('type', 'full')  # full, doctor, nurse
    
    try:
        # Get analytics data based on user role
        if user_role == 'doctor' or report_type == 'doctor':
            analytics_data = get_doctor_analytics_data(request.user)
            title = f"Doctor Analytics Report - {request.user.full_name}"
        elif user_role == 'nurse' or report_type == 'nurse':
            analytics_data = get_nurse_analytics_data(request.user)
            title = f"Nurse Analytics Report - {request.user.full_name}"
        else:
            analytics_data = get_full_analytics_data()
            title = "MediSync Analytics Report"
        
        # Generate PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="analytics_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 20))
        
        # Report metadata
        meta_style = ParagraphStyle(
            'Meta',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_RIGHT,
            textColor=colors.grey
        )
        story.append(Paragraph(f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
        story.append(Spacer(1, 30))
        
        # Add analytics sections
        add_analytics_sections(story, analytics_data, styles)
        
        doc.build(story)
        return response
        
    except Exception as e:
        return Response({
            'error': f'Error generating PDF report: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_doctor_analytics_data(user):
    """Get analytics data for doctors"""
    return {
        'patient_demographics': get_latest_analytics('patient_demographics'),
        'illness_prediction': get_latest_analytics('illness_prediction'),
        'health_trends': get_latest_analytics('patient_health_trends'),
        'surge_prediction': get_latest_analytics('illness_surge_prediction'),
        'doctor_name': user.full_name,
        'specialization': getattr(user.doctor_profile, 'specialization', 'General Practice') if hasattr(user, 'doctor_profile') else 'General Practice'
    }

def get_nurse_analytics_data(user):
    """Get analytics data for nurses"""
    return {
        'medication_analysis': get_latest_analytics('medication_analysis'),
        'patient_demographics': get_latest_analytics('patient_demographics'),
        'health_trends': get_latest_analytics('patient_health_trends'),
        'volume_prediction': get_latest_analytics('patient_volume_prediction'),
        'nurse_name': user.full_name,
        'department': getattr(user.nurse_profile, 'department', 'General') if hasattr(user, 'nurse_profile') else 'General'
    }

def get_full_analytics_data():
    """Get all analytics data"""
    return {
        'patient_demographics': get_latest_analytics('patient_demographics'),
        'illness_prediction': get_latest_analytics('illness_prediction'),
        'medication_analysis': get_latest_analytics('medication_analysis'),
        'health_trends': get_latest_analytics('patient_health_trends'),
        'volume_prediction': get_latest_analytics('patient_volume_prediction'),
        'surge_prediction': get_latest_analytics('illness_surge_prediction')
    }

def get_latest_analytics(analysis_type):
    """Get latest analytics result for a specific type"""
    result = AnalyticsResult.objects.filter(
        analysis_type=analysis_type,
        status='completed'
    ).order_by('-created_at').first()
    return result.results if result else None

def add_analytics_sections(story, analytics_data, styles):
    """Add analytics sections to PDF"""
    
    # Section headers style
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    # Subsection style
    subsection_style = ParagraphStyle(
        'Subsection',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.darkgreen
    )
    
    # Content style
    content_style = ParagraphStyle(
        'Content',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # 1. Patient Demographics
    if analytics_data.get('patient_demographics'):
        story.append(Paragraph("1. Patient Demographics", section_style))
        demographics = analytics_data['patient_demographics']
        
        if 'age_distribution' in demographics:
            story.append(Paragraph("Age Distribution:", subsection_style))
            age_data = demographics['age_distribution']
            for age_group, count in age_data.items():
                story.append(Paragraph(f"• {age_group}: {count} patients", content_style))
            story.append(Spacer(1, 10))
        
        if 'gender_proportions' in demographics:
            story.append(Paragraph("Gender Distribution:", subsection_style))
            gender_data = demographics['gender_proportions']
            for gender, percentage in gender_data.items():
                story.append(Paragraph(f"• {gender}: {percentage}%", content_style))
            story.append(Spacer(1, 10))
    
    # 2. Health Trends
    if analytics_data.get('health_trends'):
        story.append(Paragraph("2. Patient Health Trends", section_style))
        trends = analytics_data['health_trends']
        
        if 'top_illnesses_by_week' in trends:
            story.append(Paragraph("Top Medical Conditions by Week:", subsection_style))
            for illness in trends['top_illnesses_by_week'][:5]:  # Top 5
                story.append(Paragraph(f"• {illness.get('medical_condition', 'N/A')}: {illness.get('count', 0)} cases", content_style))
            story.append(Spacer(1, 10))
    
    # 3. Medication Analysis
    if analytics_data.get('medication_analysis'):
        story.append(Paragraph("3. Medication Analysis", section_style))
        med_analysis = analytics_data['medication_analysis']
        
        if 'medication_pareto_data' in med_analysis:
            story.append(Paragraph("Most Prescribed Medications:", subsection_style))
            for med in med_analysis['medication_pareto_data'][:5]:  # Top 5
                story.append(Paragraph(f"• {med.get('medication', 'N/A')}: {med.get('frequency', 0)} prescriptions", content_style))
            story.append(Spacer(1, 10))
    
    # 4. Illness Prediction
    if analytics_data.get('illness_prediction'):
        story.append(Paragraph("4. Illness Prediction Analysis", section_style))
        prediction = analytics_data['illness_prediction']
        
        if 'association_result' in prediction:
            story.append(Paragraph(f"Statistical Analysis: {prediction['association_result']}", content_style))
        if 'chi_square_statistic' in prediction:
            story.append(Paragraph(f"Chi-Square Statistic: {prediction['chi_square_statistic']}", content_style))
        if 'p_value' in prediction:
            story.append(Paragraph(f"P-Value: {prediction['p_value']}", content_style))
        story.append(Spacer(1, 10))
    
    # 5. Volume Prediction
    if analytics_data.get('volume_prediction'):
        story.append(Paragraph("5. Patient Volume Prediction", section_style))
        volume = analytics_data['volume_prediction']
        
        if 'evaluation_metrics' in volume:
            metrics = volume['evaluation_metrics']
            story.append(Paragraph("Model Performance:", subsection_style))
            story.append(Paragraph(f"• Mean Absolute Error: {metrics.get('mae', 'N/A')}", content_style))
            story.append(Paragraph(f"• Root Mean Square Error: {metrics.get('rmse', 'N/A')}", content_style))
        story.append(Spacer(1, 10))
    
    # 6. Surge Prediction
    if analytics_data.get('surge_prediction'):
        story.append(Paragraph("6. Illness Surge Prediction", section_style))
        surge = analytics_data['surge_prediction']
        
        if 'forecasted_monthly_cases' in surge:
            story.append(Paragraph("Forecasted Cases for Next 6 Months:", subsection_style))
            for forecast in surge['forecasted_monthly_cases'][:3]:  # First 3 months
                story.append(Paragraph(f"• {forecast.get('date', 'N/A')}: {forecast.get('total_cases', 0)} cases", content_style))
        story.append(Spacer(1, 10))
    
    # Summary
    story.append(Paragraph("Summary", section_style))
    story.append(Paragraph(
        "This report provides comprehensive analytics insights for healthcare management. "
        "The data includes patient demographics, health trends, medication patterns, and predictive models "
        "to support evidence-based decision making and improve patient care outcomes.",
        content_style
    ))
