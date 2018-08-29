@echo off
rem S3にパッケージ化する

sam deploy --template-file packaged.yaml --stack-name notify-slack-aircon --capabilities CAPABILITY_IAM
