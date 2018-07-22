import factory
import random
from faker import Faker
from factory import fuzzy

from .models import (
    Survey, SurveyQuestion, Group,
)

from accounts.models import User

fake = Faker()

class GroupAdminFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    username = fake.name_male()
    password = fake.uuid4()


class GroupFactory(factory.DjangoModelFactory):

    class Meta:
        model = Group

    admin = factory.SubFactory(GroupAdminFactory)
    group_id = '655820674767116'
    name = fake.word()


class SurveyFactory(factory.DjangoModelFactory):

    class Meta:
        model = Survey

    group = factory.SubFactory(GroupFactory)
    message = fake.sentence()


class SurveyQuestionFactory(factory.DjangoModelFactory):

    class Meta:
        model = SurveyQuestion

    category = random.choice([1, 2, 3, 4])
    survey = factory.SubFactory(SurveyFactory)
    question = fake.sentence()


