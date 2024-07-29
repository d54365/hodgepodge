from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.auth.authentication import JWTAuthentication
from .serializers import (
    UserInfoOutputSerializer,
)


class UserInfoViewSet(viewsets.ViewSet):
    authentication_classes = (JWTAuthentication,)

    @action(methods=["GET"], detail=False, url_path="info")
    def info(self, request):
        return Response(UserInfoOutputSerializer(request.user).data)
