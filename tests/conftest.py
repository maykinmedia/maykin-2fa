import pytest
from django_otp.plugins.otp_static.models import StaticToken
from django_otp.util import random_hex


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
    # See https://github.com/jazzband/django-two-factor-auth/blob/
    # 3c4888c79e37dc4c137bbccafb5680c1e4b74eaa/tests/test_views_login.py#L225
    return user.totpdevice_set.create(name="default", key=random_hex())


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
