from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from audit.models import LoginLog, OperationLog, ExceptionLog
from common.tests.setup import create_user


class AuditAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = create_user(
            username="admin", password="Admin@1234", is_admin=True
        )
        self.regular_user = create_user(
            username="user", password="User@1234", is_admin=False
        )
        self.client = APIClient()

        self.login_log = LoginLog.objects.create(
            user=self.admin_user,
            ip="127.0.0.1",
            browser="Chrome",
            os="Windows",
            device="PC",
            login_result=LoginLog.LOGIN_RESULT_SUCCESS,
            content="Login successful",
        )

        self.operation_log = OperationLog.objects.create(
            user=self.admin_user,
            ip="127.0.0.1",
            browser="Chrome",
            os="Windows",
            device="PC",
            api="/api/test/",
            start_at="2023-01-01T12:00:00Z",
            end_at="2023-01-01T12:00:01Z",
            duration=1000,
            status_code=200,
            response={"message": "success"},
            method="GET",
            query_params={"key": "value"},
            body={"data": "test"},
            headers={"Authorization": "Bearer token"},
        )

        self.exception_log = ExceptionLog.objects.create(
            context={"user": "testuser"}, exception_stack="Traceback details"
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_get_login_logs_as_admin(self):
        self.authenticate(self.admin_user)
        response = self.client.get(reverse("audit_login-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_login_logs_as_regular_user(self):
        self.authenticate(self.regular_user)
        response = self.client.get(reverse("audit_login-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_operation_logs_as_admin(self):
        self.authenticate(self.admin_user)
        response = self.client.get(reverse("audit_operation-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_operation_logs_as_regular_user(self):
        self.authenticate(self.regular_user)
        response = self.client.get(reverse("audit_operation-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_exception_logs_as_admin(self):
        self.authenticate(self.admin_user)
        response = self.client.get(reverse("audit_exception_log-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_exception_logs_as_regular_user(self):
        self.authenticate(self.regular_user)
        response = self.client.get(reverse("audit_exception_log-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
