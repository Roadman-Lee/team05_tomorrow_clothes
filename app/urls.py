from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse
from ninja import NinjaAPI

from content_post.apis.v1.comment_router import content as comment_router
from content_post.apis.v1.detail_router import content as detail_router
from content_post.apis.v1.main_router import content as main_router
from content_post.apis.v1.scrap_router import content as scrap_router
from content_post.apis.v1.mypage_router import content as mypage_router
from content_post.apis.v1.weather_router import content as weather_router
from user_admission import views
from user_admission.apis.v1.login_router import account as login_router
from user_admission.apis.v1.logout_router import account as logout_router
from user_admission.apis.v1.register_router import account as register_router

from django.contrib.auth import views as auth_views

# version 1.0.0 >> 중요한 변경 / 중간 변경 / 최소 변경

api = NinjaAPI(urls_namespace="test_1", version="1.0.0", docs_url=None)

# ninja routers
api.add_router("login/", login_router)
api.add_router("register/", register_router)
api.add_router("", main_router)
api.add_router("detail/", detail_router)
api.add_router("detail/", scrap_router)
api.add_router("logout/", logout_router)
api.add_router("comment/", comment_router)
# api.add_router("weather/", mypage_router)
api.add_router("mypage/", mypage_router)
api.add_router("k-weather/", weather_router)

urlpatterns = [
    path("tomorrow/weather/admin/", admin.site.urls),
    path("", api.urls),
    path("accounts/", include("allauth.urls")),

    # 비밀번호 변경
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'),
         name="password_reset"),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name="password_reset_complete"),
]
