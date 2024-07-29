from typing import Optional

from django.contrib.auth.hashers import check_password

from .models import User
from .repositories import UserRepository


class UserService:
    @staticmethod
    def all_users():
        return UserRepository.all()

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        return UserRepository.get_by_username(username)

    @staticmethod
    def is_username_exists(username: str, instance: User = None) -> bool:
        return UserRepository.username_exists(username, instance)

    @staticmethod
    def is_mobile_exists(mobile: str, instance: User = None) -> bool:
        return UserRepository.mobile_exists(mobile, instance)

    @staticmethod
    def get_user_by_mobile(mobile: str) -> Optional[User]:
        return UserRepository.get_by_mobile(mobile)

    @staticmethod
    def create_user(data, created: User = None) -> User:
        user = UserRepository.create(data, created)
        return user

    @staticmethod
    def update_user(instance: User, data, updated: User = None) -> User:
        user = UserRepository.update(instance, data, updated)
        UserRepository.delete_cache(user)
        return user

    @staticmethod
    def update_last_login(instance: User) -> User:
        user = UserRepository.update_last_login_at(instance)
        UserRepository.delete_cache(user)
        return user

    @staticmethod
    def check_user_password(password: str, encoded: str) -> bool:
        return check_password(password, encoded)

    @staticmethod
    def delete_user(instance, deleted: User = None) -> None:
        UserRepository.delete(instance, deleted)
        UserRepository.delete_cache(instance)
