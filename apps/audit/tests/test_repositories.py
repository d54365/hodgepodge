from django.test import TestCase

from audit.models import LoginLog, OperationLog, ExceptionLog
from audit.repositories import (
    LoginLogRepository,
    OperationLogRepository,
    ExceptionLogRepository,
)
from common.tests.setup import create_user


class AuditRepositoryTestCase(TestCase):
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
        login_log = LoginLogRepository.create(self.login_log_data)
        self.assertIsInstance(login_log, LoginLog)

    def test_get_login_log_by_pk(self):
        login_log = LoginLogRepository.create(self.login_log_data)
        fetched_log = LoginLogRepository.get_by_pk(login_log.id)
        self.assertEqual(fetched_log.id, login_log.id)

    def test_get_all_login_logs(self):
        LoginLogRepository.create(self.login_log_data)
        logs = LoginLogRepository.all()
        self.assertGreaterEqual(logs.count(), 1)

    def test_create_operation_log(self):
        operation_log = OperationLogRepository.create(self.operation_log_data)
        self.assertIsInstance(operation_log, OperationLog)

    def test_get_operation_log_by_pk(self):
        operation_log = OperationLogRepository.create(self.operation_log_data)
        fetched_log = OperationLogRepository.get_by_pk(operation_log.id)
        self.assertEqual(fetched_log.id, operation_log.id)

    def test_get_all_operation_logs(self):
        OperationLogRepository.create(self.operation_log_data)
        logs = OperationLogRepository.all()
        self.assertGreaterEqual(logs.count(), 1)

    def test_create_exception_log(self):
        exception_log = ExceptionLogRepository.create(self.exception_log_data)
        self.assertIsInstance(exception_log, ExceptionLog)

    def test_get_exception_log_by_pk(self):
        exception_log = ExceptionLogRepository.create(self.exception_log_data)
        fetched_log = ExceptionLogRepository.get_by_pk(exception_log.id)
        self.assertEqual(fetched_log.id, exception_log.id)

    def test_get_all_exception_logs(self):
        ExceptionLogRepository.create(self.exception_log_data)
        logs = ExceptionLogRepository.all()
        self.assertGreaterEqual(logs.count(), 1)

    def test_get_login_log_by_invalid_pk(self):
        fetched_log = LoginLogRepository.get_by_pk(1111111)
        self.assertIsNone(fetched_log)

    def test_get_operation_log_by_invalid_pk(self):
        fetched_log = OperationLogRepository.get_by_pk(1111111)
        self.assertIsNone(fetched_log)

    def test_get_exception_log_invalid_pk(self):
        fetched_log = ExceptionLogRepository.get_by_pk(1111111)
        self.assertIsNone(fetched_log)
