from django.core.files.storage import default_storage
import xlrd


schema_codes = {
    "A6": "finpos",
    "SA34A": "capital",
    "A7": "cashflow",
    "A4": "incexp",
}

def update_item_code_schema(update_obj, batch_size, **kwargs):
    print("__________")
    print("Update all item codes")
    print(update_obj.id)

    file = default_storage.open(update_obj.file.name, "rb")
    workbook = xlrd.open_workbook(file_contents=file.read())
    sheet = workbook.sheet_by_index(0)

    for i in range(sheet.nrows):
        if sheet.row_values(i)[0].strip() != "":
            print(sheet.row_values(i))

    # For each model of item code update add codes with the corresponding schema version
    # It should also be possible to update item codes of a matching schema version
