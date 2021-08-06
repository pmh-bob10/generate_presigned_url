import uuid
import boto3
import requests
from botocore.config import Config

profile_name = 'bob10'
region = 'ap-northeast-1'
location = {'LocationConstraint': region}

bucket_name = 'bob10-6082-test'
# bucket_name = 'bobhw'
file_name = 'HW3-6082'
file_content = 'bob10-6082-{}'.format(uuid.uuid1())

session = boto3.Session(profile_name=profile_name)
s3 = session.client('s3', region_name=region)
s3_resource = session.resource('s3', region_name=region)

s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
print('bucket_created={}'.format(bucket_name))

file = open(file_name, 'w')
file.write(file_content)
file.close()

s3.upload_file(file_name, bucket_name, file_name)
presigned_url = s3.generate_presigned_url('get_object', ExpiresIn=3600, Params={
  'Bucket': bucket_name,
  'Key': file_name,
})
print('presigned_url={}'.format(presigned_url))

ctx = requests.get(presigned_url)
print('downloaded_file_body={}'.format(ctx.text))

s3_bucket = s3_resource.Bucket(bucket_name)
s3_bucket.object_versions.delete()
print('bucket_emptied')

s3.delete_bucket(Bucket=bucket_name)
print('bucket_deleted')
