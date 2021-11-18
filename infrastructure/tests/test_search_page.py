from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django_q.models import OrmQ

from infrastructure.models import FinancialYear, Project, AnnualSpendFile, ProjectQuarterlySpend, Expenditure, BudgetPhase
from infrastructure.upload import process_annual_document
from scorecard.models import Geography

from infrastructure.tests.helpers import BaseSeleniumTestCase
from infrastructure.tests import utils

import urllib.request
import csv


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


class CapitalSearchTest(BaseSeleniumTestCase):
    fixtures = ["seeddata"]

    def setUp(self):
        self.geography = Geography.objects.create(
            geo_level="municipality",
            geo_code="BUF",
            province_name="Eastern Cape",
            province_code="EC",
            category="A",
        )

        FinancialYear.objects.create(budget_year="2019/2020")

        super(CapitalSearchTest, self).setUp()
        Site.objects.filter(id=2).update(domain='municipalmoney.org.za', name='Scorecard')
        
    def test_search_results(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/"))
        
        utils.load_file(self.geography, mock_project_row(), "2019/2020")
        
        project = Project.objects.get(project_description="P-CNIN FURN & OFF EQUIP")
        self.assertEquals(project.project_description, "P-CNIN FURN & OFF EQUIP")
        
        self.wait_until_text_in("#result-list-container", "P-CNIN FURN & OFF EQUIP")
        
    def test_download_button_exists(self):
        selenium = self.selenium
        selenium.get("%s%s" % (self.live_server_url, "/infrastructure/projects/"))
        self.wait_until_text_in("#Search-Button", "Search")
    
    def test_download_url(self):
        utils.load_file(self.geography, mock_project_row(), "2019/2020")
        url = f"{self.live_server_url}/infrastructure/download?budget_phase=Budget+year&financial_year=2019%2F2020&province=Eastern+Cape&municipality=Buffalo+City&q=&function=Fleet+Management"
        response = urllib.request.urlopen(url)
        
