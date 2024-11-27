import boto3
from anyactions.common.exception.anyactions_exceptions import AWSInternalException

# Not used for now, might get removed

session = boto3.Session()
s3 = session.client('s3')