import random
from rest_framework.authtoken.models import Token
from accounts.models import User


def generate_sms_code() -> str:
    # Your SMS code generation logic should be here...
    sms_code = '7777'
    return sms_code


def generate_token(user: User) -> dict:
    token = Token.objects.create(user=user)

    return {
        'token': str(token.key),
    }
