import io
import os
from urllib.parse import urlparse

import boto3
from botocore.client import Config


def __split_s3_path(path):
    
    o = urlparse(path)
    bucket = o.hostname
    key = o.path.lstrip('/').rstrip('/')
    
    return bucket, key

def __join_keyBase_fileName(key_base, file_name):
    key = key_base+'/'+file_name if len(key_base)>0 else file_name
    return key

def upload_file(dst_path, src_path):
    
    bucket, key_base = __split_s3_path(dst_path)
    file_name = os.path.basename(src_path)
    
    key = __join_keyBase_fileName(key_base, file_name)
    
    s3 = boto3.client('s3')
    s3.upload_file(src_path, bucket, key)
    
    return

def upload_fileobj(dst_path, bin_obj):
    
    bucket, key = __split_s3_path(dst_path)
    
    s3 = boto3.client('s3')
    s3.upload_fileobj(bin_obj, bucket, key)
    
    return

def upload_str(dst_path, s, encoding):

    bin_obj = io.BytesIO(bytes(s, encoding=encoding))
    upload_fileobj(dst_path, bin_obj)
    
    return

def download_file_id_key(dst_path, src_path, access_id, access_key):
    os.makedirs(dst_path, exist_ok=True)
    
    bucket, key = __split_s3_path(src_path)
    file_name = os.path.basename(src_path)
    dst_path = dst_path.rstrip('/')

    #session = boto3.Session(aws_access_key_id=access_id, aws_secret_access_key=access_key)
    #s3 = session.client('s3')
    s3 = boto3.client('s3', aws_access_key_id=access_id, aws_secret_access_key=access_key)
    s3.download_file(bucket, key, dst_path+'/'+file_name)
    
    return 

def download_file(dst_path, src_path):
    os.makedirs(dst_path, exist_ok=True)
    
    bucket, key = __split_s3_path(src_path)
    file_name = os.path.basename(src_path)
    dst_path = dst_path.rstrip('/')
    
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, dst_path+'/'+file_name)
    
    return 

def download_fileobj(fp, src_path):
    
    bucket, key = __split_s3_path(src_path)
    file_name = os.path.basename(src_path)
    
    s3 = boto3.client('s3')
    s3.download_fileobj(bucket, key, fp)
    
    return

def download_as_bin(src_path):
    
    bin_obj = ''
    with io.BytesIO() as fp:
        download_fileobj(fp, src_path)
        bin_obj = fp.getvalue()
        
    return bin_obj

def download_as_str(src_path, encoding):

    binary = download_as_bin(src_path)
    
    s = str(binary, encoding=encoding, errors='replace')
    
    return s

def ls(bucket):
    s3 = boto3.resource('s3')
    bucket_obj = s3.Bucket(bucket)

    l_key = []
    for obj in bucket_obj.objects.all():
        l_key.append(obj.key)
    
    return l_key

def gen_presigned_url(src_path, days):

    bucket, key = __split_s3_path(src_path)
    
    s3 = boto3.client('s3')
    presigned_url = s3.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {'Bucket' : bucket, 'Key' : key},
        ExpiresIn = (24*60*60)*days,
        HttpMethod = 'GET')
    return presigned_url

def gen_presigned_url_key_id(src_path, days, access_id, access_key):
    
    bucket, key = __split_s3_path(src_path)
    
    s3 = boto3.client('s3', aws_access_key_id=access_id, aws_secret_access_key=access_key, config=Config(signature_version='s3v4'))
    presigned_url = s3.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {'Bucket' : bucket, 'Key' : key},
        ExpiresIn = (24*60*60)*days,
        HttpMethod = 'GET')
    return presigned_url

