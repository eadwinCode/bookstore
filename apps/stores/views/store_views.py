from django.db import transaction
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.stores.mixins import StoreViewMixin
from apps.stores.serializers import StoreSerializer
__all__ = ('CreateStoreView', 'RetrieveStoreView', 'UpdateStoreView', 'DeleteStoreView', 'ListStoresView')


class CreateStoreView(StoreViewMixin, CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RetrieveStoreView(StoreViewMixin, RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreSerializer


class UpdateStoreView(StoreViewMixin, UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreSerializer


class DeleteStoreView(StoreViewMixin, DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreSerializer


class ListStoresView(StoreViewMixin, ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreSerializer
