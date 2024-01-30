from pathlib import Path

DEBUG = True
ALLOWED_HOSTS = ["*"]

BASE_DIR = Path(__file__).resolve(strict=True).parent

SECRET_KEY = "so-secret-i-cant-believe-you-are-looking-at-this"

USE_TZ = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "maykin_2fa.db",
    }
}

INSTALLED_APPS = [
    # Standard Django apps for testing/debugging
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",
    # Required by django-two-factor-auth and its dependencies
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    # 'django_otp.plugins.otp_email',  # <- if you want email capability.
    "two_factor",
    "two_factor.plugins.webauthn",
    # 'two_factor.plugins.phonenumber',  # <- if you want phone number capability.
    # 'two_factor.plugins.email',  # <- if you want email capability.
    # 'two_factor.plugins.yubikey',  # <- for yubikey capability.
    # Own package
    "maykin_2fa",
    # Test application for (unit) tests and demo.
    "testapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "maykin_2fa.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "/static/"

ROOT_URLCONF = "testapp.urls"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "testapp.backends.No2FAModelBackend",
]

# we take care of this, conditionally
TWO_FACTOR_PATCH_ADMIN = False

# Enable hardware tokens like yubikey
TWO_FACTOR_WEBAUTHN_RP_NAME = "maykin-2fa test/demo app"
TWO_FACTOR_WEBAUTHN_AUTHENTICATOR_ATTACHMENT = "cross-platform"

# Custom settings
MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = ["testapp.backends.No2FAModelBackend"]
# MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = AUTHENTICATION_BACKENDS
