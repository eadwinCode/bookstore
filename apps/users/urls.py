from django.urls import path
from rest_framework_jwt.views import RefreshJSONWebToken, ObtainJSONWebToken

from apps.users.auth import JWTSerializer, JWTRefreshTokenSerializer
from apps.users.views import UserCreateView, DeleteUserView, EnableOrDisableUserView

urlpatterns = [
    path('create', UserCreateView.as_view(), name='create'),
    path('<int:pk>/delete', DeleteUserView.as_view(), name='delete'),
    path('<int:pk>/enable-disable', EnableOrDisableUserView.as_view(), name='enable-disable'),
    path('login', ObtainJSONWebToken.as_view(serializer_class=JWTSerializer), name='login'),
    path('api-token-refresh', RefreshJSONWebToken.as_view(serializer_class=JWTRefreshTokenSerializer), name='refresh')
]
