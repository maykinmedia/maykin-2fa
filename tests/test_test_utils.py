from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

import pytest
from two_factor.plugins.webauthn.models import WebauthnDevice
from two_factor.utils import default_device

from maykin_2fa.test import disable_admin_mfa, get_valid_totp_token


class TestHelperTests(TestCase):

    def test_mfa_disabling(self):
        User.objects.create_user(username="johny", password="password", is_staff=True)
        self.client.login(username="johny", password="password")

        with disable_admin_mfa():
            response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)


def test_totp_token_without_device(user):
    with pytest.raises(ValueError):
        get_valid_totp_token(user)


def test_totp_token_with_wrong_device_type(user):
    device = WebauthnDevice.objects.create(user=user, name="default", sign_count=0)
    assert default_device(user) == device

    with pytest.raises(ValueError):
        get_valid_totp_token(user)


def test_totp_token_with_totp_device(user, totp_device):
    token = get_valid_totp_token(user)

    assert isinstance(token, str)
    assert len(token) >= 6
