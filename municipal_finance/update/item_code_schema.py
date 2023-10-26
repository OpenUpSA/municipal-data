from .utils import (
    Updater,
)


class ItemCodeSchemaUpdater(Updater):
    print("Update all item codes")


def update_item_code_schema(update_obj, batch_size, **kwargs):
    updater = ItemCodeSchemaUpdater(update_obj, batch_size)
    updater.update()
