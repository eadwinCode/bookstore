import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from tests.test_utils import authenticate_user


class TestUserView:
    @pytest.mark.django_db
    def test_create_new_user_should_pass(self, random_email, random_username, api_client):
        url = reverse("create")
        payload = {
            'username': random_username,
            "email": random_email,
            "password": "password",
            "first_name": "test",
            "last_name": "test"
        }
        response = api_client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['token']

    @pytest.mark.django_db
    def test_create_new_user_with_existing_email_should_fail(self, random_email, random_username, api_client):
        url = reverse("create")
        payload = {
            'username': random_username,
            "email": random_email,
            "password": "password",
            "first_name": "test",
            "last_name": "test"
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_enable_or_disable_user_success(self, app_admin, user, api_client):
        client = authenticate_user(api_client, app_admin)

        url = reverse("enable-disable", kwargs={"pk": str(user.pk)})
        response = client.put(url, format="json")
        assert response.status_code == status.HTTP_200_OK

        user = User.objects.get(pk=user.pk)
        assert user.is_active is False

        with pytest.raises(Exception) as exception_info:
            authenticate_user(api_client, user)

    @pytest.mark.django_db
    def test_delete_user_success(self, app_admin, user, api_client):
        client = authenticate_user(api_client, app_admin)

        url = reverse("delete", kwargs={"pk": user.id})
        response = client.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        user = User.objects.filter(pk=user.pk).first()
        assert user is None
