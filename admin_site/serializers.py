from rest_framework import serializers
from .models import AdminUser, VerificationRequest, SystemLog


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'email', 'full_name', 'is_super_admin', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class VerificationRequestSerializer(serializers.ModelSerializer):
    reviewed_by = AdminUserSerializer(read_only=True)
    
    class Meta:
        model = VerificationRequest
        fields = [
            'id', 'user_email', 'user_full_name', 'user_role', 'status',
            'verification_document', 'submitted_at', 'reviewed_at',
            'reviewed_by', 'decline_reason', 'notes'
        ]
        read_only_fields = ['id', 'submitted_at', 'reviewed_at', 'reviewed_by']


class VerificationRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRequest
        fields = ['status', 'decline_reason', 'notes']


class DeclineVerificationSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True)
    send_email = serializers.BooleanField(default=True)


class SystemLogSerializer(serializers.ModelSerializer):
    admin_user = AdminUserSerializer(read_only=True)
    
    class Meta:
        model = SystemLog
        fields = ['id', 'admin_user', 'action', 'target', 'target_id', 'details', 'timestamp']
        read_only_fields = ['id', 'timestamp']
