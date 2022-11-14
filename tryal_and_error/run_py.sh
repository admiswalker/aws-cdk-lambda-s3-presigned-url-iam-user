#!/bin/bash

PRJ_NAME=pyenv
source ${PRJ_NAME}/bin/activate
python main.py

#event=1
#context=2
#export S3_PROCED_BUCKET_NAME='infrastack-s3procedbucketddxxxxxx-xxxxxxxxxxxx'
#export S3_PROCED_BUCKET_NAME='infrastack-s3procedbucketdd1881e7-j35xb16da13f'
#python -c "import index; index.handler($event,$context)"

