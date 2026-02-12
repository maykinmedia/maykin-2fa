=============
API reference
=============

Templates
=========

Maykin 2FA ships its own templates for tight integration in the admin interface.

In downstream projects, you may wish to extend these templates further. We've set up
some useful blocks that you can use to extend.

Base template
-------------

File ``maykin_2fa/base.html``

Used as base scaffolding for *most* of the other templates. This ensures that the small
UI from django's vanilla login template is applied.

Login template
--------------

File ``maykin_2fa/login.html``. Does **not** extend from ``maykin_2fa/base.html``.

This templated is used for the authentication flow:

* enter credentials (username + password)
* enter second factor

**Available blocks**

``{% block extra_login_options %}``
    If you provide SSO options like OpenID Connect, you can add them in this block.

``{% block recovery_options %}``
    If the user has recovery codes, this renders a small paragraph and link to the
    recovery token flow. You can override the entire block if you have significantly
    different instructions.

``{% block extra_recovery_options %}``
    Empty by default - you could include an instruction here to contact support to reset
    your device.

Other templates
---------------

The templates below do not provide additional blocks you would likely like to override.

- ``maykin_2fa/account_security.html``
- ``maykin_2fa/backup_tokens.html``
- ``maykin_2fa/recovery_token.html``
- ``maykin_2fa/setup.html``
- ``maykin_2fa/setup_complete.html``

Decorators
==========

.. automodule:: maykin_2fa.decorators
   :members:

Test helpers
============

.. automodule:: maykin_2fa.test
   :members:


Django-hijack integration
=========================

Maykin 2FA works out of the box with django-hijack. It subscribes to the
``hijack_started`` and ``hijack_ended`` signals to install a temporary hijack TOTP
device.

If you don't specify the setting ``HIJACK_PERMISSION_CHECK`` yet, you should update
this to:

.. code-block:: python

    HIJACK_PERMISSION_CHECK = "maykin_2fa.hijack.superusers_only_and_is_verified"

Alternatively, if you have a custom check, make sure to also check
``hijacker.is_verified()``.

.. _api-section:

API
===

Maykin 2FA provides an API endpoint that can be used to retrieve the status of
two factor authentication for the current user. An example response of the endpoint
can be seen below:

.. code-block:: json

    {"authStatus": {"mfaVerified": false}}

.. automodule:: maykin_2fa.api.views
   :members:
