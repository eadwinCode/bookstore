from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler

from apps.users.serializers import UserSerializer, EnableDisableUserSerializer

User = get_user_model()


class UserCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.create(serializer.data)
        read_serializer = UserSerializer(new_user)
        payload = jwt_payload_handler(new_user)
        response = {
            'token': jwt_encode_handler(payload)
        }
        response.update(read_serializer.data)
        return Response(response, status=status.HTTP_201_CREATED)


class EnableOrDisableUserView(UpdateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = EnableDisableUserSerializer


class DeleteUserView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = EnableDisableUserSerializer
