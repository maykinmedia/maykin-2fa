from django.test import Client
from django.urls import reverse

import pytest
from django_otp.plugins.otp_static.models import StaticToken
from django_otp.util import random_hex

from maykin_2fa.test import get_valid_totp_token


def _create_totp_device(user):
    # See https://github.com/jazzband/django-two-factor-auth/blob/
    # 3c4888c79e37dc4c137bbccafb5680c1e4b74eaa/tests/test_views_login.py#L225
    return user.totpdevice_set.create(name="default", key=random_hex())


@pytest.fixture
def user(db: None, django_user_model):
    """
    Inspired on pytest-django's admin_user fixture.
    """
    UserModel = django_user_model
    username = "johny"
    try:
        # The default behavior of `get_by_natural_key()` is to look up by
        # `username_field`. However the user model is free to override it with any
        # sort of custom behavior. The Django authentication backend already assumes
        # the lookup is by username, so we can assume so as well.
        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        user_data = {
            "email": "johny@example.com",
            "password": "password",
            "username": username,
            "is_staff": True,
        }
        user = UserModel._default_manager.create_user(**user_data)
    return user


@pytest.fixture
def totp_device(user):
    """
    Set up a TOTP generator device for the user fixture.
    """
    return _create_totp_device(user)


@pytest.fixture
def recovery_codes(user) -> list[str]:
    """
    Ensure (backup) recovery codes are generated for the user fixture.
    """
    device = user.staticdevice_set.create(name="backup")
    tokens = [
        StaticToken(device=device, token=StaticToken.random_token()) for _ in range(5)
    ]
    StaticToken.objects.bulk_create(tokens)
    return [token.token for token in tokens]


@pytest.fixture
def mfa_admin_user(admin_user):
    _create_totp_device(admin_user)
    return admin_user


@pytest.fixture
def mfa_verified_client(mfa_admin_user):
    """
    Log in the MFA admin user and verify with token generator.
    """
    # use a separate client instance instead of the default fixture so that both
    # can be used in the same test
    client = Client()

    admin_login_url = reverse("admin:login")
    # login superuser who can hijack
    client.post(
        admin_login_url,
        data={
            "admin_login_view-current_step": "auth",
            "auth-username": "admin",
            "auth-password": "password",
        },
    )
    client.post(
        admin_login_url,
        data={
            "admin_login_view-current_step": "token",
            "token-otp_token": get_valid_totp_token(mfa_admin_user),
        },
    )
    # sanity check that we are actually fully verified
    admin_index = client.get(reverse("admin:index"))
    assert admin_index.status_code == 200
    return client
