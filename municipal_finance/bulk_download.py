import xlsxwriter
from datetime import datetime

from django.core.files.storage import default_storage
from django.db import transaction

from municipal_finance.models.bulk_download import BulkDownload

import logging

logger = logging.Logger(__name__)


@transaction.atomic
def generate_download(**kwargs):
    # Pull data from relevent cube
    file_name = export_to_excel(kwargs["cube_model"])

    # Store file name and URL
    # file_name = aged_creditor_facts_v2_2023-07-07_23-49-37.xlsx
    # s3_url = "https://munimoney-media.s3.eu-west-1.amazonaws.com/bulk_data/"
    BulkDownload.objects.create(
        file_name=file_name",
    )


def export_to_excel(cube_model):
    queryset = cube_model.objects.all()
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    excel_file = f"{cube_model._meta.db_table}_{timestamp}.xlsx"
    workbook = xlsxwriter.Workbook(excel_file, {"constant_memory": True})
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
                    value = str(getattr(item, field.name))
                    if field.many_to_many or field.one_to_many:
                        value = ", ".join(
                            str(obj) for obj in getattr(item, field.name).all()
                        )
                else:
                    value = getattr(item, field.name)
                worksheet.write(row, col, value)
                col += 1
        row += 1
    file = default_storage.open(excel_file, 'wb')
    workbook = xlsxwriter.Workbook(file)
    workbook.close()
    file.close()

    return excel_file
