import csv
from io import StringIO

from django.db import transaction

from municipal_finance.models.bulk_download import BulkDownload
from municipal_finance.storage import upload_object

import logging
logger = logging.Logger(__name__)


@transaction.atomic
def generate_download():
    # Pull data

    # Upload file to bucket
    file_to_save = StringIO()
    csv.writer(file_to_save).writerows("file_data")
    file_to_save = bytes(file_to_save.getvalue(), encoding="utf-8")
    dev = upload_object(file_to_save, "dev.json", "munimoney-bulk-downloads")
    url = "asdf-timestamp.json"

    logger.warn(f"_______{dev}_____")
    # Store file URL
    BulkDownload.objects.create(
        file_url=url,
    )
