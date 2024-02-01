from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from maykin_2fa.test import disable_admin_mfa


class TestHelperTests(TestCase):

    def test_mfa_disabling(self):
        User.objects.create_user(username="johny", password="password", is_staff=True)
        self.client.login(username="johny", password="password")

        with disable_admin_mfa():
            response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
