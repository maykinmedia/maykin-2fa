from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import SystemCheckError
from django.urls import reverse

import pytest

from maykin_2fa import monkeypatch_admin


@pytest.fixture()
def unpatched_admin():
    """
    Ensure that the default admin site is not patched.
    """
    original = admin.site.__class__
    is_initially_patched = original is not AdminSite
    if is_initially_patched:
        admin.site.__class__ = AdminSite  # restore original

    yield

    if is_initially_patched:
        admin.site.__class__ = original


@pytest.fixture()
def patched_admin():
    """
    Ensure that the default admin site is patched.
    """
    original = admin.site.__class__

    is_initially_patched = original is not AdminSite
    if not is_initially_patched:
        monkeypatch_admin()

    yield

    if not is_initially_patched:
        admin.site.__class__ = original  # restore original


@pytest.mark.urls("tests.bad_urls.wrong_order")
def test_wrong_url_order_leads_to_exception_on_admin_login(patched_admin, client):
    """
    Raising an exception prevents redirect loops because django-two-factor-auth relies
    on settings.LOGIN_URL.
    """
    with pytest.raises(ImproperlyConfigured):
        client.get(reverse("admin:login"))


@pytest.mark.urls("tests.bad_urls.without_admin_patch")
def test_system_check_admin_patching(unpatched_admin):
    with pytest.raises(SystemCheckError, match="(maykin_2fa.E005)"):
        call_command("check")


def test_patched_admin_blocks_non_verified_users(patched_admin, admin_client, settings):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = []
    response = admin_client.get(reverse("admin:auth_user_changelist"))

    assert response.status_code == 302


def test_patched_admin_allows_verified_users(patched_admin, admin_client, settings):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = settings.AUTHENTICATION_BACKENDS
    response = admin_client.get(reverse("admin:auth_user_changelist"))

    assert response.status_code == 200
