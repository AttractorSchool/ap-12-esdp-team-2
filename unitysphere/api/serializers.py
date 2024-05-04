from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'password']

    def validate_password(self, value):
        validate_password(value)
        return value


class UserVerifySerializer(serializers.Serializer):
    user_session_id = serializers.UUIDField()
    sms_code = serializers.CharField()
