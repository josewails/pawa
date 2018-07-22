from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    facebook_id = models.CharField(max_length=50, null=True)
    messenger_authenticated = models.BooleanField(default=False)


class FacebookUser(models.Model):
    facebook_id = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    picture_data = models.CharField(max_length=10000, null=True)

