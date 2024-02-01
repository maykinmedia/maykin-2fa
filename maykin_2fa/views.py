from typing import Any

from django.contrib import admin
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from two_factor.forms import TOTPDeviceForm
from two_factor.utils import default_device
from two_factor.views import (
    BackupTokensView as _BackupTokensView,
    LoginView as _LoginView,
    ProfileView as _ProfileView,
    QRGeneratorView as _QRGeneratorView,
    SetupCompleteView as _SetupCompleteView,
    SetupView as _SetupView,
)

from .decorators import admin_mfa_required


class AdminLoginView(_LoginView):
    template_name = "maykin_2fa/login.html"
    redirect_authenticated_user = False

    def get_redirect_url(self):
        # after succesful authentication, check if the user needs to set up 2FA. If MFA
        # was configured already, login flow takes care of the OTP step.
        user = self.request.user

        if user.is_authenticated and not user.is_verified():
            # no device is expected to be set up:
            # 1. if there is a device, the wizard takes you to the second factor step
            # 2. if there is no device, we now make the user set one up.
            #
            # Note that ``get_redirect_url`` should only be invoked at the end of the
            # login process.
            device = default_device(user)
            assert (
                device is None
            ), "Unexpectedly found an existing device for a non-verified user!"
            return resolve_url("maykin_2fa:setup")

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
                # Set by upstream package if settings.LOGOUT_REDIRECT_URL is configured,
                # but that would just redirect back to /admin/ for the admin interface.
                # We unset it.
                "cancel_url": None,
            }
        )
        return context


class AdminSetupView(_SetupView):
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


# override of the two-factor-auth, since we don't want to dictate OTP_LOGIN_URL in case
# there is MFA support in public (non-admin) URLs.
@admin_mfa_required()
class BackupTokensView(_BackupTokensView):
    success_url = "maykin_2fa:backup_tokens"
    template_name = "maykin_2fa/backup_tokens.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                **admin.site.each_context(self.request),
                "title": _("MFA Backup tokens"),
                "subtitle": None,
                "app_path": self.request.get_full_path(),
            }
        )
        return context


class RecoveryTokenView(AdminLoginView):
    """
    Custom view/template to handle the recovery token flow.
    """

    template_name = "maykin_2fa/recovery_token.html"

    def get_prefix(self, request, *args, **kwargs):
        # Deliberately share the same prefix as the AdminLoginView so we can grab the
        # user from the wizard storage
        return "admin_login_view"

    def get(self, *args, **kwargs):
        # Do not reset, instead set the current step to the recovery step.
        if not self.get_user():
            return redirect(reverse("admin:login"))
        self.storage.current_step = self.BACKUP_STEP
        return self.render(self.get_form())

    def post(self, *args, **kwargs):
        # anonymous users cannot enter recovery flows
        if not self.get_user():
            return redirect(reverse("admin:login"))
        return super().post(*args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["title"] = _("Use recovery token")
        return context


class SetupCompleteView(_SetupCompleteView):
    template_name = "maykin_2fa/setup_complete.html"

    def get_context_data(self, **kwargs):
        context: dict[str, Any] = super().get_context_data(**kwargs)
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


# override of the two-factor-auth, since we don't want to dictate OTP_LOGIN_URL in case
# there is MFA support in public (non-admin) URLs.
@admin_mfa_required()
class AccountSecurityView(_ProfileView):
    template_name = "maykin_2fa/account_security.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                **admin.site.each_context(self.request),
                "title": _("Account security"),
                "subtitle": None,
                "app_path": self.request.get_full_path(),
            }
        )
        return context
