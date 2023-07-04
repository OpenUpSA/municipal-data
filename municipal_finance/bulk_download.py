import xlsxwriter

from django.core.files.storage import default_storage
from django.db import transaction

from municipal_finance.models.bulk_download import BulkDownload

import logging
logger = logging.Logger(__name__)


@transaction.atomic
def generate_download(**kwargs):
    # Pull data from relevent cube
    logger.warn(f"_______{kwargs['cube_model']}_____")
    #items = kwargs["cube"].objects.all()
    export_to_excel(kwargs['cube_model'])
    # Add data to a file object and upload to S3
    with default_storage.open('dev.xlsx', 'w') as f:
        f.write('dev')

    # Store file name and URL
    # https://munimoney-bulk-downloads.s3.eu-west-1.amazonaws.com/dev.json
    # BulkDownload.objects.create(
    #    file_url=url,
    # )

def export_to_excel(cube_model):
    queryset = cube_model.objects.all()
    excel_file = 'my_model_data.xlsx'
    workbook = xlsxwriter.Workbook(excel_file)
    worksheet = workbook.add_worksheet()

    headers = ['Column 1', 'Column 2', 'Column 3']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    row = 1
    for item in queryset:
        logger.warn(f"_______{item.objects}_____")
        worksheet.write(row, 0, item.id)
        row += 1

    workbook.close()