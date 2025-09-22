from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, GeneralDoctorProfile, NurseProfile, PatientProfile
from .serializers import UserSerializer, UserRegistrationSerializer, VerificationDocumentSerializer, ProfilePictureSerializer

# These classes are correctly defined and can be used as they are.
# They are included here for the sake of a complete, organized file.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain pair serializer to include user data in the response.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user'] = UserSerializer(user).data
        return token
    
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view.
    """
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Registers a new user and creates their associated profile.
    This single endpoint handles all user roles (doctor, nurse, patient).
    The serializer handles all validation logic.
    """
    print("Received data:", request.data)  # Add debug logging
    serializer = UserRegistrationSerializer(data=request.data)
    print("Serializer is valid:", serializer.is_valid())  # Add debug logging
    if serializer.is_valid():
        try:
            with transaction.atomic():
                print("Creating user...")  # Add debug logging
                # Create the user from validated data
                user = serializer.save()
                print("User created successfully:", user.email)  # Add debug logging
                
                # Create the appropriate profile based on the user's role
                if user.role == 'doctor':
                    print("Creating doctor profile...")  # Add debug logging
                    try:
                        GeneralDoctorProfile.objects.create(
                            user=user,
                            license_number=request.data.get('license_number', ''),
                            specialization=request.data.get('specialization', '')
                        )
                        print("Doctor profile created successfully")  # Add debug logging
                    except Exception as e:
                        print("Error creating doctor profile:", str(e))
                        raise e
                elif user.role == 'nurse':
                    try:
                        NurseProfile.objects.create(
                            user=user,
                            license_number=request.data.get('license_number', ''),
                            department=request.data.get('department', '')
                        )
                        print("Nurse profile created successfully")
                    except Exception as e:
                        print("Error creating nurse profile:", str(e))
                        raise e
                elif user.role == 'patient':
                    try:
                        PatientProfile.objects.create(
                            user=user,
                            blood_type=request.data.get('blood_type', PatientProfile.BloodType.UNKNOWN),
                            medical_condition=request.data.get('medical_condition', ''),
                            medication=request.data.get('medication', '')
                        )
                        print("Patient profile created successfully")
                    except Exception as e:
                        print("Error creating patient profile:", str(e))
                        raise e
                
                # Generate JWT tokens for the new user
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            print("Exception occurred:", str(e))  # Add debug logging
            print("Exception type:", type(e))  # Add debug logging
            return Response({
                'error': 'Registration failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Return validation errors if data is invalid
    print("Validation errors:", serializer.errors)  # Add debug logging
    print("Error details:", dict(serializer.errors))  # Add more detailed logging
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Logs in a user with email and password and returns JWT tokens.
    """
    print("Login attempt - Email:", request.data.get('email'))  # Add debug logging
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'error': 'Email and password are required.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Try to get user by email first
        try:
            user = User.objects.get(email=email)
            print("User found:", user.email, "Active:", user.is_active)  # Add debug logging
        except User.DoesNotExist:
            print("User not found with email:", email)  # Add debug logging
            return Response({
                'error': 'Invalid credentials.',
                'message': 'Email or password is incorrect. Please try again.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is active
        if not user.is_active:
            print("User is not active")  # Add debug logging
            return Response({'error': 'User account is not active.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check password
        if not user.check_password(password):
            print("Password check failed")  # Add debug logging
            return Response({
                'error': 'Invalid credentials.',
                'message': 'Email or password is incorrect. Please try again.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Create user data structure
        user_data = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role,
            'is_verified': user.is_verified
        }
        print("User data from serializer:", user_data)  # Add debug logging
        
        response_data = {
            'message': 'Login successful',
            'user': user_data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        print("Login response data:", response_data)  # Add debug logging
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print("Login error:", str(e))  # Add debug logging
        return Response({
            'error': 'Login failed.',
            'message': 'An error occurred during login. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_verification_document(request):
    """
    Upload verification document for user identity verification
    """
    serializer = VerificationDocumentSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Verification document uploaded successfully',
            'user': UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_now(request):
    """
    Submit verification request for admin review
    """
    user = request.user
    
    # Check if user already has a verification document
    if not user.verification_document:
        return Response({
            'error': 'Please upload a verification document first.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if verification request already exists
    from admin_site.models import VerificationRequest
    existing_request = VerificationRequest.objects.filter(
        user_email=user.email,
        status__in=['pending', 'approved']
    ).first()
    
    if existing_request:
        return Response({
            'error': 'Verification request already exists and is being processed.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create verification request
    verification_request = VerificationRequest.objects.create(
        user_email=user.email,
        user_full_name=user.full_name,
        user_role=user.role,
        verification_document=user.verification_document,
        status='pending'
    )
    
    return Response({
        'message': 'Verification request submitted successfully. Please wait for admin approval.',
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get current user's profile information
    """
    return Response({
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile_picture(request):
    """
    Update user's profile picture
    """
    serializer = ProfilePictureSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile picture updated successfully',
            'user': UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """
    Send password reset email to user
    """
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        if not user.is_active:
            return Response({
                'error': 'User account is not active.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset URL (for now, we'll use a simple approach)
        reset_url = f"http://localhost:9000/#/reset-password/{uid}/{token}"
        
        # Send password reset email
        subject = 'Password Reset Request - MediSync'
        message = f"""
        Hello {user.full_name},
        
        You have requested to reset your password for your MediSync account.
        
        Please click the following link to reset your password:
        {reset_url}
        
        If you did not request this password reset, please ignore this email.
        
        This link will expire in 24 hours.
        
        Best regards,
        MediSync Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # From email
                [user.email],  # To email
                fail_silently=False,
            )
            
            return Response({
                'message': 'Password reset link has been sent to your email.'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Email sending failed: {e}")
            return Response({
                'error': 'Failed to send password reset email. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except User.DoesNotExist:
        # Don't reveal if email exists or not for security
        return Response({
            'message': 'If an account with this email exists, a password reset link has been sent.'
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, uidb64, token):
    """
    Reset user password using token
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')
        
        if not new_password:
            return Response({
                'error': 'New password is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password
        if len(new_password) < 8:
            return Response({
                'error': 'Password must be at least 8 characters long.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if password contains alphanumeric characters
        if not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
            return Response({
                'error': 'Password must contain both letters and numbers.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password has been reset successfully.'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Invalid or expired reset link.'
        }, status=status.HTTP_400_BAD_REQUEST)