import random


def generate_sms_code(sms_code_len=4):
    min_code_value = 10**(sms_code_len-1)
    max_code_value = 10**sms_code_len-1
    sms_code = str(random.randint(min_code_value, max_code_value))
    print(f"SMS_CODE: {sms_code}")
    return sms_code
