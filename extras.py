import os
import random
import django
from faker import Faker
import requests
from YamJam import yamjam

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawa.settings.dev')
django.setup()

import random

from pamoja.models import (
    Survey,
    SurveyQuestion,
    Group
)


def messenger_setup():
    page_access_token = yamjam()['pamojaness']['page_access_token']

    url = 'https://graph.facebook.com/v2.6/me/messenger_profile?' \
          'access_token=' + page_access_token

    persistent_menu = [
        {
            "locale": "default",
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": '☱ Menu',
                    "payload": "main_menu"
                }
            ]
        }
    ]

    data = {
        'get_started': {
            'payload': 'get_started'
        },
        'whitelisted_domains': [
            'https://acquiro.serveo.net',
            'https://pamojaness.herokuapp.com',
            'https://m.me',
            'https://tinyurl.com'
        ],
        'persistent_menu': persistent_menu
    }

    response = requests.post(url, json=data)
    print(response.json())


def add_survey_questions():
    fake = Faker()

    groups = Group.objects.all()
    group_one = groups[0]
    group_two = groups[1]

    for survey in Survey.objects.all():
        survey.delete()

    survey_one, _ = Survey.objects.get_or_create(
        group=group_one,
        message=fake.sentence()
    )

    survey_two, _ = Survey.objects.get_or_create(
        group=group_two,
        message=fake.sentence()
    )

    for i in range(16):
        SurveyQuestion.objects.get_or_create(
            category=random.choice([1, 2, 3, 4]),
            survey=survey_one,
            question=fake.sentence()
        )
        SurveyQuestion.objects.get_or_create(
            category = random.choice([1, 2, 3, 4]),
            survey=survey_two,
            question=fake.sentence()
        )


messenger_setup()


