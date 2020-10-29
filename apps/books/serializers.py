from rest_framework import serializers
from apps.books.models import Book
from apps.users.serializers import UserRetrieveSerializer


class BookSerializer(serializers.ModelSerializer):
    created_by = UserRetrieveSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
