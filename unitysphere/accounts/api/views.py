import uuid
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status, permissions as drf_permissions, generics
from rest_framework.views import APIView

from accounts.models import User, Profile
from accounts import utils
from accounts import constants
from . import serializers
from . import exceptions
from . import permissions


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (drf_permissions.AllowAny,)
    serializer_class = serializers.UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = uuid.uuid4()
        session_key = constants.USER_SESSION_KEY.format(session_id)
        sms_code = utils.generate_sms_code(k=4)
        phone = serializer.validated_data['phone']

        user_data = {
            'phone': phone,
            'password': make_password(serializer.validated_data['password2']),
        }

        data = {
            'user_data': user_data,
            'sms_code': sms_code,
        }
        cache.set(session_key, data, constants.USER_SESSION_KEY_TTL)
        return Response({'session_id': session_id}, status=status.HTTP_202_ACCEPTED)


class UserVerifyAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_key = constants.USER_SESSION_KEY.format(serializer.validated_data['user_session_id'])
        session = cache.get(session_key)

        if session is None:
            raise exceptions.SMSCodeExpireException

        if session['sms_code'] != serializer.validated_data['sms_code']:
            raise exceptions.SMSCodeInvalidException

        user = User.objects.create(**session['user_data'])
        user.save()
        tokens = utils.generate_tokens(user)

        return Response(tokens, status=status.HTTP_201_CREATED)


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.ProfileUpdateSerializer
    permission_classes = (permissions.IsProfileOwnerOrReadOnly,)
    queryset = Profile.objects.all()


class UserToSearchingInAlliesList(APIView):
    permission_classes = (drf_permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.is_displayed_in_allies = 1 - request.user.is_displayed_in_allies
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
