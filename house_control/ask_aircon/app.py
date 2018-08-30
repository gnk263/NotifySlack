import os
import json

import requests


def lambda_handler(event, context):

    print("hello world")
    print(os.environ["SLACK_WEBHOOK_URL"])
    print(os.environ["SLACK_CHANNEL"])
