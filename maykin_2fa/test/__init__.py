from django.conf import settings
from django.test import override_settings


def disable_admin_mfa():
    """
    Test helper to disable MFA requirements in the admin.

    Based on :func:`django.test.override_settings`, so you can use it as a decorator
    or context manager.
    """
    return override_settings(
        MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS=settings.AUTHENTICATION_BACKENDS,
    )
