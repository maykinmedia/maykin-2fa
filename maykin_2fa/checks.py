from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.core.checks import Error, Warning, register
from django.core.checks.urls import check_url_config
from django.urls import NoReverseMatch, reverse

from .admin import MFARequired


@register()
def check_urlconf(app_configs, **kwargs):
    if check_url_config(app_configs, **kwargs):
        return []

    errors = []
    try:
        reverse("maykin_2fa:login")
    except NoReverseMatch:
        example_code = 'path("admin/", include((urlpatterns, "maykin_2fa"))),'
        errors.append(
            Error(
                "Broken URL config - could not resolve the 'maykin_2fa:login' URL.",
                hint=f"Try including `{example_code}` in your root `urls.py`.",
                id="maykin_2fa.E001",
            )
        )

    if apps.is_installed("two_factor.plugins.webauthn"):
        try:
            reverse("two_factor:webauthn:create_credential")
        except NoReverseMatch:
            example_code = (
                'path("admin/", include((webauthn_urlpatterns, "two_factor"))),'
            )
            errors.append(
                Error(
                    "Broken URL config - could not resolve the "
                    "'two_factor:webauthn:create_credential' URL.",
                    hint=f"Try including `{example_code}` in your root `urls.py`.",
                    id="maykin_2fa.E002",
                )
            )

    return errors


@register()
def check_authentication_backends(app_configs, **kwargs):
    bypass_backends = getattr(settings, "MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS", [])
    unknown_backends = [
        backend
        for backend in bypass_backends
        if backend not in settings.AUTHENTICATION_BACKENDS
    ]
    if not unknown_backends:
        return []

    return [
        Warning(
            "MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS contains backends not present in the "
            f"AUTHENTICATION_BACKENDS setting: {', '.join(unknown_backends)}",
            hint=(
                "Check for typos or add the backend(s) to "
                "settings.AUTHENTICATION_BACKENDS"
            ),
            id="maykin_2fa.W001",
        )
    ]


@register()
def check_middleware(app_configs, **kwargs):
    errors = []

    if "maykin_2fa.middleware.OTPMiddleware" not in settings.MIDDLEWARE:
        errors.append(
            Error(
                "`maykin_2fa.middleware.OTPMiddleware` is missing from the middleware.",
                hint="Add the maykin_2fa middleware instead of the django_otp one.",
                id="maykin_2fa.E003",
            )
        )

    if "django_otp.middleware.OTPMiddleware" in settings.MIDDLEWARE:
        errors.append(
            Error(
                "Found `django_otp.middleware.OTPMiddleware` in the middleware - this "
                "is obsolete.",
                hint=(
                    "Remove the django_otp middleware (instead, use the maykin_2fa "
                    "one)."
                ),
                id="maykin_2fa.E004",
            )
        )

    return errors


@register()
def check_admin_patched(app_configs, **kwargs):
    if check_url_config(app_configs, **kwargs):
        return []
    cls = admin.site.__class__
    if cls is MFARequired or issubclass(cls, MFARequired):
        return []

    return [
        Error(
            "The default admin site is not monkeypatched.",
            hint="Call 'maykin_2fa.monkeypatch_admin' in your root urls.py",
            id="maykin_2fa.E005",
        )
    ]
