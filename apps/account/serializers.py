from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings

from common.auth.tokens import RefreshToken
from common.constants.cache import CacheConstants
from common.constants.regex import RegexConstants
from common.utils.header import HeaderUtil
from user.services import UserService


class RegisterInputSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=RegexConstants.USERNAME,
        error_messages={
            "invalid": _(
                "请输入正确的用户名, 规则为: 3到16位(字母，数字，下划线，减号)"
            )
        },
    )
    name = serializers.CharField(max_length=32, min_length=2)
    mobile = serializers.RegexField(
        regex=RegexConstants.MOBILE,
        error_messages={
            "invalid": _("请输入正确的手机号"),
        },
    )
    password = serializers.RegexField(
        regex=RegexConstants.PASSWORD,
        error_messages={
            "invalid": _(
                "请输入正确的密码, 规则为: 密码必须包含至少一个小写字母、一个大写字母和一个数字，且长度在6到16位之间"
            )
        },
    )

    @staticmethod
    def validate_username(username):
        if UserService.is_username_exists(username):
            raise ValidationError({"username": _("用户名已被使用")})
        return username

    @staticmethod
    def validate_mobile(mobile):
        if UserService.is_mobile_exists(mobile):
            raise ValidationError({"mobile": _("手机号已被使用")})
        return mobile

    def create(self, validated_data):
        validated_data["is_admin"] = False
        return UserService.create_user(validated_data)


class PwdLoginInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=16)

    def validate(self, attrs):
        user = UserService.get_user_by_username(attrs["username"])
        if not user:
            raise ValidationError({"password": _("用户不存在或密码错误")})

        if not UserService.check_user_password(attrs["password"], user.password):
            raise ValidationError({"password": _("用户不存在或密码错误")})

        attrs["user"] = user

        return attrs


class TokenRefreshInputSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, refresh):
        request = self.context["request"]

        try:
            refresh_token = RefreshToken(refresh)
            user_id = refresh_token[api_settings.USER_ID_CLAIM]
        except TokenError:
            raise AuthenticationFailed("token decode error")

        if (
            cache.get(
                CacheConstants.USER_JWT_REFRESH_TOKEN.format(
                    device=request.user_agent.device.family, user_id=user_id
                )
            )
            != refresh
        ):
            raise AuthenticationFailed(_("token is invalid"))

        return refresh_token


class SMSCodeInputSerializer(serializers.Serializer):
    mobile = serializers.RegexField(
        regex=RegexConstants.MOBILE,
        error_messages={"invalid": _("手机号格式错误")},
    )

    def validate(self, attrs):
        request = self.context["request"]
        mobile = attrs["mobile"]

        ip = HeaderUtil.get_client_ip(request)

        if cache.has_key(CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_MINUTE.format(ip=ip)):
            raise ValidationError({"error": _("短信发送频率过快~")})

        day_ip_count = cache.get(
            CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_DAY.format(ip=ip)
        )
        if (
            day_ip_count
            and day_ip_count >= CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_DAY_MAX
        ):
            raise ValidationError(
                {
                    "error": _(
                        f"一天最多只能发送{CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_DAY_MAX}次"
                    )
                },
            )

        day_mobile_count = cache.get(
            CacheConstants.ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY.format(mobile=mobile)
        )
        if (
            day_mobile_count
            and day_mobile_count >= CacheConstants.ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY_MAX
        ):
            raise ValidationError(
                {
                    "error": _(
                        f"一天最多只能发送{CacheConstants.ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY_MAX}次"
                    )
                },
            )

        if not UserService.is_mobile_exists(mobile):
            raise ValidationError({"mobile": _("用户未注册")})

        attrs["ip"] = ip
        return attrs


class SMSCodeLoginInputSerializer(serializers.Serializer):
    mobile = serializers.RegexField(
        regex=RegexConstants.MOBILE,
        error_messages={"invalid": _("手机号格式错误")},
    )
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        mobile = attrs["mobile"]

        key = CacheConstants.ACCOUNT_SMS_CODE.format(mobile=mobile)
        value = cache.get(key)
        if value != attrs["code"]:
            raise ValidationError({"code": _("验证码错误")})

        user = UserService.get_user_by_mobile(mobile)
        if not user:
            raise ValidationError({"mobile": _("用户未注册")})

        cache.delete(key)

        attrs["user"] = user
        return attrs
