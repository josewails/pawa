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
    print(current_group)
    current_survey = Survey.objects.get(group=current_group)
    current_bot_user.question_ids = json.dumps([question.id for question in current_survey.questions.all()])
    current_bot_user.current_question_index = 0
    current_bot_user.save()

    message = 'You are taking a quick survey for ' + current_group.name + ' Facebook Group'
    messenger_bot.send_text_message(recipient_id=recipient_id, message=message)
    send_question(current_bot_user, current_survey)


def send_question(current_bot_user, current_survey):
    current_question_ids = json.loads(current_bot_user.question_ids)

    if current_bot_user.current_question_index >= len(current_question_ids):

        current_bot_user.current_survey_result_id = None
        current_bot_user.save()

        message = "Thanks for taking the survey"
        messenger_bot.send_text_message(recipient_id=current_bot_user.messenger_id, message=message)

    else:
        question_id = current_question_ids[current_bot_user.current_question_index]

        current_question = SurveyQuestion.objects.get(id=question_id)

        message = {
            'text': str(current_bot_user.current_question_index + 1) + ' : ' + current_question.question,
        }

        quick_replies = []

        for i in range(4):
            quick_replies.append(
                text_quick_reply(
                    title=str(i + 1),
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

        message = "Click below to share the survey for " + current_group.name

        url = 'https://m.me/452174761913102?ref=' + urllib.parse.quote(json.dumps(data))
        res = requests.get('http://tinyurl.com/api-create.php?url=' + url)
        share_url = res.text

        share_elements = [
            element(
                title='Quick Survey',
                subtitle='Quick Survey for ' + current_group.name,
                buttons=[
                    web_button(
                        title='Take Survey',
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

        message = 'Click below to share honesty box for ' + current_group.name

        url = 'https://m.me/452174761913102?ref=' + urllib.parse.quote(json.dumps(data))
        res = requests.get('http://tinyurl.com/api-create.php?url=' + url)
        share_url = res.text

        share_elements = [
            element(
                title='Post Anonymously',
                subtitle="Now you can post anonymously to " + current_group.name,
                buttons=[
                    web_button(
                        title='Post Now',
                        url=share_url,
                        messenger_extensions=True,
                        height='full'
                    )
                ]
            )
        ]

    elements = (
        element(
            title='Share on messenger',
            subtitle=message + ' on facebook messenger',
            buttons=[
                share_with_template(share_elements)
            ]
        ),
        element(
            title='Share on whatsapp',
            subtitle=message + ' on whatsapp',
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

    elements = [
        element(
            title='Activity_score',
            subtitle='Now you can see the activity score of your group',
            buttons=[
                web_button(
                    title='Activity Score',
                    url=settings.SITE_URL+'/get_group_info/' + str(current_bot_user.current_group_id),
                    messenger_extensions=True,
                    height='full'
                )
            ]
        ),
        element(
            title='Honesty Box',
            subtitle='This is a small honesty box that you want to hear about',
            buttons =[
                postback_button(
                    title='Honesty Box',
                    payload='honesty_box',
                )
            ]
        ),
        element(
            title='Engagement',
            subtitle="Measure Engagment and satisfaction score",
            buttons =[
                postback_button(
                    'Measure',
                    payload='measure_engagement'
                )
            ]
        ),
        element(
            title='Dashaboard',
            subtitle="Show dashboard results",
            buttons=[
                web_button(
                    title="Dashboard",
                    url=settings.SITE_URL + '/dashboard/' + str(current_bot_user.current_group_id),
                    messenger_extensions=True,
                    height='full'
                )
            ]
        ),

        element(
            title='Honesty Inbox',
            subtitle='Shows all anonymous posts',
            buttons = [
                web_button(
                    title="Honesty Inbox",
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




