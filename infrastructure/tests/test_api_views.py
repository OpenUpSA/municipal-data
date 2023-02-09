from django.test import TestCase


class TestProject(TestCase):
    fixtures = ["test_infrastructure.json"]

    def test_infrastructure_project_filters(self):
        response = self.client.get(
            "/api/v1/infrastructure/search/?q=&province=Western+Cape&municipality=City+of+Cape+Town&project_type=New&function=Administrative+and+Corporate+Support&budget_phase=Budget+year&quarterly_phase=Original+Budget&financial_year=2019%2F2020&ordering=-total_forecast_budget"
        )
        self.assertEqual(response.status_code, 200)
        js = response.json()
        self.assertEquals(js["count"], 2)
        self.assertEquals(len(js["results"]["projects"]), 2)

    def test_infrastructure_project_search(self):
        response = self.client.get(
            "/api/v1/infrastructure/search/?q=PC001002004002_00473&budget_phase=Budget+year&quarterly_phase=Original+Budget&financial_year=2019%2F2020&ordering=-total_forecast_budget"
        )
        self.assertEqual(response.status_code, 200)
        js = response.json()
        self.assertEquals(js["count"], 1)
        self.assertEquals(len(js["results"]["projects"]), 1)

        response = self.client.get(
            "/api/v1/infrastructure/search/?q=Acquisition&budget_phase=Budget+year&quarterly_phase=Original+Budget&financial_year=2019%2F2020&ordering=-total_forecast_budget"
        )
        self.assertEqual(response.status_code, 200)
        js = response.json()
        self.assertEquals(js["count"], 1)
        self.assertEquals(len(js["results"]["projects"]), 1)

    def test_facet_count(self):
        response = self.client.get(
            "/api/v1/infrastructure/search/?q=&budget_phase=Budget+year&financial_year=2019%2F2020"
        )
        self.assertEqual(response.status_code, 200)

        js = response.json()
        self.assertEquals(js["results"]["facets"]["municipality"][0]["count"], 2)
