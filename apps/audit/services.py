from .repositories import (
    LoginLogRepository,
    OperationLogRepository,
    ExceptionLogRepository,
)


class LoginLogService:
    @staticmethod
    def get_by_pk(pk):
        return LoginLogRepository.get_by_pk(pk)

    @staticmethod
    def all():
        return LoginLogRepository.all()

    @staticmethod
    def create(data):
        return LoginLogRepository.create(data)


class OperationLogService:
    @staticmethod
    def get_by_pk(pk):
        return OperationLogRepository.get_by_pk(pk)

    @staticmethod
    def all():
        return OperationLogRepository.all()

    @staticmethod
    def create(data):
        return OperationLogRepository.create(data)


class ExceptionLogService:
    @staticmethod
    def get_by_pk(pk):
        return ExceptionLogRepository.get_by_pk(pk)

    @staticmethod
    def all():
        return ExceptionLogRepository.all()

    @staticmethod
    def create(data):
        return ExceptionLogRepository.create(data)
