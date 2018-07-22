from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('main', views.main, name='main'),
    path('posts/<group_id>', views.all_posts, name="posts"),
    path('anonymous_post/<group_id>', views.anonymous_post, name='anonymous-post'),
    path('anonymous_post_success', views.anonymous_post_success, name='anonymous-post-success'),
    path('get_group_info/<group_id>', views.get_group_info, name='get-group-info'),
    path('activity_score/<group_info_id>', views.activity_score, name='activity-score'),
    path('dashboard/<group_id>', views.dashboard, name='dashboard'),
    path('delete_post', views.delete_post, name='delete-post')
]
