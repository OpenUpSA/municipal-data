from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django_q.models import OrmQ

from infrastructure.models import FinancialYear, Project, AnnualSpendFile, ProjectQuarterlySpend, Expenditure
from infrastructure.upload import process_annual_document
from scorecard.models import Geography

from infrastructure.tests.helpers import BaseSeleniumTestCase


class CapitalProjectTest(BaseSeleniumTestCase):
    fixtures = ["seeddata"]

    def setUp(self):
        self.geography = Geography.objects.create(
            geo_level="municipality",
            geo_code="BUF",
            province_name="Eastern Cape",
            province_code="EC",
            category="A",
        )

        self.fy = FinancialYear.objects.create(budget_year="2019/2020", active=1)

        fields = {
            "geography": self.geography,
            "function": "Community Halls and Facilities",
            "project_description": "P-CNIEU COM FAC HALLS",
            "project_number": "PC002002002002001001_00001",
            "project_type": "Upgrading",
            "mtsf_service_outcome": "An efficient, effective and development-oriented public service",
            "iudf": "Inclusion and access",
            "asset_class": "Community Facilities",
            "asset_subclass": "Halls",
            "ward_location": "Coastal,Whole of the Metro,...",
            "longitude": "10",
            "latitude": "20",
            "latest_implementation_year": self.fy,
        }
        self.project = Project.objects.create(**fields)

        self.create_expenditure(15500000, "Full Year Forecast", "2018/2019")
        self.create_expenditure(5500000, "Budget year", "2019/2020")
        self.create_expenditure(6000000, "Budget year", "2020/2021")
        financial_year = FinancialYear.objects.create(budget_year="2021/2022")

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
        self.wait_until_text_in(".ward", "Coastal,Whole of the Metro,...")
        self.wait_until_text_in(".full-year-forecast .year", "2018/2019")
        self.wait_until_text_in(".project-detail_text.forecast", "R15.50 Million")
        self.wait_until_text_in(".budget-year-1 .year", "2019/2020")
        self.wait_until_text_in(".project-detail_text.budget1", "R5.50 Million")
        self.wait_until_text_in(".budget-year-2 .year", "2020/2021")
        self.wait_until_text_in(".project-detail_text.budget2", "R6.00 Million")
        self.wait_until_text_in(".budget-year-3 .year", "2021/2022")
        self.wait_until_text_in(".project-detail_text.budget3", "Not available")

        self.wait_until_text_in(".subsection-chart_wrapper .project-detail_heading", "NO DATA AVAILABLE")

    def test_quarterly_chat(self):
        self.quarterly_spend = ProjectQuarterlySpend.objects.create(
            project=self.project,
            financial_year=self.fy,
            q1=1000,
        )

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/"))
        selenium.find_element_by_css_selector(".narrow-card_first-column-2").click()

        self.wait_until_text_in(".subsection-chart_wrapper", "Financial Year 2019/2020")
