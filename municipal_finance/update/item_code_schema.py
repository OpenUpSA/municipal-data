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


def update_item_code_schema(update_obj, batch_size, **kwargs):
    file = default_storage.open(update_obj.file.name, "rb")
    workbook = xlrd.open_workbook(file_contents=file.read())

    for item_key in schema_codes:
        if item_key in workbook.sheet_names():
            sheet = workbook.sheet_by_name(item_key)
            item_codes = {}

            for i in range(sheet.nrows):
                row = sheet.row_values(i)
                schema_code = row[0].strip()
                if schema_code != "" and schema_code in schema_codes:
                    desc = row[2].strip()
                    desc = desc.split(" / ")[-1].strip()
                    code = row[1].strip()
                    subcategory = None
                    if schema_code == "A4" and len(row) > 9 and row[9]:
                        parts = str(row[9]).strip().split(":")
                        if len(parts) >= 2:
                            subcategory = parts[1].strip()
                    item_codes[code] = (desc, subcategory)

            for key, (label, subcategory) in item_codes.items():
                defaults = {'label': label}
                if subcategory is not None:
                    defaults['subcategory'] = subcategory
                schema_codes[schema_code].objects.update_or_create(
                    code=key,
                    defaults=defaults
                )
