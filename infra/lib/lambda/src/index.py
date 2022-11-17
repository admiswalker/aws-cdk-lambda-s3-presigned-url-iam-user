import os
import boto3
import botocore

import aws_s3_wrapper as s3


def get_ssm_parameters(param_key):
    region = 'ap-northeast-1'
    ssm = boto3.client('ssm', region_name=region)

    ret = ssm.get_parameters(
        Names=[
            param_key,
        ],
    )
    return ret['Parameters'][0]['Value']

def main():

    S3_PROCED_BUCKET_NAME = os.environ['S3_PROCED_BUCKET_NAME']
    SECRET_NAME = os.environ['SECRET_NAME']
    print('S3_PROCED_BUCKET_NAME', S3_PROCED_BUCKET_NAME)
    print('SECRET_NAME', SECRET_NAME)

    bucket = S3_PROCED_BUCKET_NAME
    l_key = s3.ls(bucket)
    key = l_key[0]
    print('key', key)

    dst_path = '/tmp'
    src_path = 's3://'+bucket+'/'+key
    s3.download_file(dst_path, src_path)
    print('dl end')

    days=int(7)
    access_id = get_ssm_parameters('secret-access-key-id')
    access_key = get_ssm_parameters('secret-access-key')
    presigned_url = s3.gen_presigned_url_key_id(src_path, days, access_id, access_key)
    print('presigned_url', presigned_url)
    
    return


def handler(event, context):
    ret = "event: " + str(event) + "context: " + str(context)
    
    print()
    print('--- begin: main() --------------------------------')
    main()
    print('---------------------------------- end: main() ---')
    print()
    
    return ret
