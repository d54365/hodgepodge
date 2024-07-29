from django.core.cache import cache
from django.test import TestCase

from common.constants.cache import CacheConstants
from common.tests.setup import create_user
from user.models import User
from user.repositories import UserRepository


class UserRepositoryTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.admin_user = create_user(
            username="admin", password="Admin@1234", is_admin=True
        )
        self.user_data = {
            "username": "newuser",
            "mobile": "12345678901",
            "password": "NewUser@1234",
            "name": "New User",
            "is_admin": False,
        }

    def test_get_all(self):
        users = UserRepository.all()
        self.assertTrue(len(users) > 0)

    def test_get_by_id(self):
        cache.delete(CacheConstants.USER.format(user_id=self.user.id))
        user = UserRepository.get_by_id(self.user.id)
        self.assertEqual(user.id, self.user.id)

    def test_get_by_id_with_cache(self):
        user = UserRepository.get_by_id(self.user.id)
        self.assertEqual(user.id, self.user.id)

    def test_get_by_username(self):
        user = UserRepository.get_by_username(self.user.username)
        self.assertEqual(user.username, self.user.username)

    def test_username_exists(self):
        exists = UserRepository.username_exists(self.user.username)
        self.assertTrue(exists)

    def test_username_exists_with_exclude(self):
        exists = UserRepository.username_exists(self.user.username, self.user)
        self.assertFalse(exists)

    def test_mobile_exists(self):
        exists = UserRepository.mobile_exists(self.user.mobile)
        self.assertTrue(exists)

    def test_mobile_exists_with_exclude(self):
        exists = UserRepository.mobile_exists(self.user.mobile, self.user)
        self.assertFalse(exists)

    def test_create(self):
        user = UserRepository.create(self.user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.user_data["username"])

    def test_update(self):
        updated_data = self.user_data.copy()
        updated_data["name"] = "Updated User"
        user = UserRepository.update(self.user, updated_data)
        self.assertEqual(user.name, "Updated User")

    def test_update_last_login_at(self):
        user = UserRepository.update_last_login_at(self.user)
        self.assertIsNotNone(user.last_login_at)

    def test_delete(self):
        UserRepository.delete(self.user, self.admin_user)
        user = UserRepository.get_by_id(self.user.id)
        self.assertIsNone(user)
