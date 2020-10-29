from apps.stores.models import StoreBook, Store, StoreBookSubscription
import factory

from tests.books.factories import BookFactory
from tests.users.factories import UserFactory


class StoreFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "store_name{0}".format(n))
    bio = factory.Sequence(lambda n: "store_bio{0}".format(n))
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Store


class StoreBookFactory(factory.DjangoModelFactory):
    store = factory.SubFactory(StoreFactory)
    book = factory.SubFactory(BookFactory)
    borrowed_by = None

    class Meta:
        model = StoreBook


class StoreBookSubscriptionFactory(factory.DjangoModelFactory):
    store_book = factory.SubFactory(StoreBookFactory)
    subscriber = factory.SubFactory(UserFactory)

    class Meta:
        model = StoreBookSubscription
