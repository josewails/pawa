from .general_utils import (
    send_survey
)

from .general_utils import (
    handle_get_started
)

def handle_text_message(recipient_id, text_message):
    handle_get_started(recipient_id)