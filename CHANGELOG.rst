=========
Changelog
=========

1.0.0 (2024-02-05)
==================

The library is now considered feature complete.

* [#9] Added built-in support for djano-hijack
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
