from auths.api.views import TokenObtainView, TokenRefreshView
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from ..api.urls import urlpatterns


class DiscoverTestCase(TestCase):
    def test_discovered(self):
        pass


class TestUrlsPatterns(SimpleTestCase):
    def setUp(self):
        self.patterns = [str(url.pattern) for url in urlpatterns]

    def test_auth_urls_included(self):
        self.assertIn("token-obtain/", self.patterns)

    def test_users_urls_included(self):
        self.assertIn("token-refresh/", self.patterns)


class TestUrlsNamespaces(SimpleTestCase):
    def setUp(self):
        self.token_obtain_url = "/api/v1/auth/token-obtain/"
        self.token_refresh_url = "/api/v1/auth/token-refresh/"

    def test_token_obtain_reverse(self):
        self.assertEqual(self.token_obtain_url, reverse("token-obtain"))

    def test_token_refresh_reverse(self):
        self.assertEqual(self.token_refresh_url, reverse("token-refresh"))


class TestUrlsRouting(SimpleTestCase):
    def setUp(self):
        self.token_obtain_url = "/api/v1/auth/token-obtain/"
        self.token_refresh_url = "/api/v1/auth/token-refresh/"
        self.token_obtain_resolver = resolve(self.token_obtain_url)
        self.token_refresh_resolver = resolve(self.token_refresh_url)

    def test_token_obtain_route(self):
        self.assertEqual(self.token_obtain_resolver.func.cls, TokenObtainView)

    def test_token_refresh_route(self):
        self.assertEqual(self.token_refresh_resolver.func.cls, TokenRefreshView)
