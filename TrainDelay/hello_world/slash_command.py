import os
import json
import requests

from common_lambda import get_notify_delays, get_message

# https://api.slack.com/methods/chat.postEphemeral
SLACK_EPHEMERAL_URL = "https://slack.com/api/chat.postEphemeral"


def lambda_handler(event, context) -> None:

    notify_delays = get_notify_delays()

    # Slack用のメッセージを作成して投げる
    (title, detail) = get_message(notify_delays)
    post_slack(title, detail)

    return


def post_slack(title, detail) -> None:
    """SlackにPostする

    Args:
        title: メッセージのタイトル
        detail: メッセージの詳細（遅延情報）

    Returns:

    """
    # https://api.slack.com/incoming-webhooks
    # https://api.slack.com/docs/message-formatting
    # https://api.slack.com/docs/messages/builder
    payload = {
        'attachments': [
            {
                'color': '#36a64f',
                'pretext': title,
                'text': detail
            }
        ]
    }

    # http://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/
    try:
        response = requests.post(SLACK_EPHEMERAL_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        print(response.status_code)
