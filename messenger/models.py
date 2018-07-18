import requests
import json

from django.db import models
from django.conf import settings
from accounts.models import User

page_access_token = settings.PAGE_ACCESS_TOKEN

class BotUser(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    messenger_id = models.CharField(max_length=50)
    profile_data = models.CharField(
        max_length=100000,
        null=True
    )
    question_ids = models.CharField(max_length=10000, null=True)
    current_question_index = models.IntegerField(null=True)
    current_survey_result_id = models.IntegerField(null=True)
    current_group_id = models.IntegerField(null=True)

    def get_fb_data(self):

        url = 'https://graph.facebook.com/v2.6/' + self.messenger_id + '?fields=first_name,' \
              'last_name,profile_pic&access_token=' + page_access_token

        profile_data = requests.get(url).json()
        self.profile_data = json.dumps(profile_data)
        self.save()

    def get_name(self):
        try:
            name = json.loads(self.profile_data)['first_name']

        except KeyError:
            name = json.load(self.profile_data)['first_name']
        return name

    def __str__(self):
        return self.messenger_id