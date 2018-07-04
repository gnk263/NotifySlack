import os
import boto3
import json
import requests
from datetime import timedelta
from datetime import datetime

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]
AWS_ACCOUNT_NAME = os.environ["AWS_ACCOUNT_NAME"]

def lambda_handler(event, context):
    message = get_message()
    post_slack(message)

def get_aws_billing():
    resource = boto3.client("cloudwatch", region_name="us-east-1")

    #https://boto3.readthedocs.io/en/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_statistics
    #https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-namespaces.html
    #https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/billing-metricscollected.html
    response = resource.get_metric_statistics(
        Namespace="AWS/Billing",
        MetricName="EstimatedCharges",
        Dimensions=[
            {
                "Name": "Currency",
                "Value": "USD"
            }
        ],
        StartTime=get_yesterday_datetime(),
        EndTime=get_current_datetime(),
        Period=24*60*60,
        Statistics=["Maximum"]
    )

    billing = response["Datapoints"][0]["Maximum"]
    timestamp = response["Datapoints"][0]["Timestamp"].strftime("%Y/%m/%d")

    return (billing, timestamp)

def get_message():
    (billing, timestamp) = get_aws_billing()
    return f"[{AWS_ACCOUNT_NAME}]\n{timestamp}までの請求金額は ${billing} です。"

def post_slack(message):
    payload = {
        "text": message,
        "channel": SLACK_CHANNEL
    }

    #http://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/
    try:
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        print(response.status_code)

def get_yesterday_datetime():
    today = datetime.today()
    yesterday = today - timedelta(days=1)

    #ISO 8601
    return yesterday.isoformat()

def get_current_datetime():
    #ISO 8601
    return datetime.today().isoformat()