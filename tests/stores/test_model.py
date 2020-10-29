import pytest

from apps.stores.models import Store, StoreBook, StoreBookSubscription

py_test_mark = pytest.mark.django_db


class TestStoreModel:
    @py_test_mark
    def test_create_model(self, user):
        store = Store.objects.create(name="New Store", owner=user)
        assert store.name == 'New Store'
        assert store.owner == user


class TestStoreBookModel:
    @py_test_mark
    def test_create_model(self, book, store):
        store = StoreBook.objects.create(store=store, book=book)
        assert store.is_available
        assert store.borrowed_by is None

    @py_test_mark
    def test_store_book_not_available_on_borrowed(self, book, store, user):
        store = StoreBook.objects.create(store=store, book=book, borrowed_by=user)
        assert store.is_available is False
        assert store.borrowed_by == user

    @py_test_mark
    def test_model_unique_constraint_works(self, book, store):
        StoreBook.objects.create(store=store, book=book)
        with pytest.raises(Exception) as ex:
            StoreBook.objects.create(store=store, book=book)
        assert 'UNIQUE constraint failed' in str(ex)


class TestStoreBookSubscriptionModel:
    @py_test_mark
    def test_create_model(self, store_book, user):
        store = StoreBookSubscription.objects.create(store_book=store_book, subscriber=user)
        assert store.store_book == store_book
        assert store.subscriber == user

    @py_test_mark
    def test_model_unique_constraint_works(self,store_book, user):
        StoreBookSubscription.objects.create(store_book=store_book, subscriber=user)
        with pytest.raises(Exception) as ex:
            StoreBookSubscription.objects.create(store_book=store_book, subscriber=user)
        assert 'UNIQUE constraint failed' in str(ex)
