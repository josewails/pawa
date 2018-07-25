import urllib.parse

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings

from .forms import (
    PostForm,
    GroupInfoForm
)

from .utils import get_groups_context, response_with_x_frames
from messenger.utils.general_utils import handle_get_started

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

@xframe_options_exempt
def anonymous_post(request, group_id):
    context = dict()

    fb_origin = request.GET.get('fb_iframe_origin')

    post_form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            message = post_form.cleaned_data['message']
            post = Post(message=message, group_id=group_id)
            post.save()

            response = HttpResponseRedirect('/anonymous_post_success/' + str(group_id))
            return response_with_x_frames(response, fb_origin)

    context['post_form'] = post_form
    response = render(request, 'anonymous_post.html', context)
    return response_with_x_frames(response, fb_origin)


def all_posts(request, group_id):

    fb_origin = request.GET.get('fb_iframe_origin')

    posts = Post.objects.filter(group_id=group_id)

    response = render(request, 'posts.html', {'posts': posts})
    return response_with_x_frames(response, fb_origin)


@xframe_options_exempt
def anonymous_post_success(request, group_id):

    fb_origin = request.GET.get('fb_iframe_origin')

    context = dict()
    context['pawa_url'] = 'https://m.me/452174761913102?ref=' + urllib.parse.quote('send_menu')
    context['anonymous_post_url'] = settings.SITE_URL + '/anonymous_post/' + str(group_id)
    response = render(request, 'anonymous_post_success.html', context)
    return response_with_x_frames(response, fb_origin)


def get_group_info(request, group_id):

    fb_origin = request.GET.get('fb_iframe_origin')

    context = dict()
    group_info_form = GroupInfoForm()
    current_group = Group.objects.get(id=group_id)

    if request.method == "POST":
        group_info_form = GroupInfoForm(request.POST)

        if group_info_form.is_valid():
            group_info = group_info_form.save()
            group_info.group = current_group
            group_info.save()

            response = HttpResponseRedirect(settings.SITE_URL + '/activity_score/' + str(group_info.id))
            return response_with_x_frames(response, fb_origin)

    context['group_info_form'] = group_info_form

    response = render(request, 'get_group_info.html', context)
    return response_with_x_frames(response, fb_origin)


@xframe_options_exempt
def activity_score(request, group_info_id):
    context = dict()

    fb_origin = request.GET.get('fb_iframe_origin')

    group_info, _ = GroupInfo.objects.get_or_create(pk=group_info_id)
    current_group_id = group_info.group.id
    context['dashboard_url'] = settings.SITE_URL + '/dashboard/' + str(current_group_id)
    context['pawa_url'] = 'https://m.me/452174761913102?ref=' + urllib.parse.quote('send_menu')
    context['activity_score'] = group_info.activity_score

    response = render(request, 'activity_score.html', context)
    return response_with_x_frames(response, fb_origin)

@xframe_options_exempt
def dashboard(request, group_id):

    fb_origin = request.GET.get('fb_iframe_origin')

    current_group = Group.objects.get(id=group_id)
    context = get_groups_context(current_group)
    context['current_group'] = current_group

    response = render(request, 'dashboard.html', context)
    return response_with_x_frames(response, fb_origin)


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


@csrf_exempt
def web_view_close(request):

    if request.method == 'POST':
        psid = request.POST['psid']
        type = request.POST['type']

        if psid:

            if type == 'activity_score':

                handle_get_started(recipient_id=psid, message="Thanks for measuring activity score, "
                                                              "You can try something else here")

                return HttpResponse('success')

            else:

                handle_get_started(recipient_id=psid, message="Thanks for posting, You can try something else here")

                return HttpResponse('success')

        else:
            return HttpResponse('error')

    return HttpResponse('error')
