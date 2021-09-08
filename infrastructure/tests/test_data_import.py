from django.test import TestCase, Client, override_settings, TransactionTestCase
from django.conf import settings
from django.urls import reverse
from io import BytesIO
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django_q.models import OrmQ
from django_q.tasks import AsyncTask, fetch, result
import time
import rest_framework.response

from infrastructure.models import FinancialYear, QuarterlySpendFile, AnnualSpendFile, Expenditure, Project
from infrastructure.tests import utils
from infrastructure.utils import load_excel
from scorecard.models import Geography


@override_settings(Q_CLUSTER={**settings.Q_CLUSTER, 'sync': True, 'poll': 2, 'max_attempts': 3})
class FileTest(TransactionTestCase):

    def setUp(self):
        fixtures = ["seeddata.json"]
        self.client = Client()
        self.username = 'admin'
        self.email = 'test@whatever.com'
        self.password = 'password'
        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        FileTest.geography = Geography.objects.create(
            geo_level="municipality",
            geo_code="BUF",
            province_name="Eastern Cape",
            province_code="EC",
            category="A",
        )

    def test_file_upload(self):
        """Scope of Test: Testing the file upload in Django Admin to processing file and add to Django_Q"""
        self.client.login(username=self.username, password=self.password)
        fy = FinancialYear.objects.create(budget_year="2019/2020", active=1)

        self.assertEquals(FinancialYear.objects.all().count(), 1)
        self.assertEquals(AnnualSpendFile.objects.all().count(), 0)

        # the app name, the name of the model and the name of the view
        url = reverse('admin:infrastructure_annualspendfile_add')

        with open('infrastructure/tests/test_files/test.xlsx', 'rb', ) as f:
            resp = self.client.post(url, {'financial_year': fy.pk, 'document': f}, follow=True)
        self.assertContains(resp, "Dataset is currently being processed.", status_code=200)

        file = AnnualSpendFile.objects.all().values("id")

        a = AsyncTask('infrastructure.upload.process_document', file[0]['id'], sync=True)
        a.run()

        fileSpend = AnnualSpendFile.objects.all().values("status")
        filestatus = fileSpend[0]['status']

        self.assertEquals(AnnualSpendFile.objects.all().count(), 1)
        self.assertEquals(filestatus, 1)
        self.assertEquals(Project.objects.count(), 27)

        response = self.client.get("/api/v1/infrastructure/search/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PC002003005_00002')


    def test_file_upload_fail(self):
        """Scope of Test: Testing if the file upload fail in Django Admin to processing file and add to Django_Q"""
        self.client.login(username=self.username, password=self.password)
        fy = FinancialYear.objects.create(budget_year="2019/2020", active=1)

        self.assertEquals(FinancialYear.objects.all().count(), 1)
        self.assertEquals(AnnualSpendFile.objects.all().count(), 0)

        # the app name, the name of the model and the name of the view
        url = reverse('admin:infrastructure_annualspendfile_add')
        with open('infrastructure/tests/test_files/failtest.xlsx', 'rb', ) as f:
            resp = self.client.post(url, {'financial_year': fy.pk, 'document': f}, follow=True)
        self.assertContains(resp, "Dataset is currently being processed.", status_code=200)
        file = AnnualSpendFile.objects.all().values("id")

        a = AsyncTask('infrastructure.upload.process_document', file[0]['id'], sync=True)
        with self.assertRaises(ValueError):
            a.run()
            raise ValueError()

        self.assertEquals(AnnualSpendFile.objects.all().count(), 1)
        file = AnnualSpendFile.objects.all().values("status")

        self.assertEquals(file[0]['status'], 2)


    def test_year_error(self):
        """Scope of Test: Test if a file uploaded in Django Admin with incorrect year selection and content returns an error to Django_Q"""
        self.client.login(username=self.username, password=self.password)
        fy = FinancialYear.objects.create(budget_year="2019/2020", active=1)

        self.assertEquals(FinancialYear.objects.all().count(), 1)
        self.assertEquals(AnnualSpendFile.objects.all().count(), 0)

        url = reverse('admin:infrastructure_annualspendfile_add')
        with open('infrastructure/tests/test_files/failyear.xlsx', 'rb', ) as f:
            resp = self.client.post(url, {'financial_year': fy.pk, 'document': f}, follow=True)
        self.assertContains(resp, "Dataset is currently being processed.", status_code=200)
        file = AnnualSpendFile.objects.all().values("id")

        a = AsyncTask('infrastructure.upload.process_document', file[0]['id'], sync=True)
        with self.assertRaises(ValueError):
            a.run()
            raise ValueError()

        self.assertEquals(AnnualSpendFile.objects.all().count(), 1)
        file = AnnualSpendFile.objects.all().values("status")

        self.assertEquals(file[0]['status'], 2)
