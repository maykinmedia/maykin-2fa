from django.urls import reverse

from pytest_django.asserts import assertRedirects, assertTemplateUsed


def test_renders_own_template(settings, client, user, totp_device):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = settings.AUTHENTICATION_BACKENDS
    client.login(username="johny", password="password")

    response = client.get(reverse("maykin_2fa:account_security"))

    assertTemplateUsed(response, "maykin_2fa/account_security.html")


def test_user_must_be_verified(settings, client, user, totp_device):
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = []
    client.login(username="johny", password="password")
    url = reverse("maykin_2fa:account_security")

    response = client.get(url)

    assertRedirects(
        response,
        f"{reverse('admin:login')}?next={url}",
        fetch_redirect_response=False,
    )
