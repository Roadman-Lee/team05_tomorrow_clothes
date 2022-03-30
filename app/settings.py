"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import json
import os
from pathlib import Path
from typing import List

from .local_settings import MYSQLRDS, TEAM5_SECRET

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = TEAM5_SECRET["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS: List[str] = ["*"]

# Application definition
AUTH_USER_MODEL = "user_admission.User"

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "content_post.apps.ContentPostConfig",
    "user_admission.apps.UserAdmissionConfig",
    "ninja",
    # 필수는 아니지만, ninja를 넣으면 OpenAPI/Swagger UI는 포함된 JavaScript 번들에서 (더 빠르게) 로드됩니다(그렇지 않으면 JavaScript 번들이 CDN에서 제공됨).
    "storages",
    # The following apps are required:
    "django.contrib.auth",
    "django.contrib.messages",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # ... include the providers you want to enable:
    "allauth.socialaccount.providers.kakao",
]

SITE_ID = 1

LOGIN_REDIRECT_URL = "/"  # 로그인 후 리디렉션할 페이지
ACCOUNT_LOGOUT_REDIRECT_URL = "/login"  # 로그아웃 후 리디렉션 할 페이지
ACCOUNT_LOGOUT_ON_GET = True  # 로그아웃 버튼 클릭 시 자동 로그아웃
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SESSION_REMEMBER = None
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_STORE_TOKENS = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",  # `allauth` needs this from django
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "app.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


import pymysql

pymysql.install_as_MySQLdb()

DATABASES = MYSQLRDS

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "https://s3.console.aws.amazon.com/s3/buckets/team05-tomorrow-clothes?region=ap-northeast-2&tab=objects/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "/img/upload/")
# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# APPEND_SLASH = False


with open(os.path.join(BASE_DIR, "config/aws.json")) as f:
    secrets = json.loads(f.read())
AWS_ACCESS_KEY_ID = secrets["AWS"]["ACCESS_KEY_ID"]  # .csv 파일에 있는 내용을 입력 Access key ID
AWS_SECRET_ACCESS_KEY = secrets["AWS"][
    "SECRET_ACCESS_KEY"
]  # .csv 파일에 있는 내용을 입력 Secret access key
AWS_REGION = "ap-northeast-2"

###S3 Storages
AWS_STORAGE_BUCKET_NAME = secrets["AWS"]["STORAGE_BUCKET_NAME"]  # 설정한 버킷 이름
AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_DEFAULT_ACL = "public-read"  # ACL 권한을 public 으로 바꿔준다.
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

with open(os.path.join(BASE_DIR, "config/smtp.json")) as f:
    secrets = json.loads(f.read())
EMAIL_HOST = 'smtp.gmail.com'
# 메일을 호스트하는 서버
EMAIL_PORT = '587'
# gmail과의 통신하는 포트
EMAIL_HOST_USER = 'seojh8910@gmail.com'
# 발신할 이메일
EMAIL_HOST_PASSWORD = secrets["smtp"]["password"]
# 발신할 메일의 비밀번호
EMAIL_USE_TLS = True
# TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# 사이트와 관련한 자동응답을 받을 이메일 주소,'webmaster@localhost'

# CORS_ORIGIN_ALLOW_ALL = True  # <- 모든 호스트 허용
# # CORS_ORIGIN_WHITELIST = ['http://ec2-15-164-94-71.ap-northeast-2.compute.amazonaws.com:8000','http://15.164.94.71:8000']
# CORS_ALLOW_CREDENTIALS = True
