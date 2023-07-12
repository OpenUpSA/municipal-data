import xlsxwriter
import sys
import hashlib
from datetime import datetime

from django.core.files.storage import default_storage
from django.db import transaction

from municipal_finance.models.bulk_download import BulkDownload

import logging

logger = logging.Logger(__name__)

split_cubes = [
    "bsheet_facts",
    "financial_position_facts_v2",
    "aged_debtor_facts",
    "aged_debtor_facts_v2",
    "capital_facts",
    "capital_facts_v2",
    "cflow_facts",
    "cflow_facts_v2",
    "conditional_grant_facts",
    "grant_facts_v2",
    "incexp_facts",
    "incexp_facts_v2",
]


@transaction.atomic
def generate_download(**kwargs):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Pull data from relevent cube
    if kwargs["cube_model"]._meta.db_table in split_cubes:
        # file_name = split_dump_to_excel(kwargs["cube_model"], timestamp)
        file_name = dump_cube_to_excel(kwargs["cube_model"], timestamp)
    else:
        file_name = dump_cube_to_excel(kwargs["cube_model"], timestamp)

    # Store file names (URL slug)
    # BulkDownload.objects.create(
    #    file_name=file_name,
    # )

    # Draw metadata for this dump
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with default_storage.open(file_name, "rb") as f:
        data = f.read()
        md5.update(data)
        sha1.update(data)
        size = sys.getsizeof(data)

    metadata = {
        "last updated": timestamp,
        "slug": file_name,
        "sha1": sha1,
        "md5": md5,
        "file size": size,
    }

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
    return file_name


def split_dump_to_excel(cube_model, timestamp):
    queryset = cube_model.objects.all().order_by("financial_year")

    current_year = 0
    max_rows = 1000000
    worksheet_count = 1

    for item in queryset:
        col = 0

        if item.financial_year != current_year:
            try:
                workbook.close()
                file.close()
            except:
                pass

            row = 1
            current_year = item.financial_year
            file_name = f"{cube_model._meta.db_table}_{current_year}__{timestamp}.xlsx"
            file = default_storage.open(file_name, "wb")
            workbook = xlsxwriter.Workbook(file, {"constant_memory": True})
            worksheet = workbook.add_worksheet()

            # Generalise header for different cube columns
            headers = [
                field.verbose_name.title() for field in cube_model._meta.get_fields()
            ]
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)
        else:
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

        if row > max_rows:
            worksheet = workbook.add_worksheet()
            row = 0

    workbook.close()
    file.close()
    return file_name
