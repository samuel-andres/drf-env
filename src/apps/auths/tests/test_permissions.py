from auths.api.permissions import IsVerified
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from core.factories.users_factories import UserFactory


class IsVerifiedTestCase(TestCase):
    def setUp(self):
        self.permission = IsVerified()
        self.verified_user = UserFactory(is_verified=True)
        self.unverified_user = UserFactory(is_verified=False)
        self.request_factory = RequestFactory()

    def test_has_permission_authenticated_verified_user(self):
        request = self.request_factory.get("/test/")
        request.user = self.verified_user
        self.assertTrue(self.permission.has_permission(request, None))

    def test_has_permission_authenticated_unverified_user(self):
        request = self.request_factory.get("/test/")
        request.user = self.unverified_user
        self.assertFalse(self.permission.has_permission(request, None))

    def test_has_permission_unauthenticated_user(self):
        request = self.request_factory.get("/test/")
        request.user = AnonymousUser()
        self.assertFalse(self.permission.has_permission(request, None))


class DiscoverTestCase(TestCase):
    def test_discovered(self):
        pass
