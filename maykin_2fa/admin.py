from django.contrib.admin import AdminSite
from django.core.exceptions import ImproperlyConfigured


class MFARequired(AdminSite):
    """
    AdminSite enforcing MFA verified staff users.

    .. warning:: This is a *copy* of two_factor.admin.AdminSiteOTPRequired, rather than
       subclassing. As of 1.18.0, the OTPRequiredMixin forces a URL resolution to
       ``two_factor:setup``, which is not included for our admin purposes. Using a
       different class/instance bypasses this check.

       We have our own logic that forces users to set up the MFA flow.
    """

    def has_permission(self, request):
        """
        Returns True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        if not super().has_permission(request):
            return False
        return request.user.is_verified()

    def login(self, request, extra_context=None):
        """
        Disabled to enforce usage of the custom login views.
        """
        raise ImproperlyConfigured(
            "Ensure the maykin_2fa urls are included *before* the default "
            "admin.site.urls."
        )


# sanity check that our own admin site variant overrides the same methods as the
# AdminSiteOTPRequiredMixin does, to catch upstream changes asap.
if __debug__:  # pragma: no cover
    import inspect

    from two_factor.admin import AdminSiteOTPRequiredMixin

    upstream_methods = {
        name
        for name, obj in inspect.getmembers(AdminSiteOTPRequiredMixin)
        if inspect.isfunction(obj)
    }
    own_methods = {
        name for name, obj in MFARequired.__dict__.items() if inspect.isfunction(obj)
    }
    if not_in_both := upstream_methods ^ own_methods:
        raise TypeError(
            f"Implementations have mismatching set of methods. Check: {not_in_both}."
        )
