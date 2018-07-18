from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import exceptions

from .forms import (
    PostForm,
    GroupInfoForm
)

from .utils import get_groups_context

from .models import (
    Group,
    GroupInfo,
    Post
)


facebook_graph_url = 'https://graph.facebook.com'


def home(request):
    context = {}

    return render(request, 'home.html',context)


def main(request):
    context = {}
    try:
        context['user_groups'] = Group.objects.filter(admin=request.user)

    except exceptions.ObjectDoesNotExist:
        context['user_groups'] = []

    return render(request, 'main.html', context)


def anonymous_post(request, group_id):
    context = dict()

    post_form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            message = post_form.cleaned_data['message']
            post = Post(message=message, group_id=group_id)
            post.save()

            return HttpResponseRedirect('/anonymous_post_success')

    context['post_form'] = post_form
    return render(request, 'anonymous_post.html', context)


def all_posts(request, group_id):

    posts = Post.objects.filter(group_id=group_id)

    return render(request, 'posts.html', {'posts': posts})


def anonymous_post_success(request):
    return render(request, 'anonymous_post_success.html', {})


def get_group_info(request, group_id):

    context = dict()
    group_info_form = GroupInfoForm()
    current_group = Group.objects.get(id=group_id)

    if request.method == "POST":
        group_info_form = GroupInfoForm(request.POST)

        if group_info_form.is_valid():
            group_info = group_info_form.save()
            group_info.group = current_group
            group_info.save()

            return HttpResponseRedirect('/activity_score/' + str(group_info.id))

    context['group_info_form'] = group_info_form

    return render(request, 'get_group_info.html', context)


def activity_score(request, group_info_id):
    context = dict()

    group_info, _ = GroupInfo.objects.get_or_create(pk=group_info_id)
    context['activity_score'] = group_info.activity_score

    return render(request, 'activity_score.html', context)


def dashboard(request, group_id):

    current_group = Group.objects.get(id=group_id)
    context = get_groups_context(current_group)
    context['current_group'] = current_group

    return render(request, 'dashboard.html', context)



