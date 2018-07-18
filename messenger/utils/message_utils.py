def element(title, subtitle=None, image_url=None, default_action=None, buttons=None):

    """
        * This creates an element for facebook messenger generic template.

    :param title: The title of the element.
    :param subtitle: The subtitle of the element.
    :param image_url: The image_url of the element.
    :param default_action: The default_action of the element.
    :param buttons: A list of buttons for this element
    :return:
        element data
    """
    data = {
        'title': title,
        'image_url': image_url,
        'subtitle': subtitle,
        'default_action': default_action,
        'buttons': buttons,
    }

    return data



def text_quick_reply(title, payload):
    """
     ->Generate a quick reply with the title as title and payload as payload

    :param title:
    :param payload:
    :return:
    """
    quick_reply = {
        "content_type": "text",
        "title": title,
        "payload": payload
    }
    return quick_reply


def web_button(title, url, messenger_extensions=False, height='full'):
    """
        * This creates a web button for facebook messenger

    :param title: The title of the button.
    :param url: The url of the button.
    :param messenger_extensions:  This determines whether messenger extensions are enabled or not.
    :param height: The height of the webview if enabled <compact, tall, full>
    :return:
        button data
    """

    button = {
        'type': 'web_url',
        'title': title,
        'url': url,
        'messenger_extensions': messenger_extensions,
        'webview_height_ratio': height
    }

    return button


def postback_button(title, payload):

    """
        * This creates a postback button for facebook messenger.

    :param title: The title of the button.
    :param payload: The payload of the button
    :return:
        button data
    """

    button = {
        'type': 'postback',
        'title': title,
        'payload': payload
    }

    return button


def share_with_template(elements):
    """
        * This creates a share button for facebook messenger

    :param elements: elements that will show up when this share button is clicked

    :return:
    """
    btn = {
        "type": "element_share",
        "share_contents": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }
    }

    return btn