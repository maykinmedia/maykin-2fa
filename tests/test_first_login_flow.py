"""
Test flow for when the user logs in for the first time on the admin interface.

The default admin site enforces two-factor authentication, which means that a user
without any MFA devices gets redirected to the setup flow.
"""

from binascii import unhexlify

from django.test import Client
from django.urls import reverse

from django_otp.oath import totp
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed


def test_first_login_flow(settings, user, client: Client):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = []
    admin_index_url = reverse("admin:index")
    admin_login_url = reverse("admin:login")
    mfa_setup_url = reverse("maykin_2fa:setup")
    mfa_setup_complete_url = reverse("maykin_2fa:setup_complete")

    # Unauthenticated - must send you to the admin login URL
    index_response = client.get(admin_index_url)
    assertRedirects(index_response, f"{admin_login_url}?next={admin_index_url}")

    # Login page
    login_page = client.get(index_response["Location"])
    assertTemplateUsed(login_page, "maykin_2fa/login.html")

    login_response = client.post(
        index_response["Location"],
        data={
            "admin_login_view-current_step": "auth",
            "auth-username": "johny",
            "auth-password": "password",
        },
        follow=True,
    )

    assert login_response.wsgi_request.path == mfa_setup_url
    assertTemplateUsed(login_response, "maykin_2fa/setup.html")

    # Set up a token generator
    client.post(mfa_setup_url, data={"admin_setup_view-current_step": "welcome"})

    generator_response = client.post(
        mfa_setup_url,
        data={
            "admin_setup_view-current_step": "method",
            "method-method": "generator",
        },
    )
    assertTemplateUsed(generator_response, "maykin_2fa/setup.html")
    assertContains(generator_response, "Token")

    # Submit the token
    key = generator_response.context["keys"]["generator"]
    token = totp(unhexlify(key.encode()))
    token_response = client.post(
        mfa_setup_url,
        data={
            "admin_setup_view-current_step": "generator",
            "generator-token": token,
        },
        follow=True,
    )
    assert token_response.wsgi_request.path == mfa_setup_complete_url
    assertTemplateUsed(token_response, "maykin_2fa/setup_complete.html")


def test_authenticated_not_verified(settings, user, client: Client):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = []
    admin_index_url = reverse("admin:index")
    admin_login_url = reverse("admin:login")
    mfa_setup_url = reverse("maykin_2fa:setup")
    # ensure user is already logged in
    client.login(username="johny", password="password")

    # user is logged in but not verified -> send them to the login flow so that they
    # can set up their device.
    # XXX: would be cool if they can get sent directly to the setup view, but there are
    # no options there to log out/authenticate as a different user *and* it requires
    # us to override django's built in behaviour of redirect_to_login...
    index_response = client.get(admin_index_url)
    assertRedirects(index_response, f"{admin_login_url}?next={admin_index_url}")

    # log in again
    login_response = client.post(
        index_response["Location"],
        data={
            "admin_login_view-current_step": "auth",
            "auth-username": "johny",
            "auth-password": "password",
        },
        follow=True,
    )

    assert login_response.wsgi_request.path == mfa_setup_url
    assertTemplateUsed(login_response, "maykin_2fa/setup.html")
