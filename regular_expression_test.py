import re

def validate_phone_number(number):
    if not re.match(r'^01[016789][1-9]\d{6,7}$',number):
        return False
    return True


print(validate_phone_number('01012345678'))
print(validate_phone_number('0111234567'))
print(validate_phone_number('01212345678'))
print(validate_phone_number('016123456789'))
