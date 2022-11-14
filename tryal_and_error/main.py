import boto3
import aws_s3_wrapper as s3



def main():
    aws_access_key_id=""
    aws_secret_access_key=""
    
    src_path = 's3://infrastack-s3rawbucket833c2224-1y1a9ch1oxk4i/example_2022_1113.txt'
    
    #client = boto3.client('iam',aws_access_key_id="XXX",aws_secret_access_key="XXX")
    #client = boto3.client('iam',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    #users = client.list_users()
    #print(users)
    #exit(0)

    #dst_path = './'
    #s3.download_file_id_key(dst_path, src_path, aws_access_key_id, aws_secret_access_key)

    days=7
    presigned_url = s3.gen_presigned_url_key_id(src_path, days, aws_access_key_id, aws_secret_access_key)
    print('presigned_url', presigned_url)
    
    return

def get_ssm_parameters(param_key):
    region = 'ap-northeast-1'
    ssm = boto3.client('ssm', region_name=region)

    ret = ssm.get_parameters(
        Names=[
            param_key,
        ],
    )
    return = ret['Parameters'][0]['Value']


def test():
    get_ssm_parameters('secret-access-key-id')
    get_ssm_parameters('secret-access-key')
    return


#main()
test()


