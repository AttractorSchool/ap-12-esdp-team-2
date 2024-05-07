from django.core.cache import cache

from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import constants, exceptions, serializers, mixins
from .serializers import UserCreateSerializer, UserLoginSerializer


class UserCreateAPIView(mixins.UserAuthAPIViewMixin, APIView):
    serializer = UserCreateSerializer


class UserLoginAPIView(mixins.UserAuthAPIViewMixin, APIView):
    serializer = UserLoginSerializer


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

        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': access,
            'refresh': refresh,
        },status=status.HTTP_201_CREATED)
