from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User

from ...update import (
    update_cash_flow_v2,
)
from ...utils import import_data
from ...models import (
    CflowFactsV2,
    CashFlowV2Update,
)

from ..resources import CashFlowFactsV2Resource


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/cash_flow_v2"


class UpdateCashFlowV2(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            CashFlowFactsV2Resource,
            f"{FIXTURES_PATH}/cash_flow_facts_v2.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = CashFlowV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = CashFlowV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_without_updates(self):
        self.assertEqual(CflowFactsV2.objects.all().count(), 19)
        update_cash_flow_v2(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(CflowFactsV2.objects.all().count(), 24)
        self.assertEqual(self.insert_obj.deleted, 0)
        self.assertEqual(self.insert_obj.inserted, 5)

    def test_with_updates(self):
        self.assertEqual(CflowFactsV2.objects.all().count(), 19)
        update_cash_flow_v2(
            self.update_obj,
            batch_size=4,
        )
        self.assertEqual(CflowFactsV2.objects.all().count(), 24)
        self.assertEqual(self.update_obj.deleted, 5)
        self.assertEqual(self.update_obj.inserted, 10)
