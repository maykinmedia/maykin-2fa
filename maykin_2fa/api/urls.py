from django.urls import path

from maykin_2fa.api.views import UserInfoView

app_name = "maykin_2fa_api"

urlpatterns = [
    path("accounts/me", UserInfoView.as_view(), name="user_info"),
]
