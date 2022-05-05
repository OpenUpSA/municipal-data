
from django.test import TransactionTestCase
from django.core.files import File
from django.contrib.auth.models import User

from ...update import (
    update_audit_opinion_facts,
)
from ...utils import import_data
from ...models import (
    AuditOpinionFacts,
    AuditOpinionFactsUpdate,
)

from ..resources import AuditOpinionFactsResource


FIXTURES_PATH = "municipal_finance/fixtures/tests/update/audit_opinion_facts"


class UpdateAuditOpinionFacts(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            AuditOpinionFactsResource,
            f"{FIXTURES_PATH}/audit_opinion_facts.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = AuditOpinionFactsUpdate.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = AuditOpinionFactsUpdate.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_without_updates(self):
        self.assertEqual(AuditOpinionFacts.objects.all().count(), 3)
        update_audit_opinion_facts(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(AuditOpinionFacts.objects.all().count(), 4)
        self.assertEqual(self.insert_obj.deleted, 0)
        self.assertEqual(self.insert_obj.inserted, 1)

    def test_with_updates(self):
        self.assertEqual(AuditOpinionFacts.objects.all().count(), 3)
        update_audit_opinion_facts(
            self.update_obj,
            batch_size=4,
        )
        self.assertEqual(AuditOpinionFacts.objects.all().count(), 4)
        self.assertEqual(self.update_obj.deleted, 1)
        self.assertEqual(self.update_obj.inserted, 2)

    def test_report_url(self):
        self.assertEqual(
            AuditOpinionFacts.objects.get(demarcation_code="CPT", financial_year="2018").report_url,
            "http://mfma.treasury.gov.za/Documents/07.%20Audit%20Reports/2017-18/01.%20Metros/CPT%20Cape%20Town/CPT%20Cape%20Town%20Audit%20Report%202017-18.pdf"
        )
        update_audit_opinion_facts(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(
            AuditOpinionFacts.objects.get(demarcation_code="CPT", financial_year="2019").report_url,
            ""
        )
