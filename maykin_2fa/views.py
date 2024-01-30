from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import resolve_url
from django.utils.translation import gettext_lazy as _

from two_factor.forms import TOTPDeviceForm
from two_factor.utils import default_device
from two_factor.views import (
    BackupTokensView as _BackupTokensView,
    LoginView as _LoginView,
    QRGeneratorView as _QRGeneratorView,
    SetupCompleteView as _SetupCompleteView,
    SetupView as _SetupView,
)


class AdminLoginView(_LoginView):
    template_name = "maykin_2fa/login.html"
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

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context.update(
            {
                **admin.site.each_context(self.request),
                "title": _("Log in"),
                "subtitle": None,
                "app_path": self.request.get_full_path(),
            }
        )
        return context


class AdminSetupView(_SetupView):
    # TODO: update to our own templates/URLs
    success_url = "maykin_2fa:setup_complete"
    qrcode_url = "maykin_2fa:qr"
    template_name = "maykin_2fa/setup.html"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        # patch the form input type to not have numeric input controls...
        # I checked that this does not mutate the entire class :)
        if isinstance(form, TOTPDeviceForm):
            form.fields["token"].widget.input_type = "text"

        return form

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context.update(
            {
                **admin.site.each_context(self.request),
                "title": _("Set up MFA"),
                "subtitle": None,
                "app_path": self.request.get_full_path(),
                # Cancelling MFA setup is not optional.
                "cancel_url": None,
            }
        )
        return context


class BackupTokensView(_BackupTokensView):
    success_url = "maykin_2fa:backup_tokens"
    # TODO
    template_name = "two_factor/core/backup_tokens.html"


class SetupCompleteView(_SetupCompleteView):
    template_name = "maykin_2fa/setup_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                **admin.site.each_context(self.request),
                "title": _("MFA setup complete"),
                "subtitle": None,
                "app_path": self.request.get_full_path(),
            }
        )
        return context


class QRGeneratorView(_QRGeneratorView):
    pass
