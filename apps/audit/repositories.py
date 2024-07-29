from .models import LoginLog, OperationLog, ExceptionLog


class LoginLogRepository:
    @staticmethod
    def get_by_pk(pk):
        try:
            return LoginLog.objects.get(id=pk)
        except LoginLog.DoesNotExist:
            return None

    @staticmethod
    def all():
        return LoginLog.objects.all().order_by("-id")

    @staticmethod
    def create(data):
        return LoginLog.objects.create(**data)


class OperationLogRepository:
    @staticmethod
    def get_by_pk(pk):
        try:
            return OperationLog.objects.get(id=pk)
        except OperationLog.DoesNotExist:
            return None

    @staticmethod
    def all():
        return OperationLog.objects.all().order_by("-id")

    @staticmethod
    def create(data):
        return OperationLog.objects.create(**data)


class ExceptionLogRepository:
    @staticmethod
    def get_by_pk(pk):
        try:
            return ExceptionLog.objects.get(id=pk)
        except ExceptionLog.DoesNotExist:
            return None

    @staticmethod
    def all():
        return ExceptionLog.objects.all().order_by("-id")

    @staticmethod
    def create(data):
        return ExceptionLog.objects.create(**data)
