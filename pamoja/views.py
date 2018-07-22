from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import (
    PostForm,
    GroupInfoForm
)

from .utils import get_groups_context, response_with_x_frames

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
    if not request.user.is_anonymous:
        context['user_groups'] = Group.objects.filter(admin=request.user)

    else:
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

            response = HttpResponseRedirect('/anonymous_post_success')
            return response_with_x_frames(response)

    context['post_form'] = post_form
    response = render(request, 'anonymous_post.html', context)
    return response_with_x_frames(response)

def all_posts(request, group_id):

    posts = Post.objects.filter(group_id=group_id)

    response = render(request, 'posts.html', {'posts': posts})
    return response_with_x_frames(response)

def anonymous_post_success(request):
    response = render(request, 'anonymous_post_success.html', {})
    return response_with_x_frames(response)


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

            response = HttpResponseRedirect('/activity_score/' + str(group_info.id))
            return response_with_x_frames(response)

    context['group_info_form'] = group_info_form

    response = render(request, 'get_group_info.html', context)
    return response_with_x_frames(response)


def activity_score(request, group_info_id):
    context = dict()

    group_info, _ = GroupInfo.objects.get_or_create(pk=group_info_id)
    context['activity_score'] = group_info.activity_score

    response = render(request, 'activity_score.html', context)
    return response_with_x_frames(response)


def dashboard(request, group_id):

    current_group = Group.objects.get(id=group_id)
    context = get_groups_context(current_group)
    context['current_group'] = current_group

    response = render(request, 'dashboard.html', context)
    return response_with_x_frames(response)


@csrf_exempt
def delete_post(request):

    if request.method == "POST":
        post_id = request.POST['post_id']

        try:
            current_post = Post.objects.get(id=post_id)

        except:
            return HttpResponse("not-exist")

        else:
            current_post.delete()
            return HttpResponse('deleted')

    return HttpResponse('error')





