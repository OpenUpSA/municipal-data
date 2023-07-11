import xlsxwriter
import sys
import hashlib
from datetime import datetime

from django.core.files.storage import default_storage
from django.db import transaction

from municipal_finance.models.bulk_download import BulkDownload

import logging

logger = logging.Logger(__name__)


@transaction.atomic
def generate_download(**kwargs):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Pull data from relevent cube
    file = dump_cube_to_excel(kwargs["cube_model"], timestamp)

    # Store file name and URL
    BulkDownload.objects.create(
        file_name=file["slug"],
    )

    # Draw metadata for this dump
    metadata = {
        "last updated": timestamp,
    }
    metadata.update(file)
    file = default_storage.open("index.json", "wb")
    file.write(metadata)
    file.close()

    # Aggregate all metadata


def dump_cube_to_excel(cube_model, timestamp):
    queryset = cube_model.objects.all()

    file_name = f"{cube_model._meta.db_table}_{timestamp}.xlsx"
    file = default_storage.open(file_name, "wb")
    workbook = xlsxwriter.Workbook(file, {"constant_memory": True})
    worksheet = workbook.add_worksheet()

    # Generalise header for different cube columns
    headers = [field.verbose_name.title() for field in cube_model._meta.get_fields()]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    row = 1
    for item in queryset:
        col = 0
        for field in cube_model._meta.get_fields():
            # Handle related fields
            if field.concrete:
                if field.is_relation:
                    if field.many_to_many or field.one_to_many:
                        value = ", ".join(
                            str(obj) for obj in getattr(item, field.name).all()
                        )
                else:
                    value = getattr(item, field.name)
                worksheet.write(row, col, value)
                col += 1
        row += 1

    workbook.close()
    file.close()

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with default_storage.open(file_name, "rb") as f:
        data = f.read()
        md5.update(data)
        sha1.update(data)
        size = sys.getsizeof(data)

    return {
        "slug": file_name,
        "sha1": sha1.hexdigest(),
        "md5": md5.hexdigest(),
        "file size": size,
    }
