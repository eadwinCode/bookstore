from apps.books.models import Book
import factory

from tests.users.factories import UserFactory


class BookFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "book_name{0}".format(n))
    author = factory.Sequence(lambda n: "book_author{0}".format(n))
    description = factory.Sequence(lambda n: "book_description{0}".format(n))
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Book
