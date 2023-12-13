from django.core.files.storage import default_storage
import xlrd3 as xlrd

from municipal_finance.models import (
    FinancialPositionItemsV2,
    CapitalItemsV2,
    CflowItemsV2,
    IncexpItemsV2,
)

schema_codes = {
    "A6": FinancialPositionItemsV2,
    "SA34A": CapitalItemsV2,
    "A7": CflowItemsV2,
    "A4": IncexpItemsV2,
}

schema_codes_tmp = {
    "A6": "finpos",
}


def update_item_code_schema(update_obj, batch_size, **kwargs):
    file = default_storage.open(update_obj.file.name, "rb")
    workbook = xlrd.open_workbook(file_contents=file.read())
    sheet = workbook.sheet_by_index(0)

    for i in range(sheet.nrows):
        schema_code = sheet.row_values(i)[0].strip()
        if schema_code != "" and schema_code in schema_codes:
            label = sheet.row_values(i)[4].strip()
            code = sheet.row_values(i)[1].strip()

            schema_codes[schema_code].objects.create(
                code=code, label=label, version=update_obj
            )
