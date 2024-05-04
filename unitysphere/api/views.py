from django.core.cache import cache
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from django.contrib.auth.models import User
from . import serializers, constants, utils as api_utils
import uuid


class UserCreateAPIView(APIView):

    def post(self, request):
        print(request.data)
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = uuid.uuid4()
        session_key = constants.USER_SESSION_KEY.format(session_id)
        sms_code = api_utils.generate_sms_code(sms_code_len=4)
        data = {
            "user_data": serializer.validated_data,
            "sms_code": sms_code,
        }
        cache.set(session_key, data, constants.USER_SESSION_KEY_TTL)
        return Response({'session_id': session_id}, status=status.HTTP_202_ACCEPTED)


class UserVerifyAPIView(APIView):

    def post(self, request):
        serializer = serializers.UserVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_key = serializer.validated_data['user_session_id']
        session = cache.get(session_key)

        if session is None:
            error_message = "The SMS code has expired. Try again"
            return Response({'sms_verification_error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        if session['sms_code'] != serializer.validated_data['sms_code']:
            error_message = "Incorrect SMS code! Repeat the set!"
            return Response({'sms_verification_error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**session['user_data'])
        login(request, user)
        return Response({'message': 'User verified and logged in successfully'}, status=status.HTTP_200_OK)
