from django.test import TestCase
from unittest import mock
import json
from . import models, serializers
import json

def request_mock(json_data, response_code=200):
    def _request_mock(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(json_data, response_code)
    return _request_mock

cpt_coords = {
    "min_lat": -34.35833999699997,
    "max_lat": -33.47127600399995,
    "parts": 2,
    "centre_lon": 18.594296829500248,
    "max_lon": 19.005338203000065,
    "min_lon": 18.307220001000076,
    "centre_lat": -33.89270693372812
}

fixtures = {
    "parent_map": {
        "geo_level":"my geo_level",
        "geo_code": "CPT",
        "name": "my name",
        "long_name": "my long_name",
        "square_kms":  1000,
        "parent_level":  None,
        "parent_code":  None,
        "province_name": "pr",
        "province_code": "prov",
        "category": "my",
        "miif_category": "my miff_category",
        "population":  2000,
    },

    "child_map": {
       "geo_level":"my geo_levels2",
       "geo_code": "my codes2",
       "name": "my names2",
       "long_name": "my long_names2",
       "square_kms":  1000,
       "parent_level":  None,
       "parent_code":  None,
       "province_name": "my provinces2",
       "province_code": "pr2",
       "category": "m2",
       "miif_category": "my miff_categorys2",
       "population":  2000,
    }
}


class TestGeographies(TestCase):

    def test_geography(self):

        parent_geography = models.Geography.objects.create(**fixtures["parent_map"])
        child_geography = models.Geography.objects.create(**fixtures["child_map"])

        js_parent = serializers.GeographySerializer(parent_geography, context={"request": None}).data
        js_child = serializers.GeographySerializer(child_geography, context={"request": None}).data

        coords = [cpt_coords[x] for x in ["min_lon", "min_lat", "max_lon", "max_lat"]]
        parent_json = dict(fixtures["parent_map"], bbox=coords)

        self.assertDictEqual(parent_json, js_parent)
        self.assertEquals(fixtures["child_map"], js_child)

class TestBoundingBoxes(TestCase):
    @mock.patch('requests.get', side_effect=request_mock(cpt_coords))
    def test_fake_request(self, mock_get):
        muni = fixtures["parent_map"]
        muni["geo_code"] = "CPT"

        geography = models.Geography.objects.create(**muni)
        bbox = geography.bbox
        coords = [cpt_coords[x] for x in ["min_lon", "min_lat", "max_lon", "max_lat"]]
        self.assertEquals(coords, bbox)

    def test_request(self):
        muni = fixtures["parent_map"]
        muni["geo_code"] = "CPT"

        geography = models.Geography.objects.create(**muni)
        bbox = geography.bbox
        coords = [cpt_coords[x] for x in ["min_lon", "min_lat", "max_lon", "max_lat"]]
        self.assertEquals(coords, bbox)
