from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class TokenObtainViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.token_obtain_url = "/api/v1/auth/token-obtain/"
        get_user_model().objects.create_user(
            email="validuser@email.com", password="validpassword", username="validusername"
        )

    def test_token_obtain_view_returns_tokens(self):
        response = self.client.post(
            self.token_obtain_url,
            {
                "email": "validuser@email.com",
                "password": "validpassword",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain_view_returns_error_on_invalid_credentials(self):
        response = self.client.post(
            self.token_obtain_url,
            {
                "email": "invaliduser@email.com",
                "password": "invalidpassword",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)


class TokenRefreshViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.token_refresh_url = "/api/v1/auth/token-refresh/"
        self.user = get_user_model().objects.create_user(
            email="user@email.com", password="password", username="username"
        )
        self.refresh_token = RefreshToken.for_user(self.user)

    def test_token_refresh_view_returns_access_token(self):
        response = self.client.post(
            self.token_refresh_url,
            {
                "refresh": str(self.refresh_token),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_token_refresh_view_returns_refresh_token(self):
        response = self.client.post(
            self.token_refresh_url,
            {
                "refresh": str(self.refresh_token),
            },
        )

        self.assertEqual(response.status_code, 200)
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


class TokenIsVerifiedView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.token_obtain_url = "/api/v1/auth/token-obtain/"
        self.is_verified_url = "/api/v1/auth/is-verified/"
        get_user_model().objects.create_superuser(
            email="validuser@email.com",
            password="validpassword",
            username="validusername",
        )
        self.response = self.client.post(
            self.token_obtain_url,
            {
                "email": "validuser@email.com",
                "password": "validpassword",
            },
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
