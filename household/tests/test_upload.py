from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django_q.models import OrmQ
from django.db.models import Q

from household.models import (
    HouseholdServiceTotal,
    HouseholdBillTotal,
    DataSetFile,
    FinancialYear,
    BudgetPhase,
    HouseholdClass,
    HouseholdService,
)
from scorecard.models import Geography
from household.upload import import_bill_data


class HouseholdsTestCase(TestCase):
    fixtures = ["seeddata", "compiled_profile"]

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

    def test_query_response(self):
        geography = Geography.objects.get(geo_code="BUF")
        year_2021 = FinancialYear.objects.get(budget_year="2020/21")
        budget_phase = BudgetPhase.objects.get(name="Budget Year")
        class_middle = HouseholdClass.objects.get(name="Middle Income Range")
        class_affordable = HouseholdClass.objects.get(name="Affordable Range")
        class_indigent = HouseholdClass.objects.get(name="Indigent HH receiving FBS")
        household_service = HouseholdService.objects.get(name="Property rates")

        HouseholdBillTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_middle,
            percent=8.17,
            total=3567.89
        )
        HouseholdBillTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_middle,
            percent=7.37,
            total=3830.83
        )
        bill_summary = HouseholdBillTotal.summary.bill_totals(geography.geo_code)
        self.assertEqual(bill_summary.count(), 2)
        self.assertEqual(bill_summary[0]["financial_year__budget_year"], "2020/21")
        self.assertEqual(bill_summary[0]["household_class__name"], "Middle Income Range")
        self.assertEqual(float(bill_summary[0]["total"]), 3567.89)
        self.assertEqual(bill_summary[0]["percent"], 8.17)

        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_middle,
            service=household_service,
            total=2071
        )
        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_affordable,
            service=household_service,
            total=3102
        )
        HouseholdServiceTotal.objects.create(
            geography=geography,
            financial_year=year_2021,
            budget_phase=budget_phase,
            household_class=class_indigent,
            service=household_service,
            total=704
        )
        service_middle = (
            HouseholdServiceTotal.summary.active(geography.geo_code)
            .middle()
            .order_by("financial_year__budget_year")
        )
        service_affordable = (
            HouseholdServiceTotal.summary.active(geography.geo_code)
            .affordable()
            .order_by("financial_year__budget_year")
        )
        service_indigent = (
            HouseholdServiceTotal.summary.active(geography.geo_code)
            .indigent()
            .order_by("financial_year__budget_year")
        )
        self.assertEqual(service_middle.count(), 1)
        self.assertEqual(service_middle[0]["financial_year__budget_year"], "2020/21")
        self.assertEqual(service_middle[0]["total"], 2071.00)
        self.assertEqual(service_middle[0]["service__name"], "Property rates")
        self.assertEqual(service_middle[0]["household_class__name"], "Middle Income Range")
        self.assertEqual(service_affordable.count(), 1)
        self.assertEqual(service_affordable[0]["financial_year__budget_year"], "2020/21")
        self.assertEqual(service_affordable[0]["total"], 3102.00)
        self.assertEqual(service_affordable[0]["service__name"], "Property rates")
        self.assertEqual(service_affordable[0]["household_class__name"], "Affordable Range")
        self.assertEqual(service_indigent.count(), 1)
        self.assertEqual(service_indigent[0]["financial_year__budget_year"], "2020/21")
        self.assertEqual(service_indigent[0]["total"], 704.00)
        self.assertEqual(service_indigent[0]["service__name"], "Property rates")
        self.assertEqual(service_indigent[0]["household_class__name"], "Indigent HH receiving FBS")
