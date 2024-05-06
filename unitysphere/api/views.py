from django.core.cache import cache
from django.db import IntegrityError

from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from . import serializers, constants, utils as api_utils
from .serializers import UserCreateSerializer, UserLoginSerializer


class UserCreateAPIView(api_utils.UserAuthAPIViewMixin, APIView):
    serializer = UserCreateSerializer


class UserLoginAPIView(api_utils.UserAuthAPIViewMixin, APIView):
    serializer = UserLoginSerializer


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

        try:
            user = User.objects.create(**session['user_data'])
        except IntegrityError:
            user = User.objects.get(phone=session['user_data']['phone'])

        login(request, user)
        return Response({'message': 'User verified and logged in successfully'}, status=status.HTTP_200_OK)
