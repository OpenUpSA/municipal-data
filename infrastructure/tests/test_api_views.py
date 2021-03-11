from django.test import Client, TestCase
from infrastructure import utils
from infrastructure import models
import json
from scorecard.profiles import MunicipalityProfile
#from scorecard.admin import MunicipalityProfileAdmin # not working
from scorecard.admin import MunicipalityProfilesCompilationAdmin


class TestProject(TestCase):
    fixtures = ["test_infrastructure.json"]

       
    def test_infrastructure_project_search(self):
        response = self.client.get("/api/v1/infrastructure/projects/?geo=BUF")
        self.assertEqual(response.status_code, 200)
        js = response.json()
        self.assertEquals(len(js["results"]), 1)
        self.assertEquals(len(js["results"][0]["geography"]["bbox"]), 0)

        response = self.client.get("/api/v1/infrastructure/search/?province=Eastern+Cape&municipality=Buffalo+City&q=&budget_phase=Budget+year&financial_year=2019%2F2020&ordering=-total_forecast_budget")
        self.assertEqual(response.status_code, 200)
        js = response.json()
        self.assertEquals(len(js["results"]), 3)

    def test_municipal_profile_list_page(self):
        c = Client()
        response = c.get("/profiles/municipality-BUF-buffalo-city",follow=True)

        self.assertContains(response, '<h1 class="page-heading__title">Buffalo City</h1>')
    # def test_municipal_project_detail_view(self):
    #     c = Client()
    #     response = c.get("/infrastructure/projects/313")
    #     self.assertEqual(response.status_code, 200)
        # self.assertContains(
        #     response, "PC001002006001_00019"
        # )

        
    # def test_municipal_project_detail_view(self):
    #     response = self.client.get('/infrastructure/projects/313',follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     #self.assertContains(response,"PC001002006001_00019")
