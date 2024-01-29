import functools

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .middleware import is_verified


@receiver(user_logged_in, dispatch_uid="maykin_2fa.add_is_verified_method")
def add_is_verified_method(sender, request, user, **kwargs):
    """
    Add the method ``is_verified`` to the user instance.

    Normally this is added through middleware, but because django's ``login`` function
    assigns `request.user = instance`` directly from the DB, this method is lost.
    """
    user.is_verified = functools.partial(is_verified, user)
    if not hasattr(user, "otp_device"):
        user.otp_device = None
