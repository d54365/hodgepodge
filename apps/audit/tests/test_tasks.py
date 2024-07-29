from django.test import TestCase

from audit.models import LoginLog, OperationLog, ExceptionLog
from audit.tasks import save_operation_log, save_exception_log, save_login_log
from common.tests.setup import create_user


class AuditTaskTestCase(TestCase):
    def setUp(self):
        self.user = create_user()

        self.login_log_data = {
            "user_id": self.user.id,
            "ip": "127.0.0.1",
            "browser": "Chrome",
            "os": "Windows",
            "device": "PC",
            "login_result": LoginLog.LOGIN_RESULT_SUCCESS,
            "content": "Login successful",
        }

        self.operation_log_data = {
            "user_id": self.user.id,
            "ip": "127.0.0.1",
            "browser": "Chrome",
            "os": "Windows",
            "device": "PC",
            "api": "/api/test/",
            "start_at": "2023-01-01T12:00:00Z",
            "end_at": "2023-01-01T12:00:01Z",
            "duration": 1000,
            "status_code": 200,
            "response": {"message": "success"},
            "method": "GET",
            "query_params": {"key": "value"},
            "body": {"data": "test"},
            "headers": {"Authorization": "Bearer token"},
        }

        self.exception_log_data = {
            "context": {"user": "testuser"},
            "exception_stack": "Traceback details",
        }

    def test_save_login_log(self):
        save_login_log(self.login_log_data)
        login_log = LoginLog.objects.get(user=self.user)
        self.assertEqual(login_log.ip, "127.0.0.1")

    def test_save_operation_log(self):
        save_operation_log(self.operation_log_data)
        operation_log = OperationLog.objects.get(user=self.user)
        self.assertEqual(operation_log.api, "/api/test/")

    def test_save_exception_log(self):
        save_exception_log(self.exception_log_data)
        exception_log = ExceptionLog.objects.get(context__user="testuser")
        self.assertEqual(exception_log.exception_stack, "Traceback details")
