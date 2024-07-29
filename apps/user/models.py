from django.db import models

from common.models.base import BaseModel, BaseManager, ForeignKey


class User(BaseModel):
    username = models.CharField(max_length=64, verbose_name="用户名", unique=True)
    mobile = models.CharField(max_length=64, verbose_name="手机号", unique=True)
    password = models.CharField(max_length=128, verbose_name="密码")
    name = models.CharField(max_length=32, verbose_name="姓名")
    last_login_at = models.DateTimeField(null=True, verbose_name="上次登陆时间")
    is_admin = models.BooleanField(default=False, verbose_name="是否是管理员")
    created = ForeignKey("self", verbose_name="创建人", related_name="user_created")
    updated = ForeignKey("self", verbose_name="上次修改人", related_name="user_updated")
    created_name = models.CharField(max_length=32)
    updated_name = models.CharField(max_length=32, default="")

    objects = BaseManager()

    @property
    def is_authenticated(self):
        return True
