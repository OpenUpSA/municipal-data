from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.core.files import File

from ..models import MunicipalityStaffContactsUpload, MunicipalityStaffContacts
from ..update import update_municipal_staff_contacts


class UpdateMunicipalContactsTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sample", email="sample@some.co", password="testpass",
        )
        self.initial_upload = MunicipalityStaffContactsUpload.objects.create(
            user=self.user,
            file=File(
                open(
                    'municipal_finance/fixtures/municipal_contacts/initial.csv',
                    'rb',
                ),
            ),
        )
        self.update_upload = MunicipalityStaffContactsUpload.objects.create(
            user=self.user,
            file=File(
                open(
                    'municipal_finance/fixtures/municipal_contacts/update.csv',
                    'rb',
                ),
            ),
        )

    def test_initial_and_update(self):
        # Upload the initial data
        result = update_municipal_staff_contacts(self.initial_upload)
        records = MunicipalityStaffContacts.objects.all()
        self.assertEquals(result, {"updated": 0, "created": 4})
        self.assertQuerysetEqual(records, [repr(o) for o in [
            MunicipalityStaffContacts(
                id=1,
                demarcation_code="AAA",
                role="Role A",
                title="Ms",
                name="First Name",
                office_number="012 123 1111",
                fax_number="081 123 1111",
                email_address="one@some.co",
            ),
            MunicipalityStaffContacts(
                id=2,
                demarcation_code="AAA",
                role="Role B",
                title="Mr",
                name="Second Name",
                office_number="012 123 2222",
                fax_number="081 123 2222",
                email_address="two@some.co",
            ),
            MunicipalityStaffContacts(
                id=3,
                demarcation_code="BBB",
                role="Role A",
                title="Dr",
                name="Third Name",
                office_number="012 123 3333",
                fax_number="081 123 3333",
                email_address="three@some.co",
            ),
            MunicipalityStaffContacts(
                id=4,
                demarcation_code="BBB",
                role="Role B",
                title="Mrs",
                name="Fourth Name",
                office_number="012 123 4444",
                fax_number="081 123 4444",
                email_address="four@some.co",
            ),
        ]], ordered=False)
        # Upload an update
        result = update_municipal_staff_contacts(self.update_upload)
        records = MunicipalityStaffContacts.objects.all()
        self.assertEquals(result, {"updated": 2, "created": 1})
        self.assertQuerysetEqual(records, [repr(o) for o in [
            MunicipalityStaffContacts(
                id=1,
                demarcation_code="AAA",
                role="Role A",
                title="Mr",
                name="New First Name",
                office_number="012 321 1111",
                fax_number="081 321 1111",
                email_address="one@updated.co",
            ),
            MunicipalityStaffContacts(
                id=2,
                demarcation_code="AAA",
                role="Role B",
                title="Mr",
                name="Second Name",
                office_number="012 123 2222",
                fax_number="081 123 2222",
                email_address="two@some.co",
            ),
            MunicipalityStaffContacts(
                id=3,
                demarcation_code="BBB",
                role="Role A",
                title="Dr",
                name="Third Name",
                office_number="012 123 3333",
                fax_number="081 123 3333",
                email_address="three@some.co",
            ),
            MunicipalityStaffContacts(
                id=4,
                demarcation_code="BBB",
                role="Role B",
                title="Mr",
                name="Fourth Name Updated",
                office_number="012 321 4444",
                fax_number="081 321 4444",
                email_address="four@updated.co",
            ),
            MunicipalityStaffContacts(
                id=5,
                demarcation_code="CCC",
                role="Role A",
                title="Mr",
                name="Five Name",
                office_number="012 123 5555",
                fax_number="081 123 5555",
                email_address="five@some.co",
            ),
        ]], ordered=False)
