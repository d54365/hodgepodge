from common.utils.random import RandomUtil
from user.services import UserService


def create_user(username="testuser", password="Test@1234", is_admin=False):
    return UserService.create_user(
        {
            "username": username,
            "name": "Test User",
            "mobile": f"13{RandomUtil.generate_number(9)}",
            "password": password,
            "is_admin": is_admin,
        }
    )
