import json

from urllib.parse import unquote
from common_lambda import get_notify_delays, get_message


def lambda_handler(event, context) -> dict:
    # 受信したパラメータを解析する
    request_param = parse_slash_commands(event['body'])
    print(json.dumps(request_param))

    if request_param['command'] != '/train':
        # 想定コマンドと異なるため何もしない
        return {
            "statusCode": 200,
        }

    notify_delays = get_notify_delays()

    # Slack用のメッセージを作成して返却する
    (title, detail) = get_message(notify_delays)

    # https://api.slack.com/incoming-webhooks
    # https://api.slack.com/docs/message-formatting
    # https://api.slack.com/docs/messages/builder
    # https://api.slack.com/slash-commands
    payload = {
        'response_type': 'ephemeral',    # コマンドを起動したユーザのみに返答する
        'attachments': [
            {
                'color': '#36a64f',
                'pretext': title,
                'text': detail
            }
        ]
    }

    return {
        "statusCode": 200,
        "body": json.dumps(payload)
    }


def parse_slash_commands(payload) -> dict:
    """Slash commandsのパラメータを解析する

    Args:
        payload: 受信したSlash commandsのパラメータ

    Returns:
        dict: 解析したパラメータとその内容
    """
    params = {}
    key_value_list = unquote(payload).split("&")
    for item in key_value_list:
        (key, value) = item.split("=")
        params[key] = value
    return params
