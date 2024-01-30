from django.core.exceptions import ImproperlyConfigured

from two_factor.admin import AdminSiteOTPRequired


class MFARequired(AdminSiteOTPRequired):
    def login(self, request, extra_context=None):
        """
        Disabled to enforce usage of the custom login views.
        """
        raise ImproperlyConfigured(
            "Ensure the maykin_2fa urls are included *before* the default "
            "admin.site.urls."
        )
