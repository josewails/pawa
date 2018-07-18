import json

from messenger.models import (
    BotUser
)

from pamoja.models import (
    Survey,
    SurveyResult,
    SurveyQuestion
)

from .general_utils import (
    send_question
)


def handle_quick_reply(recipient_id, quick_reply_message):

    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    payload = json.loads(quick_reply_message['payload'])

    if 'rating' in payload:
        handle_rating(current_bot_user, payload)


def handle_rating(current_bot_user, payload):

    current_survey, _ = Survey.objects.get_or_create(id=payload['survey_id'])
    current_question, _ = SurveyQuestion.objects.get_or_create(id=payload['question_id'])

    if not current_bot_user.current_survey_result_id:
        survey_result = SurveyResult.objects.create(survey=current_survey)
        current_bot_user.current_survey_result_id = survey_result.id
        current_bot_user.save()

    else:
        survey_result = SurveyResult.objects.get(id=current_bot_user.current_survey_result_id)

    current_result = json.loads(survey_result.result)
    current_question_category = current_question.category

    current_result[current_question_category-1].append(payload['rating'])
    survey_result.result = json.dumps(current_result)
    survey_result.save()

    current_bot_user.current_question_index = current_bot_user.current_question_index + 1
    current_bot_user.save()

    send_question(current_bot_user=current_bot_user, current_survey=current_survey)