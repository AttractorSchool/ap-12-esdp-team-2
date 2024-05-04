from django.core.cache import cache
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from . import serializers, constants, utils as api_utils
import uuid
from django.contrib.auth.hashers import make_password


class UserCreateAPIView(APIView):

    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = uuid.uuid4()
        session_key = constants.USER_SESSION_KEY.format(session_id)
        sms_code = api_utils.generate_sms_code(sms_code_len=4)
        user_data = {
            'phone': serializer.validated_data['phone'],
            'password': make_password(serializer.validated_data['password']),
        }
        data = {
            "user_data": user_data,
            "sms_code": sms_code,
        }
        cache.set(session_key, data, constants.USER_SESSION_KEY_TTL)
        return Response({'session_id': session_id}, status=status.HTTP_202_ACCEPTED)


class UserVerifyAPIView(APIView):

    def post(self, request):
        serializer = serializers.UserVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_key = constants.USER_SESSION_KEY.format(serializer.validated_data['user_session_id'])
        session = cache.get(session_key)
        if session is None:
            error_message = "Срок смс кода истек. Повторите регистрацию"
            return Response({'sms_code': [error_message,]}, status=status.HTTP_400_BAD_REQUEST)

        if session['sms_code'] != serializer.validated_data['sms_code']:
            error_message = "Не верный СМС код! Повторите ввод!"
            return Response({'sms_code': [error_message,]}, status=status.HTTP_400_BAD_REQUEST)

        user = User(**session['user_data'])
        user.is_superuser = True
        user.is_staff = True
        user.save()
        login(request, user)
        return Response({'message': 'User verified and logged in successfully'}, status=status.HTTP_200_OK)
