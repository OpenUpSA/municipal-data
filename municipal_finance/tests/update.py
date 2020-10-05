from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files import File

from ..models import MunicipalityStaffContactsUpload, MunicipalityStaffContacts
from ..update import update_municipal_staff_contacts


class UpdateMunicipalContactsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.upload = MunicipalityStaffContactsUpload.objects.create(
            user=self.user,
            file=File(
                open(
                    'municipal_finance/fixtures/municipal_contacts.csv',
                    'rb',
                ),
            ),
        )

    def test_upload_processes_correctly(self):
        update_municipal_staff_contacts(self.upload)
        records = MunicipalityStaffContacts.objects.all()
        self.assertQuerysetEqual(records, [
            MunicipalityStaffContacts(
                demarcation_code="AAA",
                role="Role A",
                title="Ms",
                name="First Name",
                office_number="012 123 1111",
                fax_number="081 123 1111",
                email_address="one@some.co",
            ),
            MunicipalityStaffContacts(
                demarcation_code="AAA",
                role="Role B",
                title="Mr",
                name="Second Name",
                office_number="012 123 2222",
                fax_number="081 123 2222",
                email_address="two@some.co",
            ),
            MunicipalityStaffContacts(
                demarcation_code="BBB",
                role="Role A",
                title="Dr",
                name="Third Name",
                office_number="012 123 3333",
                fax_number="081 123 3333",
                email_address="three@some.co",
            ),
            MunicipalityStaffContacts(
                demarcation_code="BBB",
                role="Role B",
                title="Mrs",
                name="Fourth Name",
                office_number="012 123 4444",
                fax_number="081 123 4444",
                email_address="four@some.co",
            ),
        ], transform=lambda x: x, ordered=False)
