from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django_q.models import OrmQ

from household.models import (
    HouseholdServiceTotal,
    HouseholdBillTotal,
    DataSetFile,
)

from household.upload import import_bill_data


class HouseholdsTestCase(TestCase):
    fixtures = ["geography", "budgetphase", "financialyear", "householdclass", "householdservice"]

    def setUp(self):
        self.client = Client()
        self.username = 'admin'
        self.email = 'test@whatever.com'
        self.password = 'password'
        self.user = User.objects.create_superuser(self.username, self.email, self.password)

    def test_bill_upload(self):
        self.client.login(username=self.username, password=self.password)
        self.assertEquals(HouseholdBillTotal.objects.all().count(), 0)
        self.assertEqual(OrmQ.objects.count(), 0)

        upload_url = reverse('admin:household_datasetfile_add')
        with open('household/tests/test_files/national_bill_totals.csv', 'rb', ) as f:
            resp = self.client.post(upload_url, {'csv_file': f, 'file_type': 'Bill'}, follow=True)

        self.assertContains(resp, "Dataset is currently being processed.", status_code=200)

        spend_file = DataSetFile.objects.first()
        self.assertEqual(OrmQ.objects.count(), 1)
        task = OrmQ.objects.first()
        task_file_id = task.task()["args"][0]
        task_method = task.func()

        self.assertEqual(task_method, 'household.upload.import_bill_data')
        self.assertEqual(task_file_id, spend_file.id)

        import_bill_data(task_file_id)

        self.assertEquals(DataSetFile.objects.count(), 1)
        spend_file = DataSetFile.objects.first()
        self.assertEquals(HouseholdBillTotal.objects.count(), 2)

    def test_service_upload(self):
        self.client.login(username=self.username, password=self.password)
        self.assertEquals(HouseholdServiceTotal.objects.all().count(), 0)
        self.assertEqual(OrmQ.objects.count(), 0)

        upload_url = reverse('admin:household_datasetfile_add')
        with open('household/tests/test_files/national_service_totals.csv', 'rb', ) as f:
            resp = self.client.post(upload_url, {'csv_file': f, 'file_type': 'Service'}, follow=True)

        self.assertContains(resp, "Dataset is currently being processed.", status_code=200)

        spend_file = DataSetFile.objects.first()
        self.assertEqual(OrmQ.objects.count(), 1)
        task = OrmQ.objects.first()
        task_file_id = task.task()["args"][0]
        task_method = task.func()

        self.assertEqual(task_method, 'household.upload.import_bill_data')
        self.assertEqual(task_file_id, spend_file.id)

        import_bill_data(task_file_id)

        self.assertEquals(DataSetFile.objects.count(), 1)
        spend_file = DataSetFile.objects.first()
        self.assertEquals(HouseholdServiceTotal.objects.count(), 2)

    def test_average_increase(self):
        pass
