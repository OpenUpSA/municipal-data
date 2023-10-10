from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    region_name = "eu-west-1"
