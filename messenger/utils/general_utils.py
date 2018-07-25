import urllib.parse
import json
import requests
from pymessenger.bot import Bot
from django.conf import settings
from pamoja.models import (
    Group,
    Survey,
    SurveyQuestion
)

from messenger.models import (
    BotUser
)

from .message_utils import (
    text_quick_reply,
    web_button,
    element,
    share_with_template,
    postback_button
)

page_access_token = settings.PAGE_ACCESS_TOKEN
messenger_bot = Bot(page_access_token)


def send_survey(recipient_id, group_id):

    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    current_group = Group.objects.get(id=group_id)
    current_survey = Survey.objects.all().first()
    current_bot_user.question_ids = json.dumps([question.id for question in current_survey.questions.all()])
    current_bot_user.current_question_index = 0
    current_bot_user.save()

    message = 'Hi 👋, you are taking a Sense of Community survey for ' + current_group.name
    messenger_bot.send_text_message(recipient_id=recipient_id, message=message)
    message = "It will take you 2 minutes only 😄. Let's go 🚀"
    messenger_bot.send_text_message(recipient_id=recipient_id, message=message)
    send_question(current_bot_user, current_survey)


def send_question(current_bot_user, current_survey):
    current_question_ids = json.loads(current_bot_user.question_ids)

    if current_bot_user.current_question_index >= len(current_question_ids):

        current_bot_user.current_survey_result_id = None
        current_bot_user.save()

        message = "Thanks for taking the survey. It helps us improve our community!"
        messenger_bot.send_text_message(recipient_id=current_bot_user.messenger_id, message=message)
        message = "🎈"
        messenger_bot.send_text_message(recipient_id=current_bot_user.messenger_id, message=message)

    else:
        question_id = current_question_ids[current_bot_user.current_question_index]

        current_question = SurveyQuestion.objects.get(id=question_id)

        message = {
            'text': str(current_bot_user.current_question_index + 1) + ' : ' + current_question.question,
        }

        quick_replies = []

        choices = ['Not at all', 'Somewhat', 'Mostly', 'Completely']

        for i in range(4):
            quick_replies.append(
                text_quick_reply(
                    title=choices[i],
                    payload=json.dumps(
                        {
                            'question_id': question_id,
                            'survey_id': current_survey.id,
                            'rating': i + 1
                        }
                    )
                )
            )

        message['quick_replies'] = quick_replies

        messenger_bot.send_action(recipient_id=current_bot_user.messenger_id, action='typing_on')
        messenger_bot.send_message(recipient_id=current_bot_user.messenger_id, message=message)


def send_share_template(recipient_id, group_id, type=None):
    """

    :param recipient_id:
    :param group_id:
    :return:
    """

    current_group = Group.objects.get(id=group_id)

    if type == 'survey':
        data = {
            'survey_ref': {
                'data': {
                    'group_id': group_id
                }
            }
        }

        message = '🖱️Tap share to send Sense of Community survey link to ' + current_group.name + ' members '

        url = 'https://m.me/452174761913102?ref=' + urllib.parse.quote(json.dumps(data))
        res = requests.get('http://tinyurl.com/api-create.php?url=' + url)
        share_url = res.text

        share_elements = [
            element(
                title='How helpful is this community❓',
                subtitle='We want to gauge sense of community, belonging & satisfaction in ' + current_group.name +  ' group. Take a quick survey 👇',
                buttons=[
                    web_button(
                        title='Take Survey 🙋',
                        url=share_url
                    )
                ]
            )
        ]

    else:
        data = {
            'honesty_box_ref': {
                'data': {
                    'group_id': group_id
                }
            }
        }

        message = '🖱️Share honesty box link for ' + current_group.name + ' members to post anonymously'

        url = 'https://m.me/452174761913102?ref=' + urllib.parse.quote(json.dumps(data))
        res = requests.get('http://tinyurl.com/api-create.php?url=' + url)
        share_url = res.text

        share_elements = [
            element(
                title='💌Honesty Box',
                subtitle="Now you can post sensitive questions anonymously and get help from " + current_group.name + " members ",
                buttons=[
                    web_button(
                        title='Post anonymously 📤',
                        url=share_url,
                        messenger_extensions=True,
                        height='full'
                    )
                ]
            )
        ]

    elements = (
        element(
            title='✔️Send to Messenger group',
            subtitle=message,
            buttons=[
                share_with_template(share_elements)
            ]
        ),
        element(
            title='✅Send to WhatsApp group',
            subtitle=message,
            buttons=[
                web_button(
                    title='Share on whatsapp',
                    url='https://wa.me/?text=' + share_url
                )
            ]
        )
    )

    messenger_bot.send_generic_message(recipient_id=recipient_id, elements=elements)


def handle_get_started(recipient_id, message=""):
    """
        * Handles the case where a get_started button is tapped

    :param recipient_id:
    :param message
    :return:
    """

    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)

    if not current_bot_user.current_group_id:
        handle_no_group(recipient_id=recipient_id)
        return

    elements = [
        element(
            title='📈Group Activity Score',
            subtitle='➡️Navigate to Group Insights on Facebook to get this data',
            buttons=[
                web_button(
                    title='Activity Score 🔢',
                    url=settings.SITE_URL+'/get_group_info/' + str(current_bot_user.current_group_id),
                    messenger_extensions=True,
                    height='full'
                )
            ]
        ),
        element(
            title='✉️HonestyBox',
            subtitle='Give members a voice to seek help with the power to post anonymously',
            buttons =[
                postback_button(
                    title='Give a voice 🎤',
                    payload='honesty_box',
                )
            ]
        ),
        element(
            title='👪 Sense of community (SOC)',
            subtitle="📉Gauge sense of community with the scientific SOC(V) index survey",
            buttons =[
                postback_button(
                    'Measure SOC 🌡️',
                    payload='measure_engagement'
                )
            ]
        ),
        element(
            title='📊Dashboard',
            subtitle="👀See Pawa stats & insights on your group",
            buttons=[
                web_button(
                    title="Go to Dashboard ➡️",
                    url=settings.SITE_URL + '/dashboard/' + str(current_bot_user.current_group_id),
                    messenger_extensions=True,
                    height='full'
                )
            ]
        ),

        element(
            title='📥Honesty Inbox',
            subtitle='👀View, post or delete sensitive content shared anonymously',
            buttons = [
                web_button(

                    title="Go to Inbox ➡️",
                    url=settings.SITE_URL + '/posts/' + str(current_bot_user.current_group_id),
                    messenger_extensions=True,
                    height='full'

                )
            ]
        )
    ]

    messenger_bot.send_text_message(recipient_id, message=message)
    messenger_bot.send_action(recipient_id=recipient_id, action='typing_on')
    messenger_bot.send_generic_message(recipient_id=recipient_id, elements=elements)


def handle_no_group(recipient_id):

    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)

    message = "Hi %s" % current_bot_user.get_name()
    messenger_bot.send_text_message(recipient_id=recipient_id, message=message)

    message = 'This bot is meant for group admins, You must chose a group first. Click below to see our Landing page'

    buttons = [
        web_button(
            title='Pawa Page',
            url='http://localhost:3000'
        )
    ]

    messenger_bot.send_action(recipient_id=recipient_id, action='typing_on')
    messenger_bot.send_button_message(recipient_id=recipient_id, text=message, buttons=buttons)





