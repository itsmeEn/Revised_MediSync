from rest_framework import serializers
from .models import User, GeneralDoctorProfile, NurseProfile, PatientProfile
from django.utils import timezone


class GeneralDoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralDoctorProfile
        fields = "__all__"


class NurseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseProfile
        fields = "__all__"


class PatientProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        return (timezone.now().date() - obj.date_of_birth).days // 365

    class Meta:
        model = PatientProfile
        fields = "__all__"
        read_only_fields = ["user"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for general User details."""
    doctor_profile = GeneralDoctorProfileSerializer(read_only=True)
    nurse_profile = NurseProfileSerializer(read_only=True)
    patient_profile = PatientProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "role", "date_of_birth", "gender",
            "is_verified", "doctor_profile", "nurse_profile", "patient_profile",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "full_name", "role", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        # You can add logic here to create the appropriate profile based on the role
        return user
