from django.conf import settings
from django.test import override_settings

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
