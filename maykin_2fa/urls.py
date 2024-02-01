from django.urls import include, path

from .views import (
    AccountSecurityView,
    AdminLoginView,
    AdminSetupView,
    BackupTokensView,
    QRGeneratorView,
    RecoveryTokenView,
    SetupCompleteView,
)

# See two_factor/urls.py for a reference of the (core) urls

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="login"),
    path("mfa/setup/", AdminSetupView.as_view(), name="setup"),
    path("mfa/qrcode/", QRGeneratorView.as_view(), name="qr"),
    path("mfa/setup/complete/", SetupCompleteView.as_view(), name="setup_complete"),
    path("mfa/backup/tokens/", BackupTokensView.as_view(), name="backup_tokens"),
    path("mfa/recovery/", RecoveryTokenView.as_view(), name="recovery"),
    # 'profile'
    path("mfa/", AccountSecurityView.as_view(), name="account_security"),
]

webauthn_urlpatterns = [
    path(
        "mfa/webauthn/",
        include("two_factor.plugins.webauthn.urls", namespace="two_factor_webauthn"),
    ),
]
