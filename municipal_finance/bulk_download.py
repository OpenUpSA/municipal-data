from django.db import transaction

from municipal_finance.models.bulk_downloads import BulkDownload


@transaction.atomic
def generate_download():
    # Pull data

    # Upload file to bucket
    url = "asdf-timestamp.json"

    # Store file URL
    BulkDownload.objects.create(
        file_url=url,
    )
