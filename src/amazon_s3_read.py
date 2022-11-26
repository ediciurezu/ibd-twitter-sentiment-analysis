
import boto3
import boto.s3
from boto.s3.key import Key

def read_from_bucket_version_boto3(bucket_name, aws_access_key_id, aws_secret_access_key, key):
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    s3 = session.resource('s3')
    obj = s3.Object(bucket_name, key)
    body = obj.get()['Body'].read().decode('utf-8') 
    print(f'{key} -> {body}')

def read_from_bucket_version_boto(bucket_name, aws_access_key_id, aws_secret_access_key, key):
    conn = boto.connect_s3(aws_access_key_id,
                        aws_secret_access_key)

    bucket = conn.get_bucket(bucket_name)
    k = Key(bucket)
    k.key = key
    body = k.get_contents_as_string()
    print(f'{key} -> {body}')



read_from_bucket_version_boto3('test-ibd', AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, 'test file ioana')
read_from_bucket_version_boto('test-ibd', AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, 'test file ioana')