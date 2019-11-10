from django.test import TestCase
from infrastructure import utils
from infrastructure import models
import json

class TestProject(TestCase):
    fixtures = ["test_infrastructure.json"]

    def test_individual_project(self):
        test_data = json.loads(""" {
            "id": 1,
            "expenditure": [ ],
            "geography": {
                "bbox": [18.307220001000076, -34.35833999699997, 19.005338203000065, -33.47127600399995],
                "geo_level": "municipality",
                "geo_code": "CPT",
                "name": "City of Cape Town",
                "long_name": "City of Cape Town, Western Cape",
                "square_kms": 2446.42989002681,
                "parent_level": "province",
                "parent_code": "WC",
                "province_name": "Western Cape",
                "province_code": "WC",
                "category": "A",
                "miif_category": "A",
                "population": 3740026
            },
            "function": "Administrative and Corporate Support",
            "project_description": "Acquisition & Registr & servitude FY20",
            "project_number": "PC001002004002_00473",
            "project_type": "New",
            "mtsf_service_outcome": "An efficient, competitive and responsive economic infrastructure network",
            "iudf": "Growth",
            "own_strategic_objectives": "Infrastructure Investment Programme",
            "asset_class": "Water Supply Infrastructure",
            "asset_subclass": "Boreholes",
            "ward_location": "Corporate Infrastructure Projects",
            "longitude": 0,
            "latitude": 0
        }
        """)
        self.maxDiff = None
        response = self.client.get("/api/infrastructure/projects/1/?full=True")
        self.assertEqual(response.status_code, 200)

        js = response.json()
        self.assertEquals(test_data, js)

    def test_geography_projects(self):
        response = self.client.get("/api/infrastructure/projects/?geo=CPT")
        self.assertEqual(response.status_code, 200)
        js = response.json()
        self.assertEquals(len(js["results"]), 2)

        response = self.client.get("/api/infrastructure/projects/?geo=WC011")
        self.assertEqual(response.status_code, 200)
        js = response.json()
        self.assertEquals(len(js["results"]), 1)
