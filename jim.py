import boto3, botocore
from botocore.config import Config

aws = boto3.session.Session()

s3_client = aws.client("s3",
    endpoint_url=f'https://s3.eu-west-2.amazonaws.com',)

def get_presigned_key(object):
  BUCKET = 'jim-bulk-data-upload'
  url = s3_client.generate_presigned_url(
      'get_object',
      Params={'Bucket': BUCKET, 'Key': object},
      #ExpiresIn=300
      )
  return(url)

print(get_presigned_key("sample.txt"))
# https://jim-bulk-data-upload.s3.eu-west-2.amazonaws.com/sample.txt
