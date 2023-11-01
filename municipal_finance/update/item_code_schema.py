from django.core.files.storage import default_storage
import xlrd


schema_codes = {
    "finpos": "A6",
    "capital": "SA34A",
    "cashflow": "A7",
    "incexp": "A4",
}


def update_item_code_schema(update_obj, batch_size, **kwargs):
    print("__________")
    print("Update all item codes")

    file = default_storage.open(update_obj.file.name, "rb")
    workbook = xlrd.open_workbook(file_contents=file.read())
    sheet = workbook.sheet_by_index(0)

    for i in range(sheet.nrows):
        for j in range(sheet.ncols):
            print(sheet.cell_value(i, j))

    # For each model of item code update add codes with the corresponding schema version
    # It should also be possible to update item codes of a matching schema version
