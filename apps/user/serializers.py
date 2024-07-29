from rest_framework import serializers

from .models import User


class UserInfoOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "name", "mobile", "is_admin", "last_login_at")
