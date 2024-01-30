import functools
from typing import TypeAlias

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.http import HttpRequest

from django_otp.middleware import (
    OTPMiddleware as _OTPMiddleware,
    is_verified as otp_is_verified,
)

# probably a TypeVar(bound=...) makes more sense but we don't allow using generics here,
# so let's cover the most ground using a simple union.
AnyUser: TypeAlias = AbstractBaseUser | AnonymousUser


def is_verified(user: AbstractBaseUser) -> bool:
    """
    Modified version of :func:`django_otp.middleware.is_verified` to add bypass logic.

    This function may not be called with an :class:`AnonymousUser` instance!

    If the user backend that the user authenticated with is on the allow list, we do
    not perform the real OTP device check from the library, but just mark the user as
    verified.
    """
    # check our allow list for authentication backends
    backends_to_skip_verification_for = getattr(
        settings, "MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS", []
    )
    if (
        backends_to_skip_verification_for
        and user.is_authenticated
        and user.backend in backends_to_skip_verification_for  # type: ignore
    ):
        return True
    # fall back to default library behaviour
    return otp_is_verified(user)


class OTPMiddleware(_OTPMiddleware):
    """
    Substitute our own :func:`is_verified` check instead of the upstream one.

    This middleware *replaces* :class:`django_otp.middleware.OTPMiddleware` to add
    allow-list behaviour for certain authentication backends. This marks the user
    authentication as being verified even though the 2FA requirements in the project
    itself have been bypassen.

    This setup allows us to enforce 2FA when logging in with username + password, but
    be less strict when signing it via OIDC/other SSO solutions that already enforce
    MFA at another level outside of our scope.
    """

    def _verify_user(self, request: HttpRequest, user: AnyUser):
        # call the super but replace the `is_verified` callable
        user = super()._verify_user(request, user)
        # this is *not* persisted on the user object after authenticate
        user.backend = request.session.get(BACKEND_SESSION_KEY)
        user.is_verified = functools.partial(is_verified, user)  # type: ignore
        return user
