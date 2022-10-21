import boto3
from botocore.config import Config
import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

session = boto3.Session(
    aws_access_key_id=env('AWS_ACCESS_KEY'),
    aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY'),
)

my_config = Config(
    region_name = 'eu-west-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)


s3_client = session.client('s3', config=my_config)

def get_presigned_key(object):
  BUCKET = 'jim-bulk-data-upload'
  url = s3_client.generate_presigned_url(
      'get_object',
      Params={'Bucket': BUCKET, 'Key': object},
      ExpiresIn=300)
  return(url)

print(get_presigned_key("sample.txt"))
# https://jim-bulk-data-upload.s3.eu-west-2.amazonaws.com/sample.txt
