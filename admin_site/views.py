from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import os

from .models import AdminUser, VerificationRequest, SystemLog
from .serializers import (
    AdminUserSerializer, AdminLoginSerializer, VerificationRequestSerializer,
    VerificationRequestUpdateSerializer, DeclineVerificationSerializer, SystemLogSerializer
)
from .authentication import AdminJWTAuthentication


def log_admin_action(admin_user, action, target, target_id, details=""):
    """Helper function to log admin actions."""
    SystemLog.objects.create(
        admin_user=admin_user,
        action=action,
        target=target,
        target_id=target_id,
        details=details
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def admin_overview(request):
    """
    Admin API overview - provides information about available endpoints
    """
    return Response({
        'message': 'MediSync Admin API',
        'version': '1.0.0',
        'endpoints': {
            'login': '/api/admin/login/',
            'dashboard_stats': '/api/admin/dashboard/stats/',
            'verifications': '/api/admin/verifications/',
            'system_logs': '/api/admin/logs/',
        },
        'description': 'Administrative interface for managing user verifications and system operations'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """
    Admin login endpoint
    """
    serializer = AdminLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user and isinstance(user, AdminUser):
            if not user.is_active:
                return Response({
                    'error': 'Account is deactivated.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'admin_user': AdminUserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials.',
                'message': 'Email or password is incorrect.'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_token_refresh(request):
    """
    Admin token refresh endpoint
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'error': 'Refresh token is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Decode and verify the refresh token
        refresh = RefreshToken(refresh_token)
        
        # Get the user from the token
        user_id = refresh.payload.get('user_id')
        try:
            user = AdminUser.objects.get(id=user_id)
        except AdminUser.DoesNotExist:
            return Response({
                'error': 'Invalid refresh token.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate new access token
        new_access_token = refresh.access_token
        
        return Response({
            'access': str(new_access_token),
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Invalid refresh token.'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
def admin_dashboard_stats(request):
    """
    Get dashboard statistics
    """
    if not isinstance(request.user, AdminUser):
        return Response({
            'error': 'Access denied. Admin privileges required.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    stats = {
        'pending': VerificationRequest.objects.filter(status='pending').count(),
        'approved': VerificationRequest.objects.filter(status='approved').count(),
        'declined': VerificationRequest.objects.filter(status='declined').count(),
        'archived': VerificationRequest.objects.filter(status='archived').count(),
        'total': VerificationRequest.objects.count(),
    }
    
    return Response(stats, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
def verification_requests_list(request):
    """
    Get all verification requests with filtering
    """
    if not isinstance(request.user, AdminUser):
        return Response({
            'error': 'Access denied. Admin privileges required.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Get query parameters for filtering
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    queryset = VerificationRequest.objects.all()
    
    # Filter by status
    if status_filter and status_filter != 'all':
        queryset = queryset.filter(status=status_filter)
    
    # Filter by search query
    if search_query:
        queryset = queryset.filter(
            models.Q(user_full_name__icontains=search_query) |
            models.Q(user_email__icontains=search_query)
        )
    
    # Order by submitted date (newest first)
    queryset = queryset.order_by('-submitted_at')
    
    serializer = VerificationRequestSerializer(queryset, many=True)
    
    return Response({
        'verifications': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
def accept_verification(request, verification_id):
    """
    Accept a verification request
    """
    if not isinstance(request.user, AdminUser):
        return Response({
            'error': 'Access denied. Admin privileges required.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        verification = VerificationRequest.objects.get(id=verification_id)
        verification.approve(request.user)
        
        # Log the action
        log_admin_action(
            request.user, 
            'approve_verification', 
            'verification_request', 
            verification_id,
            f"Approved verification for {verification.user_email}"
        )
        
        # Send email notification to user
        try:
            subject = 'Verification Approved - MediSync'
            message = f"""
            Dear {verification.user_full_name},
            
            Your verification request has been approved! You can now access all features of your MediSync account.
            
            Thank you for your patience.
            
            Best regards,
            MediSync Admin Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [verification.user_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send approval email: {e}")
        
        return Response({
            'message': 'Verification approved successfully'
        }, status=status.HTTP_200_OK)
        
    except VerificationRequest.DoesNotExist:
        return Response({
            'error': 'Verification request not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
def decline_verification(request, verification_id):
    """
    Decline a verification request
    """
    if not isinstance(request.user, AdminUser):
        return Response({
            'error': 'Access denied. Admin privileges required.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = DeclineVerificationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    reason = serializer.validated_data['reason']
    send_email = serializer.validated_data['send_email']
    
    try:
        verification = VerificationRequest.objects.get(id=verification_id)
        verification.decline(request.user, reason)
        
        # Log the action
        log_admin_action(
            request.user, 
            'decline_verification', 
            'verification_request', 
            verification_id,
            f"Declined verification for {verification.user_email}. Reason: {reason}"
        )
        
        # Send email notification to user if requested
        if send_email:
            try:
                subject = 'Verification Declined - MediSync'
                message = f"""
                Dear {verification.user_full_name},
                
                Your verification request has been declined for the following reason:
                
                {reason}
                
                Please review the requirements and submit a new verification request with the correct documentation.
                
                If you have any questions, please contact our support team.
                
                Best regards,
                MediSync Admin Team
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [verification.user_email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send decline email: {e}")
        
        return Response({
            'message': 'Verification declined successfully'
        }, status=status.HTTP_200_OK)
        
    except VerificationRequest.DoesNotExist:
        return Response({
            'error': 'Verification request not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
def archive_verification(request, verification_id):
    """
    Archive a verification request
    """
    if not isinstance(request.user, AdminUser):
        return Response({
            'error': 'Access denied. Admin privileges required.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        verification = VerificationRequest.objects.get(id=verification_id)
        verification.archive(request.user)
        
        # Log the action
        log_admin_action(
            request.user, 
            'archive_verification', 
            'verification_request', 
            verification_id,
            f"Archived verification for {verification.user_email}"
        )
        
        return Response({
            'message': 'Verification archived successfully'
        }, status=status.HTTP_200_OK)
        
    except VerificationRequest.DoesNotExist:
        return Response({
            'error': 'Verification request not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
def update_verification(request, verification_id):
    """
    Update verification request details
    """
    if not isinstance(request.user, AdminUser):
        return Response({
            'error': 'Access denied. Admin privileges required.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        verification = VerificationRequest.objects.get(id=verification_id)
        serializer = VerificationRequestUpdateSerializer(verification, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # Log the action
            log_admin_action(
                request.user, 
                'update_verification', 
                'verification_request', 
                verification_id,
                f"Updated verification for {verification.user_email}"
            )
            
            return Response({
                'message': 'Verification updated successfully',
                'verification': VerificationRequestSerializer(verification).data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except VerificationRequest.DoesNotExist:
        return Response({
            'error': 'Verification request not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
def system_logs(request):
    """
    Get system logs for audit purposes
    """
    if not isinstance(request.user, AdminUser):
        return Response({
            'error': 'Access denied. Admin privileges required.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Only super admins can view logs
    if not request.user.is_super_admin:
        return Response({
            'error': 'Access denied. Super admin privileges required.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    logs = SystemLog.objects.all()[:100]  # Limit to last 100 logs
    serializer = SystemLogSerializer(logs, many=True)
    
    return Response({
        'logs': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([AdminJWTAuthentication])
@permission_classes([IsAuthenticated])
def serve_verification_document(request, verification_id):
    """
    Serve verification document with appropriate headers for iframe embedding
    """
    verification = get_object_or_404(VerificationRequest, id=verification_id)
    
    if not verification.verification_document:
        raise Http404("Document not found")
    
    # Get the file path
    file_path = verification.verification_document.path
    
    if not os.path.exists(file_path):
        raise Http404("File not found on disk")
    
    # Open and serve the file with appropriate headers
    file_handle = open(file_path, 'rb')
    response = FileResponse(file_handle, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    
    # Allow iframe embedding
    response['X-Frame-Options'] = 'ALLOWALL'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    response['Access-Control-Allow-Headers'] = '*'
    
    return response
