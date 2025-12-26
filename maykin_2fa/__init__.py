def monkeypatch_admin():
    """
    Monkeypatch the admin to enforce 2FA.

    2FA is enforced but can be bypassed by putting the relevant authentication
    backend(s) on the allow list. In development, you might want to set all backends
    as bypassed:

    .. code-block::

        MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = AUTHENTICATION_BACKENDS

    .. note:: Users who log in with username + password in the admin **and** have any
       MFA-device configured on their account will still get the MFA prompt, even if
       the authentication backend is present in the bypass list.

       This may seem unintuitive, however, it would be unexpected for the users who went
       through the effort of securing their account that this is now suddenly no longer
       active.

    Upstream documentation:
    https://django-two-factor-auth.readthedocs.io/en/stable/implementing.html#admin-site
    """
    from django.contrib import admin

    from .admin import MFARequired

    admin.site.__class__ = MFARequired
