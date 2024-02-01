from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django_otp.decorators import otp_required


def admin_mfa_required():
    """
    Require multi-factor authentication for admin views.

    Decorator for class-based views.
    """
    otp_decorator = otp_required(login_url=reverse_lazy("admin:login"))
    return method_decorator(otp_decorator, name="dispatch")
