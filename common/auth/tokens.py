from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken as RefreshToken_


class RefreshToken(RefreshToken_):
    @property
    def access_token(self):
        token = super().access_token

        # 添加自定义字段
        token["key"] = settings.SIMPLE_JWT["JWT_KEY"]

        return token
