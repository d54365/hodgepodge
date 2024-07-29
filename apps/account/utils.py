import datetime

from django.core.cache import cache
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.settings import api_settings

from audit.models import LoginLog
from audit.tasks import save_login_log
from common.auth.tokens import RefreshToken
from common.constants.cache import CacheConstants
from common.utils.header import HeaderUtil
from common.utils.timezone import TimezoneUtil
from user.services import UserService


class AccountHelper:
    @classmethod
    def login(cls, request, serializer):
        user_agent = request.user_agent
        login_log_data = {
            "ip": HeaderUtil.get_client_ip(request),
            "browser": user_agent.browser.family,
            "os": user_agent.os.family,
            "device": user_agent.device.family,
            "login_result": LoginLog.LOGIN_RESULT_FAILED,
            "user_id": None,
        }

        serializer = serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=False)
        if serializer.errors:
            login_log_data["content"] = serializer.errors
            save_login_log.delay(login_log_data)
            raise ValidationError(serializer.errors)

        user = serializer.validated_data["user"]
        login_log_data["user_id"] = user.id
        login_log_data["login_result"] = LoginLog.LOGIN_RESULT_SUCCESS
        save_login_log.delay(login_log_data)

        return cls.get_login_data(request, user)

    @staticmethod
    def get_login_data(request, user):
        UserService.update_last_login(user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)  # noqa

        access_expire_second = int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds())
        refresh_expire_second = int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds())
        cache.set(
            CacheConstants.USER_JWT_REFRESH_TOKEN.format(
                device=request.user_agent.device.family,
                user_id=user.id,
            ),
            str(refresh),
            refresh_expire_second,
        )

        now = timezone.now()
        ret = {
            "access": access_token,
            "access_expire_at": TimezoneUtil.convert_utc_to_local(
                now + datetime.timedelta(seconds=access_expire_second),
            ),
            "refresh": str(refresh),
            "refresh_expire_at": TimezoneUtil.convert_utc_to_local(
                now + datetime.timedelta(seconds=refresh_expire_second),
            ),
        }

        return ret
