from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.auth.tokens import RefreshToken
from common.constants.cache import CacheConstants
from common.utils.random import RandomUtil
from user.services import UserService


class AccountAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("account-register")
        self.pwd_login_url = reverse("account-login-pwd")
        self.sms_code_url = reverse("account-sms-code")
        self.sms_code_login_url = reverse("account-login-sms-code")
        self.token_refresh_url = reverse("account-token-refresh")
        self.logout_url = reverse("account-logout")

        self.user_data = {
            "username": "testuser",
            "name": "Test User",
            "mobile": "13511111111",
            "password": "Test@1234",
            "is_admin": False,
        }

        self.user = UserService.create_user(self.user_data)
        self.user_data["password"] = "Test@1234"  # 原始密码用于登录测试

    def test_register(self):
        data = {**self.user_data, "username": "test001", "mobile": "13511111112"}
        response = self.client.post(self.register_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_password_login(self):
        response = self.client.post(
            self.pwd_login_url,
            data={
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_sms_code_request(self):
        response = self.client.post(
            self.sms_code_url, data={"mobile": self.user_data["mobile"]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("msg", response.data)

    def test_sms_code_login(self):
        # Simulate sending SMS code
        send_sms_code(self.user_data["mobile"])
        code = cache.get(
            CacheConstants.ACCOUNT_SMS_CODE.format(mobile=self.user_data["mobile"])
        )

        response = self.client.post(
            self.sms_code_login_url,
            data={"mobile": self.user_data["mobile"], "code": code},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        # First, login to get refresh token
        login_response = self.client.post(
            self.pwd_login_url,
            data={
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
            format="json",
        )
        refresh_token = login_response.data["refresh"]

        response = self.client.post(
            self.token_refresh_url, data={"refresh": refresh_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_logout(self):
        # 登陆验证在网关里统一认证, 然后在请求头里传递 USER_ID
        self.client.credentials(HTTP_X_USER_ID=str(self.user.id))

        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_with_existing_username(self):
        UserService.create_user(
            {
                "username": "duplicateuser",
                "name": "Duplicate User",
                "mobile": "12345678902",
                "password": "Test@1234",
                "is_admin": False,
            }
        )
        response = self.client.post(
            self.register_url,
            data={
                "username": "duplicateuser",
                "name": "New User",
                "mobile": "12345678903",
                "password": "Test@1234",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_register_with_existing_mobile(self):
        UserService.create_user(
            {
                "username": "newuser",
                "name": "New User",
                "mobile": "13000000000",
                "password": "Test@1234",
                "is_admin": False,
            }
        )
        response = self.client.post(
            self.register_url,
            data={
                "username": "anotheruser",
                "name": "Another User",
                "mobile": "13000000000",
                "password": "Test@1234",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("mobile", response.data)

    def test_login_with_invalid_password(self):
        response = self.client.post(
            self.pwd_login_url,
            data={"username": self.user_data["username"], "password": "WrongPassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_login_with_invalid_username(self):
        response = self.client.post(
            self.pwd_login_url,
            data={"username": "WrongUsername", "password": "WrongPassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_sms_code_request_with_too_many_requests(self):
        # Simulate multiple SMS code requests to hit the rate limit
        ip = "127.0.0.1"
        ip_limit_minute_key = CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_MINUTE.format(
            ip=ip
        )
        ip_limit_day_key = CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_DAY.format(ip=ip)
        mobile_limit_day_key = CacheConstants.ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY.format(
            mobile=self.user_data["mobile"]
        )

        cache.set(ip_limit_minute_key, 1)
        response = self.client.post(
            self.sms_code_url, data={"mobile": self.user_data["mobile"]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

        cache.delete(ip_limit_minute_key)
        cache.set(ip_limit_day_key, CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_DAY_MAX)
        response = self.client.post(
            self.sms_code_url, data={"mobile": self.user_data["mobile"]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

        cache.delete(ip_limit_day_key)
        cache.set(
            mobile_limit_day_key, CacheConstants.ACCOUNT_SMS_CODE_LIMIT_MOBILE_DAY_MAX
        )
        response = self.client.post(
            self.sms_code_url, data={"mobile": self.user_data["mobile"]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        cache.delete(mobile_limit_day_key)

        self.client.post(
            self.sms_code_url, data={"mobile": self.user_data["mobile"]}, format="json"
        )
        cache.delete(ip_limit_minute_key)

        self.client.post(
            self.sms_code_url, data={"mobile": self.user_data["mobile"]}, format="json"
        )

    def test_sms_code_request_with_invalid_mobile(self):
        ip = "127.0.0.1"
        cache.delete(CacheConstants.ACCOUNT_SMS_CODE_LIMIT_IP_MINUTE.format(ip=ip))
        response = self.client.post(
            self.sms_code_url, data={"mobile": "13900000000"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_sms_code(self):
        response = self.client.post(
            self.sms_code_login_url,
            data={"mobile": self.user_data["mobile"], "code": "000000"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("code", response.data)

    def test_login_with_invalid_mobile(self):
        code = RandomUtil.generate_number(6)
        mobile = "13800000000"

        cache.set(
            CacheConstants.ACCOUNT_SMS_CODE.format(mobile=mobile),
            code,
            CacheConstants.ACCOUNT_SMS_CODE_TIMEOUT,
        )

        response = self.client.post(
            self.sms_code_login_url,
            data={"mobile": mobile, "code": code},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("mobile", response.data)

    def test_token_refresh_with_invalid_refresh(self):
        response = self.client.post(
            self.token_refresh_url, data={"refresh": "WrongRefresh"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_token_refresh_with_not_exists_refresh(self):
        refresh = RefreshToken.for_user(self.user)  # noqa

        response = self.client.post(
            self.token_refresh_url, data={"refresh": str(refresh)}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Utils to simulate sending SMS code
def send_sms_code(mobile):
    code = RandomUtil.generate_number(6)
    cache.set(
        CacheConstants.ACCOUNT_SMS_CODE.format(mobile=mobile),
        code,
        CacheConstants.ACCOUNT_SMS_CODE_TIMEOUT,
    )
