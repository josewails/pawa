import json

from pymessenger.bot import Bot
from django.conf import settings

from messenger.models import (
    BotUser
)

from pamoja.models import (
    Group
)

from .general_utils import (
    handle_get_started
)

from .message_utils import (
    web_button
)

from .general_utils import (
    send_survey
)

messenger_bot = Bot(access_token=settings.PAGE_ACCESS_TOKEN)


def handle_referral(recipient_id, referral, ref_type):

    if ref_type == 'optin':
        if referral == 'pamojaness_messenger':
            handle_pamojaness_messenger(recipient_id)

    elif ref_type == 'normal':
        if 'honesty_box_ref' in referral:
            group_id = json.loads(referral)['honesty_box_ref']['data']['group_id']
            handle_honesty_box_ref(recipient_id, group_id)

        elif 'survey_ref' in referral:
            group_id = json.loads(referral)['survey_ref']['data']['group_id']
            handle_survey_ref(recipient_id, group_id)

        elif 'selected_group_id' in referral:
            group_id = json.loads(referral)['selected_group_id']
            handle_selected_group_ref(recipient_id, group_id)

        elif referral == 'send_menu':
            handle_get_started(recipient_id=recipient_id, message='Back to Pawa, you can try some of these other tools :)')

    elif ref_type == 'get_started':
        if 'honesty_box_ref' in referral:
            group_id = json.loads(referral)['honesty_box_ref']['data']['group_id']
            handle_honesty_box_ref(recipient_id, group_id)

        elif 'survey_ref' in referral:
            group_id = json.loads(referral)['survey_ref']['data']['group_id']
            handle_survey_ref(recipient_id, group_id)

        elif 'selected_group_id' in referral:
            group_id = json.loads(referral)['selected_group_id']
            handle_selected_group_ref(recipient_id, group_id)


def handle_pamojaness_messenger(recipient_id):

    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    name = current_bot_user.get_name()
    message = 'Hi  %s!👋Welcome to Pawa on Messenger ❤️' % name

    messenger_bot.send_text_message(recipient_id=recipient_id, message=message)


def handle_honesty_box_ref(recipient_id, group_id):
    message = 'By posting anonymously you can safely get help! ⚠️Dont share personal identifiable details like name, place of work, address etc'

    buttons = [
        web_button(
            title='Post now 📤',
            url=settings.SITE_URL + '/anonymous_post/' + str(group_id),
            messenger_extensions = True,
            height='full'
        )
    ]

    messenger_bot.send_button_message(recipient_id=recipient_id, text=message, buttons=buttons)


def handle_survey_ref(recipient_id, group_id):
    send_survey(recipient_id=recipient_id, group_id=group_id)


def handle_selected_group_ref(recipient_id, group_id):
    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    current_bot_user.current_group_id = group_id
    current_bot_user.save()

    name = current_bot_user.get_name()

    message = '❤️'
    messenger_bot.send_text_message(recipient_id=recipient_id, message=message)
    
    message = 'Hi %s!👋 welcome to Pawa on Messenger' % name
    messenger_bot.send_text_message(recipient_id=recipient_id, message=message)

    current_group = Group.objects.get(id=group_id)
    message = "Happy to help you with tools to drive engagement in %s . Just tap a button on the MENU below 👇" % current_group.name

    handle_get_started(recipient_id=recipient_id, message=message)

