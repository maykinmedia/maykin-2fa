Maykin 2FA
==========

:Version: 1.0.0
:Source: https://github.com/maykinmedia/maykin-2fa
:Keywords: django, two factor, multi factor auth, mfa

|build-status| |code-quality| |black| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

An opinionated integration of django-two-factor-auth_ in the Django admin interface.

.. contents::

.. section-numbering::

Features
========

* Uses upstream django-two-factor-auth package rather than maintaining a fork
* Ships templates in the Django admin login layout for the two-factor authentication flow
* Multi-factor authentication is enforced for admin users, but...
* Allows marking certain authentication backends (like Single-Sign-On solutions) as
  exempt from this rule
* Works with django-hijack out of the box
* Does not get in the way of using django-two-factor-auth for your public UI
* Commitment to support (at least) maintained Django LTS versions

Installation, usage and contributing
====================================

Please see the documentation hosted on Read The Docs.

.. _django-two-factor-auth: https://django-two-factor-auth.readthedocs.io/en/stable/index.html

.. |build-status| image:: https://github.com/maykinmedia/maykin-2fa/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/maykin-2fa/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/maykinmedia/maykin-2fa/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/maykin-2fa/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/maykinmedia/maykin-2fa/branch/main/graph/badge.svg
    :target: https://app.codecov.io/gh/maykinmedia/maykin-2fa
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/maykin-2fa/badge/?version=latest
    :target: https://maykin-2fa.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/maykin-2fa.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/maykin-2fa.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/maykin-2fa.svg
    :target: https://pypi.org/project/maykin-2fa/
