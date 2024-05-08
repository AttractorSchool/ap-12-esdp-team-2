import uuid

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from accounts.models import User
from accounts.utils import generate_sms_code
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api import constants, exceptions, serializers
from .serializers import UserCreateSerializer


class UserCreateAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = uuid.uuid4()
        session_key = constants.USER_SESSION_KEY.format(session_id)
        sms_code = generate_sms_code(k=4)
        phone = serializer.validated_data['phone']

        user_data = {
            'phone': phone,
            'password': make_password(serializer.validated_data['password']),
        }

        data = {
            'user_data': user_data,
            'sms_code': sms_code,
        }
        cache.set(session_key, data, constants.USER_SESSION_KEY_TTL)
        return Response(
            {'session_id': session_id},
            status=status.HTTP_202_ACCEPTED,
        )


class UserVerifyAPIView(APIView):

    def post(self, request):
        serializer = serializers.UserVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_key = constants.USER_SESSION_KEY.format(serializer.validated_data['user_session_id'])
        session = cache.get(session_key)

        if session is None:
            raise exceptions.SMSCodeExpireException

        if session['sms_code'] != serializer.validated_data['sms_code']:
            raise exceptions.SMSCodeInvalidException

        user = User.objects.create(**session['user_data'])

        # access = AccessToken.for_user(user)
        # refresh = RefreshToken.for_user(user)
        #
        # return Response({
        #     'access': access,
        #     'refresh': refresh,
        # }, status=status.HTTP_201_CREATED)