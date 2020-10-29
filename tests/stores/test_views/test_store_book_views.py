import pytest
from django.core import mail
from django.urls import reverse
from rest_framework import status

from apps.stores.models import Store, StoreBook
from tests.stores.factories import StoreBookFactory
from tests.test_utils import authenticate_user
from tests.users.factories import UserFactory


class TestUserView:
    @pytest.mark.django_db
    def test_store_list_view_works(self, api_client, user, build_store_list):
        client = authenticate_user(api_client, user)
        build_store_list(owner=user, batch_count=4)

        url = reverse("store:list")
        response = client.get(url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    @pytest.mark.django_db
    def test_users_can_create_store(self, api_client, user):
        client = authenticate_user(api_client, user)
        url = reverse("store:create")
        payload = {
            'name': 'New BookStore',
            "bio": "Some description",
        }
        response = client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Store.objects.filter(name='New BookStore').first(), 'Store was not created'

    @pytest.mark.django_db
    def test_store_owners_can_view_store_details(self, api_client, store):
        client = authenticate_user(api_client, store.owner)
        url = reverse("store:detail", kwargs=dict(id=store.id))

        response = client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert store.name in response.data.values()

    @pytest.mark.django_db
    def test_store_owners_can_view_store_update_store_details(self, api_client, store):
        client = authenticate_user(api_client, store.owner)
        url = reverse("store:update", kwargs=dict(id=store.id))

        payload = {
            'name': 'New BookStore Updated',
            "bio": "Some description",
        }
        response = client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert 'New BookStore Updated' in response.data.values()

    @pytest.mark.django_db
    def test_can_add_book_to_store(self, api_client, store):
        client = authenticate_user(api_client, store.owner)
        url = reverse("store:book-create", kwargs=dict(store_id=store.id))
        payload = {
            'name': 'BookStore Startup lol',
            "description": "Some description",
            "author": "Eadwin"
        }
        response = client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_store_owner_can_see_books_in_store(self, api_client, build_store_book_list, store):
        build_store_book_list(store=store, batch_count=4)
        client = authenticate_user(api_client, store.owner)
        url = reverse("store:books", kwargs=dict(id=store.id))

        response = client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    @pytest.mark.django_db
    def test_users_can_borrow_book_from_store_owner(self, api_client, store_book, user):
        client = authenticate_user(api_client, store_book.store.owner)
        url = reverse("store:book-borrow", kwargs=dict(
            store_id=store_book.store.id, book_id=store_book.book.id, user_id=user.id))

        response = client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert StoreBook.objects.get(id=store_book.id).is_available is False

        response = client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_502_BAD_GATEWAY

    @pytest.mark.django_db
    def test_users_can_return_borrowed_book_from_store_owner(self, api_client, store, book, user):
        store_book = StoreBookFactory(store=store, book=book, borrowed_by=user)
        client = authenticate_user(api_client, store.owner)
        url = reverse("store:book-return", kwargs=dict(
            store_id=store.id, book_id=book.id))

        response = client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert StoreBook.objects.get(id=store_book.id).is_available
        response = client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_502_BAD_GATEWAY

    @pytest.mark.django_db
    def test_subscribed_users_on_a_book_store_gets_notified(self, api_client, store_book_subscription, user):
        store_book_subscription.store_book.borrowed_by = UserFactory()
        store_book_subscription.store_book.save()

        client = authenticate_user(api_client, store_book_subscription.store_book.store.owner)
        url = reverse("store:book-return", kwargs=dict(
            store_id=store_book_subscription.store_book.store.id,
            book_id=store_book_subscription.store_book.book.id))

        response = client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(mail.outbox) > 0
