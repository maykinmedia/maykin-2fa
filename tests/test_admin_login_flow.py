"""
Assert that the user must provide their second factor during the login process.
"""

from django.test import Client
from django.urls import reverse

from django_otp.oath import totp
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed
from two_factor.utils import totp_digits


def totp_str(key):
    return str(totp(key)).zfill(totp_digits())


def test_totp_device(settings, totp_device, client: Client):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = []
    admin_index_url = reverse("admin:index")
    admin_login_url = reverse("admin:login")

    # Login page
    login_page = client.get(admin_login_url)
    assertTemplateUsed(login_page, "maykin_2fa/login.html")

    login_response = client.post(
        admin_login_url,
        data={
            "admin_login_view-current_step": "auth",
            "auth-username": "johny",
            "auth-password": "password",
        },
    )

    assert login_response.wsgi_request.path == admin_login_url
    assertTemplateUsed(login_response, "maykin_2fa/login.html")
    assertContains(login_response, "Token")

    # Generator token page
    token_response = client.post(
        admin_login_url,
        data={
            "admin_login_view-current_step": "token",
            "token-otp_token": totp_str(totp_device.bin_key),
        },
    )
    assertRedirects(token_response, admin_index_url, fetch_redirect_response=False)

    admin_index = client.get(admin_index_url)
    assert admin_index.status_code == 200


def test_non_verified_user_is_logged_out(settings, totp_device, client: Client):
    """
    After enforcing 2fa, existing user sessions for (non-verified) users with TOTP
    devices need to log in again.
    """
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = []
    admin_index_url = reverse("admin:index")
    admin_login_url = reverse("admin:login")

    # try to access the index page
    index_response = client.get(admin_index_url)
    assertRedirects(index_response, f"{admin_login_url}?next={admin_index_url}")

    # log in again
    login_response = client.post(
        admin_login_url,
        data={
            "admin_login_view-current_step": "auth",
            "auth-username": "johny",
            "auth-password": "password",
        },
        follow=True,
    )
    assert login_response.wsgi_request.path == admin_login_url
    assertTemplateUsed(login_response, "maykin_2fa/login.html")
    assertContains(login_response, "Token")
