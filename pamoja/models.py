import json
import urllib.parse
from django.db import models
from accounts.models import User
from django.db.models.signals import post_save


class Group(models.Model):
    admin = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    group_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    def group_messenger_url(self):
        data = {
            'selected_group_id': self.id
        }

        return 'https://m.me/452174761913102?ref=' + urllib.parse.quote(json.dumps(data))

    class Meta:
        unique_together = ('admin', 'group_id')


class GroupInfo(models.Model):

    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    total_posts = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_reactions = models.IntegerField(default=0)
    active_members = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    activity_score = models.FloatField(null=True)

    def group_name(self):
        if self.group:
            return self.group.name + ' - Group Info'

    def __str__(self):
        return self.created_on.strftime("%Y-%m-%d %H:%M:%S")


class Post(models.Model):
    """

    Model for an anonymous post

    """

    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    message = models.TextField()

    def __str__(self):
        return 'Post ' +  str(self.id)


class Survey(models.Model):
    """

    Model for a group survey

    """

    group = models.OneToOneField(Group, null=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return 'Survey - ' + str(self.id)


class SurveyQuestion(models.Model):

    """

    Model for a survey question.

    """

    category_choices = (
        (1, 'Reinforcement of needs'),
        (2, 'Memebership'),
        (3, 'Influence'),
        (4, 'Shared Emotional Connection')
    )

    category = models.IntegerField(choices=category_choices)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=1000)

    def __str__(self):
        return self.question


class SurveyResult(models.Model):
    """

    Model for Survey Result

    """

    default_result = [[] * 4] * 4

    created_on = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='results')
    result = models.CharField(max_length=1000, default=json.dumps(default_result))

    def __str__(self):
        return 'Survey-' + str(self.id) + "(" + self.created_on.strftime("%Y-%m-%d %H:%M:%S") + ")"


def add_activity_score(sender, instance, **kwargs):

    post_save.disconnect(add_activity_score, sender=sender)

    activity_score = (instance.total_posts + instance.total_comments * 2 + instance.total_reactions) / \
                     instance.active_members

    instance.activity_score = activity_score
    instance.save()

    post_save.connect(add_activity_score, sender=sender)


post_save.connect(add_activity_score, sender=GroupInfo)