#!/bin/bash

WEBHOOK_URL="https://hoge"

sam deploy \
    --template-file packaged.yaml \
    --stack-name NotifyBillingToSlack \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides SlackWebhookUrl=$WEBHOOK_URL
