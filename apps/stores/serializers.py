from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.books.serializers import BookSerializer
from apps.stores.models import Store, StoreBook, StoreBookSubscription
from apps.users.serializers import UserRetrieveSerializer


class StoreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=Store.objects.all())], required=True)
    owner = UserRetrieveSerializer(read_only=True)

    class Meta:
        model = Store
        fields = ['name', 'bio', 'owner', 'id']


class StoreBookSerializer(serializers.ModelSerializer):
    borrowed_by = UserRetrieveSerializer(read_only=True)
    store = serializers.HyperlinkedRelatedField(view_name='store:detail', lookup_url_kwarg='id', read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = StoreBook
        fields = '__all__'


class BorrowOrReturnStoreBookSerializer(serializers.ModelSerializer):
    borrowed_by = UserRetrieveSerializer(read_only=True)
    store = serializers.HyperlinkedRelatedField(view_name='store:detail', lookup_url_kwarg='id', read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = StoreBook
        fields = ['borrowed_by', 'store', 'book']


class StoreBookSubscriptionSerializer(serializers.ModelSerializer):
    store_book = StoreBookSerializer(read_only=True)
    subscriber = UserRetrieveSerializer(read_only=True)

    class Meta:
        model = StoreBookSubscription
        fields = ['store_book', 'subscriber', 'id']
