from storages.backends.s3boto3 import S3Boto3Storage
import os
import boto3


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


def upload_file(file_name, bucket):
    s3_client = boto3.client("s3")
    response = s3_client.upload_file(file_name, bucket, f"{file_name}_object")
    return True
