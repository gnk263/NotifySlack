import os
import json

import requests

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]

def lambda_handler(event, context):

    print("hello world")

    post_slack("This is test message.")

def post_slack(message):
    payload = {
        "text": message,
        "channel": SLACK_CHANNEL
    }

    # http://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/
    try:
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        print(response.status_code)
