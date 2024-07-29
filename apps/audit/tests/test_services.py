from django.test import TestCase

from audit.models import LoginLog, OperationLog, ExceptionLog
from audit.services import LoginLogService, OperationLogService, ExceptionLogService
from common.tests.setup import create_user


class AuditServiceTestCase(TestCase):
    def setUp(self):
        self.user = create_user()

        self.login_log_data = {
            "user": self.user,
            "ip": "127.0.0.1",
            "browser": "Chrome",
            "os": "Windows",
            "device": "PC",
            "login_result": LoginLog.LOGIN_RESULT_SUCCESS,
            "content": "Login successful",
        }

        self.operation_log_data = {
            "user": self.user,
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

    def test_create_login_log(self):
        login_log = LoginLogService.create(self.login_log_data)
        self.assertIsInstance(login_log, LoginLog)

    def test_get_login_log_by_pk(self):
        login_log = LoginLogService.create(self.login_log_data)
        fetched_log = LoginLogService.get_by_pk(login_log.id)
        self.assertEqual(fetched_log.id, login_log.id)

    def test_get_all_login_logs(self):
        LoginLogService.create(self.login_log_data)
        logs = LoginLogService.all()
        self.assertGreaterEqual(logs.count(), 1)

    def test_create_operation_log(self):
        operation_log = OperationLogService.create(self.operation_log_data)
        self.assertIsInstance(operation_log, OperationLog)

    def test_get_operation_log_by_pk(self):
        operation_log = OperationLogService.create(self.operation_log_data)
        fetched_log = OperationLogService.get_by_pk(operation_log.id)
        self.assertEqual(fetched_log.id, operation_log.id)

    def test_get_all_operation_logs(self):
        OperationLogService.create(self.operation_log_data)
        logs = OperationLogService.all()
        self.assertGreaterEqual(logs.count(), 1)

    def test_create_exception_log(self):
        exception_log = ExceptionLogService.create(self.exception_log_data)
        self.assertIsInstance(exception_log, ExceptionLog)

    def test_get_exception_log_by_pk(self):
        exception_log = ExceptionLogService.create(self.exception_log_data)
        fetched_log = ExceptionLogService.get_by_pk(exception_log.id)
        self.assertEqual(fetched_log.id, exception_log.id)

    def test_get_all_exception_logs(self):
        ExceptionLogService.create(self.exception_log_data)
        logs = ExceptionLogService.all()
        self.assertGreaterEqual(logs.count(), 1)
