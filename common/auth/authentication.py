from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from common.utils.header import HeaderUtil
from user.services import UserService


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = HeaderUtil.get_user_id(request)
        if not user_id:
            raise AuthenticationFailed(_("用户不存在"))

        return self.get_user(user_id), user_id

    @staticmethod
    def get_user(user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise AuthenticationFailed(_("用户不存在"))
        return user
