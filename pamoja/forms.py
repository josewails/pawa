from django import forms
from .models import (
    GroupInfo,
    Group,
    Post
)


class GroupInfoForm(forms.ModelForm):

    class Meta:
        model = GroupInfo
        exclude = ['activity_score', 'group', 'created_on']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['group']