import os

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]

def lambda_handler(event, context):
    # TODO implement
    return 'Hello from Lambda'
