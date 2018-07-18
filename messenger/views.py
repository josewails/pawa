import json

from django.core import exceptions
from django.http import HttpResponse
from django.views.decorators.csrf import  csrf_exempt

from .utils.referral_utils import handle_referral
from .utils.post_back_utils import handle_post_back
from .utils.text_message_utils import handle_text_message
from .utils.quick_reply_utils import handle_quick_reply

from .models import BotUser

@csrf_exempt
def webhook(request):

    """

    :param request:

        * The request method will always be sent by facebook messenger to our webhook whenever a new user interacts
         with the bot

        * Depending on the request data, a different kind of message will be sent back to the user

    :return:
      It returns a Http Response(Somehow irrelevant but it prevents django from throwing exceptions)
    """

    if request.method == 'GET':

        if 'hub.mode' in request.GET and 'hub.verify_token' in request.GET:
            if request.GET['hub.mode'] == 'subscribe' and request.GET['hub.verify_token'] == 'pamojaness_way':
                return HttpResponse(request.GET['hub.challenge'])
            else:
                return HttpResponse("Wrong verification code")
        else:
            return HttpResponse("Bi :p")


    elif request.method == 'POST':


        request_data = json.loads(request.body.decode('utf-8'))

        print(request_data)

        recipient_id = request_data['entry'][0]['messaging'][0]['sender']['id']

        # The following block of try-except blocks just checks for what type of message we are receiving

        try:
            BotUser.objects.get(messenger_id=recipient_id)
        except exceptions.ObjectDoesNotExist:
            bot_user = BotUser.objects.create(messenger_id=recipient_id)
            bot_user.get_fb_data()

        try:
            postback = request_data['entry'][0]['messaging'][0]['postback']
        except KeyError:
            postback = None

        try:
            quick_reply_message = request_data['entry'][0]['messaging'][0]['message']['quick_reply']
        except KeyError:
            quick_reply_message = None

        try:
            text_message = request_data['entry'][0]['messaging'][0]['message']['text']
        except KeyError:
            text_message = None

        try:
            referral = request_data['entry'][0]['messaging'][0]['referral']['ref']
        except KeyError:
            referral = None

        try:
            optin_referral = request_data['entry'][0]['messaging'][0]['optin']['ref']

        except KeyError:
            optin_referral = None

        try:
            get_started_referral = request_data['entry'][0]['messaging'][0]['postback']['referral']['ref']
        except KeyError:
            get_started_referral = None

        if text_message and not quick_reply_message:
            handle_text_message(recipient_id, text_message=text_message)

        elif quick_reply_message:
            handle_quick_reply(recipient_id, quick_reply_message)

        elif postback and not get_started_referral:
            handle_post_back(recipient_id=recipient_id, payload=postback['payload'])

        elif optin_referral:
            handle_referral(recipient_id, optin_referral, ref_type='optin')

        elif get_started_referral:
            handle_referral(recipient_id, get_started_referral, ref_type='get_started')

        elif referral:
            handle_referral(recipient_id, referral,ref_type='normal')

        return HttpResponse('')


    