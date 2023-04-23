from auths.api.serializers import TokenObtainSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase


class TokenObtainSerializerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@email.com", username="testuser", password="testpassword"
        )

    def test_get_token_contains_username(self):
        serializer = TokenObtainSerializer()
        token = serializer.get_token(self.user)

        self.assertEqual(token["username"], self.user.username)


class DiscoverTestCase(TestCase):
    def test_discovered(self):
        pass
