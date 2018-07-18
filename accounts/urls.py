from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import (
    pamoja_logout,
    login
)

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', pamoja_logout, name='logout'),
    path('oauth/', include('social_django.urls', namespace='social'))
]