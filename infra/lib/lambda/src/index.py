import aws_s3_wrapper as s3
import os


def main():

    S3_PROCED_BUCKET_NAME = os.environ['S3_PROCED_BUCKET_NAME']
    print('S3_PROCED_BUCKET_NAME', S3_PROCED_BUCKET_NAME)

    bucket = S3_PROCED_BUCKET_NAME
    l_key = s3.ls(bucket)
    key = l_key[0]

    dst_path = '/tmp'
    s3.download_file(dst_path, 's3://'+bucket+'/'+key)

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
