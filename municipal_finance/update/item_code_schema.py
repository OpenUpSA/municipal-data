schema_codes = {
    "finpos": "A6",
    "capital": "SA34A",
    "cashflow": "A7",
    "incexp": "A4",
}


def update_item_code_schema(update_obj, batch_size, **kwargs):
    print("__________")
    print("Update all item codes")
    # For each model of item code update add codes with the corresponding schema version
    # It should also be possible to update item codes of a matching schema version
