@echo off
rem S3にパッケージ化する

aws cloudformation package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket gnk263-lambda-bucket
