@echo off
rem S3にパッケージ化する

aws cloudformation deploy --template-file packaged.yaml --stack-name notify-slack-aircon --capabilities CAPABILITY_IAM
