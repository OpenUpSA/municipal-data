from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User
from django.conf import settings

from ..utils import import_data
from ..models import AgedCreditorFactsV2Update, AgedCreditorFactsV2
from .resources import AgedCreditorFactsV2Resource
from django.core.files.storage import default_storage

from municipal_finance import bulk_download
from municipal_finance.views import get_bulk_downloads
import json

FIXTURES_PATH = "municipal_finance/fixtures/tests/update/aged_creditor_facts_v2"


class UpdateAgedCreditorFactsV2(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        self.aggregate_index = f"bulk_downloads_dev/index.json"
        self.cube_index = f"bulk_downloads_dev/aged_creditor_facts_v2/index.json"

        import_data(
            AgedCreditorFactsV2Resource,
            f"{FIXTURES_PATH}/aged_creditor_facts_v2.csv",
        )
        self.user = User.objects.create_user(
            username="sample",
            email="sample@some.co",
            password="testpass",
        )
        self.insert_obj = AgedCreditorFactsV2Update.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )

        bulk_download.generate_download(cube_model=AgedCreditorFactsV2)

    def test_metadata_is_created(self):
        with default_storage.open(self.cube_index, "r") as file:
            data = json.load(file)
        self.assertEqual(len(data["aged_creditor_facts_v2"]["files"]), 1)

        with default_storage.open(self.aggregate_index, "r") as file:
            data = json.load(file)
        self.assertEqual(len(data["aged_creditor_facts_v2"]["files"]), 1)

    def test_download_contents(self):
        with default_storage.open(self.cube_index, "r") as file:
            data = json.load(file)

        for file in data["aged_creditor_facts_v2"]["files"]["All"]:
            if file["format"] == "csv":
                file_name = file["file_name"]

        with default_storage.open(
            f"{settings.BULK_DOWNLOAD_DIR}/aged_creditor_facts_v2/{file_name}", "r"
        ) as file:
            data = file.read()

        file_lines = data.splitlines()
        self.assertEqual(
            file_lines[0],
            "id,demarcation_code,period_code,g1_amount,l1_amount,l120_amount,l150_amount,l180_amount,l30_amount,l60_amount,l90_amount,total_amount,financial_year,period_length,financial_period,item,amount_type",
        )
        self.assertEqual(
            file_lines[1],
            "1,CPT,2018AUDA,-1058474965,0,0,0,0,0,0,0,-1058474965,2018,year,2018,0100,AUDA",
        )

    def test_download_context(self):
        context = get_bulk_downloads()
        self.assertEqual(len(context["aged_creditor_facts_v2"]["files"]), 1)