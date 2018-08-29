import os
import json

import requests


def lambda_handler(event, context):

    print("hello world")
    print(os.environ["POST_SLACK_URL"])
