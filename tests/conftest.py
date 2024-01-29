import pytest


@pytest.fixture
def user(db: None, django_user_model):
    """
    Inspired on pytest-django's admin_user fixture.
    """
    UserModel = django_user_model
    username = "johny"
    try:
        # The default behavior of `get_by_natural_key()` is to look up by `username_field`.
        # However the user model is free to override it with any sort of custom behavior.
        # The Django authentication backend already assumes the lookup is by username,
        # so we can assume so as well.
        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        user_data = {"email": "johny@example.com"}
        user_data["password"] = "password"
        user_data["username"] = username
        user = UserModel._default_manager.create_user(**user_data)
    return user
