from django.http import HttpRequest, HttpResponse
from django.utils.functional import SimpleLazyObject

import pytest

from maykin_2fa.middleware import OTPMiddleware


@pytest.fixture()
def user_request(request, client, rf, user) -> HttpRequest:
    marker = request.node.get_closest_marker("user_request_auth_backend")
    backend = None if not marker else marker.args[0]
    # sets the backend and session
    client.force_login(user, backend=backend)

    # create a standalone request instance, by copying over the session and mimicking
    # the `django.contrib.auth.middleware.AuthenticationMiddleware` middleware
    django_request = rf.get("/irrelevant")
    django_request.session = client.session
    django_request.user = SimpleLazyObject(lambda: user)
    return django_request


@pytest.mark.user_request_auth_backend("django.contrib.auth.backends.ModelBackend")
def test_authenticated_but_not_verified(user_request, settings):
    """
    Test that a user who logs in is not verified by default.
    """
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = []
    middleware = OTPMiddleware(lambda req: HttpResponse())

    middleware(user_request)

    # standard Django behaviour
    user = user_request.user
    assert user.is_authenticated
    assert user.backend == "django.contrib.auth.backends.ModelBackend"
    # OTP middleware adds the `is_verified` callable
    assert hasattr(user, "is_verified")
    assert callable(user.is_verified)
    # we didn't go through any 2FA flows, so the user is *NOT* verified
    assert user.is_verified() is False


@pytest.mark.user_request_auth_backend("testapp.backends.No2FAModelBackend")
def test_authenticated_and_2fa_verification_bypassed(user_request, settings):
    """
    Test that a user is "2FA-verified" when authenticated through a backend on the
    allow list.
    """
    settings.MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = [
        "testapp.backends.No2FAModelBackend"
    ]
    middleware = OTPMiddleware(lambda req: HttpResponse())

    middleware(user_request)

    # standard Django behaviour
    user = user_request.user
    assert user.is_authenticated
    assert user.backend == "testapp.backends.No2FAModelBackend"
    # OTP middleware adds the `is_verified` callable
    assert hasattr(user, "is_verified")
    assert callable(user.is_verified)
    # didn't go through any 2FA flows, but the backend is on the allow list
    assert user.is_verified()
