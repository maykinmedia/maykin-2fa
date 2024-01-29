from django.urls import path

from .views import (
    AdminLoginView,
    AdminSetupView,
    BackupTokensView,
    QRGeneratorView,
    SetupCompleteView,
)

app_name = "maykin_2fa"

# See two_factor/urls.py for a reference of the (core) urls

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="login"),
    path("mfa/setup/", AdminSetupView.as_view(), name="setup"),
    path("mfa/qrcode/", QRGeneratorView.as_view(), name="qr"),
    path("mfa/setup/complete/", SetupCompleteView.as_view(), name="setup_complete"),
    path("mfa/backup/tokens/", BackupTokensView.as_view(), name="backup_tokens"),
]
