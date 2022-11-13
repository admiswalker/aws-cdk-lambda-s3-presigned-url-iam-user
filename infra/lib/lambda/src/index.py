import aws_s3_wrapper as s3
import os

#import botocore 
#import botocore.session 
#from aws_secretsmanager_caching import SecretCache, SecretCacheConfig 


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
    s3.download_file(dst_path, 's3://'+bucket+'/'+key)
    print('dl end')

    presigned_url = s3.gen_presigned_url(bucket, key, days=int(7))
    print(presigned_url)
    
    return


def handler(event, context):
    ret = "event: " + str(event) + "context: " + str(context)
    
    print()
    print('--- begin: main() --------------------------------')
    main()
    print('---------------------------------- end: main() ---')
    print()
    
    return ret
