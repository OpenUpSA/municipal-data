from django.contrib.sites.models import Site

from scorecard.models import Geography
from municipal_finance.tests.helpers import BaseSeleniumTestCase
from selenium.webdriver.common.keys import Keys
from infrastructure.tests import utils
from infrastructure.models import FinancialYear, Project, Expenditure, BudgetPhase, ProjectQuarterlySpend

import urllib.request
from constance.test import override_config


def download_column_headers():
    columns = "province,municipality,project_number,project_description,project_type,function,asset_class,mtsf_service_outcome,own_strategic_objectives,iudf,budget phase,financial year,amount,latitude,longitude"
    return columns

def project_download_data():
    project_data = 'Eastern Cape,Buffalo City,PC002003005_00002,P-CNIN FURN & OFF EQUIP,New,Administrative and Corporate Support,Furniture and Office Equipment,"An efficient, effective and development-oriented public service",OWN MUNICIPAL STRATEGIC OBJECTIVE,Growth,Budget year,2019/2020,4000.00,0.0,0.0'
    return project_data

def get_download_row(row_contents):
    row = row_contents.decode('utf-8')
    row = row.strip('\n')
    row = row.strip('\r')
    return row

def create_expenditure(project, amount, phase, year):
    budget_phase = BudgetPhase.objects.get(name=phase)
    financial_year = FinancialYear.objects.get_or_create(budget_year=year)

    expenditure = Expenditure.objects.create(
        project=project,
        budget_phase=budget_phase,
        financial_year=financial_year[0],
        amount=amount,
    )
    return expenditure

def project_base(geography, year):
    return {
        "geography": geography,
        "project_type": "New",
        "mtsf_service_outcome": "An efficient, effective and development-oriented public service",
        "iudf": "Growth",
        "own_strategic_objectives": "OWN MUNICIPAL STRATEGIC OBJECTIVE",
        "asset_class": "Furniture and Office Equipment",
        "asset_subclass": "",
        "ward_location": "Administrative or Head Office",
        "longitude": "0",
        "latitude": "0",
        "latest_implementation_year": year,
    }

def project_one():
    return {
        "function": "Administrative and Corporate Support",
        "project_description": "P-CNIN FURN & OFF EQUIP",
        "project_number": "PC002003005_00002",
    }


class CapitalSearchTest(BaseSeleniumTestCase):
    fixtures = ["demo-data", "seeddata"]

    def setUp(self):
        super(CapitalSearchTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')

    def test_municipality_search_filter(self):
        geography = Geography.objects.get(geo_code="BUF")
        financial_year = FinancialYear.objects.get(budget_year="2019/2020")

        project = Project.objects.create(**project_base(geography, financial_year), **project_one())
        create_expenditure(project, 4000, "Budget year", "2019/2020")
        create_expenditure(project, 5000, "Budget year", "2020/2021")
        create_expenditure(project, 6000, "Budget year", "2021/2022")

        project_two = {
            "function": "Economic Development/Planning",
            "project_description": "P-CIN RDS ROADS",
            "project_number": "PC001002006001_00028",
        }

        geography = Geography.objects.get(geo_code="TSH")
        project = Project.objects.create(**project_base(geography, financial_year), **project_two)
        create_expenditure(project, 7000, "Budget year", "2019/2020")
        create_expenditure(project, 8000, "Budget year", "2020/2021")
        create_expenditure(project, 9000, "Budget year", "2021/2022")

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/?municipality=Buffalo+City"))

        self.wait_until_text_in(".page-heading", "2019/2020")
        self.wait_until_text_in("#municipality-dropdown", "Buffalo City")
        self.wait_until_text_in(".search-detail_projects", "1")

        self.wait_until_text_in("#result-list-container", "P-CNIN FURN & OFF EQUIP")
        self.wait_until_text_in("#result-list-container", "ADMINISTRATIVE AND CORPORATE SUPPORT")
        self.wait_until_text_in("#result-list-container", "R4.00 K")

        results = selenium.find_element_by_css_selector("#result-list-container")
        self.assertNotIn("P-CIN RDS ROADS", results.text)

    @override_config(CAPITAL_PROJECT_SUMMARY_YEAR="2020/2021")
    def test_implementation_year_filter(self):
        geography = Geography.objects.get(geo_code="BUF")
        financial_year = FinancialYear.objects.get(budget_year="2019/2020")

        project = Project.objects.create(**project_base(geography, financial_year), **project_one())
        create_expenditure(project, 4000, "Budget year", "2019/2020")
        create_expenditure(project, 5000, "Budget year", "2020/2021")
        create_expenditure(project, 6000, "Budget year", "2021/2022")


        financial_year = FinancialYear.objects.get(budget_year="2020/2021")
        project_two = {
            "function": "Administrative and Corporate Support",
            "project_description": "P-CNIN FURN & OFF EQUIP",
            "project_number": "PC002003005_00002",
        }

        geography = Geography.objects.get(geo_code="TSH")
        project = Project.objects.create(**project_base(geography, financial_year), **project_two)
        create_expenditure(project, 12000, "Budget year", "2020/2021")
        create_expenditure(project, 13000, "Budget year", "2021/2022")
        create_expenditure(project, 14000, "Budget year", "2022/2023")

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/?financial_year=2020%2F2021"))

        self.wait_until_text_in(".search-detail_projects", "1")

        self.wait_until_text_in("#result-list-container", "P-CNIN FURN & OFF EQUIP")
        self.wait_until_text_in("#result-list-container", "ADMINISTRATIVE AND CORPORATE SUPPORT")
        self.wait_until_text_in("#result-list-container", "R12.00 K")

        results = selenium.find_element_by_css_selector("#result-list-container")
        self.assertNotIn("R4.00 K", results.text)

    def download_button_exists(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/"))

        download_button = selenium.find_element_by_id('Download-Button')
        download_button.click()
        self.assertEquals(download_button.get_attribute("href"), f"{self.live_server_url}/infrastructure/download?budget_phase=Budget+year&financial_year=2019%2F2020")

    def test_download_url(self):
        geography = Geography.objects.get(geo_code="BUF")
        financial_year = FinancialYear.objects.get(budget_year="2019/2020")

        project_data = {
            "function": "Administrative and Corporate Support",
            "project_description": "P-CNIN FURN & OFF EQUIP",
            "project_number": "PC002003005_00002",
        }

        project = Project.objects.create(**project_base(geography, financial_year), **project_data)
        create_expenditure(project, 2000, "Audited Outcome", "2017/2018")
        create_expenditure(project, 3000, "Full Year Forecast", "2018/2019")
        create_expenditure(project, 4000, "Budget year", "2019/2020")
        create_expenditure(project, 5000, "Budget year", "2020/2021")
        create_expenditure(project, 6000, "Budget year", "2021/2022")

        url = f"{self.live_server_url}/infrastructure/download?budget_phase=Budget+year&financial_year=2019%2F2020"
        response = urllib.request.urlopen(url)
        contents = response.readlines()

        headers = get_download_row(contents[0])
        project_row = get_download_row(contents[1])

        self.assertEquals(len(contents), 2)
        self.assertEquals(download_column_headers(), headers)
        self.assertEquals(project_download_data(), project_row)

    def test_search_projects(self):
        geography = Geography.objects.get(geo_code="BUF")
        financial_year = FinancialYear.objects.get(budget_year="2019/2020")

        project = Project.objects.create(**project_base(geography, financial_year), **project_one())
        create_expenditure(project, 4000, "Budget year", "2019/2020")
        create_expenditure(project, 5000, "Budget year", "2020/2021")
        create_expenditure(project, 6000, "Budget year", "2021/2022")

        quarterly_data = {
            "function": "Economic Development/Planning",
            "project_description": "P-CIN RDS ROADS",
            "project_number": "PC001002006001_00028",
        }

        project = Project.objects.create(**project_base(geography, financial_year), **quarterly_data)
        create_expenditure(project, 7000, "Original Budget", "2019/2020")
        ProjectQuarterlySpend.objects.create(project=project, financial_year=financial_year, q1=1000)

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/"))

        self.wait_until_text_in(".search-detail_projects", "2")
        self.wait_until_text_in("#search-total-forecast", "R4,000")

        self.wait_until_text_in("#result-list-container", "P-CNIN FURN & OFF EQUIP")
        self.wait_until_text_in("#result-list-container", "ADMINISTRATIVE AND CORPORATE SUPPORT")
        self.wait_until_text_in("#result-list-container", "R4.00 K")

    def test_search_annual_and_quarterly(self):
        # When an annual project exists check info is correctly updated and displayed after a quarterly update
        geography = Geography.objects.get(geo_code="BUF")
        financial_year = FinancialYear.objects.get(budget_year="2019/2020")

        project = Project.objects.create(**project_base(geography, financial_year), **project_one())
        create_expenditure(project, 7000, "Budget year", "2019/2020")
        create_expenditure(project, 8000, "Budget year", "2020/2021")
        create_expenditure(project, 9000, "Budget year", "2021/2022")
        create_expenditure(project, 12000, "Full Year Forecast", "2018/2019")

        create_expenditure(project, 10000, "Original Budget", "2019/2020")
        create_expenditure(project, 11000, "Adjusted Budget", "2019/2020")
        ProjectQuarterlySpend.objects.create(project=project, financial_year=financial_year, q1=1000)

        project_two = {
            "function": "Economic Development/Planning",
            "project_description": "P-CIN RDS ROADS",
            "project_number": "PC001002006001_00028",
        }
        project = Project.objects.create(**project_base(geography, financial_year), **project_two)
        create_expenditure(project, 7000, "Budget year", "2019/2020")
        create_expenditure(project, 8000, "Budget year", "2020/2021")
        create_expenditure(project, 9000, "Budget year", "2021/2022")
        create_expenditure(project, 12000, "Full Year Forecast", "2018/2019")

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/?municipality=Buffalo+City"))

        self.wait_until_text_in(".page-heading", "2019/2020")
        self.wait_until_text_in("#municipality-dropdown", "Buffalo City")
        self.wait_until_text_in(".search-detail_projects", "2")
        self.wait_until_text_in("#search-total-forecast", "R14,000")

        self.wait_until_text_in("#result-list-container", "P-CNIN FURN & OFF EQUIP")
        self.wait_until_text_in("#result-list-container", "ADMINISTRATIVE AND CORPORATE SUPPORT")
        self.wait_until_text_in("#result-list-container", "R7.00 K")

        self.enter_text("#Infrastructure-Search-Input", "P-CIN RDS ROADS")
        self.click("#Search-Button")

        self.wait_until_text_in(".search-detail_projects", "1")
        self.wait_until_text_in("#result-list-container", "P-CIN RDS ROADS")
        self.wait_until_text_in("#result-list-container", "R7.00 K")

    def test_search_quarterly(self):
        # Test that quarterly uploads can create and display new projects
        geography = Geography.objects.get(geo_code="BUF")
        financial_year = FinancialYear.objects.get(budget_year="2019/2020")

        project = Project.objects.create(**project_base(geography, financial_year), **project_one())
        create_expenditure(project, 2000, "Audited Outcome", "2018/2019")
        create_expenditure(project, 10000, "Original Budget", "2019/2020")
        create_expenditure(project, 11000, "Adjusted Budget", "2019/2020")
        ProjectQuarterlySpend.objects.create(project=project, financial_year=financial_year, q1=1000)

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/?municipality=Buffalo+City"))

        self.wait_until_text_in(".page-heading", "2019/2020")
        self.wait_until_text_in("#municipality-dropdown", "Buffalo City")
        self.wait_until_text_in(".search-detail_projects", "1")
        self.wait_until_text_in("#result-list-container", "P-CNIN FURN & OFF EQUIP")
        self.wait_until_text_in("#result-list-container > a.narrow-card_wrapper-2.w-inline-block > div.narrow-card_last-column-2", "")

    def test_url_query_string(self):
        geography = Geography.objects.get(geo_code="BUF")
        financial_year = FinancialYear.objects.get(budget_year="2019/2020")

        project = Project.objects.create(**project_base(geography, financial_year), **project_one())
        create_expenditure(project, 2000, "Audited Outcome", "2018/2019")
        create_expenditure(project, 10000, "Original Budget", "2019/2020")
        create_expenditure(project, 11000, "Adjusted Budget", "2019/2020")
        ProjectQuarterlySpend.objects.create(project=project, financial_year=financial_year, q1=1000)

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/?q=cnin&province=Eastern+Cape&municipality=Buffalo+City&project_type=New&function=Administrative+and+Corporate+Support"))

        self.wait_until_text_in(".page-heading", "2019/2020")
        self.assertEquals(selenium.find_element_by_css_selector("#Infrastructure-Search-Input").get_attribute('value'), "cnin")
        self.wait_until_text_in("#province-dropdown", "Eastern Cape")
        self.wait_until_text_in("#municipality-dropdown", "Buffalo City")
        self.wait_until_text_in("#type-dropdown", "New")
        self.wait_until_text_in("#functions-dropdown", "Administrative and Corporate Support")
        self.wait_until_text_in(".search-detail_projects", "1")
        self.wait_until_text_in("#result-list-container", "P-CNIN FURN & OFF EQUIP")

    def test_search_events(self):
        geography = Geography.objects.get(geo_code="BUF")
        financial_year = FinancialYear.objects.get(budget_year="2019/2020")
        project = Project.objects.create(**project_base(geography, financial_year), **project_one())
        create_expenditure(project, 7000, "Budget year", "2019/2020")
        project_two = {
            "function": "Economic Development/Planning",
            "project_description": "P-CIN RDS ROADS",
            "project_number": "PC001002006001_00028",
        }
        project = Project.objects.create(**project_base(geography, financial_year), **project_two)
        create_expenditure(project, 7000, "Budget year", "2019/2020")

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/?municipality=Buffalo+City"))
        self.wait_until_text_in(".search-detail_projects", "2")

        # Press enter key
        self.enter_text("#Infrastructure-Search-Input", "P-CIN RDS ROADS")
        selenium.find_element_by_css_selector("#Infrastructure-Search-Input").send_keys(Keys.RETURN)
        self.wait_until_text_in(".search-detail_projects", "1")
        # Click clear filter button
        self.click(".clear-filter__text")
        self.wait_until_text_in(".search-detail_projects", "2")
        # Add a filter with a dropdown menu
        self.click("#functions-dropdown .chart-dropdown_trigger")
        self.selenium.find_elements_by_css_selector("#functions-dropdown .chart-dropdown_list a")[1].click()
        self.wait_until_text_in(".search-detail_projects", "1")
        # Remove filters with a dropdown menu
        self.click("#functions-dropdown")
        self.click("#functions-dropdown")
        self.click("#functions-dropdown")
        self.wait_until_text_in(".search-detail_projects", "2")

    def test_back_button(self):
        geography = Geography.objects.get(geo_code="BUF")
        financial_year = FinancialYear.objects.get(budget_year="2019/2020")
        project = Project.objects.create(**project_base(geography, financial_year), **project_one())
        create_expenditure(project, 7000, "Budget year", "2019/2020")
        project_two = {
            "function": "Economic Development/Planning",
            "project_description": "P-CIN RDS ROADS",
            "project_number": "PC001002006001_00028",
        }
        project = Project.objects.create(**project_base(geography, financial_year), **project_two)
        create_expenditure(project, 7000, "Budget year", "2019/2020")

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/?municipality=Buffalo+City"))
        self.wait_until_text_in(".search-detail_projects", "2")

        # Add a filter with a dropdown menu
        self.click("#functions-dropdown .chart-dropdown_trigger")
        self.selenium.find_elements_by_css_selector("#functions-dropdown .chart-dropdown_list a")[1].click()
        self.wait_until_text_in(".search-detail_projects", "1")
        self.wait_until_text_in("#functions-dropdown .text-block", "Administrative and Corporate Support")

        # Click back button
        selenium.back()
        self.wait_until_text_in(".search-detail_projects", "2")
        self.wait_until_text_in("#functions-dropdown .text-block", "All Functions")
