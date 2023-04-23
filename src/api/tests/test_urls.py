from django.test import SimpleTestCase, TestCase

from ..urls import urlpatterns


class DiscoverTestCase(TestCase):
    def test_discovered(self):
        pass


class TestUrls(SimpleTestCase):
    def setUp(self):
        self.patterns = [str(url.pattern) for url in urlpatterns]

    def test_auth_urls_included(self):
        self.assertIn("auth/", self.patterns)

    def test_users_urls_included(self):
        self.assertIn("users/", self.patterns)
