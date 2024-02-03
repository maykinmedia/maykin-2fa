"""
Support for django-hijack in the django admin interface when MFA is enforced.

Originally authored by @Bartvaderkin as part of
https://github.com/open-formulieren/open-forms.
"""

from typing import Any

from django.core.exceptions import SuspiciousOperation
from django.dispatch import receiver
from django.http import HttpRequest

from django_otp import login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice
from hijack.signals import hijack_ended, hijack_started
from two_factor.utils import default_device

from .typing import VerifiableUser

HIJACK_DEVICE_NAME = "hijack_device"


@receiver(hijack_started, dispatch_uid="maykin_2fa.hijack_started.manage_totp_device")
def handle_hijack_start(
    sender: None,
    hijacker: VerifiableUser,
    hijacked: VerifiableUser,
    request: HttpRequest,
    **kwargs: Any,
):
    """
    Create a hijack device if needed.

    If a staff user gets hijacked, a multi-factor device needs to be set to be able
    to use the admin interface as that user. Set a temporary hijack device to achieve
    this.
    """
    # Crash if the hijacker was not MFA verified. This should prevent the hijack too
    # because the hijack views are wrapped in atomic transactions. An explicit
    # request.session.save() *may* still make the hijack go through since the signal
    # only fires *after* the hijack is performed.
    if not hijacker.is_verified():
        raise SuspiciousOperation(
            f"User {hijacker.get_username()} hijacked user "
            f"{hijacked.get_username()} without being two-factor verified."
        )

    # XXX possibly we can create our own plugin/device type for this?
    hijack_device, _ = TOTPDevice.objects.get_or_create(
        user=hijacked,
        name=HIJACK_DEVICE_NAME,
    )
    otp_login(request, hijack_device)


@receiver(hijack_ended, dispatch_uid="maykin_2fa.hijack_ended.manage_totp_device")
def handle_hijack_end(
    sender: None,
    hijacker: VerifiableUser,
    hijacked: VerifiableUser,
    request: HttpRequest,
    **kwargs: Any,
):
    """
    1. Remove any dummy OTP devices for the hijacked user.
    2. Restore the original OTP device for the hijacker.

    Determining the 'original' OTP device for the hijacker is not trivial - we can not
    simply store a reference to ``hijacker.otp_device`` in the session data in the
    :func:`maykin_2fa.hijack_signals.handle_hijack_start` handler because releasing the
    user calls django's :func:`django.contrib.auth.login`, which flushes the
    session. Flushing the session causes us to lose that information *before* the
    ``hijack_ended`` signal fires.

    Instead, we grab the default device from the hijacker and restore that - at the
    time of writing it does not seem to be possible to use multiple devices (see also
    https://github.com/maykinmedia/maykin-2fa/issues/11) - so that the hijacker is
    verified again.

    * django-hijack validates that a release can only be done after an acquire
    * therefore, enforcing a verified user during hijack implies that only verified
      users can release
    """
    TOTPDevice.objects.filter(user=hijacked, name=HIJACK_DEVICE_NAME).delete()

    # restore 'original' device. See the docstring for why this is not guaranteed to be
    # the original device.
    original_device = default_device(hijacker)
    if original_device is not None:
        otp_login(request, original_device)
    else:
        hijacker.otp_device = None
