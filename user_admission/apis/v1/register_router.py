import json
from typing import Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from ninja import Form, Router, Schema

from user_admission.apis.v1.schemas.register_request import RegisterRequest
from user_admission.apis.v1.schemas.register_response import RegisterResponse
from user_admission.services.create_user_service import (
    create_users,
    email_check,
    password_check,
)

# register = Router(tags=["MemberManagement"])
#                     # 스웨거에서 쓰는것

account = Router(tags=["MemberManagement"])


# register page render router
@account.get("/", url_name="register", response=RegisterResponse)
def get_register_page(request: HttpRequest) -> HttpResponse:
    return render(request, "register.html")


@account.post("/")
def create_user(
        request: HttpRequest, register_request: RegisterRequest = Form(...)
) -> HttpResponse:
    email = email_check(register_request.email)
    # 이메일 유효성 검사에서 석세스 or 에러를 리턴
    password = password_check(register_request.password)
    # 패스워드 유효성 검사에서 석세스 or 에러 리턴
    email = list(email.keys())[0]
    password = list(password.keys())[0]
    if email == 'success' and password == 'success':
        # 만약 둘다 석세스라면
        user = create_users(
            register_request.email, register_request.password, register_request.nick_name
        )
        # 서비스로직(빈칸체크,이메일중복체크) 통과후 유저 생성후 메세지 리턴
        new_user_msg = list(user.keys())[0]
        if new_user_msg == "error":
            # 메세지가 에러라면
            return render(request, "register.html")
        else:
            # 에러가 아니라면
            return redirect("/login")
    else:
        # 둘다 석세스가 아니라면
        return render(request, "register.html")


class Email(Schema):
    email: str


@account.post("/reduplication")
def post_email_reduplication(request: HttpRequest, email: Email):
    check = email_check(email.email)
    # 이메일유효성검사 서비스로직 통과후 메세지 리턴
    return check


@account.post("/password")
def post_password_reduplication(request: HttpRequest) -> object:
    password = json.loads(request.body)['password']
    # 받은 패스워드
    check = password_check(password)
    # 유효성검사 로직 통과후 메세지 리턴
    return check
