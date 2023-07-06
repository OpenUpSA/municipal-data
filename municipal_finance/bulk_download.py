import xlsxwriter

from django.core.files.storage import default_storage
from django.db import transaction

from municipal_finance.models.bulk_download import BulkDownload

import logging

logger = logging.Logger(__name__)


@transaction.atomic
def generate_download(**kwargs):
    # Pull data from relevent cube
    export_to_excel(kwargs["cube_model"])

    # Store file name and URL
    # https://munimoney-bulk-downloads.s3.eu-west-1.amazonaws.com/dev.json
    # BulkDownload.objects.create(
    #    file_url=url,
    # )


def export_to_excel(cube_model):
    queryset = cube_model.objects.all()
    excel_file = "my_model_data.xlsx"
    workbook = xlsxwriter.Workbook(excel_file, {"constant_memory": True})
    worksheet = workbook.add_worksheet()

    # Generalise header for different cube columns
    headers = [field.verbose_name.title() for field in cube_model._meta.get_fields()]
    # logger.warn(f"_______{headers}_____")
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
    workbook.close()

    file = default_storage.open("bulk_downloads", "wb")
    workbook.save(file)
    file.close()
