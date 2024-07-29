from celery import shared_task

from .services import OperationLogService, ExceptionLogService, LoginLogService


@shared_task
def save_operation_log(data):
    OperationLogService.create(data)


@shared_task
def save_exception_log(data):
    ExceptionLogService.create(data)


@shared_task
def save_login_log(data):
    LoginLogService.create(data)
