from django.test import TestCase, Client, override_settings, TransactionTestCase
from django.conf import settings
from django.urls import reverse
from io import BytesIO
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django_q.models import OrmQ
import rest_framework.response
import xlrd

from infrastructure.models import FinancialYear, QuarterlySpendFile, AnnualSpendFile, Expenditure, Project, BudgetPhase, ProjectQuarterlySpend
from infrastructure.tests import utils
from infrastructure.utils import load_excel
from infrastructure.upload import process_annual_document, process_quarterly_document
from scorecard.models import Geography


def mock_project_row():
    """This is the project data that mock_existing_project_row will update"""
    mock_data = { 'Function': 'Administrative and Corporate Support',
        'Project Description': 'P-CNIN FURN & OFF EQUIP',
        'Project Number': 'PC002003005_00002',
        'Type': 'New',
        'MTSF Service Outcome': 'An efficient, effective and development-oriented public service',
        'IUDF': 'Growth',
        'Own Strategic Objectives': 'OWN MUNICIPAL STRATEGIC OBJECTIVE',
        'Asset Class': 'Furniture and Office Equipment',
        'Asset Sub-Class': '',
        'Ward Location': 'Administrative or Head Office',
        'GPS Longitude': '0', 'GPS Latitude': '0',
        'Audited Outcome 2017/18': 2000.0,
        'Full Year Forecast 2018/19': 3000.0,
        'Budget year 2019/20': 4000.0,
        'Budget year 2020/21': 5000.0,
        'Budget year 2021/22': 6000.0
    }
    yield mock_data

def mock_data_existing_project_row():
    """This should update the project from mock_project_row()"""
    mock_data = { 'Function': 'Administrative and Corporate Support',
        'Project Description': 'P-CNIN FURN & OFF EQUIP',
        'Project Number': 'PC002003005_00002',
        'Type': 'Renewal',
        'MTSF Service Outcome': 'A project update',
        'IUDF': 'Governance',
        'Own Strategic Objectives': 'TO BE CORRECTED',
        'Asset Class': 'Furniture and Office',
        'Asset Sub-Class': 'Equipment',
        'Ward Location': 'Head Office',
        'GPS Longitude': '1', 'GPS Latitude': '2',
        'Audited Outcome 2018/19': 2100.0,
        'Full Year Forecast 2019/20': 3100.0,
        'Budget year 2020/21': 4000.0,
        'Budget year 2021/22': 5000.0,
        'Budget year 2022/23': 6100.0
    }
    yield mock_data

def mock_new_project_row():
    """Composite key fields should not match mock_project_row() so that this creates a new project"""
    mock_data = { 'Function': 'Administrative and Corporate Support',
        'Project Description': 'P-CNIN FURN & OFF EQUIP - NEW DESCRIPTION',
        'Project Number': 'PC002003005_00002',
        'Type': 'Renewal',
        'MTSF Service Outcome': 'A project update',
        'IUDF': 'Governance',
        'Own Strategic Objectives': 'TO BE CORRECTED',
        'Asset Class': 'Furniture and Office',
        'Asset Sub-Class': 'Equipment',
        'Ward Location': 'Head Office',
        'GPS Longitude': '1', 'GPS Latitude': '2',
        'Audited Outcome 2018/19': 2100.0,
        'Full Year Forecast 2019/20': 3100.0,
        'Budget year 2020/21': 4000.0,
        'Budget year 2021/22': 5000.0,
        'Budget year 2022/23': 6100.0
    }
    yield mock_data

def mock_quarterly_row():
    """This is used to create a set of quarterly spends"""
    mock_data = { 'Function': 'Administrative and Corporate Support',
        'Project Description': 'P-CNIN FURN & OFF EQUIP',
        'Project Number': 'PC002003005_00002',
        'Type': 'New',
        'MTSF Service Outcome': 'An efficient, effective and development-oriented public service',
        'IUDF': 'Growth',
        'Own Strategic Objectives': 'OWN MUNICIPAL STRATEGIC OBJECTIVE',
        'Asset Class': 'Furniture and Office Equipment',
        'Asset Sub-Class': '',
        'Ward Location': 'Administrative or Head Office',
        'GPS Longitude': '0', 'GPS Latitude': '0',
        'Audited Outcome 2018/19': 1000.0,
        'Audited Outcome 2019/20': 2000.0,
        'Original Budget 2019/20': 3000.0,
        'Adjusted Budget 2019/20': 4000.0,
        'Q1 Sept Actual 2019/20': 5000.0,
        'Q2 Dec Actual 2019/20': 6000.0,
        'Q3 Mar Actual 2019/20': 7000.0,
        'Q4 June Actual 2019/20': 8000.0,
    }
    yield mock_data

def mock_quarterly_update_row():
    """This is used to create a set of quarterly spends"""
    mock_data = { 'Function': 'Administrative and Corporate Support',
        'Project Description': 'P-CNIN FURN & OFF EQUIP',
        'Project Number': 'PC002003005_00002',
        'Type': 'New',
        'MTSF Service Outcome': 'An efficient, effective and development-oriented public service',
        'IUDF': 'Growth',
        'Own Strategic Objectives': 'OWN MUNICIPAL STRATEGIC OBJECTIVE',
        'Asset Class': 'Furniture and Office Equipment',
        'Asset Sub-Class': '',
        'Ward Location': 'Administrative or Head Office',
        'GPS Longitude': '0', 'GPS Latitude': '0',
        'Audited Outcome 2019/20': 9000.0,
        'Audited Outcome 2020/21': 10000.0,
        'Original Budget 2020/21': 11000.0,
        'Adjusted Budget 2020/21': 12000.0,
        'Q1 Sept Actual 2020/21': 13000.0,
        'Q2 Dec Actual 2020/21': 14000.0,
        'Q3 Mar Actual 2020/21': 15000.0,
        'Q4 June Actual 2020/21': 16000.0,
    }
    yield mock_data


def verify_expenditure(this, amount, budget_phase, year):
    expenditure = Expenditure.objects.get(amount=amount)
    this.assertEquals(expenditure.budget_phase.name, budget_phase)
    this.assertEquals(expenditure.financial_year.budget_year, year)


class FileTest(TransactionTestCase):
    fixtures = ["seeddata"]

    def setUp(self):
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
        fy = FinancialYear.objects.create(budget_year="2019/2020")

        self.assertEquals(AnnualSpendFile.objects.all().count(), 0)
        self.assertEqual(OrmQ.objects.count(), 0)

        # the app name, the name of the model and the name of the view
        upload_url = reverse('admin:infrastructure_annualspendfile_add')

        with open('infrastructure/tests/test_files/test.xlsx', 'rb', ) as f:
            resp = self.client.post(upload_url, {'financial_year': fy.pk, 'document': f}, follow=True)
        self.assertContains(resp, "Dataset is currently being processed.", status_code=200)

        spend_file = AnnualSpendFile.objects.first()
        self.assertEquals(spend_file.status, AnnualSpendFile.PROGRESS)

        self.assertEqual(OrmQ.objects.count(), 1)
        task = OrmQ.objects.first()
        task_file_id = task.task()["args"][0]
        task_method = task.func()
        self.assertEqual(task_method, 'infrastructure.upload.process_annual_document')
        self.assertEqual(task_file_id, spend_file.id)
        # run the code
        process_annual_document(task_file_id)

        self.assertEquals(AnnualSpendFile.objects.count(), 1)
        spend_file = AnnualSpendFile.objects.first()
        self.assertEquals(spend_file.status, AnnualSpendFile.SUCCESS)
        self.assertEquals(Project.objects.count(), 2)

        response = self.client.get("/api/v1/infrastructure/search/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PC002003005_00002')


    def test_file_upload_fail(self):
        """Scope of Test: Testing if the file upload fail in Django Admin to processing file and add to Django_Q"""
        self.client.login(username=self.username, password=self.password)
        fy = FinancialYear.objects.create(budget_year="2019/2020")

        self.assertEquals(FinancialYear.objects.all().count(), 1)
        self.assertEquals(AnnualSpendFile.objects.all().count(), 0)

        url = reverse('admin:infrastructure_annualspendfile_add')
        with open('infrastructure/tests/test_files/failtest.xlsx', 'rb', ) as f:
            resp = self.client.post(url, {'financial_year': fy.pk, 'document': f}, follow=True)
        self.assertContains(resp, "Dataset is currently being processed.", status_code=200)

        spend_file = AnnualSpendFile.objects.first()
        self.assertEquals(spend_file.status, AnnualSpendFile.PROGRESS)

        self.assertEqual(OrmQ.objects.count(), 1)
        task = OrmQ.objects.first()
        task_file_id = task.task()["args"][0]
        task_method = task.func()
        self.assertEqual(task_method, 'infrastructure.upload.process_annual_document')
        self.assertEqual(task_file_id, spend_file.id)
        self.assertRaises(ValueError, process_annual_document, task_file_id)

        self.assertEquals(AnnualSpendFile.objects.all().count(), 1)
        spend_file = AnnualSpendFile.objects.first()
        self.assertEquals(spend_file.status, AnnualSpendFile.ERROR)


    def test_year_error(self):
        """Scope of Test: Test if a file uploaded in Django Admin with incorrect year selection and content returns an error to Django_Q"""
        self.client.login(username=self.username, password=self.password)
        fy = FinancialYear.objects.create(budget_year="2019/2020")

        self.assertEquals(FinancialYear.objects.all().count(), 1)
        self.assertEquals(AnnualSpendFile.objects.all().count(), 0)

        url = reverse('admin:infrastructure_annualspendfile_add')
        with open('infrastructure/tests/test_files/failyear.xlsx', 'rb', ) as f:
            resp = self.client.post(url, {'financial_year': fy.pk, 'document': f}, follow=True)
        self.assertContains(resp, "Dataset is currently being processed.", status_code=200)

        spend_file = AnnualSpendFile.objects.first()
        self.assertEquals(spend_file.status, AnnualSpendFile.PROGRESS)

        self.assertEqual(OrmQ.objects.count(), 1)
        task = OrmQ.objects.first()
        task_file_id = task.task()["args"][0]
        task_method = task.func()
        self.assertEqual(task_method, 'infrastructure.upload.process_annual_document')
        self.assertEqual(task_file_id, spend_file.id)
        self.assertRaises(ValueError, process_annual_document, task_file_id)

        self.assertEquals(AnnualSpendFile.objects.all().count(), 1)
        spend_file = AnnualSpendFile.objects.first()
        self.assertEquals(spend_file.status, AnnualSpendFile.ERROR)


    def test_upload_project(self):
        """Scope of Test: With no existing projects run an upload and check that the correct fields are populated"""
        self.assertEquals(BudgetPhase.objects.all().count(), 5)

        geography = Geography.objects.get(geo_code="BUF")

        fy = FinancialYear.objects.create(budget_year="2019/2020")
        utils.load_file(geography, mock_project_row(), fy)

        project = Project.objects.get(function="Administrative and Corporate Support")
        self.assertEquals(project.project_description, "P-CNIN FURN & OFF EQUIP")
        self.assertEquals(project.project_number, "PC002003005_00002")
        self.assertEquals(project.project_type, "New")
        self.assertEquals(project.mtsf_service_outcome, "An efficient, effective and development-oriented public service")
        self.assertEquals(project.iudf, "Growth")
        self.assertEquals(project.own_strategic_objectives, "OWN MUNICIPAL STRATEGIC OBJECTIVE")
        self.assertEquals(project.asset_class, "Furniture and Office Equipment")
        self.assertEquals(project.asset_subclass, "")
        self.assertEquals(project.ward_location, "Administrative or Head Office")
        self.assertEquals(project.longitude, 0.0)
        self.assertEquals(project.latitude, 0.0)

        self.assertEquals(Expenditure.objects.all().count(), 5)
        verify_expenditure(self, 2000.00, "Audited Outcome", "2017/2018")
        verify_expenditure(self, 3000.00, "Full Year Forecast", "2018/2019")
        verify_expenditure(self, 4000.00, "Budget year", "2019/2020")
        verify_expenditure(self, 5000.00, "Budget year", "2020/2021")
        verify_expenditure(self, 6000.00, "Budget year", "2021/2022")


    def test_update_project(self):
        """Scope of Test: With an existing project import a new project with the same composite key and check that non-key fields are updated"""

        geography = Geography.objects.get(geo_code="BUF")
        utils.load_file(geography, mock_project_row(), "2019/2020")

        project = Project.objects.get(project_description="P-CNIN FURN & OFF EQUIP")
        self.assertEquals(project.project_description, "P-CNIN FURN & OFF EQUIP")
        self.assertEquals(project.project_number, "PC002003005_00002")
        self.assertEquals(project.project_type, "New")
        self.assertEquals(project.mtsf_service_outcome, "An efficient, effective and development-oriented public service")
        self.assertEquals(project.iudf, "Growth")
        self.assertEquals(project.own_strategic_objectives, "OWN MUNICIPAL STRATEGIC OBJECTIVE")
        self.assertEquals(project.asset_class, "Furniture and Office Equipment")
        self.assertEquals(project.asset_subclass, "")
        self.assertEquals(project.ward_location, "Administrative or Head Office")
        self.assertEquals(project.longitude, 0.0)
        self.assertEquals(project.latitude, 0.0)

        utils.load_file(geography, mock_data_existing_project_row(), "2020/2021")
        self.assertEquals(Project.objects.all().count(), 1)

        project = Project.objects.get(project_description="P-CNIN FURN & OFF EQUIP")
        self.assertEquals(project.project_type, "Renewal")
        self.assertEquals(project.mtsf_service_outcome, "A project update")
        self.assertEquals(project.iudf, "Governance")
        self.assertEquals(project.own_strategic_objectives, "TO BE CORRECTED")
        self.assertEquals(project.asset_class, "Furniture and Office")
        self.assertEquals(project.asset_subclass, "Equipment")
        self.assertEquals(project.ward_location, "Head Office")
        self.assertEquals(project.longitude, 1.0)
        self.assertEquals(project.latitude, 2.0)

        self.assertEquals(Expenditure.objects.all().count(), 8)
        verify_expenditure(self, 2100.00, "Audited Outcome", "2018/2019")
        verify_expenditure(self, 3100.00, "Full Year Forecast", "2019/2020")
        verify_expenditure(self, 6100.00, "Budget year", "2022/2023")


    def test_new_project(self):
        """Scope of Test: With an existing project import a new project with a new composite key and check that a new  project is created"""

        geography = Geography.objects.get(geo_code="BUF")
        utils.load_file(geography, mock_project_row(), "2019/2020")

        project = Project.objects.get(project_description="P-CNIN FURN & OFF EQUIP")
        self.assertEquals(project.project_description, "P-CNIN FURN & OFF EQUIP")
        self.assertEquals(project.project_number, "PC002003005_00002")
        self.assertEquals(project.project_type, "New")
        self.assertEquals(project.mtsf_service_outcome, "An efficient, effective and development-oriented public service")
        self.assertEquals(project.iudf, "Growth")
        self.assertEquals(project.own_strategic_objectives, "OWN MUNICIPAL STRATEGIC OBJECTIVE")
        self.assertEquals(project.asset_class, "Furniture and Office Equipment")
        self.assertEquals(project.asset_subclass, "")
        self.assertEquals(project.ward_location, "Administrative or Head Office")
        self.assertEquals(project.longitude, 0.0)
        self.assertEquals(project.latitude, 0.0)

        utils.load_file(geography, mock_new_project_row(), "2020/2021")
        self.assertEquals(Project.objects.all().count(), 2)

        project = Project.objects.get(project_description="P-CNIN FURN & OFF EQUIP - NEW DESCRIPTION")
        self.assertEquals(project.project_type, "Renewal")
        self.assertEquals(project.mtsf_service_outcome, "A project update")
        self.assertEquals(project.iudf, "Governance")
        self.assertEquals(project.own_strategic_objectives, "TO BE CORRECTED")
        self.assertEquals(project.asset_class, "Furniture and Office")
        self.assertEquals(project.asset_subclass, "Equipment")
        self.assertEquals(project.ward_location, "Head Office")
        self.assertEquals(project.longitude, 1.0)
        self.assertEquals(project.latitude, 2.0)

        self.assertEquals(Expenditure.objects.all().count(), 10)

        expenditure_id = Expenditure.objects.get(amount=2100).project_id
        new_expenditures = Expenditure.objects.filter(project_id=expenditure_id)
        self.assertEquals(new_expenditures.count(), 5)

        verify_expenditure(self, 2100.00, "Audited Outcome", "2018/2019")
        verify_expenditure(self, 3100.00, "Full Year Forecast", "2019/2020")
        verify_expenditure(self, 6100.00, "Budget year", "2022/2023")


    def test_quarterly_upload(self):
        """Scope of Test: Check that a quarterly upload file will create quarterly spend data"""

        geography = Geography.objects.get(geo_code="BUF")
        utils.load_file(geography, mock_project_row(), "2019/2020")
        project = Project.objects.get(project_description="P-CNIN FURN & OFF EQUIP")

        self.client.login(username=self.username, password=self.password)
        upload_url = reverse('admin:infrastructure_quarterlyspendfile_add')

        fy = FinancialYear.objects.get(budget_year="2019/2020")

        with open('infrastructure/tests/test_files/quarterly.xlsx', 'rb', ) as f:
            resp = self.client.post(upload_url, {'financial_year': fy.pk, 'document': f}, follow=True)

        self.assertContains(resp, "Dataset is currently being processed.", status_code=200)

        spend_file = QuarterlySpendFile.objects.first()
        self.assertEquals(spend_file.status, QuarterlySpendFile.PROGRESS)

        self.assertEqual(OrmQ.objects.count(), 1)
        task = OrmQ.objects.first()
        task_file_id = task.task()["args"][0]
        task_method = task.func()
        self.assertEqual(task_method, 'infrastructure.upload.process_quarterly_document')
        self.assertEqual(task_file_id, spend_file.id)
        process_quarterly_document(task_file_id)

        self.assertEquals(QuarterlySpendFile.objects.count(), 1)
        self.assertEquals(Project.objects.count(), 2)

        self.assertEquals(ProjectQuarterlySpend.objects.count(), 2)
        self.assertEquals(ProjectQuarterlySpend.objects.get(project__project_description="P-CNIEU COM FAC HALLS", financial_year=fy).q1, 150027)
        self.assertEquals(ProjectQuarterlySpend.objects.get(project__project_description="P-CNIEU COM FAC HALLS", financial_year=fy).q2, 529282)
        self.assertEquals(ProjectQuarterlySpend.objects.get(project__project_description="P-CNIEU COM FAC HALLS", financial_year=fy).q3, 2168473)


    def test_quarterly_update(self):
        """Scope of Test: Check that quarterly spends can be updated for a specific project"""

        geography = Geography.objects.get(geo_code="BUF")

        fy = FinancialYear.objects.create(budget_year="2019/2020")
        utils.load_file(geography, mock_project_row(), fy)
        utils.load_file(geography, mock_quarterly_row(), fy)

        fy = FinancialYear.objects.get(budget_year="2020/2021")
        utils.load_file(geography, mock_data_existing_project_row(), fy)
        utils.load_file(geography, mock_quarterly_update_row(), fy)

        self.assertEquals(ProjectQuarterlySpend.objects.count(), 2)
        self.assertEquals(ProjectQuarterlySpend.objects.get(project__project_description="P-CNIN FURN & OFF EQUIP", financial_year=fy).q1, 13000)
        self.assertEquals(ProjectQuarterlySpend.objects.get(project__project_description="P-CNIN FURN & OFF EQUIP", financial_year=fy).q2, 14000)
        self.assertEquals(ProjectQuarterlySpend.objects.get(project__project_description="P-CNIN FURN & OFF EQUIP", financial_year=fy).q3, 15000)
        self.assertEquals(ProjectQuarterlySpend.objects.get(project__project_description="P-CNIN FURN & OFF EQUIP", financial_year=fy).q4, 16000)

