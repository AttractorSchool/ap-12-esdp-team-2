import random


def generate_sms_code(k: int = 4) -> str:
    nums = '0123456789'
    sms_code = ''.join(random.choices(nums, k=k))
    print(f"SMS_CODE: {sms_code}")
    return sms_code
