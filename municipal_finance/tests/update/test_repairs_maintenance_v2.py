from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User

from ...update import (
    update_repairs_maintenance_v2,
)
from ...utils import import_data
from ...models import (
    RepairsMaintenanceFactsV2,
    RepairsMaintenanceV2Update,
)

from ..resources import RepairsMaintenanceFactsV2Resource


FIXTURES_PATH = ("municipal_finance/fixtures/tests/update/"
                 "repairs_maintenance_v2")


class UpdateCashFlowV2(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            RepairsMaintenanceFactsV2Resource,
            f"{FIXTURES_PATH}/repairs_maintenance_facts_v2.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = RepairsMaintenanceV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = RepairsMaintenanceV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_without_updates(self):
        self.assertEqual(RepairsMaintenanceFactsV2.objects.all().count(), 10)
        update_repairs_maintenance_v2(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(RepairsMaintenanceFactsV2.objects.all().count(), 13)
        self.assertEqual(self.insert_obj.deleted, 0)
        self.assertEqual(self.insert_obj.inserted, 3)

    def test_with_updates(self):
        self.assertEqual(RepairsMaintenanceFactsV2.objects.all().count(), 10)
        update_repairs_maintenance_v2(
            self.update_obj,
            batch_size=4,
        )
        self.assertEqual(RepairsMaintenanceFactsV2.objects.all().count(), 13)
        self.assertEqual(self.update_obj.deleted, 3)
        self.assertEqual(self.update_obj.inserted, 6)
