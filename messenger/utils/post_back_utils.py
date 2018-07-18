from django.conf import settings
from pymessenger.bot import Bot


from messenger.models import (
    BotUser
)
from .message_utils import (
    element,
    web_button,
    postback_button,
    share_with_template
)

from .general_utils import (
    handle_get_started,
    send_share_template
)

site_url = settings.SITE_URL
messenger_bot = Bot(settings.PAGE_ACCESS_TOKEN)


def handle_post_back(recipient_id, payload):

    if payload == 'get_started':
        current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
        name = current_bot_user.get_name()

        message = 'Hi  %s,  thanks for getting in touch!' % name
        handle_get_started(recipient_id, message=message)

    if payload == 'measure_engagement':
        handle_measure_engagement(recipient_id)

    if payload == 'honesty_box':
        handle_honesty_box_postback(recipient_id)


def handle_measure_engagement(recipient_id):

    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    group_id = current_bot_user.current_group_id

    send_share_template(recipient_id=recipient_id, group_id=group_id, type='survey')


def handle_honesty_box_postback(recipient_id):

    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    group_id = current_bot_user.current_group_id
    send_share_template(recipient_id=recipient_id, group_id=group_id, type='honesty_box')
