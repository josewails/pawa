from django.urls import path

import api.views as api_views

urlpatterns = [
    path('create_facebook_user', api_views.create_facebook_user.as_view(), name='create-facebook-user'),
    path('get_groups_data', api_views.get_groups_data.as_view(), name='get-groups-data')
]