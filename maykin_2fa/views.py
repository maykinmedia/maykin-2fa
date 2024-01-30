from django.contrib.auth import logout
from django.shortcuts import resolve_url

from two_factor.utils import default_device
from two_factor.views import (
    BackupTokensView as _BackupTokensView,
    LoginView as _LoginView,
    QRGeneratorView as _QRGeneratorView,
    SetupCompleteView as _SetupCompleteView,
    SetupView as _SetupView,
)


class AdminLoginView(_LoginView):
    template_name = "two_factor/core/login.html"
    redirect_authenticated_user = False

    def get_redirect_url(self):
        # after succesful authentication, check if the user needs to set up 2FA. If MFA
        # was configured already, login flow takes care of the OTP step.
        user = self.request.user

        if user.is_authenticated and not user.is_verified():
            # if no device is set up, redirect to the setup.
            device = default_device(user)
            if device is None:
                return resolve_url("maykin_2fa:setup")

            # a device is configured, but wasn't used - this may have been an aborted
            # authentication process. Log the user out and have the go through the login
            # flow again.
            logout(self.request)
            return resolve_url("maykin_2fa:login")

        admin_index = resolve_url("admin:index")
        return super().get_redirect_url() or admin_index


class AdminSetupView(_SetupView):
    # TODO: update to our own templates/URLs
    success_url = "maykin_2fa:setup_complete"
    qrcode_url = "maykin_2fa:qr"
    template_name = "two_factor/core/setup.html"


class BackupTokensView(_BackupTokensView):
    success_url = "maykin_2fa:backup_tokens"
    template_name = "two_factor/core/backup_tokens.html"


class SetupCompleteView(_SetupCompleteView):
    template_name = "maykin_2fa/setup_complete.html"


class QRGeneratorView(_QRGeneratorView):
    pass
