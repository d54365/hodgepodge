from common.auth.authentication import JWTAuthentication
from common.auth.permissions import AdminPermission
from common.drf.viewsets import ReadOnlyModelViewSet
from .serializers import (
    LoginLogOutputSerializer,
    OperationLogOutputSerializer,
    ExceptionLogOutputSerializer,
)
from .services import (
    LoginLogService,
    OperationLogService,
    ExceptionLogService,
)


class LoginLogViewSet(ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)
    service = LoginLogService
    queryset = LoginLogService.all()
    serializer_class = LoginLogOutputSerializer


class OperationLogViewSet(ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)
    service = OperationLogService
    queryset = OperationLogService.all()
    serializer_class = OperationLogOutputSerializer


class ExceptionLogViewSet(ReadOnlyModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)
    service = ExceptionLogService
    queryset = ExceptionLogService.all()
    serializer_class = ExceptionLogOutputSerializer
