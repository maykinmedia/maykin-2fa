from django.contrib.auth.backends import ModelBackend


class No2FAModelBackend(ModelBackend):
    """
    Custom backend which is allow-listed to bypass 2FA via the settings.
    """

    pass
