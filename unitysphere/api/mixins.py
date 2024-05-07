import uuid

from django.core.cache import cache
from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework import status

from api import constants, utils


class UserAuthAPIViewMixin:

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = uuid.uuid4()
        session_key = constants.USER_SESSION_KEY.format(session_id)
        sms_code = utils.generate_sms_code(sms_code_len=4)
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
