import boto3, botocore
from botocore.config import Config
import json
import environ
env = environ.Env()
environ.Env.read_env()

aws = boto3.session.Session()

s3_client = aws.client("s3",
    endpoint_url=f'https://s3.eu-west-2.amazonaws.com',) # why is this necessary to get a key that works?
sns_client = aws.client("sns")

def get_presigned_key(object):
  BUCKET = 'jim-bulk-data-upload'
  url = s3_client.generate_presigned_url(
      'get_object',
      Params={'Bucket': env("JIM_S3_BUCKET"), 'Key': object},
      #ExpiresIn=300
      )
  return(url)

def send_sns_message(consignment_reference, presigned_url):
  message = {
    "consignment-reference": consignment_reference,
    "s3-folder-url": presigned_url,
    "consignment-type": "judgment",
    "number-of-retries": 0
  }
  print(env("JIM_SNS_TOPIC"))
  return sns_client.publish(
    TopicArn=env("JIM_SNS_TOPIC"),
    Message=json.dumps(message),
  )

# print(get_presigned_key("sample.txt"))
print(send_sns_message("TRE-1111-ABC1", get_presigned_key("TRE-1111-ABC1.tar.gz")))

# https://jim-bulk-data-upload.s3.eu-west-2.amazonaws.com/sample.txt
