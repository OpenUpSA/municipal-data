from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.core.files import File

from ...utils import import_data
from ...models import (
    MunicipalStaffContactsUpdate,
    MunicipalStaffContacts,
)
from ...update import (
    update_municipal_staff_contacts,
)

from ..resources import MunicipalStaffContactsResource


FIXTURES_PATH = ("municipal_finance/fixtures/tests/update/"
                 "municipal_staff_contacts")


class UpdateMunicipalContactsTestCase(TransactionTestCase):
    serialized_rollback = True

    def setUp(self):
        import_data(
            MunicipalStaffContactsResource,
            f"{FIXTURES_PATH}/municipal_staff_contacts.csv",
        )
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.insert_obj = MunicipalStaffContactsUpdate.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/insert.csv", "rb")),
        )
        self.update_obj = MunicipalStaffContactsUpdate.objects.create(
            user=self.user,
            file=File(open(f"{FIXTURES_PATH}/update.csv", "rb")),
        )

    def test_insert(self):
        self.assertEqual(MunicipalStaffContacts.objects.all().count(), 9)
        update_municipal_staff_contacts(
            self.insert_obj,
            batch_size=4,
        )
        self.assertEqual(MunicipalStaffContacts.objects.all().count(), 14)
        self.assertEqual(self.insert_obj.deleted, 0)
        self.assertEqual(self.insert_obj.inserted, 5)

    def test_update(self):
        self.assertEqual(MunicipalStaffContacts.objects.all().count(), 9)
        update_municipal_staff_contacts(
            self.update_obj,
            batch_size=4,
        )
        self.assertEqual(MunicipalStaffContacts.objects.all().count(), 14)
        self.assertEqual(self.update_obj.deleted, 3)
        self.assertEqual(self.update_obj.inserted, 8)
