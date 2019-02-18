import os
import boto3
import json
import requests
from datetime import timedelta
from datetime import date

SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

# https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/monitoring/viewing_metrics_with_cloudwatch.html
# https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/list-metrics.html
# aws cloudwatch list-metrics --namespace "AWS/Billing" --region us-east-1
# このリスト内容はユーザ毎に異なる
BILLING_SERVICE_LIST = [
    'AWSBudgets',
    'AWSIoT',
    'AmazonDynamoDB',
    'AmazonCloudWatch',
    'AmazonEC2',
    'AWSLambda',
    'AWSDataTransfer',
    'AmazonS3',
    'AmazonApiGateway',
    'AWSMarketplace',
]


def lambda_handler(event, context):
    (title, detail) = get_message()
    post_slack(title, detail)


def get_aws_billing():
    resource = boto3.client('cloudwatch', region_name='us-east-1')

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_data
    # https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html
    # https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html
    response = resource.get_metric_data(
        MetricDataQueries=get_metrics(),
        StartTime=get_yesterday_datetime(),
        EndTime=get_today_datetime(),
    )
    return formatting(response)


def get_metrics():
    # 合計取得
    metrics = [
        {
            'Id': 'all',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/Billing',
                    'MetricName': 'EstimatedCharges',
                    'Dimensions': [
                        {
                            'Name': 'Currency',
                            'Value': 'USD'
                        }
                    ],
                },
                'Period': 24 * 60 * 60,
                'Stat': 'Maximum'
            }
        }
    ]

    # サービス毎に取得
    for service_name in BILLING_SERVICE_LIST:
        metrics.append({
            # 先頭が大文字だと怒られるためすべて小文字にする
            'Id': service_name.lower(),
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/Billing',
                    'MetricName': 'EstimatedCharges',
                    'Dimensions': [
                        {
                            'Name': 'Currency',
                            'Value': 'USD'
                        },
                        {
                            'Name': 'ServiceName',
                            'Value': service_name
                        }
                    ],
                },
                'Period': 24 * 60 * 60,
                'Stat': 'Maximum'
            }
        })

    return metrics


def formatting(response):
    details = []

    for item in response['MetricDataResults']:
        label = item['Label']
        timestamp = item['Timestamps'][0].strftime('%Y/%m/%d')
        billing = item['Values'][0]

        if label == 'EstimatedCharges':
            total = {
                'timestamp': timestamp,
                'billing': billing
            }
        else:
            details.append({
                'service_name': label,
                'billing': billing
            })

    return {
        'total': total,
        'details': details
    }


def get_message():
    billings = get_aws_billing()

    timestamp = billings['total']['timestamp']
    total_billing = billings['total']['billing']

    title = f'{timestamp}までの請求額は、{total_billing} USDです。'

    details = []
    for item in billings['details']:
        if item['billing'] == 0.0:
            # 請求無し（0.0 USD）の場合は、内訳を表示しない
            continue
        service_name = item['service_name']
        billing = item['billing']
        details.append(f'　・{service_name}: {billing} USD')

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


def get_yesterday_datetime():
    today = date.today()
    yesterday = today - timedelta(days=1)

    # ISO 8601
    return yesterday.isoformat()


def get_today_datetime():
    # ISO 8601
    return date.today().isoformat()
