from django.test import TransactionTestCase
from django.core.files import File

from ..update import update_item_code_schema
from ..models import ItemCodeSchema, CflowItemsV2


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/"


class UpdateItemSchema(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        self.insert_obj = ItemCodeSchema.objects.create(
            version=1,
            file=File(open(f"{FIXTURES_PATH}/item_schema.xlsx", "rb")),
        )

    def test_new_schema_version(self):
        schema = ItemCodeSchema.objects.get(version=1)
        self.assertEqual(schema.version, "1")

    def test_schema_codes(self):
        items = CflowItemsV2.objects.all()
        self.assertEqual(items.count(), 32)

        update_item_code_schema(
            self.insert_obj,
            batch_size=4,
        )
        uploaded_items = CflowItemsV2.objects.all()
        # Expecting 1 more items
        self.assertEqual(uploaded_items.count(), 33)

        item_code = CflowItemsV2.objects.get(code="1234")
        self.assertEqual(item_code.code, "1234")
