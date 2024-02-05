from django.apps import apps
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

import pytest
from two_factor.utils import default_device

try:
    import hijack
except ImportError:
    hijack = None

pytestmark = [
    pytest.mark.skipif(
        hijack is None, reason="Skipping hijack tests, dependency not installed."
    ),
    pytest.mark.django_db,
    pytest.mark.urls("tests.hijack_urls"),
]


@pytest.fixture(autouse=True)
def hijack_settings(settings):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = []
    settings.INSTALLED_APPS = settings.INSTALLED_APPS + ["hijack"]
    settings.MIDDLEWARE = settings.MIDDLEWARE + [
        "hijack.middleware.HijackUserMiddleware"
    ]
    return settings


def test_hijack_enabled():
    # smoke test for invalid test fixtures/configuration
    is_installed = apps.is_installed("hijack")

    assert is_installed


def test_can_hijack_staff_user(
    mfa_admin_user, client: Client, mfa_verified_client: Client
):
    admin_index_url = reverse("admin:index")
    # set up other staff user
    other_user = User.objects.create_user(
        username="other",
        password="password",
        is_staff=True,
        is_superuser=False,
    )

    # can't log in by themselves with mfa enabled
    assert default_device(other_user) is None
    client.login(username="other", password="password")
    other_user_response = client.get(admin_index_url)
    assert other_user_response.status_code == 302
    client.logout()

    # do the hijack
    response = mfa_verified_client.post(
        reverse("hijack:acquire"),
        data={
            "user_pk": other_user.pk,
            "next": admin_index_url,
        },
    )
    assert response.status_code == 302

    admin_index = mfa_verified_client.get(admin_index_url)
    assert admin_index.status_code == 200
    assert admin_index.context["request"].user == other_user

    # and release the user again
    mfa_verified_client.post(reverse("hijack:release"))

    admin_index = mfa_verified_client.get(admin_index_url)
    assert admin_index.status_code == 200
    assert admin_index.context["request"].user == mfa_admin_user


def test_release_without_hijack_not_possible(mfa_admin_user, client):
    # Test that MFA cannot be bypassed by username/password login + a release call
    client.login(username="admin", password="password")

    response = client.post(reverse("hijack:release"))

    assert response.status_code == 403


def test_hijack_without_verification_not_possible(mfa_admin_user, client):
    other_user = User.objects.create_user(username="other", password="password")
    client.login(username="admin", password="password")

    # SuspiciousOperation gets converted to HTTP 400 by Django
    response = client.post(
        reverse("hijack:acquire"),
        data={"user_pk": other_user.pk},
    )

    assert response.status_code == 400


def test_hijack_staff_user_with_bypass_enabled(admin_user, client: Client, settings):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = settings.AUTHENTICATION_BACKENDS
    admin_index_url = reverse("admin:index")
    # set up other staff user
    other_user = User.objects.create_user(
        username="other",
        password="password",
        is_staff=True,
        is_superuser=False,
    )
    # log in
    client.login(username="admin", password="password")
    admin_index = client.get(reverse("admin:index"))
    assert admin_index.status_code == 200

    response = client.post(
        reverse("hijack:acquire"),
        data={
            "user_pk": other_user.pk,
            "next": admin_index_url,
        },
    )
    assert response.status_code == 302

    admin_index = client.get(admin_index_url)
    assert admin_index.status_code == 200
    assert admin_index.context["request"].user == other_user

    # and release the user again
    client.post(reverse("hijack:release"))

    admin_index = client.get(admin_index_url)
    assert admin_index.status_code == 200
    assert admin_index.context["request"].user == admin_user


def test_custom_permission_check(settings, admin_user, client: Client):
    settings.HIJACK_PERMISSION_CHECK = (
        "maykin_2fa.hijack.superusers_only_and_is_verified"
    )
    # set up other staff user
    other_user = User.objects.create_user(
        username="other",
        password="password",
        is_staff=True,
        is_superuser=False,
    )
    client.login(username="admin", password="password")

    # do the hijack
    response = client.post(
        reverse("hijack:acquire"),
        data={"user_pk": other_user.pk},
    )
    assert response.status_code == 403
