#!/bin/bash

BUCKET_NAME="gnk263-lambda-bucket"

sam package \
    --output-template-file packaged.yaml \
    --s3-bucket $BUCKET_NAME
