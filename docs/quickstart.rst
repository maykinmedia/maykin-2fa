==========
Quickstart
==========

Installation
============

Install from PyPI with pip:

.. code-block:: bash

    pip install maykin-2fa


Settings
========

As this library bundles django-two-factor-auth, the installation instructions of it are
relevant. For typical Maykin usage, you'll want to:

**Add the required ``INSTALLED_APPS`` entries**

.. code-block:: python

    INSTALLED_APPS = [
        ...,
        # Required by django-two-factor-auth and its dependencies
        "django_otp",
        "django_otp.plugins.otp_static",
        "django_otp.plugins.otp_totp",
        "two_factor",
        "two_factor.plugins.webauthn",
        "maykin_2fa",
        ...,
    ]

**Set up our middleware override**

We ship a modified ``django-otp`` middleware - so instead of ``django_otp.middleware.OTPMiddleware``,
you must set ``maykin_2fa.middleware.OTPMiddleware``, after the authentication middleware:

.. code-block:: python

    MIDDLEWARE = [
        ...,
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "maykin_2fa.middleware.OTPMiddleware",
        ...,
    ]

**Disable admin patching**

.. code-block:: python

    TWO_FACTOR_PATCH_ADMIN = False

The default is ``True``. Patching the admin uses some project-global URLs, which we
will manage ourselves instead.

.. todo:: CHECK IF THIS STILL NEEDED!

**Congigure WebAuthn relying party**

This is required when using the WebAuthn plugin so you can use hardware tokens.

.. code-block:: python

    TWO_FACTOR_WEBAUTHN_RP_NAME = "TODO - figure out what the meaning is"

.. todo:: look into details of this, but the setting is required.

**Configure allow list to skip 2FA-enforcement**

By default, this package ensures the admin enforces 2FA. However, when logging it
through OpenID Connect or other Single-Sign-On solutions, this can lead to double 2FA
flows. Since these alternative login flows typically come with a custom Django
authentication backend, you can add them to an allowlist to bypass the application MFA.

.. code-block::

    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
        "mozilla_django_oidc_db.backends.OIDCAuthenticationBackend",
    ]

    MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = [
        "mozilla_django_oidc_db.backends.OIDCAuthenticationBackend",
    ]

.. todo:: add system check to check that each backend is in the ``AUTHENTICATION_BACKENDS`` setting.

Usage
=====

Should be plug and play - there is no additional frontend stuff.

.. todo:: Complete if relevant.
