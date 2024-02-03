from django.apps import apps

import pytest

try:
    import hijack
except ImportError:
    hijack = None

pytestmark = [
    pytest.mark.skipif(
        hijack is None, reason="Skipping hijack tests, dependency not installed."
    ),
    pytest.mark.django_db,
    pytest.mark.urls("tests.hijack_urls"),
]


@pytest.fixture(autouse=True)
def hijack_settings(settings):
    settings.INSTALLED_APPS = settings.INSTALLED_APPS + ["hijack"]
    settings.MIDDLEWARE = settings.MIDDLEWARE + [
        "hijack.middleware.HijackUserMiddleware"
    ]
    return settings


def test_hijack_enabled():
    # smoke test for invalid test fixtures/configuration
    is_installed = apps.is_installed("hijack")

    assert is_installed
