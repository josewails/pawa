import json
from unittest.mock import patch
from django.test import TestCase
from pymessenger import Bot
from messenger.utils.post_back_utils import (
    handle_post_back
)

from messenger.utils.referral_utils import  (
    handle_referral
)

from messenger.utils.general_utils import (
    send_survey,
    send_share_template
)

from .factories import (
    BotUserFactory
)

from messenger.utils.quick_reply_utils import (
    handle_quick_reply
)

from pamoja.factories import  (
    SurveyFactory,
    SurveyQuestionFactory,
    GroupAdminFactory,
    GroupFactory
)



class TestPostBack(TestCase):

    def setUp(self):
        self.bot_user = BotUserFactory()

    @patch.object(Bot,'send_text_message')
    @patch.object(Bot, 'send_action')
    @patch.object(Bot, 'send_generic_message')
    def test_get_started(self, send_text_message, send_action, send_generic_message):

        handle_post_back(recipient_id=self.bot_user.messenger_id, payload='get_started')

        # Assert the method send_text_message is called once.

        self.assertEqual(send_text_message.call_count, 1)
        self.assertEqual(send_action.call_count, 1)
        self.assertEqual(send_generic_message.call_count, 1)

    @patch.object(Bot, 'send_button_message')
    def test_handle_measure_engagement(self, send_button_message):

        handle_post_back(recipient_id=self.bot_user.messenger_id, payload='measure_engagement')

        # Assert that the send_button message is used only once
        self.assertEqual(send_button_message.call_count, 1)

    @patch.object(Bot, 'send_button_message')
    def test_handle_honesty_box_postback(self, send_button_message):

        handle_post_back(recipient_id=self.bot_user.messenger_id, payload='honesty_box')

        # Assert that send_button_message is called only once
        self.assertEqual(send_button_message.call_count, 1)


class TestReferral(TestCase):

    def setUp(self):
        self.bot_user = BotUserFactory()
        self.group_admin = GroupAdminFactory()
        self.group = GroupFactory(admin=self.group_admin)

    @patch.object(Bot, 'send_text_message')
    def test_web_referral(self, send_text_message):

        handle_referral(self.bot_user.messenger_id, referral='pamojaness_messenger', ref_type='optin')

        # Assert the send_text_message is called once

        self.assertEqual(send_text_message.call_count, 1)


    @patch.object(Bot, 'send_button_message')
    def test_honesty_box_ref(self, send_button_message):

        data = {
            'honesty_box_ref': {
                'data': {
                    'group_id': self.group.id
                }
            }
        }

        handle_referral(self.bot_user.messenger_id, referral=json.dumps(data), ref_type='normal')

        self.assertEqual(send_button_message.call_count, 1)


class TestQuickReply(TestCase):

    def setUp(self):
        self.bot_user = BotUserFactory()
        self.group_admin = GroupAdminFactory()
        self.group = GroupFactory(admin=self.group_admin)
        self.survey = SurveyFactory(group=self.group)

        self.survey_questions = []

        for i in range(5):
            self.survey_questions.append(SurveyQuestionFactory(survey=self.survey))

    @patch.object(Bot, 'send_action')
    @patch.object(Bot, 'send_message')
    def test_handle_rating(self, send_message, send_action):
        data = {
            'payload': json.dumps(
                    {
                        'question_id': self.survey_questions[0].id,
                        'survey_id': self.survey.id,
                        'rating': 1

                    }
                )

            }

        handle_quick_reply(recipient_id=self.bot_user.messenger_id, quick_reply_message=data)

        self.assertEqual(send_message.call_count, 1)
        self.assertEqual(send_action.call_count, 1)


class TestGeneral(TestCase):

    def setUp(self):
        self.group_admin = GroupAdminFactory()
        self.group = GroupFactory(admin=self.group_admin)

        self.bot_user = BotUserFactory()
        self.survey = SurveyFactory(group=self.group)

        self.survey_questions = []
        for i in range(5):
            self.survey_questions.append(SurveyQuestionFactory(survey=self.survey))

    @patch.object(Bot, 'send_action')
    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_text_message')
    def test_send_survey(self, send_text_message, send_message, send_action):

        send_survey(recipient_id=self.bot_user.messenger_id, group_id=self.survey.group.id)

        self.assertEqual(send_text_message.call_count, 1)
        self.assertEqual(send_message.call_count, 1)
        self.assertEqual(send_action.call_count, 1)

    @patch.object(Bot, 'send_generic_message')
    def test_share_template(self, send_generic_message):

        send_share_template(self.bot_user.messenger_id, self.group.id, type='survey')
        self.assertEqual(send_generic_message.call_count, 1)

        send_share_template(self.bot_user.messenger_id, self.group.id, type='honesty_box')
        self.assertEqual(send_generic_message.call_count, 2)






