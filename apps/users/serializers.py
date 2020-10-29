from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'username', 'is_staff', 'is_superuser', 'password')
        read_only_fields = ('is_staff', 'is_superuser')

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            **validated_data
        )
        return user


class UserRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'username', 'id', 'groups', 'is_active')
        read_only_fields = ('groups',)


class EnableDisableUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = []

    def update(self, instance, validated_data, **kwargs):
        instance.is_active = not instance.is_active
        instance.save()
        return instance
