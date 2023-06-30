import os
from django.conf import settings
import boto3

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


def upload_object(file_object, name, bucket):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    response = s3.put_object(
        Body=file_object,
        Bucket=bucket,
        Key=f"{name}_object",
    )
    # response = s3.upload_file(name, bucket, f"{name}_object")
    return response
