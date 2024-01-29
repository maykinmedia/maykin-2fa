from django.shortcuts import resolve_url

from two_factor.views import (
    BackupTokensView as _BackupTokensView,
    LoginView as _LoginView,
    QRGeneratorView as _QRGeneratorView,
    SetupCompleteView as _SetupCompleteView,
    SetupView as _SetupView,
)


class AdminLoginView(_LoginView):
    template_name = "two_factor/core/login.html"
    redirect_authenticated_user = True

    def get_redirect_url(self):
        # after succesful authentication, check if the user needs to set up 2FA. If MFA
        # was configured already, login flow takes care of the OTP step.
        user = self.request.user

        if user.is_authenticated and not user.is_verified():
            return resolve_url("maykin_2fa:setup")
        return super().get_redirect_url()


class AdminSetupView(_SetupView):
    # TODO: update to our own templates/URLs
    success_url = "maykin_2fa:setup_complete"
    qrcode_url = "maykin_2fa:qr"
    template_name = "two_factor/core/setup.html"


class BackupTokensView(_BackupTokensView):
    success_url = "maykin_2fa:backup_tokens"
    template_name = "two_factor/core/backup_tokens.html"


class SetupCompleteView(_SetupCompleteView):
    template_name = "two_factor/core/setup_complete.html"


class QRGeneratorView(_QRGeneratorView):
    pass
