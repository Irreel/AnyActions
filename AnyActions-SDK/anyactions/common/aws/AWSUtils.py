import boto3

session = boto3.Session()

def get_s3_client():
    return boto3.client('s3')