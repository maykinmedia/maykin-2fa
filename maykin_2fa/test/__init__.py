from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.test import override_settings

from django_otp.oath import totp
from two_factor.utils import default_device, totp_digits

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

# Webtest backends, taken from https://github.com/django-webtest/django-webtest/blob/
# 6370c1afe034da416b03b2f88b7c71b9a49122c6/django_webtest/backends.py
DJANGO_WEBTEST_BACKENDS = (
    "django_webtest.backends.WebtestUserBackend",
    "django_webtest.backends.WebtestUserWithoutPermissionsBackend",
)


def disable_admin_mfa():
    """
    Test helper to disable MFA requirements in the admin.

    Based on :func:`django.test.override_settings`, so you can use it as a decorator
    or context manager.
    """
    django_backends = settings.AUTHENTICATION_BACKENDS
    all_backends = django_backends + list(DJANGO_WEBTEST_BACKENDS)
    return override_settings(MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS=all_backends)


def _totp_str(key: bytes):
    return str(totp(key)).zfill(totp_digits())


def get_valid_totp_token(user: AbstractBaseUser) -> str:
    """
    Given a user instance, generate a valid token for the default ``TOTPDevice``.

    :raises ValueError: if the default device is not a
      :class:`django_otp.plugins.otp_totp.models.TOTPDevice`.
    """
    from django_otp.plugins.otp_totp.models import TOTPDevice

    device = default_device(user)
    if device is None:
        raise ValueError("The user does not have a default device set up.")
    if not isinstance(device, TOTPDevice):
        raise ValueError("The user's default device is not a TOTPDevice.")
    return _totp_str(device.bin_key)
