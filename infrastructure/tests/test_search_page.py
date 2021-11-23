from django.contrib.sites.models import Site

from infrastructure.models import FinancialYear
from scorecard.models import Geography
from infrastructure.tests.helpers import BaseSeleniumTestCase
from infrastructure.tests import utils

import urllib.request
#from constance import config
from constance.test import override_config

def mock_project_one():
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


def mock_project_two():
    mock_data = { 'Function': 'Economic Development/Planning',
        'Project Description': 'P-CIN RDS ROADS',
        'Project Number': 'PC001002006001_00028',
        'Type': 'New',
        'MTSF Service Outcome': 'An efficient, competitive and responsive economic infrastructure network',
        'IUDF': 'Growth',
        'Own Strategic Objectives': 'OWN MUNICIPAL STRATEGIC OBJECTIVE',
        'Asset Class': 'Roads Infrastructure',
        'Asset Sub-Class': '',
        'Ward Location': 'Coastal,Midland,...',
        'GPS Longitude': '0', 'GPS Latitude': '0',
        'Audited Outcome 2017/18': 2000.0,
        'Full Year Forecast 2018/19': 3000.0,
        'Budget year 2019/20': 4000.0,
        'Budget year 2020/21': 5000.0,
        'Budget year 2021/22': 6000.0
    }
    yield mock_data

def mock_project_next_financial_year():
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
        'Audited Outcome 2018/19': 10000.0,
        'Full Year Forecast 2019/20': 11000.0,
        'Budget year 2020/21': 12000.0,
        'Budget year 2021/22': 13000.0,
        'Budget year 2022/23': 14000.0
    }
    yield mock_data

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


class CapitalSearchTest(BaseSeleniumTestCase):
    fixtures = ["demo-data", "seeddata"]

    def setUp(self):
        FinancialYear.objects.create(budget_year="2019/2020")

        super(CapitalSearchTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')

    def test_municipality_search_filter(self):

        geography = Geography.objects.get(geo_code="BUF")
        utils.load_file(geography, mock_project_one(), "2019/2020")
        geography = Geography.objects.get(geo_code="TSH")
        utils.load_file(geography, mock_project_two(), "2019/2020")

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/?municipality=Buffalo+City"))

        self.wait_until_text_in(".search-detail_projects", "1")

        self.wait_until_text_in("#result-list-container", "P-CNIN FURN & OFF EQUIP")
        self.wait_until_text_in("#result-list-container", "ADMINISTRATIVE AND CORPORATE SUPPORT")
        self.wait_until_text_in("#result-list-container", "R4.00 K")

    @override_config(CAPITAL_PROJECT_SUMMARY_YEAR="2020/2021")
    def test_implementation_year_filter(self):

        geography = Geography.objects.get(geo_code="BUF")
        utils.load_file(geography, mock_project_one(), "2019/2020")
        utils.load_file(geography, mock_project_next_financial_year(), "2020/2021")

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/?financial_year=2020%2F2021"))

        self.wait_until_text_in(".search-detail_projects", "1")

        self.wait_until_text_in("#result-list-container", "P-CNIN FURN & OFF EQUIP")
        self.wait_until_text_in("#result-list-container", "ADMINISTRATIVE AND CORPORATE SUPPORT")
        self.wait_until_text_in("#result-list-container", "R12.00 K")

    def download_button_exists(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/"))

        download_button = selenium.find_element_by_id('Download-Button')
        download_button.click()
        self.assertEquals(download_button.get_attribute("href"), f"{self.live_server_url}/infrastructure/download?budget_phase=Budget+year&financial_year=2019%2F2020")

    def test_download_url(self):
        geography = Geography.objects.get(geo_code="BUF")
        utils.load_file(geography, mock_project_one(), "2019/2020")

        url = f"{self.live_server_url}/infrastructure/download?budget_phase=Budget+year&financial_year=2019%2F2020"
        response = urllib.request.urlopen(url)
        contents = response.readlines()

        headers = get_download_row(contents[0])
        project_row = get_download_row(contents[1])

        self.assertEquals(len(contents), 2)
        self.assertEquals(download_column_headers(), headers)
        self.assertEquals(project_download_data(), project_row)
