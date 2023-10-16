from storages.backends.s3boto3 import S3Boto3Storage
from municipal_finance import settings
import boto3
import tempfile


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    region_name = settings.AWS_REGION


def amazon_s3(file_name):
    """
    Get file from amazon and process
    """
    temp_file = tempfile.NamedTemporaryFile()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3.download_fileobj(
        settings.AWS_STORAGE_BUCKET_NAME, "media/" + file_name, temp_file
    )

    return temp_file
