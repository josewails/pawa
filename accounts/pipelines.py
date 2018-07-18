import requests
import urllib.parse
import json
from pamoja.models import (
    Group
)

facebook_graph_url = 'https://graph.facebook.com'


def save_group(backend, user, response, *args, **kwargs):

    social_user = kwargs['social']
    user_data = social_user.extra_data
    facebook_id = user_data['id']
    url = facebook_graph_url + '/' + str(facebook_id)
    user_access_token = user_data['access_token']
    params = {
        'access_token': user_access_token,
        'fields': 'groups{administrator,name}'
    }

    user.messenger_authenticated = True
    user.facebook_id = facebook_id
    user.save()

    res = requests.get(url, params=params).json()

    # Extract groups, first_name and last_name from data

    try:
        groups = res['groups']['data']

    except KeyError:
        groups = []

    user_groups = [group for group in groups if group['administrator']]

    for user_group in user_groups:
        data = {
            'selected_group_id': user_group['id']
        }
        url = 'https://m.me/452174761913102?ref=' + urllib.parse.quote(json.dumps(data))
        group, _ = Group.objects.get_or_create(group_id=user_group['id'])
        group.admin = user
        group.group_bot_url = url
        group.name = user_group['name']
        group.save()
