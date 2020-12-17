
from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User

from ...update import (
    update_grant_facts_v2,
)
from ...utils import import_data
from ...models import (
    GrantFactsV2,
    GrantFactsV2Update,
)

from ..resources import GrantFactsV2Resource


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/grant_facts_v2"


class UpdateAgedDebtorFactsV2(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            GrantFactsV2Resource,
            f"{FIXTURES_PATH}/grant_facts_v2.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = GrantFactsV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = GrantFactsV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_without_updates(self):
        self.assertEqual(GrantFactsV2.objects.all().count(), 27)
        update_grant_facts_v2(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(GrantFactsV2.objects.all().count(), 36)
        self.assertEqual(self.insert_obj.deleted, 0)
        self.assertEqual(self.insert_obj.inserted, 9)

    def test_with_updates(self):
        self.assertEqual(GrantFactsV2.objects.all().count(), 27)
        update_grant_facts_v2(
            self.update_obj,
            batch_size=4,
        )
        self.assertEqual(GrantFactsV2.objects.all().count(), 36)
        self.assertEqual(self.update_obj.deleted, 9)
        self.assertEqual(self.update_obj.inserted, 18)
