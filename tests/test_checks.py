from io import StringIO

from django.core.management import call_command
from django.core.management.base import SystemCheckError

import pytest


@pytest.mark.urls("tests.bad_urls.missing_core")
def test_urlconf_check_core_missing():
    with pytest.raises(SystemCheckError, match="(maykin_2fa.E001)"):
        call_command("check")


@pytest.mark.urls("tests.bad_urls.missing_webauthn")
def test_urlconf_check_webauthn_missing():
    with pytest.raises(SystemCheckError, match="(maykin_2fa.E002)"):
        call_command("check")


@pytest.mark.urls("tests.bad_urls.missing_webauthn")
def test_urlconf_without_webauhn_ok(settings):
    from testapp.settings import INSTALLED_APPS

    settings.INSTALLED_APPS = [
        app for app in INSTALLED_APPS if app != "two_factor.plugins.webauthn"
    ]
    settings.SILENCED_SYSTEM_CHECKS = ["maykin_2fa.E005"]

    call_command("check", stdout=StringIO())


def test_bypass_backend_not_in_auth_backends(settings):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = ["__unknown__"]
    settings.SILENCED_SYSTEM_CHECKS = ["maykin_2fa.E005"]
    stderr = StringIO()

    call_command("check", stderr=stderr)

    assert "(maykin_2fa.W001)" in stderr.getvalue()


def test_wrong_middleware(settings):
    settings.MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django_otp.middleware.OTPMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    with pytest.raises(SystemCheckError, match="(maykin_2fa.E004)"):
        call_command("check")


def test_middleware_missing(settings):
    settings.MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    with pytest.raises(SystemCheckError, match="(maykin_2fa.E003)"):
        call_command("check")


def test_okay_configuration():
    # testapp.settings is a valid configuration
    call_command("check", stdout=StringIO())


@pytest.mark.urls("tests.bad_urls.invalid")
def test_bad_urlconf():
    with pytest.raises(SystemCheckError, match="(urls.E004)"):
        call_command("check")
