from django.contrib.sites.models import Site

from scorecard.models import Geography
from infrastructure.tests.helpers import BaseSeleniumTestCase
from infrastructure.tests import utils

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
        'Audited Outcome 2017/18': 7000.0,
        'Full Year Forecast 2018/19': 8000.0,
        'Budget year 2019/20': 9000.0,
        'Budget year 2020/21': 10000.0,
        'Budget year 2021/22': 11000.0
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


class ScorecardIndicatorTest(BaseSeleniumTestCase):
    fixtures = ["demo-data", "seeddata"]

    def setUp(self):
        super(ScorecardIndicatorTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')

    def test_indicator(self):
        geography = Geography.objects.get(geo_code="BUF")
        utils.load_file(geography, mock_project_one(), "2019/2020")
        utils.load_file(geography, mock_project_two(), "2019/2020")

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        self.wait_until_text_in("#capital-projects", "2019-2020")
        self.wait_until_text_in("#capital-projects", "P-CNIN FURN & OFF EQUIP")
        self.wait_until_text_in("#capital-projects", "R4 000")
        self.wait_until_text_in("#capital-projects", "P-CIN RDS ROADS")
        self.wait_until_text_in("#capital-projects", "R9 000")
        self.wait_until_text_in("#capital-projects", "Showing 2 of 2")

    @override_config(CAPITAL_PROJECT_SUMMARY_YEAR="2020/2021")
    def test_indicator_by_year(self):
        geography = Geography.objects.get(geo_code="BUF")
        utils.load_file(geography, mock_project_one(), "2019/2020")
        utils.load_file(geography, mock_project_next_financial_year(), "2020/2021")

        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/profiles/municipality-BUF-buffalo-city/"))

        self.wait_until_text_in("#capital-projects", "2020-2021")
        self.wait_until_text_in("#capital-projects", "R12 000")
        self.wait_until_text_in("#capital-projects", "Showing 1 of 1")
