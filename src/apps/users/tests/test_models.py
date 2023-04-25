from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import DataError, IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from factory.fuzzy import FuzzyText

from core.factories.users_factories import UserFactory


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.email = "test@email.com"
        self.username = "username"
        self.exceeded_username = FuzzyText(length=151)
        self.exceeded_first_name = FuzzyText(length=151)
        self.exceeded_last_name = FuzzyText(length=151)

    def test_email_field_is_unique(self):
        UserFactory(email=self.email)
        with self.assertRaises(IntegrityError):
            UserFactory(email=self.email)

    def test_username_field_is_unique(self):
        UserFactory(username=self.username)
        with self.assertRaises(IntegrityError):
            UserFactory(username=self.username)

    def test_username_field_length_exceeds_limit(self):
        with self.assertRaises(DataError):
            UserFactory(username=self.exceeded_username)

    def test_first_name_field_length_exceeds_limit(self):
        with self.assertRaises(DataError):
            UserFactory(first_name=self.exceeded_first_name)

    def test_last_name_field_length_exceeds_limit(self):
        with self.assertRaises(DataError):
            UserFactory(first_name=self.exceeded_last_name)

    def test_start_date_field_is_today_by_default(self):
        user = UserFactory(start_date=self.user_model._meta.get_field("start_date").get_default())
        self.assertEquals(user.start_date.date(), datetime.now().date())

    def test_is_verifield_field_is_false_by_default(self):
        user = UserFactory(is_verified=self.user_model._meta.get_field("is_verified").get_default())
        self.assertFalse(user.is_verified)

    def test__str__returns_username(self):
        user = UserFactory(username="somename")
        self.assertEquals(str(user), user.username)


class UserManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.user_data = dict(email="testuser@example.com", password="testpassword")

    def test_successful_create_user_with_just_email_and_password(self):
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_fail_creating_user_without_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password=self.user_data["password"])
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password=self.user_data["password"])
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(password=self.user_data["password"])

    def test_fail_creating_user_with_invalid_password(self):
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(email=self.user_data["email"], password="")

    def test_fail_creating_user_without_password(self):
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(email=self.user_data["email"])

    def test_create_user_returns_user_instance(self):
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertIsInstance(user, get_user_model())

    def test_create_user_is_saved_in_db(self):
        self.assertFalse(get_user_model().objects.all().exists())
        get_user_model().objects.create_user(**self.user_data)
        self.assertTrue(get_user_model().objects.all().exists())

    def test_create_superuser_creates_superuser(self):
        user = get_user_model().objects.create_superuser(**self.user_data)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_creates_verified_user(self):
        user = get_user_model().objects.create_superuser(**self.user_data)
        self.assertTrue(user.is_verified)


class DiscoverTestCase(TestCase):
    def test_discovered(self):
        pass
