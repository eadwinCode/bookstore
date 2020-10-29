import factory
from django.contrib.auth import get_user_model
from factory import post_generation


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda n: "person{0}@example.com".format(n))
    username = factory.Sequence(lambda n: "person_username{0}".format(n))

    @post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password("password")

    class Meta:
        model = get_user_model()
