import os
import json
import requests


JSON_ADDR = 'https://rti-giken.jp/fhc/api/train_tetsudo/delay.json'

SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']


def lambda_handler(event, context):

    notify_delays = get_notify_delays()

    if not notify_delays:
        # 遅延が無ければ通知しない
        return

    # Slack用のメッセージを作成して投げる
    (title, detail) = get_message(notify_delays)
    post_slack(title, detail)

    return


def get_notify_delays():

    current_delays = get_current_delays()

    target_list = get_target_list()

    notify_delays = []

    for delay_item in current_delays:
        for check_item in target_list:
            if delay_item['name'] == check_item['name'] and delay_item['company'] == check_item['company']:
                notify_delays.append(check_item)

    return notify_delays


def get_target_list():
    with open('target.json') as f:
        return json.load(f)


def get_current_delays():
    try:
        res = requests.get(JSON_ADDR)
    except requests.RequestException as e:
        print(e)
        raise e

    if res.status_code == 200:
        return json.loads(res.text)
    return []


def get_message(delays):
    title = "電車の遅延があります。"

    details = []

    for item in delays:
        company = item['company']
        name = item['name']
        website = item['website']
        details.append(f'・{company}： {name}： <{website}|こちら>')

    return title, '\n'.join(details)


def post_slack(title, detail):
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
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        print(response.status_code)