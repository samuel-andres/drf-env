from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.factories.users_factories import UserFactory


class TokenObtainViewTest(TestCase):
    def setUp(self):
        UserFactory(email="validuser@email.com", password="validpassword")
        self.client = APIClient()
        self.token_obtain_url = "/api/v1/auth/token-obtain/"
        self.valid_payload = {
            "email": "validuser@email.com",
            "password": "validpassword",
        }
        self.invalid_payload = {
            "email": "invaliduser@email.com",
            "password": "invalidpassword",
        }

    def test_token_obtain_view_returns_tokens(self):
        response = self.client.post(self.token_obtain_url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain_view_returns_error_on_invalid_credentials(self):
        response = self.client.post(self.token_obtain_url, self.invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)


class TokenRefreshViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.token_refresh_url = "/api/v1/auth/token-refresh/"
        self.refresh_token = RefreshToken.for_user(UserFactory())

    def test_token_refresh_view_returns_access_token(self):
        response = self.client.post(
            self.token_refresh_url,
            {
                "refresh": str(self.refresh_token),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_refresh_view_returns_refresh_token(self):
        response = self.client.post(
            self.token_refresh_url,
            {
                "refresh": str(self.refresh_token),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)

    def test_token_refresh_blacklist_used_token(self):
        self.client.post(
            self.token_refresh_url,
            {
                "refresh": str(self.refresh_token),
            },
        )

        response = self.client.post(
            self.token_refresh_url,
            {
                "refresh": str(self.refresh_token),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals("Token is blacklisted", response.data["detail"])

    def test_token_refresh_view_returns_error_on_invalid_refresh_token(self):
        response = self.client.post(
            self.token_refresh_url,
            {
                "refresh": "invalidtoken",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals("Token is invalid or expired", response.data["detail"])


class TokenIsVerifiedViewTest(TestCase):
    def setUp(self):
        UserFactory(email="validuser@email.com", password="validpassword", is_verified=True)
        self.client = APIClient()
        self.token_obtain_url = "/api/v1/auth/token-obtain/"
        self.is_verified_url = "/api/v1/auth/is-verified/"
        self.valid_payload = {
            "email": "validuser@email.com",
            "password": "validpassword",
        }
        self.response = self.client.post(
            self.token_obtain_url,
            self.valid_payload,
        )
        self.access_token = self.response.data["access"]

    def test_token_is_valid(self):
        response = self.client.get(
            self.is_verified_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DiscoverTestCase(TestCase):
    def test_discovered(self):
        pass
