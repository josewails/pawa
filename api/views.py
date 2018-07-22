import json
import urllib.parse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import exceptions
from accounts.models import FacebookUser
from pamoja.models import (
    Group
)

class create_facebook_user(APIView):
    """

    API view to create a new facebook user.

    """

    def post(self, request):

        data = request.data

        if 'email' in data:
            email = data['email']
        else:
            email  = None

        try:
            facebook_user = FacebookUser.objects.get(facebook_id=data['id'])

        except exceptions.ObjectDoesNotExist:



            facebook_user = FacebookUser.objects.create(
                facebook_id=data['id'],
                name=data['name'],
                access_token=data['accessToken'],
                email=email,
                picture_data=json.dumps(data['picture']['data'])
            )
            self.add_groups(groups=data['groups']['data'], facebook_user=facebook_user)

            data = {
                'success': 'user added successfully'
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            facebook_user.name = data['name'],
            facebook_user.picture_data = data['picture']['data']
            facebook_user.email = email
            facebook_user.save()
            self.add_groups(groups=data['groups']['data'], facebook_user=facebook_user)

            data = {
                'success': 'user updated successfully'
            }

            return Response(data, status=status.HTTP_200_OK)

    def add_groups(self, groups, facebook_user):

        user_groups = [group for group in groups if group['administrator']]

        for user_group in user_groups:
            group, _ = Group.objects.get_or_create(group_id=user_group['id'])
            group.admin = facebook_user
            group.name = user_group['name']
            group.save()


class get_groups_data(APIView):

    def post(self, request):

        try:
            facebook_user = FacebookUser.objects.get(facebook_id=request.data['facebook_id'])

        except exceptions.ObjectDoesNotExist:

            data ={
                'error': 'User not found'
            }

            return Response(data, status=status.HTTP_404_NOT_FOUND)

        else:

            data = {
                "bot": True,
                "type": "option",
                "data": "Here are your groups.",
                "title": "Choose an Option",
                "showOptions": True,
                "options": [

                ]
            }


            groups = facebook_user.group_set.all()

            for group in groups:
                data['options'].append(
                    {
                        "type": "link",
                        "data": group.group_messenger_url(),
                        "text": group.name
                    }
                )

            return Response(data, status=status.HTTP_200_OK)
