from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import HttpResponse, redirect, render
from ninja import Router, Form

from user_admission.apis.v1.schemas.login_response import LoginResponse
from user_admission.apis.v1.schemas.login_request import LoginRequest

account = Router(tags=["MemberManagement"])


@account.get("/", url_name="login", response=LoginResponse)
def get_login_page(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


@account.post("/", url_name="login", response=LoginResponse)
def post_login(request: HttpRequest, loginrequest: LoginRequest = Form(...)) -> HttpResponse:
    username = loginrequest.username
    # 입력된 유저네임
    password = loginrequest.password
    # 입력된 패스워드
    user = auth.authenticate(request, username=username, password=password)
    # 유저네임과 패스워드가 일치하지않으면 None을 리턴하게된다
    if user is not None:
        # 일치한다면
        auth.login(request, user)
        # 로그인
        return redirect("/")
    else:
        error = {"error": "이메일 또는 비밀번호를 확인해주세요."}
        return render(request, "login.html", error)
