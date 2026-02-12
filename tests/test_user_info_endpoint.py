from django.contrib.auth.models import AbstractBaseUser
from django.test import Client
from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_non_authenticated_user_get(client: Client):
    response = client.get(reverse("maykin_2fa_api:user_info"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_authenticated_user_get(client: Client, user: AbstractBaseUser):
    client.login(username="johny", password="password")
    response = client.get(reverse("maykin_2fa_api:user_info"))

    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {
        "authStatus": {
            "mfaVerified": False,
        }
    }


@pytest.mark.django_db
def test_mfa_authenticated_user_get(mfa_verified_client: Client):
    response = mfa_verified_client.get(reverse("maykin_2fa_api:user_info"))

    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {
        "authStatus": {
            "mfaVerified": True,
        }
    }
