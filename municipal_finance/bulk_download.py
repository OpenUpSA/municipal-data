import csv
import StringIO
import xlsxwriter

from django.core.files.storage import default_storage
from django.db import transaction

from municipal_finance.models.bulk_download import BulkDownload
from municipal_finance.storage import upload_object

import logging
logger = logging.Logger(__name__)


@transaction.atomic
def generate_download(**kwargs):
    # Pull data from relevent cube
    logger.warn(f"_______{kwargs['cube']}_____")
    #items = kwargs["cube"].objects.all()

    # Add data to a file object and upload to S3
    with default_storage.open('dev.xlsx', 'w') as f:
        f.write('dev')

    # Store file name and URL
    # https://munimoney-bulk-downloads.s3.eu-west-1.amazonaws.com/dev.json
    # BulkDownload.objects.create(
    #    file_url=url,
    # )
