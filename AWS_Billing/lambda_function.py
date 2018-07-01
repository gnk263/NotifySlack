import os
import boto3
from datetime import datetime

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]

def lambda_handler(event, context):
    # TODO implement
    return 'Hello from Lambda'

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
        StartTime=get_month_first_datetime(),
        EndTime=get_current_datetime(),
        Period=24*60*60,
        Statistics=["Maximum"]
    )

    billing = response["Datapoints"][0]["Maximum"]
    timestamp = response["Datapoints"][0]["Timestamp"].strftime("%Y/%m/%d")

    return (billing, timestamp)

def get_month_first_datetime():
    today = datetime.today()
    year = today.year
    month = today.month

    #ISO 8601
    return datetime(year, month, 1, 0, 0, 0).isoformat()

def get_current_datetime():
    #ISO 8601
    return datetime.today().isoformat()