
from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User

from ...update import (
    update_financial_position_facts_v2,
)
from ...utils import import_data
from ...models import (
    FinancialPositionFactsV2,
    FinancialPositionFactsV2Update,
)

from ..resources import FinancialPositionFactsV2Resource


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/financial_position_facts_v2"


class UpdateAgedDebtorFactsV2(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            FinancialPositionFactsV2Resource,
            f"{FIXTURES_PATH}/financial_position_facts_v2.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = FinancialPositionFactsV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = FinancialPositionFactsV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_without_updates(self):
        self.assertEqual(FinancialPositionFactsV2.objects.all().count(), 57)
        update_financial_position_facts_v2(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(FinancialPositionFactsV2.objects.all().count(), 77)
        self.assertEqual(self.insert_obj.deleted, 0)
        self.assertEqual(self.insert_obj.inserted, 20)

    def test_with_updates(self):
        self.assertEqual(FinancialPositionFactsV2.objects.all().count(), 57)
        update_financial_position_facts_v2(
            self.update_obj,
            batch_size=4,
        )
        self.assertEqual(FinancialPositionFactsV2.objects.all().count(), 77)
        self.assertEqual(self.update_obj.deleted, 20)
        self.assertEqual(self.update_obj.inserted, 40)
