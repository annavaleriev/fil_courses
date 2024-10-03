import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from factory.fuzzy import FuzzyText, FuzzyDecimal

from materials.models import Course, Lesson
from users.models import MODER_GROUP_NAME

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.LazyAttribute(
        lambda n: "{}.{}@example.com".format(n.first_name, n.last_name).lower()
    )
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User


class AdminUserFactory(UserFactory):
    is_superuser = True


class ModerGroupFactory(factory.django.DjangoModelFactory):
    name = MODER_GROUP_NAME

    class Meta:
        model = Group


class CourseFactory(factory.django.DjangoModelFactory):
    title = FuzzyText()
    price = FuzzyDecimal(low=10.00, high=100.00)

    class Meta:
        model = Course


class LessonFactory(factory.django.DjangoModelFactory):
    title = FuzzyText()
    course = factory.SubFactory(CourseFactory)
    video = factory.Sequence(lambda n: "https://www.youtube.com/?watch%04d" % n)

    class Meta:
        model = Lesson
