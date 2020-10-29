from apps.stores.models import StoreBook, Store, StoreBookSubscription
from bookstore.utils.custom_exceptions import ModelNotFoundException


class StoreBookBorrowAndReturnViewMixins:
    def get_object(self):
        store_id, book_id = self.kwargs.get('store_id'), self.kwargs.get('book_id')
        store_book = StoreBook.objects.select_related('store', 'book').filter(
            store__id=store_id, book__id=book_id, store__owner=self.request.user).first()
        if not store_book:
            raise ModelNotFoundException('Model not found')
        self.check_object_permissions(self.request, store_book)
        return store_book


class StoreViewMixin:
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoryBookQuerySetMixin:
    def get_queryset(self):
        return StoreBookSubscription.objects.select_related('store_book', 'subscriber').filter(
            store_book__store__owner=self.request.user)
