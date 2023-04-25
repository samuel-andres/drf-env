from auths.api.serializers import TokenObtainSerializer
from django.test import TestCase

from core.factories.users_factories import UserFactory


class TokenObtainSerializerTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_get_token_contains_username(self):
        serializer = TokenObtainSerializer()
        token = serializer.get_token(self.user)

        self.assertEqual(token["username"], self.user.username)


class DiscoverTestCase(TestCase):
    def test_discovered(self):
        pass
