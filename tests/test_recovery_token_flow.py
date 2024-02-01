import random

from django.urls import reverse

import pytest
from pytest_django.asserts import assertContains, assertRedirects, assertTemplateUsed


@pytest.mark.django_db
def test_non_authenticated_user_get(client):
    recovery_url = reverse("maykin_2fa:recovery")
    login_url = reverse("admin:login")

    response = client.get(recovery_url)

    # we don't care about the ?next parameter, this is not a meaningful flow
    assertRedirects(response, login_url)


@pytest.mark.django_db
def test_non_authenticated_user_post(client):
    recovery_url = reverse("maykin_2fa:recovery")
    login_url = reverse("admin:login")

    response = client.post(recovery_url)

    # we don't care about the ?next parameter, this is not a meaningful flow
    assertRedirects(response, login_url)


def test_recovery_token_authenticated_user(
    client, user, totp_device, recovery_codes: list[str]
):
    recovery_url = reverse("maykin_2fa:recovery")

    # start at the login wizard
    login_response = client.post(
        reverse("admin:login"),
        data={
            "admin_login_view-current_step": "auth",
            "auth-username": "johny",
            "auth-password": "password",
        },
    )
    assert login_response.status_code == 200

    # check that the URL initializes on the recovery step
    recovery_page = client.get(recovery_url)

    assertTemplateUsed(recovery_page, "maykin_2fa/recovery_token.html")
    assertContains(recovery_page, "Verify")

    # enter a valid recovery token
    response = client.post(
        recovery_url,
        data={
            "admin_login_view-current_step": "backup",
            "backup-otp_token": random.choice(recovery_codes),
        },
    )
    assertRedirects(response, reverse("admin:index"))
