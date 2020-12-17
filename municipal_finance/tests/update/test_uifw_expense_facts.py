
from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User

from ...update import (
    update_uifw_expense_facts,
)
from ...utils import import_data
from ...models import (
    UIFWExpenseFacts,
    UIFWExpenseFactsUpdate,
)

from ..resources import UIFWExpenseFactsResource


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/uifw_expense_facts"


class UpdateAgedDebtorFactsV2(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            UIFWExpenseFactsResource,
            f"{FIXTURES_PATH}/uifw_expense_facts.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = UIFWExpenseFactsUpdate.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = UIFWExpenseFactsUpdate.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_without_updates(self):
        self.assertEqual(UIFWExpenseFacts.objects.all().count(), 9)
        update_uifw_expense_facts(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(UIFWExpenseFacts.objects.all().count(), 12)
        self.assertEqual(self.insert_obj.deleted, 0)
        self.assertEqual(self.insert_obj.inserted, 3)

    def test_with_updates(self):
        self.assertEqual(UIFWExpenseFacts.objects.all().count(), 9)
        update_uifw_expense_facts(
            self.update_obj,
            batch_size=4,
        )
        self.assertEqual(UIFWExpenseFacts.objects.all().count(), 12)
        self.assertEqual(self.update_obj.deleted, 3)
        self.assertEqual(self.update_obj.inserted, 6)
