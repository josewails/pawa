from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

def login(request):
    context = {}
    return render(request, 'registration/login.html', context)

def pamoja_logout(request):
    logout(request)
    return HttpResponseRedirect('/')