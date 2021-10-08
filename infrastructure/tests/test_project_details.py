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
        self.wait_until_text_in(".page-heading", "Municipal Infrastructure Projects")

        selenium.find_element_by_css_selector(".narrow-card_first-column-2").click()

        self.wait_until_text_in(".project-description", "P-CNIEU COM FAC HALLS")
        self.wait_until_text_in(".project-number__value", "PC002002002002001001_00001")

        self.wait_until_text_in(".asset-class", "Community Facilities (Halls)")
        self.wait_until_text_in(".function", "Community Halls and Facilities")
        self.wait_until_text_in(".mtsf-outcome", "An efficient, effective and development-oriented public service")
        self.wait_until_text_in(".iudf", "Inclusion and access")
        self.wait_until_text_in(".province", "Eastern Cape")
        #self.wait_until_text_in(".municipality", "Buffalo City") Webflow needs a fix to make this work
        self.wait_until_text_in(".ward", "Coastal,Whole of the Metro,...")
        self.wait_until_text_in(".full-year-forecast .year", "2018/2019")
        self.wait_until_text_in(".project-detail_text.forecast", "R15.50 Million")
        self.wait_until_text_in(".project-detail_text.budget1", "R5.50 Million")
        self.wait_until_text_in(".project-detail_text.budget2", "R6.00 Million")
        self.wait_until_text_in(".project-detail_text.budget3", "R15.00 Million")
