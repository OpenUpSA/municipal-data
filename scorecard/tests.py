from django.test import TestCase
import json
from . import models, serializers

class TestSerializers(TestCase):
    @classmethod
    def setUp(cls):
        pass
        #cls.geography = Geography.objects.create(
        #    geo_level="X",
        #    geo_code="geo_code",
        #    province_name="Western Cape",
        #    province_code="WC",
        #    category="A",
        #)

    def test_geography(self):
        parent_map = {
           "geo_level":"my geo_level",
           "geo_code": "my code",
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
        }

        child_map = {
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

        parent_geography = models.Geography.objects.create(**parent_map)
        child_geography = models.Geography.objects.create(**child_map)

        js_parent = serializers.GeographySerializer(parent_geography, context={"request": None}).data
        js_child = serializers.GeographySerializer(child_geography, context={"request": None}).data
        
        self.assertEquals(parent_map, js_parent)
        self.assertEquals(child_map, js_child)
