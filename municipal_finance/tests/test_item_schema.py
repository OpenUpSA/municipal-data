from django.test import TransactionTestCase
from django.core.files import File

from ..update import update_item_code_schema
from ..models import ItemCodeSchema, CflowItemsV2


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/"


class UpdateItemSchema(TransactionTestCase):
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
        self.assertEqual(items.count(), 0)

        update_item_code_schema(
            self.insert_obj,
            batch_size=4,
        )
        uploaded_items = CflowItemsV2.objects.all()
        self.assertEqual(uploaded_items.count(), 5)

        item_code = CflowItemsV2.objects.get(code="0110")
        self.assertEqual(item_code.code, "0110")
        self.assertEqual(item_code.version.version, "1")
