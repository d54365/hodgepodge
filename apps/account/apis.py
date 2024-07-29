import datetime

from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings

from common.auth.authentication import JWTAuthentication
from common.constants.cache import CacheConstants
from common.utils.timezone import TimezoneUtil
from .serializers import (
    RegisterInputSerializer,
    PwdLoginInputSerializer,
    TokenRefreshInputSerializer,
    SMSCodeInputSerializer,
    SMSCodeLoginInputSerializer,
)
from .tasks import send_sms_code
from .utils import AccountHelper


class UserAccountViewSet(viewsets.ViewSet):
    @action(methods=["POST"], detail=False, url_path="register")
    def register(self, request):
        serializer = RegisterInputSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(AccountHelper.get_login_data(request, user))

    @action(methods=["POST"], detail=False, url_path="login/pwd")
    def login_pwd(self, request):
        return Response(AccountHelper.login(request, PwdLoginInputSerializer))

    @action(methods=["POST"], detail=False, url_path="sms-code")
    def sms_code(self, request):
        serializer = SMSCodeInputSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        ip = serializer.validated_data["ip"]

        send_sms_code.delay(mobile)

        cache.set(
            CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_MINUTE.format(ip=ip),
            1,
            timeout=CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_MINUTE_TIMEOUT,
        )

        # 短信发送限制
        day_ip_key = CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_DAY.format(ip=ip)
        if cache.has_key(day_ip_key):
            cache.incr(day_ip_key)
        else:
            cache.set(
                day_ip_key, 1, CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_DAY_TIMEOUT
            )

        day_mobile_key = CacheConstants.ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY.format(
            mobile=mobile
        )
        if cache.has_key(day_mobile_key):
            cache.incr(day_mobile_key)
        else:
            cache.set(
                day_mobile_key,
                1,
                CacheConstants.ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY_TIMEOUT,
            )

        return Response({"msg": _("短信发送成功")})

    @action(methods=["POST"], detail=False, url_path="login/sms-code")
    def login_sms_code(self, request):
        return Response(AccountHelper.login(request, SMSCodeLoginInputSerializer))

    @action(methods=["POST"], detail=False, url_path="token-refresh")
    def token_refresh(self, request):
        serializer = TokenRefreshInputSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        access = str(refresh_token.access_token)
        access_expire_second = int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds())
        return Response(
            {
                "access": access,
                "access_expire_at": TimezoneUtil.convert_utc_to_local(
                    timezone.now() + datetime.timedelta(seconds=access_expire_second),
                ),
            }
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path="logout",
        authentication_classes=(JWTAuthentication,),
    )
    def logout(self, request):
        cache.delete(
            CacheConstants.USER_JWT_REFRESH_TOKEN.format(
                device=request.user_agent.device.family, user_id=request.user.id
            )
        )
        return Response()
