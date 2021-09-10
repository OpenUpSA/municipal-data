from django.test import Client, TestCase
from infrastructure import utils
from infrastructure import models
import json

from infrastructure.models import FinancialYear, QuarterlySpendFile, Expenditure, Project

from scorecard.models import Geography
from scorecard.profiles import MunicipalityProfile
from scorecard.admin import MunicipalityProfilesCompilationAdmin


class TestProject(TestCase):
    def setUp(self):
        fixtures = ["test_infrastructure.json"]
        TestProject.geography = Geography.objects.create(
            geo_level="municipality",
            geo_code="BUF",
            province_name="Eastern Cape",
            province_code="EC",
            category="A",
        )


    def test_infrastructure_project_search(self):
         response = self.client.get(
             "/api/v1/infrastructure/search/?province=Eastern+Cape&municipality=Buffalo+City&q=&budget_phase=Budget+year&financial_year=2019%2F2020&ordering=-total_forecast_budget")
         self.assertEqual(response.status_code, 200)
         js = response.json()
         self.assertEquals(len(js["results"]), 3)
