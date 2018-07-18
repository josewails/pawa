from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    facebook_id = models.CharField(max_length=50, null=True)
    messenger_authenticated = models.BooleanField(default=False)

