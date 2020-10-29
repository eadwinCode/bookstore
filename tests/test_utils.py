from django.contrib.auth import get_user_model
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer
)
from rest_framework.test import APIClient

User = get_user_model()


def authenticate_user(client, user, admin_user=False):
    if admin_user:
        user.is_superuser = True
        user.save()

    serializer = JSONWebTokenSerializer()

    attrs = {
        user.USERNAME_FIELD: user.get_username(),
        "password": "password",
    }
    user_credential = serializer.validate(attrs)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + user_credential.get("token"))
    return client
