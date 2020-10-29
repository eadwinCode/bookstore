from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.books.serializers import BookSerializer
from apps.stores.mixins import StoreBookBorrowAndReturnViewMixins
from apps.stores.models import StoreBook, Store
from apps.stores.serializers import StoreBookSerializer, BorrowOrReturnStoreBookSerializer
from apps.stores.tasks import process_subscription_notification
from bookstore.utils.model_utils import get_object_or_400

User = get_user_model()
__all__ = ('ListStoreBooksView', 'AddStoreBooksView', 'BorrowStoreBooksView', 'ReturnStoreBooksView')


class ListStoreBooksView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreBookSerializer

    def get_queryset(self):
        return StoreBook.objects.filter(store_id=self.kwargs.get('id'), store__owner=self.request.user)


class AddStoreBooksView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookSerializer
    queryset = StoreBook.objects.all()

    def post(self, request, *args, **kwargs):
        store_id = self.kwargs.get('store_id')
        store = get_object_or_400(
            Store, id=store_id, error_message='Store with id {} does not exist'.format(store_id)
        )
        self.check_object_permissions(self.request, store)
        self.kwargs.setdefault('store', store)
        return self.create(request, *args, **kwargs)

    @transaction.atomic
    def perform_create(self, serializer):
        book = serializer.save(created_by=self.request.user)
        self.queryset.create(book=book, store=self.kwargs.get('store'))


class BorrowStoreBooksView(StoreBookBorrowAndReturnViewMixins, GenericAPIView):
    """
    post user_id
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BorrowOrReturnStoreBookSerializer
    queryset = StoreBook.objects.all()

    def post(self, request, *args, **kwargs):
        store_book = self.get_object()
        user_id = self.kwargs.get('user_id')
        user = get_object_or_400(
            User, id=user_id, error_message='User with id {} does not exist'.format(user_id)
        )
        if store_book.borrowed_by:
            return Response(
                {'message': 'Borrowed book can not be reassigned. It must be returned'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        store_book.borrowed_by = user
        store_book.save()
        read_serializer = BorrowOrReturnStoreBookSerializer(store_book, context=self.get_serializer_context())
        return Response(read_serializer.data, status=status.HTTP_200_OK)


class ReturnStoreBooksView(StoreBookBorrowAndReturnViewMixins, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BorrowOrReturnStoreBookSerializer
    queryset = StoreBook.objects.all()

    def post(self, request, *args, **kwargs):
        store_book = self.get_object()
        if store_book.borrowed_by:
            store_book.borrowed_by = None
            store_book.save()
            process_subscription_notification(store_book_id=store_book.id)
            read_serializer = BorrowOrReturnStoreBookSerializer(store_book, context=self.get_serializer_context())
            return Response(read_serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'message': 'It is already returned'},
            status=status.HTTP_502_BAD_GATEWAY
        )
