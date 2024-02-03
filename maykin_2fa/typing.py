from typing import Protocol

from django_otp.models import Device


class VerifiableUser(Protocol):
    """
    The `is_verified` callback gets added through the OTP middleware.
    """

    is_active: bool
    is_anonymous: bool
    is_authenticated: bool

    otp_device: Device | None

    def get_username(self) -> str: ...

    def is_verified(self) -> bool: ...
