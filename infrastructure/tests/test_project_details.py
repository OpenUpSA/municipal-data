from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django_q.models import OrmQ

from infrastructure.models import FinancialYear, Project, AnnualSpendFile
from infrastructure.upload import process_annual_document
from scorecard.models import Geography

from infrastructure.tests.helpers import BaseSeleniumTestCase


class CapitalProjectTest(BaseSeleniumTestCase):
    fixtures = ["seeddata"]

    def setUp(self):
        self.client = Client()
        self.username = 'admin'
        self.email = 'test@whatever.com'
        self.password = 'password'
        self.user = User.objects.create_superuser(self.username, self.email, self.password)

        self.geography = Geography.objects.create(
            geo_level="municipality",
            geo_code="BUF",
            province_name="Eastern Cape",
            province_code="EC",
            category="A",
        )

        self.client.login(username=self.username, password=self.password)
        fy = FinancialYear.objects.create(budget_year="2019/2020", active=1)

        upload_url = reverse('admin:infrastructure_annualspendfile_add')

        with open('infrastructure/tests/test_files/test.xlsx', 'rb', ) as f:
            resp = self.client.post(upload_url, {'financial_year': fy.pk, 'document': f}, follow=True)

        task = OrmQ.objects.first()
        task_file_id = task.task()["args"][0]
        process_annual_document(task_file_id)

        super(CapitalProjectTest, self).setUp()

    def test_project_details(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/"))
        project_title = selenium.find_element_by_css_selector(".page-heading").text
        selenium.find_element_by_css_selector(".narrow-card_first-column-2").click()

        self.assertEqual(project_title, "Municipal Infrastructure Projects")
        project_desc = selenium.find_element_by_css_selector(".project-number__value").text
        self.assertEqual(project_desc, "PC002002002002001001_00001")
