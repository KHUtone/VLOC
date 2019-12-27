import boto3
import botocore

__aws_access_key_id__ = 'YOUR_ACCESS_KEY_ID'
__aws_secret_access_key__ = 'YOUR_SECRET_ACCESS_KEY'


s3 = boto3.client(
    's3',
    aws_access_key_id = __aws_access_key_id__,
    aws_secret_access_key = __aws_secret_access_key__)

filename = 'FILE_NAME' #업로드 파일이름
bucket_name = 'BUCKET_NAME' #버킷이름

s3.download_file(bucket_name, filename, 'YOUR_DIRECTORY'+filename)

# s3.upload_file(filepath, bucket_name, upload_file_name(클라우드에서 저장될 이름)))
# s3.upload_file('C:\\Users\\starc\\Desktop\\khuthon\\download\\'+filename, bucket_name, 'upload_'+filename)