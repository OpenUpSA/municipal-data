from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User
from datetime import datetime, timedelta

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

    def test_aged_creditor_v1(self):
        manager = get_manager()
        with manager.get_engine().connect() as connection:
            cube = get_cube_with_last_updated(connection, manager, "aged_creditor")

        self.assertEqual(cube["last_updated"], "2020-10")

    def test_aged_creditor_v2(self):
        update_aged_creditor_facts_v2(
            self.insert_obj,
            batch_size=4,
        )
        manager = get_manager()
        with manager.get_engine().connect() as connection:
            cube = get_cube_with_last_updated(connection, manager, "aged_creditor_v2")
        current_time = datetime.today()-timedelta(hours=2)
        self.assertEqual(cube["last_updated"], current_time.strftime("%Y-%m-%d, %H:%M"))
