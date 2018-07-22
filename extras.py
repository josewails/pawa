import os
import random
import django
from faker import Faker
import requests
from YamJam import yamjam

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawa.settings.production')
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

    data = {
        'get_started': {
            'payload': 'get_started'
        },
        'whitelisted_domains': [
            'https://acquiro.serveo.net',
            'https://pamojaness.herokuapp.com',
            'https://m.me'
        ]
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

def add_test_user():



    access_token = 'EAADYF2DPXZAgBAPbIzv9kvs0Ut2SIqvs63BC3Ft13mZAow6msbCDuXPgNUSKck2cPZCFrHUzRqiRilZA8EzH8dZAqVHIS1' \
                   'p0LngMYJZBtOdFqiifXZBQqc3KkjPpBRnmC9J0PCZBCHuLGRIxZCBJpXsCdC1NuVd9yNm6XhlPqXAcfGO3JlIEKvPNlNrMS' \
                   'UW8eed1urQBcwwurugZDZD'


    facebook_graph_url = 'https://graph.facebook.com?access_token=' + access_token

    data = {
        'name': "pawa",
        'password': 'pawaness'
    }

    re=requests.post(
        url=facebook_graph_url,
        json=data
    )

    print(re)

add_survey_questions()

