import random

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
import uuid
from django.contrib.auth.hashers import make_password

from api import constants


def generate_sms_code(sms_code_len=4):
    min_code_value = 10**(sms_code_len-1)
    max_code_value = 10**sms_code_len-1
    sms_code = str(random.randint(min_code_value, max_code_value))
    print(f"SMS_CODE: {sms_code}")
    return sms_code


def mask_phone_number(phone_number):
    phone_number = phone_number[:7] + "***" + phone_number[10:]
    return phone_number


class UserAuthAPIViewMixin:
    serializer = None
    existing_user = False

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = uuid.uuid4()
        session_key = constants.USER_SESSION_KEY.format(session_id)
        sms_code = generate_sms_code(sms_code_len=4)
        phone = serializer.validated_data['phone']
        user_data = {
            'phone': phone,
            'password': make_password(serializer.validated_data['password']),
        }
        # if self.existing_user:
        #     authenticate(**user_data)

        data = {
            "user_data": user_data,
            "sms_code": sms_code,
        }
        cache.set(session_key, data, constants.USER_SESSION_KEY_TTL)
        return Response(
            {'session_id': session_id, 'phone': mask_phone_number(phone)},
            status=status.HTTP_202_ACCEPTED
        )
