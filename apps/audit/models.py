from django.db import models

from common.models.base import BaseModel, ForeignKey, BaseManager
from user.models import User


class LoginLog(BaseModel):
    LOGIN_RESULT_SUCCESS = 0
    LOGIN_RESULT_FAILED = 1
    LOGIN_RESULT_CHOICES = (
        (LOGIN_RESULT_SUCCESS, "成功"),
        (LOGIN_RESULT_FAILED, "失败"),
    )

    user = ForeignKey(User, related_name="audit_login_log_user")
    ip = models.GenericIPAddressField(verbose_name="IP")
    browser = models.CharField(max_length=128, default="")
    os = models.CharField(max_length=128, default="")
    device = models.CharField(max_length=128, default="")
    login_result = models.PositiveSmallIntegerField(
        choices=LOGIN_RESULT_CHOICES, verbose_name="登陆结果"
    )
    content = models.CharField(max_length=128, verbose_name="登陆失败原因", default="")

    objects = BaseManager()


class OperationLog(BaseModel):
    user = ForeignKey(User, related_name="audit_operation_log_user")
    ip = models.GenericIPAddressField(verbose_name="IP")
    browser = models.CharField(max_length=128, default="")
    os = models.CharField(max_length=128, default="")
    device = models.CharField(max_length=128, default="")
    api = models.CharField(max_length=128, verbose_name="请求地址", db_index=True)
    start_at = models.DateTimeField(verbose_name="请求开始时间")
    end_at = models.DateTimeField(verbose_name="请求响应时间")
    duration = models.IntegerField(verbose_name="响应耗时(毫秒)")
    status_code = models.IntegerField(verbose_name="状态码", db_index=True)
    response = models.JSONField(null=True, verbose_name="返回值")
    method = models.CharField(max_length=32, verbose_name="请求方式")
    query_params = models.JSONField(null=True)
    body = models.JSONField(verbose_name="请求体", null=True)
    headers = models.JSONField(verbose_name="请求头")

    objects = BaseManager()


class ExceptionLog(BaseModel):
    context = models.JSONField(null=True, verbose_name="上下文")
    exception_stack = models.TextField(verbose_name="异常堆栈")

    objects = BaseManager()
