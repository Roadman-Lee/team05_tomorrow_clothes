import re

from user_admission.models import User


# 유저 생성
def create_users(email: str, password: str, nick_name: str) -> object:
    if email == "" or password == "" or nick_name == "":
        msg = {"error": "모두 입력해주세요."}
        return msg
    else:
        exist_check = User.objects.filter(username=email)
        if exist_check.exists():
            msg = {"error": "중복된 이메일입니다."}
            return msg
        else:
            User.objects.create_user(
                username=email, password=password, nick_name=nick_name, email=email,
                pro_img_url='images/프로필이미지4.jpeg'
            )
            msg = {"success": "가입에 성공하셨습니다."}
            return msg


# 비밀번호 유효성 검사
def password_check(password: str) -> object:
    password_regex = re.compile(
        "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}"
    )
    if not password_regex.match(password):
        msg = {"error": "8자 이상의 알파벳, 숫자, 특수문자를 사용하세요."}
        return msg
    else:
        msg = {"success": "올바른 형식입니다."}
        return msg
    # ?= : 전방 탐색. 주어진 값의 앞에서 부터 찾는다.
    # (?=.*[A-Za-z]) > A부터 Z, a부터 z까지 여러 개가 반복 되어 올 수 있음
    # (?=.*\d) > \d 정수 검색 = 0~9 가능 하다는 뜻
    # (?=.*[$@$!%*#?&]) > [] 내의 특수문자들만 비밀번호로 사용가능 >> 이것도 틀리는 경우 오류 발생 이유를 출력해주긴 해야함
    # [A-Za-z\d$@$!%*#?&]{8,} > 앞의 값들 중 8개 이상 일치해야함 즉 8글자 이상의 비밀번호 입력해야함.


# 이메일 유효성 검사
def email_check(username: str) -> object:
    email_regex = re.compile("^[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if not email_regex.match(username):
        msg = {"error": "이메일 형식이 아닙니다."}
        return msg
    else:
        exist_check = User.objects.filter(username=username)
        if exist_check.exists():
            msg = {"error": "중복된 이메일입니다."}
            return msg
        else:
            msg = {"success": "사용가능한 이메일입니다."}
            return msg
    # ^[a-zA-Z0-9+-_.]+@
    # @를 기준으로 앞부분 > 계정. 영문 대소문자, 숫자, +-_. 특수문자 확인
    # [a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$
    # @를 기준으로 뒷부분 > (도메인).(최상위 도메인)
    # 최상위 도메인은 co.kr 처럼 여러 단계일수 있으므로 $ 붙여주어 가장 마지막에 위치하는것 확인
