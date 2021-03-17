import re

def password_check(pwd):
    if len(pwd) < 8 or len(pwd) > 21 and not re.findall('[0-9]+', pwd) \
            and not re.findall('[a-z]', pwd):
        # print("숫자의 길이, 영문 대소문자 구성에 맞지 않음!")
        return False

    elif not re.findall('[$!@%^&*#~<>/]', pwd):
        # print("최소 1개 이상의 특수문자가 필요")
        return False

    # print("pwd 유효")
    return True
