=========
Changelog
=========

2.1.0 (2026-02-20)
==================

Feature release.

**Features**

* [#5] Added API endpoint that exposes authentication and multi-factor verification status
  of a user.

**Project maintenance**

* Fixed references to non-existent ``coverage`` package extra dependency group.

2.0.1 (2025-01-07)
==================

Bugfix release.

* Fixed compatibility with django-otp 1.7+.

2.0.0 (2025-12-26)
==================

Maintenance release, addming/fixing support for newer versions of dependencies.

Despite the breaking changes listed below, upgrading should be straight forward if
you're already on Python 3.12+ and Django 4.2 or newer.

**💥 Breaking changes**

* Dropped support for Python 3.10 and 3.11.
* Dropped support for Django 3.2.
* The mininimum required version of ``django-two-factor-auth`` is bumped to 1.18.1.
* The ``phonenumberslite`` dependency is no longer installed due to it not being
  required anymore in ``django-two-factor-auth``.

**Features**

* Confirmed support for Python 3.13 and 3.14.
* Confirmed support for Django 5.2 and 6.0.
* Added alias ``disable_mfa`` for the existing ``disable_admin_mfa`` test helper.
* Fixed compatibility with ``django-two-factor-auth`` 1.18 and newer.

**Bugfixes**

* [#17] Fixed missing error message when using an already used recovery code.

**Project maintenance**

* [#14] Added documentation about bypass behaviour when a user has a MFA-device
  configured.
* The CI pipeline is now run nightly to catch breakages due to dependency changes.
* Simplified the optional (dev) dependency groups.
* Replaced black, isort and flake8 with Ruff.

1.0.2 (2025-01-16)
==================

Minor fix

* Add possibility to override the error message in the login template shown when the
  user is already authenticated.

1.0.1 (2024-07-25)
==================

Minor bugfix

* [#16] Fixed redirect_to feature in the admin login

1.0.0 (2024-02-05)
==================

The library is now considered feature complete.

* [#9] Added built-in support for django-hijack
* Added more test helpers
* Confirmed support for Django 3.2 to allow migrating existing projects

0.2.2 (2024-02-02)
==================

Fixed packaging mistake

* Ensure the .mo files are bundled in the package

0.2.1 (2024-02-02)
==================

Patch release after upgrading some projects

* Fixed system check dependency on URLconf being loaded
* Added/modified Dutch translations

0.2.0 (2024-02-01)
==================

MVP release - this release offers the same features as our django-two-factor-auth fork,
you should be able to replace it with this library now.

.. note:: The installation requirements require Django 3.2+ to facilitate upgrading to
   Django 4.2. The templates/styling have not been tested on Django 3.2 yet.

* Implemented the "account security" page and links to it
* Implemented page to manage backup tokens and links to it
* Implemented and tested the backup code/token recovery flow
* Added support for django-webtest in ``@disable_admin_mfa`` test decorator
* Added API reference documentation

    * Documented the decorator(s)
    * Documented the test helper(s)
    * Documented template blocks available for override

* Added tests

0.1.0 (2024-01-31)
==================

Initial proof of concept.
