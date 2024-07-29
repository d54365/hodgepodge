from typing import Optional

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.db import models
from django.utils import timezone

from common.constants.cache import CacheConstants
from .models import User


class UserRepository:
    @staticmethod
    def all() -> models.QuerySet:
        return User.objects.all().order_by("-id")

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        key = CacheConstants.USER.format(user_id=user_id)
        user = cache.get(key)
        if user:
            return user

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

        cache.set(key, user, CacheConstants.USER_TIMEOUT)
        return user

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        return user

    @staticmethod
    def username_exists(username: str, instance: User = None) -> bool:
        queryset = User.objects.filter(username=username)
        if instance is not None:
            queryset = queryset.exclude(id=instance.id)
        return queryset.exists()

    @staticmethod
    def mobile_exists(mobile: str, instance: User = None) -> bool:
        queryset = User.objects.filter(mobile=mobile)
        if instance is not None:
            queryset = queryset.exclude(id=instance.id)
        return queryset.exists()

    @staticmethod
    def get_by_mobile(mobile: str) -> Optional[User]:
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            return None
        return user

    @staticmethod
    def create(data, created: User = None) -> User:
        user = User.objects.create(
            username=data["username"],
            mobile=data["mobile"],
            password=make_password(data["password"]),
            name=data["name"],
            is_admin=data["is_admin"],
            created=created,
            created_name=created.name if created else "",
            updated=created,
            updated_name=created.name if created else "",
        )
        return user

    @staticmethod
    def update(instance: User, data, updated: User = None) -> User:
        instance.username = data["username"]
        instance.mobile = data["mobile"]
        instance.name = data["name"]
        instance.updated = updated
        instance.updated_name = updated.name if updated else ""
        instance.save()
        return instance

    @staticmethod
    def update_last_login_at(instance: User) -> User:
        instance.last_login_at = timezone.now()
        instance.save(update_fields=("last_login_at",))
        return instance

    @staticmethod
    def delete(instance, deleted: User = None) -> None:
        now = timezone.now().timestamp()
        instance.username = f"{instance.username}_del_{now}"
        instance.mobile = f"{instance.mobile}_del_{now}"
        instance.is_delete = True
        instance.updated = deleted
        instance.updated_name = deleted.name if deleted else ""
        instance.save(
            update_fields=(
                "username",
                "mobile",
                "is_delete",
                "updated",
                "updated_name",
                "updated_at",
            )
        )

    @staticmethod
    def delete_cache(user) -> None:
        cache.delete(CacheConstants.USER.format(user_id=user.id))
