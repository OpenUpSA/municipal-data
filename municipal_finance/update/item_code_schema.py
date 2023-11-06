from django.core.files.storage import default_storage
import xlrd

from municipal_finance.models import (
    FinancialPositionItemsV2,
)

schema_codes = {
    "A6": "finpos",
    "SA34A": "capital",
    "A7": "cashflow",
    "A4": "incexp",
}

schema_codes_tmp = {
    "A6": "finpos",
}


def update_item_code_schema(update_obj, batch_size, **kwargs):
    print("__________")
    print("Update all item codes")
    print(update_obj.id)

    file = default_storage.open(update_obj.file.name, "rb")
    workbook = xlrd.open_workbook(file_contents=file.read())
    sheet = workbook.sheet_by_index(0)

    for i in range(sheet.nrows):
        schema_code = sheet.row_values(i)[0].strip()
        if schema_code != "" and schema_code in schema_codes_tmp:
            label = sheet.row_values(i)[4].strip()
            code = sheet.row_values(i)[1].strip()

            FinancialPositionItemsV2.objects.create(
                code=code, label=label, version=update_obj
            )
