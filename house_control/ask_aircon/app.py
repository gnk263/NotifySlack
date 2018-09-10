import os
import json

import requests

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

def lambda_handler(event, context):
    post_slack("エアコンをOnにしますか？")

def post_slack(message):
    payload = {
        "attachments": [
            {
                "text": message,
                "callback_id": "ask_aircon",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "aircon",
                        "text": "Yes",
                        "type": "button",
                        "value": "yes"
                    },
                    {
                        "name": "aircon",
                        "text": "No",
                        "type": "button",
                        "value": "no"
                    }
                ]
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
