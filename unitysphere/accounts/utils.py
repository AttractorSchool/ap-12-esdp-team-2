import random
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


def generate_sms_code(k: int = 4) -> str:
    nums = '0123456789'
    sms_code = ''.join(random.choices(nums, k=k))
    print(f"SMS_CODE: {sms_code}")
    return sms_code


def generate_tokens(user: User) -> dict:
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
