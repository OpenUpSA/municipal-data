from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User
from datetime import datetime

from ..update import update_aged_creditor_facts_v2
from ..utils import import_data
from ..models import AgedCreditorFactsV2Update
from .resources import AgedCreditorFactsV2Resource
from ..cubes import get_manager
from ..views import get_cube_with_last_updated


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/aged_creditor_facts_v2"


class UpdateAgedCreditorFactsV2(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            AgedCreditorFactsV2Resource,
            f"{FIXTURES_PATH}/aged_creditor_facts_v2.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = AgedCreditorFactsV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = AgedCreditorFactsV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_aged_creditor_v2(self):
        update_aged_creditor_facts_v2(
            self.insert_obj,
            batch_size=4,
        )
        manager = get_manager()
        with manager.get_engine().connect() as connection:
            a = get_cube_with_last_updated(connection, manager, "aged_creditor_v2")

        self.assertEqual(datetime.strptime(a["last_updated"][0:10], "%Y-%m-%d"), datetime.today().strftime("%Y-%m-%d"))