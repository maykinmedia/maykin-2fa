==========
Test tools
==========

Enforcing multi-factor authentication creates some challenges in (integration) tests
for the admin, either with django's test :class:`django.test.Client` or with other
solutions like ``django-webtest``.

We have some guidelines and tools to make dealing with those difficulties much more
easy.

Built in helpers
================

Disabling MFA checks
--------------------

You can use the :func:`maykin_2fa.test.disable_admin_mfa` decorator/context manager to
automatically mark an authenticated user in the admin as verified. This uses the
``MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS`` setting under the hood.

It includes the authentication backends used by django-webtest, so you can use it
without any extra steps on ``WebTest``-based test cases.

Example:

.. code-block:: python

    from django_webtest import WebTest
    from maykin_2fa.test import disable_admin_mfa


    @disable_admin_mfa()
    class MyAdminTests(WebTest):

        def test_admin_index(self):
            user = User.objects.create_user(
                username="admin", password="password", is_staff=True
            )

            response = self.app.get(reverse("amdin:index"), user=user)

            self.assertEqual(response.status_code, 200)


TOTP token
----------

When a TOTP token device is set up for a user, you can easily generate a valid
authentication token using :func:`maykin_2fa.test.get_valid_totp_token`.

See :ref:`testing_recipes_factory_boy` for a code sample.


Recipes
=======

.. _testing_recipes_factory_boy:

Factory-boy
-----------

Factory-boy is a popular solution to generate realistic dummy data. You can leverage it
to also automatically set up a TOTP device to reflect a token generator second factor
by using the ``Trait`` feature from factory boy.

.. code-block:: python
   :caption: accounts/tests/factories.py

    # e.g. in accounts/tests/factories.py
    import factory
    from django_otp.util import random_hex


    class TOTPDeviceFactory(factory.django.DjangoModelFactory):
        user = factory.SubFactory("accounts.tests.factories.UserFactory")
        key = factory.LazyAttribute(lambda o: random_hex())

        class Meta:
            model = "otp_totp.TOTPDevice"


    class UserFactory(factory.django.DjangoModelFactory):
        username = factory.Sequence(lambda n: f"user-{n}")
        password = factory.PostGenerationMethodCall("set_password", "secret")

        class Meta:
            model = "accounts.User"

        class Params:
            with_totp_device = factory.Trait(
                device=factory.RelatedFactory(
                    TOTPDeviceFactory,
                    "user",
                    name="default",
                )
            )

And then you can use it as:

.. code-block:: python
   :caption: tests/test_something.py

    from maykin_2fa.test ipmort get_valid_totp_token
    from two_factor.utils import default_device, totp_digits

    from accounts.tests.factories import UserFactory

    user = UserFactory.create(with_totp_device=True)
    token = get_valid_totp_token(user)
    assert isinstance(token, str)
