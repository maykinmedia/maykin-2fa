from django.apps import AppConfig, apps


class Maykin2FaConfig(AppConfig):
    name = "maykin_2fa"

    def ready(self):
        from . import checks  # noqa
        from . import signals  # noqa

        # enable django-hijack integration if it's installed
        if apps.is_installed("hijack"):
            from . import hijack_signals  # noqa
