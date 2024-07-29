from rest_framework.mixins import DestroyModelMixin as DestroyModelMixin_
from rest_framework.viewsets import (
    ModelViewSet as ModelViewSet_,
    ReadOnlyModelViewSet as ReadOnlyModelViewSet_,
)

from .generics import GenericAPIView
from .pagination import PageNumberPagination


class DestroyModelMixin(DestroyModelMixin_):
    def perform_destroy(self, instance):
        self.service.delete(instance, self.request.user)  # noqa


class ModelViewSet(ModelViewSet_, GenericAPIView, DestroyModelMixin):
    pagination_class = PageNumberPagination


class ReadOnlyModelViewSet(ReadOnlyModelViewSet_, GenericAPIView):
    pagination_class = PageNumberPagination
