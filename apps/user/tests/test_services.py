from django.test import TestCase

from common.tests.setup import create_user
from user.models import User
from user.services import UserService


class UserServiceTestCase(TestCase):
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

    def test_get_all_users(self):
        users = UserService.all_users()
        self.assertTrue(len(users) > 0)

    def test_get_user_by_id(self):
        user = UserService.get_user_by_id(self.user.id)
        self.assertEqual(user.id, self.user.id)

    def test_get_user_by_username(self):
        user = UserService.get_user_by_username(self.user.username)
        self.assertEqual(user.username, self.user.username)

    def test_is_username_exists(self):
        exists = UserService.is_username_exists(self.user.username)
        self.assertTrue(exists)

    def test_is_username_exists_with_exclude(self):
        exists = UserService.is_username_exists(self.user.username, self.user)
        self.assertFalse(exists)

    def test_is_mobile_exists(self):
        exists = UserService.is_mobile_exists(self.user.mobile)
        self.assertTrue(exists)

    def test_is_mobile_exists_with_exclude(self):
        exists = UserService.is_mobile_exists(self.user.mobile, self.user)
        self.assertFalse(exists)

    def test_create_user(self):
        user = UserService.create_user(self.user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.user_data["username"])

    def test_update_user(self):
        updated_data = self.user_data.copy()
        updated_data["name"] = "Updated User"
        user = UserService.update_user(self.user, updated_data)
        self.assertEqual(user.name, "Updated User")

    def test_update_last_login(self):
        user = UserService.update_last_login(self.user)
        self.assertIsNotNone(user.last_login_at)

    def test_check_user_password(self):
        is_valid = UserService.check_user_password("Test@1234", self.user.password)
        self.assertTrue(is_valid)

    def test_delete_user(self):
        UserService.delete_user(self.user, self.admin_user)
        deleted_user = UserService.get_user_by_id(self.user.id)
        self.assertIsNone(deleted_user)
