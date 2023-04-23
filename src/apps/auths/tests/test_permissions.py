from auths.api.permissions import IsVerified
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase


class IsVerifiedTestCase(TestCase):
    def setUp(self):
        self.permission = IsVerified()
        self.verified_user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="password",
            username="testuser",
        )
        self.verified_user.is_verified = True
        self.verified_user.save()
        self.unverified_user = get_user_model().objects.create_user(
            email="unverifieduser@example.com",
            password="password",
            username="unverifieduser",
        )
        self.factory = RequestFactory()

    def test_has_permission_authenticated_verified_user(self):
        request = self.factory.get("/test/")
        request.user = self.verified_user
        self.assertTrue(self.permission.has_permission(request, None))

    def test_has_permission_authenticated_unverified_user(self):
        request = self.factory.get("/test/")
        request.user = self.unverified_user
        self.assertFalse(self.permission.has_permission(request, None))

    def test_has_permission_unauthenticated_user(self):
        request = self.factory.get("/test/")
        request.user = AnonymousUser()
        self.assertFalse(self.permission.has_permission(request, None))


class DiscoverTestCase(TestCase):
    def test_discovered(self):
        pass
