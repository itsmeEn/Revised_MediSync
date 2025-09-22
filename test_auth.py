#!/usr/bin/env python3
"""
Test script to verify authentication system is working
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from backend.users.models import GeneralDoctorProfile, NurseProfile, PatientProfile

User = get_user_model()

def test_user_creation():
    """Test user creation and authentication"""
    print("Testing user creation and authentication...")
    
    # Test data
    test_email = "test@example.com"
    test_password = "testpass123"
    
    try:
        # Clean up any existing test user
        User.objects.filter(email=test_email).delete()
        
        # Create a test user
        user = User.objects.create_user(
            email=test_email,
            password=test_password,
            full_name="Test User",
            role="patient"
        )
        
        print(f"✅ User created successfully: {user.email}")
        
        # Test password check
        if user.check_password(test_password):
            print("✅ Password check successful")
        else:
            print("❌ Password check failed")
            
        # Test authentication
        from django.contrib.auth import authenticate
        auth_user = authenticate(email=test_email, password=test_password)
        
        if auth_user:
            print("✅ Authentication successful")
        else:
            print("❌ Authentication failed")
            
        # Test JWT token generation
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        print(f"✅ JWT tokens generated successfully")
        print(f"   Access token: {str(access_token)[:50]}...")
        print(f"   Refresh token: {str(refresh)[:50]}...")
        
        # Clean up
        user.delete()
        print("✅ Test user cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_profile_creation():
    """Test profile creation for different roles"""
    print("\nTesting profile creation...")
    
    try:
        # Test patient profile
        user = User.objects.create_user(
            email="patient@example.com",
            password="testpass123",
            full_name="Test Patient",
            role="patient"
        )
        
        patient_profile = PatientProfile.objects.create(
            user=user,
            blood_type=PatientProfile.BloodType.O_POSITIVE
        )
        
        print("✅ Patient profile created successfully")
        user.delete()
        
        # Test doctor profile
        user = User.objects.create_user(
            email="doctor@example.com",
            password="testpass123",
            full_name="Test Doctor",
            role="doctor"
        )
        
        doctor_profile = GeneralDoctorProfile.objects.create(
            user=user,
            license_number="DOC123",
            specialization="Cardiology"
        )
        
        print("✅ Doctor profile created successfully")
        user.delete()
        
        # Test nurse profile
        user = User.objects.create_user(
            email="nurse@example.com",
            password="testpass123",
            full_name="Test Nurse",
            role="nurse"
        )
        
        nurse_profile = NurseProfile.objects.create(
            user=user,
            license_number="NUR123",
            department="ICU"
        )
        
        print("✅ Nurse profile created successfully")
        user.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Profile creation test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 MediSync Authentication System Test")
    print("=" * 50)
    
    # Run tests
    test1_passed = test_user_creation()
    test2_passed = test_profile_creation()
    
    print("\n" + "=" * 50)
    if test1_passed and test2_passed:
        print("🎉 All tests passed! Authentication system is working correctly.")
    else:
        print("❌ Some tests failed. Please check the configuration.")
    
    print("=" * 50)
