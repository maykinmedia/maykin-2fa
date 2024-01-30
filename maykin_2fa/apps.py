from django.apps import AppConfig


class Maykin2FaConfig(AppConfig):
    name = "maykin_2fa"

    def ready(self):
        from . import signals  # noqa