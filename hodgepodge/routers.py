from django.conf import settings
from rest_framework import routers

from account import apis as account_apis
from audit import apis as audit_apis
from user import apis as user_apis

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register("api/account", account_apis.UserAccountViewSet, basename="account")

router.register("api/user", user_apis.UserInfoViewSet, basename="user")

router.register("api/audit/login", audit_apis.LoginLogViewSet, basename="audit_login")
router.register(
    "api/audit/operation", audit_apis.OperationLogViewSet, basename="audit_operation"
)
router.register(
    "api/audit/exception",
    audit_apis.ExceptionLogViewSet,
    basename="audit_exception_log",
)
