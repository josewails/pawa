import factory
from faker import Faker
import json

from .models import BotUser

fake = Faker()

class BotUserFactory(factory.DjangoModelFactory):

    class Meta:
        model = BotUser

    messenger_id = fake.sha1(raw_output=False)
    profile_data = json.dumps(
        {
            'first_name': fake.word(),
            'last_name': fake.word()
        }
    )
    question_ids = json.dumps([1,2,3,4,5,6])
    current_question_index = 1


