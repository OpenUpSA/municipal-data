from django.test import TestCase

from infrastructure.models import Project


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

    def test_coordinates_match_search_filters(self):
        Project.objects.filter(pk__in=[1, 2]).update(latitude=-33.92, longitude=18.42)
        params = "?q=&budget_phase=Budget+year&quarterly_phase=Original+Budget&financial_year=2019%2F2020"

        search = self.client.get("/api/v1/infrastructure/search/" + params).json()
        coordinates = self.client.get("/api/v1/infrastructure/coordinates/" + params).json()

        search_ids = {p["id"] for p in search["results"]["projects"]}
        coordinate_ids = {p["id"] for p in coordinates["results"]}
        located_ids = set(
            Project.objects.filter(pk__in=search_ids)
            .exclude(latitude=0)
            .values_list("id", flat=True)
        )
        self.assertTrue(located_ids)
        self.assertEqual(coordinate_ids, located_ids)

    def test_facet_count(self):
        response = self.client.get(
            "/api/v1/infrastructure/search/?q=&budget_phase=Budget+year&financial_year=2019%2F2020"
        )
        self.assertEqual(response.status_code, 200)

        js = response.json()
        self.assertEquals(js["results"]["facets"]["municipality"][0]["count"], 2)
        self.assertEquals(js["results"]["facets"]["type"][0]["count"], 2)
        self.assertEquals(js["results"]["facets"]["function"][0]["count"], 2)
        self.assertEquals(js["results"]["facets"]["province"][0]["count"], 2)
