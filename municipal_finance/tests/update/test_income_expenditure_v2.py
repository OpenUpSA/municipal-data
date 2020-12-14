from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User

from ...update import (
    update_income_expenditure_v2,
)
from ...utils import import_data
from ...models import (
    IncexpFactsV2,
    IncomeExpenditureV2Update,
)

from ..resources import IncexpFactsV2Resource


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/income_expenditure_v2"


class UpdateIncomeExpenditureV2(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            IncexpFactsV2Resource,
            f"{FIXTURES_PATH}/income_expenditure_facts_v2.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = IncomeExpenditureV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = IncomeExpenditureV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_without_updates(self):
        self.assertEqual(IncexpFactsV2.objects.all().count(), 24)
        update_income_expenditure_v2(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(IncexpFactsV2.objects.all().count(), 30)
        self.assertEqual(self.insert_obj.deleted, 0)
        self.assertEqual(self.insert_obj.inserted, 6)

    def test_with_updates(self):
        self.assertEqual(IncexpFactsV2.objects.all().count(), 24)
        update_income_expenditure_v2(
            self.update_obj,
            batch_size=4,
        )
        self.assertEqual(IncexpFactsV2.objects.all().count(), 30)
        self.assertEqual(self.update_obj.deleted, 6)
        self.assertEqual(self.update_obj.inserted, 12)
