from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.stores.mixins import StoryBookQuerySetMixin
from apps.stores.models import StoreBook
from apps.stores.serializers import StoreBookSubscriptionSerializer
from bookstore.utils.model_utils import get_object_or_400
__all__ = ('StoryBookSubscribeView', 'StoryBookUnSubscribeView', 'StoryBookSubscribersListView')
User = get_user_model()


class StoryBookSubscribeView(StoryBookQuerySetMixin, CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreBookSubscriptionSerializer

    def post(self, request, *args, **kwargs):
        store_book_id = self.kwargs.get('store_book_id')
        user_id = self.kwargs.get('user_id')
        user = get_object_or_400(
            User, id=user_id, error_message='User with id {} does not exist'.format(user_id)
        )
        store_book = get_object_or_400(
            StoreBook, id=store_book_id, store__owner=self.request.user,
            error_message='StoreBook with id {} does not exist'.format(user_id)
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        not_saved = self.perform_create(serializer, store_book, user)
        headers = self.get_success_headers(serializer.data)
        if not not_saved:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(dict(message=not_saved), status=status.HTTP_502_BAD_GATEWAY, headers=headers)

    @transaction.atomic
    def perform_create(self, serializer, store_book, user):
        try:
            serializer.save(store_book=store_book, subscriber=user)
        except Exception as ex:
            return str(ex)


class StoryBookUnSubscribeView(StoryBookQuerySetMixin, DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreBookSubscriptionSerializer
    lookup_url_kwarg = 'store_book_subscription_id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StoryBookSubscribersListView(StoryBookQuerySetMixin, ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreBookSubscriptionSerializer

    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        query_set = super().get_queryset()
        return query_set.filter(store_book__store_id=store_id)
